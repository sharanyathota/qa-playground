import os
import sys
import time

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from selenium import webdriver
import pytest
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import Excelutils

"""
Data-Driven Test for Login functionality using Excel data.

Expected Excel structure in testdata.xlsx, Sheet1:
Column 1 (A): Username/Email
Column 2 (B): Password  
Column 3 (C): Expected Result (pass/fail)
Column 4 (D): Actual Result (will be written by test)

Example:
Row 1 (Header): Username | Password | Expected | Actual
Row 2: admin@yourstore.com | admin | pass | 
Row 3: invalid@test.com | wrongpass | fail |
Row 4: admin@yourstore.com | wrongpass | fail |
"""

class TestLogin_DDT():
    base_url = ReadConfig.getApplicationURL()
    path = "/Users/sharanya/PycharmProjects/nopcommerce/testdata/testdata.xlsx"
    logger = LogGen.loggen()

    @pytest.mark.parametrize("username, password, expected_result", 
                           Excelutils.get_data_as_list(path, 'Sheet1', skip_header=True))
    def test_login_ddt(self, setup, username, password, expected_result):
        self.logger.info("****TestLogin_DDT****")
        self.logger.info(f"****Testing with username: {username}****")
        
        self.driver = setup
        self.driver.get(self.base_url)
        self.lp = LoginPage(self.driver)
        
        try:
            # Enter credentials
            self.lp.setUsername(username)
            self.lp.setPassword(password)
            self.lp.clickLogin()
            
            # Give some time for the page to load
            time.sleep(2)
            
            # Check the result
            title = self.driver.title
            self.logger.info(f"Page title after login: {title}")
            
            if expected_result.lower() == "pass":
                # Expected to pass
                if "Dashboard" in title and "nopCommerce" in title:
                    assert True
                    self.logger.info(f"***Login successful for {username}***")
                    self.write_test_result(username, "Pass")
                else:
                    self.logger.error(f"***Login Failed for {username} - Expected pass but got failure***")
                    self.take_screenshot(f"login_failure_{username}")
                    self.write_test_result(username, "Fail")
                    assert False
            else:
                # Expected to fail
                if "Dashboard" not in title or "nopCommerce" not in title:
                    assert True
                    self.logger.info(f"***Login correctly failed for {username} (as expected)***")
                    self.write_test_result(username, "Pass")
                else:
                    self.logger.error(f"***Login unexpectedly succeeded for {username}***")
                    self.write_test_result(username, "Fail")
                    assert False
                    
        except Exception as e:
            self.logger.error(f"***Exception occurred during test: {str(e)}***")
            self.take_screenshot(f"exception_{username}")
            self.write_test_result(username, "Error")
            assert False
        finally:
            if self.driver:
                self.driver.close()
    
    def take_screenshot(self, test_name):
        """Helper method to take screenshot on failure"""
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = f"./screenshots/{test_name}_{timestamp}.png"
            self.driver.get_screenshot_as_file(screenshot_path)
            self.logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
    
    def write_test_result(self, username, result):
        """Helper method to write test results back to Excel"""
        try:
            success = Excelutils.update_test_result(self.path, 'Sheet1', username, result)
            if success:
                self.logger.info(f"Result '{result}' written to Excel for {username}")
            else:
                self.logger.warning(f"Could not find username '{username}' in Excel to update result")
        except Exception as e:
            self.logger.error(f"Error writing result to Excel: {str(e)}")






