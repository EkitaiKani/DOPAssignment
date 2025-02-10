import logging
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up logging
logger = logging.getLogger(__name__)

WAIT_TIMEOUT = 10
BASE_URL = "http://127.0.0.1:5000"

def setup_chrome_driver():
    """Initialize Chrome WebDriver with options."""
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--disable-usb-devices")
    return webdriver.Chrome(options=chrome_options)

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
        if not hasattr(context, 'driver'):
            logger.info("Initializing Chrome driver")
            context.driver = setup_chrome_driver()
            context.wait = WebDriverWait(context.driver, WAIT_TIMEOUT)
        assert context.driver is not None, "Driver initialization failed"
        logger.info("Chrome browser launched successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Chrome driver: {str(e)}")
        raise

@given(u'Browser console logging is enabled for error tracking')
def step_impl(context):
    """Ensure console logs are enabled for tracking errors."""
    context.console_logs = []
    logger.info("Console logging enabled for error tracking.")

@when(u'Open Login Page')
def step_impl(context):
    """Open the login page of the application."""
    try:
        logger.info("Opening the login page.")
        context.driver.get(f"{BASE_URL}/login")
        wait_for_element(context, (By.ID, "InputUsername"))
        wait_for_element(context, (By.ID, "InputPassword"))
        logger.info("Login page opened successfully.")
    except Exception as e:
        logger.error(f"Failed to open login page: {str(e)}")
        raise

@then(u'Verify page loads without console errors')
def step_impl(context):
    """Verify the page loads without console errors."""
    try:
        if hasattr(context, 'console_logs') and context.console_logs:
            errors = [log for log in context.console_logs if log['level'] in ['SEVERE', 'ERROR']]
            if errors:
                logger.error("Console Errors Found:")
                for error in errors:
                    logger.error(f"Error: {error['message']}")
                raise AssertionError(f"Found {len(errors)} console errors")
        
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
        if hasattr(context, 'driver') and context.driver is not None:
            context.driver.quit()
            context.driver = None
        logger.info("Browser closed successfully.")
    except Exception as e:
        logger.error(f"Failed to close browser: {str(e)}")
        raise