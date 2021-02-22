from typing import List, NamedTuple, Optional, Tuple

from gql import Client, gql
from gql.transport.exceptions import TransportServerError
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import ConnectionError

from yuos_query.exceptions import (
    BaseYuosException,
    ConnectionException,
    InvalidIdException,
)

ProposalInfo = NamedTuple(
    "ProposalInfo",
    (
        ("id", str),
        ("title", str),
        ("proposer", Tuple[str, str]),
        ("users", List[Tuple[str, str]]),
    ),
)


class YuosClient:
    def __init__(self, url, token, implementation=None):
        self.url = url
        self.token = token
        self.implementation = (
            implementation if implementation else _ProposalSystemWrapper()
        )
        self.instrument_list = {}

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
            if not self.instrument_list:
                self.instrument_list = self._get_instruments()

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

    def samples_by_id(self, proposal_id):
        try:
            data = self.implementation.get_sample_details_by_proposal_id(
                self.token, self.url, proposal_id
            )
            return data
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error

    def _find_proposal(self, converted_id, data):
        for proposal in data:
            # In the proposal system the proposal ID is called the shortCode
            if "shortCode" in proposal and proposal["shortCode"] == converted_id:
                users = self.extract_users(proposal)
                proposer = self.extract_proposer(proposal)
                return ProposalInfo(converted_id, proposal["title"], proposer, users)
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
        data = self.implementation.get_proposal_for_instrument(
            self.token, self.url, instrument_id
        )
        return data

    @staticmethod
    def extract_proposer(proposal):
        if "proposer" in proposal:
            proposer = (
                proposal["proposer"].get("firstname", ""),
                proposal["proposer"].get("lastname", ""),
            )
        else:
            proposer = None
        return proposer

    @classmethod
    def extract_users(cls, proposal):
        if "users" in proposal:
            return [
                (x.get("firstname", ""), x.get("lastname", ""))
                for x in proposal["users"]
            ]
        return []

    @classmethod
    def extract_sample_info(cls, target, data):
        target = [x.lower() for x in target]
        results = []
        for sample in data:
            questions = sample["questionary"]["steps"][0]["fields"]
            result = cls._get_answers_by_question(questions, target)
            if result:
                results.append(result)
        return results

    @classmethod
    def _get_answers_by_question(cls, questions, target):
        result = {}
        for question in questions:
            # SMELL question within question?
            key_question = question["question"]["question"]
            if key_question.lower() in target:
                result[key_question.lower()] = question["value"]

        return result


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

    def get_proposal_for_instrument(self, token, url, instrument_id):
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

    def get_sample_data_by_id(self, token, url, db_id):
        json_data = self.execute_query(
            token,
            url,
            """
            {
                samples(filter: {proposalId: $DBID$})  {
                    proposalId
                    title
                }
            }
            """.replace(
                "$DBID$", str(db_id)
            ),
        )
        return json_data["samples"]

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
                          question{
                            question
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
