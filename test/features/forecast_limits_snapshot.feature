Feature: Provide forecast limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide forecast limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  Scenario Outline: Obtaining the latest forecast snapshot
    Given the Accept header is set to <content_type>
    When the client requests the current Forecast Limits Snapshot
    Then the Content-Type header in the response is <content_type>
    And the response is a valid Forecast Limits Snapshot
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
