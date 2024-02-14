#!/bin/bash

export DATA_MOUNT=/home/tim/Work/nexa/nexa-audio-video-pipelines/data

OUT_PATH=$DATA_MOUNT/out
DOCKER_COMPOSE_PATH=/home/tim/Work/nexa/tools/OpenFace/docker-compose.yml

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

file="$DATA_MOUNT/test/A67_pea_v_3.mov"

# run Openface with docker
docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"
docker exec openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user


docker-compose -f $DOCKER_COMPOSE_PATH down