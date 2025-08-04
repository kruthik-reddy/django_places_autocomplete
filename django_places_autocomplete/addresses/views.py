from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from .forms import AddressForm
from .models import Address
from .services import geocode_forward, geocode_reverse


def address_form_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = {
                'full_address': form.cleaned_data['address'],
                'street_number': form.cleaned_data['street_number'],
                'route': form.cleaned_data['route'],
                'city': form.cleaned_data['locality'],
                'state': form.cleaned_data['administrative_area_level_1'],
                'country': form.cleaned_data['country'],
                'postal_code': form.cleaned_data['postal_code'],
                'latitude': form.cleaned_data['latitude'],
                'longitude': form.cleaned_data['longitude'],
            }
            Address.objects.create(**data)
            return JsonResponse({'success': True, 'message': 'Address saved successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors})

    form = AddressForm()
    return render(request, 'addresses/address_form.html', {'form': form})


def address_list_view(request):
    qs = Address.objects.order_by('-created_at')
    paginator = Paginator(qs, 10)            # 10 per page
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request,
                  'addresses/address_list.html',
                  {'page_obj': page_obj})


def geocode_view(request):
    address = request.GET.get("address")
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    try:
        if address:
            results = geocode_forward(address)
        elif lat and lng:
            try:
                lat_f = float(lat)
                lng_f = float(lng)
            except ValueError:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "lat and lng must be valid numbers",
                    },
                    status=400,
                )
            results = geocode_reverse(lat_f, lng_f)
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Provide either address or both lat and lng parameters",
                },
                status=400,
            )

        return JsonResponse({"success": True, "results": results})
    except Exception as exc:  # pragma: no cover - defensive programming
        return JsonResponse({"success": False, "error": str(exc)}, status=400)
