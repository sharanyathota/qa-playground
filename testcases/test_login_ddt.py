import os
import time

from selenium import webdriver
import pytest
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import Excelutils

class TestLogin_DDT():
    base_url = ReadConfig.getApplicationURL()
    path = "./Users/sharanya/PycharmProjects/nopcommerce/testdata/testdata.xlsx"

    logger = LogGen.loggen()


    def test_login_ddt(self,setup):
        self.logger.info("****TestLogin_DDT***")
        self.logger.info("****Verifying TestLogin_DDT***")
        self.driver = setup
        self.driver.get(self.base_url)
        self.lp = LoginPage(self.driver)
        self.rows = Excelutils.get_row_count(self.path,'Sheet1')
        self.lp.setUsername(username=self.username)
        self.lp.setPassword(password=self.password)
        self.lp.clickLogin()
        title = self.driver.title
        if title == "Dashboard / nopCommerce administrationtest":
            assert True
            self.driver.close()
            self.logger.info("***Login successful***")
        else:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = f"./screenshots/login_failure_{timestamp}.png"
            self.driver.get_screenshot_as_file(screenshot_path)
            assert False
        self.logger.error("***Login Failed***")






