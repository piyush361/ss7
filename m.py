import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

model = tf.keras.models.load_model("sms_fraud_model.h5")

df = pd.read_csv("latest.csv", sep=',')

max_words = 5000
max_len = 50
tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
df["clean_message"] = df["clean_message"].astype(str)
tokenizer.fit_on_texts(df["clean_message"]) 

fraud_patterns = {
    "phishing": "Phishing scams involve fraudsters impersonating legitimate entities like banks, government agencies, or well-known companies...",
    "lottery": "Lottery scams falsely inform recipients that they have won a significant prize, often in a lottery they never entered...",
    "bank_fraud": "Bank fraud scams trick recipients into revealing their banking details by pretending to be from a legitimate financial institution...",
    "fake_job": "Fake job scams offer high-paying opportunities with minimal effort, luring job seekers with promises of flexible work hours and easy income...",
    "investment_scam": "Investment scams promise guaranteed returns with little to no risk, often using fake success stories and endorsements...",
    "romance_scam": "Romance scams involve fraudsters creating fake online identities to establish relationships with victims, gaining their trust over time...",
    "subscription_fraud": "Subscription fraud messages claim that the recipient has been signed up for a premium service and will be charged unless they cancel immediately...",
    "tech_support_scam": "Tech support scams claim that the recipient’s device is infected with a virus or has a serious security issue...",
    "fake_shipping": "Fake shipping scams target online shoppers by sending messages claiming that a package delivery is pending or has been delayed due to unpaid fees...",
    "charity_scam": "Charity scams exploit people's generosity by sending fraudulent donation requests for disaster relief, medical emergencies, or humanitarian aid..."
}

vectorizer = TfidfVectorizer()
pattern_texts = list(fraud_patterns.values())
tfidf_matrix = vectorizer.fit_transform(pattern_texts)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SMSRequest(BaseModel):
    message: str

@app.post("/analyze")
def analyze_sms(request: SMSRequest):
    sample_sms_seq = tokenizer.texts_to_sequences([request.message])
    sample_sms_padded = pad_sequences(sample_sms_seq, maxlen=max_len, padding='post')
    prediction = model.predict(sample_sms_padded)[0][0]
    
    severity = "low"
    if prediction > 0.7:
        severity = "high"
    elif prediction > 0.4:
        severity = "medium"
    
    response_text = "This message seems safe."
    if severity == "medium":
        response_text = "This message may be suspicious. Please be cautious."
    elif severity == "high":
        response_text = "Warning! This message is likely fraudulent. Do not engage."
    
    input_tfidf = vectorizer.transform([request.message])
    similarities = cosine_similarity(input_tfidf, tfidf_matrix).flatten()
    matched_pattern = list(fraud_patterns.keys())[np.argmax(similarities)]
    
    fraud_pattern_distribution = {pattern: float(similarities[i]) for i, pattern in enumerate(fraud_patterns.keys())}
    
    return {
        "response": response_text,
        "severity": severity,
        "spam_probability": float(prediction),
        "pattern_match": matched_pattern,
        "fraud_pattern_distribution": fraud_pattern_distribution
    }
