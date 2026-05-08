API_URL = "https://api.smartdok.no/"
HEADERS = {"Authorization": "Bearer test"}

SUMMARY_TEMPLATE = {
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

REPORT_TEMPLATE = {
    **SUMMARY_TEMPLATE,
    "ReportedBySubcontractor": False,
    "Values": [],
}

PROJECT_PAYLOAD = {
    "Id": 5,
    "ProjectName": "Site A",
    "ProjectNumber": "1234",
    "Departments": [1, 2],
    "Location": "Oslo",
    "ProjectOwnerName": "Alice",
    "ProjectOwnerEmail": "alice@example.com",
    "ProjectOwnerMobile": "+4790000000",
    "ClientCompanyName": "Acme",
    "ClientCompanyContact": "Bob",
    "ClientCompanyEmail": "bob@acme.com",
    "ClientCompanyMobile": "+4790000001",
    "DescriptionText": "...",
    "DocumentUrl": "https://example.com/doc",
    "UserIds": [],
}


def page(items, total):
    """Wrap a list of items into the SmartDok paginated CollectionOutput shape."""
    return {"Items": items, "Count": len(items), "TotalCount": total}
