Feature: DemoQA Elements Interaction
  Scenario: Successful checkbox selection
    Given the demoqa website is open
    When the elements link is clicked
    And the check box link is clicked
    And the select home checkbox is clicked
    Then the select home checkbox should be selected