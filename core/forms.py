import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import ContactMessage

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]*[a-zA-Z0-9])?"
    r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your name",
                    "autocomplete": "name",
                    "required": True,
                    "minlength": "2",
                    "maxlength": "120",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                    "type": "email",
                    "required": True,
                    "inputmode": "email",
                    "maxlength": "254",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-input form-textarea",
                    "placeholder": "Tell me about your project or opportunity...",
                    "rows": 5,
                    "required": True,
                    "minlength": "10",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise ValidationError("Please enter your full name (at least 2 characters).")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        validate_email(email)
        if not EMAIL_PATTERN.match(email):
            raise ValidationError("Please enter a valid email address (e.g. you@example.com).")
        return email

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise ValidationError("Please enter a message with at least 10 characters.")
        return message
