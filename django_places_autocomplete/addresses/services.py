from __future__ import annotations

"""Service functions for interacting with the Google Geocoding API."""

from typing import Dict, List

import requests
from django.conf import settings
from django.core.cache import cache

GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"


def _handle_response(data: Dict) -> List[Dict]:
    """Validate and normalise data from the Google Geocoding API.

    Parameters
    ----------
    data: Dict
        Parsed JSON payload returned from the API.

    Returns
    -------
    list of dict
        Simplified results containing the ``formatted_address``, ``place_id``
        and coordinates for each item returned by the API.

    Raises
    ------
    RuntimeError
        If the API call did not succeed. The error message provided by the
        API (``error_message``) is propagated where available.
    """

    status = data.get("status")
    if status != "OK":
        message = data.get("error_message", status)
        raise RuntimeError(message)

    results: List[Dict] = []
    for result in data.get("results", []):
        geometry = result.get("geometry", {})
        location = geometry.get("location", {})
        results.append(
            {
                "formatted_address": result.get("formatted_address"),
                "place_id": result.get("place_id"),
                "latitude": location.get("lat"),
                "longitude": location.get("lng"),
                "types": result.get("types", []),
            }
        )
    return results


def geocode_forward(address: str) -> List[Dict]:
    """Forward geocode an address string using the Google Geocoding API.

    Results are cached using the Django cache framework keyed by the
    provided ``address``.

    Parameters
    ----------
    address: str
        The address to geocode.

    Returns
    -------
    list of dict
        A list of simplified geocoding results.
    """

    cache_key = f"geocode_forward:{address}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    params = {"address": address, "key": settings.GOOGLE_MAPS_API_KEY}
    response = requests.get(GEOCODE_ENDPOINT, params=params, timeout=10)
    data = response.json()
    results = _handle_response(data)
    cache.set(cache_key, results)
    return results


def geocode_reverse(lat: float, lng: float) -> List[Dict]:
    """Reverse geocode a latitude and longitude pair using the API.

    Results are cached using the Django cache framework keyed by the
    ``lat`` and ``lng`` values.

    Parameters
    ----------
    lat, lng: float
        Coordinate pair to reverse geocode.

    Returns
    -------
    list of dict
        A list of simplified geocoding results.
    """

    cache_key = f"geocode_reverse:{lat}:{lng}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    params = {"latlng": f"{lat},{lng}", "key": settings.GOOGLE_MAPS_API_KEY}
    response = requests.get(GEOCODE_ENDPOINT, params=params, timeout=10)
    data = response.json()
    results = _handle_response(data)
    cache.set(cache_key, results)
    return results
