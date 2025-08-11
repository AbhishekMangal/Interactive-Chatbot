<<<<<<< HEAD
# 📚 ChatBot for Website & PDF (RAG-based)

A **Retrieval-Augmented Generation (RAG)** application that lets users upload **PDF documents** or provide **website URLs**, and then interactively ask questions about their content.  
This chatbot uses **Gemini 2.5 Flash LLM** and **Google Generative AI Embeddings**, with **FAISS** as the vector database for fast, semantic search.

---

## 🚀 Features

- **PDF Upload & URL Input** → Extracts text from PDFs or web pages.
- **RAG-based Querying** → Uses FAISS vector database for efficient retrieval.
- **Gemini 2.5 Flash LLM** → Fast and cost-efficient large language model.
- **Google Generative AI Embeddings** → Converts content into high-quality embeddings for semantic search.
- **Interactive Chat Interface** → Ask natural language questions and get context-aware answers.
- **FastAPI Backend** → Lightweight and high-performance API layer.
- **LangChain Integration** → Handles retrieval, chunking, and LLM orchestration.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.10 |
| **Framework** | FastAPI |
| **LLM** | [Gemini 2.5 Flash](https://ai.google.dev/gemini-api) |
| **Embeddings** | [Google Generative AI Embeddings](https://ai.google.dev) |
| **Vector Store** | [FAISS](https://github.com/facebookresearch/faiss) |
| **Orchestration** | [LangChain](https://www.langchain.com/) |
| **PDF Loader** | PyPDFLoader |
| **Web Loader** | UnstructuredURLLoader |

---

## 📂 Project Structure

```
chatbot/
│
├── src/
│   ├── helper.py           # Core RAG logic
│   ├── chatbot.py          # Main chatbot API
│   ├── utils.py            # Utility functions
│
├── static/
│   ├── docs/               # Uploaded PDFs
│   ├── css/                # Styles
│
├── templates/              # HTML templates
├── requirements.txt
├── README.md
└── main.py                 # FastAPI entry point
```

---

## ⚡ Quick Start

### 1️⃣ Create a Virtual Environment
```bash
conda create -n chatBot python=3.10 -y
conda activate chatBot
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add API Keys  
You will need:
- **Google API Key** (for Gemini & Embeddings)  
Store it in an `.env` file:
```env
GOOGLE_API_KEY=your_api_key_here
```

### 4️⃣ Run the Application
```bash
uvicorn main:app --reload
```
Visit **http://127.0.0.1:8000** in your browser.

---

## 📌 How It Works

1. **Upload PDF or Enter URL**  
   The document is loaded using **PyPDFLoader** or **UnstructuredURLLoader**.
2. **Chunk & Embed**  
   Content is split into smaller chunks and converted into embeddings using **Google Generative AI Embeddings**.
3. **Store in FAISS**  
   Embeddings are stored in **FAISS** for fast similarity search.
4. **Ask Questions**  
   Your query is embedded and matched with relevant chunks from the database.
5. **Generate Answer**  
   **Gemini 2.5 Flash** LLM generates a concise, context-aware response.

---

## 📸 Demo

*(Insert screenshot or GIF of chatbot in action here)*

---

## 🔗 Useful Links

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS GitHub Repo](https://github.com/facebookresearch/faiss)
- [Google Generative AI API](https://ai.google.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 🧑‍💻 Author

**Abhishek Mangal**  
📧 Email: *your-email@example.com*  
💼 LinkedIn: *[Your LinkedIn Profile](https://linkedin.com/in/yourprofile)*

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======
# Interactive-Chatbot
Interactive RAG-based chatbot using FastAPI, LangChain, FAISS, and Gemini 2.5 Flash that lets users upload PDFs or URLs and ask context-aware questions. If an answer isn’t found in the documents, it clearly informs the user and provides a general-knowledge response.
>>>>>>> 5067d4a67b0dc66d2eb67377b28e1b1048e03e9c
