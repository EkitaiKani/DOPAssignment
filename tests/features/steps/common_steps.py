from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os

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
    chrome_options = setup_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_for_element(context, locator, timeout=WAIT_TIMEOUT):
    """Wait for an element to be present."""
    return WebDriverWait(context.driver, timeout).until(
        EC.presence_of_element_located(locator),
        message=f"Element {locator} not found after {timeout} seconds"
    )

def clear_console_logs(context):
    """Clear existing browser console logs."""
    context.console_logs = []

def log_console_errors(context):
    """Log browser console errors for later analysis."""
    browser_logs = context.driver.get_log('browser')
    context.console_logs.extend(browser_logs)
    
    errors = [log for log in browser_logs if log['level'] in ['SEVERE', 'ERROR']]
    if errors:
        print("Console Errors Found:")
        for error in errors:
            print(f"Error: {error['message']}")
        return errors
    return None

# Step definitions
@given(u'Chrome browser is launch')
def step_impl(context):
    context.driver = setup_chrome_driver()
    context.wait = WebDriverWait(context.driver, WAIT_TIMEOUT)

@given(u'Browser console logging is enabled for error tracking')
def step_impl(context):
    clear_console_logs(context)

@when(u'Open Login Page')
def step_impl(context):
    context.driver.get(f"{BASE_URL}/login")
    
@then(u'Verify page loads without console errors')
def step_impl(context):
    # Get browser console errors
    errors = log_console_errors(context)
    if errors:
        assert False, f"Found {len(errors)} console errors"

    # Verify essential elements are present
    try:
        context.wait.until(EC.presence_of_element_located((By.ID, "InputUsername")))
        context.wait.until(EC.presence_of_element_located((By.ID, "InputPassword")))
    except TimeoutException:
        assert False, "Username or Password field not found on the login page"
