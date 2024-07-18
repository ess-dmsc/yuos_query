from unittest import mock

import pytest

from example_data import get_ymir_example_data
from yuos_query.data_classes import User
from yuos_query.exceptions import UnknownInstrumentException
from yuos_query.proposal_system import GqlWrapper, ProposalRequester

KNOWN_PROPOSAL_ID = "597001"
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

    system = ProposalRequester(":: url ::", ":: token ::", {}, wrapper)

    proposals = system.get_proposals_for_instrument("ymir")
    assert len(proposals) > 10
    assert proposals[KNOWN_PROPOSAL_ID].title == "For testing yuos"
    assert proposals[KNOWN_PROPOSAL_ID].id == KNOWN_PROPOSAL_ID
    assert proposals[KNOWN_PROPOSAL_ID].users == [
        User(
            firstname="Fredrik",
            lastname="Bolmsten",
            fed_id="fredrikbolmsten",
            organisation="European Spallation Source ERIC (ESS)",
        ),
        User(
            firstname="Jonas",
            lastname="Petersson",
            fed_id="jonaspetersson",
            organisation="Other",
        ),
    ]
    assert proposals[KNOWN_PROPOSAL_ID].proposer == (
        User(
            firstname="Matt",
            lastname="Clarke",
            fed_id="mattclarke",
            organisation="European Spallation Source ERIC (ESS)",
        )
    )
    assert len(proposals[KNOWN_PROPOSAL_ID].samples) == 2


def test_ignore_instrument_name_case():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, get_ymir_example_data()]

    system = ProposalRequester(":: url ::", ":: token ::", {}, wrapper)

    proposals = system.get_proposals_for_instrument("yMiR")

    assert len(proposals) > 10


def test_unrecognised_instrument_raises():
    wrapper = mock.create_autospec(GqlWrapper)
    wrapper.request.side_effect = [INSTRUMENT_INFO_RESPONSE, get_ymir_example_data()]

    system = ProposalRequester(":: url ::", ":: token ::", {}, wrapper)

    with pytest.raises(UnknownInstrumentException):
        system.get_proposals_for_instrument("NOT AN INSTRUMENT")
