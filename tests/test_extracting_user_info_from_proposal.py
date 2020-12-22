from yuos_query.proposal_system import ProposalSystemClient


def test_extracting_users_when_no_users_gives_no_users():
    proposal_no_users = {
        "id": 123,
        "title": "Title filled out correctly",
        "users": [],
        "proposer": {"firstname": "Alberto", "lastname": "Accountant"},
    }

    results = ProposalSystemClient.extract_users(proposal_no_users)
    assert len(results) == 0


def test_extracting_users_when_users_not_present_gives_no_users():
    # Not sure if is possible, but...
    proposal_no_users = {
        "id": 123,
        "title": "Title filled out correctly",
        "proposer": {"firstname": "Alberto", "lastname": "Accountant"},
    }

    results = ProposalSystemClient.extract_users(proposal_no_users)
    assert len(results) == 0


def test_extracting_users_when_user_missing_firstname_or_lastname_inserts_blanks():
    # Not sure if is possible, but...
    proposal_missing_parts = {
        "id": 123,
        "title": "Title filled out correctly",
        "users": [
            {"firstname": "Ralf"},  # Missing lastname
            {"lastname": "Fields"},  # Missing firstname
        ],
        "proposer": {"firstname": "Alberto", "lastname": "Accountant"},
    }

    results = ProposalSystemClient.extract_users(proposal_missing_parts)
    assert len(results) == 2
    assert ("Ralf", "") in results
    assert ("", "Fields") in results


def test_extracting_proposer_when_not_present_gives_none():
    # Not sure if is possible, but...
    proposal_no_proposer = {
        "id": 123,
        "title": "Title filled out correctly",
        "users": [
            {"firstname": "Sven", "lastname": "Svensson"},
        ],
    }

    result = ProposalSystemClient.extract_proposer(proposal_no_proposer)
    assert result is None
