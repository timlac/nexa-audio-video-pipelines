import os
import subprocess
from glob import glob


os.environ['DATA_MOUNT'] = "/home/tim/Work/nexa/nexa-audio-video-pipelines/data"
DATA_MOUNT = os.getenv("DATA_MOUNT")


DOCKER_COMPOSE_PATH = "/home/tim/Work/nexa/tools/OpenFace/docker-compose.yml"

INPUT_DIR = os.path.join(DATA_MOUNT, "test/sentimotion")
OUTPUT_DIR = os.path.join(DATA_MOUNT, "out/multiple")


input_files = glob(INPUT_DIR + "/*")

# Start OpenFace Docker container
subprocess.run(f"docker-compose -f \"{DOCKER_COMPOSE_PATH}\" up -d openface && sync", shell=True, check=True)
subprocess.run(['sync'])  # Ensure the service starts


for input_file in input_files:
    subprocess.run('docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f {} -out_dir {}'
                   .format(input_file, OUTPUT_DIR), shell=True, check=True)


subprocess.run(f"docker exec openface chown -R {os.getuid()}:{os.getuid()} {DATA_MOUNT}", shell=True, check=True)

subprocess.run(f'docker-compose -f {DOCKER_COMPOSE_PATH} down', shell=True, check=True)
