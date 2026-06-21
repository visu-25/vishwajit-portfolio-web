import json
import logging
import threading
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import send_mail
from django.db import close_old_connections
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _build_notification_content(contact_message):
    recipient = settings.CONTACT_NOTIFICATION_EMAIL
    subject = f"Portfolio contact: {contact_message.name}"
    context = {
        "contact": contact_message,
        "site_url": getattr(settings, "SITE_URL", "").rstrip("/"),
    }
    message = render_to_string("emails/contact_notification.txt", context)
    return recipient, subject, message


def _send_via_smtp(recipient, subject, message) -> bool:
    sent = send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )
    return sent > 0


def _send_via_resend(recipient, subject, message) -> bool:
    api_key = getattr(settings, "RESEND_API_KEY", "")
    if not api_key:
        return False

    payload = json.dumps(
        {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [recipient],
            "subject": subject,
            "text": message,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return 200 <= response.status < 300


def send_contact_notification(contact_message) -> bool:
    """Email the site owner when a visitor submits the contact form."""
    recipient, subject, message = _build_notification_content(contact_message)

    try:
        if getattr(settings, "RESEND_API_KEY", ""):
            return _send_via_resend(recipient, subject, message)
        return _send_via_smtp(recipient, subject, message)
    except Exception:
        logger.exception(
            "Failed to send contact notification for message id=%s",
            contact_message.pk,
        )
        return False


def _send_in_background(contact_id: int) -> None:
    close_old_connections()
    try:
        from core.models import ContactMessage

        contact = ContactMessage.objects.get(pk=contact_id)
        send_contact_notification(contact)
    except Exception:
        logger.exception("Background contact email failed for id=%s", contact_id)
    finally:
        close_old_connections()


def send_contact_notification_async(contact_message) -> None:
    """Send notification in a background thread so the HTTP response is not blocked."""
    threading.Thread(
        target=_send_in_background,
        args=(contact_message.pk,),
        daemon=True,
    ).start()
