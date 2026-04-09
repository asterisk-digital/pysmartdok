import logging
import warnings
from typing import Optional

import requests

from .exceptions import SmartDokApiError
from .rue_models import (
    FileInformation,
    RueEventLog,
    RueMessage,
    RueReport,
    RueReportDetail,
    RueReportSummary,
)

logger = logging.getLogger(__name__)


class Rue:
    def __init__(self, api_url: str, headers: dict):
        self.api_url = api_url
        self.headers = headers

    def get_rue(
        self,
        last_updated_since: Optional[str] = None,
        project_id: Optional[int] = None,
        subproject_id: Optional[int] = None,
        rue_status: Optional[str] = None,
    ) -> list[RueReport]:
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

        return [RueReport.model_validate(item) for item in response.json()["Items"]]

    def get_rue_summaries(
        self,
        last_updated_since: Optional[str] = None,
        project_id: Optional[int] = None,
        subproject_id: Optional[int] = None,
        rue_status: Optional[str] = None,
    ) -> list[RueReportSummary]:
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
            all_items.extend(
                RueReportSummary.model_validate(item) for item in data["Items"]
            )
            if offset + data["Count"] >= data["TotalCount"]:
                break
            offset += data["Count"]
        return all_items

    def get_rue_report(self, rue_id: int) -> RueReportDetail:
        """Get a single RUE report with full detail."""
        url = self.api_url + f"rue/{rue_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return RueReportDetail.model_validate(response.json())

    def get_rue_eventlog(self, rue_id: int) -> list[RueEventLog]:
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
        return [RueEventLog.model_validate(item) for item in data["Items"]]

    def get_rue_messages(self, rue_id: int) -> list[RueMessage]:
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
        return [RueMessage.model_validate(item) for item in data["Items"]]

    def get_rue_pdf(
        self, rue_id: int, include_details: bool = False
    ) -> FileInformation:
        """Get PDF file information for a RUE report."""
        url = self.api_url + f"rue/{rue_id}/pdf"
        params = {"includeDetails": str(include_details).lower()}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return FileInformation.model_validate(response.json())
