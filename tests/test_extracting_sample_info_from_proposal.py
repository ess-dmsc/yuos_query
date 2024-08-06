from example_data import get_ymir_example_data
from yuos_query.data_extractors import extract_relevant_sample_info


def get_sample_data():
    for data in get_ymir_example_data()["proposals"]["proposals"]:
        if data["proposalId"] == "597001":  # proposalId 242
            return data["samples"]


def test_sample_info():
    result = extract_relevant_sample_info(get_sample_data())
    assert len(result) == 2
    assert result[0].name == "sample 1"
    assert result[1].name == "sample 2"


def test_supplies_default_if_relevant_data_missing():
    data_missing = [
        {
            "proposalId": 242,
            "title": "Camembert",
            "questionary": {"steps": [{"fields": []}]},
        }
    ]

    result = extract_relevant_sample_info(data_missing)
    assert len(result) == 1
    assert result[0].name == "Camembert"
