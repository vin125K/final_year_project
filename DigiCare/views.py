from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import PrescriptionForm
from .models import Patient, HeartRate
from .auth_backends import PatientAuthBackend
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Patient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import base64
import re
from googleapiclient.discovery import build
from django.conf import settings


import random
from googleapiclient.discovery import build
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def home(request):
    return render(request,'DigiCare/Home.html')





def patientsignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        visualVerification = request.POST.get('visualVerification')

        if password != confirm_password:
            return render(request, 'patient_signup.html', {'error': 'Passwords do not match'})
        
        # Hash the password
        hashed_password = make_password(password)
        
        # Create a new patient record with hashed password
        patient = Patient.objects.create(username=username, email=email, phone=phone, password=hashed_password, visual_verification=visualVerification)
        
        # Redirect to the login page upon successful registration
        return redirect('patient_login')

    return render(request, 'DigiCare/patient_signup.html')



# Function to generate OTP
def generate_otp_code():
    return str(random.randint(100000, 999999))

# Function to authenticate with Google API
def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'path_to_your_credentials.json', SCOPES)
            print("Redirect URI:", flow.redirect_uri)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Function to send email using Gmail API
def send_email(subject, message_body, recipient_email):
    credentials = authenticate_google()
    service = build('gmail', 'v1', credentials=credentials)
    message = create_message(subject, message_body, recipient_email)
    send_message(service, 'me', message)

# Function to create message for sending email
def create_message(subject, message_body, recipient_email):
    message = f'From: {settings.EMAIL_HOST_USER}\n'
    message += f'To: {recipient_email}\n'
    message += f'Subject: {subject}\n\n'
    message += message_body
    return {'raw': base64.urlsafe_b64encode(message.encode()).decode()}

# Function to send message using Gmail API
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)

# View to handle patient login and OTP generation
def patientlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        visual_verification = request.POST.get('visualVerification')  # Retrieve visual verification from the form
        
        try:
            user = Patient.objects.get(username=username)
        except Patient.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('patient_login')
        
        # Check if the entered password is correct
        if user.check_password(password) and user.visual_verification == visual_verification:  # Check visual verification
            # Generate OTP
            otp = generate_otp_code()
            
            # Send OTP to user's email using Gmail API
            subject = 'Your OTP for login'
            message_body = f'Your OTP is: {otp}'
            recipient_email = user.email
            send_email(subject, message_body, recipient_email)
            
            # Store OTP in session
            request.session['otp'] = otp
            request.session['username'] = username  # Store username in session
            
            # Redirect to OTP verification page
            return redirect('verify_otp')
        else:
            messages.error(request, 'Invalid username, password, or visual verification.')  # Inform user about invalid input
    
    return render(request, 'DigiCare/patient_login.html')




# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Patient
from django.contrib import messages

# View to handle OTP verification
# View to handle OTP verification
# View to handle OTP verification
def verify_otp(request):
    if request.method == 'POST':
        # Retrieve the entered OTP from the form
        entered_otp = request.POST.get('otp')

        # Retrieve the OTP stored in the session
        if 'otp' in request.session:
            stored_otp = request.session['otp']
            print("Stored OTP:", stored_otp)  # Debug message

            # Compare the entered OTP with the stored OTP
            if entered_otp == stored_otp:

                    print("User logged in successfully")  # Debug message
                    # Redirect to the dashboard or any desired page
                    return redirect('patient_dashboard')  # Redirect to dashboard upon successful login
              
            else:
                # Entered OTP does not match stored OTP
                messages.error(request, 'Invalid OTP. Please try again.')
                print("Invalid OTP")  # Debug message
        else:
            # OTP not found in session
            messages.error(request, 'OTP not found in session.')
            print("OTP not found in session")  # Debug message
    
    # Render the OTP verification page
    return render(request, 'DigiCare/verify_otp.html')

def patientdashboard(request):
    username = request.session.get('username')
    if username:
        user = Patient.objects.get(username=username)
        # Fetch all PrescriptionForms related to the logged-in patient
        prescription_forms = PrescriptionForm.objects.filter(patientUserName=user.username)
        heart_rate_data = HeartRate.objects.filter(username=username)
        
        print("rateee", heart_rate_data)
        return render(request, 'DigiCare/patient_dashboard.html', {'user': user, 'prescription_forms': prescription_forms,  'heart_rate_data': heart_rate_data})
    else:
        # Redirect to login page if username is not found in session
        return redirect('patient_login')















def Dform(request):
    if request.method == 'POST':
        # Handle form submission and save data to database
        doctorUserName = request.POST.get('doctorUserName')
        patientUserName = request.POST.get('patientUserName')
        patientName = request.POST.get('patientName')
        symptoms = request.POST.get('symptoms')
        medicines = request.POST.get('medicines')
        diet = request.POST.get('diet')
        tests = request.POST.get('tests')
        description = request.POST.get('description')

        # Save form data to database
        form = PrescriptionForm(doctorUserName=doctorUserName,
                                patientUserName=patientUserName,
                                patientName=patientName,
                                symptoms=symptoms,
                                medicines=medicines,
                                diet=diet,
                                tests=tests,
                                description=description)
        form.save()

        # Redirect back to the doctor view
        return redirect('doctor')

    # Fetch all submitted forms from the database
    forms = PrescriptionForm.objects.all()
    
    return render(request, 'DigiCare/Dform.html', {'forms': forms})

from django.contrib.auth.decorators import login_required

@login_required  # Ensures only logged-in users can access this view
def doctor(request):
    # Fetch forms related to the currently logged-in doctor
    forms = PrescriptionForm.objects.filter(doctorUserName=request.user.username)
    return render(request, 'DigiCare/doctor.html', {'forms': forms})

def doctorlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            login(request, user)
            # Redirect to Dform.html upon successful login
            return redirect('doctor')  # Using the correct URL pattern name
        else:
            # Handle login failure
            messages.error(request, 'Invalid username or password.')

    return render(request, 'DigiCare/doctor_login.html')

def doctorsignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        # Check if passwords match
        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'DigiCare/doctor_signup.html', {'error': 'Passwords do not match'})
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        
        # Optionally, you can save additional user details to a custom profile model
        
        # Redirect to login page
        return redirect('doctor_login')  # Use the URL pattern name, not the file path

    return render(request, 'DigiCare/doctor_signup.html')
    

# Create your views here.
# Add the user_logged_in signal handler
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # Redirect the user to their dashboard after successful login
    return redirect('patient_dashboard')