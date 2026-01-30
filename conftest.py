import pytest
from utils.driver_factory import DriverFactory


@pytest.fixture(scope="function")
def driver():
    driver = DriverFactory.get_driver()
    yield driver
    driver.quit()
