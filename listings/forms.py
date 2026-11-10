from django import forms

from interactions.models import Enquiry
from .models import Property, PropertyImage


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ('message', 'contact_phone')
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell the landlord a little about your enquiry…',
            }),
            'contact_phone': forms.TelInput(attrs={
                'placeholder': '+254 7XX XXX XXX',
                'autocomplete': 'tel',
            }),
        }


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            'title', 'category', 'property_type', 'description',
            'county', 'town', 'neighbourhood', 'bedrooms', 'bathrooms',
            'floor_area_sq_m', 'monthly_rent', 'security_deposit',
            'agency_fee', 'other_charges', 'availability',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'monthly_rent': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'security_deposit': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'agency_fee': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'other_charges': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

    def clean(self):
        cleaned = super().clean()
        county = cleaned.get('county')
        town = cleaned.get('town')
        neighbourhood = cleaned.get('neighbourhood')
        if county and town and town.county_id != county.id:
            self.add_error('town', 'Choose a town in the selected county.')
        if town and neighbourhood and neighbourhood.town_id != town.id:
            self.add_error(
                'neighbourhood',
                'Choose a neighbourhood in the selected town.',
            )
        return cleaned


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ('image', 'is_primary')

    def clean_image(self):
        image = self.cleaned_data['image']
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Images must be 5 MB or smaller.')
        return image
