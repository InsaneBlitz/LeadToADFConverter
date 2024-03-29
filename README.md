# LeadToADFConverter

Transforms leads captured via web forms into ADF (Auto-lead Data Format) XML for seamless integration into automotive CRMs. `LeadToADFConverter` automates the retrieval of lead data from Google Spreadsheets, generated by website forms, and converts this information into the industry-standard ADF XML format. This script is designed for businesses looking to streamline their lead management process, ensuring quick and efficient transfer of potential customer data to their dealership management systems. Ideal for auto dealerships and digital marketing professionals in the automotive industry.

## Features

- **Automated Lead Retrieval**: Fetches new lead data from a specified Google Spreadsheet automatically.
- **ADF XML Conversion**: Converts lead data into ADF XML format, ready for import into automotive CRM systems.
- **Email Integration**: Sends the generated ADF XML to specified recipients, facilitating immediate follow-up.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/InsaneBlitz/LeadToADFConverter.git
   ```

2. **Install Required Libraries**:
   Navigate to the repository directory and install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- Update the `PROJECT_ID`, `SECRET_ID`, and `service_account` variables in the script with your Google Cloud and Spreadsheet details.
- Customize the email sending function `sendADFEmail` with your SMTP server settings.

## Usage

Execute the script with Python to start processing leads:
```bash
python LeadToADFConverter.py
```

Follow the on-screen prompts or configure the script to run at scheduled intervals for continuous lead processing.

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.

## About the Author

This script was created by Alexis, a passionate developer known on GitHub as [InsaneBlitz](https://github.com/InsaneBlitz). Alexis is dedicated to creating solutions that streamline and automate business processes.
