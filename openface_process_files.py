import os
import subprocess
from glob import glob
from dotenv import load_dotenv
import argparse
from pathlib import Path


# Function to find the lowest common ancestor directory
def find_common_ancestor(dir1, dir2):
    path1 = Path(dir1).resolve()
    path2 = Path(dir2).resolve()
    common_ancestor = os.path.commonpath([path1, path2])
    return common_ancestor


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process some directories.')
parser.add_argument('input_dir', type=str, help='Input directory')
parser.add_argument('output_dir', type=str, help='Output directory')

args = parser.parse_args()

# Load variables from .env file
load_dotenv()
DOCKER_COMPOSE_PATH = os.getenv("DOCKER_COMPOSE_PATH")

# Use arguments for INPUT_DIR and OUTPUT_DIR
INPUT_DIR = os.path.abspath(args.input_dir)
OUTPUT_DIR = os.path.abspath(args.output_dir)

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Determine DATA_MOUNT as the lowest common ancestor of INPUT_DIR and OUTPUT_DIR
DATA_MOUNT = find_common_ancestor(INPUT_DIR, OUTPUT_DIR)

# Set the DATA_MOUNT environment variable
os.environ['DATA_MOUNT'] = DATA_MOUNT
# Search for .mov and .mp4 files recursively within INPUT_DIR
input_files = (glob(os.path.join(INPUT_DIR, "**/*.mov"), recursive=True)
               + glob(os.path.join(INPUT_DIR, "**/*.mp4"), recursive=True))

# Start OpenFace Docker container
subprocess.run(f'docker-compose -f "{DOCKER_COMPOSE_PATH}" up -d openface && sync', shell=True, check=True)
subprocess.run(['sync'])  # Ensure the service starts

for input_file in input_files:
    subprocess.run(f'docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze '
                   f'-f "{input_file}" -out_dir "{OUTPUT_DIR}"', shell=True, check=True)

subprocess.run(f'docker exec openface chown -R {os.getuid()}:{os.getuid()} "{DATA_MOUNT}"', shell=True, check=True)

subprocess.run(f'docker-compose -f "{DOCKER_COMPOSE_PATH}" down --remove-orphans', shell=True, check=True)
