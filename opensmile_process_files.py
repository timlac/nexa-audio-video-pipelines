import os
import opensmile
from glob import glob
import argparse
from utils import get_filename
from dotenv import load_dotenv

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process audio files with openSMILE.')
parser.add_argument('input_dir', type=str, help='Input directory for audio files')
parser.add_argument('output_dir', type=str, help='Output directory for CSV files')

args = parser.parse_args()

# Initialize openSMILE
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

# Use arguments for input and output directories
input_dir = args.input_dir
output_dir = args.output_dir

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Search for audio files recursively within input_dir
file_paths = (glob(os.path.join(input_dir, '**/*.mov'), recursive=True)
              + glob(os.path.join(input_dir, "**/*.mp4"), recursive=True))

for idx, file_path in enumerate(file_paths):
    print(f"processing file {file_path}, number {idx + 1} out of {len(file_paths)}")

    df = smile.process_file(file_path)

    filename = get_filename(file_path)
    output_path = os.path.join(output_dir, filename + ".csv")

    # Save CSV
    df.to_csv(output_path)
