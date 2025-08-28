import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import secrets
import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPVerification

logger = logging.getLogger(__name__)

def generate_and_send_otp(user, length: int = 6, ttl_minutes: int = 5, min_seconds_between_sends: int = 60):
    """
    Generate an OTP, save it to OTPVerification, and send it via email.
    Raises ValueError for bad input, Exception for send failure or rate-limit.
    Returns the otp_code (useful for tests) or raises on failure.
    """
    # basic validation
    if not user or not getattr(user, "email", None):
        raise ValueError("User must exist and have an email address.")

    # ensure user is persisted
    if user.pk is None:
        user.save()

    now = timezone.now()

    # simple rate-limit: disallow repeated sends within min_seconds_between_sends
    last = OTPVerification.objects.filter(user=user).order_by("-created_at").first()
    if last and (now - last.created_at).total_seconds() < min_seconds_between_sends:
        raise Exception("OTP was recently sent. Please wait a moment before requesting another.")

    # generate secure numeric OTP
    otp_code = f"{secrets.randbelow(10 ** length):0{length}d}"  # e.g. '004321'

    expires_at = now + timedelta(minutes=ttl_minutes)

    # remove old OTPs (or you can keep history if desired)
    OTPVerification.objects.filter(user=user).delete()

    # create new OTP object
    otp_obj = OTPVerification.objects.create(user=user, otp_code=otp_code, expires_at=expires_at)

    subject = "Your OTP for Registration"
    message = (
        f"Hi {getattr(user, 'username', '')},\n\n"
        f"Your One-Time Password (OTP) is: {otp_code}\n\n"
        f"This code will expire in {ttl_minutes} minutes.\n\n"
        "If you didn't request this, please ignore this email."
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as exc:
        logger.exception("Failed to send OTP email to %s", user.email)
        # cleanup OTP if email didn't send
        OTPVerification.objects.filter(pk=otp_obj.pk).delete()
        raise

    return otp_code
#  Could not send OTP email: column feedback_otpverification.attempts does not exist LINE 1: ...ted_at", "feedback_otpverification"."expires_at", "feedback_... ^