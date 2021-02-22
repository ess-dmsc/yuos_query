def extract_proposer(proposal):
    if "proposer" in proposal:
        proposer = (
            proposal["proposer"].get("firstname", ""),
            proposal["proposer"].get("lastname", ""),
        )
    else:
        proposer = None
    return proposer


def extract_sample_info(target, data):
    def _get_answers_by_question(questions, target):
        result = {}
        for question in questions:
            # SMELL question within question?
            key_question = question["question"]["question"]
            if key_question.lower() in target:
                result[key_question.lower()] = question["value"]

        return result

    target = [x.lower() for x in target]
    results = []
    for sample in data:
        questions = sample["questionary"]["steps"][0]["fields"]
        result = _get_answers_by_question(questions, target)
        if result:
            results.append(result)
    return results


def extract_users(proposal):
    if "users" in proposal:
        return [
            (x.get("firstname", ""), x.get("lastname", "")) for x in proposal["users"]
        ]
    return []
