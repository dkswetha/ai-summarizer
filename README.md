# AI Text Summarizer
 
A full-stack web application that summarizes long text and PDF documents using AI. Built with HTML/CSS/JS frontend and Python FastAPI backend, powered by the HuggingFace Inference API with `facebook/bart-large-cnn`.
 
  **Live Demo:** [[https://ai-summarizer-xmc2.onrender.com]](https://ai-summarizer-xmc2.onrender.com)]
 
---
 
## Project Structure
 
```
summarizer-app/
│
├── requirements.txt          ← Root requirements (used by Render)
├── start.sh                  ← Render start script
├── .python-version           ← Python 3.11.0
├── .gitignore
│
├── backend/
│   ├── main.py               ← FastAPI server & API routes
│   └── summarizer.py         ← HuggingFace API integration
│
└── frontend/
    ├── index.html            ← Main UI
    ├── style.css             ← Styling
    └── script.js             ← Frontend logic & API calls
```
 
---
 
## Tech Stack
 
| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python FastAPI |
| AI Model | HuggingFace Inference API (`facebook/bart-large-cnn`) |
| PDF Reading | `pypdf` (pure Python) |
| Server | Uvicorn |
| Hosting | Render (backend + frontend) |
 
---
 
## Features
 
- Paste any long text and get an AI-generated summary
- Upload a PDF file and summarize its contents
-  Powered by BART Large CNN — state-of-the-art summarization model
- Fully deployed and accessible from any browser
---
 
## Live Deployment (Render)
 
The app is deployed on Render with the following configuration:
 
| Setting | Value |
|---|---|
| Runtime | Python 3.11 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `bash start.sh` |
| Environment Variable | `HF_TOKEN` = your HuggingFace token |
 
---
 
## Run Locally
 
### Prerequisites
- Python 3.11
- A free HuggingFace account and API token
### Step 1 — Clone the repo
```bash
git clone https://github.com/yourusername/summarizer-app.git
cd summarizer-app
```
 
### Step 2 — Create and activate virtual environment
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```
 
### Step 3 — Install dependencies
```powershell
pip install fastapi uvicorn pypdf aiofiles python-multipart requests python-dotenv
```
 
### Step 4 — Set up environment variable
 
Create a `.env` file inside the `backend/` folder:
```
HF_TOKEN=your_huggingface_token_here
```
 
### Step 5 — Add dotenv loading to `backend/main.py`
 
Add these 2 lines at the very top of `main.py` for local development:
```python
from dotenv import load_dotenv
load_dotenv()
```
 
### Step 6 — Run the server
```powershell
cd backend
uvicorn main:app --reload
```
 
### Step 7 — Open the app
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
 
---
 
## API Endpoints
 
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check — confirms server is running |
| `GET` | `/api` | Returns API status message |
| `POST` | `/summarize/text` | Accepts plain text, returns summary |
| `POST` | `/summarize/pdf` | Accepts PDF upload, returns summary |
| `GET` | `/debug` | Tests HuggingFace API connection |
 
---

 
