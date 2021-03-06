SAMPLE_EXAMPLE = [
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
                        },
                        {
                            "value": None,
                            "dependencies": [],
                            "question": {
                                "question": "Sample name and/or material",
                                "naturalKey": "sample_basis",
                            },
                        },
                        {
                            "value": "CHE3S",
                            "dependencies": [],
                            "question": {
                                "question": "Chemical formula",
                                "naturalKey": "text_input_1603713145780",
                            },
                        },
                        {
                            "value": False,
                            "dependencies": [],
                            "question": {
                                "question": "Special Isotopes",
                                "naturalKey": "boolean_1607087013135",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "boolean_1607087013135",
                                    "questionId": "text_input_1607087043945",
                                }
                            ],
                            "question": {
                                "question": "Please give details",
                                "naturalKey": "special_isotopes_input",
                            },
                        },
                        {
                            "value": None,
                            "dependencies": [],
                            "question": {
                                "question": "New question",
                                "naturalKey": "embellishment_1607087117745",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [],
                            "question": {
                                "question": "Additional components",
                                "naturalKey": "text_input_1603874407022",
                            },
                        },
                        {
                            "value": ["Other"],
                            "dependencies": [],
                            "question": {
                                "question": "Form",
                                "naturalKey": "selection_from_options_1601536868245",
                            },
                        },
                        {
                            "value": "Gel",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1601536868245",
                                    "questionId": "text_input_1602676349290",
                                }
                            ],
                            "question": {
                                "question": "Please give details",
                                "naturalKey": "text_input_1602676349290",
                            },
                        },
                        {
                            "value": ["Store at 4C"],
                            "dependencies": [],
                            "question": {
                                "question": "Special Requirements",
                                "naturalKey": "selection_from_options_1601536990025",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1601536990025",
                                    "questionId": "text_input_1603713303928",
                                }
                            ],
                            "question": {
                                "question": "Please give details",
                                "naturalKey": "text_input_1603713303928",
                            },
                        },
                        {
                            "value": {"unit": None, "value": 10},
                            "dependencies": [],
                            "question": {
                                "question": "Total number of the same sample",
                                "naturalKey": "number_input_1610713981207",
                            },
                        },
                        {
                            "value": {"unit": "kg", "value": 5},
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
                            "value": [],
                            "dependencies": [],
                            "question": {
                                "question": "Add File(s)  Please attach all related Safety Data Sheets (SDS) and Crystallographic Information (CIF) files.",
                                "naturalKey": "file_upload_1601537324380",
                            },
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["Yes"],
                            "dependencies": [],
                            "question": {
                                "question": "Temperature ambient?",
                                "naturalKey": "selection_from_options_1609928685331",
                            },
                        },
                        {
                            "value": {"min": "", "max": "", "unit": "kelvin"},
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609928685331",
                                    "questionId": "interval_1609858014044",
                                }
                            ],
                            "question": {
                                "question": "Temperatur Range",
                                "naturalKey": "interval_1609858014044",
                            },
                        },
                        {
                            "value": ["Yes"],
                            "dependencies": [],
                            "question": {
                                "question": "Pressure ambient?",
                                "naturalKey": "selection_from_options_1609929012415",
                            },
                        },
                        {
                            "value": {"min": "", "max": "", "unit": "pascal"},
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929012415",
                                    "questionId": "interval_1609858071129",
                                }
                            ],
                            "question": {
                                "question": "Pressure range",
                                "naturalKey": "interval_1609858071129",
                            },
                        },
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Magnetic field?",
                                "naturalKey": "selection_from_options_1609929067527",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929067527",
                                    "questionId": "text_input_1602681867032",
                                }
                            ],
                            "question": {
                                "question": "Magnetic field strength(T)",
                                "naturalKey": "text_input_1602681867032",
                            },
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Are there any Radioactive hazards associated with your sample?",
                                "naturalKey": "selection_from_options_1609929138919",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929138919",
                                    "questionId": "text_input_1602681978151",
                                }
                            ],
                            "question": {
                                "question": "Please give more details (max 100 characters)",
                                "naturalKey": "text_input_1602681978151",
                            },
                        },
                        {
                            "value": ["Yes"],
                            "dependencies": [],
                            "question": {
                                "question": "Are there any Biological hazards associated with your sample?",
                                "naturalKey": "selection_from_options_1609929232267",
                            },
                        },
                        {
                            "value": "If we leave the cheese out too long it will go mouldy",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929232267",
                                    "questionId": "text_input_1602682027045",
                                }
                            ],
                            "question": {
                                "question": "Please give more details (max 100 characters)",
                                "naturalKey": "text_input_1602682027045",
                            },
                        },
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Is your sample sensitive to air?",
                                "naturalKey": "selection_from_options_1609929356031",
                            },
                        },
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Is your sample sensitive to water vapour?",
                                "naturalKey": "selection_from_options_1609929408773",
                            },
                        },
                        {
                            "value": [],
                            "dependencies": [],
                            "question": {
                                "question": "Are there any other hazards associated with your sample?",
                                "naturalKey": "selection_from_options_1609929454945",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929454945",
                                    "questionId": "text_input_1602682939107",
                                }
                            ],
                            "question": {
                                "question": "Please give details (max 255 characters)",
                                "naturalKey": "text_input_1602682939107",
                            },
                        },
                        {
                            "value": None,
                            "dependencies": [],
                            "question": {
                                "question": "New question",
                                "naturalKey": "embellishment_1602684762285",
                            },
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
                            "dependencies": [],
                            "question": {
                                "question": "New question",
                                "naturalKey": "embellishment_1601536727146_sample",
                            },
                        },
                        {
                            "value": None,
                            "dependencies": [],
                            "question": {
                                "question": "Sample name and/or material",
                                "naturalKey": "sample_basis",
                            },
                        },
                        {
                            "value": "unknown",
                            "dependencies": [],
                            "question": {
                                "question": "Chemical formula",
                                "naturalKey": "text_input_1603713145780",
                            },
                        },
                        {
                            "value": True,
                            "dependencies": [],
                            "question": {
                                "question": "Special Isotopes",
                                "naturalKey": "boolean_1607087013135",
                            },
                        },
                        {
                            "value": "Chaource's one",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "boolean_1607087013135",
                                    "questionId": "text_input_1607087043945",
                                }
                            ],
                            "question": {
                                "question": "Please give details",
                                "naturalKey": "special_isotopes_input",
                            },
                        },
                        {
                            "value": None,
                            "dependencies": [],
                            "question": {
                                "question": "New question",
                                "naturalKey": "embellishment_1607087117745",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [],
                            "question": {
                                "question": "Additional components",
                                "naturalKey": "text_input_1603874407022",
                            },
                        },
                        {
                            "value": ["Liquid"],
                            "dependencies": [],
                            "question": {
                                "question": "Form",
                                "naturalKey": "selection_from_options_1601536868245",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1601536868245",
                                    "questionId": "text_input_1602676349290",
                                }
                            ],
                            "question": {
                                "question": "Please give details",
                                "naturalKey": "text_input_1602676349290",
                            },
                        },
                        {
                            "value": ["Store at 4C"],
                            "dependencies": [],
                            "question": {
                                "question": "Special Requirements",
                                "naturalKey": "selection_from_options_1601536990025",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1601536990025",
                                    "questionId": "text_input_1603713303928",
                                }
                            ],
                            "question": {
                                "question": "Please give details",
                                "naturalKey": "text_input_1603713303928",
                            },
                        },
                        {
                            "value": {"unit": None, "value": 1},
                            "dependencies": [],
                            "question": {
                                "question": "Total number of the same sample",
                                "naturalKey": "number_input_1610713981207",
                            },
                        },
                        {
                            "value": {"unit": "g", "value": 100},
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
                            "value": [],
                            "dependencies": [],
                            "question": {
                                "question": "Add File(s)  Please attach all related Safety Data Sheets (SDS) and Crystallographic Information (CIF) files.",
                                "naturalKey": "file_upload_1601537324380",
                            },
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Temperature ambient?",
                                "naturalKey": "selection_from_options_1609928685331",
                            },
                        },
                        {
                            "value": {"max": 20, "min": 4, "unit": "celsius"},
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609928685331",
                                    "questionId": "interval_1609858014044",
                                }
                            ],
                            "question": {
                                "question": "Temperatur Range",
                                "naturalKey": "interval_1609858014044",
                            },
                        },
                        {
                            "value": ["Yes"],
                            "dependencies": [],
                            "question": {
                                "question": "Pressure ambient?",
                                "naturalKey": "selection_from_options_1609929012415",
                            },
                        },
                        {
                            "value": {"min": "", "max": "", "unit": "pascal"},
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929012415",
                                    "questionId": "interval_1609858071129",
                                }
                            ],
                            "question": {
                                "question": "Pressure range",
                                "naturalKey": "interval_1609858071129",
                            },
                        },
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Magnetic field?",
                                "naturalKey": "selection_from_options_1609929067527",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929067527",
                                    "questionId": "text_input_1602681867032",
                                }
                            ],
                            "question": {
                                "question": "Magnetic field strength(T)",
                                "naturalKey": "text_input_1602681867032",
                            },
                        },
                    ]
                },
                {
                    "fields": [
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Are there any Radioactive hazards associated with your sample?",
                                "naturalKey": "selection_from_options_1609929138919",
                            },
                        },
                        {
                            "value": "",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929138919",
                                    "questionId": "text_input_1602681978151",
                                }
                            ],
                            "question": {
                                "question": "Please give more details (max 100 characters)",
                                "naturalKey": "text_input_1602681978151",
                            },
                        },
                        {
                            "value": ["Yes"],
                            "dependencies": [],
                            "question": {
                                "question": "Are there any Biological hazards associated with your sample?",
                                "naturalKey": "selection_from_options_1609929232267",
                            },
                        },
                        {
                            "value": "can create strange doors",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929232267",
                                    "questionId": "text_input_1602682027045",
                                }
                            ],
                            "question": {
                                "question": "Please give more details (max 100 characters)",
                                "naturalKey": "text_input_1602682027045",
                            },
                        },
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Is your sample sensitive to air?",
                                "naturalKey": "selection_from_options_1609929356031",
                            },
                        },
                        {
                            "value": ["No"],
                            "dependencies": [],
                            "question": {
                                "question": "Is your sample sensitive to water vapour?",
                                "naturalKey": "selection_from_options_1609929408773",
                            },
                        },
                        {
                            "value": ["Other"],
                            "dependencies": [],
                            "question": {
                                "question": "Are there any other hazards associated with your sample?",
                                "naturalKey": "selection_from_options_1609929454945",
                            },
                        },
                        {
                            "value": "if left on the floor, people can slip on them",
                            "dependencies": [
                                {
                                    "dependencyNaturalKey": "selection_from_options_1609929454945",
                                    "questionId": "text_input_1602682939107",
                                }
                            ],
                            "question": {
                                "question": "Please give details (max 255 characters)",
                                "naturalKey": "text_input_1602682939107",
                            },
                        },
                        {
                            "value": None,
                            "dependencies": [],
                            "question": {
                                "question": "New question",
                                "naturalKey": "embellishment_1602684762285",
                            },
                        },
                    ]
                },
            ]
        },
    },
]
