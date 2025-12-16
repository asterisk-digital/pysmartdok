import pysmartdok

def test_trivial():
    assert True

def test_api_client():
    api_client = pysmartdok.ApiClient(api_token='')

    assert api_client
