from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils import logger
from utils.config_reader import ConfigReader
from utils.logger import Logger

logger = Logger.get_logger("ui_test")

def test_open_google(driver):
    url = ConfigReader.get("ui", "base_url")

    logger.info(f"Opening URL: {url}")

    driver.get(url)

    logger.info("Page opened successfully")

    assert "Facebook" in driver.title

    logger.info("Assertion passed")



