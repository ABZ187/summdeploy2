from django.db import models
from django.db.models import fields

from rest_framework.serializers import ModelSerializer
from .models import NewsLetter


class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = '__all__'
