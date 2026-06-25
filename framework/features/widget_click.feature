Feature: DemoQA Widgets Interaction
  As a user
  I want to interact with the DemoQA widgets
  So that I can verify the functionality

  Scenario: Expand and collapse accordian sections
    Given I am on the DemoQA homepage
    When I navigate to the Widgets page
    And I click on the Accordian link
    And I expand the "Where does it come from?" section
    And I expand the "Why do we use it?" section
    And I click on the Interactions link
    Then the Interactions page should be displayed