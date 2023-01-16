from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('paraphraser', views.paraphraser, name='paraphraser'),
    path('downloadPdf', views.downloadPdf, name='downloadPdf'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('words', views.counter, name='counter'),
    path('payment', views.coffee_payment, name='payment'),
    path('payment-status', views.payment_status, name='payment-status'),
    path('subscription', views.get_subscription, name='subscription'),
    path('subscription-status', views.subscription_status, name='subscription-status'),
    path('get-premium', views.get_premium, name='get-premium'),
    # path('audio', views.create_audio, name='create_audio'),
    # path('stop_audio', views.stop_audio, name='stop_audio'),
    path('account-verification/<slug:token>', views.verify_email, name='account-verification')
]