import os

import pytest

from yuos_query.exceptions import (
    ConnectionException,
    InvalidQueryException,
    InvalidTokenException,
)
from yuos_query.proposal_system import (
    INSTRUMENT_QUERY,
    GqlWrapper,
    create_proposal_query,
)

KNOWN_PROPOSAL_ID = "199842"
YMIR_ID = 4  # From the proposal system
URL = "https://useroffice-test.esss.lu.se/graphql"

SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
class TestProposalSystemAPI:
    """
    This defines our understanding of how the proposal system works.
    If these tests break then it probably means a change to the proposal system
    which we need to adjust to.
    """

    def test_querying_with_non_server_url_raises(self):
        api = GqlWrapper("https://www.google.com", YUOS_TOKEN)

        with pytest.raises(ConnectionException):
            api.request(INSTRUMENT_QUERY)

    def test_querying_with_non_valid_url_raises(self):
        api = GqlWrapper("missing.protocol.com", YUOS_TOKEN)

        with pytest.raises(ConnectionException):
            api.request(INSTRUMENT_QUERY)

    def test_querying_with_invalid_token_raises(self):
        api = GqlWrapper(URL, "INVALID TOKEN")

        with pytest.raises(InvalidTokenException):
            api.request(INSTRUMENT_QUERY)

    def test_querying_with_malformed_query_raises(self):
        api = GqlWrapper(URL, YUOS_TOKEN)

        with pytest.raises(InvalidQueryException):
            api.request("MALFORMED QUERY")

    def test_querying_for_non_numeric_instrument_id_raises(self):
        api = GqlWrapper(URL, YUOS_TOKEN)

        with pytest.raises(InvalidQueryException):
            api.request(create_proposal_query("NOT NUMERIC"))

    def test_querying_for_float_instrument_id_raises(self):
        api = GqlWrapper(URL, YUOS_TOKEN)

        with pytest.raises(InvalidQueryException):
            api.request(create_proposal_query(123.45))

    @pytest.mark.parametrize("test_input", [-10000, 10000])
    def test_querying_with_out_of_range_instrument_id_return_empty_list(
        self, test_input
    ):
        api = GqlWrapper(URL, YUOS_TOKEN)

        result = api.request(create_proposal_query(test_input))

        assert len(result["proposals"]["proposals"]) == 0

    def test_querying_for_instruments_returns_expected_data(self):
        api = GqlWrapper(URL, YUOS_TOKEN)

        result = api.request(INSTRUMENT_QUERY)

        # Check structure matches query
        assert "instruments" in result
        assert "instruments" in result["instruments"]
        assert "id" in result["instruments"]["instruments"][0]

    def test_querying_for_proposals_returns_expected_data(self):
        api = GqlWrapper(URL, YUOS_TOKEN)

        response = api.request(create_proposal_query(YMIR_ID))

        result = None
        for proposal in response["proposals"]["proposals"]:
            if proposal["proposalId"] == KNOWN_PROPOSAL_ID:
                result = proposal
                break

        assert result["title"] == "Dynamics of Supercooled H2O in confined geometries"
        assert result["primaryKey"] == 232
        assert len(result["users"]) == 2
        assert len(result["samples"]) == 2
        assert result["proposer"]["firstname"] == "Jonathan"
        assert result["proposer"]["lastname"] == "Taylor"
        assert {"firstname": "pascale", "lastname": "deen"} in result["users"]
        assert result["samples"][0]["id"] == 143
        assert result["samples"][0]["title"] == "Water"
