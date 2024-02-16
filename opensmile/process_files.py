import os
import opensmile
import glob

from utils import get_filename

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

input_dir = "/home/tim/Work/nexa/nexa-audio-video-pipelines/data/test/sentimotion/**/*"

# all the output .csv files will be put in this directory, under the same name
output_dir = "/home/tim/Work/nexa/nexa-audio-video-pipelines/data/out/opensmile/multiple"

file_paths = glob.glob(input_dir, recursive=True)

for idx, file_path in enumerate(file_paths):
    print("processing file {}, number {} out of {}".format(file_path, idx, len(file_paths)))

    df = smile.process_file(file_path)

    filename = get_filename(file_path)
    output_path = os.path.join(output_dir, filename + ".csv")
    # save csv
    df.to_csv(output_path, index=False)
