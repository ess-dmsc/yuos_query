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
KNOWN_PROPOSAL_ID = "352814-1"
KNOWN_FED_ID = "jekabskarklins"


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

        result = client.proposal_by_id(KNOWN_PROPOSAL_ID)

        assert result.id == KNOWN_PROPOSAL_ID
        assert result.proposer == ("Jekabs", "Karklins", "jekabskarklins", "")
        assert result.samples == [
            SampleInfo("262e2b02-be1a-4dd8-8152-8ba9f1a37188"),
            SampleInfo("beed135e-c839-4e04-a0c5-b944517f5490"),
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
