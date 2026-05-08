import responses
from conftest import API_URL, HEADERS

from pysmartdok.users import Users


@responses.activate
def test_get_users_passes_include_inactive():
    users = Users(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "Users",
        json={"Items": [{"Id": "u1"}]},
    )
    result = users.get_users(include_inactive=True)
    assert result == [{"Id": "u1"}]
    assert responses.calls[0].request.url.endswith("all=true&active=true")


@responses.activate
def test_get_user():
    users = Users(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "Users/abc-123",
        json={"Id": "abc-123", "Name": "Alice"},
    )
    assert users.get_user("abc-123") == {"Id": "abc-123", "Name": "Alice"}


@responses.activate
def test_get_current_user():
    users = Users(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "Users/current",
        json={"Id": "me"},
    )
    assert users.get_current_user() == {"Id": "me"}


@responses.activate
def test_get_license_info():
    users = Users(API_URL, HEADERS)
    responses.add(
        responses.GET,
        API_URL + "LicenseInfo",
        json={"AvailableLicenses": 5, "TotalLicenses": 10},
    )
    info = users.get_license_info()
    assert info["AvailableLicenses"] == 5
