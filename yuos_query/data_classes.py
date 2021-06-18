from typing import List, NamedTuple, Tuple

SampleInfo = NamedTuple(
    "SampleInfo",
    (
        ("name", str),
        ("formula", str),
        ("number", int),
        ("mass_or_volume", Tuple[float, str]),
        ("density", Tuple[float, str]),
    ),
)


ProposalInfo = NamedTuple(
    "ProposalInfo",
    (
        ("id", str),
        ("title", str),
        ("proposer", Tuple[str, str, str]),
        ("users", List[Tuple[str, str, str]]),
        ("db_id", int),
        ("samples", List[SampleInfo]),
    ),
)
