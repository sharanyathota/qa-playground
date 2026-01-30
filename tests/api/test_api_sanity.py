from utils.api_client import APIClient

def test_httpbin_get():
    client = APIClient()
    response = client.get("https://httpbin.org/get")

    assert response.status_code == 200
    assert "url" in response.json()
