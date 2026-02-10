from utils import logger
from utils.api_client import APIClient
from utils.config_reader import ConfigReader
from utils.logger import Logger

logger = Logger.get_logger("api_test")

def test_httpbin_get():
    base = ConfigReader.get("api", "base_url")

    logger.info(f"Calling API: {base}/get")

    client = APIClient()
    response = client.get(f"{base}/get")

    logger.info(f"Response status: {response.status_code}")

    assert response.status_code == 200

    logger.info("API assertion passed")
