# TRANSCRIBER

## 1 be on linux and know how to use a trerminal

## Install docker 

https://docs.docker.com/engine/install/debian/

## Build docker image

```bash
docker build -t transcriber .
```

## Transcriber

```bash
docker run -it -v ./:/ transcriber > output.txt
```

## Results

If you follow these steps successfully you should see a progress bar updaiting. Once done you will have output.txt.
