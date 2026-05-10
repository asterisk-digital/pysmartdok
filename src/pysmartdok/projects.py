import logging
from typing import Optional

from ._http import _HttpClient
from .exceptions import SmartDokApiError
from .project_models import Project, SubProject

logger = logging.getLogger(__name__)


class Projects(_HttpClient):
    def get_projects(
        self,
        project_number: Optional[str] = None,
        project_name: Optional[str] = None,
        include_inactive: bool = False,
        include_orders: bool = False,
        updated_since: Optional[str] = None,
        created_since: Optional[str] = None,
    ) -> list[Project]:
        """Get projects. By default returns only active, non-order projects."""
        url = self.api_url + "Projects"
        params: dict = {
            "all": str(include_inactive).lower(),
            "includeOrders": str(include_orders).lower(),
        }
        if project_number is not None:
            params["projectNumber"] = project_number
        if project_name is not None:
            params["projectName"] = project_name
        if updated_since is not None:
            params["updatedSince"] = updated_since
        if created_since is not None:
            params["createdSince"] = created_since

        logger.debug("GET %s params=%s", url, params)
        response = self._request("GET", url, params=params)
        response.raise_for_status()

        data = response.json()
        if "Items" not in data:
            raise SmartDokApiError(
                "Failed to get projects from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )
        items = data["Items"]
        logger.info("Fetched %d projects", len(items))
        return [Project.model_validate(item) for item in items]

    def get_project(self, project_id: int) -> Project:
        """Get a single project by ID."""
        url = self.api_url + f"Projects/{project_id}"
        logger.debug("GET %s", url)
        response = self._request("GET", url)
        response.raise_for_status()
        return Project.model_validate(response.json())

    def get_subprojects(
        self,
        project_id: int,
        sub_project_number: Optional[str] = None,
        sub_project_name: Optional[str] = None,
        include_inactive: bool = False,
        updated_since: Optional[str] = None,
    ) -> list[SubProject]:
        """Get subprojects for a project."""
        url = self.api_url + f"Projects/{project_id}/SubProjects"
        params: dict = {"all": str(include_inactive).lower()}
        if sub_project_number is not None:
            params["subProjectNumber"] = sub_project_number
        if sub_project_name is not None:
            params["subProjectName"] = sub_project_name
        if updated_since is not None:
            params["updatedSince"] = updated_since

        logger.debug("GET %s params=%s", url, params)
        response = self._request("GET", url, params=params)
        response.raise_for_status()

        data = response.json()
        if "Items" not in data:
            raise SmartDokApiError(
                "Failed to get subprojects from SmartDok API. Items not found in response."
                + " Response body: "
                + response.text
            )
        return [SubProject.model_validate(item) for item in data["Items"]]

    def get_next_project_number(self) -> str:
        """Get next available project number."""
        url = self.api_url + "Projects/NextProjectNumber"
        logger.debug("GET %s", url)
        response = self._request("GET", url)
        response.raise_for_status()
        return response.json()
