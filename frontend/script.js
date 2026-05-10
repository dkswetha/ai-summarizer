const API = "https://ai-summarizer-zkj2.onrender.com/";

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('text-section').style.display = tab === 'text' ? 'block' : 'none';
    document.getElementById('pdf-section').style.display = tab === 'pdf' ? 'block' : 'none';
    event.target.classList.add('active');
}

async function summarizeText() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) return alert("Please enter some text!");

    showLoading();
    try {
        const formData = new FormData();
        formData.append("text", text);

        const res = await fetch(`${API}/summarize/text`, { method: "POST", body: formData });
        const data = await res.json();
        showResult(data.summary || data.error);
    } catch (err) {
        showResult("Error: Could not connect to backend. Is the server running?");
    }
}

async function summarizePDF() {
    const file = document.getElementById('pdfInput').files[0];
    if (!file) return alert("Please select a PDF file!");

    showLoading();
    try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch(`${API}/summarize/pdf`, { method: "POST", body: formData });
        const data = await res.json();
        showResult(data.summary || data.error);
    } catch (err) {
        showResult("Error: Could not connect to backend. Is the server running?");
    }
}

function showLoading() {
    document.getElementById('output-box').style.display = 'block';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('summaryText').textContent = '';
}

function showResult(text) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('summaryText').textContent = text;
}
