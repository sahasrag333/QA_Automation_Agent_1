Feature: Book Store Application Navigation
  As a user
  I want to navigate through the book store application
  So that I can access the book details

  Scenario: Successful navigation to book details
    Given I am on the demoqa homepage
    When I click on the book store application link
    Then I should be on the book store application page
    When I click on the profile link
    Then I should be on the profile page
    When I click on the profile link again
    Then I should still be on the profile page
    When I click on the book store link
    Then I should be on the book store page
    When I click on the you dont know js book link
    Then I should be on the you dont know js book details page