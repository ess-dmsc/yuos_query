from tests.sample_data_example import SAMPLE_EXAMPLE
from yuos_query.data_extractors import extract_relevant_sample_info


def test_sample_info():
    result = extract_relevant_sample_info(SAMPLE_EXAMPLE)
    assert len(result) == 2
    assert result[0].name == ""
    assert result[0].formula == "CHE3S"
    assert result[0].number == 10
    assert result[0].density == (0, "g/cm*3")
    assert result[0].mass_or_volume == (5, "kg")


def test_supplies_default_if_relevant_data_missing():
    data_missing = [
        {
            "proposalId": 242,
            "title": "Camembert",
            "questionary": {
                "steps": [
                    {
                        "fields": [
                            {
                                "value": {"unit": None, "value": ""},
                                "dependencies": [],
                                "question": {
                                    "question": "Density (g/cm*3)",
                                    "naturalKey": "number_input_1610713898040",
                                },
                            },
                        ]
                    }
                ]
            },
        }
    ]

    result = extract_relevant_sample_info(data_missing)
    assert len(result) == 1
    assert result[0].name == ""
    assert result[0].formula == ""
    assert result[0].number == 1
    assert result[0].density == (0, "g/cm*3")
    assert result[0].mass_or_volume == (0, "")


def test_supplies_default_if_blank_data():
    data_missing = [
        {
            "proposalId": 242,
            "title": "Camembert",
            "id": 153,
            "questionary": {
                "steps": [
                    {
                        "fields": [
                            {
                                "value": {"unit": "kg", "value": ""},
                                "dependencies": [],
                                "question": {
                                    "question": "Mass or volume",
                                    "naturalKey": "number_input_1610698357121",
                                },
                            },
                            {
                                "value": {"unit": None, "value": ""},
                                "dependencies": [],
                                "question": {
                                    "question": "Density (g/cm*3)",
                                    "naturalKey": "number_input_1610713898040",
                                },
                            },
                            {
                                "value": {"value": "", "unit": None},
                                "dependencies": [],
                                "question": {
                                    "question": "Total number of the same sample",
                                    "naturalKey": "number_input_1610713981207",
                                },
                            },
                        ]
                    }
                ]
            },
        }
    ]
    result = extract_relevant_sample_info(data_missing)
    assert result[0].density == (0, "g/cm*3")
    assert result[0].mass_or_volume == (0, "kg")
    assert result[0].number == 1
