import os

import pytest

from yuos_query.data_classes import User
from yuos_query.exceptions import (
    ConnectionException,
    ServerException,
    UnknownInstrumentException,
)
from yuos_query.proposal_system_scicat import ProposalRequester

KNOWN_PROPOSAL_ID = "352814"

YMIR_ID = "ebfb7106-b885-4eda-b414-3f6fb80443e4"  # From the proposal system
URL = "https://staging.scicat.ess.eu"

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

    def test_querying_a_url_that_is_not_a_scicat_backend_raises(self):
        # The host resolves but has no SciCat endpoints, so it answers with a
        # 404 rather than failing at the transport level.
        api = ProposalRequester(
            "https://www.google.com/scicat-explorer", YUOS_TOKEN, {}
        )

        with pytest.raises(ServerException):
            api.get_proposal_by_id(KNOWN_PROPOSAL_ID)

    def test_querying_with_non_valid_url_raises(self):
        api = ProposalRequester("missing.protocol.com", YUOS_TOKEN, {})

        with pytest.raises(ConnectionException):
            api.get_proposal_by_id(KNOWN_PROPOSAL_ID)

    def test_querying_an_unreachable_host_raises(self):
        api = ProposalRequester("https://not-a-real-host.invalid", YUOS_TOKEN, {})

        with pytest.raises(ConnectionException):
            api.get_proposal_by_id(KNOWN_PROPOSAL_ID)

    def test_querying_with_invalid_token_returns_no_data(self):
        # SciCat does not reject an invalid token on this endpoint; it answers
        # 200 with an empty result set, so no proposal is found.
        api = ProposalRequester(URL, "ECDCINTEGRATIONTEST", {})

        assert api.get_proposal_by_id(KNOWN_PROPOSAL_ID) is None

    def test_querying_for_unknown_instrument_raises(self):
        api = ProposalRequester(URL, YUOS_TOKEN, {})

        with pytest.raises(UnknownInstrumentException):
            api.get_proposals_for_instrument("NOT_AN_INSTRUMENT")

    def test_querying_for_numeric_instrument_name_raises(self):
        # Instruments are identified by short code now, not by a numeric id,
        # so a number matches nothing.
        api = ProposalRequester(URL, YUOS_TOKEN, {})

        with pytest.raises(UnknownInstrumentException):
            api.get_proposals_for_instrument("4")

    def test_querying_for_instruments_returns_expected_data(self):
        api = ProposalRequester(URL, YUOS_TOKEN, {})

        assert api._get_instrument_id("YMIR") == YMIR_ID

    def test_querying_for_proposals_returns_expected_data(self):
        api = ProposalRequester(URL, YUOS_TOKEN, {})

        proposals = api.get_proposals_for_instrument("YMIR")

        assert KNOWN_PROPOSAL_ID in proposals
        result = proposals[KNOWN_PROPOSAL_ID]

        assert result.id == KNOWN_PROPOSAL_ID
        assert result.title == "Energy Storage (Powder Diffraction) - 352814-1"
        assert result.proposer == User("Jekabs", "Karklins", "jekabskarklins", "")
        # The proposal carries no affiliation for the PI or the visitors, so
        # the organisation is empty for everyone. The PI is also visitor 1.
        assert result.users == [
            User("Jekabs", "Karklins", "jekabskarklins", ""),
            User("Massimiliano", "Novelli", "massimilianonovelli", ""),
            User("Yoganandan Apple", "Pandiyan", "yoganandan applepandiyan", ""),
        ]

    def test_querying_for_experiments_returns_expected_data(self):
        api = ProposalRequester(URL, YUOS_TOKEN, {})

        proposals = api.get_proposals_for_instrument("YMIR")

        assert KNOWN_PROPOSAL_ID in proposals
        result = proposals[KNOWN_PROPOSAL_ID]

        assert result.id == KNOWN_PROPOSAL_ID
        assert [s.id for s in result.samples] == [
            "262e2b02-be1a-4dd8-8152-8ba9f1a37188",
            "beed135e-c839-4e04-a0c5-b944517f5490",
        ]

    def test_querying_by_id_matches_the_instrument_listing(self):
        api = ProposalRequester(URL, YUOS_TOKEN, {})

        by_id = api.get_proposal_by_id(KNOWN_PROPOSAL_ID)
        from_listing = api.get_proposals_for_instrument("YMIR")[KNOWN_PROPOSAL_ID]

        assert by_id == from_listing
