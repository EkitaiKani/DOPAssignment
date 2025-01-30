from behave import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import tempfile

def step_impl(context):
    # Create a unique temporary directory for user data
    user_data_dir = tempfile.mkdtemp()

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Use a unique directory
    chrome_options.add_argument("--no-sandbox")  # Required for running in CI environments
    chrome_options.add_argument("--headless")  # Run in headless mode for CI

    # Launch Chrome with the specified options
    context.driver = webdriver.Chrome(options=chrome_options)

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

@then(u'Verify Login title is present')
def step_impl(context):
    title = context.driver.title
    assert title == "Student Login"

@then(u'Close browser')
def step_impl(context):
    context.driver.quit()
    
@then(u'Input username "{userName}" and password "{passWord}"')
def step_impl(context, userName, passWord):
    context.driver.find_element("id", "InputUsername").send_keys(userName)
    context.driver.find_element("id", "InputPassword").send_keys(passWord)
    
@then(u'Input multiple "{userName}" and "{passWord}"')
def step_impl(context, userName, passWord):
    context.driver.find_element("id", "InputUsername").send_keys(userName)
    context.driver.find_element("id", "InputPassword").send_keys(passWord)
    
@then(u'Submit form')
def step_impl(context):
    context.driver.find_element("css selector", "form button.btn.btn-primary").submit()
    time.sleep(5)
    
@then(u'Verify student login')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.url_contains("/student")
    )
    url = context.driver.current_url
    assert url == "http://127.0.0.1:5000/student", f"Expected URL: http://127.0.0.1:5000/student, Actual URL: {url}"

@then(u'Verify admin login')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.url_contains("/admin")
    )
    url = context.driver.current_url
    assert url == "http://127.0.0.1:5000/admin", f"Expected URL: http://127.0.0.1:5000/admin, Actual URL: {url}"


@then(u'Verify failed student login')
def step_impl(context):
    # Wait for alert
    wait = WebDriverWait(context.driver, 10)
    alert = wait.until(EC.alert_is_present())
    
    # Check alert text
    alert_text = alert.text
    assert "Invalid username" in alert_text
    
    # Dismiss alert
    alert.accept()
        
# @then(u'Check locked out')
# def step_impl(context):
#     error = context.driver.find_element(By.TAG_NAME, "h3").text
#     assert error == "Epic sadface: Sorry, this user has been locked out."
