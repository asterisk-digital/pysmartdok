import json
import logging
import warnings
from typing import List, Dict, Optional

import requests

from .exceptions import SmartDokApiError
from .users import Users

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, api_token: str):
        if api_token is None or api_token == "":
            raise ValueError("api_token must be a valid string")
        self.api_token = api_token
        self.api_url = "https://api.smartdok.no/"
        self.headers = {}
        self.authenticate()
        # Headers are set by authenticate
        self.users = Users(self.api_url, self.headers)

    def authenticate(self):
        url = self.api_url + "Authorize/ApiToken"
        post_body = json.dumps({"Token": self.api_token})
        response = requests.post(
            url, data=post_body, headers={"Content-Type": "application/json"}
        )
        if response.status_code >= 300:
            raise SmartDokApiError(
                "Failed to authenticate with SmartDok API."
                + " Response code: "
                + str(response.status_code)
                + " Response body: "
                + response.text
            )

        # The session token contains quotes, so we need to remove them
        session_token = response.text.replace('"', "")

        self.headers = {"Authorization": "Bearer " + session_token}

    def get_qd(self) -> List[Dict]:
        url = self.api_url + "qd/v2"
        response = requests.get(url, headers=self.headers)
        if response.status_code >= 300:
            raise SmartDokApiError(
                "Failed to get QD data from SmartDok API."
                + " Response code: "
                + str(response.status_code)
                + " Response body: "
                + response.text
            )

        if "Items" not in response.json():
            raise SmartDokApiError(
                "Failed to get QD data from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )

        items = response.json()["Items"]

        return items

    def get_rue(
        self,
        last_updated_since: Optional[str] = None,
        project_id: Optional[int] = None,
        subproject_id: Optional[int] = None,
        rue_status: Optional[str] = None,
    ) -> list[dict]:
        """Get RUE reports. DEPRECATED: Use get_rue_summaries() instead."""
        warnings.warn(
            "get_rue() is deprecated. The GET /rue endpoint has been deprecated by SmartDok. "
            "Use get_rue_summaries() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        logger.warning(
            "GET /rue is deprecated by SmartDok. Use get_rue_summaries() instead."
        )
        url = self.api_url + "rue"
        params = {}
        if last_updated_since is not None:
            params["lastUpdatedSince"] = last_updated_since
        if project_id is not None:
            params["projectId"] = project_id
        if subproject_id is not None:
            params["subprojectId"] = subproject_id
        if rue_status is not None:
            params["rueStatus"] = rue_status

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        if "Items" not in response.json():
            raise SmartDokApiError(
                "Failed to get RUE data from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )

        return response.json()["Items"]

    def get_rue_summaries(
        self,
        last_updated_since: Optional[str] = None,
        project_id: Optional[int] = None,
        subproject_id: Optional[int] = None,
        rue_status: Optional[str] = None,
    ) -> list[dict]:
        """Get all RUE report summaries, handling pagination automatically."""
        url = self.api_url + "rue/summaries"
        all_items = []
        offset = 0
        while True:
            params: dict = {"Offset": offset, "Count": 100}
            if last_updated_since is not None:
                params["LastUpdatedSince"] = last_updated_since
            if project_id is not None:
                params["ProjectId"] = project_id
            if subproject_id is not None:
                params["SubprojectId"] = subproject_id
            if rue_status is not None:
                params["RueStatus"] = rue_status

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            if "Items" not in data:
                raise SmartDokApiError(
                    "Failed to get RUE summaries from SmartDok API. Items not found in response."
                    + " Response body: "
                    + response.text
                )
            all_items.extend(data["Items"])
            if offset + data["Count"] >= data["TotalCount"]:
                break
            offset += data["Count"]
        return all_items

    def get_rue_report(self, rue_id: int) -> dict:
        """Get a single RUE report with full detail."""
        url = self.api_url + f"rue/{rue_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_rue_eventlog(self, rue_id: int) -> list[dict]:
        """Get the event log (audit trail) for a RUE report."""
        url = self.api_url + f"rue/{rue_id}/eventlog"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        if "Items" not in data:
            raise SmartDokApiError(
                "Failed to get RUE event log from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )
        return data["Items"]

    def get_rue_messages(self, rue_id: int) -> list[dict]:
        """Get messages/comments for a RUE report."""
        url = self.api_url + f"rue/{rue_id}/messages"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        if "Items" not in data:
            raise SmartDokApiError(
                "Failed to get RUE messages from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )
        return data["Items"]

    def get_rue_pdf(self, rue_id: int, include_details: bool = False) -> dict:
        """Get PDF file information for a RUE report.

        Returns a dict with 'Filename', 'DownloadUrl', 'FileSize', and 'FileDate'.
        """
        url = self.api_url + f"rue/{rue_id}/pdf"
        params = {"includeDetails": str(include_details).lower()}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_projects(self) -> list[dict]:
        url = self.api_url + "Projects"
        query_params = {"all": "true"}
        response = requests.get(url, headers=self.headers, params=query_params)
        response.raise_for_status()

        items = response.json()["Items"]
        return items
