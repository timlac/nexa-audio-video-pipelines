import subprocess
import os
import glob
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT")

# Define paths
host_video_dir = os.path.join(PROJECT_ROOT, 'data/test/sentimotion')
host_base_output_dir = os.path.join(PROJECT_ROOT, 'data/out/openpose/multiple')
host_models_dir = os.path.join(PROJECT_ROOT, 'data/models/openpose/models/')
container_name = 'd0ckaaa/openpose'

# Define OpenPose parameters
net_resolution = '-1x160'
display = '0'
render_pose = '0'


# Function to run a command
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Error executing command: {command}\n{result.stderr}')
    else:
        print(result.stdout)


# Start the container in detached mode and keep it running
container_id_command = (f'docker run -d --gpus all --user $(id -u):$(id -g) '
                        f'-v "{host_video_dir}:/input" '
                        f'-v "{host_base_output_dir}:/output" '
                        f'{container_name} /bin/bash -c "sleep infinity"')

container_id = subprocess.check_output(container_id_command, shell=True, text=True).strip()

# Copy the models into the running container
copy_models_command = f'docker cp "{host_models_dir}" {container_id}:/opt/openpose/'
run_command(copy_models_command)

# Loop through each video file in the directory
for video_file in os.listdir(host_video_dir):
    if not video_file.endswith(('.mov', '.avi', '.mp4')):  # Add or remove file extensions as needed
        continue

    # Generate a unique output directory for each video file
    video_name = os.path.splitext(video_file)[0]  # Remove the file extension
    host_output_dir = os.path.join(host_base_output_dir, video_name)

    # Create the output directory if it doesn't exist
    os.makedirs(host_output_dir, exist_ok=True)

    # Execute OpenPose within the running container for each video
    exec_command = (f'docker exec {container_id} /bin/bash -c "cd /opt/openpose && ./build/examples/openpose/openpose.bin '
                    f'--video /input/{video_file} '
                    f'--display {display} --render_pose {render_pose} --net_resolution {net_resolution} --write_json /output/{video_name}"')

    run_command(exec_command)

    print(f'Processing of {video_file} complete. Output saved to {host_output_dir}')

# Stop and remove the container after all videos are processed
stop_container_command = f'docker stop {container_id}'
run_command(stop_container_command)
