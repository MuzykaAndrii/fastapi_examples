import json


def open_mock_json(model: str):
    with open(f"tests/mocks/mock_{model}.json") as f:
        return json.load(f)
