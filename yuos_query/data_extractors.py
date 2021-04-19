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


def extract_relevant_sample_info(data):
    def _extract_for_sample(sample_data):
        collected_data = {
            "name": "",
            "formula": "",
            "number": 1,
            "mass_or_volume": ("", ""),
            "density": ("", "g/cm*3"),
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
                    if question["value"]:
                        collected_data["mass_or_volume"] = (
                            question["value"]["value"]
                            if "value" in question["value"]
                            else "",
                            question["value"]["unit"]
                            if "unit" in question["value"]
                            else "",
                        )
                elif question_key == "Density (g/cm*3)":
                    if question["value"] and "value" in question["value"]:
                        collected_data["density"] = (
                            question["value"]["value"],
                            "g/cm*3",
                        )
            except KeyError:
                # If the data cannot be extracted then we have to use the defaults
                pass

        return SampleInfo(**collected_data)

    results = []
    for sample in data:
        results.append(_extract_for_sample(sample))
    return results
