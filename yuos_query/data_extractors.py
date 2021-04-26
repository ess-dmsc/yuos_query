def extract_proposer(proposal):
    if "proposer" in proposal:
        proposer = (
            proposal["proposer"].get("firstname", ""),
            proposal["proposer"].get("lastname", ""),
        )
    else:
        proposer = None
    return proposer


def extract_users(proposal):
    if "users" in proposal:
        return [
            (x.get("firstname", ""), x.get("lastname", "")) for x in proposal["users"]
        ]
    return []


def _extract_sample_data(sample_data):
    extracted_data = {
        "name": "",
        "formula": "",
        "number": 1,
        "mass/volume": (0, ""),
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
                extracted_data["mass/volume"] = _extract_value_with_units(question)
            elif question_key == "Density (g/cm*3)":
                extracted_data["density"] = _extract_value_with_units(
                    question, "g/cm*3"
                )
        except KeyError:
            # If the data cannot be extracted then we have to use the defaults
            pass

    return extracted_data


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
