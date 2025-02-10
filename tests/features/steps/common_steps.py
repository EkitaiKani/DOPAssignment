from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Constants
WAIT_TIMEOUT = 10
BASE_URL = "http://127.0.0.1:5000"

def setup_chrome_options():
    """Configure Chrome options for headless mode, no GPU, etc."""
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    return chrome_options

def setup_chrome_driver():
    """Initialize Chrome WebDriver with options."""
    try:
        chrome_options = setup_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Chrome driver: {str(e)}")
        raise

def wait_for_element(context, locator, timeout=WAIT_TIMEOUT):
    """Wait for an element to be present."""
    return WebDriverWait(context.driver, timeout).until(
        EC.presence_of_element_located(locator),
        message=f"Element {locator} not found after {timeout} seconds"
    )

def clear_console_logs(context):
    """Clear existing browser console logs."""
    if hasattr(context, 'console_logs'):
        context.console_logs = []

def log_console_errors(context):
    """Log browser console errors for later analysis."""
    if not hasattr(context, 'driver'):
        logger.error("Driver not initialized when attempting to log console errors")
        return None

    browser_logs = context.driver.get_log('browser')
    if not hasattr(context, 'console_logs'):
        context.console_logs = []
    context.console_logs.extend(browser_logs)
    
    errors = [log for log in browser_logs if log['level'] in ['SEVERE', 'ERROR']]
    if errors:
        logger.error("Console Errors Found:")
        for error in errors:
            logger.error(f"Browser Error: {error['message']}")
        return errors
    return None

# Environment hooks - Move these to environment.py
def before_all(context):
    """Initialize global context settings"""
    context.config.setup_logging()

def before_scenario(context, scenario):
    """Initialize browser before each scenario"""
    try:
        if not hasattr(context, 'driver'):
            context.driver = setup_chrome_driver()
            context.wait = WebDriverWait(context.driver, WAIT_TIMEOUT)
            logger.info(f"WebDriver initialized for scenario: {scenario.name}")
    except Exception as e:
        logger.error(f"Failed to initialize scenario: {str(e)}")
        raise

def after_scenario(context, scenario):
    """Clean up after each scenario"""
    try:
        if hasattr(context, 'driver'):
            context.driver.quit()
            delattr(context, 'driver')
            logger.info(f"WebDriver cleaned up for scenario: {scenario.name}")
    except Exception as e:
        logger.error(f"Error in after_scenario cleanup: {str(e)}")

# Step definitions
@given(u'Chrome browser is launch')
def step_impl(context):
    try:
        assert hasattr(context, 'driver'), "Driver not initialized"
        logger.info("Chrome browser launched successfully")
    except AssertionError as e:
        logger.error("Driver initialization failed in 'Chrome browser is launch' step")
        raise

@given(u'Browser console logging is enabled for error tracking')
def step_impl(context):
    clear_console_logs(context)
    logger.info("Console logging enabled")

@when(u'Open Login Page')
def step_impl(context):
    try:
        assert hasattr(context, 'driver'), "Driver not initialized"
        context.driver.get(f"{BASE_URL}/login")
        logger.info("Navigated to login page")
    except Exception as e:
        logger.error(f"Failed to open login page: {str(e)}")
        raise

@then(u'Verify page loads without console errors')
def step_impl(context):
    try:
        assert hasattr(context, 'driver'), "Driver not initialized"
        errors = log_console_errors(context)
        if errors:
            raise AssertionError(f"Found {len(errors)} console errors")

        # Verify essential elements are present
        wait_for_element(context, (By.ID, "InputUsername"))
        wait_for_element(context, (By.ID, "InputPassword"))
        logger.info("Page loaded successfully without console errors")
    except Exception as e:
        logger.error(f"Page verification failed: {str(e)}")
        raise

@then(u'Close browser')
def step_impl(context):
    try:
        assert hasattr(context, 'driver'), "Driver not initialized"
        logger.info("Browser will be closed in after_scenario hook")
    except AssertionError as e:
        logger.error("Driver not found during browser close step")
        raise