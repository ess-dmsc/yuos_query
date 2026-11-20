import json

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.data_classes import User
from yuos_query.utils import (
    deserialise_proposals_from_json,
    serialise_proposals_to_json,
)


def test_converting_proposals_to_json_and_back():
    proposal_json = serialise_proposals_to_json(VALID_PROPOSAL_DATA)
    proposals = deserialise_proposals_from_json(proposal_json)
    assert proposals["471120"].id == VALID_PROPOSAL_DATA["471120"].id
    assert proposals["471120"].title == VALID_PROPOSAL_DATA["471120"].title
    assert proposals["471120"].proposer == VALID_PROPOSAL_DATA["471120"].proposer
    assert proposals["471120"].users == VALID_PROPOSAL_DATA["471120"].users
    assert proposals["471120"].db_id == VALID_PROPOSAL_DATA["471120"].db_id
    assert (
        proposals["471120"].local_contacts
        == VALID_PROPOSAL_DATA["471120"].local_contacts
    )

    assert (
        proposals["471120"].samples[0].id == VALID_PROPOSAL_DATA["471120"].samples[0].id
    )
    assert (
        proposals["471120"].samples[0].name
        == VALID_PROPOSAL_DATA["471120"].samples[0].name
    )


def test_reading_cache_without_email_gives_empty_email():
    cache_without_email = json.dumps(
        {
            "123456": {
                "id": "123456",
                "title": "A test proposal",
                "proposer": ["John", "Doe", "johndoe", "ESS"],
                "users": [["Jane", "Doe", "janedoe", "ESS"]],
                "db_id": 0,
                "samples": [],
            }
        }
    )

    proposals = deserialise_proposals_from_json(cache_without_email)

    assert proposals["123456"].proposer == User("John", "Doe", "johndoe", "ESS", "")
    assert proposals["123456"].users == [User("Jane", "Doe", "janedoe", "ESS", "")]


def test_reading_cache_without_local_contacts_gives_empty_list():
    cache_without_local_contacts = json.dumps(
        {
            "123456": {
                "id": "123456",
                "title": "A test proposal",
                "proposer": ["John", "Doe", "johndoe", "ESS", "john@ess.eu"],
                "users": [],
                "db_id": 0,
                "samples": [],
            }
        }
    )

    proposals = deserialise_proposals_from_json(cache_without_local_contacts)

    assert proposals["123456"].local_contacts == []
