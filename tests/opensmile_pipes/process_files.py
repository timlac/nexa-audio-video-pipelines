import os
import opensmile
import glob

from utils import get_filename

from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT")


smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

input_dir = os.path.join(PROJECT_ROOT, "data/test/sentimotion/**/*")

# all the output .csv files will be put in this directory, under the same name
output_dir = os.path.join(PROJECT_ROOT, "data/out/opensmile/multiple")
os.makedirs(output_dir, exist_ok=True)

file_paths = glob.glob(input_dir, recursive=True)

for idx, file_path in enumerate(file_paths):
    print("processing file {}, number {} out of {}".format(file_path, idx, len(file_paths)))

    df = smile.process_file(file_path)

    filename = get_filename(file_path)
    output_path = os.path.join(output_dir, filename + ".csv")
    # save csv
    df.to_csv(output_path, index=False)
