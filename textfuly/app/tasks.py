from celery import shared_task

from django.core.mail import send_mail

from django.conf import settings

from .models import ScheduleMail, NewsLetter



@shared_task(name="send_scheduled_mails")
def send_scheduled_mails():
    mail = ScheduleMail.objects.all().first()

    send_mail(
        subject=mail.subject,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[_.mail for _ in NewsLetter.objects.all()],
        message=mail.message,
        fail_silently=True,
        html_message=mail.html_content
    )

    print("Running send_scheduled mail")
