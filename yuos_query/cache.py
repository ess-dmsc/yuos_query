class Cache:
    def __init__(self, instrument):
        self.instrument = instrument
        self.proposals = {}

    def update(self, proposals):
        self.proposals = proposals

    def export_to_json(self, filename):
        with open(filename, "w") as f:
            f.write("LOL")
