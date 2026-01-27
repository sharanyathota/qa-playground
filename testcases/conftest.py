import html

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import pytest
from py.xml import html


@pytest.fixture()
def setup(request):
    browser = request.config.getoption("--browser", default="chrome").lower()

    if browser == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(5)
    try:
        driver.maximize_window()
    except Exception:
        pass  # Safari may not support maximize

    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to use for tests"
    )

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


#pytest html reports
def pytest_configure(config):
    if hasattr(config, 'metadata'):
        config.metadata['Project Name'] = 'nopcommerce'
        config.metadata['module Name'] = 'commerce'
        config.metadata['testet Name'] = 'sharanya'

def pytest_html_report_title(report):
    report.title = "nopcommerce Test Results"

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append(html.p("Project Name: nopcommerce"))



