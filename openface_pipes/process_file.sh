#!/bin/bash

# Load environment variables from .env file
export $(cat ../.env | xargs)

export DATA_MOUNT=$PROJECT_ROOT/data

OUT_PATH=$DATA_MOUNT/out/openface/single

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

#file="$DATA_MOUNT/test/dyads/dyad_1/1A.mp4"
file="$DATA_MOUNT/test/sentimotion/A67_pea_v_3.mov"

# run Openface with docker
docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"

docker exec openface chown -R $(id -u):$(id -g) "$OUT_PATH"

docker-compose -f "$DOCKER_COMPOSE_PATH" down