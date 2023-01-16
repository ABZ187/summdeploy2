import markdown2 as markdown2
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)


class ColdCoffee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)


class Subscription(models.Model):
    email = models.EmailField(max_length=100)
    amount = 299
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)


class NewsLetter(models.Model):
    mail = models.EmailField(
        max_length=100,
        verbose_name='User\'s Email',
        unique=True
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mail


class ScheduleMail(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Email\' Subject')
    message = models.TextField(
        max_length=3000,
        verbose_name='Markdown\'s Content'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

    @property
    def html_content(self):
        markdown = markdown2.Markdown()
        return markdown.convert(self.message)
