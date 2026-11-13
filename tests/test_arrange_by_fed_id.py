from tests.test_yuos_client import VALID_PROPOSAL_DATA
from yuos_query.data_classes import ProposalInfo, User
from yuos_query.data_extractors import arrange_by_user


def test_can_organise_proposals_by_fed_id():
    proposals_by_users = arrange_by_user(VALID_PROPOSAL_DATA)
    result = proposals_by_users["jonathantaylor"]

    assert len(result) == 2
    assert {p.id for p in result} == {"471120", "871067"}


def test_excludes_experiment_where_user_is_only_proposer():
    proposals_by_users = arrange_by_user(VALID_PROPOSAL_DATA)

    assert "bobbolmsten" not in proposals_by_users


def test_proposal_listed_once_when_proposer_is_also_a_user():
    proposer = User("Petra", "Aulin", "petraaulin", "ESS")
    proposal = ProposalInfo(
        id="917148",
        title="Proposer is also a user",
        proposer=proposer,
        users=[proposer],
        db_id=0,
        samples=[],
    )

    proposals_by_users = arrange_by_user({"917148": proposal})

    assert [p.id for p in proposals_by_users["petraaulin"]] == ["917148"]
