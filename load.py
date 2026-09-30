from sentence_transformers import SentenceTransformer
import numpy as np

with open("notes.txt", encoding="utf-8") as f:
    text = f.read()

chunks = text.split("\n\n")

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(chunks)


def retrieve(question, k=2):
    q_vec = model.encode([question])[0]
    scores = [np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v)) for v in vectors]
    top = np.argsort(scores)[::-1][:k]
    return [chunks[i] for i in top]


def build_prompt(question, k=2):
    context = "\n\n".join(retrieve(question, k))
    return f"""Answer the question using only the context below.

Context:
{context}

Question: {question}
Answer:"""


# --- Gemini call (switched off for now) ---
# from google import genai
# client = genai.Client()
# prompt = build_prompt("How much does a latte cost?")
# response = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
# print(response.text)


# --- Retrieval eval ---
eval_set = [
    ("How much coffee per 250 ml of water for pour-over?", 0),
    ("How long does coffee steep in a French press?", 1),
    ("What pressure is used to make espresso?", 2),
    ("Which coffee species has more caffeine?", 3),
    ("Why does my coffee taste sour?", 4),
    ("How should I store coffee beans?", 5),
]

hits = 0
for q, expected in eval_set:
    top = retrieve(q, k=2)
    ok = chunks[expected] in top
    hits += ok
    print(ok, "|", q)

print(f"retrieval accuracy: {hits}/{len(eval_set)}")

