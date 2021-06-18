from unittest import mock

import pytest

from example_data import get_ymir_example_data
from yuos_query.exceptions import UnknownInstrumentException
from yuos_query.proposal_system import GqlWrapper, ProposalRequester

KNOWN_PROPOSAL_ID = "471120"
YMIR_EXAMPLE_DATA = get_ymir_example_data()
INSTRUMENT_INFO_RESPONSE = {
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
                "id": 5,
                "shortCode": "DREAM",
                "description": "Bispectral Powder Diffractometer",
                "name": "DREAM",
            },
            {
                "id": 4,
                "shortCode": "YMIR",
                "description": "Test beamline",
                "name": "YMIR",
            },
        ]
    }
}


def test_gets_proposal_information():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, YMIR_EXAMPLE_DATA]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    proposals = system.get_proposals_for_instrument("ymir")

    assert len(proposals) == 17
    assert (
        proposals[KNOWN_PROPOSAL_ID].title
        == "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12"
    )
    assert proposals[KNOWN_PROPOSAL_ID].id == KNOWN_PROPOSAL_ID
    assert proposals[KNOWN_PROPOSAL_ID].users == [
        ("jonathan", "Taylor"),
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


def test_ignore_instrument_name_case():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, YMIR_EXAMPLE_DATA]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    proposals = system.get_proposals_for_instrument("yMiR")

    assert len(proposals) == 17


def test_unrecognised_instrument_raises():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, YMIR_EXAMPLE_DATA]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    with pytest.raises(UnknownInstrumentException):
        system.get_proposals_for_instrument("NOT AN INSTRUMENT")
