from behave import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import common_steps
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
    
@then(u'Input multiple "{userName}" and "{passWord}"')
def step_impl(context, userName, passWord):
    try:
        username_field = wait_for_element(context, (By.ID, "InputUsername"))
        password_field = wait_for_element(context, (By.ID, "InputPassword"))
        
        username_field.clear()
        username_field.send_keys(userName)
        password_field.clear()
        password_field.send_keys(passWord)
        
        logger.info(f"Entered credentials: {userName} / {passWord}")
    except Exception as e:
        logger.error(f"Failed to input credentials for multiple users: {str(e)}")
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