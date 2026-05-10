from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    text = text.strip()

    if len(text.split()) < 30:
        return "Text is too short to summarize!"

    max_chunk = 1000
    words = text.split()
    chunks = [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]

    summaries = []
    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=300,   # ← increased from 150
            min_length=100,   # ← increased from 30
            do_sample=False
        )
        summaries.append(result[0]['summary_text'])

    return " ".join(summaries)