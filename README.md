# Ethiopian History RAG

This project is a notebook-based retrieval-augmented generation experiment over a local plain-text copy of the Wikipedia article [History of Ethiopia](https://en.wikipedia.org/wiki/History_of_Ethiopia). The notebook strips whitespace, splits the text into four-sentence chunks with a one-sentence overlap, embeds them with `all-MiniLM-L6-v2`, stores the vectors and text in a persistent local ChromaDB collection, retrieves the three nearest chunks for a question, and asks Groq's `openai/gpt-oss-120b` model to answer from that context or refuse when the context does not support an answer. The source text and local database are not included in this repository.

## Pipeline

```text
ethiopian_history.txt
  -> split into sentences; trim and discard empty sentences
  -> four-sentence chunks (one-sentence overlap)
  -> all-MiniLM-L6-v2 embeddings
  -> persistent ChromaDB at ./chroma_db, collection "israel_history"

question
  -> embed with the same model
  -> retrieve the three nearest chunks
  -> send question and retrieved context to Groq (openai/gpt-oss-120b)
  -> context-grounded answer or refusal
```

## Setup (Windows PowerShell)

1. Install Python and the VS Code Python and Jupyter extensions.
2. From the project directory, create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the packages imported by the notebook:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create your local environment file and add your own Groq API key to it:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   Replace `your_key_here` in `.env` with your key. Do not commit `.env`.

5. Supply your own text file at the project root named `ethiopian_history.txt`. The notebook reads that exact path. The data used for this experiment was the Wikipedia article “History of Ethiopia” (CC BY-SA); the text file is deliberately not included here.
6. Open `rag_experiment.ipynb` in VS Code, select the `.venv` Python kernel, and run its cells in order from top to bottom.

## Notebook Cell Order

1. Import dependencies and load `ethiopian_history.txt`.
2. Define sentence chunking and create chunks.
3. Load `all-MiniLM-L6-v2` and embed the chunks.
4. Create or open the persistent ChromaDB collection and store the chunks and embeddings.
5. Retrieve context and ask the Groq model a sample question.
6. Run the data-hygiene checks, seven in-scope questions, and three out-of-scope refusal checks. This cell makes model API calls.
7. Run retrieval and answer spot checks.

## Example

Question: “Who led Ethiopia to victory at the Battle of Adwa?”

A context-supported answer should identify Menelik; the notebook's evaluation checks for the keyword `menelik`.

## Informal evaluation

In the notebook's saved seven-question test, retrieval hit rate was 6/7 and answer accuracy was 5/7. The two answer-check failures were keyword-matching artifacts; the displayed answers were not wrong. All 3/3 out-of-scope questions were correctly refused. This sample is tiny and is not a broad performance measure.

## Known limitations

- Some chunks exceed the embedding model's 256-token limit, so the tail is not embedded.
- The current chunking code uses a one-sentence overlap, rather than no overlap. Names and related context can still be separated when they occur farther apart than a chunk can contain.
- The pipeline has been tested on one document only.
- The free API tier has rate limits.
