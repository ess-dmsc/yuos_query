from unittest import mock

import pytest

from example_data import get_ymir_example_data
from yuos_query.exceptions import UnknownInstrumentException
from yuos_query.proposal_system import GqlWrapper, ProposalRequester

KNOWN_PROPOSAL_ID = "199842"
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
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, get_ymir_example_data()]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    proposals = system.get_proposals_for_instrument("ymir")
    assert len(proposals) == 19
    assert (
        proposals[KNOWN_PROPOSAL_ID].title
        == "Dynamics of Supercooled H2O in confined geometries"
    )
    assert proposals[KNOWN_PROPOSAL_ID].id == KNOWN_PROPOSAL_ID
    assert proposals[KNOWN_PROPOSAL_ID].users == [
        ("pascale", "deen", "pascaledeen", "Other"),
        ("Andrew", "Jackson", "andrewjackson", "European Spallation Source ERIC (ESS)"),
    ]
    assert proposals[KNOWN_PROPOSAL_ID].proposer == (
        "Jonathan",
        "Taylor",
        "jonathantaylor",
        "European Spallation Source ERIC (ESS)",
    )
    assert len(proposals[KNOWN_PROPOSAL_ID].samples) == 2
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].name == ""
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].formula == "H2O"
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].number == 1
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].density == (1, "g/cm*3")
    assert proposals[KNOWN_PROPOSAL_ID].samples[0].mass_or_volume == (7, "mL")
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].name == ""
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].formula == "SiO2 - B2O3"
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].number == 1
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].density == (5.5, "g/cm*3")
    assert proposals[KNOWN_PROPOSAL_ID].samples[1].mass_or_volume == (10, "g")


def test_ignore_instrument_name_case():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, get_ymir_example_data()]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    proposals = system.get_proposals_for_instrument("yMiR")

    assert len(proposals) == 19


def test_unrecognised_instrument_raises():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, get_ymir_example_data()]

    system = ProposalRequester(":: url ::", ":: token ::", wrapper)

    with pytest.raises(UnknownInstrumentException):
        system.get_proposals_for_instrument("NOT AN INSTRUMENT")
