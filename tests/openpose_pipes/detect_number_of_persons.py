import os
import json
from glob import glob


def get_json(json_path):
    with open(json_path) as f:
        d = json.load(f)
    return d


def detect_number_of_persons(openpose_output, file):
    if len(openpose_output['people']) > 1:
        print(f'more than one person found for {file}')
        raise ValueError(f'more than one person found for {file}')
    elif len(openpose_output['people']) < 0:
        print(f'no person found for file{file}')
        raise ValueError(f'no person found for file {file}')
    else:
        # print("one person found")
        pass


def detect_for_files(glob_path):
    files = glob(glob_path)

    for idx, file in enumerate(files):
        data = get_json(file)
        detect_number_of_persons(data, file)

    print(f'number of files processed: {len(files)}')


# path = '../data/out/openpose/single/*.json'
path = '../data/out/openpose/multiple/**/*.json'


detect_for_files(path)
