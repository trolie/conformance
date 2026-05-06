@realtime
Feature: Provide real-time limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide real-time limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
    
    # GET Limits Real-Time Snapshot
    Scenario Outline: Get limits real-time snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests for the current real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true |

    Scenario Outline: Get limits real-time snapshot (detailed)
        Given the Accept header is set to `<content_type>`
        When the client requests for the current real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json |

    # prism_fail: Prism returns the wrong Content-Type for media type parameter variants
    @prism_fail
    Scenario Outline: Get limits real-time snapshot (detailed, include-psr-header=false)
        Given the Accept header is set to `<content_type>`
        When the client requests for the current real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |
    

    # GET Regional Limits Real-Time Snapshot
    Scenario Outline: Get regional limits real-time snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests for the current regional real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true |

    Scenario Outline: Get regional limits real-time snapshot (detailed)
        Given the Accept header is set to `<content_type>`
        When the client requests for the current regional real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json |

    # prism_fail: Prism returns the wrong Content-Type for media type parameter variants
    @prism_fail
    Scenario Outline: Get regional limits real-time snapshot (detailed, include-psr-header=false)
        Given the Accept header is set to `<content_type>`
        When the client requests for the current regional real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |

    Scenario Outline: Media types are required for real-time snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests for the current real-time snapshot
        Then the response is 406 Not Acceptable
        And the Content-Type header in the response is `application/problem+json`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/json |
        | application/vnd.trolie.forecast-limits-snapshot.v1+json |

    Scenario Outline: Media types are required for regional real-time snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests for the current regional real-time snapshot
        Then the response is 406 Not Acceptable
        And the Content-Type header in the response is `application/problem+json`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/json |
        | application/vnd.trolie.forecast-limits-snapshot.v1+json |


