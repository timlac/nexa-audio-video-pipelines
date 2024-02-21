import os
import json
from glob import glob


def get_json(path):
    with open(path) as f:
        d = json.load(f)
    return d


files = glob('../data/out/openpose/single/*.json')

for file in files:
    data = get_json(file)

