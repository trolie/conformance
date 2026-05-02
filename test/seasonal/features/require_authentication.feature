@skip_rate_limiting @seasonal @auth
Feature: All Seasonal requests require authentication
  As a Clearinghouse Operator
  I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
  when a client attempts to access any Seasonal resources
  So that only authorized clients can access the system
  Without revealing any information about resources that may or may not exist

  Background:
    Given a TROLIE client that has not been authenticated

  Scenario: Get Seasonal Ratings Snapshot requires authorization
    When the client requests the current Seasonal Limits Snapshot
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Seasonal Rating Proposal Status requires authorization
    When the client requests the Seasonal Rating Proposal Status
    Then the response is Unauthorized
    And the response is empty

  Scenario: Submit a Seasonal Ratings Proposal requires authorization
    Given an empty body and no Content-Type specified
    When the client submits a Seasonal Ratings Proposal
    Then the response is Unauthorized
    And the response is empty
