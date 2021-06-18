from yuos_query.data_classes import SampleInfo


def extract_proposer(proposal):
    if "proposer" in proposal:
        proposer = (
            proposal["proposer"].get("firstname", "").strip(),
            proposal["proposer"].get("lastname", "").strip(),
        )
    else:
        proposer = None
    return proposer


def extract_users(proposal):
    if "users" in proposal:
        return [
            (x.get("firstname", "").strip(), x.get("lastname", "").strip())
            for x in proposal["users"]
        ]
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
            fed_id = f"{user[0]}{user[1]}".lower()
            for_user = proposals_by_users.get(fed_id, [])
            for_user.append(proposal)
            proposals_by_users[fed_id] = for_user

    return proposals_by_users
