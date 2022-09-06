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


class YuosServer:
    def __init__(self, instrument, cache, requester):
        self.instrument = instrument
        self.cache = cache
        self.system = requester

    @classmethod
    def create(cls, url, token, instrument, cache_filepath, proxies):
        return cls(
            instrument,
            FileCache(cache_filepath),
            ProposalRequester(url, token, proxies),
        )

    def update_cache(self):
        try:
            proposals = self.system.get_proposals_for_instrument(self.instrument)
            self.cache.update(proposals)
            self.cache.export_to_file()
        except ServerException as error:
            raise DataUnavailableException("Proposal system unavailable") from error
        except ExportCacheException:
            raise


class YuosCacheClient:
    def __init__(self, cache):
        self.cache = cache

    @classmethod
    def create(cls, cache_filepath):
        return cls(FileCache(cache_filepath))

    def proposal_by_id(self, proposal_id: str) -> Optional[ProposalInfo]:
        """
        Find the proposal.

        :param proposal_id: proposal ID
        :return: the proposal information or None if not found
        """
        if not self._does_proposal_id_conform(proposal_id):
            raise InvalidIdException()
        return self.cache.proposals.get(proposal_id)

    def all_proposals(self):
        return self.cache.proposals

    def proposals_for_user(self, fed_id: str) -> List[ProposalInfo]:
        if fed_id not in self.cache.proposals_by_fed_id:
            return []
        return self.cache.proposals_by_fed_id[fed_id]

    def _does_proposal_id_conform(self, proposal_id: str) -> bool:
        # Does proposal_id conform to the expected pattern?
        return all(c.isdigit() for c in proposal_id)

    def update_cache(self):
        try:
            self.cache.import_from_file()
        except ImportCacheException as error:
            raise DataUnavailableException("Could not import cached data") from error
