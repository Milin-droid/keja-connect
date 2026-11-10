
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Enquiry
from .serializers import EnquirySerializer


class IsSeeker(IsAuthenticated):
    """
    Only house seekers and users with both roles can send enquiries.
    """

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.role in ['seeker', 'both']
        )


class IsAdvertiser(IsAuthenticated):
    """
    Only property advertisers and users with both roles can view
    enquiries about their properties.
    """

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.role in ['advertiser', 'both']
        )


class EnquiryCreateView(generics.CreateAPIView):
    """
    Allows a seeker to enquire about a published, available property.
    """

    serializer_class = EnquirySerializer
    permission_classes = [IsSeeker]

    def perform_create(self, serializer):
        property = serializer.validated_data['property']

        if property.owner_id == self.request.user.id:
            raise ValidationError(
                "You cannot send an enquiry about your own property."
            )

        serializer.save(seeker=self.request.user)


class PropertyEnquiryListView(generics.ListAPIView):
    """
    Allows advertisers to view enquiries about their own properties.
    """

    serializer_class = EnquirySerializer
    permission_classes = [IsAdvertiser]

    def get_queryset(self):
        return Enquiry.objects.filter(
            property__owner=self.request.user
        ).select_related('property', 'seeker')
