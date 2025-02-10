from behave import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import common_steps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use constants from common_steps
WAIT_TIMEOUT = common_steps.WAIT_TIMEOUT
BASE_URL = common_steps.BASE_URL


@given('I am logged in as an admin')
def step_impl(context):
    common_steps.wait_for_element(context, (By.ID, "InputUsername")).send_keys("Admin")
    common_steps.wait_for_element(context, (By.ID, "InputPassword")).send_keys("supersecretpassword")
    common_steps.wait_for_element(context, (By.ID, "login")).click()
    WebDriverWait(context.driver, 10).until(EC.title_is("Admin"))

@then('I should see a list of all student accounts')
def step_impl(context):
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    assert students_table.is_displayed(), "Students table is not displayed"

@given('I enter studentID, "{student_id}" into the search bar')
def step_impl(context, student_id):
    search_bar = common_steps.wait_for_element(context, (By.ID, "search-bar"))
    search_bar.send_keys(student_id)
    assert search_bar.get_attribute("value") == student_id, "Student ID mismatch"

@given('I enter username, "{student_name}" into the search bar')
def step_impl(context, student_name):
    search_bar = common_steps.wait_for_element(context, (By.ID, "search-bar"))
    search_bar.send_keys(student_name)
    assert search_bar.get_attribute("value") == student_name, "Student name mismatch"

@then('the search results should show the student "{student_name}"')
def step_impl(context, student_name):
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    assert len(rows) > 1, "No student accounts found"
    first_row = rows[1]
    columns = first_row.find_elements(By.TAG_NAME, "td")
    assert columns[1].text == student_name, "Student name mismatch in results"

@given('I click on create student account')
def step_impl(context):
    create_student_button = common_steps.wait_for_element(context, (By.ID, "create-student"))
    create_student_button.click()
    WebDriverWait(context.driver, 10).until(EC.title_is("Create Student"))

@given('I enter "Student ID" as "{student_id}"')
def step_impl(context, student_id):
    student_id_input = common_steps.wait_for_element(context, (By.ID, "studentid"))  
    student_id_input.clear()
    student_id_input.send_keys(student_id)

@given('I enter "Student Name" as "{student_name}"')
def step_impl(context, student_name):
    student_name_input = common_steps.wait_for_element(context, (By.ID, "username"))  
    student_name_input.clear()
    student_name_input.send_keys(student_name)

@given('I enter "Student current points" as "{points}"')
def step_impl(context, points):
    points_input = common_steps.wait_for_element(context, (By.ID, "points"))
    points_input.clear()
    points_input.send_keys(points)

@given('I enter "Username" as "{username}"')
def step_impl(context, username):
    username_input = common_steps.wait_for_element(context, (By.ID, "username"))
    username_input.clear()
    username_input.send_keys(username)

@given('I enter "Password" as "{password}"')
def step_impl(context, password):
    password_input = common_steps.wait_for_element(context, (By.ID, "password"))
    password_input.clear()
    password_input.send_keys(password)

@given('I enter "Diploma of Study" as "{diploma}"')
def step_impl(context, diploma):
    diploma_input = common_steps.wait_for_element(context, (By.ID, "diplomaofstudy")) 
    diploma_input.clear()
    diploma_input.send_keys(diploma)

@given('I enter "Year of Entry" as "{year_of_entry}"')
def step_impl(context, year_of_entry):
    year_input = common_steps.wait_for_element(context, (By.ID, "yearofentry"))
    year_input.clear()
    year_input.send_keys(year_of_entry)

@given('I enter "Email Address" as "{email}"')
def step_impl(context, email):
    email_input = common_steps.wait_for_element(context, (By.ID, "emailaddress"))
    email_input.clear()
    email_input.send_keys(email)

@given('I submit the form')
def step_impl(context):
    create_student_button = common_steps.wait_for_element(context, (By.ID, "createStudent"))
    create_student_button.click()
    WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    alert = context.driver.switch_to.alert
    assert alert.text == "Student created successfully!", "Alert message mismatch"
    alert.accept()

@then('the student "{student_name}" should be added to the student list')
def step_impl(context, student_name):
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns[1].text == student_name:
            return
    assert False, f"Student '{student_name}' not found in the student list"

@given('I choose to edit student "{student_name}"')
def step_impl(context, student_name):
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns and student_name in [col.text for col in columns]:
            try:
                edit_button = row.find_element(By.ID, "editStudent")
                edit_button.click()
                WebDriverWait(context.driver, 10).until(EC.title_is("Edit Student"))
                return
            except Exception as e:
                assert False, f"Failed to click 'Edit' button for student '{student_name}': {str(e)}'"
    assert False, f"Student '{student_name}' not found in the student list"

@given('I update the diploma of study to "{diploma}"')
def step_impl(context, diploma):
    diploma_input = common_steps.wait_for_element(context, (By.ID, "diplomaofstudy"))
    diploma_input.clear()
    diploma_input.send_keys(diploma)

@given('I save the changes')
def step_impl(context):
    edit_student_button = common_steps.wait_for_element(context, (By.ID, "editStudent"))
    edit_student_button.click()
    WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    alert = context.driver.switch_to.alert
    alert_message = alert.text
    assert alert_message == "Student updated successfully!", f"Expected alert message 'Student updated successfully!', but got '{alert_message}'"
    alert.accept()
    context.driver.get("http://127.0.0.1:5000/admin")

@then('the student "{student_name}" should be in "{diploma}" as his diploma of study')
def step_impl(context, student_name, diploma):
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns and student_name in [col.text for col in columns]:
            try:
                assert columns[2].text == diploma, f"Expected diploma '{diploma}', but found '{columns[2].text}'"
                return
            except AssertionError as e:
                assert False, str(e)
    assert False, f"Student '{student_name}' not found in the student list"

@given('I choose to delete student "{student_name}"')
def step_impl(context, student_name):
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns and student_name in [col.text for col in columns]:
            try:
                delete_button = row.find_element(By.ID, "deleteStudent")
                delete_button.click()
                return
            except Exception as e:
                assert False, f"Failed to click 'Delete' button for student '{student_name}': {str(e)}'"
    assert False, f"Student '{student_name}' not found in the student list"

@when('I confirm deletion')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    alert = context.driver.switch_to.alert
    alert_message = alert.text
    assert alert_message == "Are you sure you want to delete this student?", f"Expected alert message 'Are you sure you want to delete this student?', but got '{alert_message}'"
    alert.accept()

@then('the student "{student_name}" should no longer be in the student list')
def step_impl(context, student_name):
    WebDriverWait(context.driver, 10).until(EC.staleness_of(common_steps.wait_for_element(context, (By.ID, "students-table"))))
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns and student_name in [col.text for col in columns]:
            assert False, f"Student '{student_name}' is still in the student list after deletion"
