from tests.sample_data_example import SAMPLE_EXAMPLE
from yuos_query.data_extractors import extract_relevant_sample_info


def test_extracts_relevant_questions_and_answers():
    result = extract_relevant_sample_info(SAMPLE_EXAMPLE)

    assert len(result) == 2
    assert len(result[0]) == 5

    assert result[0].name is None
    assert result[0].formula == "CHE3S"
    assert result[0].number == 10
    assert result[0].mass_or_volume == (5, "kg")
    assert result[0].density == ("", "g/cm*3")

    assert result[1].name is None
    assert result[1].formula == "unknown"
    assert result[1].number == 1
    assert result[1].mass_or_volume == (100, "g")
    assert result[1].density == ("", "g/cm*3")
