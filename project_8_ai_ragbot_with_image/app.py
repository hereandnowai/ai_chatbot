# 1. Install and Import the libraries
from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr
import base64

# 2. Setup API Key & OpenAI Client
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 3. Function to get image description
def get_image_description(image_path):
    if image_path is None:
        return "Please upload an image."

    # Read and encode the image
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # 4. Call the LLM
    response = client.chat.completions.create(
        model="gemini-1.5-flash-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the image in detail."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content

# 5. Create and Launch Gradio UI
if __name__ == "__main__":
    gr.Interface(
        fn=get_image_description,
        inputs=gr.Image(type="filepath", label="Upload Image"),
        outputs=gr.Textbox(label="Image Description"),
        title="AI Image Describer by HERE AND NOW AI",
        description="Upload an image (PNG, JPG, JPEG) and the AI will describe it for you.",
    ).launch()