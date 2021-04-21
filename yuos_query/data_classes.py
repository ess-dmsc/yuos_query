from typing import List, NamedTuple, Tuple

ProposalInfo = NamedTuple(
    "ProposalInfo",
    (
        ("id", str),
        ("title", str),
        ("proposer", Tuple[str, str]),
        ("users", List[Tuple[str, str]]),
        ("db_id", int),
    ),
)

SampleInfo = NamedTuple(
    "SampleInfo",
    (
        ("name", str),
        ("formula", str),
        ("number", str),
        ("mass_or_volume", Tuple[float, str]),
        ("density", Tuple[float, str]),
    ),
)
