from typing import Optional

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
    def __init__(self, url, token, instrument, cache_filepath, cache=None, system=None):
        self.url = url
        self.token = token
        self.instrument = instrument
        self.cache = cache if cache else FileCache(instrument, cache_filepath)
        self.system = system if system else ProposalRequester(url, token)

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
        try:
            proposals = self.system.get_proposals_for_instrument(self.instrument)
            self.cache.update(proposals)
            self.cache.export_to_json()
        except ServerException:
            try:
                if self.cache.is_empty():
                    self.cache.import_from_json()
            except ImportCacheException as ex:
                raise DataUnavailableException(
                    "Proposal system and Cache unavailable"
                ) from ex
        except ExportCacheException:
            raise
