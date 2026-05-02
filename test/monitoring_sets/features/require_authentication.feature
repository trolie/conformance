@skip_rate_limiting @monitoring_sets @auth
Feature: All Monitoring Set requests require authentication
  As a Clearinghouse Operator
  I want to ensure that unauthenticated requests receive 401 Unauthorized
  when a client attempts to access any Monitoring Set resources

  Background:
    Given a TROLIE client that has not been authenticated

  Scenario: Create Monitoring Set requires authorization
    Given an empty body and no Content-Type specified
    When the client creates a Monitoring Set
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Monitoring Set by id requires authorization
    When the client requests a Monitoring Set by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Update Monitoring Set requires authorization
    Given an empty body and no Content-Type specified
    When the client updates a Monitoring Set by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Delete Monitoring Set requires authorization
    When the client deletes a Monitoring Set by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Default Monitoring Set requires authorization
    When the client requests the Default Monitoring Set
    Then the response is Unauthorized
    And the response is empty
