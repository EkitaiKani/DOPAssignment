from behave import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
WAIT_TIMEOUT = 10
BASE_URL = "http://127.0.0.1:5000"
CHROME_DRIVER_PATH = '/usr/bin/chromedriver'

def setup_chrome_options():
    """Configure Chrome options with best practices"""
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    return chrome_options

@given(u'Chrome browser is launch')
def step_impl(context):
    try:
        chrome_options = setup_chrome_options()
        service = Service(CHROME_DRIVER_PATH)
        context.driver = webdriver.Chrome(service=service, options=chrome_options)
        context.wait = WebDriverWait(context.driver, WAIT_TIMEOUT)
        logger.info("Chrome browser launched successfully")
    except WebDriverException as e:
        logger.error(f"Failed to launch Chrome browser: {str(e)}")
        raise

@given(u'Browser console logging is enabled for error tracking')
def step_impl(context):
    context.console_logs = []
    logger.info("Console logging enabled")

@when(u'Open Login Page')
def step_impl(context):
    try:
        context.driver.get(f"{BASE_URL}/login")
        context.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info("Login page loaded successfully")
    except TimeoutException:
        logger.error("Timeout while loading login page")
        raise

def wait_for_element(context, locator, timeout=WAIT_TIMEOUT):
    """Utility function to wait for and return an element"""
    try:
        element = WebDriverWait(context.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        logger.error(f"Element not found: {locator}")
        raise

@then('Verify page loads without console errors')
def step_verify_no_console_errors(context):
    browser_logs = context.driver.get_log('browser')
    errors = [log for log in browser_logs if log['level'] in ['SEVERE', 'ERROR']]
    
    # Log all console entries for debugging
    for log in browser_logs:
        logger.debug(f"Console log: {log}")
    
    if errors:
        for error in errors:
            logger.error(f"Console error: {error['message']}")
        raise AssertionError(f"Found {len(errors)} console errors")
    
    # Verify essential elements with custom wait function
    username_field = wait_for_element(context, (By.ID, "InputUsername"))
    password_field = wait_for_element(context, (By.ID, "InputPassword"))
    
    assert username_field.is_displayed(), "Username field not visible"
    assert password_field.is_displayed(), "Password field not visible"

@then(u'Verify Login title is present')
def step_impl(context):
    try:
        context.wait.until(EC.title_is("Student Login"))
        logger.info("Login title verified successfully")
    except TimeoutException:
        actual_title = context.driver.title
        logger.error(f"Expected title 'Student Login', got '{actual_title}'")
        raise

@then(u'Input username "{username}" and password "{password}"')
def step_impl(context, username, password):
    try:
        username_field = wait_for_element(context, (By.ID, "InputUsername"))
        password_field = wait_for_element(context, (By.ID, "InputPassword"))
        
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Credentials entered successfully")
    except Exception as e:
        logger.error(f"Failed to input credentials: {str(e)}")
        raise

@then(u'Submit form')
def step_impl(context):
    try:
        submit_button = wait_for_element(context, (By.ID, "login"))
        submit_button.click()
        time.sleep(1)  # Short wait for form submission
        logger.info("Form submitted successfully")
    except Exception as e:
        logger.error(f"Failed to submit form: {str(e)}")
        raise

@then(u'Verify student login')
def step_impl(context):
    try:
        context.wait.until(EC.url_to_be(f"{BASE_URL}/student"))
        logger.info("Student login verified successfully")
    except TimeoutException:
        current_url = context.driver.current_url
        logger.error(f"Failed to verify student login. Expected URL: {BASE_URL}/student, Got: {current_url}")
        raise

@then(u'Verify admin login')
def step_impl(context):
    try:
        context.wait.until(EC.url_to_be(f"{BASE_URL}/admin"))
        logger.info("Admin login verified successfully")
    except TimeoutException:
        current_url = context.driver.current_url
        logger.error(f"Failed to verify admin login. Expected URL: {BASE_URL}/admin, Got: {current_url}")
        raise

@then(u'Verify failed student login')
def step_impl(context):
    try:
        alert = context.wait.until(EC.alert_is_present())
        alert_text = alert.text
        assert "Invalid username" in alert_text, f"Expected 'Invalid username' in alert, got: {alert_text}"
        alert.accept()
        logger.info("Failed login verified successfully")
    except TimeoutException:
        logger.error("Alert not present for failed login")
        raise

@then(u'Close browser')
def step_impl(context):
    if hasattr(context, 'driver'):
        context.driver.quit()
        logger.info("Browser closed successfully")