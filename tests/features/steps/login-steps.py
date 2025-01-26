from behave import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

@given(u'Chrome browser is launch')
def step_impl(context):
    context.driver = webdriver.Chrome()

@when(u'Open Login Page')
def step_impl(context):
    context.driver.get("http://127.0.0.1:5000/login")

@then(u'Verify Login title is present')
def step_impl(context):
    title = context.driver.title
    assert title == "Student Login"

@then(u'Close browser')
def step_impl(context):
    context.driver.close
    
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
    
@then(u'Verify login')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.url_contains("/student")
    )
    url = context.driver.current_url
    assert url == "http://127.0.0.1:5000/student", f"Expected URL: http://127.0.0.1:5000/student, Actual URL: {url}"

@then(u'Verify failed login')
def step_impl(context):
    # Wait for alert
    wait = WebDriverWait(context.driver, 10)
    alert = wait.until(EC.alert_is_present())
    
    # Check alert text (optional)
    alert_text = alert.text
    assert "Login failed" in alert_text
    
    # Dismiss alert
    alert.accept()
        
# @then(u'Check locked out')
# def step_impl(context):
#     error = context.driver.find_element(By.TAG_NAME, "h3").text
#     assert error == "Epic sadface: Sorry, this user has been locked out."
