from unittest import mock

from example_data import get_ymir_example_data
from yuos_query.cache import Cache
from yuos_query.proposal_system import _ProposalSystemWrapper

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

YMIR_EXAMPLE_DATA = get_ymir_example_data()


def test_refresh_cache_calls_proposal_system():
    impl = mock.create_autospec(_ProposalSystemWrapper)
    impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST

    cache = Cache(":: some_token ::", ":: some_url ::", "YMIR", implementation=impl)
    cache.refresh()

    impl.get_instrument_data.assert_called_once()
    impl.get_proposals_including_samples_for_instrument.assert_called_once()


def test_cache_gives_dictionary_of_proposals():
    impl = mock.create_autospec(_ProposalSystemWrapper)
    impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    impl.get_proposals_including_samples_for_instrument.return_value = YMIR_EXAMPLE_DATA

    cache = Cache(":: some_token ::", ":: some_url ::", "YMIR", implementation=impl)
    cache.refresh()

    assert len(cache.cached_proposals) == 17
    assert (
        cache.cached_proposals["471120"].title
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
