import responses
from conftest import API_URL, HEADERS

from pysmartdok.common_models import FileInformation, RegistrationStatus
from pysmartdok.qd import Qd
from pysmartdok.qd_models import QDReport


@responses.activate
def test_get_qd_reports_passes_filters_and_parses():
    qd = Qd(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "qd/v2",
        json=[
            {
                "Id": 1,
                "Status": "Open",
                "SubmitDate": "2024-01-01T00:00:00Z",
                "Title": "Test deviation",
                "EventId": 100,
                "ProjectId": 5,
            }
        ],
    )
    result = qd.get_qd_reports(project_id=5, qd_status="Open")
    assert len(result) == 1
    assert isinstance(result[0], QDReport)
    assert result[0].status is RegistrationStatus.OPEN
    assert "projectId=5" in responses.calls[0].request.url
    assert "qdStatus=Open" in responses.calls[0].request.url


@responses.activate
def test_get_qd_pdf():
    qd = Qd(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "qd/9/pdf",
        json={
            "Filename": "qd-9.pdf",
            "DownloadUrl": "https://example.com/qd-9.pdf",
            "FileSize": 1234,
        },
    )
    info = qd.get_qd_pdf(9, include_details=True)
    assert isinstance(info, FileInformation)
    assert info.filename == "qd-9.pdf"
    assert "includeDetails=true" in responses.calls[0].request.url
