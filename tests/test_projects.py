import responses
from conftest import API_URL, HEADERS, PROJECT_PAYLOAD

from pysmartdok.project_models import Project, SubProject
from pysmartdok.projects import Projects


@responses.activate
def test_get_projects_default_excludes_inactive_and_orders():
    projects = Projects(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "Projects",
        json={"Items": [PROJECT_PAYLOAD], "Count": 1, "TotalCount": 1, "Offset": 0},
    )
    result = projects.get_projects()
    assert len(result) == 1
    assert isinstance(result[0], Project)
    assert result[0].project_name == "Site A"
    url = responses.calls[0].request.url
    assert "all=false" in url
    assert "includeOrders=false" in url


@responses.activate
def test_get_project():
    projects = Projects(API_URL, HEADERS)
    responses.add(responses.GET, API_URL + "Projects/5", json=PROJECT_PAYLOAD)
    result = projects.get_project(5)
    assert isinstance(result, Project)
    assert result.id == 5


@responses.activate
def test_get_subprojects():
    projects = Projects(API_URL, HEADERS)
    sub_payload = {
        "Id": 1,
        "ProjectId": 5,
        "SubProjectName": "Sub",
        "SubProjectNumber": "001",
        "Project": {
            "ProjectId": 5,
            "ProjectName": "Site A",
            "ProjectNumber": "1234",
        },
    }
    responses.add(
        responses.GET,
        API_URL + "Projects/5/SubProjects",
        json={"Items": [sub_payload], "Count": 1, "TotalCount": 1, "Offset": 0},
    )
    result = projects.get_subprojects(5)
    assert len(result) == 1
    assert isinstance(result[0], SubProject)
    assert result[0].project.project_name == "Site A"


@responses.activate
def test_get_next_project_number():
    projects = Projects(API_URL, HEADERS)
    responses.add(responses.GET, API_URL + "Projects/NextProjectNumber", json="1235")
    assert projects.get_next_project_number() == "1235"
