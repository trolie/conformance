@seasonal_overrides
Feature: Caching of Seasonal Override responses supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of Seasonal Override responses
    So that clients can avoid unnecessary re-fetching of unchanged data

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    # prism_fail: Prism does not implement ETag generation or If-None-Match conditional GET logic
    @prism_fail
    Scenario Outline: Support Conditional GET for Seasonal Overrides list
        Given the Accept header is set to `<accept_header>`
        And the client has obtained the current Seasonal Overrides list with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
            | accept_header |
            | application/vnd.trolie.seasonal-override-set.v1+json |
