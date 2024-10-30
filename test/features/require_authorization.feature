
Feature: All requests require authorization
  
  Background:
    Given a TROLIE client that has not been authorized


  Scenario: Get Forecast Limits Snapshot requires authorization
    When the client requests the current Forecast Limits Snapshot
    Then the response is Unauthorized

  Scenario: Get Historical Forecast Limits Snapshot requires authorization
    When the client requests a Historical Forecast Limits Snapshot
    Then the response is Unauthorized
