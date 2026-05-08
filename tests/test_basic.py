import pytest
import responses

import pysmartdok
from pysmartdok.rue import Rue
from pysmartdok.rue_models import RueReport, RueReportSummary, RueStatus
from pysmartdok.users import Users

API_URL = "https://api.smartdok.no/"
HEADERS = {"Authorization": "Bearer test"}


@responses.activate
def test_api_client_authenticate_success():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"session-token-abc"',
        status=200,
    )
    client = pysmartdok.ApiClient(api_token="real-token")
    assert client.headers == {"Authorization": "Bearer session-token-abc"}


@responses.activate
def test_api_client_authenticate_failure():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body="unauthorized",
        status=401,
    )
    with pytest.raises(pysmartdok.SmartDokApiError):
        pysmartdok.ApiClient(api_token="bad-token")


def test_api_client_rejects_empty_token():
    with pytest.raises(ValueError):
        pysmartdok.ApiClient(api_token="")


@responses.activate
def test_get_rue_summaries_paginates():
    rue = Rue(API_URL, HEADERS)

    def page(items, total):
        return {"Items": items, "Count": len(items), "TotalCount": total}

    summary_template = {
        "Id": 0,
        "EventId": 1,
        "Title": "t",
        "Status": "Open",
        "Severity": "Low",
        "SubmitDate": "2024-01-01T00:00:00Z",
        "EventTime": "2024-01-01T00:00:00Z",
        "ProjectId": 1,
        "OwnerId": "owner",
    }
    page1 = [{**summary_template, "Id": i} for i in range(100)]
    page2 = [{**summary_template, "Id": i} for i in range(100, 150)]

    responses.add(responses.GET, API_URL + "rue/summaries", json=page(page1, 150))
    responses.add(responses.GET, API_URL + "rue/summaries", json=page(page2, 150))

    result = rue.get_rue_summaries()
    assert len(result) == 150
    assert all(isinstance(r, RueReportSummary) for r in result)
    assert result[0].id == 0
    assert result[-1].id == 149
    assert result[0].status is RueStatus.OPEN


@responses.activate
def test_get_rue_report_parses_full_detail():
    rue = Rue(API_URL, HEADERS)
    payload = {
        "Id": 42,
        "EventId": 1001,
        "Title": "Slip on stairs",
        "Description": "Wet floor not signposted",
        "Status": "Open",
        "Severity": "High",
        "SubmitDate": "2024-03-01T08:00:00Z",
        "EventTime": "2024-03-01T07:30:00Z",
        "ProjectId": 7,
        "OwnerId": "owner-uuid",
        "ReportedBySubcontractor": False,
        "Values": [],
        "GeoLocation": {"Lat": 59.9, "Lon": 10.7},
    }
    responses.add(responses.GET, API_URL + "rue/42", json=payload)

    report = rue.get_rue_report(42)
    assert isinstance(report, RueReport)
    assert report.id == 42
    assert report.title == "Slip on stairs"
    assert report.geo_location.lat == 59.9


@responses.activate
def test_get_rue_summaries_raises_on_missing_items():
    rue = Rue(API_URL, HEADERS)
    responses.add(responses.GET, API_URL + "rue/summaries", json={"Unexpected": True})
    with pytest.raises(pysmartdok.SmartDokApiError):
        rue.get_rue_summaries()


@responses.activate
def test_users_get_users_passes_include_inactive():
    users = Users(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "Users",
        json={"Items": [{"Id": "u1"}]},
    )
    result = users.get_users(include_inactive=True)
    assert result == [{"Id": "u1"}]
    assert responses.calls[0].request.url.endswith("all=true&active=true")
