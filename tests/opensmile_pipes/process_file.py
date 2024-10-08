import opensmile
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT")

input_path = os.path.join(PROJECT_ROOT, "data/test/random_examples/jodie_foster.mp4")
output_dir = os.path.join(PROJECT_ROOT, "data/out/opensmile/single/")
output_filename = "jodie_foster.csv"
os.makedirs(output_dir, exist_ok=True)

# set opensmile parameters
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

print(f"Processing {input_path}")
# process sound file
df = smile.process_file(input_path)
print(f'Done')

# save csv
df.to_csv(os.path.join(output_dir, output_filename))
print(f'Saved to {os.path.join(output_dir, output_filename)}')
