from typing import Dict, List, NamedTuple

SampleInfo = NamedTuple(
    "SampleInfo",
    (
        ("id", str),
        ("name", str),
        ("characteristics", Dict),
    ),
)


class User(NamedTuple):
    firstname: str
    lastname: str
    fed_id: str
    organisation: str
    email: str = ""


ProposalInfo = NamedTuple(
    "ProposalInfo",
    (
        ("id", str),
        ("title", str),
        ("proposer", User),
        ("users", List[User]),
        ("db_id", int),
        ("samples", List[SampleInfo]),
    ),
)
