import os
from copy import deepcopy
from json.decoder import JSONDecodeError

from yuos_query.exceptions import ExportCacheException, ImportCacheException
from yuos_query.utils import (
    deserialise_proposals_from_json,
    serialise_proposals_to_json,
)


class Cache:
    def __init__(self, instrument, cache_directory):
        self.instrument = instrument
        self.cache_directory = cache_directory
        self.proposals = {}

    def update(self, proposals):
        self.proposals = deepcopy(proposals)

    def export_to_json(self, filename):
        filepath = os.path.join(self.cache_directory, filename)
        try:
            with open(filepath, "w") as file:
                file.write(serialise_proposals_to_json(self.proposals))
        except Exception as ex:
            raise ExportCacheException(f"Export exception: {ex}")

    def import_from_json(self, filename):
        filepath = os.path.join(self.cache_directory, filename)
        try:
            with open(filepath, "r") as file:
                self.proposals = deserialise_proposals_from_json(file.read())
        except FileNotFoundError as ex:
            raise ImportCacheException(f"File not found: {filepath}") from ex
        except JSONDecodeError as ex:
            raise ImportCacheException(
                f"Could not deserialise data from file: {filepath}"
            ) from ex
        except Exception as ex:
            raise ImportCacheException(f"Import exception: {ex}") from ex

    def clear_cache(self):
        self.proposals = {}
