import os
from unittest import mock

import pytest
from requests.exceptions import ConnectionError

from yuos_query.proposal_system import (
    ConnectionException,
    InvalidCredentialsException,
    InvalidIdException,
    ProposalSystemClient,
    _ProposalSystemWrapper,
)

# These tests can be run against the real system and should do the same as the mocked version.
# Just need to set the environment variables "USER" and "PASSWORD"
USE_REAL_SYSTEM = True if "TEST_USER" in os.environ else False

if USE_REAL_SYSTEM:
    URL = "https://useroffice-test.esss.lu.se/graphql"
    TEST_USER = os.environ["TEST_USER"]
    TEST_PASSWORD = os.environ["TEST_PASSWORD"]
else:
    URL = "https://something.com"
    TEST_USER = "account@ess.eu"
    TEST_PASSWORD = "apassword"

# Copied from a real server
VALID_INSTRUMENT_LIST = [
    {"id": 4, "shortCode": "YMIR", "description": "Our test beamline", "name": "YMIR"},
    {
        "id": 3,
        "shortCode": "asztalos",
        "description": "test\n",
        "name": "Asztalos Instrument",
    },
    {
        "id": 2,
        "shortCode": "s adasd",
        "description": "d asdas",
        "name": "Test instrument 2",
    },
    {
        "id": 1,
        "shortCode": "sd ad",
        "description": "d asdasd",
        "name": "Test instrument 1",
    },
]

UNKNOWN_INSTRUMENT_ID_RESPONSE = []
VALID_PROPOSAL_ID = 169

# Copied from a real server
VALID_RESPONSE_DATA = [
    {
        "id": 169,
        "title": "The magnetic field dependence of the director state in the quantum spin hyperkagome compound Yb3Ga5O12",
        "users": [
            {"firstname": "jonathan ", "lastname": "Taylor"},
            {"firstname": "Johan", "lastname": "Andersson"},
        ],
        "proposer": {"firstname": "Fredrik-user", "lastname": "Bolmsten"},
    }
]


def generate_standard_mock():
    mocked_impl = mock.create_autospec(_ProposalSystemWrapper)
    mocked_impl.get_token.return_value = {"login": {"token": "eyJhbG"}}
    mocked_impl.get_instrument_data.return_value = VALID_INSTRUMENT_LIST
    mocked_impl.get_proposal_for_instrument.return_value = VALID_RESPONSE_DATA
    return mocked_impl


def create_client(url, user, password, mocked_impl):
    if USE_REAL_SYSTEM:
        # Actually test against the real system
        return ProposalSystemClient(url, user, password)
    else:
        # Use the mock
        return ProposalSystemClient(url, user, password, mocked_impl)


def test_querying_for_proposal_by_id_with_invalid_url_raise_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_token.side_effect = ConnectionError("oops")

    proposal_system = create_client(
        "https://does.not.exist",
        TEST_USER,
        TEST_PASSWORD,
        mocked_impl,
    )

    with pytest.raises(ConnectionException):
        proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)


def test_querying_for_proposal_by_id_with_invalid_password_raise_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_token.side_effect = InvalidCredentialsException("oops")

    proposal_system = create_client(
        URL,
        TEST_USER,
        "wrong_password",
        mocked_impl,
    )

    with pytest.raises(InvalidCredentialsException):
        proposal_system.proposal_by_id("loki", VALID_PROPOSAL_ID)


def test_querying_for_proposal_by_id_with_invalid_user_raise_correct_exception_type():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_token.side_effect = InvalidCredentialsException("oops")

    proposal_system = create_client(
        URL,
        "wrong_user",
        TEST_PASSWORD,
        mocked_impl,
    )

    with pytest.raises(InvalidCredentialsException):
        proposal_system.proposal_by_id("loki", VALID_PROPOSAL_ID)


def test_querying_for_proposal_by_id_gets_correct_proposal():
    mocked_impl = generate_standard_mock()

    proposal_system = create_client(URL, TEST_USER, TEST_PASSWORD, mocked_impl)
    results = proposal_system.proposal_by_id("YMIR", VALID_PROPOSAL_ID)

    assert results.id == VALID_PROPOSAL_ID
    assert results.title.startswith("The magnetic field dependence")
    assert results.proposer == ("Fredrik-user", "Bolmsten")
    assert len(results.users) == 2
    assert ("Johan", "Andersson") in results.users


def test_querying_for_proposal_by_id_with_id_that_does_not_conform_to_pattern_raises():
    mocked_impl = generate_standard_mock()

    proposal_system = create_client(URL, TEST_USER, TEST_PASSWORD, mocked_impl)

    with pytest.raises(InvalidIdException):
        proposal_system.proposal_by_id("loki", "abc")


def test_querying_for_proposal_id_with_unknown_instrument_raises_correct_exception_type():
    mocked_impl = generate_standard_mock()

    proposal_system = create_client(URL, TEST_USER, TEST_PASSWORD, mocked_impl)

    with pytest.raises(InvalidIdException):
        proposal_system.proposal_by_id(
            "instrument that does not exist", VALID_PROPOSAL_ID
        )


def test_querying_for_unknown_proposal_id_returns_nothing():
    mocked_impl = generate_standard_mock()
    mocked_impl.get_proposal_for_instrument.return_value = (
        UNKNOWN_INSTRUMENT_ID_RESPONSE
    )

    proposal_system = create_client(
        URL,
        TEST_USER,
        TEST_PASSWORD,
        mocked_impl,
    )

    assert proposal_system.proposal_by_id("YMIR", 1234567) is None
