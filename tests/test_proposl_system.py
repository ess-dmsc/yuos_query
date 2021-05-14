from unittest import mock

from example_data import get_ymir_example_data
from yuos_query.proposal_system import GqlWrapper, ProposalSystem

KNOWN_PROPOSAL_ID = "471120"

YMIR_ID = 4
DREAM_ID = 5

GET_INSTRUMENT_RESPONSE = {
    "instruments": {
        "instruments": [
            {
                "id": 7,
                "shortCode": "asztalos",
                "description": "test instrument\n",
                "name": "asztalos",
            },
            {
                "id": 6,
                "shortCode": "DEMAX",
                "description": "DEMAX Lab",
                "name": "DEMAX",
            },
            {
                "id": DREAM_ID,
                "shortCode": "DREAM",
                "description": "Bispectral Powder Diffractometer",
                "name": "DREAM",
            },
            {
                "id": YMIR_ID,
                "shortCode": "YMIR",
                "description": "Test beamline",
                "name": "YMIR",
            },
        ]
    }
}


def test_getting_instrument_information():
    impl = mock.create_autospec(GqlWrapper)
    impl.request.return_value = GET_INSTRUMENT_RESPONSE

    system = ProposalSystem(":: url ::", ":: token ::", impl)

    results = system.get_instrument_data()

    assert results["ymir"] == YMIR_ID
    assert results["dream"] == DREAM_ID


def test_getting_proposal_information():
    impl = mock.create_autospec(GqlWrapper)
    impl.request.return_value = get_ymir_example_data()

    system = ProposalSystem(":: url ::", ":: token ::", impl)

    proposals = system.get_proposals_by_instrument_id(":: id ::")

    assert len(proposals) == 17
    assert (
        proposals[KNOWN_PROPOSAL_ID].title
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
    assert proposals[KNOWN_PROPOSAL_ID].id == KNOWN_PROPOSAL_ID
    assert proposals[KNOWN_PROPOSAL_ID].users == [
        ("jonathan ", "Taylor"),
        ("Johan", "Andersson"),
    ]
    assert proposals[KNOWN_PROPOSAL_ID].proposer == ("Fredrik", "Bolmsten")
    assert len(proposals[KNOWN_PROPOSAL_ID].samples) == 3
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].name == ""
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].formula == "Yb3Ga5O12"
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].number == 1
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].density == (0, "g/cm*3")
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].mass_or_volume == (0, "")
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].name == ""
    assert (
        proposals[KNOWN_PROPOSAL_ID].samples[1].formula
        == "(EO)20-(PO)45-(EO)30, D2O, NaCl, SDS"
    )
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].number == 1
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].density == (0, "g/cm*3")
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].mass_or_volume == (0, "µg")
