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
    TEST_TOKEN = os.environ["TEST_TOKEN"]

TEST_URL = "https://useroffice-test.esss.lu.se/graphql"
YMIR_ID = 4

OLD_STYLE_TOKEN = {"login": {"token": None}}


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_if_url_does_not_exist_raises():
    does_not_exist = TEST_URL.replace("e", "")
    with pytest.raises(requests.exceptions.ConnectionError):
        _ProposalSystemWrapper().get_proposal_for_instrument(
            OLD_STYLE_TOKEN, does_not_exist, YMIR_ID, TEST_TOKEN
        )


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_for_ymir_instrument():
    wrapper = _ProposalSystemWrapper()
    results = wrapper.get_proposal_for_instrument(
        OLD_STYLE_TOKEN, TEST_URL, YMIR_ID, TEST_TOKEN
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
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_invalid_token_raises_transport_error():
    with pytest.raises(TransportServerError):
        wrapper = _ProposalSystemWrapper()
        _ = wrapper.get_proposal_for_instrument(
            OLD_STYLE_TOKEN, TEST_URL, YMIR_ID, ":: not a valid token ::"
        )


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_instruments_list():
    wrapper = _ProposalSystemWrapper()

    results = wrapper.get_instrument_data(OLD_STYLE_TOKEN, TEST_URL, TEST_TOKEN)

    # We should get data back, but it may not be the same data each time!
    # So just test the structure for now
    assert len(results) > 0
    assert "id" in results[0]
    assert "shortCode" in results[0]
    assert "name" in results[0]
