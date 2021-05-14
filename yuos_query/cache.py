class Cache:
    def __init__(self):
        self.instrument_ids = {}
        self.proposals = {}

    def update(self, inst_data, proposals):
        self.instrument_ids = inst_data
        self.proposals = proposals
