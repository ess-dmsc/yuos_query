import os

from yuos_query.proposal_system import YuosClient

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]


URL = "https://useroffice-test.esss.lu.se/graphql"


def test_retrival_of_all_proposals_for_an_instrument():
    client = YuosClient(URL, YUOS_TOKEN)

    results = client.get_proposals_and_samples_for_an_instrument("YMIR")

    assert len(results) == 17
    assert (
        results["471120"]["title"]
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )

    assert results["471120"]["id"] == 169
    assert results["471120"]["users"] == [
        ("jonathan ", "Taylor"),
        ("Johan", "Andersson"),
    ]
    assert results["471120"]["proposer"] == ("Fredrik", "Bolmsten")
    assert len(results["471120"]["samples"]) == 3
    assert results["471120"]["samples"][0].name == ""
    assert results["471120"]["samples"][0].formula == "Yb3Ga5O12"
    assert results["471120"]["samples"][0].number == 1
    assert results["471120"]["samples"][0].density == (0, "g/cm*3")
    assert results["471120"]["samples"][0].mass_or_volume == (0, "")
