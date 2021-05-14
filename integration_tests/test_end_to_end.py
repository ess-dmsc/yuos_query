import os

import pytest

from yuos_query.yuos_client import YuosClient

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]

SERVER_URL = "https://useroffice-test.esss.lu.se/graphql"


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_get_proposals_and_sample_for_specific_id_on_ymir_instrument():
    client = YuosClient(SERVER_URL, YUOS_TOKEN, "YMIR")

    result = client.proposal_by_id("471120")

    assert (
        result.title
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
    assert result.id == "471120"
    assert result.users == [
        ("jonathan ", "Taylor"),
        ("Johan", "Andersson"),
    ]
    assert result.proposer == ("Fredrik", "Bolmsten")
    assert len(result.samples) == 3
    assert result.samples[0].name == ""
    assert result.samples[0].formula == "Yb3Ga5O12"
    assert result.samples[0].number == 1
    assert result.samples[0].density == (0, "g/cm*3")
    assert result.samples[0].mass_or_volume == (0, "")
    assert result.samples[1].name == ""
    assert result.samples[1].formula == "(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS"
    assert result.samples[1].number == 1
    assert result.samples[1].density == (0, "g/cm*3")
    assert result.samples[1].mass_or_volume == (0, "µg")
    assert result.samples[2].name == ""
    assert result.samples[2].formula == "PEO, D2O, NaCl, EtOH"
    assert result.samples[2].number == 1
    assert result.samples[2].density == (0, "g/cm*3")
    assert result.samples[2].mass_or_volume == (0, "µg")
