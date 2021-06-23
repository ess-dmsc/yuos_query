from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.data_extractors import arrange_by_user


def test_can_organise_proposals_by_fed_id():
    proposals_by_users = arrange_by_user(VALID_PROPOSAL_DATA)
    result = proposals_by_users["jonathantaylor"]

    assert len(result) == 2
    assert {p.id for p in result} == {"471120", "871067"}


def test_includes_experiment_where_user_is_proposer():
    proposals_by_users = arrange_by_user(VALID_PROPOSAL_DATA)
    result = proposals_by_users["fredrikbolmsten"]

    assert len(result) == 1
    assert {p.id for p in result} == {"471120"}
