import pytest
import responses
from conftest import API_URL, HEADERS, REPORT_TEMPLATE, SUMMARY_TEMPLATE, page

import pysmartdok
from pysmartdok.common_models import FileInformation, RegistrationStatus
from pysmartdok.rue import Rue
from pysmartdok.rue_models import RueEventLog, RueMessage, RueReport, RueReportSummary


@responses.activate
def test_get_rue_summaries_paginates():
    rue = Rue(API_URL, HEADERS)
    page1 = [{**SUMMARY_TEMPLATE, "Id": i} for i in range(100)]
    page2 = [{**SUMMARY_TEMPLATE, "Id": i} for i in range(100, 150)]

    responses.add(responses.GET, API_URL + "rue/summaries", json=page(page1, 150))
    responses.add(responses.GET, API_URL + "rue/summaries", json=page(page2, 150))

    result = rue.get_rue_summaries()
    assert len(result) == 150
    assert all(isinstance(r, RueReportSummary) for r in result)
    assert result[0].id == 0
    assert result[-1].id == 149
    assert result[0].status is RegistrationStatus.OPEN


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
def test_get_rue_eventlog():
    rue = Rue(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "rue/9/eventlog",
        json={
            "Items": [
                {
                    "Id": 1,
                    "Description": "Created",
                    "ChangeTime": "2024-01-01T00:00:00Z",
                    "UserId": "u1",
                }
            ]
        },
    )
    log = rue.get_rue_eventlog(9)
    assert len(log) == 1
    assert isinstance(log[0], RueEventLog)
    assert log[0].description == "Created"


@responses.activate
def test_get_rue_messages():
    rue = Rue(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "rue/9/messages",
        json={
            "Items": [
                {
                    "Id": 1,
                    "Message": "hi",
                    "SubmitterId": "u1",
                    "TimeStamp": "2024-01-01T00:00:00Z",
                }
            ]
        },
    )
    messages = rue.get_rue_messages(9)
    assert len(messages) == 1
    assert isinstance(messages[0], RueMessage)
    assert messages[0].message == "hi"


@responses.activate
def test_get_rue_pdf():
    rue = Rue(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "rue/9/pdf",
        json={
            "Filename": "rue-9.pdf",
            "DownloadUrl": "https://example.com/rue-9.pdf",
            "FileSize": 12345,
        },
    )
    info = rue.get_rue_pdf(9, include_details=True)
    assert isinstance(info, FileInformation)
    assert info.filename == "rue-9.pdf"
    assert "includeDetails=true" in responses.calls[0].request.url


@responses.activate
def test_get_rue_reports_fans_out_threaded():
    rue = Rue(API_URL, HEADERS)
    summaries = [{**SUMMARY_TEMPLATE, "Id": i} for i in range(3)]
    responses.add(responses.GET, API_URL + "rue/summaries", json=page(summaries, 3))
    for i in range(3):
        responses.add(
            responses.GET,
            API_URL + f"rue/{i}",
            json={**REPORT_TEMPLATE, "Id": i},
        )

    reports = rue.get_rue_reports(threads=4)
    assert len(reports) == 3
    assert all(isinstance(r, RueReport) for r in reports)
    assert [r.id for r in reports] == [0, 1, 2]
