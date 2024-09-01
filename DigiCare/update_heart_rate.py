import os
import sys
import time
import random
import base64
import logging
import django
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.core.management.base import BaseCommand


# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Final_Year_Project.settings')
django.setup()

from DigiCare.models import HeartRate, Patient

# Set up logging
logging.basicConfig(filename='update_heart_rate.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'path_to_your_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_alert_email(subject, message_body, recipient_email):
    creds = authenticate_google()
    service = build('gmail', 'v1', credentials=creds)
    message = create_message(subject, message_body, recipient_email)
    try:
        service.users().messages().send(userId='me', body=message).execute()
        logger.info(f'Alert email sent to {recipient_email}')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

def create_message(subject, message_body, recipient_email):
    message = f'From: your_email@example.com\n'  # Replace with your email
    message += f'To: {recipient_email}\n'
    message += f'Subject: {subject}\n\n'
    message += message_body
    raw_message = base64.urlsafe_b64encode(message.encode()).decode()
    return {'raw': raw_message}

def main():
    logger.info("Heart rate update script started.")
    while True:
        try:
            # Generate random heart rate
            heart_rate = random.randint(55, 100)
            username = 'chetan'  # Replace with the actual username

            # Check if the user exists and update or create the entry
            existing_entry = HeartRate.objects.filter(username=username).first()
            if existing_entry:
                existing_entry.heart_rate = heart_rate
                existing_entry.save()
                logger.info(f"Heart rate updated for user '{username}': {heart_rate} bpm")
            else:
                HeartRate.objects.create(username=username, heart_rate=heart_rate)
                logger.info(f"New heart rate entry created for user '{username}': {heart_rate} bpm")

            # Check heart rate and send alert if below threshold
            if heart_rate < 60:
                try:
                    patient = Patient.objects.get(username=username)
                    recipient_email = patient.email
                    subject = "Low Heart Rate Alert"
                    message_body = f"Your heart rate is {heart_rate} bpm, which is lower than the normal range. Please consult your physician."
                    send_alert_email(subject, message_body, recipient_email)
                except Patient.DoesNotExist:
                    logger.error(f'Patient with username {username} not found')

            time.sleep(3)  # Wait for 3 seconds before the next update

        except Exception as e:
            logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
