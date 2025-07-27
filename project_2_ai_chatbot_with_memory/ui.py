import gradio as gr # Import the Gradio library for building UIs
from app import ai_chatbot # Import the AI chatbot function from the app module
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
        fn=ai_chatbot, # Function to call for chatbot responses
        chatbot=gr.Chatbot(height=500, avatar_images=(None, brand_info['chatbot']['avatar']), type="messages"), # Configure chatbot display
        title=brand_info['organizationName'], # Set the title of the chat interface
        description=brand_info['slogan'], # Set the description/slogan
        type="messages", # Specify the message format
        examples=[
            ["What is AI?"],
            ["Can you explain machine learning?"],
            ["How does a neural network work?"],
            ["What is natural language processing?"],
            ["Tell me about computer vision."],
            ["How can I start learning AI?"],
            ["What is the difference between AI and machine learning?"],
            ["Can you give me an example of AI in everyday life?"],
            ["What are some fun AI projects I can try?"],
            ["How does AI help in healthcare?"],
            ["What is reinforcement learning?"],
            ["Can you explain deep learning?"],    
            ["What is the future of AI?"],
            ["How do I build my first AI model?"],
            ["What are some ethical considerations in AI?"],
            ["Can you explain supervised and unsupervised learning?"],
            ["What is the Turing Test?"],
            ["How does AI impact our daily lives?"],
            ["What are some popular AI tools and frameworks?"],
            ["How can AI can be used in education?"],
            ["What is the role of data in AI?"],
        ] # Example prompts for the chatbot
    )

# Launch the Gradio interface when the script is executed
if __name__ == "__main__":
    demo.launch(favicon_path=brand_info['logo']['favicon']) # Launch the demo with the specified favicon path