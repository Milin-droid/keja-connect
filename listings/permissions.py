
from rest_framework.permissions import BasePermission

from .models import Property, PropertyImage


class IsPropertyAdvertiser(BasePermission):
    """
    Only authenticated advertisers can manage their properties
    and upload images to properties they own.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ['advertiser', 'both']
        )

    def has_object_permission(self, request, view, obj):

        # When checking a property directly.
        if isinstance(obj, Property):
            return obj.owner_id == request.user.id

        # When checking an image, follow its property relationship.
        if isinstance(obj, PropertyImage):
            return obj.property.owner_id == request.user.id

        return False
