from __future__ import annotations

"""Service functions for interacting with the Google Geocoding API."""

from typing import Dict, List

import requests
from django.conf import settings
from django.core.cache import cache

# Endpoints for the (v4) Geocoding API
GEOCODE_FORWARD_ENDPOINT = "https://geocoding.googleapis.com/v1/geocode:forward"
GEOCODE_REVERSE_ENDPOINT = "https://geocoding.googleapis.com/v1/geocode:reverse"


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
        API is propagated where available.
    """

    # New API returns an ``error`` object instead of a status string.
    if "error" in data:
        message = data["error"].get("message", "Unknown error")
        raise RuntimeError(message)

    status = data.get("status")
    if isinstance(status, str) and status != "OK":
        # Legacy structure
        message = data.get("error_message", status)
        raise RuntimeError(message)
    if isinstance(status, dict):
        code = status.get("code")
        if code and code != "OK":
            raise RuntimeError(status.get("message", code))

    items = data.get("geocodingResults") or data.get("results", [])

    results: List[Dict] = []
    for result in items:
        # v4 API returns ``location.latLng``
        location = result.get("location", {})
        lat_lng = location.get("latLng", {})
        results.append(
            {
                "formatted_address": result.get("formattedAddress")
                or result.get("formatted_address"),
                "place_id": result.get("placeId") or result.get("place_id"),
                "latitude": lat_lng.get("latitude") or location.get("lat"),
                "longitude": lat_lng.get("longitude") or location.get("lng"),
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

    params = {"key": settings.GOOGLE_MAPS_API_KEY}
    payload = {"address": address}
    response = requests.post(
        GEOCODE_FORWARD_ENDPOINT, params=params, json=payload, timeout=10
    )
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

    params = {"key": settings.GOOGLE_MAPS_API_KEY}
    payload = {"latlng": {"latitude": lat, "longitude": lng}}
    response = requests.post(
        GEOCODE_REVERSE_ENDPOINT, params=params, json=payload, timeout=10
    )
    data = response.json()
    results = _handle_response(data)
    cache.set(cache_key, results)
    return results
