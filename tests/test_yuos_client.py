from unittest import mock

import pytest

from yuos_query.data_classes import ProposalInfo, SampleInfo, User
from yuos_query.exceptions import (
    DataUnavailableException,
    ImportCacheException,
    InvalidIdException,
    ServerException,
)
from yuos_query.file_cache import FileCache
from yuos_query.proposal_system import ProposalRequester
from yuos_query.yuos_client import YuosClient

VALID_PROPOSAL_DATA = {
    "471120": ProposalInfo(
        id="471120",
        title="The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        proposer=User("Bob", "Bolmsten", "bobbolmsten"),
        users=[
            User("jonathan", "Taylor", "jonathantaylor"),
            User("Johan", "Andersson", "johanandersson"),
        ],
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
        proposer=User("Andrew", "Jackson", "andrewjackson"),
        users=[
            User("jonathan", "Taylor", "jonathantaylor"),
            User("Caroline", "Curfs", "carolinecurfs"),
        ],
        db_id=242,
        samples=[],
    ),
}


class TestYuosClient:
    @pytest.fixture(autouse=True)
    def prepare(self):
        self.cache = mock.create_autospec(FileCache)
        self.system = mock.create_autospec(ProposalRequester)

    def create_client(self, cache=None, update_cache=True):
        if not cache:
            cache = self.cache

        return YuosClient(
            ":: url ::",
            ":: token ::",
            "YMIR",
            ":: file ::",
            update_cache=update_cache,
            cache=cache,
            system=self.system,
        )

    def test_on_construction_proposal_system_called_and_cache_updated(self):
        _ = self.create_client()

        self.system.get_proposals_for_instrument.assert_called_once()
        self.cache.update.assert_called_once()
        self.cache.export_to_file.assert_called_once()

    def test_on_refreshing_cache_proposal_system_called_and_cache_updated(self):
        _ = self.create_client()

        self.system.get_proposals_for_instrument.assert_called_once()
        self.cache.update.assert_called_once()

    def test_querying_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        client = self.create_client()

        with pytest.raises(InvalidIdException):
            client.proposal_by_id("abc")

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        self.cache.proposals = VALID_PROPOSAL_DATA

        client = self.create_client()

        assert client.proposal_by_id("00000") is None

    def test_querying_for_proposal_by_id_gives_proposal_info(self):
        self.cache.proposals = VALID_PROPOSAL_DATA

        client = self.create_client()
        proposal_info = client.proposal_by_id("471120")

        assert (
            proposal_info.title
            == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
        )
        assert proposal_info.id == "471120"
        assert proposal_info.users == [
            ("jonathan", "Taylor", "jonathantaylor"),
            ("Johan", "Andersson", "johanandersson"),
        ]
        assert proposal_info.proposer == ("Bob", "Bolmsten", "bobbolmsten")

    def test_if_proposal_system_unavailable_load_from_cache(self):
        self.system.get_proposals_for_instrument.side_effect = ServerException("oops")

        _ = self.create_client()
        self.cache.import_from_file.assert_called_once()

    def test_if_proposal_system_unavailable_and_load_from_cache_raises(self):
        self.system.get_proposals_for_instrument.side_effect = ServerException("oops")
        self.cache.import_from_file.side_effect = ImportCacheException("oops")

        with pytest.raises(DataUnavailableException):
            _ = self.create_client()

    def test_if_proposal_system_unavailable_and_cache_not_empty_then_do_not_import(
        self,
    ):
        self.system.get_proposals_for_instrument.side_effect = ServerException("oops")
        self.cache.is_empty.return_value = False

        _ = self.create_client()
        self.cache.import_from_file.assert_not_called()

    def test_on_refresh_proposal_system_called_and_cache_updated(self):
        client = self.create_client()
        self.cache.reset_mock()
        self.system.reset_mock()

        client.update_cache()

        self.system.get_proposals_for_instrument.assert_called_once()
        self.cache.update.assert_called_once()
        self.cache.export_to_file.assert_called_once()

    def test_can_get_proposals_by_fed_id(self):
        cache = FileCache(":: filepath ::")
        cache.update(VALID_PROPOSAL_DATA)
        self.system.get_proposals_for_instrument.return_value = VALID_PROPOSAL_DATA

        client = self.create_client(cache, update_cache=False)
        proposals = client.proposals_for_user("jonathantaylor")

        assert len(proposals) == 2
        assert {p.id for p in proposals} == {"471120", "871067"}

    def test_unrecognised_fed_id(self):
        cache = FileCache(":: filepath ::")
        cache.update(VALID_PROPOSAL_DATA)
        self.system.get_proposals_for_instrument.return_value = VALID_PROPOSAL_DATA

        client = self.create_client(cache, update_cache=False)
        proposals = client.proposals_for_user("not_a_fed_id")

        assert len(proposals) == 0
