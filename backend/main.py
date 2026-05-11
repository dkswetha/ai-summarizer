from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.summarizer import summarize_text
from pypdf import PdfReader
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api")
def root():
    return {"message": "Summarizer API is running!"}

@app.post("/summarize/text")
async def summarize_from_text(text: str = Form(...)):
    try:
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e), "detail": "summarizer failed"}

@app.post("/summarize/pdf")
async def summarize_from_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    if not full_text.strip():
        return {"error": "Could not extract text from PDF."}
    summary = summarize_text(full_text)
    return {"summary": summary}

@app.get("/debug")
async def debug():
    import requests, os
    HF_TOKEN = os.environ.get("HF_TOKEN", "")
    response = requests.post(
        "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={
            "inputs": "The quick brown fox jumps over the lazy dog. This is a test sentence to check if the model is working correctly and returning a proper summary.",
            "options": {"wait_for_model": True}
        },
        timeout=120
    )
    return {
        "status_code": response.status_code,
        "response_text": response.text[:500],
        "token_set": bool(HF_TOKEN)
    }

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
