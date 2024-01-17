import speech_recognition as sr

def recognize_language(audio_file):
    r = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    
    try:
        text = r.recognize_google(audio, language='en-US')  # Attempt to recognize English
        return 'en'
    except sr.UnknownValueError:
        pass
    
    try:
        text = r.recognize_google(audio, language='zh-CN')  # Attempt to recognize Chinese
        return 'cn'
    except sr.UnknownValueError:
        pass
    
    try:
        text = r.recognize_google(audio, language='ja-JP')  # Attempt to recognize Japanese
        return 'jp'
    except sr.UnknownValueError:
        pass
    
    try:
        text = r.recognize_google(audio, language='th-TH')  # Attempt to recognize Thai
        return 'th'
    except sr.UnknownValueError:
        pass
    
    return 'unknown'  # If none of the languages were recognized

if __name__ == "__main__":
    audio_file = 'path_to_your_audio_file.wav'  # Replace with your audio file path
    language = recognize_language(audio_file)
    
    if language == 'en':
        print("This is an English audio.")
    elif language == 'cn':
        print("This is a Chinese audio.")
    elif language == 'jp':
        print("This is a Japanese audio.")
    elif language == 'th':
        print("This is a Thai audio.")
    else:
        print("Language could not be determined.")
