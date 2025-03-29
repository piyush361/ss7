from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for all origins (modify as needed for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store received reports
reports = []
total = 0  # Initialize total packet count

@app.post("/report")
def receive_report(report: dict):
    reports.append(report)
    return {"message": "Report received"}

@app.get("/reports")
def get_reports():
    return reports

@app.post("/count")
def update_count():
    global total
    total += 1
    return {"message": "Count updated"}

@app.get("/count")
def get_count():
    return {"total_packets": total}  # Return JSON response
