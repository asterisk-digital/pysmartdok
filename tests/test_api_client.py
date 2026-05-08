import pytest
import responses
from conftest import API_URL

import pysmartdok


@responses.activate
def test_authenticate_success():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"session-token-abc"',
        status=200,
    )
    client = pysmartdok.ApiClient(api_token="real-token")
    assert client.headers == {
        "Authorization": "Bearer session-token-abc",
        "User-Agent": "pysmartdok",
    }


@responses.activate
def test_custom_user_agent():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"tok"',
        status=200,
    )
    client = pysmartdok.ApiClient(api_token="t", user_agent="myapp(you@example.com)")
    assert client.headers["User-Agent"] == "myapp(you@example.com)"
    assert responses.calls[0].request.headers["User-Agent"] == "myapp(you@example.com)"


@responses.activate
def test_authenticate_failure():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body="unauthorized",
        status=401,
    )
    with pytest.raises(pysmartdok.SmartDokApiError):
        pysmartdok.ApiClient(api_token="bad-token")


def test_rejects_empty_token():
    with pytest.raises(ValueError):
        pysmartdok.ApiClient(api_token="")
