import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import requests

from .exceptions import SmartDokApiError
from .rue_models import (
    FileInformation,
    RueEventLog,
    RueMessage,
    RueReport,
    RueReportSummary,
)

logger = logging.getLogger(__name__)


class Rue:
    def __init__(self, api_url: str, headers: dict):
        self.api_url = api_url
        self.headers = headers

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

            logger.debug("GET %s params=%s", url, params)
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
            logger.debug(
                "Fetched %d summaries (offset=%d, total=%d)",
                len(data["Items"]),
                offset,
                data["TotalCount"],
            )
            if offset + data["Count"] >= data["TotalCount"]:
                break
            offset += data["Count"]
        logger.info("Fetched %d RUE summaries", len(all_items))
        return all_items

    def get_rue_report(self, rue_id: int) -> RueReport:
        """Get a single RUE report with full detail."""
        url = self.api_url + f"rue/{rue_id}"
        logger.debug("GET %s", url)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return RueReport.model_validate(response.json())

    def get_rue_eventlog(self, rue_id: int) -> list[RueEventLog]:
        """Get the event log (audit trail) for a RUE report."""
        url = self.api_url + f"rue/{rue_id}/eventlog"
        logger.debug("GET %s", url)
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
        logger.debug("GET %s", url)
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
        logger.debug("GET %s params=%s", url, params)
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return FileInformation.model_validate(response.json())

    def get_rue_reports(
        self,
        threads: int = 8,
        last_updated_since: Optional[str] = None,
        project_id: Optional[int] = None,
        subproject_id: Optional[int] = None,
        rue_status: Optional[str] = None,
    ) -> list[RueReport]:
        """Get full RUE report details for all matching summaries.

        Fetches summaries first, then fans out to GET /rue/{id} concurrently.
        Results preserve summary ordering.
        """
        summaries = self.get_rue_summaries(
            last_updated_since=last_updated_since,
            project_id=project_id,
            subproject_id=subproject_id,
            rue_status=rue_status,
        )
        logger.info(
            "Fetching %d full RUE reports with %d threads",
            len(summaries),
            threads,
        )
        with ThreadPoolExecutor(max_workers=threads) as executor:
            reports = list(executor.map(lambda s: self.get_rue_report(s.id), summaries))
        logger.info("Fetched %d full RUE reports", len(reports))
        return reports
