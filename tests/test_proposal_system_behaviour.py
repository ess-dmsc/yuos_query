from unittest import mock

import pytest
from requests.exceptions import ConnectionError

from tests.test_extracting_sample_info_from_proposal import EXAMPLE_DATA
from yuos_query import YuosClient
from yuos_query.exceptions import (
    ConnectionException,
    InvalidCredentialsException,
    InvalidIdException,
)
from yuos_query.proposal_system import _ProposalSystemWrapper

# Copied from a real server
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

# Copied from a real server
VALID_RESPONSE_DATA = [
    {
        "id": 169,
        "shortCode": "471120",
        "title": "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        "users": [
            {"firstname": "jonathan ", "lastname": "Taylor"},
            {"firstname": "Johan", "lastname": "Andersson"},
        ],
        "proposer": {"firstname": "Fredrik-user", "lastname": "Bolmsten"},
    }
]

URL = "https://something.com"
TEST_USER = "account@ess.eu"
TEST_PASSWORD = "apassword"


def generate_standard_mock():
    mocked_impl = mock.create_autospec(_ProposalSystemWrapper)
    mocked_impl.get_token.return_value = {"login": {"token": "eyJhbG"}}
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposal_for_instrument.return_value = VALID_RESPONSE_DATA
    mocked_impl.get_sample_details_by_proposal_id.return_value = EXAMPLE_DATA
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
            mocked_impl.get_token.side_effect = ConnectionError("oops")
        if invalid_user or invalid_password:
            mocked_impl.get_token.side_effect = InvalidCredentialsException("oops")
        if unknown_id:
            mocked_impl.get_proposal_for_instrument.return_value = (
                UNKNOWN_INSTRUMENT_ID_RESPONSE
            )

        return YuosClient(URL, TEST_USER, TEST_PASSWORD, mocked_impl)

    def test_querying_for_proposal_by_id_with_invalid_url_raise_correct_exception_type(
        self,
    ):
        proposal_system = self.create_client(invalid_url=True)

        with pytest.raises(ConnectionException):
            proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

    def test_querying_for_proposal_by_id_with_invalid_password_raise_correct_exception_type(
        self,
    ):
        proposal_system = self.create_client(invalid_password=True)

        with pytest.raises(InvalidCredentialsException):
            proposal_system.proposal_by_id("loki", VALID_PROPOSAL_ID)

    def test_querying_for_proposal_by_id_with_invalid_user_raise_correct_exception_type(
        self,
    ):
        proposal_system = self.create_client(invalid_user=True)

        with pytest.raises(InvalidCredentialsException):
            proposal_system.proposal_by_id("loki", VALID_PROPOSAL_ID)

    def test_querying_for_proposal_by_id_gets_correct_proposal(self):
        proposal_system = self.create_client()

        results = proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

        assert results.id == VALID_PROPOSAL_ID
        assert results.title.startswith("The magnetic field dependence")
        assert results.proposer == ("Fredrik-user", "Bolmsten")
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

    def test_querying_for_proposal_id_with_unknown_instrument_raises_correct_exception_type(
        self,
    ):
        proposal_system = self.create_client()

        with pytest.raises(InvalidIdException):
            proposal_system.proposal_by_id("::unknown instrument::", VALID_PROPOSAL_ID)

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        proposal_system = self.create_client(unknown_id=True)

        assert proposal_system.proposal_by_id("YMIR", "1234567") is None

    def test_querying_for_samples_by_proposal_id_returns_sample_info(self):
        proposal_system = self.create_client()

        results = proposal_system.samples_by_id("242")

        assert len(results) == 2  # Two samples

        # TODO Finish this
