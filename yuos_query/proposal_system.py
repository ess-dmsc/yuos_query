from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from graphql import GraphQLError
from requests import RequestException

from yuos_query.exceptions import (
    BaseYuosException,
    InvalidQueryException,
    InvalidTokenException,
    InvalidUrlException,
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
        except RequestException as error:
            raise InvalidUrlException(error) from error
        except GraphQLError as error:
            raise InvalidQueryException(error) from error
        except Exception as error:
            raise BaseYuosException(error) from error


class ProposalSystem:
    """
    Don't use this directly, use YuosClient
    """

    def __init__(self, url, token):
        self.wrapper = GqlWrapper(url, token)

    def get_instrument_data(self):
        json_data = self._execute(INSTRUMENT_QUERY)
        return json_data["instruments"]["instruments"]

    def get_proposals_by_instrument_id(self, instrument_id):
        query = create_proposal_query(instrument_id)
        json_data = self._execute(query)
        return json_data["proposals"]["proposals"]

    def _execute(self, query):
        return self.wrapper.request(query)
