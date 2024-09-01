"""
WSGI config for Final_Year_Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'Final_Year_Project.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'Final_Year_Project.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_module')

application = get_wsgi_application()
