from example_data import get_ymir_example_data
from yuos_query.data_extractors import extract_relevant_sample_info


def get_sample_data():
    for data in get_ymir_example_data():
        if data["proposalId"] == "711730":
            return data["samples"]


def test_sample_info():
    result = extract_relevant_sample_info(get_sample_data())
    assert len(result) == 2
    assert result[0].id == "1d850a9d-91dd-4076-86ac-90fb62d5f35b"
    assert result[1].id == "23cb93c2-9461-4bde-9f40-812794876c7f"


def test_supplies_default_if_relevant_data_missing():
    data_missing = [
        {
            "proposalId": "711730",
            "_id": "Camembert",
        }
    ]

    result = extract_relevant_sample_info(data_missing)
    assert len(result) == 1
    assert result[0].id == "Camembert"
