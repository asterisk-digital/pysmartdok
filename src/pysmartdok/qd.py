import logging
from typing import Optional

import requests

from .qd_models import QDReport
from .rue_models import FileInformation

logger = logging.getLogger(__name__)


class Qd:
    def __init__(self, api_url: str, headers: dict):
        self.api_url = api_url
        self.headers = headers

    def get_qd_reports(
        self,
        last_updated_since: Optional[str] = None,
        project_id: Optional[int] = None,
        subproject_id: Optional[int] = None,
        qd_status: Optional[str] = None,
    ) -> list[QDReport]:
        """Get all QD reports (extended schema)."""
        url = self.api_url + "qd/v2"
        params: dict = {}
        if last_updated_since is not None:
            params["lastUpdatedSince"] = last_updated_since
        if project_id is not None:
            params["projectId"] = project_id
        if subproject_id is not None:
            params["subprojectId"] = subproject_id
        if qd_status is not None:
            params["qdStatus"] = qd_status

        logger.debug("GET %s params=%s", url, params)
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        items = response.json()
        logger.info("Fetched %d QD reports", len(items))
        return [QDReport.model_validate(item) for item in items]

    def get_qd_pdf(self, qd_id: int, include_details: bool = False) -> FileInformation:
        """Get PDF file information for a QD report."""
        url = self.api_url + f"qd/{qd_id}/pdf"
        params = {"includeDetails": str(include_details).lower()}
        logger.debug("GET %s params=%s", url, params)
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return FileInformation.model_validate(response.json())
