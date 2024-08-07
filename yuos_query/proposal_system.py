from gql import Client, gql
from gql.transport.exceptions import TransportQueryError, TransportServerError
from gql.transport.requests import RequestsHTTPTransport
from graphql import GraphQLError
from requests import RequestException

from yuos_query.data_classes import ProposalInfo
from yuos_query.data_extractors import (
    extract_proposer,
    extract_relevant_sample_info,
    extract_users,
)
from yuos_query.exceptions import (
    ConnectionException,
    InvalidQueryException,
    InvalidTokenException,
    ServerException,
    UnknownInstrumentException,
)

INSTRUMENT_QUERY = """
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
            """


def create_proposal_query(instrument_id):
    return """
        {
            proposals(filter: {instrumentId: $INST$}){
                totalCount
                proposals {
                  primaryKey
                  title
                  proposalId
                  users {
                    firstname
                    lastname
                    institution
                  }
                  proposer {
                    firstname
                    lastname
                    institution
                  }
                  samples {
                    title
                    id
                  }
                }
              }
            }
        """.replace(
        "$INST$", str(instrument_id)
    )


class GqlWrapper:
    def __init__(self, url, token, proxies):
        self.token = token
        self.url = url
        self.proxies = proxies

    def request(self, query):
        try:
            token = f"Bearer {self.token}"
            transport = RequestsHTTPTransport(
                url=self.url,
                verify=True,
                headers={"Authorization": token},
                proxies=self.proxies,
            )
            client = Client(transport=transport, fetch_schema_from_transport=True)
            with client as session:
                return session.execute(gql(query))
        except TransportQueryError as error:
            raise InvalidTokenException(error) from error
        except TransportServerError as error:
            raise ConnectionException(error) from error
        except RequestException as error:
            raise ConnectionException(error) from error
        except GraphQLError as error:
            raise InvalidQueryException(error) from error
        except Exception as error:
            raise ServerException(error) from error


class ProposalRequester:
    """
    Don't use this directly, use YuosServer
    """

    def __init__(self, url, token, proxies, wrapper=None):
        self.wrapper = wrapper if wrapper else GqlWrapper(url, token, proxies)

    def _get_instrument_id(self, name):
        data = self._execute(INSTRUMENT_QUERY)
        for inst in data["instruments"]["instruments"]:
            if inst["shortCode"].lower() == name:
                return inst["id"]
        raise UnknownInstrumentException(f"Unknown instrument {name}")

    def get_proposals_for_instrument(self, name):
        instrument_id = self._get_instrument_id(name.lower())
        return self._get_proposals(instrument_id)

    def _get_proposals(self, instrument_id):
        query = create_proposal_query(instrument_id)
        data = self._execute(query)
        return self._extract_proposals(data["proposals"]["proposals"])

    def _execute(self, query):
        return self.wrapper.request(query)

    def _extract_proposals(self, response):
        proposals = {}
        for proposal in response:
            users = extract_users(proposal)
            proposer = extract_proposer(proposal)
            title = proposal["title"]
            id = proposal["primaryKey"]
            prop_id = proposal["proposalId"]
            samples = extract_relevant_sample_info(proposal["samples"])

            proposals[prop_id] = ProposalInfo(
                prop_id, title, proposer, users, id, samples
            )

        return proposals
