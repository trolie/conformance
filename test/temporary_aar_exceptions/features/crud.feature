@temporary_aar_exceptions
Feature: Temporary AAR Exception CRUD operations

    As a Ratings Provider
    I want to create, read, update, and delete Temporary AAR Exceptions
    So that I can apply temporary modifications to Ambient Adjusted Ratings

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  # GET /temporary-aar-exceptions
  Scenario Outline: List temporary AAR exceptions
    Given the Accept header is set to `<content_type>`
    When the client requests the list of Temporary AAR Exceptions
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.temporary-aar-exception-set.v1+json |

  # POST /temporary-aar-exceptions
  # prism_fail: Prism does not have an example response for this POST endpoint
  @prism_fail
  Scenario Outline: Create a temporary AAR exception
    Given the Content-type header is set to `<request_type>`
    And the body is loaded from `<file_name>`
    When the client creates a Temporary AAR Exception
    Then the response is 201 Created
    And the Content-Type header in the response is `<response_type>`
    And the response is schema-valid

    Examples:
    | request_type                                                           | file_name                              | response_type |
    | application/vnd.trolie.temporary-aar-exception-request.v1+json        | data/temporary_aar_exception.json      | application/vnd.trolie.temporary-aar-exception.v1+json |

  # GET /temporary-aar-exceptions/{id}
  # prism_fail: Prism does not have an example for this GET-by-id endpoint
  @prism_fail
  Scenario Outline: Get a temporary AAR exception by id
    Given the Accept header is set to `<content_type>`
    When the client requests a Temporary AAR Exception by id
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid

    Examples:
    | content_type |
    | application/vnd.trolie.temporary-aar-exception.v1+json |

  # PUT /temporary-aar-exceptions/{id}
  # prism_fail: Prism does not have an example response for PUT endpoints
  @prism_fail
  Scenario Outline: Update a temporary AAR exception
    Given the Content-type header is set to `<request_type>`
    And the body is loaded from `<file_name>`
    When the client updates a Temporary AAR Exception by id
    Then the response is 204 No Content

    Examples:
    | request_type                                                    | file_name |
    | application/vnd.trolie.temporary-aar-exception-request.v1+json | data/temporary_aar_exception.json |

  # DELETE /temporary-aar-exceptions/{id}
  # prism_fail: Prism does not have an example response for DELETE endpoints
  @prism_fail
  Scenario: Delete a temporary AAR exception
    When the client deletes a Temporary AAR Exception by id
    Then the response is 204 No Content
