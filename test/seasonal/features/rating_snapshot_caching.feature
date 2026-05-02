@seasonal
Feature: Caching of Seasonal Rating Snapshots supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of Seasonal Rating Snapshots
    So that clients can obtain the latest data without unnecessary network traffic
    when the client has already obtained the still-current snapshot

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    # prism_fail: Prism does not implement ETag generation or If-None-Match conditional GET logic
    @prism_fail
    Scenario Outline: Support Conditional GET for Seasonal Rating Snapshot
        Given the Accept header is set to `<accept_header>`
        And the client has obtained the current Seasonal Rating Snapshot with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
            | accept_header |
            | application/vnd.trolie.seasonal-rating-snapshot.v1+json |
            | application/vnd.trolie.seasonal-rating-snapshot-detailed.v1+json |
            | application/vnd.trolie.seasonal-rating-snapshot-detailed.v1+json; include-psr-header=false |

    # prism_fail: Prism does not implement ETag generation or If-None-Match conditional GET logic
    @prism_fail
    Scenario Outline: Support Conditional GET for Seasonal Rating Proposal Status
        Given the Accept header is set to `<accept_header>`
        And the client has obtained the current Seasonal Rating Proposal Status with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
            | accept_header |
            | application/vnd.trolie.seasonal-ratings-proposal-status.v1+json |
