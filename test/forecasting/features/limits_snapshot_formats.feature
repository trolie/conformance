@forecasting
Feature: Provide forecast limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide forecast limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  Scenario Outline: Obtaining the latest forecast snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  Scenario Outline: Obtaining the latest slim forecast snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |
      # TODO: Prism's mock server returns the wrong media type
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true |
      # This literally crashes Prism's mock server
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true; limit-type=apparent-power  |
      # Overall, we need to whitelist the media types supported
      # using a test config and use the blacklist to assert 415 Unsupported Media Type

  Scenario Outline: Client should be permitted to request `application/problem+json` explicitly
    Given the Accept header is set to `<content_type>, application/problem+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  Scenario Outline: Client should be permitted to accept `*/*` explicitly
    Given the Accept header is set to `<content_type>, */*`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  @prism_fail
  Scenario: Requesting the slim forecast snapshot requires a limit type
    Given the Accept header is set to `application/vnd.trolie.forecast-limits-snapshot-slim.v1+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 415 Unsupported Media Type
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid


  @prism_fail
  Scenario Outline: Limit forecasts should support conditional GET
    Given the Accept header is set to `<content_type>`
    And the client requests the current Forecast Limits Snapshot
    When the client issues a conditional GET for the same resource
    Then the response is 304 Not Modified
    And the the response is empty
    And there is no Content-Type header in the response
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power, inputs-used=true |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true, limit-type=apparent-power  |

  # Prism ignores bad query params and sends a 200 OK
  @prism_fail
  Scenario Outline: Bad query params are malformed requests
    Given the Accept header is set to `<content_type>`
    And the client has bad query parameters
    When the client requests the current Forecast Limits Snapshot
    Then the response is 400 Bad Request
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power, inputs-used=true |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true, limit-type=apparent-power  |

  Scenario Outline: Sending a body with a GET request is a bad request 
    Given the Accept header is set to `<content_type>`
    And the client has a non-empty body
    When the client requests the current Forecast Limits Snapshot
    Then the response is 400 Bad Request
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |
      | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |

  Scenario Outline: Media types are required
    Given the Accept header is set to `<content_type>`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 406 Not Acceptable
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/json |
      | application/vnd.trolie.realtime-limits-snapshot.v1+json |
      # Prism returns 200, incorrectly, for the following @prism_fail
      #| */* |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json, limit-type=apparent-power |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true; limit-type=apparent-power  |
