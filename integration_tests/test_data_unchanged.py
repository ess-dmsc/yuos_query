import json
import os

import pytest
from approvaltests.approvals import verify
from approvaltests.reporters.python_native_reporter import PythonNativeReporter

from integration_tests.test_proposal_system_api import URL, YMIR_ID
from yuos_query.proposal_system import GqlWrapper, create_proposal_query

# These tests are skipped if the YUOS_TOKEN environment variable is not defined
SKIP_TEST = True
if "YUOS_TOKEN" in os.environ:
    SKIP_TEST = False
    YUOS_TOKEN = os.environ["YUOS_TOKEN"]

SERVER_URL = "https://useroffice-test.esss.lu.se/graphql"


@pytest.mark.skipif(
    SKIP_TEST, reason="no token supplied for testing against real system"
)
def test_if_data_has_changed_on_proposal_system():
    """If this test fails then it is likely that the data for YMIR has changed
    on the proposal system.

    If this is the case then ymir_data_example.json will need to be replaced
    with the latest data.
    """
    api = GqlWrapper(URL, YUOS_TOKEN)
    response = api.request(create_proposal_query(YMIR_ID))
    verify(json.dumps(response), PythonNativeReporter())
