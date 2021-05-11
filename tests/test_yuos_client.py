from unittest import mock

import pytest

from yuos_query.cache import Cache
from yuos_query.data_classes import ProposalInfo, SampleInfo
from yuos_query.exceptions import InvalidIdException
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
            SampleInfo(
                name="",
                formula="PEO, D2O, NaCl, EtOH",
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
        samples=[
            SampleInfo(
                name="",
                formula="CHE3S",
                number=10,
                mass_or_volume=(5, "kg"),
                density=(0, "g/cm*3"),
            ),
            SampleInfo(
                name="",
                formula="unknown",
                number=1,
                mass_or_volume=(100, "g"),
                density=(0, "g/cm*3"),
            ),
        ],
    ),
}


class TestYuosClient:
    def test_during_client_construction_cache_refresh_is_called(self):
        mock_cache = mock.create_autospec(Cache)
        _ = YuosClient(":: some_url ::", ":: some_token ::", "YMIR", mock_cache)

        mock_cache.refresh.assert_called_once()

    def test_querying_for_proposal_by_id_with_id_that_does_not_conform_to_pattern_raises(
        self,
    ):
        mock_cache = mock.create_autospec(Cache)
        client = YuosClient(":: some_url ::", ":: some_token ::", "YMIR", mock_cache)

        with pytest.raises(InvalidIdException):
            client.proposal_by_id("abc")

    def test_querying_for_unknown_proposal_id_returns_nothing(self):
        mock_cache = mock.create_autospec(Cache)
        mock_cache.proposals = VALID_PROPOSAL_DATA

        client = YuosClient(":: some_url ::", ":: some_token ::", "YMIR", mock_cache)

        assert client.proposal_by_id("00000") is None

    def test_querying_for_proposal_by_id_gives_proposal_info(self):
        mock_cache = mock.create_autospec(Cache)
        mock_cache.proposals = VALID_PROPOSAL_DATA

        client = YuosClient(":: some_url ::", ":: some_token ::", "YMIR", mock_cache)
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
        assert len(proposal_info.samples) == 3
        assert proposal_info.samples[0].name == ""
        assert proposal_info.samples[0].formula == "Yb3Ga5O12"
        assert proposal_info.samples[0].number == 1
        assert proposal_info.samples[0].density == (0, "g/cm*3")
        assert proposal_info.samples[0].mass_or_volume == (0, "")
        assert proposal_info.samples[1].name == ""
        assert (
            proposal_info.samples[1].formula == "(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS"
        )
        assert proposal_info.samples[1].number == 1
        assert proposal_info.samples[1].density == (0, "g/cm*3")
        assert proposal_info.samples[1].mass_or_volume == (0, "µg")
