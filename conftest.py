import pytest
from utils.driver_factory import DriverFactory
from utils.logger import Logger
import os
from datetime import datetime


logger = Logger.get_logger("framework")


@pytest.fixture(scope="function")
def driver(request):
    driver = DriverFactory.get_driver()
    yield driver

    # After test execution
    if request.node.rep_call.failed:
        take_screenshot(driver, request.node.name)

    driver.quit()


def take_screenshot(driver, test_name):
    screenshot_dir = os.path.join(
        os.path.dirname(__file__),
        "screenshots"
    )

    os.makedirs(screenshot_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{test_name}_{timestamp}.png"

    file_path = os.path.join(screenshot_dir, file_name)

    driver.save_screenshot(file_path)

    logger.info(f"Screenshot saved: {file_path}")


# Pytest hook to get test result
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)
