from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from summarizer import summarize_text
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
    import requests
    HF_TOKEN = os.environ.get("HF_TOKEN", "")
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
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

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
