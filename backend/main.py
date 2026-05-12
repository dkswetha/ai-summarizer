from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from summarizer import summarize_text
from pypdf import PdfReader
import io
import os
import requests

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

@app.get("/debug")
async def debug():
    HF_TOKEN = os.environ.get("HF_TOKEN", "")
    try:
        response = requests.post(
            "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": "The sun is a star at the center of our solar system. It provides energy for life on Earth through light and heat. Without the sun life would not exist on our planet.",
                "options": {"wait_for_model": True}
            },
            timeout=120
        )
        return {
            "status_code": response.status_code,
            "response": response.text[:500],
            "token_present": bool(HF_TOKEN),
            "token_starts_with": HF_TOKEN[:7] if HF_TOKEN else "MISSING"
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/summarize/text")
async def summarize_from_text(text: str = Form(...)):
    try:
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

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

# StaticFiles MUST be last — it catches everything including API routes if mounted too early
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
