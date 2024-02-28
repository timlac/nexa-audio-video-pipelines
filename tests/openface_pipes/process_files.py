import os
import subprocess
from glob import glob
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
DOCKER_COMPOSE_PATH = os.getenv("DOCKER_COMPOSE_PATH")

# set the DATA_MOUNT variable
os.environ['DATA_MOUNT'] = os.path.join(PROJECT_ROOT, 'data')
DATA_MOUNT = os.getenv("DATA_MOUNT")

INPUT_DIR = os.path.join(DATA_MOUNT, "test/sentimotion")
OUTPUT_DIR = os.path.join(DATA_MOUNT, "out/openface/multiple")

input_files = glob(INPUT_DIR + "/*")

# Start OpenFace Docker container
subprocess.run(f"docker-compose -f \"{DOCKER_COMPOSE_PATH}\" up -d openface && sync", shell=True, check=True)
subprocess.run(['sync'])  # Ensure the service starts


for input_file in input_files:
    subprocess.run('docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f {} -out_dir {}'
                   .format(input_file, OUTPUT_DIR), shell=True, check=True)


subprocess.run(f"docker exec openface chown -R {os.getuid()}:{os.getuid()} {DATA_MOUNT}", shell=True, check=True)

subprocess.run(f'docker-compose -f {DOCKER_COMPOSE_PATH} down', shell=True, check=True)
