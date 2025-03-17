from multiprocessing import Pool
import speech_recognition as sr
from pydub import AudioSegment, silence
from tqdm import tqdm
import os

audio_file = "/tmp/GMT20250227-160420_Recording.m4a"
converted_file = "/tmp/converted_audio.wav"

if not os.path.exists(converted_file):
    print("Converting audio file...")
    audio = AudioSegment.from_file(audio_file, format="m4a")
    audio = audio.set_frame_rate(16000)  # Reduce sample rate
    audio.export(converted_file, format="wav")

# Load converted WAV file
audio = AudioSegment.from_wav(converted_file)

# Function to detect non-silent segments in a chunk
def detect_speech_chunk(start_end):
    start, end = start_end
    return silence.detect_nonsilent(audio[start:end], min_silence_len=700, silence_thresh=-40)

# Split the file into 1-minute segments for parallel processing
chunk_duration = 60000  # 1 minute in milliseconds
audio_length = len(audio)
chunk_ranges = [(i, min(i + chunk_duration, audio_length)) for i in range(0, audio_length, chunk_duration)]

print(f"Splitting audio into {len(chunk_ranges)} chunks for parallel silence detection...")

# Run silence detection in parallel
with Pool(processes=os.cpu_count()) as pool:
    results = list(tqdm(pool.imap_unordered(detect_speech_chunk, chunk_ranges), total=len(chunk_ranges), desc="Detecting Speech Segments"))

# Merge results from all chunks
non_silent_chunks = [segment for sublist in results for segment in sublist]

if not non_silent_chunks:
    print("No speech detected!")
    os.remove(converted_file)
    exit()

# Initialize Recognizer
recognizer = sr.Recognizer()

print(f"\nDetected {len(non_silent_chunks)} speech segments.")

with tqdm(total=len(non_silent_chunks), desc="Transcribing") as pbar:
    for i, (start, end) in enumerate(non_silent_chunks):
        chunk = audio[start:end]
        chunk_file = f"/tmp/chunk_{i}.wav"
        chunk.export(chunk_file, format="wav")

        with sr.AudioFile(chunk_file) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language="lv-LV")
        except sr.UnknownValueError:
            text = "[Unrecognized Speech]"
        except sr.RequestError as e:
            text = f"[Error: {e}]"

        print(f"[{start / 1000:.2f}s - {end / 1000:.2f}s] {text}")
        os.remove(chunk_file)  # Clean up
        pbar.update(1)

os.remove(converted_file)
print("\nTranscription Completed. Temporary WAV file deleted.")

