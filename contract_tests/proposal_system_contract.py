import pytest

from yuos_query.exceptions import ConnectionException, InvalidIdException

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
        assert results.db_id == 169

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

    def test_querying_for_samples_by_database_id_returns_sample_info(self):
        proposal_system = self.create_client()

        results = proposal_system.samples_by_id(242)

        assert len(results) == 2  # Two samples

        assert results[0].name == ""
        assert results[0].formula == "CHE3S"
        assert results[0].number == 10
        assert results[0].mass_or_volume == (5, "kg")
        assert results[0].density == (0, "g/cm*3")

        assert results[1].name == ""
        assert results[1].formula == "unknown"
        assert results[1].number == 1
        assert results[1].mass_or_volume == (100, "g")
        assert results[1].density == (0, "g/cm*3")
