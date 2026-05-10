import os
import requests

HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def summarize_text(text: str) -> str:
    text = text.strip()
    if len(text.split()) < 30:
        return "Text is too short to summarize!"

    max_chunk = 800
    words = text.split()
    chunks = [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]

    summaries = []
    for chunk in chunks:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={
                "inputs": chunk,
                "parameters": {
                    "max_length": 300,
                    "min_length": 100,
                    "do_sample": False
                }
            }
        )
        result = response.json()
        if isinstance(result, dict) and "error" in result:
            return "Model is loading on HuggingFace servers, please wait 20 seconds and try again."
        summaries.append(result[0]['summary_text'])

    return " ".join(summaries)
