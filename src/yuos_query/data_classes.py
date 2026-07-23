from typing import Dict, List, NamedTuple, Tuple

SampleInfo = NamedTuple(
    "SampleInfo",
    (
        ("id", str),
        ("name", str),
        ("characteristics", Dict),
    ),
)

User = NamedTuple(
    "User",
    (
        ("firstname", str),
        ("lastname", str),
        ("fed_id", str),
        ("organisation", str),
    ),
)


ProposalInfo = NamedTuple(
    "ProposalInfo",
    (
        ("id", str),
        ("title", str),
        ("proposer", Tuple[str, str, str]),
        ("users", List[User]),
        ("db_id", int),
        ("samples", List[SampleInfo]),
    ),
)
