from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_reply_notification(sender, receiver, post_url, reply):
    subject = f'{sender}: Replied to your post - "{reply.post}"'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiver.email]

    html_message = render_to_string(
        "email_templates/new_reply.html",
        {
            "sender": sender,
            "title": reply.post,
            "post_url": post_url,
            "reply": reply,
        },
    )

    send_mail(subject, None, email_from, recipient_list, html_message=html_message)
