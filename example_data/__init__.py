import json
import os

location = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_ymir_example_data():
    with open(
        os.path.join(location, "example_data", "ymir_data_example.json"),
        "r",
        encoding="utf8",
    ) as f:
        return json.loads(f.read())
