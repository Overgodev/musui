import os
import time
import openai
from audioutils import play_sound, record_and_cache_audio, delete_cached_file, is_whisper
from speech_recognition import recognize_language
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def send_to_gpt(cached_filename, language):
    # Load the cached audio file
    cache_folder = "audio_cache"
    audio_path = os.path.join(cache_folder, cached_filename)
    with open(audio_path, "rb") as file:
        audio_content = file.read()

    # Create a prompt based on the detected language
    if language == "en":
        prompt = f"Translate the following English audio into text:\n{audio_content.decode('utf-8')}"
    elif language == "cn":
        prompt = f"Translate the following Chinese audio into text:\n{audio_content.decode('utf-8')}"
    elif language == "jp":
        prompt = f"Translate the following Japanese audio into text:\n{audio_content.decode('utf-8')}"
    elif language == "th":
        prompt = f"Translate the following Thai audio into text:\n{audio_content.decode('utf-8')}"
    else:
        prompt = "Language could not be determined."

    # Send the prompt to GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
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

    # Check if the audio is a whisper or in a specific language
    language = recognize_language(os.path.join(cache_folder, cached_filename))
    if is_whisper(cached_filename, whisper_threshold):
        print("Whisper detected! Deleting cached audio.")
        delete_cached_file(cache_folder, cached_filename)
    else:
        print(f"Language detected: {language}")

        # Send cached file and detected language to GPT-3
        send_to_gpt(cached_filename, language)

        # Convert voice to text using Google Web Speech API and update the cached audio
        recognized_text = voice_to_text(cached_filename)
        if recognized_text:
            print("Updating cached audio with recognized text.")
        else:
            print("No recognized text to update.")
