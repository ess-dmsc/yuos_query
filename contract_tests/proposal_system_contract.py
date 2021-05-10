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
        instrument_name: str = "YMIR",
        invalid_url: bool = False,
        invalid_user: bool = False,
        invalid_password: bool = False,
        unknown_id: bool = False,
    ):
        raise NotImplementedError()

    def test_querying_for_proposal_by_id_with_invalid_url_raises(
        self,
    ):
        with pytest.raises(ConnectionException):
            self.create_client(invalid_url=True)

    def test_querying_for_proposal_by_id_gets_correct_proposal(self):
        proposal_system = self.create_client()

        results = proposal_system.proposal_by_id(VALID_PROPOSAL_ID)

        assert results.id == VALID_PROPOSAL_ID
        assert results.title.startswith("The magnetic field dependence")
        assert results.proposer == ("Fredrik", "Bolmsten")
        assert len(results.users) == 2
        assert ("Johan", "Andersson") in results.users
        assert results.db_id == 169

    def test_when_querying_for_proposal_by_id_instrument_name_case_is_ignored(self):
        proposal_system = self.create_client()

        results = proposal_system.proposal_by_id(VALID_PROPOSAL_ID)

        assert results.id == VALID_PROPOSAL_ID

    def test_querying_for_proposal_by_id_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        proposal_system = self.create_client()

        with pytest.raises(InvalidIdException):
            proposal_system.proposal_by_id("abc")

    def test_client_constructor_with_unknown_instrument_name_raises(
        self,
    ):
        with pytest.raises(InvalidIdException):
            _ = self.create_client(":: not an instrument ::")

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        proposal_system = self.create_client(unknown_id=True)

        assert proposal_system.proposal_by_id("00000") is None

    def test_retrieval_of_all_proposals_and_samples_for_an_instrument(self):
        client = self.create_client()

        results = client.get_all_proposals_for_instrument("YMIR")

        assert len(results) == 17
        assert (
            results["471120"].title
            == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
        )
        assert results["471120"].id == "471120"
        assert results["471120"].users == [
            ("jonathan ", "Taylor"),
            ("Johan", "Andersson"),
        ]
        assert results["471120"].proposer == ("Fredrik", "Bolmsten")
        assert len(results["471120"].samples) == 3
        assert results["471120"].samples[0].name == ""
        assert results["471120"].samples[0].formula == "Yb3Ga5O12"
        assert results["471120"].samples[0].number == 1
        assert results["471120"].samples[0].density == (0, "g/cm*3")
        assert results["471120"].samples[0].mass_or_volume == (0, "")
        assert results["471120"].samples[1].name == ""
        assert (
            results["471120"].samples[1].formula
            == "(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS"
        )
        assert results["471120"].samples[1].number == 1
        assert results["471120"].samples[1].density == (0, "g/cm*3")
        assert results["471120"].samples[1].mass_or_volume == (0, "µg")
