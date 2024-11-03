from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_update_account_notification(user):
    subject = "Security Notification: Account Update Alert"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    html_message = render_to_string(
        "email_templates/update_account_notification.html",
        {
            "user_email": user.email,
            "user_name": user.username,
        },
    )

    send_mail(subject, None, email_from, recipient_list, html_message=html_message)
