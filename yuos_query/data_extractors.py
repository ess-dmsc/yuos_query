from yuos_query.data_classes import SampleInfo
from yuos_query.exceptions import SampleInfoMissingException


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
        collected_data = {}

        questions = sample_data["questionary"]["steps"][0]["fields"]
        for question in questions:
            question_key = question["question"]["question"]
            if question_key == "Sample name and/or material":
                collected_data["name"] = question["value"]
            elif question_key == "Chemical formula":
                collected_data["formula"] = question["value"]
            elif question_key == "Total number of the same sample":
                collected_data["number"] = question["value"]["value"]
            elif question_key == "Mass or volume":
                collected_data["mass_or_volume"] = (
                    question["value"]["value"],
                    question["value"]["unit"],
                )
            elif question_key == "Density (g/cm*3)":
                collected_data["density"] = (question["value"]["value"], "g/cm*3")

        try:
            return SampleInfo(**collected_data)
        except TypeError as error:
            raise SampleInfoMissingException() from error

    results = []
    for sample in data:
        results.append(_extract_for_sample(sample))
    return results
