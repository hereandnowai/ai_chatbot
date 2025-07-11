import gradio as gr
from app import ai_chatbot

chat_interface = gr.ChatInterface(
    fn=ai_chatbot,
    title="Caramel AI - AI Teacher built by HERE AND NOW AI",
    description="Ask Caramel AI anything about AI! Caramel AI is here to teach you AI in a simple and friendly way. Let's learn together!",
    theme="default",
    flagging_mode="never",
    type="messages",
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
        ["How can AI be used in education?"],
        ["What is the role of data in AI?"],
    ]
)

if __name__ == "__main__":
    chat_interface.launch()