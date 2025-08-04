from __future__ import annotations

"""Service functions for interacting with the Google Geocoding API."""

from typing import Dict, List

import requests
from django.conf import settings

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

    Parameters
    ----------
    address: str
        The address to geocode.

    Returns
    -------
    list of dict
        A list of simplified geocoding results.
    """

    params = {"address": address, "key": settings.GOOGLE_MAPS_API_KEY}
    response = requests.get(GEOCODE_ENDPOINT, params=params, timeout=10)
    data = response.json()
    return _handle_response(data)


def geocode_reverse(lat: float, lng: float) -> List[Dict]:
    """Reverse geocode a latitude and longitude pair using the API.

    Parameters
    ----------
    lat, lng: float
        Coordinate pair to reverse geocode.

    Returns
    -------
    list of dict
        A list of simplified geocoding results.
    """

    params = {"latlng": f"{lat},{lng}", "key": settings.GOOGLE_MAPS_API_KEY}
    response = requests.get(GEOCODE_ENDPOINT, params=params, timeout=10)
    data = response.json()
    return _handle_response(data)
