# Step 1 - Downloading & Installing necessary Libraries
# Step 2 - Importing the installed libraries
from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr
import requests
import PyPDF2
import json

# Step 3 - on VS CODE Loading the API Key & base_url
load_dotenv() # This loads the environment variables from .env
api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-2.5-flash-lite"

client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai", api_key=api_key)

# Step 4 - Load branding data
branding_json_path = os.path.join(os.path.dirname(__file__), 'branding.json')
with open(branding_json_path, 'r') as f:
    branding = json.load(f)

brand = branding['brand']
# Step 5 - Getting the source file from github.com/hereandnowai
url = "https://raw.githubusercontent.com/hereandnowai/rag-workshop/main/pdfs/About_HERE_AND_NOW_AI.pdf"
response = requests.get(url)

# Step 6 - Save it to a file in the current working directory
PDF_FILE_NAME = "About_HERE_AND_NOW_AI.pdf"
PDF_PATH = os.path.join(os.path.dirname(__file__), PDF_FILE_NAME)

with open(PDF_PATH, "wb") as f:
    f.write(response.content)

# Step 7 - Read the PDF and extract text
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

# Step 8 - Function to the call the LLM
def get_response(message, history):  # history needed by ChatInterface
    prompt = f"Context from {PDF_PATH}:\n{pdf_context}\n\nQuestion: {message}\n\nAnswer based only on context:"
    messages = [{"role":"system", "content":prompt}]
    messages.extend(history)
    messages.append({"role":"user", "content":message})
    response = client.chat.completions.create(model=model, messages=messages)
    ai_response = response.choices[0].message.content
    return ai_response

# Step 9 - Create a modern UI
if __name__ == "__main__":
    css = """
    .gradio-container {
        background-color: #008080; /* Teal Green */
        color: #FFFF00; /* Yellow text */
    }
    #sidebar {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }
    #sidebar h2, #sidebar em, #sidebar h3 {
        color: #008080; /* Teal Green */
    }
    #chatbot {
        height: 600px;
        overflow: auto;
    }
    .gr-image {
        border-radius: 10px;
    }
    """
    with gr.Blocks(theme=gr.themes.Monochrome(primary_hue="yellow", secondary_hue="teal"), css=css) as app:
        with gr.Row():
            with gr.Column(scale=1, elem_id="sidebar"):
                gr.Image(brand['logo']['favicon'], height=150, width=150)
                gr.Markdown(f"## {brand['organizationName']}")
                gr.Markdown(f"*{brand['slogan']}*")
                gr.Markdown("---")
                gr.Markdown("### Connect with us")
                for name, link in brand['socialMedia'].items():
                    gr.Markdown(f"[{name.capitalize()}]({link})")

            with gr.Column(scale=3):
                gr.ChatInterface(
                    fn=get_response,
                    chatbot=gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        avatar_images=(None, brand['chatbot']['avatar']),
                        type="messages"
                    ),
                    type="messages",
                    title="AI Assistant",
                    description="Ask me anything about HERE AND NOW AI based on the provided document.",
                    examples=[
                        ["Where is HERE AND NOW AI?"],
                        ["What is the mission of HERE AND NOW AI?"],
                        ["Who is the CTO of HERE AND NOW AI?"],
                        ["What is Madame Deepti?"],
                        ["What services does HERE AND NOW AI provide?"]
                    ]
                )
    app.launch()