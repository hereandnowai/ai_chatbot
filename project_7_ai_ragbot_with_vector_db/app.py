import gradio as gr
import os, requests
from openai import OpenAI
import PyPDF2
import numpy as np
import faiss
import pickle
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
embedding_model = SentenceTransformer('BAAI/bge-small-en-v1.5')

PDF_FILE_NAME = "About_HERE_AND_NOW_AI.pdf"
PDFS_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
PDF_PATH = os.path.join(PDFS_DIR, PDF_FILE_NAME)
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store.pkl")

def get_embeddings(text): return np.array(embedding_model.encode(text))

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text(): text += page.extract_text()
    return text

def load_or_create_vector_store():
    if os.path.exists(VECTOR_STORE_PATH):
        with open(VECTOR_STORE_PATH, "rb") as f: return pickle.load(f)
    
    os.makedirs(PDFS_DIR, exist_ok=True)
    if not os.path.exists(PDF_PATH):
        url = "https://raw.githubusercontent.com/hereandnowai/rag-workshop/main/pdfs/About_HERE_AND_NOW_AI.pdf"
        with open(PDF_PATH, "wb") as f: f.write(requests.get(url).content)
    
    text = read_pdf(PDF_PATH)
    chunks = [text[i:i + 200] for i in range(0, len(text), 200)]
    embeddings = np.array([get_embeddings(chunk) for chunk in chunks]).astype('float32')
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    with open(VECTOR_STORE_PATH, "wb") as f: pickle.dump((chunks, index), f)
    return chunks, index

def search_similar_chunk(query, chunks, index, top_k=1):
    query_embedding = get_embeddings(query).astype('float32')
    D, I = index.search(np.expand_dims(query_embedding, axis=0), top_k)
    return [chunks[i] for i in I[0]]

chunks, index = load_or_create_vector_store()

def get_response(query, history):
    context = "\n\n".join(search_similar_chunk(query, chunks, index, top_k=3))
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer based only on the provided context. If the information is not in the context, state that you cannot answer based on the provided information."
    response = client.chat.completions.create(model="gemini-2.5-flash", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

if __name__ == "__main__":
    gr.ChatInterface(
        fn=get_response,
        title="RAG from Vector DB",
        type="messages",
        examples=[["CTO"],["CEO"],["CMO"],["Contact Info"]]
        ).launch()