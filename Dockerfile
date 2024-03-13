# Use a smaller base image, e.g., python:3.10-slim-buster
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user with an explicit UID
RUN adduser -u 5678 --disabled-password --gecos "" appuser

# Change ownership of the app directory to the non-root user
RUN chown -R appuser /app

# Switch to the non-root user
USER appuser

# Specify the command to run the application
CMD ["python", "main.py"]