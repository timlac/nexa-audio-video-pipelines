# Audio Video Pipelines

Welcome to the repository for audio-video pipelines for the DSY project and others. 

## Opensmile 

Relies on simple python wrapper [package](https://pypi.org/project/opensmile/).  

## Openface 

Current implementation relies on the Docker file provided in the [OpenFace repository](https://github.com/TadasBaltrusaitis/OpenFace/wiki/Docker).
Runs as a service. 

## Openpose

Current implementation relies on this Docker [image](https://hub.docker.com/r/d0ckaaa/openpose). 
The installation script for Openpose is supposed to fetch models from a webpage, but the links are [broken](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1602).
To fix this I have downloaded the models manually from [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1602#issuecomment-641653411).
So in the process file/files scripts the models are automatically copied into the container after start.

The output format for openpose is described in the [documentation](https://cmu-perceptual-computing-lab.github.io/openpose/web/html/doc/md_doc_02_output.html).
Since openpose produces one output file for every frame I am currently working on simple script to merge
the output into one large json/csv file, see script `json_to_csv`.

### Considerations

Sensitive to GPU memory. Fails in my personal computer GPU: `NVIDIA RTX A2000 8GB` using higher resolutions. 
Fails when trying to extract hand pose altogether.

Openpose produces one output per person when there are multiple people in the frame, 
but does not keep track of who is who across multiple frames. This can be handled in multiple ways:

- Make sure there is only one person across all frames in the output files. See script `detect_number_of_persons`.
- Explore different options for person tracking, see [Github issue](https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1448).
- Use Openface person identification and sync some part of the body, 
  e.g. the nose, and apply the same person id to the openpose output. 
