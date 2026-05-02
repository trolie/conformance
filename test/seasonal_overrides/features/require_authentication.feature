@skip_rate_limiting @seasonal_overrides @auth
Feature: All Seasonal Override requests require authentication
  As a Clearinghouse Operator
  I want to ensure that unauthenticated requests receive 401 Unauthorized
  when a client attempts to access any Seasonal Override resources

  Background:
    Given a TROLIE client that has not been authenticated

  Scenario: List Seasonal Overrides requires authorization
    When the client requests the list of Seasonal Overrides
    Then the response is Unauthorized
    And the response is empty

  Scenario: Create Seasonal Override requires authorization
    Given an empty body and no Content-Type specified
    When the client creates a Seasonal Override
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Seasonal Override by id requires authorization
    When the client requests a Seasonal Override by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Delete Seasonal Override requires authorization
    When the client deletes a Seasonal Override by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Update Seasonal Override requires authorization
    Given an empty body and no Content-Type specified
    When the client updates a Seasonal Override by id
    Then the response is Unauthorized
    And the response is empty
