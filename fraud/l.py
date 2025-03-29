import speech_recognition as sr
from pydub import AudioSegment

audio = AudioSegment.from_mp3("fraud_alert_hindi.mp3")
audio.export("converted.wav", format="wav")

r = sr.Recognizer()

with sr.AudioFile("converted.wav") as source:
    audio_data = r.record(source)

try:
    text = r.recognize_google(audio_data, language="hi")  # Use 'hi' for Hindi, 'mr' for Marathi
    print("Extracted Text:", text)
except sr.UnknownValueError:
    print("Could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results; {e}")
