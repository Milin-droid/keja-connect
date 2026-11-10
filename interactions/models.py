
from django.conf import settings
from django.db import models
from listings.models import Property


class Enquiry(models.Model):

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        READ = 'read', 'Read'
        RESPONDED = 'responded', 'Responded'
        CLOSED = 'closed', 'Closed'

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    message = models.TextField()

    contact_phone = models.CharField(
        max_length=20,
        help_text="Phone number where the landlord can reach you."
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry for {self.property.title} by {self.seeker.username}"

    class Meta:
        ordering = ['-created_at']
