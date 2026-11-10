
from django.db import models
from django.conf import settings


class County(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Counties'

class Town(models.Model):
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name='towns'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.county.name}"

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['county', 'name'],
                name='unique_town_per_county'
            )
        ]


class Neighbourhood(models.Model):
    town = models.ForeignKey(
        Town,
        on_delete=models.CASCADE,
        related_name='neighbourhoods'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.town.name}"

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['town', 'name'],
                name='unique_neighbourhood_per_town'
            )
        ]


class LocationSuggestion(models.Model):

    class LocationType(models.TextChoices):
        TOWN = 'town', 'Town'
        NEIGHBOURHOOD = 'neighbourhood', 'Neighbourhood'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    location_type = models.CharField(
        max_length=20,
        choices=LocationType.choices
    )

    name = models.CharField(max_length=100)

    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name='location_suggestions'
    )

    town = models.ForeignKey(
        Town,
        on_delete=models.CASCADE,
        related_name='location_suggestions',
        null=True,
        blank=True
    )

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='location_suggestions'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
