#!/bin/bash

# Load environment variables from .env file
export $(cat ../.env | xargs)

# Define paths
HOST_VIDEO_PATH=$PROJECT_ROOT/data/test/sentimotion/A67_pea_v_3.mov  # Full path to the input video on your host
HOST_OUTPUT_DIR=$PROJECT_ROOT/data/out/openpose/single  # Directory where you want to save output on your host
HOST_MODELS_DIR=$PROJECT_ROOT/data/models/openpose/models/  # Directory where your OpenPose models are located on your host
CONTAINER_NAME=d0ckaaa/openpose  # Name of the OpenPose Docker image

# Define OpenPose parameters
NET_RESOLUTION="-1x160"  # Adjust based on your GPU memory and requirements
DISPLAY="0"
RENDER_POSE="0"
WRITE_JSON="output/"  # Directory inside the container where JSON output will be saved

# Start the container in detached mode and keep it running
CONTAINER_ID=$(docker run -d --gpus all --user $(id -u):$(id -g) -v $(dirname "$HOST_VIDEO_PATH"):/input \
-v $HOST_OUTPUT_DIR:/output $CONTAINER_NAME /bin/bash -c "sleep infinity")


echo $CONTAINER_ID

# Copy the models into the running container
docker cp $HOST_MODELS_DIR $CONTAINER_ID:/opt/openpose/

# Execute OpenPose within the container
docker exec $CONTAINER_ID /bin/bash -c "cd /opt/openpose && ./build/examples/openpose/openpose.bin \
--video /input/'$(basename "$HOST_VIDEO_PATH")' \
--display $DISPLAY --render_pose $RENDER_POSE --net_resolution $NET_RESOLUTION --write_json /output"


# Stop and remove the container
docker stop $CONTAINER_ID

echo "Processing of $(basename "$HOST_VIDEO_PATH") complete. Output saved to $HOST_OUTPUT_DIR"