
Feature: All requests require authorization
  
  Background:
    Given a TROLIE client that has not been authorized


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
