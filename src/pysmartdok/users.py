import logging
import warnings

import requests

from .exceptions import SmartDokApiError

logger = logging.getLogger(__name__)


class Users:
    def __init__(self, api_url: str, headers: dict):
        self.api_url = api_url
        self.headers = headers

    def get_users(self, include_inactive: bool = False) -> list[dict]:
        """Get users. By default returns only active users."""
        url = self.api_url + "Users"
        params = {
            "all": str(include_inactive).lower(),
            "active": "true",
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json()
        if "Items" not in data:
            raise SmartDokApiError(
                "Failed to get users from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )
        return data["Items"]

    def get_user(self, user_id: str) -> dict:
        """Get a single user by ID (UUID)."""
        url = self.api_url + f"Users/{user_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_current_user(self) -> dict:
        """Get the currently authenticated user."""
        url = self.api_url + "Users/current"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_roles(self) -> list[str]:
        """Get roles. DEPRECATED: Use the Role model on UserOutput instead."""
        warnings.warn(
            "get_roles() is deprecated. The GET /Roles endpoint has been deprecated by SmartDok.",
            DeprecationWarning,
            stacklevel=2,
        )
        logger.warning("GET /Roles is deprecated by SmartDok.")
        url = self.api_url + "Roles"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_license_info(self) -> dict:
        """Get license info. Returns AvailableLicenses and TotalLicenses."""
        url = self.api_url + "LicenseInfo"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
