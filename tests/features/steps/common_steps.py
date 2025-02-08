from behave import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

@given(u'Chrome browser is launch')
def step_impl(context):
    context.driver = webdriver.Chrome()

@given(u'Browser console logging is enabled for error tracking')
def step_impl(context):
    # Clear existing logs
    context.console_logs = []

@when(u'Open Login Page')
def step_impl(context):
    context.driver.get("http://127.0.0.1:5000/login")
    
@then('Verify page loads without console errors')
def step_verify_no_console_errors(context):
    # Get browser console logs
    browser_logs = context.driver.get_log('browser')
    wait = WebDriverWait(context.driver, 10)

    
    # Filter for severe errors
    errors = [
        log for log in browser_logs 
        if log['level'] in ['SEVERE', 'ERROR']
    ]
    
    # Store logs for later analysis
    context.console_logs.extend(browser_logs)
    
    # Assert no severe errors
    if errors:
        print("Console Errors Found:")
        for error in errors:
            print(f"Error: {error['message']}")
        assert False, f"Found {len(errors)} console errors"
    
    # Verify essential elements are present
    assert wait.until(
        EC.presence_of_element_located((By.ID, "InputUsername"))
    ), "Username field not found"
    
    assert wait.until(
        EC.presence_of_element_located((By.ID, "InputPassword"))
    ), "Password field not found"
