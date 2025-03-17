FROM python:alpine

RUN pip install --upgrade pip
RUN pip install SpeechRecognition pydub tqdm
RUN apk update && apk upgrade && apk add --no-cache flac ffmpeg

CMD ["python", "/tmp/tmp.py"]
