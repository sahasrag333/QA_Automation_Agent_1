Feature: DemoQA Elements Interaction
  Scenario: Successful Click on Click Me Button
    Given the demoqa website is open
    When the Elements link is clicked
    And the Buttons option is selected
    And the Click Me button is clicked
    Then the Click Me button should be in a clicked state