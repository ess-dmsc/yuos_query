from yuos_query.data_extractors import extract_sample_info

EXAMPLE_DATA = [
    {
        "proposalId": 242,
        "title": "Camembert",
        "questionary": {
            "steps": [
                {
                    "fields": [
                        {
                            "value": None,
                            "question": {"question": "New question"},
                        },
                        {
                            "value": None,
                            "question": {"question": "Sample name and/or material"},
                        },
                        {
                            "value": "CHE3S",
                            "question": {"question": "Chemical formula"},
                        },
                        {
                            "value": False,
                            "question": {"question": "Special Isotopes"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Please give details"},
                        },
                        {
                            "value": None,
                            "question": {"question": "New question"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Additional components"},
                        },
                        {"value": ["Other"], "question": {"question": "Form"}},
                        {
                            "value": "Gel",
                            "question": {"question": "Please give details"},
                        },
                        {
                            "value": ["Store at 4C"],
                            "question": {"question": "Special Requirements"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Please give details"},
                        },
                        {
                            "value": {"unit": None, "value": 10},
                            "question": {"question": "Total number of the same sample"},
                        },
                        {
                            "value": {"unit": "kg", "value": 5},
                            "question": {"question": "Mass or volume"},
                        },
                        {
                            "value": {"unit": None, "value": ""},
                            "question": {"question": "Density (g/cm*3)"},
                        },
                        {
                            "value": [],
                            "question": {
                                "question": "Add File(s)  Please attach all related Safety Data Sheets (SDS) and Crystallographic Information (CIF) files."
                            },
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["Yes"],
                            "question": {"question": "Temperature ambient?"},
                        },
                        {
                            "value": {"min": "", "max": "", "unit": "kelvin"},
                            "question": {"question": "Temperatur Range"},
                        },
                        {
                            "value": ["Yes"],
                            "question": {"question": "Pressure ambient?"},
                        },
                        {
                            "value": {"min": "", "max": "", "unit": "pascal"},
                            "question": {"question": "Pressure range"},
                        },
                        {
                            "value": ["No"],
                            "question": {"question": "Magnetic field?"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Magnetic field strength(T)"},
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["No"],
                            "question": {
                                "question": "Are there any Radioactive hazards associated with your sample?"
                            },
                        },
                        {
                            "value": "",
                            "question": {
                                "question": "Please give more details (max 100 characters)"
                            },
                        },
                        {
                            "value": ["Yes"],
                            "question": {
                                "question": "Are there any Biological hazards associated with your sample?"
                            },
                        },
                        {
                            "value": "If we leave the cheese out too long it will go mouldy",
                            "question": {
                                "question": "Please give more details (max 100 characters)"
                            },
                        },
                        {
                            "value": ["No"],
                            "question": {
                                "question": "Is your sample sensitive to air?"
                            },
                        },
                        {
                            "value": ["No"],
                            "question": {
                                "question": "Is your sample sensitive to water vapour?"
                            },
                        },
                        {
                            "value": [],
                            "question": {
                                "question": "Are there any other hazards associated with your sample?"
                            },
                        },
                        {
                            "value": "",
                            "question": {
                                "question": "Please give details (max 255 characters)"
                            },
                        },
                        {
                            "value": None,
                            "question": {"question": "New question"},
                        },
                    ]
                },
            ]
        },
    },
    {
        "proposalId": 242,
        "title": "Chaource",
        "questionary": {
            "steps": [
                {
                    "fields": [
                        {
                            "value": None,
                            "question": {"question": "New question"},
                        },
                        {
                            "value": None,
                            "question": {"question": "Sample name and/or material"},
                        },
                        {
                            "value": "unknown",
                            "question": {"question": "Chemical formula"},
                        },
                        {
                            "value": True,
                            "question": {"question": "Special Isotopes"},
                        },
                        {
                            "value": "Chaource's one",
                            "question": {"question": "Please give details"},
                        },
                        {
                            "value": None,
                            "question": {"question": "New question"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Additional components"},
                        },
                        {"value": ["Liquid"], "question": {"question": "Form"}},
                        {
                            "value": "",
                            "question": {"question": "Please give details"},
                        },
                        {
                            "value": ["Store at 4C"],
                            "question": {"question": "Special Requirements"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Please give details"},
                        },
                        {
                            "value": {"unit": None, "value": 1},
                            "question": {"question": "Total number of the same sample"},
                        },
                        {
                            "value": {"unit": "g", "value": 100},
                            "question": {"question": "Mass or volume"},
                        },
                        {
                            "value": {"unit": None, "value": ""},
                            "question": {"question": "Density (g/cm*3)"},
                        },
                        {
                            "value": [],
                            "question": {
                                "question": "Add File(s)  Please attach all related Safety Data Sheets (SDS) and Crystallographic Information (CIF) files."
                            },
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["No"],
                            "question": {"question": "Temperature ambient?"},
                        },
                        {
                            "value": {"max": 20, "min": 4, "unit": "celsius"},
                            "question": {"question": "Temperatur Range"},
                        },
                        {
                            "value": ["Yes"],
                            "question": {"question": "Pressure ambient?"},
                        },
                        {
                            "value": {"min": "", "max": "", "unit": "pascal"},
                            "question": {"question": "Pressure range"},
                        },
                        {
                            "value": ["No"],
                            "question": {"question": "Magnetic field?"},
                        },
                        {
                            "value": "",
                            "question": {"question": "Magnetic field strength(T)"},
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["No"],
                            "question": {
                                "question": "Are there any Radioactive hazards associated with your sample?"
                            },
                        },
                        {
                            "value": "",
                            "question": {
                                "question": "Please give more details (max 100 characters)"
                            },
                        },
                        {
                            "value": ["Yes"],
                            "question": {
                                "question": "Are there any Biological hazards associated with your sample?"
                            },
                        },
                        {
                            "value": "can create strange doors",
                            "question": {
                                "question": "Please give more details (max 100 characters)"
                            },
                        },
                        {
                            "value": ["No"],
                            "question": {
                                "question": "Is your sample sensitive to air?"
                            },
                        },
                        {
                            "value": ["No"],
                            "question": {
                                "question": "Is your sample sensitive to water vapour?"
                            },
                        },
                        {
                            "value": ["Other"],
                            "question": {
                                "question": "Are there any other hazards associated with your sample?"
                            },
                        },
                        {
                            "value": "if left on the floor, people can slip on them",
                            "question": {
                                "question": "Please give details (max 255 characters)"
                            },
                        },
                        {
                            "value": None,
                            "question": {"question": "New question"},
                        },
                    ]
                },
            ]
        },
    },
]


def test_extract_one_question():
    result = extract_sample_info(["Chemical formula"], EXAMPLE_DATA)
    assert len(result) == 2
    assert result[0]["chemical formula"] == "CHE3S"
    assert result[1]["chemical formula"] == "unknown"


def test_extracting_information_ignores_question_case():
    result = extract_sample_info(["chemical formula"], EXAMPLE_DATA)
    assert result[0]["chemical formula"] == "CHE3S"


def test_extracting_information_for_invalid_question():
    result = extract_sample_info([":: not a question ::"], EXAMPLE_DATA)
    assert not result


def test_multiple_questions_gives_correct_answers():
    questions = ["Chemical formula", "Special Isotopes"]
    result = extract_sample_info(questions, EXAMPLE_DATA)
    assert result[0]["chemical formula"] == "CHE3S"
    assert not result[0]["special isotopes"]


def test_multiple_invalid_questions_returns_nothing():
    questions = [":: not a question 1::", ":: not a question 2::"]
    result = extract_sample_info(questions, EXAMPLE_DATA)
    assert not result


# TODO: We should be able to run these tests against the real server too
# TODO: Return all the questions and all the answers?
