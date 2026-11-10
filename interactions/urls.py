
from django.urls import path

from .views import (
    EnquiryCreateView,
    PropertyEnquiryListView,
)

urlpatterns = [
    # A seeker sends an enquiry
    path(
        'enquiries/',
        EnquiryCreateView.as_view(),
        name='enquiry-create'
    ),

    # An advertiser views enquiries about their properties
    path(
        'my-enquiries/',
        PropertyEnquiryListView.as_view(),
        name='my-enquiries'
    ),
]
