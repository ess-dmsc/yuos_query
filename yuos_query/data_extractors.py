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
        result = {}

        questions = sample_data["questionary"]["steps"][0]["fields"]
        for question in questions:
            question_key = question["question"]["question"]
            if question_key == "Sample name and/or material":
                result["name"] = question["value"]
            elif question_key == "Chemical formula":
                result["formula"] = question["value"]
            elif question_key == "Total number of the same sample":
                result["number"] = question["value"]["value"]
            elif question_key == "Mass or volume":
                result["mass_or_volume"] = (
                    question["value"]["value"],
                    question["value"]["unit"],
                )
            elif question_key == "Density (g/cm*3)":
                result["density"] = (question["value"]["value"], "g/cm*3")
        return SampleInfo(**result)

    results = []
    for sample in data:
        results.append(_extract_for_sample(sample))
    return results
