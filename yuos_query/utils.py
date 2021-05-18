import json

from yuos_query.data_classes import ProposalInfo, SampleInfo


def serialise_proposals_to_json(proposals):

    json_proposals = {}
    for id, proposal in proposals.items():
        json_proposal = {
            "id": proposal.id,
            "title": proposal.title,
            "proposer": list(proposal.proposer),
            "users": [[user[0], user[1]] for user in proposal.users],
            "db_id": proposal.db_id,
            "samples": [
                {
                    "name": sample.name,
                    "formula": sample.formula,
                    "number": sample.number,
                    "mass_or_volume": list(sample.mass_or_volume),
                    "density": list(sample.density),
                }
                for sample in proposal.samples
            ],
        }
        json_proposals[id] = json_proposal

    return json.dumps(json_proposals, indent=4)


def deserialise_proposals_from_json(json_proposals):
    proposals = {}
    for id, value in json.loads(json_proposals).items():
        proposal = ProposalInfo(
            id=value["id"],
            title=value["title"],
            proposer=tuple(value["proposer"]),
            users=[tuple(user) for user in value["users"]],
            db_id=value["db_id"],
            samples=[
                SampleInfo(
                    name=sample["name"],
                    formula=sample["formula"],
                    number=sample["number"],
                    mass_or_volume=tuple(sample["mass_or_volume"]),
                    density=tuple(sample["density"]),
                )
                for sample in value["samples"]
            ],
        )
        proposals[id] = proposal

    return proposals
