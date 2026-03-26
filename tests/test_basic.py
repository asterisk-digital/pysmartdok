import pysmartdok


def test_trivial():
    assert True


def test_api_client_without_token():
    api_client = None

    try:
        api_client = pysmartdok.ApiClient(api_token="")
    except ValueError:
        assert True
    else:
        assert False

    assert api_client is None


def test_api_client_with_token():
    api_client = None

    try:
        api_client = pysmartdok.ApiClient(api_token="test")
    except pysmartdok.api_client.SmartDokApiError:
        assert True
    else:
        assert False

    assert api_client is None
