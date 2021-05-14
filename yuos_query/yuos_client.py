from typing import Optional

from yuos_query.cache import Cache
from yuos_query.data_classes import ProposalInfo
from yuos_query.exceptions import InvalidIdException
from yuos_query.proposal_system import ProposalSystem


class YuosClient:
    def __init__(self, url, token, instrument, cache=Cache(), system=None):
        self.url = url
        self.token = token
        self.instrument = instrument
        self.cache = cache
        self.system = system if system else ProposalSystem(url, token)

        self.update_cache()

    def proposal_by_id(self, proposal_id: str) -> Optional[ProposalInfo]:
        """
        Find the proposal.

        :param proposal_id: proposal ID
        :return: the proposal information or None if not found
        """
        converted_id = self._validate_proposal_id(proposal_id)
        return self.cache.proposals.get(converted_id)

    def _validate_proposal_id(self, proposal_id: str) -> str:
        # Does proposal_id conform to the expected pattern?
        try:
            # Currently just needs to be a numeric string
            return str(int(proposal_id))
        except Exception as error:
            raise InvalidIdException(error) from error

    def update_cache(self):
        inst_data = self.system.get_instrument_data()
        proposals = self.system.get_proposals_by_instrument_id(
            inst_data[self.instrument.lower()]
        )
        self.cache.update(inst_data, proposals)
