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
They live in the `tests` directory and can be run directly from the main directory using pytest.
```
> pytest
```

### Integration tests
There are "pure" integration_tests in the `integration_tests` directory and are not run automatically by pytest because they
actually connect to a real server and are, thus, a bit slower to run.

There are also programmer tests that *can* be run against the real system in the `tests` directory (for example: test_proposal_system_behaviour.py).
Again, when run against the real server these tests are a bit slower to run.

To run these tests, the `TEST_USER` and `TEST_PASSWORD` environment variables must be set using a real user (with the correct permissions) and the
corresponding password:

```
> TEST_USER=<the username> TEST_PASSWORD=<the password> pytest
```

**All these "integration tests" should be run before submitting code and semi-regularly to check that the real server's API hasn't changed.**

**Jenkins will run the tests against the real system automatically for pull requests**
