from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


class ProposalSystem:
    """
    Don't use this directly, use YuosClient
    """

    def _execute_query(self, token, url, query_json):
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
        json_data = self._execute_query(
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

    def get_proposals_by_instrument_id(self, token, url, instrument_id):
        json_data = self._execute_query(
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
