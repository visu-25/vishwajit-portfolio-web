import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_contact_notification(contact_message) -> bool:
    """Email the site owner when a visitor submits the contact form."""
    recipient = settings.CONTACT_NOTIFICATION_EMAIL
    subject = f"Portfolio contact: {contact_message.name}"
    context = {
        "contact": contact_message,
        "site_url": getattr(settings, "SITE_URL", "").rstrip("/"),
    }
    message = render_to_string("emails/contact_notification.txt", context)

    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        return sent > 0
    except Exception:
        logger.exception(
            "Failed to send contact notification for message id=%s",
            contact_message.pk,
        )
        return False
