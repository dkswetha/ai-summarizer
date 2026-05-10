import os
import requests
import time

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
        # Retry up to 3 times (model may be loading)
        for attempt in range(3):
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
                },
                timeout=60
            )

            # Empty response — model loading, wait and retry
            if response.status_code == 503 or len(response.text.strip()) == 0:
                time.sleep(10)
                continue

            # Parse response safely
            try:
                result = response.json()
            except Exception:
                time.sleep(10)
                continue

            # HuggingFace returns loading error as dict
            if isinstance(result, dict) and "error" in result:
                if "loading" in result["error"].lower():
                    time.sleep(15)
                    continue
                return f"API Error: {result['error']}"

            # Success
            if isinstance(result, list) and len(result) > 0:
                summaries.append(result[0]['summary_text'])
                break

        else:
            return "Model is still loading on HuggingFace servers. Please try again in 30 seconds."

    return " ".join(summaries)
