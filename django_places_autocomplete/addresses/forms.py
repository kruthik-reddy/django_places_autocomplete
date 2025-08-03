from django import forms

class AddressForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors',
            'placeholder': 'Enter your address...',
            'id': 'address-input',
            'autocomplete': 'off',
        })
    )
    street_number = forms.CharField(max_length=50, required=False, widget=forms.HiddenInput())
    route = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    locality = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    administrative_area_level_1 = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    country = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    postal_code = forms.CharField(max_length=20, required=False, widget=forms.HiddenInput())
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
