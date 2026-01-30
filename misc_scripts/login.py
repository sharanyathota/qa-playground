import os
import time

from selenium import webdriver
import pytest
from pages.LoginPage import LoginPage
from utils.readProperties import ReadConfig
from utils.customLogger import LogGen

class TestLogin():
    base_url = ReadConfig.getApplicationURL()
    username = ReadConfig.getUserEmail()
    password = ReadConfig.getUserPassword()

    logger = LogGen.loggen()

    def test_verify_homepage_title(self,setup):
        self.logger.info("****TestLogin****")
        self.logger.info("****Verifying homepage title****")
        self.driver = setup
        self.driver.get(self.base_url)
        title = self.driver.title
        if title == "nopCommerce demo store. Login":
            assert True
            self.driver.close()
            self.logger.info("****homepage title verified****")
        else:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            screenshot_dir = os.path.join(project_root, "screenshots")
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"title_failure_{timestamp}.png")
            self.driver.get_screenshot_as_file(screenshot_path)
            self.logger.error("****homepage title verification failed****")
            assert False


    def test_login(self,setup):
        self.driver = setup
        self.driver.get(self.base_url)
        self.lp = LoginPage(self.driver)
        self.lp.setUsername(username=self.username)
        self.lp.setPassword(password=self.password)
        self.lp.clickLogin()
        title = self.driver.title
        if title == "Dashboard / nopCommerce administrationtest":
            assert True
            self.driver.close()
        else:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = f"./screenshots/login_failure_{timestamp}.png"
            self.driver.get_screenshot_as_file(screenshot_path)
            assert False






