#!/usr/bin/env python3
"""
Simple script to run the data-driven test without pytest.
This script demonstrates how to run the DDT test manually.
"""

import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pageObjects.LoginPage import LoginPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
from utilities import Excelutils
import time

def setup_driver():
    """Setup Chrome driver"""
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)
    driver.maximize_window()
    return driver

def run_login_test(username, password, expected_result):
    """Run a single login test"""
    logger = LogGen.loggen()
    base_url = ReadConfig.getApplicationURL()
    path = "/Users/sharanya/PycharmProjects/nopcommerce/testdata/testdata.xlsx"
    
    logger.info(f"****Testing with username: {username}****")
    
    driver = setup_driver()
    try:
        driver.get(base_url)
        lp = LoginPage(driver)
        
        # Enter credentials
        lp.setUsername(username)
        lp.setPassword(password)
        lp.clickLogin()
        
        # Give some time for the page to load
        time.sleep(2)
        
        # Check the result
        title = driver.title
        logger.info(f"Page title after login: {title}")
        
        if expected_result.lower() == "pass":
            # Expected to pass
            if "Dashboard" in title and "nopCommerce" in title:
                logger.info(f"***Login successful for {username}***")
                result = "Pass"
            else:
                logger.error(f"***Login Failed for {username} - Expected pass but got failure***")
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                screenshot_path = f"./screenshots/login_failure_{username}_{timestamp}.png"
                driver.get_screenshot_as_file(screenshot_path)
                result = "Fail"
        else:
            # Expected to fail
            if "Dashboard" not in title or "nopCommerce" not in title:
                logger.info(f"***Login correctly failed for {username} (as expected)***")
                result = "Pass"
            else:
                logger.error(f"***Login unexpectedly succeeded for {username}***")
                result = "Fail"
        
        # Write result back to Excel
        try:
            success = Excelutils.update_test_result(path, 'Sheet1', username, result)
            if success:
                logger.info(f"Result '{result}' written to Excel for {username}")
        except Exception as e:
            logger.error(f"Error writing result to Excel: {str(e)}")
            
        return result
        
    except Exception as e:
        logger.error(f"***Exception occurred during test: {str(e)}***")
        return "Error"
    finally:
        driver.quit()

def main():
    """Main function to run all tests from Excel data"""
    logger = LogGen.loggen()
    path = "/Users/sharanya/PycharmProjects/nopcommerce/testdata/testdata.xlsx"
    
    logger.info("****Starting Data-Driven Login Tests****")
    
    try:
        # Get test data from Excel
        test_data = Excelutils.get_data_as_list(path, 'Sheet1', skip_header=True)
        
        if not test_data:
            logger.error("No test data found in Excel file")
            return
        
        logger.info(f"Found {len(test_data)} test cases")
        
        # Run each test case
        passed = 0
        failed = 0
        
        for i, (username, password, expected_result) in enumerate(test_data, 1):
            logger.info(f"\n=== Running Test Case {i}/{len(test_data)} ===")
            result = run_login_test(username, password, expected_result)
            
            if result == "Pass":
                passed += 1
            else:
                failed += 1
        
        # Print summary
        logger.info(f"\n=== TEST SUMMARY ===")
        logger.info(f"Total Tests: {len(test_data)}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info("===================")
        
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")

if __name__ == "__main__":
    main()
