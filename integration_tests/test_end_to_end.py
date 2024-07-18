import os
from tempfile import TemporaryDirectory

import pytest

from yuos_query.yuos_client import YuosCacheClient, YuosServer

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]

SERVER_URL = "https://scheduler-staging.useroffice.ess.eu/gateway"
KNOWN_PROPOSAL = "038243"


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_and_sample_for_specific_id_on_ymir_instrument():
    with TemporaryDirectory() as directory:
        server = YuosServer.create(
            SERVER_URL, YUOS_TOKEN, "YMIR", os.path.join(directory, "cache.json"), {}
        )
        server.update_cache()

        client = YuosCacheClient.create(os.path.join(directory, "cache.json"))
        client.update_cache()

        result = client.proposal_by_id(KNOWN_PROPOSAL)

        assert result.title == "VIP demo for WP12"
        assert result.id == KNOWN_PROPOSAL
        assert len(result.users) == 8
        assert ("Afonso", "Mukai", "afonsomukai", "ESS") in result.users
        assert result.proposer == (
            "Matt",
            "Clarke",
            "mattclarke",
            "European Spallation Source ERIC (ESS)",
        )
        assert len(result.samples) == 1
        assert result.samples[0].name == ""
        assert result.samples[0].formula == "Plastic"
        assert result.samples[0].number == 1
        assert result.samples[0].density == (1, "g/cm*3")
        assert result.samples[0].mass_or_volume == (0, "")


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_for_specific_fed_id_on_ymir_instrument():
    with TemporaryDirectory() as directory:
        server = YuosServer.create(
            SERVER_URL, YUOS_TOKEN, "YMIR", os.path.join(directory, "cache.json"), {}
        )
        server.update_cache()

        client = YuosCacheClient.create(os.path.join(directory, "cache.json"))
        client.update_cache()

        results = client.proposals_for_user("mattclarke")
        assert len(results) > 0
        assert KNOWN_PROPOSAL in {p.id for p in results}
