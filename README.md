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
used in the tests. To organize those conceptually, we intend to map onto the
[WSCC 9-Bus System](https://icseg.iti.illinois.edu/wscc-9-bus-system/). Included will be a standalone JSON model that closely follows the
`application/vnd.trolie.monitoring-set.v1+json` media type, enriched with the other information needed to represent the test data.

### How do I get started?

Checkout this repo, and open it with VS Code. It is configured with a devcontainer, so you will be prompted to build it and reopen a session with the devcontainer. After the devcontainer is started, there will be a Jupyter server running at `localhost:8888`; instructions for running the various Conformance Profiles will be found there.

