# Simple Python RAG – Cedarline Systems

Reads the two documents, chunks them (120 tokens, 20 overlap), embeds them with
`all-MiniLM-L6-v2`, stores them in a persistent ChromaDB, retrieves the top 2
chunks for a question and asks an AI model to answer only from that context.

## Project layout
```
RAG_Exercise/
├── Documents/                  the two supplied .txt files
├── chroma_db/                  created automatically on first run (keep it for submission)
├── config.py                   all settings (chunk size, model, questions...)
├── rag_utils.py                shared helper functions
├── task1_read_tokenize.py      Task 1
├── task2_chunk_embed.py        Task 2
├── task3_store_search.py       Task 3
├── task4_ai_answer.py          Task 4
├── main.py                     runs all four tasks
├── requirements.txt
└── .env.example                copy to .env and add your API key
```

## Setup in PyCharm
1. File > Open > select the `RAG_Exercise` folder.
2. Settings > Project > Python Interpreter > Add Interpreter > New virtualenv (Python 3.10–3.12).
3. Open PyCharm's Terminal and run:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`, set `AI_PROVIDER` (anthropic or openai) and paste your key.

The first run downloads the tiktoken encoding and the embedding model (~90 MB), so it needs internet.

## Run
Right-click a file > Run, or in the terminal:
```
python task1_read_tokenize.py
python task2_chunk_embed.py
python task3_store_search.py "Which days must employees work from the office?"
python task4_ai_answer.py            # all 5 test questions
python main.py                       # everything at once
```

## Screenshots to submit
- Chunks: output of `task2_chunk_embed.py`
- ChromaDB search: output of `task3_store_search.py`
- 2 AI answers: output of `task4_ai_answer.py` (include the travel-allowance
  question, which should return "I cannot find the answer in the provided documents.")
