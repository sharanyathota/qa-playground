import requests
import urllib3

# Disable SSL warnings (only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class APIClient:
    def get(self, url, headers=None, params=None):
        response = requests.get(
            url,
            headers=headers,
            params=params,
            verify=False  # ← workaround
        )
        return response
