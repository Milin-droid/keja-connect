
from django.contrib import admin
from django.db import transaction
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

    def save_formset(self, request, form, formset, change):
        with transaction.atomic():
            instances = formset.save(commit=False)

            # Delete images marked for deletion.
            for obj in formset.deleted_objects:
                obj.delete()

            # First save images marked as non-primary.
            for obj in instances:
                if not obj.is_primary:
                    obj.save()

            # Then save primary images.
            for obj in instances:
                if obj.is_primary:
                    obj.save()

            formset.save_m2m()


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = [
        'title',
        'category',
        'property_type',
        'monthly_rent',
        'county',
        'town',
        'availability',
        'listing_status',
    ]

    list_editable = [
        'availability',
        'listing_status',
    ]

    list_filter = [
        'category',
        'property_type',
        'county',
        'availability',
        'listing_status',
    ]

    search_fields = [
        'title',
        'description',
        'county__name',
        'town__name',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    inlines = [PropertyImageInline]
