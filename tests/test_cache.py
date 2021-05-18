import os
from tempfile import TemporaryDirectory

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.cache import Cache
from yuos_query.utils import (
    deserialise_proposals_from_json,
    serialise_proposals_to_json,
)


def test_exporting_data_to_json_from_cache():
    cache = Cache("YMIR")
    filename = "test_filename.json"

    with TemporaryDirectory() as directory:
        filepath = os.path.join(directory, filename)
        cache.export_to_json(filepath)
        assert os.path.exists(filepath)


def test_converting_proposals_to_json():
    proposal_json = serialise_proposals_to_json(VALID_PROPOSAL_DATA)
    proposals = deserialise_proposals_from_json(proposal_json)
    assert proposals["471120"].id == VALID_PROPOSAL_DATA["471120"].id
    assert proposals["471120"].title == VALID_PROPOSAL_DATA["471120"].title
    assert proposals["471120"].proposer == VALID_PROPOSAL_DATA["471120"].proposer
    assert proposals["471120"].users == VALID_PROPOSAL_DATA["471120"].users
    assert proposals["471120"].db_id == VALID_PROPOSAL_DATA["471120"].db_id

    assert (
        proposals["471120"].samples[0].name
        == VALID_PROPOSAL_DATA["471120"].samples[0].name
    )
    assert (
        proposals["471120"].samples[0].formula
        == VALID_PROPOSAL_DATA["471120"].samples[0].formula
    )
    assert (
        proposals["471120"].samples[0].number
        == VALID_PROPOSAL_DATA["471120"].samples[0].number
    )
    assert (
        proposals["471120"].samples[0].mass_or_volume
        == VALID_PROPOSAL_DATA["471120"].samples[0].mass_or_volume
    )
    assert (
        proposals["471120"].samples[0].density
        == VALID_PROPOSAL_DATA["471120"].samples[0].density
    )
