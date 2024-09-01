from django.urls import path
from django.http import HttpResponse
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home),
    
    path('Dform/',views.Dform,name='Dform'),
    path('doctorlogin/', views.doctorlogin, name='doctor_login'),
    path('doctorsignup/', views.doctorsignup, name='doctor_signup'),
    path('doctor/', views.doctor, name='doctor'),
    path('patientsignup/', views.patientsignup, name='patient_signup'),
    path('patientlogin/', views.patientlogin, name='patient_login'),
    path('patientdashboard/', views.patientdashboard, name='patient_dashboard'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
