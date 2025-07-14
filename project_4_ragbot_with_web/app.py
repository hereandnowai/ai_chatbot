# Step 2 - Importing the installed libraries
from openai import OpenAI
# from google.colab import userdata
from dotenv import load_dotenv
import os
import gradio as gr
import requests
from bs4 import BeautifulSoup

# Step 3 - Loading the API Key & base_url
# client = OpenAI(api_key=userdata.get("GOOGLE_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# Step 3 - for vs code
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
client = OpenAI(api_key=api_key, base_url=base_url)

# Step 4 - Getting the source file from github.com/hereandnowai
WEBSITE_URL = "https://hereandnowai.github.io/vac/"

response = requests.get(WEBSITE_URL,
                        headers={'User-Agent': 'Mozilla/5.0'},
                        timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')
website_context = soup.body.get_text(separator='\n',
                                     strip=True) if soup.body else "no info found"

# Step 5 - Function to the call the LLM
def get_response(query, history):  # history needed by ChatInterface
    prompt = f"Context from {WEBSITE_URL}:\n{website_context}\n\nQuestion: {query}\n\nAnswer based only on context:"
    response = client.chat.completions.create(
        model="gemini-1.5-flash-latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

print(get_response("who is the cto of here and now ai?", []))

# Step 6 - Create an UI
if __name__ == "__main__":
  gr.ChatInterface(fn=get_response, title="RAG from web by HERE AND NOW AI").launch()