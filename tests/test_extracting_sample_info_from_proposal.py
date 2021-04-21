from yuos_query.data_extractors import extract_relevant_sample_info


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
                                "value": None,
                                "dependencies": [],
                                "question": {
                                    "question": "New question",
                                    "naturalKey": "embellishment_1601536727146_sample",
                                },
                            }
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
    assert result[0].density == ("", "g/cm*3")
    assert result[0].mass_or_volume == ("", "")
