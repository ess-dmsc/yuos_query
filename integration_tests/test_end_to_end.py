import os
from tempfile import TemporaryDirectory

import pytest

from yuos_query.yuos_client import YuosClient

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]

SERVER_URL = "https://useroffice-test.esss.lu.se/graphql"
KNOWN_PROPOSAL = "199842"


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_and_sample_for_specific_id_on_ymir_instrument():
    with TemporaryDirectory() as directory:
        client = YuosClient(
            SERVER_URL, YUOS_TOKEN, "YMIR", os.path.join(directory, "cache.json")
        )

        result = client.proposal_by_id(KNOWN_PROPOSAL)

        assert result.title == "Dynamics of Supercooled H2O in confined geometries"
        assert result.id == KNOWN_PROPOSAL
        assert result.users == [
            ("pascale", "deen", "pascaledeen", "Other"),
            (
                "Andrew",
                "Jackson",
                "andrewjackson",
                "European Spallation Source ERIC (ESS)",
            ),
        ]
        assert result.proposer == (
            "Jonathan",
            "Taylor",
            "jonathantaylor",
            "European Spallation Source ERIC (ESS)",
        )
        assert len(result.samples) == 2
        assert result.samples[0].name == ""
        assert result.samples[0].formula == "H2O"
        assert result.samples[0].number == 1
        assert result.samples[0].density == (1, "g/cm*3")
        assert result.samples[0].mass_or_volume == (7, "mL")
        assert result.samples[1].name == ""
        assert result.samples[1].formula == "SiO2 - B2O3"
        assert result.samples[1].number == 1
        assert result.samples[1].density == (5.5, "g/cm*3")
        assert result.samples[1].mass_or_volume == (10, "g")


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_for_specific_fed_id_on_ymir_instrument():
    with TemporaryDirectory() as directory:
        client = YuosClient(
            SERVER_URL, YUOS_TOKEN, "YMIR", os.path.join(directory, "cache.json")
        )

        results = client.proposals_for_user("jonathantaylor")
        assert len(results) == 6
        assert {p.id for p in results} == {
            "871067",
            "169700",
            "035455",
            "139558",
            "199842",
            "509363",
        }
