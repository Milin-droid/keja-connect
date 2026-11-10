from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        SEEKER = 'seeker', 'House Seeker'
        ADVERTISER = 'advertiser', 'Property Advertiser'
        BOTH = 'both', 'Seeker and Advertiser'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SEEKER
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.username