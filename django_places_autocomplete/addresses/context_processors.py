def google_maps_api_key(request):
    from django.conf import settings
    return {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY}
