import os
import subprocess
import argparse
from dotenv import load_dotenv
from pathlib import Path

# --- Argument parser ---
parser = argparse.ArgumentParser(description="Run OpenFace FaceLandmarkImg on a folder of images.")
parser.add_argument("input_dir", type=str, help="Input directory containing .jpg images (e.g., patient images)")
parser.add_argument("output_dir", type=str, help="Output directory for OpenFace results")
args = parser.parse_args()

# --- Load .env variables ---
load_dotenv()
DOCKER_COMPOSE_PATH = os.getenv("DOCKER_COMPOSE_PATH")
DOCKER_IMAGE_NAME = "openface"

# --- Resolve paths ---
INPUT_DIR = os.path.abspath(args.input_dir)
OUTPUT_DIR = os.path.abspath(args.output_dir)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Mount setup (common ancestor) ---
DATA_MOUNT = os.path.commonpath([INPUT_DIR, OUTPUT_DIR])
os.environ["DATA_MOUNT"] = DATA_MOUNT

# --- Start Docker container ---
subprocess.run(f'docker-compose -f "{DOCKER_COMPOSE_PATH}" up -d {DOCKER_IMAGE_NAME} && sync', shell=True, check=True)
subprocess.run(['sync'])  # Just in case

# --- Run FaceLandmarkImg on all images in input_dir ---
subprocess.run(
    f'docker exec {DOCKER_IMAGE_NAME} FaceLandmarkImg -fdir "{INPUT_DIR}" -out_dir "{OUTPUT_DIR}" -pose -gaze -aus',
    shell=True,
    check=True
)

# --- Fix ownership (optional, useful if files are owned by root inside container) ---
subprocess.run(
    f'docker exec {DOCKER_IMAGE_NAME} chown -R {os.getuid()}:{os.getgid()} "{DATA_MOUNT}"',
    shell=True,
    check=True
)

# --- Stop Docker container ---
subprocess.run(f'docker-compose -f "{DOCKER_COMPOSE_PATH}" down --remove-orphans', shell=True, check=True)
