@monitoring_sets
Feature: Monitoring Set CRUD operations

    As a Clearinghouse Operator
    I want to create, read, update, and delete Monitoring Sets
    So that I can group transmission facilities for targeted real-time limit queries

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  # GET /default-monitoring-set
  Scenario Outline: Get the default monitoring set
    Given the Accept header is set to `<content_type>`
    When the client requests the Default Monitoring Set
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.monitoring-set.v1+json |
    | application/vnd.trolie.monitoring-set.v2+json |

  # POST /monitoring-sets
  # prism_fail: Prism does not have an example response for this POST endpoint
  @prism_fail
  Scenario Outline: Create a monitoring set
    Given the Content-type header is set to `<request_type>`
    And the body is loaded from `<file_name>`
    When the client creates a Monitoring Set
    Then the response is 201 Created
    And the Content-Type header in the response is `<response_type>`
    And the response is schema-valid

    Examples:
    | request_type                                          | file_name                        | response_type |
    | application/vnd.trolie.monitoring-set-request.v1+json | data/monitoring_set_request.json | application/vnd.trolie.monitoring-set.v1+json |
    | application/vnd.trolie.monitoring-set-request.v1+json | data/monitoring_set_request.json | application/vnd.trolie.monitoring-set.v2+json |

  # GET /monitoring-sets/{id}
  # prism_fail: Prism does not have an example for this GET-by-id endpoint
  @prism_fail
  Scenario Outline: Get a monitoring set by id
    Given the Accept header is set to `<content_type>`
    When the client requests a Monitoring Set by id
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.monitoring-set.v1+json |
    | application/vnd.trolie.monitoring-set.v2+json |

  # PUT /monitoring-sets/{id}
  # prism_fail: Prism does not have an example response for PUT endpoints
  @prism_fail
  Scenario Outline: Update a monitoring set
    Given the Content-type header is set to `<request_type>`
    And the body is loaded from `<file_name>`
    When the client updates a Monitoring Set by id
    Then the response is 204 No Content

    Examples:
    | request_type                                          | file_name |
    | application/vnd.trolie.monitoring-set-request.v1+json | data/monitoring_set_request.json |

  # DELETE /monitoring-sets/{id}
  # prism_fail: Prism does not have an example response for DELETE endpoints
  @prism_fail
  Scenario: Delete a monitoring set
    When the client deletes a Monitoring Set by id
    Then the response is 204 No Content
