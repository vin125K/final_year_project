from django.apps import AppConfig
from django.core.signals import request_started  # Corrected import
from django.db.models.signals import pre_save

# Import the logging module
import logging

# Get a logger instance
logger = logging.getLogger(__name__)

# Define the signal handler function
def start_heart_rate_update_script(sender, **kwargs):
    # Log a message indicating that the signal handler function is triggered
    logger.info("Start heart rate update script triggered")
    
    # Import call_command here to avoid circular import issues
    from django.core.management import call_command
    
    # Call your management command
    call_command('update_heart_rate')


class YourAppConfig(AppConfig):
    name = 'DigiCare'

    def ready(self):
        request_started.connect(start_heart_rate_update_script)


        