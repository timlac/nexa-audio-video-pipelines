#!/bin/bash

export DATA_MOUNT=/home/tim/Work/nexa/nexa-audio-video-pipelines/data

OUT_PATH=$DATA_MOUNT/out/single
DOCKER_COMPOSE_PATH=/home/tim/Work/nexa/tools/OpenFace/docker-compose.yml

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

#file="$DATA_MOUNT/test/dyads/dyad_1/1A.mp4"
file="$DATA_MOUNT/test/sentimotion/A67_pea_v_3.mov"

# run Openface with docker
docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"

docker-compose -f $DOCKER_COMPOSE_PATH down