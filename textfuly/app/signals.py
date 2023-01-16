from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.template.loader import render_to_string
from .models import NewsLetter
from .tasks import send_async_mail
from .models import (
    generate_unsub_url,
    encrypt_email
)


@receiver(post_save, sender=NewsLetter)
def send_confirmation_mail(sender, instance, **kwargs):
    print("POST_SAVE signal firing")

    unsub_url = generate_unsub_url(encrypt_email(instance.mail))

    message = render_to_string(
        'subscribe.html',
        {
            'email': instance.mail,
            'unsubscribe_url': unsub_url
        }
    )

    send_async_mail.delay(
        subject=f"Thanks for subscribing",
        emails=[instance.mail],
        text_msg="Thanks for joining",
        html_msg=message
    )


@receiver(post_delete, sender=NewsLetter)
def send_unsubscribe_mail(sender, instance, **kwargs):
    print("POST DELETE signal firing")

    message = render_to_string(
        'unsubscribe.html',
        {
            'email': instance.mail,
        }
    )

    send_async_mail.delay(
        subject=f"We'll miss you",
        emails=[instance.mail],
        text_msg="We'll miss you",
        html_msg=message
    )
