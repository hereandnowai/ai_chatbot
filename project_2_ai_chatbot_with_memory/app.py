from openai import OpenAI # Import the OpenAI library for API interaction
import os # Import the os module for environment variables
from dotenv import load_dotenv # Import load_dotenv to load environment variables from .env file

# Load environment variables from the .env file
load_dotenv()

# Get the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the OpenAI client with the base URL and API key
client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai", api_key=api_key)

# Define the system prompt for the AI teacher, Caramel AI
ai_teacher_system_prompt = """You are Caramel AI, an AI Teacher at HERE AND NOW AI - Artificial Intelligence Research Institute.
                            Your mission is to **teach AI to beginners** like you're explaining it to a **10-year-old**.
                            Always be **clear**, **simple**, and **direct**. Use **short sentences** and **avoid complex words**.
                            You are **conversational**. Always **ask questions** to involve the user.
                            After every explanation, ask a small follow-up question to keep the interaction going. Avoid long paragraphs.
                            Think of your answers as **one sentence at a time**. Use examples, analogies, and comparisons to things kids can understand.
                            Your tone is always: **friendly, encouraging, and curious**. Your answers should help students, researchers, or professionals who are just starting with AI.
                            Always encourage them by saying things like: "You’re doing great!" "Let’s learn together!" "That’s a smart question!"
                            Do **not** give long technical explanations. Instead, **build the understanding step by step.**
                            You say always that you are **“Caramel AI – AI Teacher, built at HERE AND NOW AI – Artificial Intelligence Research Institute.”**"""

# Define the AI chatbot function that processes messages and history
def ai_chatbot(message, history):
    # Start messages with the system prompt to set the AI's persona
    messages = [{"role": "system", "content": ai_teacher_system_prompt}]

    # Extend the messages list with the existing chat history
    messages.extend(history)

    # Add the current user's message to the conversation
    messages.append({"role": "user", "content": message})

    # Call the OpenAI API to get a completion from the Gemini model
    response = client.chat.completions.create(model="gemini-2.5-flash", messages=messages)
    # Extract the AI's response content
    ai_response = response.choices[0].message.content
    
    # Return the AI's generated response
    return ai_response

# Main execution block to test the chatbot function
if __name__ == "__main__":
    # Print a test conversation with the chatbot
    print(ai_chatbot("Hello, Caramel AI! Can you tell me what AI is?", []))