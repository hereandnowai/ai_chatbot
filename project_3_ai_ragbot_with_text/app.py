# Step 2 - Importing the installed libraries
from openai import OpenAI
# from google.colab import userdata
from dotenv import load_dotenv
import os
import gradio as gr
import requests

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

# Step 3 - on colab - Loading the API Key & base_url
# client = OpenAI(
#     api_key=userdata.get("GOOGLE_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# on vs code
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai", api_key=api_key)

# Step 4 - Getting the source file from github.com/hereandnowai
url = "https://raw.githubusercontent.com/hereandnowai/vac/refs/heads/master/prospectus-context.txt"
response = requests.get(url)

# Step 5 - Save it to a file in the current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "profile-of-hereandnowai.txt")
with open(file_path, "wb") as f:
  f.write(response.content)

# Step 6 - Fetch the text
text_path = file_path
try:
  with open(text_path, "r", encoding="utf-8") as file:
    text_lines = file.readlines()
    text_lines = [line.strip() for line in text_lines if line.strip()]
    text_context = "\n".join(text_lines) if text_lines else "No text found in TXT file."
except Exception as e:
  print(f"Error reading TXT file: {e}")
  text_context = "Error extracting text from TXT file."

# Step 7 - Function to the call the LLM
def ragbot_text(message, history):  # history needed by ChatInterface
    # System prompt that defines the context for the AI
    system_prompt = f"You are Caramel AI an ai assistant built by HERE AND NOW AI. Answer the user's questions based only on the following context: \n\n{text_context}"
    
    # Create the list of messages to send to the API
    messages = [{"role":"system", "content":system_prompt}]
    messages.extend(history)
    messages.append({"role":"user", "content":message})
    response = client.chat.completions.create(model="gemini-2.0-flash",messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    print(ragbot_text("who is the cto of here and now ai?", []))