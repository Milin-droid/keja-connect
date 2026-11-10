
from django.conf import settings
from django.db import models
from locations.models import County, Town, Neighbourhood


class Property(models.Model):

    class Category(models.TextChoices):
        RESIDENTIAL = 'residential', 'Residential'
        COMMERCIAL = 'commercial', 'Commercial'

    class PropertyType(models.TextChoices):
        # Residential
        SINGLE_ROOM = 'single_room', 'Single Room'
        BEDSITTER = 'bedsitter', 'Bedsitter'
        STUDIO = 'studio', 'Studio'
        APARTMENT = 'apartment', 'Apartment'
        HOUSE = 'house', 'House'
        MAISONETTE = 'maisonette', 'Maisonette'
        BUNGALOW = 'bungalow', 'Bungalow'
        TOWNHOUSE = 'townhouse', 'Townhouse'
        SHARED = 'shared', 'Shared Accommodation'

        # Commercial
        SHOP = 'shop', 'Shop'
        OFFICE = 'office', 'Office'
        RETAIL_SPACE = 'retail_space', 'Retail Space'
        WAREHOUSE = 'warehouse', 'Warehouse'
        COMMERCIAL_BUILDING = 'commercial_building', 'Commercial Building'

        OTHER = 'other', 'Other'

    class Availability(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        RESERVED = 'reserved', 'Reserved'
        OCCUPIED = 'occupied', 'Occupied'

    class ListingStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Review'
        PUBLISHED = 'published', 'Published'
        REJECTED = 'rejected', 'Rejected'

    # Landlord who owns this listing
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    # Basic information
    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )
    property_type = models.CharField(
        max_length=30,
        choices=PropertyType.choices
    )
    description = models.TextField()

    # Location
    county = models.ForeignKey(
        County,
        on_delete=models.PROTECT,
        related_name='properties'
    )
    town = models.ForeignKey(
        Town,
        on_delete=models.PROTECT,
        related_name='properties'
    )
    neighbourhood = models.ForeignKey(
        Neighbourhood,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )

    # Property details
    bedrooms = models.PositiveSmallIntegerField(
        null=True, blank=True
    )
    bathrooms = models.PositiveSmallIntegerField(
        null=True, blank=True
    )
    floor_area_sq_m = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Costs in Kenyan shillings
    monthly_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    security_deposit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    agency_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    other_charges = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Listing status
    availability = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE
    )
    listing_status = models.CharField(
        max_length=20,
        choices=ListingStatus.choices,
        default=ListingStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_move_in_cost(self):
        return (
            self.monthly_rent
            + self.security_deposit
            + self.agency_fee
            + self.other_charges
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='properties/'
    )

    is_primary = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            PropertyImage.objects.filter(
                property=self.property,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.property.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['property'],
                condition=models.Q(is_primary=True),
                name='one_primary_image_per_property'
            )
        ]
