import opensmile
import os
import pandas as pd

input_path = "/home/tim/Work/nexa/nexa-audio-video-pipelines/data/test/sentimotion/A67_pea_v_3.mov"
output_path = "/home/tim/Work/nexa/nexa-audio-video-pipelines/data/out/opensmile/single/A67_pea_v_3.csv"

# set opensmile parameters
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
)

# process sound file
df = smile.process_file(input_path)

# save csv
df.to_csv(output_path)
