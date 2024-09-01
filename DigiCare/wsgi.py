import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MedTech_Hackathon.settings')

application = get_wsgi_application()
