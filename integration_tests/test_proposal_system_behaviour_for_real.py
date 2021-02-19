import os

import pytest

from tests.test_proposal_system_behaviour import TestProposalSystem
from yuos_query import YuosClient

# These tests are skipped if the TEST_TOKEN environment variable is not defined
SKIP_TEST = True
if "TEST_TOKEN" in os.environ:
    SKIP_TEST = False
    TEST_TOKEN = os.environ["TEST_TOKEN"]


@pytest.mark.skipif(SKIP_TEST, reason="Not set to test against real system")
class TestProposalSystemReal(TestProposalSystem):
    def create_client(
        self,
        invalid_url: bool = False,
        invalid_user: bool = False,
        invalid_password: bool = False,
        unknown_id: bool = False,
    ):
        """
        Runs the tests against a real server!

        NOTE: Only activate one flag at a time!

        :param invalid_url: Behave like the url is invalid.
        :param invalid_user: Behave like the user is invalid.
        :param invalid_password: Behave like the password is invalid.
        :param unknown_id: Behave like the proposal id is invalid.
        :return: A YuosClient instance.
        """
        url = (
            "https://does.not.exist"
            if invalid_url
            else "https://useroffice-test.esss.lu.se/graphql"
        )

        return YuosClient(url, TEST_TOKEN)

    # Tests are inherited from TestProposalSystem
