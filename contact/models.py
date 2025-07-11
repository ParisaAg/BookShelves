from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="sender name")
    email = models.EmailField(verbose_name="sender email")
    subject = models.CharField(max_length=255, verbose_name="subject")
    message = models.TextField(verbose_name="message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    is_read = models.BooleanField(default=False, verbose_name="is read?")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "contact message"
        verbose_name_plural = "contact messages"

    def __str__(self):
        return f'Message from {self.name} on {self.subject}'