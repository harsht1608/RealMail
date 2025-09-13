from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models import EmailRequest, EmailHistory
from database import emails_collection
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Allow frontend (Streamlit) requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Helper: AI generator
# ---------------------------
def generate_email(req: EmailRequest) -> str:
    prompt = f"""
    Write a {req.tone} email for {req.role} in {req.industry}.
    The main pain point: {req.pain_point}.
    Use the template style: {req.template}.
    Recipient email: {req.recipient}.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # you can change to pro model
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else "Could not generate email."

# ---------------------------
# Routes
# ---------------------------
@app.post("/generate-email")
async def generate_email_route(request: EmailRequest):
    generated = generate_email(request)
    return {"generated_email": generated}

@app.post("/save-email")
async def save_email(request: EmailHistory):
    doc = request.dict()
    doc["created_at"] = datetime.utcnow()
    await emails_collection.insert_one(doc)
    return {"message": "Email saved successfully"}

@app.get("/history")
async def get_history(user: str = Query(..., description="User's recipient email")):
    cursor = emails_collection.find({"recipient": user}).sort("created_at", -1)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results
