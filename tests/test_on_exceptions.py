from unittest.mock import ANY

import pytest
from gql.transport.exceptions import TransportServerError

from proposal_system import ConnectionException, ProposalSystemClient

from .test_proposal_system_behaviour import (
    VALID_INSTRUMENT_LIST,
    generate_standard_mock,
)

SOME_URL = "https://something.com"
SOME_USER = "account@ess.eu"
SOME_PASSWORD = "apassword"
SOME_TOKEN = {"login": {"token": "eyJhbG"}}
VALID_PROPOSAL_ID = 169
YMIR_INFO = (4, "YMIR")


def test_issue_with_getting_instrument_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.side_effect = TransportServerError("oops")

    proposal_system = ProposalSystemClient(
        SOME_URL, SOME_USER, SOME_PASSWORD, mocked_impl
    )

    with pytest.raises(ConnectionException):
        proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)


def test_issue_with_getting_proposal_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_proposal_for_instrument.side_effect = TransportServerError("oops")

    proposal_system = ProposalSystemClient(
        SOME_URL, SOME_USER, SOME_PASSWORD, mocked_impl
    )

    with pytest.raises(ConnectionException):
        proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)


def test_once_token_received_then_it_is_cached_for_subsequent_calls():
    mocked_impl = generate_standard_mock()

    proposal_system = ProposalSystemClient(
        SOME_URL, SOME_USER, SOME_PASSWORD, mocked_impl
    )

    # Multiple calls
    _ = proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)
    _ = proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)
    _ = proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

    assert mocked_impl.get_token.call_count == 1


def test_querying_for_proposal_id_with_translates_instrument_name_into_correct_id():
    mocked_impl = generate_standard_mock()

    proposal_system = ProposalSystemClient(
        SOME_URL, SOME_USER, SOME_PASSWORD, mocked_impl
    )
    proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

    # This test is fragile because it relies on the order of the parameters
    mocked_impl.get_proposal_for_instrument.assert_called_with(ANY, ANY, YMIR_INFO[0])


def test_instrument_list_is_called_if_empty_on_proposal_query():
    """
    On previous call it fails to get the instrument list, so when another proposal
    query is made it should try again to get the instrument list.
    """
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST

    proposal_system = ProposalSystemClient(
        SOME_URL,
        SOME_USER,
        SOME_PASSWORD,
        mocked_impl,
    )

    proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

    assert mocked_impl.get_instrument_data.call_count == 1
