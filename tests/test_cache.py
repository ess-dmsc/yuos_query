import os
from tempfile import TemporaryDirectory

import pytest

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.cache import Cache
from yuos_query.exceptions import ExportCacheException, ImportCacheException


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


def test_importing_proposals_from_file_if_does_not_exist():
    cache = Cache("YMIR")
    cache.proposals = VALID_PROPOSAL_DATA

    filename = "test_filename.json"

    with TemporaryDirectory() as directory:
        filepath = os.path.join(directory, filename)
        with pytest.raises(ImportCacheException):
            cache.import_from_json(filepath)


def test_importing_proposals_from_file_with_non_json_data():
    cache = Cache("YMIR")
    cache.proposals = VALID_PROPOSAL_DATA

    filename = "test_filename.json"

    with TemporaryDirectory() as directory:
        filepath = os.path.join(directory, filename)
        with open(filepath, "w") as file:
            file.write(":: IRRELEVANT DATA ::")

        with pytest.raises(ImportCacheException):
            cache.import_from_json(filepath)


def test_exporting_data_from_cache_with_invalid_data():
    cache = Cache("YMIR")
    CANNOT_BE_SERIALIZED = type

    cache.proposals = CANNOT_BE_SERIALIZED

    with pytest.raises(ExportCacheException):
        cache.export_to_json("test_filename.json")
