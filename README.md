# ask-your-docs

Retrieval-augmented question answering over a local text file. Ask a question in plain language and get an answer grounded in your document, or a refusal when the document doesn't contain the answer.

## How it works

```text
text file
  -> split into sentences
  -> four-sentence chunks with a one-sentence overlap
  -> embed with all-MiniLM-L6-v2 (sentence-transformers)
  -> store in a persistent ChromaDB collection

question
  -> embed with the same model
  -> retrieve the 3 nearest chunks
  -> Groq LLM (openai/gpt-oss-120b) answers using only those chunks
  -> answer, or "I cannot answer this based on the provided text."
```

## Stack

- Embeddings: `all-MiniLM-L6-v2` via sentence-transformers
- Vector store: ChromaDB (local, persistent)
- LLM: Groq API, `openai/gpt-oss-120b`

## Setup (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
```

2. Install the dependencies:

```powershell
   python -m pip install -r requirements.txt
```

3. Add your own Groq API key:

```powershell
   Copy-Item .env.example .env
   notepad .env
```

   Replace `your_key_here` with your key. Never commit `.env`.

4. Put a plain-text file in the project root. The notebook reads `ethiopian_history.txt` by default, so either use that name or change the filename in the loading cell.
5. Open `rag_experiment.ipynb`, select the `.venv` kernel, and run the cells in order.

## Evaluation

I tested the pipeline with a small set of questions over one test document, the Wikipedia article "History of Ethiopia" (CC BY-SA, not included in this repo):

| Check | Result |
|---|---|
| Retrieval hit rate (7 in-scope questions) | 6/7 |
| Answer accuracy, keyword match (same 7) | 5/7 |
| Out-of-scope questions correctly refused | 3/3 |

The two answer-check failures were keyword-matching artifacts, not wrong answers. The test set is tiny, so treat these numbers as a sanity check and not a benchmark.

## Known limitations

- Some chunks are longer than the embedding model's 256-token limit, so the end of those chunks is never embedded.
- A one-sentence overlap doesn't always keep a name and the sentences that refer to it in the same chunk.
- Only tested on one document.
- The free Groq tier has rate limits.
