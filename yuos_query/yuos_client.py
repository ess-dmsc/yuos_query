from typing import List, Optional

from yuos_query.data_classes import ProposalInfo
from yuos_query.exceptions import (
    DataUnavailableException,
    ExportCacheException,
    ImportCacheException,
    InvalidIdException,
    ServerException,
)
from yuos_query.file_cache import FileCache
from yuos_query.proposal_system import ProposalRequester


class YuosClient:
    def __init__(
        self,
        url,
        token,
        instrument,
        cache_filepath,
        update_cache=True,
        cache=None,
        system=None,
    ):
        self.instrument = instrument
        self.cache = cache if cache else FileCache(cache_filepath)
        self.system = system if system else ProposalRequester(url, token)

        if update_cache:
            self.update_cache()

    def proposal_by_id(self, proposal_id: str) -> Optional[ProposalInfo]:
        """
        Find the proposal.

        :param proposal_id: proposal ID
        :return: the proposal information or None if not found
        """
        if not self._does_proposal_id_conform(proposal_id):
            raise InvalidIdException()
        return self.cache.proposals.get(proposal_id)

    def proposals_for_user(self, fed_id: str) -> List[ProposalInfo]:
        if fed_id not in self.cache.proposals_by_fed_id:
            return []
        return self.cache.proposals_by_fed_id[fed_id]

    def _does_proposal_id_conform(self, proposal_id: str) -> bool:
        # Does proposal_id conform to the expected pattern?
        return all(c.isdigit() for c in proposal_id)

    def update_cache(self):
        try:
            proposals = self.system.get_proposals_for_instrument(self.instrument)
            self.cache.update(proposals)
            self.cache.export_to_file()
        except ServerException:
            try:
                if self.cache.is_empty():
                    self.cache.import_from_file()
            except ImportCacheException as error:
                raise DataUnavailableException(
                    "Proposal system and cache unavailable"
                ) from error
        except ExportCacheException:
            raise
