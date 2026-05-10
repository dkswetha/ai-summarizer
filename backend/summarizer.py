from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-6-6",
    device=-1
)

def summarize_text(text):
    text = text.strip()
    if len(text.split()) < 30:
        return "Text is too short to summarize!"

    max_chunk = 600
    words = text.split()
    chunks = [" ".join(words[i:i+max_chunk]) for i in range(0, len(words), max_chunk)]

    summaries = []
    for chunk in chunks:
        result = summarizer(chunk, max_length=200, min_length=60, do_sample=False, truncation=True)
        summaries.append(result[0]['summary_text'])

    return " ".join(summaries)
