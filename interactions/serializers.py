
from rest_framework import serializers
from listings.models import Property
from .models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):

    # Keep this required in API submissions even though the migration uses
    # a temporary blank value to preserve existing enquiry rows.
    contact_phone = serializers.CharField(max_length=20, required=True)

    seeker = serializers.ReadOnlyField(
        source='seeker.username'
    )

    property_title = serializers.ReadOnlyField(
        source='property.title'
    )

    class Meta:
        model = Enquiry

        fields = [
            'id',
            'property',
            'property_title',
            'seeker',
            'message',
            'contact_phone',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'seeker',
            'property_title',
            'status',
            'created_at',
            'updated_at',
        ]

    def validate_property(self, value):

        if value.listing_status != Property.ListingStatus.PUBLISHED:
            raise serializers.ValidationError(
                "You can only enquire about published properties."
            )

        if value.availability != Property.Availability.AVAILABLE:
            raise serializers.ValidationError(
                "This property is not currently available."
            )

        return value
