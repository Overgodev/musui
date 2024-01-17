import pygame
import sounddevice as sd
import numpy as np
import os
import time
import datetime

# Function to play a sound
def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Function to record audio and cache it
def record_and_cache_audio(cache_folder, duration):
    sample_rate = 44100  # You can adjust this as needed
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()
    
    # Create a unique filename using the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    cache_filename = f"voice_{len(os.listdir(cache_folder)) + 1}_{duration}s_{current_datetime}.npy"
    
    cache_path = os.path.join(cache_folder, cache_filename)
    np.save(cache_path, recording)
    return cache_filename

# Function to delete a cached file
def delete_cached_file(cache_folder, cache_filename):
    cache_path = os.path.join(cache_folder, cache_filename)
    
    try:
        os.remove(cache_path)
        print(f"Deleted cached file: {cache_path}")
    except FileNotFoundError:
        print(f"File not found: {cache_path}")

# Function to detect a whisper (based on audio intensity)
def is_whisper(audio_signal, whisper_threshold):
    audio_intensity = np.max(np.abs(audio_signal))
    return audio_intensity < whisper_threshold

if __name__ == "__main__":
    sound_file = "your_sound_file.mp3"  # Replace with your sound file path
    cache_folder = "audio_cache"
    duration = 5  # Recording duration in seconds
    whisper_threshold = 500  # Adjust this threshold as needed
    
    # Play the sound
    play_sound(sound_file)
    
    # Record audio and cache it, and get the cached filename
    os.makedirs(cache_folder, exist_ok=True)
    cached_filename = record_and_cache_audio(cache_folder, duration)
    print(f"Audio recorded and cached as: {cached_filename}")
    
    # Monitor for a whisper to trigger deletion
    while True:
        audio_input = sd.rec(1024, channels=2, dtype=np.int16)
        sd.wait()
        
        if is_whisper(audio_input, whisper_threshold):
            delete_cached_file(cache_folder, cached_filename)
            break
