import logging
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up logging
logger = logging.getLogger(__name__)

WAIT_TIMEOUT = 10
BASE_URL = "http://127.0.0.1:5000"  # Base URL for the app

def wait_for_element(context, locator, timeout=WAIT_TIMEOUT):
    """Wait for an element to be present on the page."""
    try:
        element = WebDriverWait(context.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except Exception as e:
        logger.error(f"Error waiting for element {locator}: {str(e)}")
        raise

# Step Definitions

@given(u'Chrome browser is launch')
def step_impl(context):
    """Ensure the browser is launched."""
    try:
        assert hasattr(context, 'driver'), "Driver not initialized"
        logger.info("Chrome browser launched successfully.")
    except AssertionError as e:
        logger.error("Driver initialization failed in 'Chrome browser is launch' step")
        raise

@given(u'Browser console logging is enabled for error tracking')
def step_impl(context):
    """Ensure console logs are enabled for tracking errors."""
    context.console_logs = []  # Clear any existing logs
    logger.info("Console logging enabled for error tracking.")

@when(u'Open Login Page')
def step_impl(context):
    """Open the login page of the application."""
    try:
        logger.info("Opening the login page.")
        context.driver.get(f"{BASE_URL}/login")
        wait_for_element(context, (By.ID, "InputUsername"))  # Wait for username field to be present
        wait_for_element(context, (By.ID, "InputPassword"))  # Wait for password field to be present
        logger.info("Login page opened successfully.")
    except Exception as e:
        logger.error(f"Failed to open login page: {str(e)}")
        raise

@then(u'Verify page loads without console errors')
def step_impl(context):
    """Verify the page loads without console errors."""
    try:
        # Check for browser console errors
        if hasattr(context, 'console_logs') and context.console_logs:
            errors = [log for log in context.console_logs if log['level'] in ['SEVERE', 'ERROR']]
            if errors:
                logger.error("Console Errors Found:")
                for error in errors:
                    logger.error(f"Error: {error['message']}")
                raise AssertionError(f"Found {len(errors)} console errors")
        
        # Verify essential elements are present on the page
        wait_for_element(context, (By.ID, "InputUsername"))
        wait_for_element(context, (By.ID, "InputPassword"))
        logger.info("Page loaded successfully without any console errors.")
    except Exception as e:
        logger.error(f"Failed to verify page load: {str(e)}")
        raise

@then(u'Close browser')
def step_impl(context):
    """Close the browser."""
    try:
        assert hasattr(context, 'driver'), "Driver not initialized"
        logger.info("Browser will be closed in after_scenario hook.")
    except AssertionError as e:
        logger.error("Driver not found during browser close step")
        raise
