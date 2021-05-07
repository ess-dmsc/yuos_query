import pytest
from gql.transport.exceptions import TransportServerError

from contract_tests.test_proposal_system_behaviour_mocked import (
    VALID_INSTRUMENT_LIST,
    generate_standard_mock,
)
from yuos_query.exceptions import ConnectionException
from yuos_query.proposal_system import YuosClient

SOME_URL = "https://something.com"
SOME_TOKEN = "not_a_real_token"
VALID_PROPOSAL_ID = "169"
YMIR_INFO = (4, "YMIR")


def test_issue_with_getting_instrument_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.side_effect = TransportServerError("oops")

    with pytest.raises(ConnectionException):
        YuosClient(SOME_URL, SOME_TOKEN, "YMIR", implementation=mocked_impl)


def test_issue_with_getting_proposal_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposals_including_samples_for_instrument.side_effect = (
        TransportServerError("oops")
    )

    with pytest.raises(ConnectionException):
        YuosClient(SOME_URL, SOME_TOKEN, "YMIR", implementation=mocked_impl)
