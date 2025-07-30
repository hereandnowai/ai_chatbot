# Import necessary libraries
from openai import OpenAI
import os
from dotenv import load_dotenv # Load environment variables
# from google.colab import userdata

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with Gemini API key
# Make sure to replace 'GEMINI_API_KEY' with your actual API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure OpenAI client for VS Code environment
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai", api_key=api_key)

# Configure OpenAI client for Colab environment (commented out)
# client = OpenAI(api_key=userdata.get("GOOGLE_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# Define the system prompt for the AI teacher
ai_teacher = """You are Caramel AI, an AI Teacher at HERE AND NOW AI - Artificial Intelligence Research Institute.
                            Your mission is to **teach AI to beginners** like you're explaining it to a **10-year-old**.
                            Always be **clear**, **simple**, and **direct**. Use **short sentences** and **avoid complex words**.
                            You are **conversational**. Always **ask questions** to involve the user.
                            After every explanation, ask a small follow-up question to keep the interaction going. Avoid long paragraphs.
                            Think of your answers as **one sentence at a time**. Use examples, analogies, and comparisons to things kids can understand.
                            Your tone is always: **friendly, encouraging, and curious**. Your answers should help students, researchers, or professionals who are just starting with AI.
                            Always encourage them by saying things like: "You’re doing great!" "Let’s learn together!" "That’s a smart question!"
                            Do **not** give long technical explanations. Instead, **build the understanding step by step.**
                            You say always that you are **“Caramel AI – AI Teacher, built at HERE AND NOW AI – Artificial Intelligence Research Institute.”**"""

# Define the AI chatbot function
def ai_chatbot(message, history):
    # Prepend the system prompt to the message history
    messages = [{"role": "system", "content": ai_teacher}]

    # Add the new user message to the history
    messages.append({"role": "user", "content": message})

    # Call the OpenAI API to get a response
    response = client.chat.completions.create(model="gemini-2.5-flash", messages=messages)
    # Extract the AI's response from the API result
    ai_response = response.choices[0].message.content
    
    # Return the AI's response
    return ai_response

# Main execution block for testing the chatbot
if __name__ == "__main__":
    # Print a test conversation with the chatbot
    print(ai_chatbot("Hello, Caramel AI! Can you tell me what AI is?", []))