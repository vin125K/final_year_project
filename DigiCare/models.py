from django.db import models
from django.contrib.auth.hashers import check_password as auth_check_password
from django.contrib.auth.hashers import check_password as auth_check_password, make_password
from django.contrib.auth.models import AbstractUser

class PrescriptionForm(models.Model):
    doctorUserName = models.CharField(max_length=100)
    patientUserName = models.CharField(max_length=100)
    patientName = models.CharField(max_length=100)
    symptoms = models.TextField()
    medicines = models.TextField()
    diet = models.TextField()
    tests = models.TextField()
    description = models.TextField(blank=True)

    # You can add more fields as needed

    # Optionally, you can add a timestamp field to track when the form was submitted
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patientName  # Or any other meaningful representation



class Patient(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    visual_verification = models.CharField(max_length=255)  # New field for visual verification

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return auth_check_password(raw_password, self.password)


class HeartRate(models.Model):
    username = models.CharField(max_length=150)  # Assuming username length won't exceed 150 characters
    heart_rate = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username       


