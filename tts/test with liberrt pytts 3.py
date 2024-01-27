import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Text to be converted to speech
text = "Hello, this is a simple example of Text-to-Speech in Python."

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Convert text to speech
engine.say(text)

# Wait for the speech to finish
engine.runAndWait()
