import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import OTPVerification

def generate_and_send_otp(user):
    otp_code = ''.join(random.choices('0123456789', k=6))
    expires_at = timezone.now() + timedelta(minutes=10) # OTP valid for 10 minutes

    # Delete any existing OTPs for the user
    OTPVerification.objects.filter(user=user).delete()

    # Save new OTP
    OTPVerification.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)

    subject = 'Your OTP for Registration'
    message = f'Hi {user.username},\n\nYour One-Time Password (OTP) for registration is: {otp_code}\n\nThis OTP is valid for 10 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL # You need to set DEFAULT_FROM_EMAIL in settings.py
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)