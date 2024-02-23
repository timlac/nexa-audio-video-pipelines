import json
from glob import glob

from constants import hand_keypoints, body_keypoints


def process_keypoints(keypoints_data, keypoints, prefix):
    """Process keypoints data and return structured keypoint information with the specified prefix."""
    frame_data = {}
    for i, keypoint in enumerate(keypoints):
        base_index = i * 3
        frame_data[f'{prefix}{keypoint}_x'] = keypoints_data[base_index]
        frame_data[f'{prefix}{keypoint}_y'] = keypoints_data[base_index + 1]
        frame_data[f'{prefix}{keypoint}_c'] = keypoints_data[base_index + 2]
    return frame_data


# Define the directory containing the JSON output files and the output JSON file path
json_dir = '../data/out/openpose/multiple/A102_gra_p_3/*.json'
aggregated_json_path = '../data/out/openpose/aggregated_data.json'

json_files = glob(json_dir)

# Initialize an empty list to hold the structured data for all frames
all_frames_data = []

# Process each JSON file
for frame_index, json_file in enumerate(sorted(json_files)):
    with open(json_file) as f:
        data = json.load(f)

    # Assuming there's only one person detected per frame for simplicity
    if data['people']:
        person_data = data['people'][0]
        frame_data = {'frame': frame_index}

        # Process body, left hand, and right hand keypoints
        frame_data.update(process_keypoints(person_data['pose_keypoints_2d'], body_keypoints, 'body_'))
        # frame_data.update(process_keypoints(person_data['hand_left_keypoints_2d'], hand_keypoints, 'left_hand_'))
        # frame_data.update(process_keypoints(person_data['hand_right_keypoints_2d'], hand_keypoints, 'right_hand_'))

        all_frames_data.append(frame_data)

# Write the structured data to a new JSON file
with open(aggregated_json_path, 'w') as f:
    json.dump(all_frames_data, f)

print(f"Structured JSON data for body and hand keypoints has been saved to {aggregated_json_path}")
