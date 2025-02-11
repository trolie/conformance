@forecasting
Feature: Support querying subsets of the available forecasted limits

    As a Clearinghouse Operator
    I want to support querying subsets of the available forecasted limits
    So that clients can obtain just the data they need
    when they request a forecast limits snapshot and specify a query parameter
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And the Accept header is set to `application/vnd.trolie.forecast-limits-snapshot.v1+json`

    @prism_fail
    Scenario Outline: Obtain just forecast limits starting from a given time in the future
        Given the current wall clock time at the Clearinghouse is today at 11am GMT, i.e., <server_time>
        When the client requests forecast limits with `offset-period-start` for an hour from then at <request_offset_time>
        Then the response should only include forecast limits starting at the `offset-period-start` in the server's time zone, i.e., <response_first_period> 

        Examples:
        | server_time           | request_offset_time | response_first_period |
        | 06:00:00-05:00        | 06:00:00-06:00      | 07:00:00-05:00        |
        | 05:00:00-06:00        | 07:00:00-05:00      | 06:00:00-06:00        |
    
    @todo
    Scenario: What to do when `offset-period-start` is in the past?

    @prism_fail
    Scenario Outline: Query forecast limits with period-end
        Given the current wall clock time at the Clearinghouse is today at 11am GMT, i.e., <server_time>
        When the client requests forecast limits with period-end <request_last_period>
        Then the response should include forecast limits up to <response_last_period> in the server's time zone
        Examples:
        | server_time            | request_last_period  | response_last_period |
        | 06:00:00-05:00         | 09:00:00-06:00       | 10:00:00-05:00       |

    @prism_fail
    Scenario: Query forecast limits with static-only
        When the client requests forecast limits with static-only set to true
        Then the response should include only static forecast limits

    Scenario Outline: Query forecast limits with monitoring-set filter
        When the client requests forecast limits with monitoring-set filter <monitoring_set_id>
        Then the response should include forecast limits for the monitoring set <monitoring_set_id>
        Examples:
        | monitoring_set_id |
        | default           |

    @requires_model
    Scenario Outline: Query forecast limits with resource-id filter
        When the client requests forecast limits with resource-id filter <resource_id>
        Then the response should include forecast limits for the resource id <resource_id>
        Examples:
        | resource_id |
        | 8badf00d    |
