# yuos_query
Python wrapper for querying the ESS user office system

## Install requirements
```
pip install -r requirements.txt
```

For developers:
```
pip install -r requirements-dev.txt
pre-commit install
```

## Tests
### Programmer tests
These tests live in the `tests` directory and can be run directly from the main directory using pytest.
```
> pytest tests
```

### Contract tests
These tests live in the `contract_tests` directory. They are tests that respect the contract of the system.
There are tests that run against the real system (slow) and the mocked system. These tests ultimately ensure that the
mocked tests and the real system tests behave in the same way.

The tests against the real system do not run by default as they can be slow. To run these tests, the `YUOS_TOKEN`
environment variable must be set to the value of the token in blackbox:

```
> YUOS_TOKEN=<the long token string> pytest contract_tests
```

### Integration tests
There are "pure" integration_tests in the `integration_tests` directory and are not run automatically by pytest because they
actually connect to a real server and are, thus, a bit slower to run.

The purpose of the integration_tests is to test the low-level behaviour of the real system, so any changes to that system's
API will be flagged.

To run these tests, the `YUOS_TOKEN` environment variable must be set to the value of the token in blackbox:

```
> YUOS_TOKEN=<the long token string> pytest integration_tests
```

**All these tests should be run before submitting code and semi-regularly to check that the real server's API hasn't changed.**

**Jenkins will run the tests against the real system automatically for pull requests.**

**Jenkins will also run the tests on main daily, so if there are breaking any API changes we will know about it.**

## Example usage

```
import os
from yuos_query.proposal_system import YuosClient

client = YuosClient("some url", os.environ["YUOS_TOKEN"])
proposal_info = client.proposal_by_id(instrument_name, proposal_id)
```
