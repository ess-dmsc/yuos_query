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
        _ProposalSystemWrapper().get_proposals_including_samples_for_instrument(
            YUOS_TOKEN, url_does_not_exist, YMIR_ID
        )


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_invalid_token_raises_transport_error():
    with pytest.raises(TransportQueryError):
        wrapper = _ProposalSystemWrapper()
        _ = wrapper.get_proposals_including_samples_for_instrument(
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
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_and_sample_for_ymir_instrument():
    wrapper = _ProposalSystemWrapper()
    proposals = wrapper.get_proposals_including_samples_for_instrument(
        YUOS_TOKEN, TEST_URL, YMIR_ID
    )

    for proposal in proposals:
        # 471120 is a known proposal
        if proposal["shortCode"] == "471120":
            result = proposal
            break
    else:
        result = None

    assert (
        result["title"]
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
    assert result["id"] == 169
    assert len(result["users"]) == 2
    assert len(result["samples"]) == 3
    assert result["proposer"]["firstname"] == "Fredrik"
    assert result["proposer"]["lastname"] == "Bolmsten"
    assert {"firstname": "jonathan ", "lastname": "Taylor"} in result["users"]
    assert result["samples"][0]["id"] == 77
    assert result["samples"][0]["title"] == "Yb3Ga5O12"
