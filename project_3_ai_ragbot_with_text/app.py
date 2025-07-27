import os # Import the os module for interacting with the operating system
from openai import OpenAI # Import the OpenAI library for API interaction
from dotenv import load_dotenv # Import load_dotenv to load environment variables
import requests # Import requests for making HTTP requests

# Load environment variables from the .env file
load_dotenv()

# Get the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
# Raise an error if the API key is not found
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not found.")

# Initialize the OpenAI client with the base URL and API key
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai", api_key=api_key)

# Define the URL for the text context file on GitHub
url = "https://raw.githubusercontent.com/hereandnowai/vac/refs/heads/master/prospectus-context.txt"
# Make an HTTP GET request to fetch the content
response = requests.get(url)

# Determine the script's directory and define the local file path for saving the text
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "profile-of-hereandnowai.txt")
# Write the fetched content to the local file
with open(file_path, "wb") as f:
    f.write(response.content)

# Set the path to the text file for reading
text_path = file_path
# Attempt to read the text content from the file
try:
    with open(text_path, "r", encoding="utf-8") as file:
        # Read lines, strip whitespace, and join them into a single string
        text_lines = file.readlines()
        text_context = "\n".join([line.strip() for line in text_lines if line.strip()])
# Handle exceptions during file reading
except Exception as e:
    print(f"Error reading TXT file: {e}")
    text_context = "Error extracting text from TXT file."

# Define the RAG chatbot function
def ragbot_text(message, history):
    # Define the system prompt, incorporating the fetched text context
    system_prompt = f"You are Caramel AI an ai assistant built by HERE AND NOW AI. Answer the user's questions based only on the following context: \n\n{text_context}"
    # Initialize messages with the system prompt
    messages = [{"role":"system", "content":system_prompt}]
    # Extend messages with the chat history
    messages.extend(history)
    # Add the current user message
    messages.append({"role":"user", "content":message})
    # Call the OpenAI API to get a response from the Gemini model
    response = client.chat.completions.create(model="gemini-2.0-flash",messages=messages)
    # Return the AI's response content
    return response.choices[0].message.content