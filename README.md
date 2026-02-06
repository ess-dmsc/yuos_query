# yuos_query
Python wrapper for querying the ESS user office system

## Usage

There are two parts to the program: a service for downloading the data from the proposal system and storing it locally,
and a client for extracting information from the local store based on queries.

Running the service:
```
uv run yuos-query -u https://useroffice.swap.ess.eu/graphql -i YMIR -c /opt/yuos/cached_proposals.json
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
> uv run pytest tests
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

## Release

- Update version in `pyproject.toml`
- Create and push a git tag: `git tag X.Y.Z && git push origin X.Y.Z`
- GitLab CI starts automatically
- Pipeline builds and uploads the package to the `ecdc-pypi` index
