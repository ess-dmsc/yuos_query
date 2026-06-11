from unittest import mock

import pytest
from example_data import get_sample_example_data, get_ymir_example_data
from yuos_query.data_classes import User
from yuos_query.exceptions import UnknownInstrumentException
from yuos_query.proposal_system_scicat import ProposalRequester

YMIR_UUID = "ebfb7106-b885-4eda-b414-3f6fb80443e4"
DREAM_UUID = "554e7fe2-a16e-11ed-bafb-f34f3b09d136"
KNOWN_PROPOSAL_ID = "711730"

INSTRUMENT_INFO_RESPONSE = [
    {"name": "YMIR", "id": YMIR_UUID},
    {"name": "DREAM", "id": DREAM_UUID},
]


def _make_mock_response(data, status_code=200):
    response = mock.Mock()
    response.status_code = status_code
    response.json.return_value = data
    response.raise_for_status = mock.Mock()
    return response


def _url_based_get(url, **kwargs):
    if "/api/v3/instruments" in url:
        return _make_mock_response(INSTRUMENT_INFO_RESPONSE)
    elif "/api/v3/proposals" in url:
        return _make_mock_response(get_ymir_example_data())
    elif "/api/v3/samples" in url:
        return _make_mock_response([])
    raise ValueError(f"Unexpected URL: {url}")


def test_gets_proposal_information():
    with mock.patch("requests.get", side_effect=_url_based_get):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposals = system.get_proposals_for_instrument("ymir")

    assert len(proposals) == 10
    assert (
        proposals[KNOWN_PROPOSAL_ID].title
        == "Spin Dynamics in Kagome Quantum Spin Liquids"
    )
    assert proposals[KNOWN_PROPOSAL_ID].id == KNOWN_PROPOSAL_ID
    assert proposals[KNOWN_PROPOSAL_ID].proposer == User(
        firstname="Jekabs_Science",
        lastname="KIarklins_User",
        fed_id="jekabs_sciencekiarklins_user",
        organisation="",
    )
    assert proposals[KNOWN_PROPOSAL_ID].users == []


def test_ignore_instrument_name_case():
    with mock.patch("requests.get", side_effect=_url_based_get):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposals = system.get_proposals_for_instrument("yMiR")

    assert len(proposals) == 10


def test_unrecognised_instrument_raises():
    with mock.patch("requests.get", side_effect=_url_based_get):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})

        with pytest.raises(UnknownInstrumentException):
            system.get_proposals_for_instrument("NOT AN INSTRUMENT")


def test_get_proposal_by_id():
    single_proposal = [
        p for p in get_ymir_example_data() if p["proposalId"] == KNOWN_PROPOSAL_ID
    ]
    single_sample = [
        s for s in get_sample_example_data() if s["proposalId"] == KNOWN_PROPOSAL_ID
    ]

    def _get_by_id(url, **kwargs):
        if "/api/v3/proposals" in url:
            return _make_mock_response(single_proposal)
        elif "/api/v3/samples" in url:
            return _make_mock_response(single_sample)
        raise ValueError(f"Unexpected URL: {url}")

    with mock.patch("requests.get", side_effect=_get_by_id):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposal = system.get_proposal_by_id(KNOWN_PROPOSAL_ID)

    assert proposal is not None
    assert proposal.id == KNOWN_PROPOSAL_ID
    assert proposal.title == "Spin Dynamics in Kagome Quantum Spin Liquids"
    assert proposal.proposer == User(
        firstname="Jekabs_Science",
        lastname="KIarklins_User",
        fed_id="jekabs_sciencekiarklins_user",
        organisation="",
    )
    assert proposal.users == []


def test_get_proposal_by_id_returns_none_when_not_found():
    with mock.patch("requests.get", return_value=_make_mock_response([])):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposal = system.get_proposal_by_id("000000")

    assert proposal is None


def _meta(value):
    return {"value": value}


PROPOSAL_WITH_USERS = {
    "proposalId": "259600",
    "pi_firstname": "Junjie",
    "pi_lastname": "Quan",
    "title": "Sample testing 2026/06/10",
    "samples": [],
    "metadata": {
        "pi_affiliation": _meta("European Spallation Source ERIC (ESS)"),
        "number_of_co_is": _meta(3),
        "co_i_1_firstname": _meta("junjie"),
        "co_i_1_lastname": _meta("quan"),
        "co_i_1_affiliation": _meta("Other"),
        "co_i_2_firstname": _meta("Yoganandan"),
        "co_i_2_lastname": _meta("Pandiyan"),
        "co_i_2_affiliation": _meta("European Spallation Source ERIC (ESS)"),
        "co_i_3_firstname": _meta("Jekabs"),
        "co_i_3_lastname": _meta("Karklins"),
        "co_i_3_affiliation": _meta("Other"),
    },
}


def test_extracts_co_investigators_as_users():
    def _get_by_id(url, **kwargs):
        if "/api/v3/proposals" in url:
            return _make_mock_response([PROPOSAL_WITH_USERS])
        elif "/api/v3/samples" in url:
            return _make_mock_response([])
        raise ValueError(f"Unexpected URL: {url}")

    with mock.patch("requests.get", side_effect=_get_by_id):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposal = system.get_proposal_by_id("259600")

    assert proposal.users == [
        User(
            firstname="junjie",
            lastname="quan",
            fed_id="junjiequan",
            organisation="Other",
        ),
        User(
            firstname="Yoganandan",
            lastname="Pandiyan",
            fed_id="yoganandanpandiyan",
            organisation="European Spallation Source ERIC (ESS)",
        ),
        User(
            firstname="Jekabs",
            lastname="Karklins",
            fed_id="jekabskarklins",
            organisation="Other",
        ),
    ]


def test_populates_proposer_organisation_from_metadata():
    def _get_by_id(url, **kwargs):
        if "/api/v3/proposals" in url:
            return _make_mock_response([PROPOSAL_WITH_USERS])
        elif "/api/v3/samples" in url:
            return _make_mock_response([])
        raise ValueError(f"Unexpected URL: {url}")

    with mock.patch("requests.get", side_effect=_get_by_id):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposal = system.get_proposal_by_id("259600")

    assert proposal.proposer == User(
        firstname="Junjie",
        lastname="Quan",
        fed_id="junjiequan",
        organisation="European Spallation Source ERIC (ESS)",
    )
