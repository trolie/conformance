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


    # Query parameters for : GET Limits Forecast Snapshot
    @prism_fail 
    Scenario Outline: Query forecast limits with offset-period-start
        Given the current wall clock time at the Clearinghouse today is set to the user's current time
        When the client requests forecast limits with `offset-period-start` set to <offset_hours> after the current time
        Then the response should include only forecast limits beginning at the current time plus <offset_hours>, in the server's time zone
        

        Examples:
        | offset_hours  | 
        | 1             |
        | 5             |
        | 7             |
        
    
    @todo
    Scenario: What to do when `offset-period-start` is in the past?


    @prism_fail  
    Scenario Outline: Query forecast limits with period-end
        Given the current wall clock time at the Clearinghouse today is set to the user's current time
        When the client requests forecast limits with `period-end` set to <offset_hours> after the current time
        Then the response should include forecast limits up to the current time plus <offset_hours>, in the server's time zone

        Examples:
        | offset_hours  |
        | 1             |
        | 5             |
        | 7             |
        
    Scenario Outline: Query forecast limits with monitoring-set filter
        When the client requests forecast limits with monitoring-set filter <monitoring_set_id>
        Then the response should include forecast limits for the monitoring set <monitoring_set_id>
        Examples:
        | monitoring_set_id |
        | default   |

    @requires_model  
    Scenario Outline: Query forecast limits with resource-id filter
        When the client requests forecast limits with resource-id filter <resource_id>
        Then the response should include forecast limits for the resource id <resource_id>
        Examples:
        | resource_id |
        | 8badf00d    |

    @prism_fail  
    Scenario: Query forecast limits with static-only
        When the client requests forecast limits with static-only set to true
        Then the response should include only static forecast limits
    
    # Query parameters for : GET Historical Limits Forecast Snapshot  
    Scenario Outline: Query historical limits forecast snapshots with offset-period-start
        Given the current wall clock time at the Clearinghouse today is set to the user's current time
        When the client requests historical forecast limits with `offset-period-start` set to <offset_hours> after the current time
        Then the response should include only forecast limits beginning at the current time plus <offset_hours>, in the server's time zone
        
        Examples:
        | offset_hours  |
        | 1             |
        | 5             |
        | 7             |

    
    Scenario Outline: Query historical limits forecast snapshots with period-end
        Given the current wall clock time at the Clearinghouse today is set to the user's current time
        When the client requests historical forecast limits with `period-end` set to <offset_hours> after the current time
        Then the response should include forecast limits up to the current time plus <offset_hours>, in the server's time zone

        Examples:
        | offset_hours  |
        | 1             |  
        | 5             |
        | 7             |

    Scenario Outline: Query historical limits forecast snapshots with monitoring-set
        When the client requests historical forecast limits with monitoring-set filter <monitoring_set_id>
        Then the response should include forecast limits for the monitoring set <monitoring_set_id>

        Examples:
        | monitoring_set_id |
        | TO1          |
    
    Scenario Outline: Query historical limits forcasting snapshots with resource-id
        When the client requests historical forecast limits with resource-id filter <resource_id>
        Then the response should include forecast limits for the resource id <resource_id>

        Examples:
        | resource_id |
        | DOUGLAS.T538.1 OUT |
        | PARKHILL.T5.T5 |
        | HEARN.34562.1 |
    
    Scenario Outline: Query historical limits forcasting snapshots with static-only
        When the client requests historical forecast limits with static-only set to true
        Then the response should include only static forecast limits

    # Query parameters for : GET Regional Limits Forecast Snapshot
    @offset_regional
    Scenario Outline: Query regional limits forecast snapshots with offset-period-start
        Given the current wall clock time at the Clearinghouse today is set to the user's current time
        When the client requests regional forecast limits with `offset-period-start` set to <offset_hours> after the current time
        Then the response should include only forecast limits beginning at the current time plus <offset_hours>, in the server's time zone

        Examples:
        | offset_hours  |
        | 1             |
        | 5             |   
        | 7             |
    @offset_regional
    Scenario Outline: Query regional limits forecast snapshots with period-end
        Given the current wall clock time at the Clearinghouse today is set to the user's current time
        When the client requests regional forecast limits with `period-end` set to <offset_hours> after the current time
        Then the response should include forecast limits up to the current time plus <offset_hours>, in the server's time zone

        Examples:
        | offset_hours  |
        | 1             |
        | 5             |   
        | 7             |
  
    
    Scenario Outline: Query regional limits forecast snapshots with monitoring-set 
        When the client requests regional forecast limits with monitoring-set filter <monitoring_set_id>
        Then the response should include forecast limits for the monitoring set <monitoring_set_id>

        Examples:
        | monitoring_set_id |
        | TO1 |
    
    Scenario Outline: Query regional limits forecast snapshots with resource-id
        When the client requests regional forecast limits with resource-id filter <resource_id>
        Then the response should include forecast limits for the resource id <resource_id>

        Examples:
        | resource_id |
        | DOUGLAS.T538.1 OUT |
        | PARKHILL.T5.T5 |
        | HEARN.34562.1 |

    Scenario: Query regional limits forecast snapshots with static-only
        When the client requests regional forecast limits with static-only set to true
        Then the response should include only static forecast limits
