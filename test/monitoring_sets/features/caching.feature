@monitoring_sets
Feature: Caching of Monitoring Set responses supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of Monitoring Set responses
    So that clients can avoid unnecessary re-fetching of unchanged data

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    # prism_fail: Prism does not implement ETag generation or If-None-Match conditional GET logic
    @prism_fail
    Scenario Outline: Support Conditional GET for Default Monitoring Set
        Given the Accept header is set to `<accept_header>`
        And the client has obtained the current Default Monitoring Set with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
            | accept_header |
            | application/vnd.trolie.monitoring-set.v1+json |
            | application/vnd.trolie.monitoring-set.v2+json |
