Feature: Verify Login is valid

	Background: Common steps
		Given   Chrome browser is launch
		When    Open Login Page

	Scenario: Check Login title
		Then    Verify Login title is present
		And     Close browser

	Scenario: Fill in login with one incorrect user data
		Then    Input userName "A1234567X" and passWord "password1"
		And     Submit form
		And     Verify failed login
		And     Close browser

	Scenario Outline: Fill in login with multiple correct user data
		Then    Input multiple "<userName>" and "<passWord>"
		And     Submit form
		And     Verify login
		And     Close browser

		Examples:
			|userName|passWord|
			|John Tan|password1| 
			|Sarah Lim|password2|
            |Admin|supersecretpassword|
