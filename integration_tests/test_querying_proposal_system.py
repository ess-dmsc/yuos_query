import os

import pytest
import requests
from gql.transport.exceptions import TransportServerError

from yuos_query.proposal_system import _ProposalSystemWrapper

# These tests are skipped if the TEST_USER and TEST_PASSWORD environment variables are not defined
SKIP_TEST = True
if "TEST_USER" in os.environ:
    SKIP_TEST = False
    TEST_USER = os.environ["TEST_USER"]
    TEST_PASSWORD = os.environ["TEST_PASSWORD"]

TEST_URL = "https://useroffice-test.esss.lu.se/graphql"
YMIR_ID = 4
KNOWN_DB_ID = 242  # Not a "proposal" ID rather the database ID.


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_can_get_token_for_test_user():
    result = _ProposalSystemWrapper().get_token(TEST_URL, TEST_USER, TEST_PASSWORD)
    assert result["login"]["token"] is not None


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_if_url_does_not_exist_raises():
    does_not_exist = TEST_URL.replace("e", "")
    with pytest.raises(requests.exceptions.ConnectionError):
        _ProposalSystemWrapper().get_token(does_not_exist, TEST_USER, TEST_PASSWORD)


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_if_user_does_not_exist_then_get_no_token():
    result = _ProposalSystemWrapper().get_token(
        TEST_URL, "not.real@ess.eu", TEST_PASSWORD
    )
    assert result["login"]["token"] is None


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_if_password_wrong_then_get_no_token():
    result = _ProposalSystemWrapper().get_token(
        TEST_URL, TEST_USER, "unlikely_to_be_right"
    )
    assert result["login"]["token"] is None


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_get_proposals_for_ymir_instrument():
    wrapper = _ProposalSystemWrapper()
    results = wrapper.get_proposal_for_instrument(
        wrapper.get_token(TEST_URL, TEST_USER, TEST_PASSWORD), TEST_URL, YMIR_ID
    )

    # We should get data back, but it may not be the same data each time!
    # So just test the structure for now
    assert len(results) > 0
    assert "shortCode" in results[0]
    assert "title" in results[0]
    assert "proposer" in results[0]
    assert "firstname" in results[0]["proposer"]
    assert "lastname" in results[0]["proposer"]
    assert "users" in results[0]


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_invalid_token_raises_transport_error():
    invalid_token = {"login": {"token": "some random nonsense ewrewrew"}}

    with pytest.raises(TransportServerError):
        wrapper = _ProposalSystemWrapper()
        _ = wrapper.get_proposal_for_instrument(invalid_token, TEST_URL, YMIR_ID)


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_get_instruments_list():
    wrapper = _ProposalSystemWrapper()

    results = wrapper.get_instrument_data(
        wrapper.get_token(TEST_URL, TEST_USER, TEST_PASSWORD),
        TEST_URL,
    )

    # We should get data back, but it may not be the same data each time!
    # So just test the structure for now
    assert len(results) > 0
    assert "id" in results[0]
    assert "shortCode" in results[0]
    assert "name" in results[0]


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_get_sample_list_by_id():
    wrapper = _ProposalSystemWrapper()

    results = wrapper.get_sample_data_by_id(
        wrapper.get_token(TEST_URL, TEST_USER, TEST_PASSWORD), TEST_URL, KNOWN_DB_ID
    )

    assert len(results) == 2
    assert {results[0]["title"], results[1]["title"]} == {"Camembert", "Chaource"}


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_get_sample_details_by_proposal_id():
    wrapper = _ProposalSystemWrapper()

    results = wrapper.get_sample_details_by_proposal_id(
        wrapper.get_token(TEST_URL, TEST_USER, TEST_PASSWORD), TEST_URL, KNOWN_DB_ID
    )

    print(results[0])
    assert len(results) == 2
    assert "questionary" in results[0] and "questionary" in results[1]
    assert len(results[0]["questionary"]["steps"]) == 3
    assert "question" in results[0]["questionary"]["steps"][0]["fields"][0]["question"]
    assert "value" in results[0]["questionary"]["steps"][0]["fields"][0]
