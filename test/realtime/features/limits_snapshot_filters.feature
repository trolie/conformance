@realtime
Feature: Support querying subsets of the available real-time limits

    As a Clearinghouse Operator
    I want to support querying subsets of the available real-time limits
    So that clients can obtain just the data they need
    when they request a real-time limits snapshot and specify a query parameter

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And the Accept header is set to `application/vnd.trolie.realtime-limits-snapshot.v1+json`

    # GET Limits Real-Time Snapshot filters
    Scenario Outline: Query real-time limits with monitoring-set filter
        When the client requests real-time limits with monitoring-set filter <monitoring_set_id>
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | monitoring_set_id |
        | default           |

    @requires_model
    Scenario Outline: Query real-time limits with resource-id filter
        When the client requests real-time limits with resource-id filter <resource_id>
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | resource_id |
        | 8badf00d    |

    # GET Regional Real-Time Limits Snapshot filters
    Scenario Outline: Query regional real-time limits with monitoring-set filter
        When the client requests regional real-time limits with monitoring-set filter <monitoring_set_id>
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | monitoring_set_id |
        | default           |

    @requires_model
    Scenario Outline: Query regional real-time limits with resource-id filter
        When the client requests regional real-time limits with resource-id filter <resource_id>
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | resource_id |
        | 8badf00d    |
