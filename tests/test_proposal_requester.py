from unittest import mock

import pytest
from example_data import get_ymir_example_data
from yuos_query.data_classes import User
from yuos_query.exceptions import UnknownInstrumentException
from yuos_query.proposal_system_scicat import ProposalRequester

YMIR_UUID = "ebfb7106-b885-4eda-b414-3f6fb80443e4"
DREAM_UUID = "554e7fe2-a16e-11ed-bafb-f34f3b09d136"
KNOWN_PROPOSAL_ID = "985796"

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

    assert len(proposals) == 40
    assert proposals[KNOWN_PROPOSAL_ID].title == "YMIR test proposal"
    assert proposals[KNOWN_PROPOSAL_ID].id == KNOWN_PROPOSAL_ID
    assert proposals[KNOWN_PROPOSAL_ID].proposer == User(
        firstname="Yoganandan",
        lastname="Pandiyan",
        fed_id="yoganandanpandiyan",
        organisation="",
    )
    assert proposals[KNOWN_PROPOSAL_ID].users == []


def test_ignore_instrument_name_case():
    with mock.patch("requests.get", side_effect=_url_based_get):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposals = system.get_proposals_for_instrument("yMiR")

    assert len(proposals) == 40


def test_unrecognised_instrument_raises():
    with mock.patch("requests.get", side_effect=_url_based_get):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})

        with pytest.raises(UnknownInstrumentException):
            system.get_proposals_for_instrument("NOT AN INSTRUMENT")


def test_get_proposal_by_id():
    single_proposal = [p for p in get_ymir_example_data() if p["proposalId"] == KNOWN_PROPOSAL_ID]

    def _get_by_id(url, **kwargs):
        if "/api/v3/proposals" in url:
            return _make_mock_response(single_proposal)
        elif "/api/v3/samples" in url:
            return _make_mock_response([])
        raise ValueError(f"Unexpected URL: {url}")

    with mock.patch("requests.get", side_effect=_get_by_id):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposal = system.get_proposal_by_id(KNOWN_PROPOSAL_ID)

    assert proposal is not None
    assert proposal.id == KNOWN_PROPOSAL_ID
    assert proposal.title == "YMIR test proposal"
    assert proposal.proposer == User(
        firstname="Yoganandan",
        lastname="Pandiyan",
        fed_id="yoganandanpandiyan",
        organisation="",
    )
    assert proposal.users == []


def test_get_proposal_by_id_returns_none_when_not_found():
    with mock.patch("requests.get", return_value=_make_mock_response([])):
        system = ProposalRequester("https://scicat.example.com", ":: token ::", {})
        proposal = system.get_proposal_by_id("000000")

    assert proposal is None
