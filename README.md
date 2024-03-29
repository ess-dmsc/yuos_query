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

## Usage

There are two parts to the program: a service for downloading the data from the proposal system and storing it locally,
and a client for extracting information from the local store based on queries.

Running the service:
```
python bin/yuos.py -u https://useroffice.swap.ess.eu/graphql -i YMIR -c /opt/yuos/cached_proposals.json
```
Typically this would be run as a service.
NOTE: requires an authenticating token environment variable.

Using the client:
```
from yuos_query.yuos_client import YuosCacheClient

client = YuosCacheClient.create('/opt/yuos/cached_proposals.json')
client.update_cache()
proposal = client.proposal_by_id("199842")
```

## Tests
### Programmer tests
These tests live in the `tests` directory and can be run directly from the main directory using pytest.
```
> pytest tests
```

### Integration tests
There are "pure" integration_tests in the `integration_tests` directory and are not run automatically by pytest because
they actually connect to a real server and are, thus, a bit slower to run.

The integration_tests contain two types of tests:
- end-to-end which check the test from the usage point of view
- low-level API tests which test the low-level behaviour of the real system, so any changes to that system's
API will be flagged.

To run these tests, the `YUOS_TOKEN` environment variable must be set to the value of the token in blackbox:

```
> YUOS_TOKEN=<the long token string> pytest integration_tests
```

**All these tests should be run before submitting code and semi-regularly to check that the real server's API hasn't
changed.**

**Jenkins will run the tests against the real system automatically for pull requests.**

**Jenkins will also run the tests on main daily, so if there are any breaking API changes we will know about it.**

## Releasing
- update the version number, commit and push
- locally, run `rm -rf build dist && python setup.py sdist bdist_wheel`
- tag the version on GitHub and upload the wheel file from the local `dist` folder.
