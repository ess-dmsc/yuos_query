from unittest.mock import ANY

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

    proposal_system = YuosClient(
        SOME_URL, SOME_TOKEN, "YMIR", implementation=mocked_impl
    )

    with pytest.raises(ConnectionException):
        proposal_system.proposal_by_id(VALID_PROPOSAL_ID)


def test_issue_with_getting_proposal_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_proposals_for_instrument.side_effect = TransportServerError("oops")

    proposal_system = YuosClient(
        SOME_URL, SOME_TOKEN, "YMIR", implementation=mocked_impl
    )

    with pytest.raises(ConnectionException):
        proposal_system.proposal_by_id(VALID_PROPOSAL_ID)


def test_querying_for_proposal_id_with_translates_instrument_name_into_correct_id():
    mocked_impl = generate_standard_mock()

    proposal_system = YuosClient(
        SOME_URL, SOME_TOKEN, "YMIR", implementation=mocked_impl
    )
    proposal_system.proposal_by_id(VALID_PROPOSAL_ID)

    # This test is fragile because it relies on the order of the parameters
    mocked_impl.get_proposals_for_instrument.assert_called_with(ANY, ANY, YMIR_INFO[0])


def test_instrument_list_is_called_if_empty_on_proposal_query():
    """
    On previous call it fails to get the instrument list, so when another proposal
    query is made it should try again to get the instrument list.
    """
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST

    proposal_system = YuosClient(
        SOME_URL, SOME_TOKEN, "YMIR", implementation=mocked_impl
    )

    proposal_system.proposal_by_id(VALID_PROPOSAL_ID)

    assert mocked_impl.get_instrument_data.call_count == 1
