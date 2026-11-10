
from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'property',
        'seeker',
        'status',
        'created_at',
    ]

    list_filter = [
        'status',
        'created_at',
    ]

    search_fields = [
        'property__title',
        'seeker__username',
        'message',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]
