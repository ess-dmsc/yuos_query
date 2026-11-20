from typing import Dict, List, NamedTuple


class SampleInfo(NamedTuple):
    id: str
    name: str
    characteristics: Dict


class User(NamedTuple):
    firstname: str
    lastname: str
    fed_id: str
    organisation: str
    email: str = ""


class ProposalInfo(NamedTuple):
    id: str
    title: str
    proposer: User
    users: List[User]
    db_id: int
    samples: List[SampleInfo]
    local_contacts: List[User] = []
