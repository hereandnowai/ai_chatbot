# Step 1 - Downloading & Installing necessary Libraries
# Step 2 - Importing the installed libraries
from openai import OpenAI
# from google.colab import userdata
from dotenv import load_dotenv
import os
import gradio as gr
import requests
import PyPDF2

# Step 3 - on COLAB Loading the API Key & base_url
# client = OpenAI(
#     api_key=userdata.get("GOOGLE_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# Step 3 - on VS CODE Loading the API Key & base_url
load_dotenv() # This loads the environment variables from .env
api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai", api_key=api_key)

# Step 4 - Getting the source file from github.com/hereandnowai
url = "https://raw.githubusercontent.com/hereandnowai/rag-workshop/main/pdfs/About_HERE_AND_NOW_AI.pdf"
response = requests.get(url)

# Step 5 - Save it to a file in the current working directory
PDF_FILE_NAME = "About_HERE_AND_NOW_AI.pdf"
PDF_PATH = os.path.join(os.path.dirname(__file__), PDF_FILE_NAME)

with open(PDF_PATH, "wb") as f:
    f.write(response.content)

# Step 6 - Read the PDF and extract text
try:
    with open(PDF_PATH, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        pdf_text_chunks = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pdf_text_chunks.append(page_text.strip())
        pdf_context = "\n".join(pdf_text_chunks) if pdf_text_chunks else "No text found in pdf"
except Exception as e:
    print(f"Error reading PDF: {e}")
    pdf_context = "Error extracting text from PDF"

# Step 7 - Function to the call the LLM
def get_response(query, history):  # history needed by ChatInterface
    prompt = f"Context from {PDF_PATH}:\n{pdf_context}\n\nQuestion: {query}\n\nAnswer based only on context:"
    response = client.chat.completions.create(
        model="gemini-1.5-flash-latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

print(get_response("who is the cto of here and now ai?", []))

# Step 8 - Create an UI
if __name__ == "__main__":
  gr.ChatInterface(fn=get_response, title="RAG from PDF by HERE AND NOW AI").launch()