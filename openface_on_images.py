import os
import subprocess
from glob import glob
from multiprocessing import Pool
from dotenv import load_dotenv
import argparse
from pathlib import Path

# --- Setup CLI ---
parser = argparse.ArgumentParser(description="Run OpenFace on images in parallel.")
parser.add_argument("input_dir", type=str, help="Directory containing input .jpg images")
parser.add_argument("output_dir", type=str, help="Directory to save OpenFace output")
parser.add_argument("--processes", type=int, default=4, help="Number of parallel workers (default: 4)")
args = parser.parse_args()

# --- Load environment (.env should define DOCKER_COMPOSE_PATH, DOCKERUSER, DOCKERTAG) ---
load_dotenv()
DOCKER_COMPOSE_PATH = os.getenv("DOCKER_COMPOSE_PATH")
DOCKER_IMAGE_NAME = "openface"

# --- Resolve and prepare paths ---
INPUT_DIR = os.path.abspath(args.input_dir)
OUTPUT_DIR = os.path.abspath(args.output_dir)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATA_MOUNT = os.path.commonpath([INPUT_DIR, OUTPUT_DIR])
os.environ["DATA_MOUNT"] = DATA_MOUNT

# --- Start Docker container ---
subprocess.run(f'docker-compose -f "{DOCKER_COMPOSE_PATH}" up -d openface && sync', shell=True, check=True)
subprocess.run(['sync'])

# --- Gather input files ---
image_paths = sorted(glob(os.path.join(INPUT_DIR, "*.jpg")))

def run_openface_on_image(image_path):
    filename = Path(image_path).name
    output_csv = os.path.join(OUTPUT_DIR, filename.replace(".jpg", ".csv"))

    if os.path.exists(output_csv):
        return  # Already processed

    cmd = (
        f'docker exec {DOCKER_IMAGE_NAME} FeatureExtraction '
        f'-2Dfp -3Dfp -pdmparams -pose -aus -gaze '
        f'-f "{image_path}" -out_dir "{OUTPUT_DIR}"'
    )

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed on {filename}: {e}")

# --- Parallel execution ---
with Pool(processes=args.processes) as pool:
    pool.map(run_openface_on_image, image_paths)

# --- Fix file permissions ---
subprocess.run(f'docker exec {DOCKER_IMAGE_NAME} chown -R {os.getuid()}:{os.getuid()} "{DATA_MOUNT}"', shell=True, check=True)

# --- Stop Docker container ---
subprocess.run(f'docker-compose -f "{DOCKER_COMPOSE_PATH}" down --remove-orphans', shell=True, check=True)
