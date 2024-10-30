
Feature: All requests require authorization

  Scenario: Get Forecast Limits Snapshot requires authorization
    Given a TROLIE client that has not been authorized
    When the client requests the current Forecast Limits Snapshot
    Then the response is Unauthorized
