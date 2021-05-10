from unittest import mock

from requests.exceptions import ConnectionError

from contract_tests.proposal_system_contract import ProposalSystemContract
from example_data import get_ymir_example_data
from yuos_query.cache import Cache
from yuos_query.proposal_system import ProposalSystem
from yuos_query.yuos_client import YuosClient

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
    mocked_impl = mock.create_autospec(ProposalSystem)
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposals_including_samples_for_instrument.return_value = (
        YMIR_EXAMPLE_DATA
    )
    return mocked_impl


class TestProposalSystemMocked(ProposalSystemContract):
    def create_client(
        self,
        instrument_name: str = "YMIR",
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
        if unknown_id:
            mocked_impl.get_proposals_including_samples_for_instrument.return_value = (
                UNKNOWN_INSTRUMENT_ID_RESPONSE
            )

        return YuosClient(
            "https://something.com",
            "not_a_real_token",
            instrument_name,
            cache=Cache(
                "not_a_real_token",
                "https://something.com",
                instrument_name,
                mocked_impl,
            ),
        )

    # Tests are inherited from ProposalSystemContract

    def test_client_refreshes_cache_on_construction(self):
        impl = mock.create_autospec(Cache)

        _ = YuosClient(":: some url ::", ":: some token ::", "YMIR", impl)

        impl.refresh.assert_called_once()
