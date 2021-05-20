import os
from tempfile import TemporaryDirectory

import pytest

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.cache import Cache
from yuos_query.exceptions import ExportCacheException, ImportCacheException


def test_exporting_data_to_json_from_cache():
    with TemporaryDirectory() as directory:
        cache = Cache("YMIR", os.path.join(directory, "test_filename.json"))
        cache.update(VALID_PROPOSAL_DATA)

        cache.export_to_json()
        cache.clear_cache()
        cache.import_from_json()

        assert cache.proposals["471120"].id == VALID_PROPOSAL_DATA["471120"].id


def test_importing_proposals_from_file_if_does_not_exist():
    with TemporaryDirectory() as directory:
        cache = Cache("YMIR", os.path.join(directory, "test_filename.json"))
        cache.update(VALID_PROPOSAL_DATA)

        with pytest.raises(ImportCacheException):
            cache.import_from_json()


def test_importing_proposals_from_file_with_non_json_data():
    filename = "test_filename.json"
    with TemporaryDirectory() as directory:
        cache = Cache("YMIR", os.path.join(directory, filename))
        cache.update(VALID_PROPOSAL_DATA)

        with open(os.path.join(directory, filename), "w") as file:
            file.write(":: IRRELEVANT DATA ::")

        with pytest.raises(ImportCacheException):
            cache.import_from_json()


def test_exporting_data_from_cache_with_invalid_data():
    cache = Cache("YMIR", "test_filename.json")
    CANNOT_BE_SERIALIZED = type

    cache.update(CANNOT_BE_SERIALIZED)

    with pytest.raises(ExportCacheException):
        cache.export_to_json()
