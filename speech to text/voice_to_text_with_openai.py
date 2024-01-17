import os
import time
import openai
from audioutils import play_sound, record_and_cache_audio, delete_cached_file, is_whisper

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def send_to_gpt(audio_filename):
    # Load the cached audio file
    cache_folder = "audio_cache"
    audio_path = os.path.join(cache_folder, audio_filename)
    with open(audio_path, "rb") as file:
        audio_content = file.read()

    # Use GPT-3 for both language detection and speech-to-text conversion
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Detect the language and convert the following audio to text:\n{audio_content.decode('utf-8')}",
        max_tokens=50  # Adjust as needed
    )

    # Extract and print the GPT-3 response
    gpt3_text = response.choices[0].text
    print("GPT-3 Response:")
    print(gpt3_text)

    # Update the cached audio with the recognized text
    updated_audio_content = f"Original audio content:\n{audio_content.decode('utf-8')}\nRecognized text:\n{gpt3_text}".encode('utf-8')
    with open(audio_path, "wb") as file:
        file.write(updated_audio_content)

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
        # Send cached file to GPT-3 for speech-to-text conversion and language detection
        send_to_gpt(cached_filename)
