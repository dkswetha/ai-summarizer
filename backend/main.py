from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from summarizer import summarize_text
from pypdf import PdfReader
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize/text")
async def summarize_from_text(text: str = Form(...)):
    summary = summarize_text(text)
    return {"summary": summary}

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

# Serve frontend files — add this at the very end
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")