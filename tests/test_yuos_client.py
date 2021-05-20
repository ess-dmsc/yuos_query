from unittest import mock

import pytest

from yuos_query.cache import Cache
from yuos_query.data_classes import ProposalInfo, SampleInfo
from yuos_query.exceptions import (
    DataUnavailableException,
    ImportCacheException,
    InvalidIdException,
    ServerException,
)
from yuos_query.proposal_system import ProposalRequester
from yuos_query.yuos_client import YuosClient

VALID_PROPOSAL_DATA = {
    "471120": ProposalInfo(
        id="471120",
        title="The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        proposer=("Fredrik", "Bolmsten"),
        users=[("jonathan ", "Taylor"), ("Johan", "Andersson")],
        db_id=169,
        samples=[
            SampleInfo(
                name="",
                formula="Yb3Ga5O12",
                number=1,
                mass_or_volume=(0, ""),
                density=(0, "g/cm*3"),
            ),
            SampleInfo(
                name="",
                formula="(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS",
                number=1,
                mass_or_volume=(0, "µg"),
                density=(0, "g/cm*3"),
            ),
        ],
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
        self.system = mock.create_autospec(ProposalRequester)

    def test_on_construction_proposal_system_called_and_cache_updated(self):
        _ = YuosClient(
            ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
        )

        self.system.get_proposals_for_instrument.assert_called_once()
        self.cache.update.assert_called_once()

    def test_on_refreshing_cache_proposal_system_called_and_cache_updated(self):
        _ = YuosClient(
            ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
        )

        self.system.get_proposals_for_instrument.assert_called_once()
        self.cache.update.assert_called_once()

    def test_querying_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        client = YuosClient(
            ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
        )

        with pytest.raises(InvalidIdException):
            client.proposal_by_id("abc")

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        self.cache.proposals = VALID_PROPOSAL_DATA

        client = YuosClient(
            ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
        )

        assert client.proposal_by_id("00000") is None

    def test_querying_for_proposal_by_id_gives_proposal_info(self):
        self.cache.proposals = VALID_PROPOSAL_DATA

        client = YuosClient(
            ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
        )
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

    def test_if_proposal_system_unavailable_load_from_cache(self):
        self.system.get_proposals_for_instrument.side_effect = ServerException("oops")

        _ = YuosClient(
            ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
        )
        self.cache.import_from_json.assert_called_once()

    def test_if_proposal_system_unavailable_and_load_from_cache_raises(self):
        self.system.get_proposals_for_instrument.side_effect = ServerException("oops")
        self.cache.import_from_json.side_effect = ImportCacheException("oops")

        with pytest.raises(DataUnavailableException):
            _ = YuosClient(
                ":: url ::", ":: token ::", "YMIR", cache=self.cache, system=self.system
            )
