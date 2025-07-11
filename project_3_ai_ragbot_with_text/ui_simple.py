# Step 8 - Create an UI
import gradio as gr
from app import ragbot_text

if __name__ == "__main__":
  gr.ChatInterface(fn=ragbot_text, title="RAG from Text by HERE AND NOW AI",type="messages").launch()