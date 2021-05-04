from unittest import mock

from requests.exceptions import ConnectionError

from contract_tests.proposal_system_contract import ProposalSystemContract
from example_data import get_example_sample_data, get_ymir_example_data
from yuos_query.proposal_system import YuosClient, _ProposalSystemWrapper

SAMPLE_EXAMPLE = get_example_sample_data()
YMIR_EXAMPLE_DATA = get_ymir_example_data()

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
    mocked_impl.get_proposals_for_instrument.return_value = VALID_RESPONSE_DATA
    mocked_impl.get_sample_details_by_proposal_id.return_value = SAMPLE_EXAMPLE
    mocked_impl.get_proposals_including_samples_for_instrument.return_value = (
        YMIR_EXAMPLE_DATA
    )
    return mocked_impl


class TestProposalSystemMocked(ProposalSystemContract):
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
            mocked_impl.get_proposals_for_instrument.side_effect = ConnectionError(
                "oops"
            )
        if unknown_id:
            mocked_impl.get_proposals_for_instrument.return_value = (
                UNKNOWN_INSTRUMENT_ID_RESPONSE
            )

        return YuosClient("https://something.com", "not_a_real_token", mocked_impl)

    # Tests are inherited from ProposalSystemContract
