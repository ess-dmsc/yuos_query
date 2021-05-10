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


class Cache:
    def __init__(self, token, url, instrument, implementation=None):
        self.token = token
        self.url = url
        self.instrument = instrument
        self.implementation = implementation if implementation else ProposalSystem()
        self.instrument_list = {}
        self.cached_proposals = {}

    def _get_instruments(self):
        data = self.implementation.get_instrument_data(self.token, self.url)
        return {inst["id"]: inst["shortCode"].lower() for inst in data}

    def _get_instrument_id_from_name(self, instrument_name):
        # Reverse look-up
        for n, v in self.instrument_list.items():
            if v.lower() == instrument_name.lower():
                return n
        raise InvalidIdException(f"instrument {instrument_name} not recognised")

    def refresh(self):
        try:
            self.instrument_list = self._get_instruments()

            self.cached_proposals = self.get_all_proposals_for_instrument(
                self.instrument
            )
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except ConnectionError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except BaseYuosException:
            raise
        except Exception as error:
            raise BaseYuosException(error) from error

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
