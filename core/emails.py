import json
import logging
import os
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
    text_body = render_to_string("emails/contact_notification.txt", context).strip()
    html_body = render_to_string("emails/contact_notification.html", context).strip()
    return recipient, subject, text_body, html_body


def _send_via_smtp(recipient, subject, text_body) -> bool:
    sent = send_mail(
        subject=subject,
        message=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )
    return sent > 0


def _get_resend_from_email() -> str:
    return getattr(
        settings,
        "RESEND_FROM_EMAIL",
        "Portfolio <onboarding@resend.dev>",
    )


def _send_via_resend(recipient, subject, text_body, html_body, reply_to=None) -> bool:
    api_key = getattr(settings, "RESEND_API_KEY", "")
    if not api_key:
        return False

    if not text_body and not html_body:
        logger.error("Refusing to send empty contact notification email")
        return False

    payload_dict = {
        "from": _get_resend_from_email(),
        "to": [recipient],
        "subject": subject,
        "text": text_body,
        "html": html_body,
    }
    if reply_to:
        payload_dict["reply_to"] = [reply_to]

    payload = json.dumps(payload_dict).encode("utf-8")
    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": getattr(
                settings,
                "RESEND_USER_AGENT",
                "vishwajit-portfolio/1.0",
            ),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response_body = json.loads(response.read().decode("utf-8"))
            logger.info(
                "Resend email accepted id=%s to=%s text_len=%s html_len=%s",
                response_body.get("id"),
                recipient,
                len(text_body),
                len(html_body),
            )
            return True
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        logger.error(
            "Resend API error %s for recipient %s (from=%s): %s",
            exc.code,
            recipient,
            payload_dict["from"],
            body,
        )
        if exc.code == 403 and "1010" in body:
            logger.error(
                "Resend blocked the request (error 1010). Ensure User-Agent is set "
                "on API requests — this is required by Resend/Cloudflare."
            )
        elif exc.code == 403 and "resend.dev" in payload_dict["from"]:
            logger.error(
                "Resend test domain only delivers to your Resend account email. "
                "Set CONTACT_NOTIFICATION_EMAIL to that address, or verify a domain "
                "at https://resend.com/domains and set RESEND_FROM_EMAIL."
            )
        raise


def send_contact_notification(contact_message) -> bool:
    """Email the site owner when a visitor submits the contact form."""
    recipient, subject, text_body, html_body = _build_notification_content(contact_message)

    try:
        if getattr(settings, "RESEND_API_KEY", ""):
            return _send_via_resend(
                recipient,
                subject,
                text_body,
                html_body,
                reply_to=contact_message.email,
            )
        return _send_via_smtp(recipient, subject, text_body)
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
    """Send notification without blocking the HTTP response on long-running hosts."""
    if os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"):
        # Serverless functions may terminate before daemon threads finish.
        send_contact_notification(contact_message)
        return

    threading.Thread(
        target=_send_in_background,
        args=(contact_message.pk,),
        daemon=True,
    ).start()
