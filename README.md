# TROLIE 1.0 Conformance Suite

This repo provides testing tools to assess how well implementations conform to
the [TROLIE API specification](https://trolie.energy/spec-1.0).

### Who is this for?

Vendors and their customers should use these tests to verify which TROLIE
operations are correctly supported by their implementations.

Additionally, there are limits to the expressivity of OpenAPI; these tests will
clarify the intended behavior where the spec is ambiguous.

Finally, we anticipate this test suite will be used in CI pipelines as fast functional tests.

### What is it?

The Conformance Suite is implemented as a set of BDD-style tests, using pytest-bdd. These tests are organized into "conformance profiles":

* Forecasting (in progress)
* Real-Time (not started)
* Seasonal (not started)
* RC Peering (not started)

#### Test Data

The majority of conformance tests will need to be able to make assumptions about
the model that is loaded into the TROLIE server implementation. This includes
Ratings Obligations, Monitoring Sets, and power system resources that will be
used in the tests. To organize those conceptually, we intend to map onto a
subset of the [ESCA60 Model](./data/).

The current plan is to provide a standalone JSON model that closely follows the
`application/vnd.trolie.monitoring-set.v1+json` media type, enriched with the
other information needed to represent the test data.

### How do I get started as a test contributor?

#### Step #1: Clone this repository.

> [!IMPORTANT]
>
> If your company uses self-signed certs, place the necessary root certificates
> in the `.devcontainer/` folder in the PEM format with a `*.crt` extension, in
> order for the devcontainer to be configured with those certificates.
>
> Also, if you're using an internal proxy for `pip`, add a
> `.devcontainer/pip.conf` file with the appropriate `index-url` configuration.

#### Step #2: Open it with VS Code

The repo is configured to be used as a devcontainer, so upon opening it in VS
Code you will be prompted to build it and reopen a session with the
devcontainer. This can take a few minutes dependening on your network. Check the
Extensions panel after the devcontainer is connected, as you will likely need to
reload the window to activate the installed extensions.

#### Step #3: Configure the Testing Environment

The `.devcontainer/docker-compose.yml` will be used to spin up an instance of a
mock server that will use the TROLIE OpenAPI spec, serving examples in the spec
as mock responses. This setup can be used to author and execute some tests that
are not dependent upon any model state in the system under test.

The pytest VS Code plugin should be installed at this point, so you can use that
to run tests against the mock server.

#### Step #4 (optional): Test against a TROLE Implementation

The mock server cannot support all of the conformance test scenarios since it
only serves static examples. The majority of the conformance suite will require
a concrete implementation that has loaded the testing model described in the
Test Data section.

There are to initial steps needs to run tests against a TROLIE implementation: configuring the environment and implementing authorization.

##### Step #4.1: Configuring the Environment

Within VS Code, the simplest way to do this is to edit [`pytest.ini`](./pytest.ini), updating the `TROLIE_BASE_URL` variable.

##### Step #4.2: Implementing Authorization

Currently the `TrolieClient` implementation in
[`test/helpers.py`](test/helpers.py) assumes the use of a bearer token in the
authorization header. We have provided a hook (see the `AuthTokenProvider`
protocol in `helpers.py`) for your implementation to return that token.

The simplest way to use that hook is to copy
[`auth_token_provider_outline.py`](./auth_token_provider_outline.py) to
`test/auth_token_provider.py` then update all of the `<<change me>>` strings in
your environment.

In the future we may switch to defining a protocol for `TrolieClient` instead,
so that users of this conformance suite can control the entire HTTP stack.

### How do I use this to demonstrate conformance of my TROLIE implementation?

TBD

### How do I use this in the CI pipeline of my TROLIE implementation?

TBD
