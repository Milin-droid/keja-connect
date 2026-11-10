from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path('dashboard/', views.landlord_dashboard, name='landlord-dashboard'),
    path('dashboard/listings/new/', views.landlord_property_create, name='landlord-property-create'),
    path('dashboard/listings/<int:pk>/edit/', views.landlord_property_edit, name='landlord-property-edit'),
    path('dashboard/listings/<int:pk>/delete/', views.landlord_property_delete, name='landlord-property-delete'),
    path('dashboard/listings/<int:pk>/images/', views.landlord_image_upload, name='landlord-image-upload'),
    path('dashboard/images/<int:pk>/delete/', views.landlord_image_delete, name='landlord-image-delete'),
    path('dashboard/enquiries/<int:pk>/status/', views.landlord_enquiry_status, name='landlord-enquiry-status'),
]
