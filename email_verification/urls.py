from django.urls import path
from . import views

app_name = 'email_verification'

urlpatterns = [
    path('verify/', views.verify_email, name='verify_email'),
    path('resend/', views.resend_verification_code, name='resend_code'),
]
