from unittest import mock

import pytest

from yuos_query.cache import Cache
from yuos_query.data_classes import ProposalInfo
from yuos_query.exceptions import InvalidIdException
from yuos_query.proposal_system import ProposalSystem
from yuos_query.yuos_client import YuosClient

VALID_PROPOSAL_DATA = {
    "471120": ProposalInfo(
        id="471120",
        title="The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        proposer=("Fredrik", "Bolmsten"),
        users=[("jonathan ", "Taylor"), ("Johan", "Andersson")],
        db_id=169,
        samples=[],
    ),
    "871067": ProposalInfo(
        id="871067",
        title="The Structure of Cheese Under Pressure",
        proposer=("Andrew", "Jackson"),
        users=[("jonathan ", "Taylor"), ("Caroline", "Curfs")],
        db_id=242,
        samples=[],
    ),
}


class TestYuosClient:
    @pytest.fixture(autouse=True)
    def prepare(self):
        self.cache = mock.create_autospec(Cache)
        self.system = mock.create_autospec(ProposalSystem)

    def test_on_construction_proposal_system_called_and_cache_updated(self):
        _ = YuosClient(":: url ::", ":: token ::", "YMIR", self.cache, self.system)

        self.system.get_instrument_data.assert_called_once()
        self.system.get_proposals_by_instrument_id.assert_called_once()
        self.cache.update.assert_called_once()

    def test_on_refreshing_cache_proposal_system_called_and_cache_updated(self):
        _ = YuosClient(":: url ::", ":: token ::", "YMIR", self.cache, self.system)

        self.system.get_instrument_data.assert_called_once()
        self.system.get_proposals_by_instrument_id.assert_called_once()
        self.cache.update.assert_called_once()

    def test_querying_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        client = YuosClient(":: url ::", ":: token ::", "YMIR", self.cache, self.system)

        with pytest.raises(InvalidIdException):
            client.proposal_by_id("abc")

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        self.cache.proposals = VALID_PROPOSAL_DATA

        client = YuosClient(":: url ::", ":: token ::", "YMIR", self.cache, self.system)

        assert client.proposal_by_id("00000") is None

    def test_querying_for_proposal_by_id_gives_proposal_info(self):
        self.cache.proposals = VALID_PROPOSAL_DATA

        client = YuosClient(":: url ::", ":: token ::", "YMIR", self.cache, self.system)
        proposal_info = client.proposal_by_id("471120")

        assert (
            proposal_info.title
            == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
        )
        assert proposal_info.id == "471120"
        assert proposal_info.users == [
            ("jonathan ", "Taylor"),
            ("Johan", "Andersson"),
        ]
        assert proposal_info.proposer == ("Fredrik", "Bolmsten")
