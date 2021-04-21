from yuos_query.data_classes import SampleInfo


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
    collected_data = {
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
                if question["value"]:
                    collected_data["name"] = question["value"]
            elif question_key == "Chemical formula":
                if question["value"]:
                    collected_data["formula"] = question["value"]
            elif question_key == "Total number of the same sample":
                if question["value"] and "value" in question["value"]:
                    collected_data["number"] = question["value"]["value"]
            elif question_key == "Mass or volume":
                collected_data["mass_or_volume"] = _extract_value_with_units(question)
            elif question_key == "Density (g/cm*3)":
                if question["value"] and "value" in question["value"]:
                    collected_data["density"] = _extract_value_with_units(
                        question, "g/cm*3"
                    )
        except KeyError:
            # If the data cannot be extracted then we have to use the defaults
            pass

    return SampleInfo(**collected_data)


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
