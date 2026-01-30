from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_open_google(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title



