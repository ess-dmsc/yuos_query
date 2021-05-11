import os

import pytest
from gql.transport.exceptions import TransportQueryError
from graphql import GraphQLError
from requests import ConnectionError

from yuos_query.proposal_system import ProposalSystem

# 471120 is a known proposal
VALID_PROPOSAL_ID = "471120"
YMIR_ID = 4  # From the proposal system

SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]
URL = "https://useroffice-test.esss.lu.se/graphql"


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
        system = ProposalSystem()

        with pytest.raises(ConnectionError):
            system.get_instrument_data(YUOS_TOKEN, "https://wwww.google.com")

    def test_querying_with_invalid_token_raises(self):
        system = ProposalSystem()

        with pytest.raises(TransportQueryError):
            system.get_instrument_data("::TOKEN::", URL)

    def test_querying_with_non_numeric_instrument_id_raises(self):
        system = ProposalSystem()

        with pytest.raises(GraphQLError):
            system.get_proposals_by_instrument_id(YUOS_TOKEN, URL, ":: string ::")

    def test_querying_with_float_instrument_id_raises(self):
        system = ProposalSystem()

        with pytest.raises(GraphQLError):
            system.get_proposals_by_instrument_id(YUOS_TOKEN, URL, 3.14)

    @pytest.mark.parametrize("test_input", [-10000, 10000])
    def test_querying_with_out_of_range_instrument_id_return_empty_list(
        self, test_input
    ):
        system = ProposalSystem()

        assert (
            len(system.get_proposals_by_instrument_id(YUOS_TOKEN, URL, test_input)) == 0
        )

    def test_get_instrument_data(self):
        system = ProposalSystem()

        results = system.get_instrument_data(YUOS_TOKEN, URL)

        assert len(results) > 0
        for instrument in results:
            if instrument["name"] == "YMIR":
                assert True
                return
        assert False

    def test_get_proposal_data(self):
        system = ProposalSystem()

        proposals = system.get_proposals_by_instrument_id(YUOS_TOKEN, URL, YMIR_ID)

        for proposal in proposals:
            if proposal["shortCode"] == VALID_PROPOSAL_ID:
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

    # TODO: move to yuos client tests

    # def test_when_querying_for_proposal_by_id_instrument_name_case_is_ignored(self):
    #     proposal_system = self.create_client()
    #
    #     results = proposal_system.proposal_by_id(VALID_PROPOSAL_ID)
    #
    #     assert results.id == VALID_PROPOSAL_ID

    # def test_querying_for_proposal_by_id_with_id_that_does_not_conform_to_pattern_raises(
    #     self,
    # ):
    #     proposal_system = self.create_client()
    #
    #     with pytest.raises(InvalidIdException):
    #         proposal_system.proposal_by_id("abc")

    # def test_client_constructor_with_unknown_instrument_name_raises(
    #     self,
    # ):
    #     with pytest.raises(InvalidIdException):
    #         _ = self.create_client(":: not an instrument ::")

    # def test_querying_for_unknown_proposal_id_returns_nothing(self):
    #     proposal_system = self.create_client(unknown_id=True)
    #
    #     assert proposal_system.proposal_by_id("00000") is None
