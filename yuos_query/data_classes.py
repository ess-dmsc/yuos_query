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
