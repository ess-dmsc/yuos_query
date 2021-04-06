import os

import pytest
import requests
from gql.transport.exceptions import TransportQueryError

from yuos_query.proposal_system import _ProposalSystemWrapper

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]

TEST_URL = "https://useroffice-test.esss.lu.se/graphql"
YMIR_ID = 4
KNOWN_DB_ID = 242  # Not a "proposal" ID rather the database ID.


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_if_url_does_not_exist_raises():
    url_does_not_exist = TEST_URL.replace("e", "")
    with pytest.raises(requests.exceptions.ConnectionError):
        _ProposalSystemWrapper().get_proposal_for_instrument(
            YUOS_TOKEN, url_does_not_exist, YMIR_ID
        )


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_for_ymir_instrument():
    wrapper = _ProposalSystemWrapper()
    results = wrapper.get_proposal_for_instrument(YUOS_TOKEN, TEST_URL, YMIR_ID)

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
    with pytest.raises(TransportQueryError):
        wrapper = _ProposalSystemWrapper()
        _ = wrapper.get_proposal_for_instrument(
            ":: not a valid token ::", TEST_URL, YMIR_ID
        )


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_instruments_list():
    wrapper = _ProposalSystemWrapper()

    results = wrapper.get_instrument_data(YUOS_TOKEN, TEST_URL)

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

    results = wrapper.get_sample_data_by_id(YUOS_TOKEN, TEST_URL, KNOWN_DB_ID)

    assert len(results) == 2
    assert {results[0]["title"], results[1]["title"]} == {"Camembert", "Chaource"}


@pytest.mark.skipif(
    SKIP_TEST, reason="no user and password supplied for testing against real system"
)
def test_get_sample_details_by_proposal_id():
    wrapper = _ProposalSystemWrapper()

    results = wrapper.get_sample_details_by_proposal_id(
        YUOS_TOKEN, TEST_URL, KNOWN_DB_ID
    )

    assert len(results) == 2
    assert "questionary" in results[0] and "questionary" in results[1]
    assert len(results[0]["questionary"]["steps"]) == 3
    assert "question" in results[0]["questionary"]["steps"][0]["fields"][0]["question"]
    assert "value" in results[0]["questionary"]["steps"][0]["fields"][0]
