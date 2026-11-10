
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from interactions.models import Enquiry
from .forms import EnquiryForm, PropertyForm, PropertyImageForm
from .models import Property, PropertyImage
from locations.models import County, Neighbourhood, Town
from .serializers import (
    PropertySerializer,
    PropertyImageSerializer,
)
from .permissions import IsPropertyAdvertiser


def public_property_browser(request):
    """Render the public catalogue using the same publication rules as the API."""
    properties = Property.objects.filter(
        listing_status=Property.ListingStatus.PUBLISHED,
        availability=Property.Availability.AVAILABLE,
    ).select_related(
        'county', 'town', 'neighbourhood'
    ).prefetch_related(Prefetch(
        'images',
        queryset=PropertyImage.objects.order_by('-is_primary', 'uploaded_at'),
    ))

    search = request.GET.get('q', '').strip()
    county_id = request.GET.get('county', '').strip()
    town_id = request.GET.get('town', '').strip()
    neighbourhood_id = request.GET.get('neighbourhood', '').strip()
    category = request.GET.get('category', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    bedrooms = request.GET.get('bedrooms', '').strip()
    min_rent = request.GET.get('min_rent', '').strip()
    max_rent = request.GET.get('max_rent', '').strip()

    if search:
        properties = properties.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(county__name__icontains=search)
            | Q(town__name__icontains=search)
            | Q(neighbourhood__name__icontains=search)
        )

    if county_id.isdigit():
        properties = properties.filter(county_id=int(county_id))
    else:
        county_id = ''

    if town_id.isdigit():
        properties = properties.filter(town_id=int(town_id))
    else:
        town_id = ''

    if neighbourhood_id.isdigit():
        properties = properties.filter(neighbourhood_id=int(neighbourhood_id))
    else:
        neighbourhood_id = ''

    valid_categories = dict(Property.Category.choices)
    if category in valid_categories:
        properties = properties.filter(category=category)
    else:
        category = ''

    valid_types = dict(Property.PropertyType.choices)
    if property_type in valid_types:
        properties = properties.filter(property_type=property_type)
    else:
        property_type = ''

    if bedrooms in ['1', '2', '3']:
        properties = properties.filter(bedrooms=int(bedrooms))
    elif bedrooms == '4+':
        properties = properties.filter(bedrooms__gte=4)
    else:
        bedrooms = ''

    def parse_rent(value):
        if not value:
            return None
        try:
            amount = Decimal(value)
        except InvalidOperation:
            return None
        return amount if amount.is_finite() and amount >= 0 else None

    minimum = parse_rent(min_rent)
    maximum = parse_rent(max_rent)
    if minimum is not None:
        properties = properties.filter(monthly_rent__gte=minimum)
    if maximum is not None:
        properties = properties.filter(monthly_rent__lte=maximum)

    return render(request, 'listings/property_browser.html', {
        'properties': properties,
        'counties': County.objects.all(),
        'towns': Town.objects.select_related('county').all(),
        'neighbourhoods': Neighbourhood.objects.select_related('town').all(),
        'categories': Property.Category.choices,
        'property_types': Property.PropertyType.choices,
        'filters': {
            'q': search,
            'county': county_id,
            'town': town_id,
            'neighbourhood': neighbourhood_id,
            'category': category,
            'property_type': property_type,
            'bedrooms': bedrooms,
            'min_rent': min_rent if minimum is not None else '',
            'max_rent': max_rent if maximum is not None else '',
        },
    })


