from unittest import mock

import pytest
from gql.transport.exceptions import TransportServerError

from contract_tests.test_proposal_system_behaviour_mocked import (
    VALID_INSTRUMENT_LIST,
    generate_standard_mock,
)
from example_data import get_ymir_example_data
from yuos_query.cache import Cache
from yuos_query.exceptions import ConnectionException
from yuos_query.proposal_system import ProposalSystem

YMIR_EXAMPLE_DATA = get_ymir_example_data()


def test_refresh_cache_calls_proposal_system():
    impl = mock.create_autospec(ProposalSystem)
    impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST

    cache = Cache(":: some_url ::", ":: some_token ::", "YMIR", implementation=impl)
    cache.refresh()

    impl.get_instrument_data.assert_called_once()
    impl.get_proposals_including_samples_for_instrument.assert_called_once()


def test_cache_gives_dictionary_of_proposals():
    impl = mock.create_autospec(ProposalSystem)
    impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    impl.get_proposals_including_samples_for_instrument.return_value = YMIR_EXAMPLE_DATA

    cache = Cache(":: some_url ::", ":: some_token ::", "YMIR", implementation=impl)
    cache.refresh()

    assert len(cache.cached_proposals) == 17
    assert (
        cache.cached_proposals["471120"].title
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
    assert cache.cached_proposals["471120"].id == "471120"
    assert cache.cached_proposals["471120"].users == [
        ("jonathan ", "Taylor"),
        ("Johan", "Andersson"),
    ]
    assert cache.cached_proposals["471120"].proposer == ("Fredrik", "Bolmsten")
    assert len(cache.cached_proposals["471120"].samples) == 3
    assert cache.cached_proposals["471120"].samples[0].name == ""
    assert cache.cached_proposals["471120"].samples[0].formula == "Yb3Ga5O12"
    assert cache.cached_proposals["471120"].samples[0].number == 1
    assert cache.cached_proposals["471120"].samples[0].density == (0, "g/cm*3")
    assert cache.cached_proposals["471120"].samples[0].mass_or_volume == (0, "")
    assert cache.cached_proposals["471120"].samples[1].name == ""
    assert (
        cache.cached_proposals["471120"].samples[1].formula
        == "(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS"
    )
    assert cache.cached_proposals["471120"].samples[1].number == 1
    assert cache.cached_proposals["471120"].samples[1].density == (0, "g/cm*3")
    assert cache.cached_proposals["471120"].samples[1].mass_or_volume == (0, "µg")


SOME_URL = "https://something.com"
SOME_TOKEN = "not_a_real_token"
VALID_PROPOSAL_ID = "169"
YMIR_INFO = (4, "YMIR")


def test_issue_with_getting_instrument_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.side_effect = TransportServerError("oops")

    cache = Cache(SOME_TOKEN, SOME_URL, "YMIR", implementation=mocked_impl)
    with pytest.raises(ConnectionException):
        cache.refresh()


def test_issue_with_getting_proposal_data_from_system_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposals_including_samples_for_instrument.side_effect = (
        TransportServerError("oops")
    )
    cache = Cache(SOME_TOKEN, SOME_URL, "YMIR", implementation=mocked_impl)
    with pytest.raises(ConnectionException):
        cache.refresh()
