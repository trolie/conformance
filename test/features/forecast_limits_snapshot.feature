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
    Then the response is 200 OK
    And the Content-Type header in the response is <content_type>
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  Scenario Outline: Obtaining the latest slim forecast snapshot
    Given the Accept header is set to <content_type>
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is <content_type>
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |
      # TODO: Prism's mock server returns the wrong media type
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power, inputs-used=true |
      # This literally crashes Prism's mock server
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true, limit-type=apparent-power  |
      # Overall, we need to whitelist the media types supported
      # using a test config and use the blacklist to assert 415 Unsupported Media Type

  @prism_fail
  Scenario: Requesting the slim forecast snapshot requires a limit type
    Given the Accept header is set to `application/vnd.trolie.forecast-limits-snapshot-slim.v1+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 415 Unsupported Media Type
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid
