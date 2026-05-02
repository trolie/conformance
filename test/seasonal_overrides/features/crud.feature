@seasonal_overrides
Feature: Seasonal Override CRUD operations

    As a Ratings Provider
    I want to create, read, update, and delete Seasonal Overrides
    So that I can manage temporary static ratings for resources exempt from AARs

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  # GET /seasonal-overrides
  Scenario Outline: List seasonal overrides
    Given the Accept header is set to `<content_type>`
    When the client requests the list of Seasonal Overrides
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.seasonal-override-set.v1+json |

  # POST /seasonal-overrides
  # prism_fail: Prism returns 422 for POST with a body (schema validation issue)
  @prism_fail
  Scenario Outline: Create a seasonal override
    Given the Content-type header is set to `<request_type>`
    And the body is loaded from `<file_name>`
    When the client creates a Seasonal Override
    Then the response is 201 Created
    And the Content-Type header in the response is `<response_type>`
    And the response is schema-valid

    Examples:
    | request_type                                          | file_name                            | response_type |
    | application/vnd.trolie.seasonal-override.v1+json | data/seasonal_override_request.json  | application/vnd.trolie.seasonal-override.v1+json |

  # GET /seasonal-overrides/{id}
  Scenario Outline: Get a seasonal override by id
    Given the Accept header is set to `<content_type>`
    When the client requests a Seasonal Override by id
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.seasonal-override.v1+json |

  # PUT /seasonal-overrides/{id}
  # prism_fail: Prism does not have an example response for PUT endpoints
  @prism_fail
  Scenario Outline: Update a seasonal override
    Given the Content-type header is set to `<request_type>`
    And the body is loaded from `<file_name>`
    When the client updates a Seasonal Override by id
    Then the response is 204 No Content

    Examples:
    | request_type                                          | file_name |
    | application/vnd.trolie.seasonal-override.v1+json | data/seasonal_override_request.json |

  # DELETE /seasonal-overrides/{id}
  # prism_fail: Prism does not have an example response for DELETE endpoints
  @prism_fail
  Scenario: Delete a seasonal override
    When the client deletes a Seasonal Override by id
    Then the response is 204 No Content

  # prism_fail: Prism cannot be instructed to return 409 for a DELETE; requires a real server
  @prism_fail
  Scenario: Cannot delete a seasonal override that is in use
    When the client deletes a Seasonal Override that is in use
    Then the response is 409 Conflict
    And the Content-Type header in the response is `application/problem+json`
    And the response is schema-valid
