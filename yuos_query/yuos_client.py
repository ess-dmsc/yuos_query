from typing import Optional

from gql.transport.exceptions import TransportServerError
from requests.exceptions import ConnectionError

from yuos_query.data_classes import ProposalInfo
from yuos_query.data_extractors import (
    extract_proposer,
    extract_relevant_sample_info,
    extract_users,
)
from yuos_query.exceptions import (
    BaseYuosException,
    ConnectionException,
    InvalidIdException,
)
from yuos_query.proposal_system import ProposalSystem


class YuosClient:
    def __init__(self, url, token, instrument, implementation=None):
        self.url = url
        self.token = token
        self.instrument = instrument
        self.implementation = implementation if implementation else ProposalSystem()
        self.instrument_list = {}
        self.cached_proposals = {}
        self.refresh_cache(instrument)

    def _get_instruments(self):
        data = self.implementation.get_instrument_data(self.token, self.url)
        return {inst["id"]: inst["shortCode"].lower() for inst in data}

    def proposal_by_id(self, proposal_id: str) -> Optional[ProposalInfo]:
        """
        Find the proposal.

        :param proposal_id: proposal ID
        :return: the proposal information or None if not found
        """
        converted_id = self._validate_proposal_id(proposal_id)
        return self.cached_proposals.get(converted_id)

    def _find_proposal(self, converted_id, data):
        for proposal in data:
            # In the proposal system the proposal ID is called the shortCode
            if "shortCode" in proposal and proposal["shortCode"] == converted_id:
                users = extract_users(proposal)
                proposer = extract_proposer(proposal)
                return ProposalInfo(
                    converted_id, proposal["title"], proposer, users, proposal["id"]
                )
        return None

    def _validate_proposal_id(self, proposal_id: str) -> str:
        # Does proposal_id conform to the expected pattern?
        try:
            # Currently just needs to be a numeric string
            return str(int(proposal_id))
        except Exception as error:
            raise InvalidIdException(error) from error

    def _get_instrument_id_from_name(self, instrument_name):
        # Reverse look-up
        for n, v in self.instrument_list.items():
            if v.lower() == instrument_name.lower():
                return n
        raise InvalidIdException(f"instrument {instrument_name} not recognised")

    def _get_proposal_data(self, instrument_id):
        data = self.implementation.get_proposals_for_instrument(
            self.token, self.url, instrument_id
        )
        return data

    def get_all_proposals_for_instrument(self, instrument_name):
        inst_id = self._get_instrument_id_from_name(instrument_name)
        response = self.implementation.get_proposals_including_samples_for_instrument(
            self.token, self.url, inst_id
        )
        proposals = {}
        for proposal in response:
            users = extract_users(proposal)
            proposer = extract_proposer(proposal)
            title = proposal["title"]
            id = proposal["id"]
            prop_id = proposal["shortCode"]
            samples = extract_relevant_sample_info(proposal["samples"])

            proposals[prop_id] = ProposalInfo(
                prop_id, title, proposer, users, id, samples
            )

        return proposals

    def refresh_cache(self, instrument):
        try:
            if not self.instrument_list:
                self.instrument_list = self._get_instruments()

            self.cached_proposals = self.get_all_proposals_for_instrument(instrument)
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except ConnectionError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except BaseYuosException:
            raise
        except Exception as error:
            raise BaseYuosException(error) from error
