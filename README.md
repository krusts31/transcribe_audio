# TRANSCRIBER

## 1 be on linux and know how to use a trerminal

## ADD YOU MP4 file to repo

open tmp.py or transcriber.py file and replace the file name with the file name you want to have a transcirbe to.

```python
audio_file = "/tmp/YOUR_FILE_NAME.m4a"
```

## Install docker 

https://docs.docker.com/engine/install/debian/

## Build docker image

```bash
docker build -t transcriber .
```

## Transcriber

```bash
docker run -it -v ./:/tmp transcriber > output.txt
```

## Results

If you follow these steps successfully you should see a progress bar updaiting. Once done you will have output.txt.
