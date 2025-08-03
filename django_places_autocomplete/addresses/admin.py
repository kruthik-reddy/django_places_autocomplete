# addresses/admin.py
from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display  = (
        "full_address",
        "city",
        "state",
        "country",
        "postal_code",
        "latitude",
        "longitude",
        "created_at",
    )
    search_fields = ("full_address", "city", "state", "country", "postal_code")
    list_filter   = ("country", "state", "city", "created_at")