def public_property_detail(request, pk):
    """Show details only for a published, currently available property."""
    property = get_object_or_404(
        Property.objects.select_related(
            'county', 'town', 'neighbourhood'
        ).prefetch_related(Prefetch(
            'images',
            queryset=PropertyImage.objects.order_by('-is_primary', 'uploaded_at'),
        )),
        pk=pk,
        listing_status=Property.ListingStatus.PUBLISHED,
        availability=Property.Availability.AVAILABLE,
    )
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, 'Sign in or create an account to send an enquiry.')
            return redirect('accounts:login')
        if request.user.role not in ['seeker', 'both']:
            messages.error(request, 'A seeker account is needed to enquire about a property.')
            return redirect('website-property-detail', pk=property.pk)
        if property.owner_id == request.user.id:
            messages.error(request, 'You cannot enquire about your own property.')
            return redirect('website-property-detail', pk=property.pk)

        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.property = property
            enquiry.seeker = request.user
            enquiry.save()
            messages.success(request, 'Your enquiry has been sent. The landlord can call you on the number you provided.')
            return redirect('website-property-detail', pk=property.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['contact_phone'] = request.user.phone_number
        form = EnquiryForm(initial=initial)

    return render(request, 'listings/property_detail.html', {
        'property': property,
        'enquiry_form': form,
    })


def _has_advertiser_role(request):
    if request.user.role not in ['advertiser', 'both']:
        messages.error(request, 'This area is for landlords and property advertisers.')
        return False
    return True


@login_required
def landlord_dashboard(request):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    properties = Property.objects.filter(owner=request.user).prefetch_related('images')
    enquiries = Enquiry.objects.filter(
        property__owner=request.user
    ).select_related('property', 'seeker')
    my_enquiries = Enquiry.objects.filter(
        seeker=request.user
    ).select_related('property', 'property__county', 'property__town')
    return render(request, 'listings/landlord_dashboard.html', {
        'properties': properties,
        'enquiries': enquiries,
        'my_enquiries': my_enquiries,
    })


@login_required
def landlord_property_create(request):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    form = PropertyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        property = form.save(commit=False)
        property.owner = request.user
        property.listing_status = Property.ListingStatus.PENDING
        property.save()
        messages.success(request, 'Listing saved and sent for admin review.')
        return redirect('listings:landlord-property-edit', pk=property.pk)
    return render(request, 'listings/landlord_property_form.html', {
        'form': form,
        'is_new': True,
    })


@login_required
def landlord_property_edit(request, pk):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    form = PropertyForm(request.POST or None, instance=property)
    if request.method == 'POST' and form.is_valid():
        property = form.save(commit=False)
        property.listing_status = Property.ListingStatus.PENDING
        property.save()
        messages.success(request, 'Changes saved and sent for admin review.')
        return redirect('listings:landlord-property-edit', pk=property.pk)
    image_form = PropertyImageForm()
    return render(request, 'listings/landlord_property_form.html', {
        'form': form,
        'property': property,
        'image_form': image_form,
        'is_new': False,
    })


@login_required
@require_POST
def landlord_image_upload(request, pk):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    form = PropertyImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.property = property
        if image.is_primary or not property.images.filter(is_primary=True).exists():
            image.is_primary = True
        image.save()
        if property.listing_status == Property.ListingStatus.PUBLISHED:
            property.listing_status = Property.ListingStatus.PENDING
            property.save(update_fields=['listing_status', 'updated_at'])
        messages.success(request, 'Property photo uploaded.')
    else:
        messages.error(request, 'Choose a valid image up to 5 MB.')
    return redirect('listings:landlord-property-edit', pk=pk)


@login_required
@require_POST
def landlord_image_delete(request, pk):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    image = get_object_or_404(
        PropertyImage, pk=pk, property__owner=request.user
    )
    property_id = image.property_id
    if image.image:
        image.image.delete(save=False)
    image.delete()
    if property_id:
        property = Property.objects.get(pk=property_id)
        if property.listing_status == Property.ListingStatus.PUBLISHED:
            property.listing_status = Property.ListingStatus.PENDING
            property.save(update_fields=['listing_status', 'updated_at'])
    messages.success(request, 'Property photo removed.')
    return redirect('listings:landlord-property-edit', pk=property_id)


@login_required
@require_POST
def landlord_enquiry_status(request, pk):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    enquiry = get_object_or_404(Enquiry, pk=pk, property__owner=request.user)
    new_status = request.POST.get('status')
    allowed_statuses = {
        Enquiry.Status.READ,
        Enquiry.Status.RESPONDED,
        Enquiry.Status.CLOSED,
    }
    if new_status in allowed_statuses:
        enquiry.status = new_status
        enquiry.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Enquiry status updated.')
    else:
        messages.error(request, 'Choose a valid enquiry status.')
    return redirect('listings:landlord-dashboard')


@login_required
@require_POST
def landlord_property_delete(request, pk):
    if not _has_advertiser_role(request):
        return redirect('property-browser')
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    property.delete()
    messages.success(request, 'Listing deleted.')
    return redirect('listings:landlord-dashboard')


# ==========================================
# 1. Advertiser Property Management
# ==========================================

class PropertyViewSet(viewsets.ModelViewSet):

    serializer_class = PropertySerializer

    permission_classes = [
        IsAuthenticated,
        IsPropertyAdvertiser,
    ]

    def get_queryset(self):
        # Advertisers can only see their own properties.
        return Property.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        # Automatically assign the logged-in advertiser.
        # New listings require admin approval.
        serializer.save(
            owner=self.request.user,
            listing_status=Property.ListingStatus.PENDING
        )


# ==========================================
# 2. Public Property Listings
# ==========================================

class PublicPropertyListView(generics.ListAPIView):

    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    filterset_fields = [
        'county',
        'property_type',
        'bedrooms',
        'category',
    ]

    def get_queryset(self):

        queryset = Property.objects.filter(
            listing_status=Property.ListingStatus.PUBLISHED,
            availability=Property.Availability.AVAILABLE
        )

        min_rent = self.request.query_params.get('min_rent')
        max_rent = self.request.query_params.get('max_rent')

        if min_rent:
            queryset = queryset.filter(
                monthly_rent__gte=min_rent
            )

        if max_rent:
            queryset = queryset.filter(
                monthly_rent__lte=max_rent
            )

        return queryset


# ==========================================
# 3. Property Image Upload
# ==========================================

class PropertyImageUploadView(generics.CreateAPIView):

    serializer_class = PropertyImageSerializer

    permission_classes = [
        IsAuthenticated,
        IsPropertyAdvertiser,
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def perform_create(self, serializer):

        # Find the property and confirm ownership.
        property = get_object_or_404(
            Property,
            pk=self.kwargs['property_id'],
            owner=self.request.user
        )

        # Save the uploaded image.
        serializer.save(property=property)


# ==========================================
# 4. Property Image Deletion
# ==========================================

class PropertyImageDeleteView(generics.DestroyAPIView):

    permission_classes = [
        IsAuthenticated,
        IsPropertyAdvertiser,
    ]

    def get_queryset(self):

        # Advertisers can only delete images
        # belonging to their own properties.
        return PropertyImage.objects.filter(
            property__owner=self.request.user
        )

    def perform_destroy(self, instance):

        # Delete the physical image file first.
        if instance.image:
            instance.image.delete(save=False)

        # Delete the database record.
        instance.delete()
