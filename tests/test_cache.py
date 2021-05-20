import os
from tempfile import TemporaryDirectory

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.cache import Cache


def test_exporting_data_to_json_from_cache():
    cache = Cache("YMIR")
    cache.proposals = VALID_PROPOSAL_DATA

    filename = "test_filename.json"

    with TemporaryDirectory() as directory:
        filepath = os.path.join(directory, filename)
        cache.export_to_json(filepath)
        assert os.path.exists(filepath)
        # Clear the cache
        cache.proposals = {}
        cache.import_from_json(filepath)

        assert cache.proposals["471120"].id == VALID_PROPOSAL_DATA["471120"].id
