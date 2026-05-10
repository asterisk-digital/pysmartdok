import pytest
import requests
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


@responses.activate
def test_reauth_on_401_then_retry():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"first-token"',
        status=200,
    )
    responses.add(responses.GET, API_URL + "Users/current", status=401)
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"second-token"',
        status=200,
    )
    responses.add(
        responses.GET,
        API_URL + "Users/current",
        json={"Id": "me"},
        status=200,
    )

    client = pysmartdok.ApiClient(api_token="real-token")
    assert client.users.get_current_user() == {"Id": "me"}
    # Two auth POSTs (initial + reauth), two GETs (401 + retry).
    assert len(responses.calls) == 4
    assert responses.calls[3].request.headers["Authorization"] == "Bearer second-token"
    # Subclient and ApiClient share the same headers dict (mutated in place).
    assert client.headers["Authorization"] == "Bearer second-token"
    assert client.users.headers is client.headers


@responses.activate
def test_no_retry_when_401_persists():
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"first-token"',
        status=200,
    )
    responses.add(responses.GET, API_URL + "Users/current", status=401)
    responses.add(
        responses.POST,
        API_URL + "Authorize/ApiToken",
        body='"second-token"',
        status=200,
    )
    responses.add(responses.GET, API_URL + "Users/current", status=401)

    client = pysmartdok.ApiClient(api_token="real-token")
    with pytest.raises(requests.HTTPError):
        client.users.get_current_user()
    # Ensures we retry exactly once, not in an infinite loop.
    assert len(responses.calls) == 4
