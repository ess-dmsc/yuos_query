from yuos_query.data_classes import SampleInfo, User


def _generate_fed_id(firstname, lastname):
    # TODO: this is a hack to generate something like a fed ID while
    # we wait for the real fed IDs to appear in the proposal system
    return f"{firstname}{lastname}".lower()


def extract_proposer(proposal):
    def _extract_name(user):
        first = user.get("firstname", "").strip()
        last = user.get("lastname", "").strip()
        return User(first, last, _generate_fed_id(first, last))

    if "proposer" in proposal:
        proposer = _extract_name(proposal["proposer"])
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
        return User(first, last, _generate_fed_id(first, last))

    if "users" in proposal:
        return [_extract_name(user) for user in proposal["users"]]
    return []


def _extract_sample_data(sample_data):
    extracted_data = {
        "name": "",
        "formula": "",
        "number": 1,
        "mass_or_volume": (0, ""),
        "density": (0, "g/cm*3"),
    }

    questions = sample_data["questionary"]["steps"][0]["fields"]
    for question in questions:
        try:
            question_key = question["question"]["question"]
            if question_key == "Sample name and/or material":
                extracted_data["name"] = _extract_simple_value(question, "")
            elif question_key == "Chemical formula":
                extracted_data["formula"] = _extract_simple_value(question, "")
            elif question_key == "Total number of the same sample":
                extracted_data["number"] = _extract_number(question, 1)
            elif question_key == "Mass or volume":
                extracted_data["mass_or_volume"] = _extract_value_with_units(question)
            elif question_key == "Density (g/cm*3)":
                extracted_data["density"] = _extract_value_with_units(
                    question, "g/cm*3"
                )
        except KeyError:
            # If the data cannot be extracted then we have to use the defaults
            pass

    return SampleInfo(**extracted_data)


def _extract_simple_value(question, default_value):
    if question["value"]:
        return question["value"]
    return default_value


def _extract_number(question, default_value):
    if (
        question["value"]
        and "value" in question["value"]
        and question["value"]["value"]
    ):
        return question["value"]["value"]
    return default_value


def _extract_value_with_units(question, default_units=""):
    value = 0
    units = default_units
    if "value" in question["value"] and question["value"]["value"]:
        value = question["value"]["value"]
    if "unit" in question["value"] and question["value"]["unit"]:
        units = question["value"]["unit"]
    return value, units


def extract_relevant_sample_info(data):
    results = []
    for sample in data:
        results.append(_extract_sample_data(sample))
    return results


def arrange_by_user(proposals_by_id):
    proposals_by_users = {}
    for proposal_id, proposal in proposals_by_id.items():
        for user in proposal.users:
            fed_id = user[2]
            for_user = proposals_by_users.get(fed_id, [])
            for_user.append(proposal)
            proposals_by_users[fed_id] = for_user

    return proposals_by_users
