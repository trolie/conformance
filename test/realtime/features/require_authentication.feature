@skip_rate_limiting @realtime @auth
Feature: All Real-Time requests require authentication
  As a Clearinghouse Operator
  I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
  when a client attempts to access any Real-Time resources
  So that only authorized clients can access the system
  Without processing the request beyond the authentication step
  and without revealing any information about resources that may or may not exist

  Background:
    Given a TROLIE client that has not been authenticated

  Scenario: Get Real-Time Limits Snapshot requires authorization
    When the client requests for the current real-time snapshot
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Regional Real-Time Limits Snapshot requires authorization
    When the client requests for the current regional real-time snapshot
    Then the response is Unauthorized
    And the response is empty

  Scenario: Get Real-Time Proposal Status requires authorization
    When the client requests for the current real-time proposal status
    Then the response is Unauthorized
    And the response is empty

  Scenario: Submit Real-Time Rating Proposal requires authorization
    Given an empty body and no Content-Type specified
    When the client submits a real-time rating proposal
    Then the response is Unauthorized
    And the response is empty
