from typing import List, NamedTuple, Optional, Tuple

from gql import Client, gql
from gql.transport.exceptions import TransportServerError
from gql.transport.requests import RequestsHTTPTransport
from requests.exceptions import ConnectionError

from yuos_query.exceptions import (
    BaseYuosException,
    ConnectionException,
    InvalidCredentialsException,
    InvalidIdException,
)

ProposalInfo = NamedTuple(
    "ProposalInfo",
    (
        ("id", int),
        ("title", str),
        ("proposer", Tuple[str, str]),
        ("users", List[Tuple[str, str]]),
    ),
)


class ProposalSystemClient:
    def __init__(
        self,
        url,
        user,
        password,
        implementation=None,
    ):
        self.url = url
        self.user = user
        self.password = password
        self.token = None
        self.implementation = (
            implementation if implementation else _ProposalSystemWrapper()
        )
        self.instrument_list = {}

    def _get_instruments(self):
        token = self._get_token()

        try:
            data = self.implementation.get_instrument_data(token, self.url)
            return {inst["id"]: inst["shortCode"].lower() for inst in data}
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error

    def proposal_by_id(
        self, instrument_name: str, proposal_id: str
    ) -> Optional[ProposalInfo]:
        """
        Query the proposal system based on the instrument and proposal ID.

        :param instrument_name: instrument name
        :param proposal_id: proposal ID
        :return: the proposal or None if not found
        """
        try:
            if not self.instrument_list:
                self.instrument_list = self._get_instruments()

            converted_id = self._validate_proposal_id(proposal_id)
            inst_id = self._get_instrument_id_from_name(instrument_name)
            data = self._get_proposal_data(inst_id)

            for proposal in data:
                if "id" in proposal and proposal["id"] == converted_id:
                    users = self.extract_users(proposal)
                    proposer = self.extract_proposer(proposal)
                    return ProposalInfo(
                        converted_id, proposal["title"], proposer, users
                    )
            return None
        except BaseYuosException:
            raise
        except Exception as error:
            raise BaseYuosException(error) from error

    def _validate_proposal_id(self, proposal_id: str) -> int:
        # Does proposal_id conform to the expected pattern?
        try:
            # Currently just needs to convertible to int
            return int(proposal_id)
        except Exception as error:
            raise InvalidIdException(error) from error

    def _get_instrument_id_from_name(self, instrument_name):
        # Reverse look-up
        for n, v in self.instrument_list.items():
            if v.lower() == instrument_name.lower():
                return n
        raise InvalidIdException(f"instrument {instrument_name} not recognised")

    def _get_proposal_data(self, instrument_id):
        token = self._get_token()

        try:
            data = self.implementation.get_proposal_for_instrument(
                token, self.url, instrument_id
            )
            return data
        except TransportServerError as error:
            raise ConnectionException(f"connection issue: {error}") from error

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

    @staticmethod
    def extract_users(proposal):
        if "users" in proposal:
            return [
                (x.get("firstname", ""), x.get("lastname", ""))
                for x in proposal["users"]
            ]
        return []

    def _get_token(self):
        if self.token:
            return self.token

        try:
            self.token = self.implementation.get_token(
                self.url, self.user, self.password
            )
            if self.token["login"]["token"] is None:
                self.token = None
                raise InvalidCredentialsException(
                    "could not obtain token - incorrect credentials?"
                )
            return self.token
        except ConnectionError as error:
            raise ConnectionException("could not connect - wrong URL?") from error


class _ProposalSystemWrapper:
    """
    Don't use this directly instead use the ProposalSystem class.
    """

    def get_token(self, url, user, password):
        """
        Function for getting a token from the proposal system.

        :param url: the proposal system URL
        :param user: the username
        :param password: the password associated with the user
        :return: the JSON response
        """
        transport = RequestsHTTPTransport(url=url, verify=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        with client as session:
            assert client.schema is not None
            query = gql(
                """
                mutation{
                    login(email: "$USER$", password: "$PASSWORD$"){
                        token
                    }
                }
                """.replace(
                    "$USER$", user
                ).replace(
                    "$PASSWORD$", password
                )
            )
            return session.execute(query)

    def execute_query(self, token, url, query_json):
        """
        Function for making a query on the proposal system.

        :param token: the authorisation token
        :param url: the proposal system URL
        :param query_json: the query to make
        :return: the JSON response
        """
        token = f"Bearer {token['login']['token']}"
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
                        id
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
