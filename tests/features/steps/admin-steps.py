from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import common_steps

# Constants for actions
WAIT_TIMEOUT = 10
BASE_URL = "http://127.0.0.1:5000"

def before_all(context):
    """Initialize the WebDriver before all tests."""
    context.driver = common_steps.setup_chrome_driver()  # Fix here
    context.wait = WebDriverWait(context.driver, WAIT_TIMEOUT)

def after_all(context):
    """Quit the WebDriver after all tests."""
    context.driver.quit()

@given('I am logged in as an admin')
def step_impl(context):
    """Login as an admin."""
    context.driver.find_element(By.ID, "InputUsername").send_keys("Admin")
    context.driver.find_element(By.ID, "InputPassword").send_keys("supersecretpassword")
    context.driver.find_element(By.ID, "login").click() 
    WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.title_is("Admin")
    )

@then('I should see a list of all student accounts')
def step_impl(context):
    """Verify the student list is displayed."""
    students_table = common_steps.wait_for_element(context, (By.ID, "students-table"))
    assert students_table.is_displayed(), "Students table is not displayed"

@given('I enter studentID, "{student_id}" into the search bar')
def step_impl(context, student_id):
    """Enter student ID into the search bar."""
    search_bar = context.driver.find_element(By.ID, "search-bar")
    search_bar.send_keys(student_id)
    assert search_bar.get_attribute("value") == student_id, f"Expected student ID '{student_id}' to be in the search bar, but found '{search_bar.get_attribute('value')}'"

@given('I enter username, "{student_name}" into the search bar')
def step_impl(context, student_name):
    """Enter student name into the search bar."""
    search_bar = context.driver.find_element(By.ID, "search-bar")
    search_bar.send_keys(student_name)
    assert search_bar.get_attribute("value") == student_name, f"Expected student name '{student_name}' to be in the search bar, but found '{search_bar.get_attribute('value')}'"

@then('the search results should show the student "{student_name}"')
def step_impl(context, student_name):
    """Verify search results show the correct student."""
    students_table = WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "students-table"))
    )
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    assert len(rows) > 1, "No student accounts found in the search results"

    first_row = rows[1]
    columns = first_row.find_elements(By.TAG_NAME, "td")
    assert columns[1].text == student_name, f"Expected student name '{student_name}' in second column, but found '{columns[1].text}'"

@given('I click on create student account')
def step_impl(context):
    """Click the button to create a student account."""
    create_student_button = WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "create-student"))
    )
    create_student_button.click()
    WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.title_is("Create Student")
    )

@given('I enter student details')
def step_impl(context):
    """Fill in student details for creating or updating the student."""
    context.driver.find_element(By.ID, "studentid").send_keys("S12345")
    context.driver.find_element(By.ID, "username").send_keys("John Doe")
    context.driver.find_element(By.ID, "points").send_keys("50")
    context.driver.find_element(By.ID, "password").send_keys("password123")
    context.driver.find_element(By.ID, "diplomaofstudy").send_keys("BSc Computer Science")
    context.driver.find_element(By.ID, "yearofentry").send_keys("2025")
    context.driver.find_element(By.ID, "emailaddress").send_keys("johndoe@example.com")

@given('I submit the form')
def step_impl(context):
    """Submit the student creation form."""
    create_student_button = context.driver.find_element(By.ID, "createStudent")
    create_student_button.click()
    WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.alert_is_present()
    )
    alert = context.driver.switch_to.alert
    alert_message = alert.text
    assert alert_message == "Student created successfully!", f"Expected alert message 'Student created successfully!', but got '{alert_message}'"
    alert.accept()

@then('the student "{student_name}" should be added to the student list')
def step_impl(context, student_name):
    """Verify the student was added to the student list."""
    students_table = context.driver.find_element(By.ID, "students-table")
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns[1].text == student_name:
            return
    assert False, f"Student '{student_name}' not found in the student list"

@given('I choose to delete student "{student_name}"')
def step_impl(context, student_name):
    """Choose to delete a student."""
    students_table = WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "students-table"))
    )
    rows = students_table.find_elements(By.TAG_NAME, "tr")

    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns and student_name in [col.text for col in columns]:
            try:
                delete_button = row.find_element(By.ID, "deleteStudent") 
                delete_button.click()
                return
            except Exception as e:
                assert False, f"Failed to click 'Delete' button for student '{student_name}': {str(e)}"

    assert False, f"Student '{student_name}' not found in the student list"

@when('I confirm deletion')
def step_impl(context):
    """Confirm the deletion of a student."""
    WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.alert_is_present()
    )
    alert = context.driver.switch_to.alert
    alert_message = alert.text
    assert alert_message == "Are you sure you want to delete this student?", f"Expected alert message 'Are you sure you want to delete this student?', but got '{alert_message}'"
    alert.accept()

@then('the student "{student_name}" should no longer be in the student list')
def step_impl(context, student_name):
    """Verify the student was removed from the student list."""
    WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.staleness_of(context.driver.find_element(By.ID, "students-table"))
    )
    students_table = WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "students-table"))
    )
    rows = students_table.find_elements(By.TAG_NAME, "tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns and student_name in [col.text for col in columns]:
            assert False, f"Student '{student_name}' is still in the student list after deletion"
