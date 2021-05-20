from json.decoder import JSONDecodeError

from yuos_query.exceptions import ExportCacheException, ImportCacheException
from yuos_query.utils import (
    deserialise_proposals_from_json,
    serialise_proposals_to_json,
)


class Cache:
    def __init__(self, instrument):
        self.instrument = instrument
        self.proposals = {}

    def update(self, proposals):
        self.proposals = proposals

    def export_to_json(self, filename):
        try:
            with open(filename, "w") as file:
                file.write(serialise_proposals_to_json(self.proposals))
        except Exception as ex:
            raise ExportCacheException(f"Export exception: {ex}")

    def import_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                self.proposals = deserialise_proposals_from_json(file.read())
        except FileNotFoundError as ex:
            raise ImportCacheException(f"File not found: {filename}") from ex
        except JSONDecodeError as ex:
            raise ImportCacheException(
                f"Could not deserialise data from file: {filename}"
            ) from ex
        except Exception as ex:
            raise ImportCacheException(f"Import exception: {ex}") from ex
