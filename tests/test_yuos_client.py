from unittest import mock

import pytest

from example_data import get_ymir_example_data
from yuos_query.data_classes import ProposalInfo, SampleInfo, User
from yuos_query.exceptions import (
    DataUnavailableException,
    InvalidIdException,
    ServerException,
)
from yuos_query.file_cache import FileCache
from yuos_query.proposal_system import ProposalRequester
from yuos_query.utils import serialise_proposals_to_json
from yuos_query.yuos_client import YuosCacheClient, YuosServer

VALID_PROPOSAL_DATA = {
    "471120": ProposalInfo(
        id="471120",
        title="The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        proposer=User("Bob", "Bolmsten", "bobbolmsten", "University A"),
        users=[
            User("jonathan", "Taylor", "jonathantaylor", "ESS"),
            User("Johan", "Andersson", "johanandersson", "University B"),
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
        proposer=User("Andrew", "Jackson", "andrewjackson", "Science"),
        users=[
            User("jonathan", "Taylor", "jonathantaylor", "NSS"),
            User("Caroline", "Curfs", "carolinecurfs", "SAD"),
        ],
        db_id=242,
        samples=[],
    ),
}


class TestYuosServer:
    @pytest.fixture(autouse=True)
    def prepare(self):
        self.cache = mock.create_autospec(FileCache)
        self.system = mock.create_autospec(ProposalRequester)

    def create_server(self, cache=None):
        if not cache:
            cache = self.cache

        return YuosServer("YMIR", cache, self.system)

    def test_on_update_proposal_system_called_and_cache_updated(self):
        server = self.create_server()
        server.update_cache()

        self.system.get_proposals_for_instrument.assert_called_once()
        self.cache.update.assert_called_once()
        self.cache.export_to_file.assert_called_once()

    def test_if_proposal_system_unavailable_then_raises(self):
        server = self.create_server()
        server.update_cache()

        self.system.get_proposals_for_instrument.side_effect = ServerException("oops")

        with pytest.raises(DataUnavailableException):
            _ = server.update_cache()


class TestYuosCacheClient:
    class InMemoryCache(FileCache):
        def _read_file(self):
            return get_ymir_example_data()

    @pytest.fixture(autouse=True)
    def prepare(self):
        self.cache = FileCache("::filepath::")
        self.cache._read_file = lambda: serialise_proposals_to_json(VALID_PROPOSAL_DATA)

    def create_client(
        self,
        cache=None,
    ):
        if not cache:
            cache = self.cache

        return YuosCacheClient(
            cache,
        )

    def test_querying_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        client = self.create_client()
        client.update_cache()

        with pytest.raises(InvalidIdException):
            client.proposal_by_id("abc")

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        client = self.create_client()
        client.update_cache()

        assert client.proposal_by_id("00000") is None

    def test_if_cache_file_missing_then_raises(
        self,
    ):
        client = self.create_client()
        self.cache._read_file = lambda: (_ for _ in ()).throw(FileNotFoundError())

        with pytest.raises(DataUnavailableException):
            client.update_cache()

    def test_querying_for_proposal_by_id_gives_proposal_info(self):
        client = self.create_client()
        client.update_cache()

        proposal_info = client.proposal_by_id("471120")

        assert (
            proposal_info.title
            == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
        )
        assert proposal_info.id == "471120"
        assert proposal_info.users == [
            ("jonathan", "Taylor", "jonathantaylor", "ESS"),
            ("Johan", "Andersson", "johanandersson", "University B"),
        ]
        assert proposal_info.proposer == (
            "Bob",
            "Bolmsten",
            "bobbolmsten",
            "University A",
        )

    def test_can_get_proposals_by_fed_id(self):
        client = self.create_client()
        client.update_cache()

        proposals = client.proposals_for_user("jonathantaylor")

        assert len(proposals) == 2
        assert {p.id for p in proposals} == {"471120", "871067"}

    def test_unrecognised_fed_id(self):
        client = self.create_client()
        client.update_cache()

        proposals = client.proposals_for_user("not_a_fed_id")

        assert len(proposals) == 0
