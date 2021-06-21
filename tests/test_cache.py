import os
from tempfile import TemporaryDirectory

import pytest

from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.data_classes import ProposalInfo
from yuos_query.exceptions import ExportCacheException, ImportCacheException
from yuos_query.file_cache import FileCache


def test_exporting_and_importing_data_to_and_from_cache():
    with TemporaryDirectory() as directory:
        cache = FileCache(os.path.join(directory, "test_filename.json"))
        cache.update(VALID_PROPOSAL_DATA)

        cache.export_to_file()
        cache.clear_cache()
        cache.import_from_file()

        assert cache.proposals["471120"].id == VALID_PROPOSAL_DATA["471120"].id
        assert len(cache.proposals_by_fed_id["jonathantaylor"]) == 2


def test_importing_proposals_from_file_if_does_not_exist():
    with TemporaryDirectory() as directory:
        cache = FileCache(os.path.join(directory, "test_filename.json"))
        cache.update(VALID_PROPOSAL_DATA)

        with pytest.raises(ImportCacheException):
            cache.import_from_file()


def test_importing_proposals_from_file_with_non_json_data():
    filename = "test_filename.json"
    with TemporaryDirectory() as directory:
        cache = FileCache(os.path.join(directory, filename))
        cache.update(VALID_PROPOSAL_DATA)

        with open(os.path.join(directory, filename), "w") as file:
            file.write(":: IRRELEVANT DATA ::")

        with pytest.raises(ImportCacheException):
            cache.import_from_file()


def test_exporting_data_from_cache_with_invalid_data():
    filename = "test_filename.json"
    with TemporaryDirectory() as directory:
        cache = FileCache(filename)
        # Put something in ProposalInfo that cannot be serialised
        CANNOT_BE_SERIALIZED = {
            "a": ProposalInfo(
                type, ":: title ::", proposer=None, users=[], db_id=123, samples=[]
            )
        }

        cache.update(CANNOT_BE_SERIALIZED)

        with pytest.raises(ExportCacheException):
            cache.export_to_file()

        # Should not leave a file behind
        assert not os.path.exists(os.path.join(directory, filename))
