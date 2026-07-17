import os
from tempfile import TemporaryDirectory

import pytest

from yuos_query.data_classes import SampleInfo
from yuos_query.yuos_client import YuosCacheClient, YuosServer

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]

SERVER_URL = "https://staging.scicat.ess.eu"
KNOWN_PROPOSAL_ID = "248711"
KNOWN_EXPERIMENT_ID = "248711-1"
KNOWN_FED_ID = "junjiequan"


def create_client(directory):
    cache_filepath = os.path.join(directory, "cache.json")
    server = YuosServer.create(SERVER_URL, YUOS_TOKEN, "YMIR", cache_filepath, {})
    server.update_cache()

    client = YuosCacheClient.create(cache_filepath)
    client.update_cache()
    return client


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_and_sample_for_specific_id_on_ymir_instrument():
    with TemporaryDirectory() as directory:
        client = create_client(directory)

        result = client.proposal_by_id(KNOWN_EXPERIMENT_ID)

        assert result.id == KNOWN_EXPERIMENT_ID
        assert result.proposer == ("Junjie", "Quan", "junjiequan", "")
        assert result.samples == [
            SampleInfo("f9e12e7e-a130-4684-9f39-4b483fe9e3e8"),
        ]


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_for_specific_fed_id_on_ymir_instrument():
    with TemporaryDirectory() as directory:
        client = create_client(directory)

        results = client.proposals_for_user(KNOWN_FED_ID)

        assert len(results) > 0
        assert KNOWN_PROPOSAL_ID in {p.id for p in results}
        assert KNOWN_EXPERIMENT_ID in {p.id for p in results}
