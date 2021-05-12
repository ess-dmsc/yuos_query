from unittest import mock

import pytest
from gql.transport.exceptions import TransportQueryError
from graphql import GraphQLError

from example_data import get_ymir_example_data
from yuos_query.cache import Cache
from yuos_query.exceptions import (
    ConnectionException,
    InvalidIdException,
    InvalidQueryException,
)
from yuos_query.proposal_system import ProposalSystem

YMIR_EXAMPLE_DATA = get_ymir_example_data()

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


def test_refresh_cache_calls_proposal_system():
    impl = mock.create_autospec(ProposalSystem)
    impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST

    cache = Cache(":: some_url ::", ":: some_token ::", "YMIR", implementation=impl)
    cache.refresh()

    impl.get_instrument_data.assert_called_once()
    impl.get_proposals_by_instrument_id.assert_called_once()


def test_cache_can_retrieve_proposals():
    impl = mock.create_autospec(ProposalSystem)
    impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    impl.get_proposals_by_instrument_id.return_value = YMIR_EXAMPLE_DATA

    cache = Cache(":: some_url ::", ":: some_token ::", "YMIR", implementation=impl)
    cache.refresh()

    assert len(cache.proposals) == 17
    assert (
        cache.proposals["471120"].title
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
    assert cache.proposals["471120"].id == "471120"
    assert cache.proposals["471120"].users == [
        ("jonathan ", "Taylor"),
        ("Johan", "Andersson"),
    ]
    assert cache.proposals["471120"].proposer == ("Fredrik", "Bolmsten")
    assert len(cache.proposals["471120"].samples) == 3
    assert cache.proposals["471120"].samples[0].name == ""
    assert cache.proposals["471120"].samples[0].formula == "Yb3Ga5O12"
    assert cache.proposals["471120"].samples[0].number == 1
    assert cache.proposals["471120"].samples[0].density == (0, "g/cm*3")
    assert cache.proposals["471120"].samples[0].mass_or_volume == (0, "")
    assert cache.proposals["471120"].samples[1].name == ""
    assert (
        cache.proposals["471120"].samples[1].formula
        == "(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS"
    )
    assert cache.proposals["471120"].samples[1].number == 1
    assert cache.proposals["471120"].samples[1].density == (0, "g/cm*3")
    assert cache.proposals["471120"].samples[1].mass_or_volume == (0, "µg")


def test_getting_proposals_for_unknown_instrument_raises_correct_exception_type():
    mocked_impl = mock.create_autospec(ProposalSystem)
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST

    cache = Cache(
        ":: url ::",
        ":: token ::",
        "NOT AN INSTRUMENT",
        implementation=mocked_impl,
    )
    with pytest.raises(InvalidIdException):
        cache.refresh()


def test_cache_ignores_instrument_name_casing():
    mocked_impl = mock.create_autospec(ProposalSystem)
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposals_by_instrument_id.return_value = YMIR_EXAMPLE_DATA

    cache = Cache(":: url ::", ":: token ::", "yMIr", implementation=mocked_impl)
    cache.refresh()

    assert len(cache.proposals)


def test_querying_with_invalid_token_raises():
    mocked_impl = mock.create_autospec(ProposalSystem)
    mocked_impl.get_instrument_data.side_effect = TransportQueryError("oops")

    cache = Cache(":: url ::", ":: token ::", "YMIR", implementation=mocked_impl)
    with pytest.raises(ConnectionException):
        cache.refresh()


def test_querying_with_non_server_url_raises():
    mocked_impl = mock.create_autospec(ProposalSystem)
    mocked_impl.get_instrument_data.side_effect = ConnectionError("oops")

    cache = Cache("https://wwww.google.com", ":: token ::", "YMIR")

    with pytest.raises(ConnectionException):
        cache.refresh()


def test_gql_query_exception_raises_correct_exception():
    """
    GraphQL raises a specific exception if there is something wrong with the query.

    For example: if the query json is invalid
    """
    mocked_impl = mock.create_autospec(ProposalSystem)
    mocked_impl.get_instrument_data.side_effect = GraphQLError("oops")

    cache = Cache(":: url ::", ":: token ::", "YMIR", implementation=mocked_impl)

    with pytest.raises(InvalidQueryException):
        cache.refresh()
