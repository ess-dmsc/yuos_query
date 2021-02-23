from unittest import mock

import pytest
from requests.exceptions import ConnectionError

from yuos_query import YuosClient
from yuos_query.exceptions import ConnectionException, InvalidIdException
from yuos_query.proposal_system import _ProposalSystemWrapper

# Copied from the real server
VALID_INSTRUMENT_LIST = [
    {"id": 4, "shortCode": "YMIR", "description": "Our test beamline", "name": "YMIR"},
    {
        "id": 3,
        "shortCode": "asztalos",
        "description": "test\n",
        "name": "Asztalos Instrument",
    },
    {
        "id": 2,
        "shortCode": "s adasd",
        "description": "d asdas",
        "name": "Test instrument 2",
    },
    {
        "id": 1,
        "shortCode": "sd ad",
        "description": "d asdasd",
        "name": "Test instrument 1",
    },
]

UNKNOWN_INSTRUMENT_ID_RESPONSE = []
VALID_PROPOSAL_ID = "471120"

# Copied from the real server
VALID_RESPONSE_DATA = [
    {
        "id": 169,
        "shortCode": "471120",
        "title": "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        "users": [
            {"firstname": "jonathan ", "lastname": "Taylor"},
            {"firstname": "Johan", "lastname": "Andersson"},
        ],
        "proposer": {"firstname": "Fredrik", "lastname": "Bolmsten"},
    }
]


def generate_standard_mock():
    mocked_impl = mock.create_autospec(_ProposalSystemWrapper)
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposal_for_instrument.return_value = VALID_RESPONSE_DATA
    return mocked_impl


class TestProposalSystem:
    def create_client(
        self,
        invalid_url: bool = False,
        invalid_user: bool = False,
        invalid_password: bool = False,
        unknown_id: bool = False,
    ):
        """
        Creates a client with a mocked implementation for talking to the server.

        This method should be overridden when creating a non-mocked version of
        these tests.

        NOTE: Only activate one flag at a time!

        :param invalid_url: Behave like the url is invalid.
        :param invalid_user: Behave like the user is invalid.
        :param invalid_password: Behave like the password is invalid.
        :param unknown_id: Behave like the proposal id is invalid.
        :return: A YuosClient instance.
        """
        mocked_impl = generate_standard_mock()

        if invalid_url:
            mocked_impl.get_instrument_data.side_effect = ConnectionError("oops")
            mocked_impl.execute_query.side_effect = ConnectionError("oops")
            mocked_impl.get_proposal_for_instrument.side_effect = ConnectionError(
                "oops"
            )
        if unknown_id:
            mocked_impl.get_proposal_for_instrument.return_value = (
                UNKNOWN_INSTRUMENT_ID_RESPONSE
            )

        return YuosClient("https://something.com", "not_a_real_token", mocked_impl)

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
