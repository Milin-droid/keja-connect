
from django.contrib import admin
from .models import County, Town, Neighbourhood, LocationSuggestion


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ['name', 'county']
    list_filter = ['county']
    search_fields = ['name', 'county__name']


@admin.register(Neighbourhood)
class NeighbourhoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'town']
    list_filter = ['town__county', 'town']
    search_fields = ['name', 'town__name']


@admin.register(LocationSuggestion)
class LocationSuggestionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'location_type', 'county',
        'town', 'submitted_by', 'status', 'created_at'
    ]

    list_filter = ['location_type', 'status', 'county']
    search_fields = ['name', 'submitted_by__username']
    readonly_fields = ['created_at']
