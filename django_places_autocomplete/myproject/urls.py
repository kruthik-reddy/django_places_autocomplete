# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Mount the app at /address/
    path('address/', include('django_places_autocomplete.addresses.urls')),

    # OPTIONAL: make the site root redirect to /address/
    path('', RedirectView.as_view(pattern_name='address_form', permanent=False)),
]
