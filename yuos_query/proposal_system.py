from typing import Optional

from gql import Client, gql
from gql.transport.exceptions import TransportServerError
from gql.transport.requests import RequestsHTTPTransport
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


class YuosClient:
    def __init__(self, url, token, implementation=None, instrument="YMIR"):
        self.url = url
        self.token = token
        self.implementation = (
            implementation if implementation else _ProposalSystemWrapper()
        )
        self.instrument_list = {}
        self.cached_proposals = []
        self.refresh_cache(instrument)

    def _get_instruments(self):
        data = self.implementation.get_instrument_data(self.token, self.url)
        return {inst["id"]: inst["shortCode"].lower() for inst in data}

    def proposal_by_id(
        self, instrument_name: str, proposal_id: str
    ) -> Optional[ProposalInfo]:
        """
        Query the proposal system based on the instrument and proposal ID.

        :param instrument_name: instrument name
        :param proposal_id: proposal ID
        :return: the proposal information or None if not found
        """
        try:
            # if not self.instrument_list:
            #     self.instrument_list = self._get_instruments()

            converted_id = self._validate_proposal_id(proposal_id)
            inst_id = self._get_instrument_id_from_name(instrument_name)
            data = self._get_proposal_data(inst_id)
            return self._find_proposal(converted_id, data)
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except ConnectionError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except BaseYuosException:
            raise
        except Exception as error:
            raise BaseYuosException(error) from error

    def samples_by_id(self, db_id):
        """
        Get the sample associated with the supplied database ID.

        The sample data is associated to the proposal ID by the internal database ID,
        so we have to use that. That is retrieved during the proposal query.

        :param db_id: the database ID
        :return: list of SampleInfo
        """
        try:
            data = self.implementation.get_sample_details_by_proposal_id(
                self.token, self.url, db_id
            )
            return extract_relevant_sample_info(data)
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except ConnectionError as error:
            raise ConnectionException(f"connection issue: {error}") from error
        except BaseYuosException:
            raise
        except Exception as error:
            raise BaseYuosException(error) from error

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
            # Currently just needs to be a string
            return str(proposal_id)
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
        if not self.instrument_list:
            self.instrument_list = self._get_instruments()

        inst_id = self._get_instrument_id_from_name(instrument_name)
        data = self.implementation.get_proposals_including_samples_for_instrument(
            self.token, self.url, inst_id
        )
        proposals = {}
        for d in data:

            users = extract_users(d)
            proposer = extract_proposer(d)
            title = d["title"]
            id = d["id"]
            prop_id = d["shortCode"]
            samples = extract_relevant_sample_info(d["samples"])

            proposals[prop_id] = {
                "users": users,
                "proposer": proposer,
                "title": title,
                "id": id,
                "samples": samples,
            }

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


class _ProposalSystemWrapper:
    """
    Don't use this directly, instead use the ProposalSystem class.
    """

    def execute_query(self, token, url, query_json):
        """
        Function for making a query on the proposal system.

        :param token: the authorisation token
        :param url: the proposal system URL
        :param query_json: the query to make
        :return: the JSON response
        """
        token = f"Bearer {token}"
        transport = RequestsHTTPTransport(
            url=url,
            verify=True,
            headers={"Authorization": token},
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        with client as session:
            query = gql(query_json)
            return session.execute(query)

    def get_instrument_data(self, token, url):
        json_data = self.execute_query(
            token,
            url,
            """
            {
                instruments {
                    instruments {
                        id
                        shortCode
                        description
                        name
                    }
                }
            }
            """,
        )
        return json_data["instruments"]["instruments"]

    def get_proposals_for_instrument(self, token, url, instrument_id):
        json_data = self.execute_query(
            token,
            url,
            """
            {
                proposals(filter: {instrumentId: $INST$}){
                    totalCount
                    proposals{
                        shortCode
                        title
                        id
                        users {
                            firstname
                            lastname
                        }
                        proposer {
                            firstname
                            lastname
                        }
                    }
                }
            }
            """.replace(
                "$INST$", str(instrument_id)
            ),
        )
        return json_data["proposals"]["proposals"]

    def get_sample_details_by_proposal_id(self, token, url, db_id):
        json_data = self.execute_query(
            token,
            url,
            """
            {
                samples(filter: {proposalId: $DBID$})  {
                    proposalId
                    title
                    questionary{
                      steps{
                        fields{
                          value
                          dependencies{
                            dependencyNaturalKey
                            questionId
                          }
                          question{
                            question
                            naturalKey
                          }
                        }
                      }
                    }
                  }
            }
            """.replace(
                "$DBID$", str(db_id)
            ),
        )
        return json_data["samples"]

    def get_proposals_including_samples_for_instrument(self, token, url, instrument_id):
        json_data = self.execute_query(
            token,
            url,
            """
            {
                proposals(filter: {instrumentId: $INST$}){
                    totalCount
                    proposals{
                        shortCode
                        title
                        id
                        users {
                            firstname
                            lastname
                        }
                        proposer {
                            firstname
                            lastname
                        }
                        samples {
                            proposalId
                            title
                            id
                            questionary {
                                steps {
                                    fields {
                                        value
                                        dependencies {
                                            dependencyNaturalKey
                                            questionId
                                        }
                                        question {
                                            question
                                            naturalKey
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """.replace(
                "$INST$", str(instrument_id)
            ),
        )
        return json_data["proposals"]["proposals"]
