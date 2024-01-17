import os
import time
import speech_recognition as sr
from audioutils import play_sound, record_and_cache_audio, delete_cached_file, is_whisper

def voice_to_text(cached_filename):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the cached audio file
    cache_folder = "audio_cache"
    audio_path = os.path.join(cache_folder, cached_filename)

    # Recognize the audio and convert it to text using Google Web Speech API
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized text:", text)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
    return ""

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

    # Check if the audio is a whisper or in a specific language using Google Web Speech API
    if is_whisper(cached_filename, whisper_threshold):
        print("Whisper detected! Deleting cached audio.")
        delete_cached_file(cache_folder, cached_filename)
    else:
        # Convert voice to text using Google Web Speech API
        recognized_text = voice_to_text(cached_filename)
        if recognized_text:
            print("Recognized text:", recognized_text)
        else:
            print("No recognized text.")
