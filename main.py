from google.cloud import secretmanager
import gspread
from datetime import datetime
import json
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def get_secret(project_id, secret_id, service_account):
    """
    Retrieves secret values from Google Secret Manager.
    """
    try:
        client = secretmanager.SecretManagerServiceClient.from_service_account_file(service_account)
        secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": secret_name})
        secret_values = json.loads(response.payload.data.decode("UTF-8"))
        return secret_values
    except Exception as e:
        print(f"Error occurred while retrieving secret: {str(e)}")
        return None

def check_and_send_leads(service_account, email, password, store_id):
    """
    Checks the leads spreadsheet for new entries and sends them in ADF format via email.
    """
    gc = gspread.service_account(filename=service_account)
    spreadsheet = gc.open_by_key('your-spreadsheet-key')
    worksheet = spreadsheet.worksheet('Leads')
    data = worksheet.get_all_records()

    processed_leads = set()

    for lead in data:
        if lead['Store'] == store_id and not is_valid_timestamp(lead.get('Sent Status', '').strip()) and (lead['Entry ID'] not in processed_leads):
            try:
                xml_data = create_lead_xml(lead)
                send_adf_email(xml_data, email, password)

                current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                update_sent_status(worksheet, lead, current_timestamp)

                processed_leads.add(lead['Entry ID'])
            except Exception as e:
                print(f"Error processing lead {lead['Entry ID']}: {str(e)}")

def update_sent_status(worksheet, lead, status):
    """
    Updates the 'Sent Status' of the lead in the worksheet.
    """
    row_number = lead['Entry ID']
    worksheet.update_cell(row_number + 2, worksheet.find('Sent Status').col, status)

def is_valid_timestamp(timestamp):
    """
    Validates the timestamp format.
    """
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def create_lead_xml(lead):
    """
    Converts the lead data into ADF XML format.
    """
    adf_root = ET.Element("adf")
    adf_entry = ET.SubElement(adf_root, "prospect")
    request_date = ET.SubElement(adf_entry, "requestdate")
    request_date.text = format_request_date(lead['Entry Date'])

    vehicle = ET.SubElement(adf_entry, "vehicle")
    vehicle.set("interest", "buy")
    ET.SubElement(vehicle, "make").text = "Your Vehicle Make"
    options = lead['Options'].split(',')
    model_name = options[0].strip() if options else ''
    ET.SubElement(vehicle, "model").text = model_name

    customer = ET.SubElement(adf_entry, "customer")
    contact = ET.SubElement(customer, "contact")
    ET.SubElement(contact, "name", part="first").text = lead.get('First Name', '')
    ET.SubElement(contact, "name", part="last").text = lead.get('Last Name', '')
    ET.SubElement(contact, "email").text = lead['Email']
    ET.SubElement(contact, "phone").text = lead['Phone']
    address = ET.SubElement(contact, "address")
    ET.SubElement(address, "postalcode").text = lead['Zip Code']

    provider = ET.SubElement(adf_entry, "provider")
    ET.SubElement(provider, "name").text = "Your Provider Name"

    adf_xml = ET.tostring(adf_root, encoding="utf-8", method="xml").decode("utf-8")
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<?adf version="1.0"?>\n{adf_xml}'

def format_request_date(request_date):
    """
    Formats the request date into the desired format.
    """
    try:
        return datetime.strptime(request_date, "%m/%d/%Y").strftime("%Y-%m-%dT%H:%M:%S%z")
    except ValueError as e:
        print(f"Error formatting request date: {str(e)}")
        return None

def send_adf_email(xml_data, email, password):
    """
    Sends an email with the ADF XML data.
    """
    sender_email = email
    receiver_email = "receiver@example.com"
    subject = "New Lead Submission"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(xml_data, "plain"))

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    project_id = 'your-google-cloud-project-id'
    secret_id = 'your-secret-id'
    store_id = 'your-store-id'

    secret_values = get_secret(project_id, secret_id, '/path/to/your/service-account-file.json')

    if secret_values:
        check_and_send_leads('/path/to/your/service-account-file.json', secret_values['email'], secret_values['password'], store_id)
