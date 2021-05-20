import os
from tempfile import TemporaryDirectory

import pytest

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.cache import Cache
from yuos_query.exceptions import ExportCacheException, ImportCacheException


def test_exporting_data_to_json_from_cache():
    with TemporaryDirectory() as directory:
        cache = Cache("YMIR", directory)
        cache.update(VALID_PROPOSAL_DATA)

        filename = "test_filename.json"
        cache.export_to_json(filename)

        cache.clear_cache()
        cache.import_from_json(filename)

        assert cache.proposals["471120"].id == VALID_PROPOSAL_DATA["471120"].id


def test_importing_proposals_from_file_if_does_not_exist():
    with TemporaryDirectory() as directory:
        cache = Cache("YMIR", directory)
        cache.update(VALID_PROPOSAL_DATA)

        filename = "test_filename.json"
        with pytest.raises(ImportCacheException):
            cache.import_from_json(filename)


def test_importing_proposals_from_file_with_non_json_data():
    with TemporaryDirectory() as directory:
        cache = Cache("YMIR", directory)
        cache.update(VALID_PROPOSAL_DATA)

        filename = "test_filename.json"
        with open(os.path.join(directory, filename), "w") as file:
            file.write(":: IRRELEVANT DATA ::")

        with pytest.raises(ImportCacheException):
            cache.import_from_json(filename)


def test_exporting_data_from_cache_with_invalid_data():
    cache = Cache("YMIR", ":: some directory ::")
    CANNOT_BE_SERIALIZED = type

    cache.update(CANNOT_BE_SERIALIZED)

    with pytest.raises(ExportCacheException):
        cache.export_to_json("test_filename.json")
