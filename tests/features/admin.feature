Feature: Admin Page Features

    Background: Common steps
        Given Chrome browser is launch
        And Browser console logging is enabled for error tracking
        When Open Login Page
        Then Verify page loads without console errors

    Scenario: Admin lists all student accounts
        Given I am logged in as an admin
        Then I should see a list of all student accounts
    
    #Scenario: Admin searches for a student account by Student ID
    #    Given I am logged in as an admin
    #    And I enter studentID, "A1234567X" into the search bar
    #    Then the search results should show the student "John Tan"

    Scenario: Admin searches for a student account by Student Name
        Given I am logged in as an admin
        And I enter username, "John Tan" into the search bar
        Then the search results should show the student "John Tan"

    Scenario: Admin creates a new student account
        Given I am logged in as an admin
        And I click on create student account
        And I enter "Student ID" as "A99999999Y"
        And I enter "Student Name" as "John Pork"
        And I enter "Student current points" as "100"
        And I enter "Username" as "John Pork"
        And I enter "Password" as "securepassword123"
        And I enter "Diploma of Study" as "Diploma in Business"
        And I enter "Year of Entry" as "2024"
        And I enter "Email Address" as "johnpork@test.com"
        And I submit the form
        Then the student "John Pork" should be added to the student list

    Scenario: Admin modifies a student account
        Given I am logged in as an admin
        And I choose to edit student "John Tan"
        And I update the diploma of study to "Diploma in Business"
        And I save the changes
        Then the student "John Tan" should be in "Diploma in Business" as his diploma of study

    Scenario: Admin deletes a student account
        Given I am logged in as an admin
        And I choose to delete student "John Pork"
        When I confirm deletion
        Then the student "John Pork" should no longer be in the student list
