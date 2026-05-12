import os
import requests
import time

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def summarize_text(text: str) -> str:
    HF_TOKEN = os.environ.get("HF_TOKEN", "")  # read token fresh every call

    text = text.strip()
    if len(text.split()) < 30:
        return "Text is too short to summarize!"

    max_chunk = 800
    words = text.split()
    chunks = [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]

    summaries = []
    for chunk in chunks:
        for attempt in range(5):
            try:
                response = requests.post(
                    API_URL,
                    headers={"Authorization": f"Bearer {HF_TOKEN}"},
                    json={
                        "inputs": chunk,
                        "parameters": {
                            "max_length": 300,
                            "min_length": 80,
                            "do_sample": False
                        },
                        "options": {
                            "wait_for_model": True
                        }
                    },
                    timeout=120
                )

                if len(response.text.strip()) == 0:
                    time.sleep(10)
                    continue

                result = response.json()

                if isinstance(result, dict) and "error" in result:
                    time.sleep(20)
                    continue

                if isinstance(result, list) and len(result) > 0:
                    summaries.append(result[0]['summary_text'])
                    break

            except Exception as e:
                time.sleep(10)
                continue
        else:
            summaries.append("[Could not summarize this section]")

    return " ".join(summaries)
