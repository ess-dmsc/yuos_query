import pytest

from yuos_query.data_extractors import extract_relevant_sample_info
from yuos_query.exceptions import SampleInfoMissingException


def test_throws_if_relevant_data_missing():
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

    with pytest.raises(SampleInfoMissingException):
        extract_relevant_sample_info(data_missing)
