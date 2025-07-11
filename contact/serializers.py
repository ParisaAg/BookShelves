# extra/serializers.py
from .models import ContactMessage
from rest_framework import serializers


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']