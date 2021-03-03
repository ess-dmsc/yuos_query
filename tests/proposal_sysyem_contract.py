import pytest

from yuos_query import ConnectionException, InvalidIdException

VALID_PROPOSAL_ID = "471120"


class ProposalSystemContract:
    """
    This defines the contract of how the proposal system should work.
    Tests using mocks and tests using the real system inherit from this.
    This should ensure that the contract is honoured.
    """

    def create_client(
        self,
        invalid_url: bool = False,
        invalid_user: bool = False,
        invalid_password: bool = False,
        unknown_id: bool = False,
    ):
        raise NotImplementedError()

    def test_querying_for_proposal_by_id_with_invalid_url_raises(
        self,
    ):
        proposal_system = self.create_client(invalid_url=True)

        with pytest.raises(ConnectionException):
            proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

    def test_querying_for_proposal_by_id_gets_correct_proposal(self):
        proposal_system = self.create_client()

        results = proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

        assert results.id == VALID_PROPOSAL_ID
        assert results.title.startswith("The magnetic field dependence")
        assert results.proposer == ("Fredrik", "Bolmsten")
        assert len(results.users) == 2
        assert ("Johan", "Andersson") in results.users

    def test_when_querying_for_proposal_by_id_instrument_name_case_is_ignored(self):
        proposal_system = self.create_client()

        results = proposal_system.proposal_by_id("yMIr", VALID_PROPOSAL_ID)

        assert results.id == VALID_PROPOSAL_ID

    def test_querying_for_proposal_by_id_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        proposal_system = self.create_client()

        with pytest.raises(InvalidIdException):
            proposal_system.proposal_by_id("loki", "abc")

    def test_querying_for_proposal_id_with_unknown_instrument_raises(
        self,
    ):
        proposal_system = self.create_client()

        with pytest.raises(InvalidIdException):
            proposal_system.proposal_by_id("::unknown instrument::", VALID_PROPOSAL_ID)

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        proposal_system = self.create_client(unknown_id=True)

        assert proposal_system.proposal_by_id("YMIR", "00000") is None
