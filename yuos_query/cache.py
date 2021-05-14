class Cache:
    def __init__(self, instrument):
        self.instrument = instrument
        self.proposals = {}

    def update(self, proposals):
        self.proposals = proposals
