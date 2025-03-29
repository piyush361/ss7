from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
from pydub import AudioSegment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processed_text = None  # Global variable to store processed text



@app.get("/tdc")
def read_text():
    if processed_text:
        return {"text": processed_text}
    return {"message": "No processed text available. Please process audio first."}