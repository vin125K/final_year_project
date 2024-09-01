from django.contrib.auth.backends import BaseBackend
from .models import Patient

class PatientAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        print("Authenticating user:", username)
        try:
            patient = Patient.objects.get(username=username)
            if patient.check_password(password):
                print("Authentication successful for user:", username)
                return patient
        except Patient.DoesNotExist:
            print("User not found:", username)

        return None
