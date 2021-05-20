from copy import deepcopy
from json.decoder import JSONDecodeError

from yuos_query.exceptions import ExportCacheException, ImportCacheException
from yuos_query.utils import (
    deserialise_proposals_from_json,
    serialise_proposals_to_json,
)


class FileCache:
    def __init__(self, instrument, cache_filepath):
        self.instrument = instrument
        self.cache_filepath = cache_filepath
        self.proposals = {}

    def update(self, proposals):
        self.proposals = deepcopy(proposals)

    def export_to_json(self):
        try:
            with open(self.cache_filepath, "w") as file:
                file.write(serialise_proposals_to_json(self.proposals))
        except Exception as ex:
            raise ExportCacheException(f"Export exception: {ex}")

    def import_from_json(self):
        try:
            with open(self.cache_filepath, "r") as file:
                self.proposals = deserialise_proposals_from_json(file.read())
        except FileNotFoundError as ex:
            raise ImportCacheException(f"File not found: {self.cache_filepath}") from ex
        except JSONDecodeError as ex:
            raise ImportCacheException(
                f"Could not deserialise data from file: {self.cache_filepath}"
            ) from ex
        except Exception as ex:
            raise ImportCacheException(f"Import exception: {ex}") from ex

    def clear_cache(self):
        self.proposals = {}

    def is_empty(self):
        return len(self.proposals) == 0