# 🎯 CV-Job Matching Platform

AI-powered CV ranking and job matching using **RAG** (Retrieval-Augmented Generation) + Local LLMs.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0+-009688.svg)

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai) installed
- Node.js 18+ (for frontend)

### Setup

```bash
# 1. Install Ollama model
ollama pull mistral:7b-instruct

# 2. Backend
cd CV-Job-matching
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Start API
python run_api.py
# API: http://localhost:8000/docs

# 4. Frontend (optional)
cd frontend
npm install
npm run dev
# UI: http://localhost:5173
```

---

## ✨ Key Features

- 🤖 **Local LLM**: mistral:7b-instruct via Ollama
- ⚡ **Fast**: 60% faster with asyncio + transformer embeddings (20x faster)
- 💾 **Efficient**: Uses 52% less RAM (4.5GB vs 9.4GB)
- 🔍 **RAG**: Smart chunking + retrieval (70% fewer tokens)
- 📊 **Batch Processing**: Rank multiple CVs concurrently
- 🎨 **Modern UI**: React + TypeScript frontend

**Performance:** Single CV in 5-6 seconds | 9 CVs in ~45 seconds

---

## 📡 Basic Usage

### API

```bash
# Match single CV
curl -X POST "http://localhost:8000/match" \
  -F "file=@cv.pdf" \
  -F "job_description=Python developer with FastAPI"
```

### Python

```python
import asyncio
from app.pipeline import run_pipeline_rag_async

async def match():
    result = await run_pipeline_rag_async("cv.pdf", "job description")
    print(f"Score: {result['final_score']}")

asyncio.run(match())
```

### Frontend

1. Go to http://localhost:5173
2. Upload CV(s)
3. Enter job description
4. Click "Match"

---

## 🛠️ Tech Stack

**Backend:** FastAPI + Ollama (mistral:7b-instruct) + sentence-transformers + asyncio  
**Frontend:** React 19 + TypeScript + Vite  
**Embeddings:** all-MiniLM-L6-v2 (90MB, 20x faster than Ollama)

---

## 📁 Project Structure

```
CV-Job-matching/
├── app/
│   ├── pipeline.py          # Main async pipeline
│   ├── agents/              # CV/JD parsing + scoring
│   ├── embedding/           # Transformer embeddings + RAG
│   ├── api/routes/          # FastAPI endpoints
│   └── utils/               # RAG + caching
├── requirements.txt
└── run_api.py

frontend/
├── src/components/          # React UI
└── src/services/api.ts      # API client
```

---

## 🚀 Performance

| Metric | Before | After V2 | Improvement |
|--------|--------|----------|-------------|
| Time (1 CV) | 14.5s | **5.4s** | 63% faster |
| RAM | 9.4GB | **4.5GB** | 52% less |
| Embeddings | 6s | **0.3s** | 20x faster |

**Key Optimizations:**
- Asyncio replaces threads (2-3x faster I/O)
- Direct transformers (no Ollama embeddings overhead)
- Single model (saves 5GB RAM)

---

## 📚 Documentation

- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Advanced Usage:** See `API_USAGE.md` in CV-Job-matching/
- **RAG Details:** Check `test_rag.py` for implementation

---

## 🐛 Troubleshooting

```bash
# Ollama not running?
ollama serve

# Port in use?
python run_api.py --port 8001

# Clear cache
curl -X POST "http://localhost:8000/cache/clear"
```

---

## 🤝 Contributing

1. Fork repo
2. Create branch: `git checkout -b feature/name`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/name`
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file

---

**Version 2.0 Highlights:**
- ⚡ Asyncio (60% faster)
- 🔢 Transformer embeddings (20x faster)
- 🤖 Single model (52% less RAM)
- 📊 Comprehensive logging

