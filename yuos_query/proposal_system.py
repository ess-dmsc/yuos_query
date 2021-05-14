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
    )


class GqlWrapper:
    def __init__(self, url, token):
        self.token = token
        self.url = url

    def request(self, query):
        try:
            token = f"Bearer {self.token}"
            transport = RequestsHTTPTransport(
                url=self.url,
                verify=True,
                headers={"Authorization": token},
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
    Don't use this directly, use YuosClient
    """

    def __init__(self, url, token, querier=None):
        self.querier = querier if querier else GqlWrapper(url, token)

    def _get_instrument_id(self, name):
        data = self._execute(INSTRUMENT_QUERY)
        ids_by_name = {
            inst["shortCode"].lower(): inst["id"]
            for inst in data["instruments"]["instruments"]
        }
        return ids_by_name.get(name)

    def get_proposals_for_instrument(self, name):
        instrument_id = self._get_instrument_id(name.lower())
        query = create_proposal_query(instrument_id)
        data = self._execute(query)
        return self._extract_proposals(data["proposals"]["proposals"])

    def _execute(self, query):
        return self.querier.request(query)

    def _extract_proposals(self, response):
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
