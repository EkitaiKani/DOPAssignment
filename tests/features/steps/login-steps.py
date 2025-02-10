from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import common_steps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use constants from common_steps
WAIT_TIMEOUT = common_steps.WAIT_TIMEOUT
BASE_URL = common_steps.BASE_URL

# Step Definitions
@then(u'Verify Login title is present')
def step_impl(context):
    try:
        context.wait.until(EC.title_is("Student Login"))
        logger.info("Login title verified successfully")
    except TimeoutException:
        actual_title = context.driver.title
        logger.error(f"Expected title 'Student Login', got '{actual_title}'")
        raise

@then(u'Input userName "{username}" and passWord "{password}"')
def step_impl(context, username, password):
    """Input username and password into the login form."""
    try:
        # Wait for the username and password fields to be present
        username_field = common_steps.wait_for_element(context, (By.ID, "InputUsername"))
        password_field = common_steps.wait_for_element(context, (By.ID, "InputPassword"))
        
        # Clear and input credentials
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        logger.info(f"Credentials entered successfully: {username} / {password}")
    except Exception as e:
        logger.error(f"Failed to input credentials: {str(e)}")
        raise

@then(u'Input multiple "{userName}" and "{passWord}"')
def step_impl(context, userName, passWord):
    """Input multiple sets of credentials into the login form."""
    try:
        # Wait for the username and password fields to be present
        username_field = common_steps.wait_for_element(context, (By.ID, "InputUsername"))
        password_field = common_steps.wait_for_element(context, (By.ID, "InputPassword"))
        
        # Clear and input credentials for each user
        username_field.clear()
        username_field.send_keys(userName)
        password_field.clear()
        password_field.send_keys(passWord)
        
        logger.info(f"Entered credentials for multiple users: {userName} / {passWord}")
    except Exception as e:
        logger.error(f"Failed to input credentials for multiple users: {str(e)}")
        raise

@then(u'Submit form')
def step_impl(context):
    """Submit the login form."""
    try:
        submit_button = common_steps.wait_for_element(context, (By.ID, "login"))
        submit_button.click()
        time.sleep(1)  # Short wait for form submission (can be replaced with an explicit wait)
        logger.info("Form submitted successfully")
    except Exception as e:
        logger.error(f"Failed to submit form: {str(e)}")
        raise

@then(u'Verify student login')
def step_impl(context):
    """Verify if the student login is successful."""
    try:
        context.wait.until(EC.url_to_be(f"{BASE_URL}/student"))
        logger.info("Student login verified successfully")
    except TimeoutException:
        current_url = context.driver.current_url
        logger.error(f"Failed to verify student login. Expected URL: {BASE_URL}/student, Got: {current_url}")
        raise

@then(u'Verify failed student login')
def step_impl(context):
    """Verify if the login failed with the expected error message."""
    try:
        # Check for alert presence (if login fails)
        alert = context.wait.until(EC.alert_is_present())
        alert_text = alert.text
        assert "Invalid username" in alert_text, f"Expected 'Invalid username' in alert, but got: {alert_text}"
        alert.accept()
        logger.info("Failed login verified successfully")
    except TimeoutException:
        logger.error("Alert not present for failed login")
        raise

@then(u'Verify admin login')
def step_impl(context):
    """Verify if the admin login is successful."""
    try:
        context.wait.until(EC.url_to_be(f"{BASE_URL}/admin"))
        logger.info("Admin login verified successfully")
    except TimeoutException:
        current_url = context.driver.current_url
        logger.error(f"Failed to verify admin login. Expected URL: {BASE_URL}/admin, Got: {current_url}")
        raise
