@forecasting
Feature: Provide forecast limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide forecast limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  # GET Limits Forecast Snapshot
  Scenario Outline: Obtaining the latest forecast snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json;include-psr-header=false |

  # prism_fail: Prism only has an example for the base forecast-limits-snapshot media type; it returns the wrong Content-Type for the detailed variant
  @prism_fail
  Scenario Outline: Obtaining the latest detailed forecast snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json;include-psr-header=false |

  # GET Limits Forecast Snapshot (Slim format)
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
  
  @todo
  Scenario: Slim media type requires a limit type
    Given the Accept header is set to `application/vnd.trolie.forecast-limits-snapshot-slim.v1+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 415 Unsupported Media Type
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid

  Scenario Outline: Client should be permitted to request `application/problem+json` explicitly
    Given the Accept header is set to `<content_type>, application/problem+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |

  # prism_fail: Prism only has an example for the base media type and returns the wrong Content-Type for the detailed variant
  @prism_fail
  Scenario Outline: Client should be permitted to request `application/problem+json` explicitly (detailed)
    Given the Accept header is set to `<content_type>, application/problem+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
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
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |

  # prism_fail: Prism only has an example for the base media type and returns the wrong Content-Type for the detailed variant
  @prism_fail
  Scenario Outline: Client should be permitted to accept `*/*` explicitly (detailed)
    Given the Accept header is set to `<content_type>, */*`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  # prism_fail: Prism does not validate Accept header media type parameters and will not return 415 when limit-type is missing from the slim media type
  @prism_fail
  Scenario: Requesting the slim forecast snapshot requires a limit type
    Given the Accept header is set to `application/vnd.trolie.forecast-limits-snapshot-slim.v1+json`
    When the client requests the current Forecast Limits Snapshot
    Then the response is 415 Unsupported Media Type
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid

  # prism_fail: Prism ignores unrecognized query parameters and returns 200 OK instead of the required 400 Bad Request
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
    Then the response is 422 Unprocessable Entity
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
      # prism_fail returns 200, incorrectly, for the following
      #| */* |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json, limit-type=apparent-power |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true; limit-type=apparent-power  |

  # GET Historical Limits Forecast Snapshot
  Scenario Outline: Get historical limits forecast snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests a Historical Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |

  # prism_fail: Prism only has an example for the base forecast-limits-snapshot media type; it returns the wrong Content-Type for the detailed variant
  @prism_fail
  Scenario Outline: Get historical limits forecast snapshot (detailed)
    Given the Accept header is set to `<content_type>`
    When the client requests a Historical Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
      | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  Scenario Outline: Get historical limits forecast snapshot (slim)
    Given the Accept header is set to `<content_type>`
    When the client requests a Historical Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
      | content_type |
      | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |

  Scenario Outline: Media types are required for Historical Forecast Limits Snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests a Historical Forecast Limits Snapshot
    Then the response is 406 Not Acceptable
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid

    Examples:
      | content_type |
      | application/json |
      | application/vnd.trolie.realtime-limits-snapshot.v1+json |

  # GET Regional Limits Forecast Snapshot
  Scenario Outline: Get regional limits forecast snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests a Regional Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples: 
    | content_type                                            | 
    | application/vnd.trolie.forecast-limits-snapshot.v1+json | 
    | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
    | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |

  # prism_fail: Prism only has an example for the base media type and returns the wrong Content-Type for the detailed variant
  @prism_fail
  Scenario Outline: Get regional limits forecast snapshot (detailed)
    Given the Accept header is set to `<content_type>`
    When the client requests a Regional Forecast Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
    | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |

  Scenario Outline: Media types are required for Regional Forecast Limits Snapshot
    Given the Accept header is set to `<content_type>`
    When the client requests a Regional Forecast Limits Snapshot
    Then the response is 406 Not Acceptable
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/json |
    | application/vnd.trolie.realtime-limits-snapshot.v1+json |
  
  # prism_fail: Prism ignores request bodies on GET requests and returns 200 OK instead of the required 400 Bad Request
  @prism_fail
  Scenario Outline: Sending a body with a GET Regional Limits Forecast Snapshot is a bad request
    Given the Accept header is set to `<content_type>`
    And the client has a non-empty body
    When the client requests a Regional Forecast Limits Snapshot
    Then the response is 400 Bad Request
    And the Content-Type header in the response is `application/vnd.trolie.error.v1+json`
    And the response is schema-valid

    Examples: 
    | content_type |
    | application/vnd.trolie.forecast-limits-snapshot.v1+json |
    | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
    | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
    | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |
    | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power |


  # POST Update Regional Limits Forecast Snapshot
  Scenario Outline: Update Regional Limits Forecast Snapshot
    Given the Content-type header is set to `<content_type>`
    And the body is loaded from `<file_name>`
    When the client submits a Regional Forecast Limits Snapshot
    Then the response is 202 OK
    And the Content-Type header in the response is `<response_type>`
    And the response is schema-valid
    


    Examples:
    | content_type                                                                            | file_name                        | response_type |
    | application/vnd.trolie.rating-forecast-proposal.v1+json                                 | data/forecast_snapshot.json      | application/vnd.trolie.rating-forecast-proposal-status.v1+json |
    #| application/vnd.trolie.rating-forecast-proposal-slim.v1+json; limit-type=apparent-power | data/forecast_proposal_slim.json | application/vnd.trolie.rating-forecast-proposal-status.v1+json |


