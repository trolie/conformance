@skip_rate_limiting @temporary_aar_exceptions @auth
Feature: All Temporary AAR Exception requests require authentication
  As a Clearinghouse Operator
  I want to ensure that unauthenticated requests receive 401 Unauthorized
  when a client attempts to access any Temporary AAR Exception resources

  Background:
    Given a TROLIE client that has not been authenticated

  Scenario: List Temporary AAR Exceptions requires authorization
    When the client requests the list of Temporary AAR Exceptions
    Then the response is Unauthorized
    And the response is empty

  Scenario: Create Temporary AAR Exception requires authorization
    Given an empty body and no Content-Type specified
    When the client creates a Temporary AAR Exception
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Temporary AAR Exception by id requires authorization
    When the client requests a Temporary AAR Exception by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Delete Temporary AAR Exception requires authorization
    When the client deletes a Temporary AAR Exception by id
    Then the response is Unauthorized
    And the response is empty

  Scenario: Update Temporary AAR Exception requires authorization
    Given an empty body and no Content-Type specified
    When the client updates a Temporary AAR Exception by id
    Then the response is Unauthorized
    And the response is empty
