Feature: Verify Login is valid

    Background: Common steps
        Given Chrome browser is launch
        And Browser console logging is enabled for error tracking
        When Open Login Page
        Then Verify page loads without console errors

	Scenario: Check Login title
		Then    Verify Login title is present
		And     Close browser

	Scenario: Fill in student login with one incorrect userName data
		Then    Input userName "A1234567X" and passWord "password1"
		And     Submit form
		And     Verify failed student login
		And     Close browser

	Scenario: Fill in admin login with one correct user data
		Then    Input userName "Admin" and passWord "supersecretpassword"
		And     Submit form
		And     Verify admin login
		And     Close browser

	Scenario Outline: Fill in student login with multiple correct user data
		Then    Input multiple "<userName>" and "<passWord>"
		And     Submit form
		And     Verify student login
		And     Close browser

		Examples:
			|userName|passWord|
			|John Tan|password1| 
			|Sarah Lim|password2|
