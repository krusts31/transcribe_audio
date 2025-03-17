import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm
import os

audio_file = "/tmp/GMT20250227-160420_Recording.m4a"
converted_file = "/tmp/converted_audio.wav"

if not os.path.exists(converted_file):
    print("Converting audio file...")
    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio.export(converted_file, format="wav")

# Initialize Recognizer
recognizer = sr.Recognizer()

# Open the audio file
with sr.AudioFile(converted_file) as source:
    duration = source.DURATION
    chunk_size = 30
    num_chunks = max(1, int(duration / chunk_size))
    
    print(f"\nTotal Duration: {duration:.2f}s | Splitting into {num_chunks} chunks")

    with tqdm(total=num_chunks, desc="Transcribing") as pbar:
        for i in range(num_chunks):
            start_time = i * chunk_size
            end_time = min((i + 1) * chunk_size, duration)

            with sr.AudioFile(converted_file) as chunk_source:
                audio_data = recognizer.record(chunk_source, duration=chunk_size, offset=start_time)

            try:
                text = recognizer.recognize_google(audio_data, language="lv-LV")
            except sr.UnknownValueError:
                text = "[Unrecognized Speech]"
            except sr.RequestError as e:
                text = f"[Error: {e}]"
            
            print(text)
            pbar.update(1)

os.remove(converted_file)
print("\nTranscription Completed. Temporary WAV file deleted.")
