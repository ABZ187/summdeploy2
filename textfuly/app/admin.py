from django.contrib import admin
from .models import ColdCoffee, Subscription, NewsLetter, ScheduleMail, Profile

admin.site.register(NewsLetter)
admin.site.register(ScheduleMail)


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id', 'token', 'user', 'verify']


@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ['id', 'email', 'order_id', 'razorpay_payment_id', 'paid']


@admin.register(ColdCoffee)
class ColdCoffee(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'amount', 'paid']