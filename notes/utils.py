from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_comment_notification(sender, receiver, note_url, comment):
    subject = f'{sender}: Left a comment to your note - "{comment.note}"'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiver.email]

    html_message = render_to_string(
        "email_templates/new_comment.html",
        {
            "sender": sender,
            "title": comment.note,
            "note_url": note_url,
            "comment": comment,
        },
    )

    send_mail(subject, None, email_from, recipient_list, html_message=html_message)
