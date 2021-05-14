from unittest import mock

from example_data import get_ymir_example_data
from yuos_query.proposal_system import GqlWrapper, ProposalRequester

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


def test_getting_proposal_information():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [GET_INSTRUMENT_RESPONSE, get_ymir_example_data()]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    proposals = system.get_proposals_for_instrument("ymir")

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
