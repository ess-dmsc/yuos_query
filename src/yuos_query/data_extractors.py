from yuos_query.data_classes import SampleInfo, User


def _generate_fed_id(firstname, lastname):
    # TODO: this is a hack to generate something like a fed ID while
    # we wait for the real fed IDs to appear in the proposal system
    return f"{firstname}{lastname}".lower()


def extract_proposer(proposal):
    def _extract_details(user):
        first = user.get("firstname", "").strip()
        last = user.get("lastname", "").strip()
        org = user.get("institution", "").strip()
        return User(first, last, _generate_fed_id(first, last), org)

    if "proposer" in proposal:
        proposer = _extract_details(proposal["proposer"])
    else:
        proposer = None
    return proposer


def extract_users(proposal):
    """
    :param proposal: The proposal
    :return: A tuple of first name, last name, fed id
    """

    def _extract_name(user):
        first = user.get("firstname", "").strip()
        last = user.get("lastname", "").strip()
        org = user.get("institution", "").strip()
        return User(first, last, _generate_fed_id(first, last), org)

    if "users" in proposal:
        return [_extract_name(user) for user in proposal["users"]]
    return []


def _extract_sample_data(sample_data):
    extracted_data = {
        "name": "",
    }

    try:
        extracted_data["name"] = sample_data.get("title", "")
    except KeyError:
        # If the data cannot be extracted then we have to use the defaults
        pass

    return SampleInfo(**extracted_data)


def _extract_simple_value(question, default_value):
    return question.get("value", default_value)


def _extract_number(question, default_value):
    try:
        return eval(question.get("value", default_value))
    except RuntimeError:
        return default_value


def _extract_value_with_units(question, default_value=0, default_units=""):
    try:
        value = eval(question.get("value", 0))
    except RuntimeError:
        value = 0
    units = question.get("units", default_units)
    return value, units


def extract_relevant_sample_info(data):
    results = []
    for sample in data:
        results.append(_extract_sample_data(sample))
    return results


def arrange_by_user(proposals_by_id):
    proposals_by_users = {}
    for proposal_id, proposal in proposals_by_id.items():
        users = proposal.users[:]
        if proposal.proposer:
            users.append(proposal.proposer)
        for user in users:
            fed_id = user[2]
            for_user = proposals_by_users.get(fed_id, [])
            for_user.append(proposal)
            proposals_by_users[fed_id] = for_user

    return proposals_by_users
