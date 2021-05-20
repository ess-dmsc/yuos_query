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
        with open(filename, "w") as file:
            file.write(serialise_proposals_to_json(self.proposals))

    def import_from_json(self, filename):
        with open(filename, "r") as file:
            self.proposals = deserialise_proposals_from_json(file.read())
