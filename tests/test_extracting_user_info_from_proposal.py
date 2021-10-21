from yuos_query.data_extractors import extract_proposer, extract_users


class ProposalBuilder:
    def __init__(self):
        self._proposal_data = {"id": "", "title": "", "users": [], "proposer": {}}

    def id(self, id):
        self._proposal_data["id"] = id
        return self

    def title(self, title):
        self._proposal_data["title"] = title
        return self

    def user(self, first, last, org):
        self._proposal_data["users"].append(self._build_user(first, last, org))
        return self

    def no_users(self):
        del self._proposal_data["users"]
        return self

    def proposer(self, first, last, org):
        self._proposal_data["proposer"] = self._build_user(first, last, org)
        return self

    def no_proposer(self):
        del self._proposal_data["proposer"]
        return self

    def _build_user(self, first, last, org):
        user = {}
        if first:
            user["firstname"] = first
        if last:
            user["lastname"] = last
        if org:
            user["organisation"] = org
        return user

    def finish(self):
        return self._proposal_data


def test_extracting_users_when_no_users_gives_no_users():
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .proposer("Alberto", "Accountant", "Some University")
        .finish()
    )

    results = extract_users(proposal)
    assert len(results) == 0


def test_extracting_users_when_no_user_field_gives_no_users():
    # Not sure if is possible, but...
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .proposer("Alberto", "Accountant", "Some University")
        .no_users()
        .finish()
    )

    results = extract_users(proposal)
    assert len(results) == 0


def test_extracting_users_stray_whitespace_removed():
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .user(" Ralf ", " Fields ", " Some University ")
        .proposer("Alberto", "Accountant", "Some University")
        .finish()
    )

    results = extract_users(proposal)
    assert results[0] == ("Ralf", "Fields", "ralffields", "Some University")


def test_extracting_users_when_user_missing_firstname_or_lastname_inserts_blanks():
    # Not sure if is possible, but...
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .user("Ralf", "", "Some University")  # Missing lastname
        .user("", "Fields", "Some University")  # Missing firstname
        .proposer("Alberto", "Accountant", "Some University")
        .finish()
    )

    results = extract_users(proposal)
    assert len(results) == 2
    assert ("Ralf", "", "ralf", "Some University") in results
    assert ("", "Fields", "fields", "Some University") in results


def test_extracting_users_when_user_missing_organisation_inserts_blanks():
    # Not sure if is possible, but...
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .user("Ralf", "Fields", "")  # Missing org
        .proposer("Alberto", "Accountant", "Some University")
        .finish()
    )

    results = extract_users(proposal)
    assert len(results) == 1
    assert ("Ralf", "Fields", "ralffields", "") in results


def test_extracting_proposer_when_not_present_gives_none():
    # Not sure if is possible, but...
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .user("Ralf", "Fields", "Some University")
        .no_proposer()
        .finish()
    )

    result = extract_proposer(proposal)
    assert result is None


def test_extracting_proposer_stray_whitespace_removed():
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .user("Ralf", "Fields", "Some University")
        .proposer(" Alberto ", " Accountant ", " Some University ")
        .finish()
    )

    result = extract_proposer(proposal)
    assert result == ("Alberto", "Accountant", "albertoaccountant", "Some University")


def test_extracting_multiple_users():
    proposal = (
        ProposalBuilder()
        .id(123)
        .title("Title filled out correctly")
        .user("Ralf", "Fields", "Some University")
        .user("Jane", "Eyre", "ESS")
        .proposer(" Alberto ", " Accountant ", " Some University ")
        .finish()
    )

    results = extract_users(proposal)
    assert len(results) == 2
    assert results[0] == ("Ralf", "Fields", "ralffields", "Some University")
    assert results[1] == ("Jane", "Eyre", "janeeyre", "ESS")
