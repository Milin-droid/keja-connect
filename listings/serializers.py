
from rest_framework import serializers
from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyImage

        fields = [
            'id',
            'image',
            'is_primary',
            'uploaded_at',
        ]

        read_only_fields = [
            'id',
            'uploaded_at',
        ]

    def validate_image(self, image):
        # Maximum image size: 5 MB
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size cannot exceed 5 MB."
            )

        return image


class PropertySerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    total_move_in_cost = serializers.ReadOnlyField()

    images = PropertyImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Property

        fields = [
            'id',
            'owner',
            'title',
            'category',
            'property_type',
            'description',
            'county',
            'town',
            'neighbourhood',
            'bedrooms',
            'bathrooms',
            'floor_area_sq_m',
            'monthly_rent',
            'security_deposit',
            'agency_fee',
            'other_charges',
            'total_move_in_cost',
            'availability',
            'listing_status',
            'images',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'owner',
            'total_move_in_cost',
            'listing_status',
            'created_at',
            'updated_at',
            'images',
        ]

    def validate(self, data):

        county = data.get(
            'county',
            getattr(self.instance, 'county', None)
        )

        town = data.get(
            'town',
            getattr(self.instance, 'town', None)
        )

        neighbourhood = data.get(
            'neighbourhood',
            getattr(self.instance, 'neighbourhood', None)
        )

        if town and county and town.county_id != county.id:
            raise serializers.ValidationError(
                "The selected town does not belong to this county."
            )

        if neighbourhood and town:
            if neighbourhood.town_id != town.id:
                raise serializers.ValidationError(
                    "The selected neighbourhood does not belong to this town."
                )

        return data
