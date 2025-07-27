import gradio as gr # Import the Gradio library for building UIs
from app import ragbot_text # Import the ragbot_text function from the app module
import json # Import the json library for handling JSON data
import os # Import the os library for interacting with the operating system

# Load branding data from the branding.json file
with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'branding.json'))) as f:
    brand_info = json.load(f)['brand']

# Create the Gradio interface using gr.Blocks for custom layout
with gr.Blocks(theme='default', title=brand_info['organizationName']) as demo:
    # Embed the logo using HTML for centering and styling
    gr.HTML(f'''<div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="{brand_info['logo']['title']}" alt="{brand_info['organizationName']} Logo" style="height: 100px;">
        </div>''')
    # Create the chat interface with specified functions and branding
    gr.ChatInterface(
        fn=ragbot_text, # Function to call for chatbot responses
        chatbot=gr.Chatbot(height=500, avatar_images=(None, brand_info['chatbot']['avatar']), type="messages"), # Configure chatbot display
        title=brand_info['organizationName'], # Set the title of the chat interface
        description=brand_info['slogan'], # Set the description/slogan
        type="messages", # Specify the message format
        examples=[
            ["What is HERE AND NOW AI?"],
            ["What is the mission of HERE AND NOW AI?"],
            ["Who is Madame Deepti?"],
            ["What courses does HERE AND NOW AI offer?"],
            ["Who is the CTO of HERE AND NOW AI?"],
            ["What is the 'Business Analytics with AI' course?"],
            ["What is the 'Full-Stack AI Developer Program'?"],
            ["What is the contact information for HERE AND NOW AI?"],
        ] # Example prompts for the chatbot
    )

# Launch the Gradio interface when the script is executed
if __name__ == "__main__":
    demo.launch(favicon_path=brand_info['logo']['favicon']) # Launch the demo with the specified favicon path