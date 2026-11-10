
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PropertyViewSet,
    PublicPropertyListView,
    PropertyImageUploadView,
    PropertyImageDeleteView,
)

router = DefaultRouter()

router.register(
    'properties',
    PropertyViewSet,
    basename='property'
)

urlpatterns = [
    # Public property listings
    path(
        'public-properties/',
        PublicPropertyListView.as_view(),
        name='public-properties'
    ),

    # Upload property images
    path(
        'properties/<int:property_id>/images/',
        PropertyImageUploadView.as_view(),
        name='property-image-upload'
    ),

    # Delete a property image
    path(
        'images/<int:pk>/',
        PropertyImageDeleteView.as_view(),
        name='property-image-delete'
    ),

    # Property management routes
    path('', include(router.urls)),
]
