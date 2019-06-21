import json


def from_json(content):
    return json.loads(content)


def to_json(content):
    return json.dumps(content)
