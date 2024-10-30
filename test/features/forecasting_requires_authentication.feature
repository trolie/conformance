
Feature: All Forecasting requests require authentication
  As a Clearinghouse Operator
  I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
  when a client attempts to access any Forecasting resources
  So that only authorized clients can access the system
  Without processing the request beyond the authentication step
  and without revealing any information about resources that may or may not exist
  
  Background:
    Given a TROLIE client that has not been authenticated


  Scenario: Get Forecast Limits Snapshot requires authorization
    When the client requests the current Forecast Limits Snapshot
    Then the response is Unauthorized

  Scenario: Get Historical Forecast Limits Snapshot requires authorization
    When the client requests a Historical Forecast Limits Snapshot
    Then the response is Unauthorized

  Scenario: Get Regional Forecast Limits Snapshot requires authorization
    When the client requests a Regional Forecast Limits Snapshot
    Then the response is Unauthorized
  
  Scenario: Updating the Regional Forecast Limits Snapshot requires authorization
    Given an empty body and no Content-Type specified
    When the client submits a Regional Forecast Limits Snapshot
    Then the response is Unauthorized

  Scenario: Submitting a Forecast Proposal requires authorization
    Given an empty body and no Content-Type specified
    When the client submits a Forecast Proposal
    Then the response is Unauthorized

  Scenario: Obtain Forecast Proposal Status requires authorization
    Given an empty body and no Content-Type specified
    And a Forecast Proposal ID which may or may not exist
    When the client requests the status of a Forecast Proposal
    Then the response is Unauthorized
