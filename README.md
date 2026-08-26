# 🎬 AI Video Assistant

Turn any meeting recording, audio file, or YouTube video into a searchable,
chattable knowledge base — automatically transcribed, summarized, and broken
down into action items, key decisions, and open questions.

---

## ✨ Features

- 🔊 **Flexible input** — point it at a local audio/video file or paste a YouTube URL
- 📝 **Automatic transcription** — multi-language support (English, Hinglish, and more)
- 🏷️ **Auto-generated title** for every session
- 📋 **Concise summary** of the full conversation
- ✅ **Action items**, 🔑 **key decisions**, and ❓ **open questions** extracted automatically
- 💬 **Chat with your meeting** — ask follow-up questions grounded in the transcript via RAG (Retrieval-Augmented Generation)
- 🖥️ **Two ways to use it** — a polished Streamlit web UI or a lightweight CLI





## 🏗️ How it works

```
Input (file / YouTube URL)
        │
        ▼
 process_input()          →  chunks the audio
        │
        ▼
 transcribe_all()         →  speech-to-text transcript
        │
        ├──▶ generate_title()          → session title
        ├──▶ summarize()               → summary
        ├──▶ extract_action_items()    → ✅ action items
        ├──▶ extract_key_decisions()   → 🔑 decisions
        ├──▶ extract_questions()       → ❓ open questions
        └──▶ build_rag_chain()         → indexed for Q&A
                    │
                    ▼
            ask_question() (chat loop)
```

---

## 📂 Project structure

```
.
├── streamlit_app.py         # Streamlit web UI
├── main.py                  # CLI entry point
├── core/
│   ├── transcriber.py        # transcribe_all()
│   ├── summarizer.py         # summarize(), generate_title()
│   ├── extractor.py          # extract_action_items(), extract_key_decisions(), extract_questions()
│   └── rag_engine.py         # build_rag_chain(), load_rag_chain(), ask_question()
├── utils/
│   └── audio_processor.py    # process_input()
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (see `.env.example`):

```env
OPENAI_API_KEY=your_api_key_here
# add any other keys your transcriber / summarizer / RAG engine needs
```

### 4. Run it

**Web UI (recommended):**

```bash
streamlit run streamlit_app.py
```

**CLI:**

```bash
python main.py
```

You'll be prompted for a file path or YouTube URL and a language, then you can
chat with the meeting directly from the terminal.

---

## 🧰 Tech stack

- [Streamlit](https://streamlit.io/) — web UI
- Python 3.10+
- Speech-to-text transcription engine (see `core/transcriber.py`)
- LLM-powered summarization & extraction
- RAG (Retrieval-Augmented Generation) for meeting Q&A

---

## 🗺️ Roadmap

- [ ] Export summary/action items to PDF or Markdown
- [ ] Multi-speaker diarization
- [ ] Persistent storage for past sessions
- [ ] Support additional languages

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the
[issues page](../../issues) or open a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
