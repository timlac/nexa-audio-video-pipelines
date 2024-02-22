import json
import os
from glob import glob


# Define the directory containing the JSON output files and the output JSON file path
json_dir = '../data/out/openpose/single/*.json'
aggregated_json_path = '../data/out/openpose/aggregated_data.json'

json_files = glob(json_dir)


# Define the keypoints based on the OpenPose model you're using (BODY_25 in this example)
keypoints = [
    'Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist', 'LShoulder', 'LElbow',
    'LWrist', 'MidHip', 'RHip', 'RKnee', 'RAnkle', 'LHip', 'LKnee', 'LAnkle',
    'REye', 'LEye', 'REar', 'LEar', 'LBigToe', 'LSmallToe', 'LHeel', 'RBigToe',
    'RSmallToe', 'RHeel'
]

# Initialize an empty list to hold the structured data for all frames
all_frames_data = []

# Process each JSON file
for frame_index, json_file in enumerate(sorted(json_files)):
    with open(json_file) as f:
        data = json.load(f)

    # Assuming there's only one person detected per frame for simplicity
    if data['people']:
        keypoints_data = data['people'][0]['pose_keypoints_2d']
        frame_data = {'frame': frame_index}

        for i, keypoint in enumerate(keypoints):
            base_index = i * 3
            frame_data[f'{keypoint}_x'] = keypoints_data[base_index]
            frame_data[f'{keypoint}_y'] = keypoints_data[base_index + 1]
            frame_data[f'{keypoint}_c'] = keypoints_data[base_index + 2]

        all_frames_data.append(frame_data)

# Write the structured data to a new JSON file
with open(aggregated_json_path, 'w') as f:
    json.dump(all_frames_data, f)

print(f"Structured JSON data has been saved to {aggregated_json_path}")
