import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1.0)  

text = "Hello! This is an automated message to inform you about a suspicious transaction on your account."
engine.save_to_file(text, 'fraud_alert.mp3') 
engine.runAndWait()

print("Audio saved as fraud_alert.mp3")
