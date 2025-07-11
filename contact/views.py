from django.shortcuts import render
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings


class ContactMessageView(generics.CreateAPIView):

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [] 

    def perform_create(self, serializer):
        contact_message = serializer.save()
        subject = f"New Contact Us Message: {contact_message.subject}"
        message_body = f"""
        You have a new message from:
        Name: {contact_message.name}
        Email: {contact_message.email}
        
        Message:
        {contact_message.message}
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL] 

        try:
            send_mail(subject, message_body, from_email, recipient_list)
        except Exception as e:
            print(f"Could not send email: {e}")