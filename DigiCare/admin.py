from django.contrib import admin

# Register your models here.
from .models import PrescriptionForm
from .models import Patient
from .models import HeartRate

admin.site.register(PrescriptionForm)
admin.site.register(Patient)
admin.site.register(HeartRate)