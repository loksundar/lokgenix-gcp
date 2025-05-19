import gradio as gr
from gradio_client import Client
from gradio_client.exceptions import AppError # Corrected: Import AppError as suggested by the traceback
import os

# --- Configuration for your Hugging Face API ---
# !!! IMPORTANT: Replace placeholder token with your actual Hugging Face API Token !!!
HF_SPACE_NAME = "loksundar000/LokGenix"


HF_API_TOKEN = os.getenv("HF_API_TOKEN", "YOUR_HUGGING_FACE_API_TOKEN_HERE") # Fallback if not set
# --- Function to call your Hugging Face API using gradio_client ---
def call_LokGenix_api(user_message, history):
    """
    Sends the user's message to the LokGenix Hugging Face Gradio App and returns the response.
    """
    print(f"User message: {user_message}")

    if not HF_API_TOKEN or HF_API_TOKEN == "YOUR_HUGGING_FACE_API_TOKEN_HERE":
        return "ERROR: Hugging Face API Token is not configured. Please set HF_API_TOKEN in the code."
    if not HF_SPACE_NAME:
        return "ERROR: Hugging Face Space Name is not configured."

    try:
        client = Client(HF_SPACE_NAME, hf_token=HF_API_TOKEN)
        
        print(f"Sending request to Hugging Face Space: {HF_SPACE_NAME} using gradio_client")
        
        result = client.predict(
            text_input=user_message,
            api_name="/handle_submission"
        )
        
        api_response = result
        if not isinstance(api_response, str):
            api_response = str(api_response) 
            
        print(f"API Response: {api_response}")
        return api_response

    except AppError as e: # Corrected: Catch AppError instead of APIError
        print(f"Gradio Client AppError: {e}") # Changed log message to reflect AppError
        return f"Error communicating with the LokGenix API (AppError): {e}"
    except Exception as e:
        print(f"An unexpected error occurred with gradio_client: {e}")
        print(f"Exception type: {type(e).__name__}")
        return f"An unexpected error occurred: {e}"

# --- Create the Gradio Chat Interface ---
LokGenix_chat_interface = gr.ChatInterface(
    fn=call_LokGenix_api,
    title="LokGenix",
    description="Gen AI agent leveraging a RAG-based knowledge system to tap into Lok Sundar’s work history, projects, and expertise—ready to answer any question about his professional journey.",
    chatbot=gr.Chatbot(
        height=600,
        show_copy_button=True,
        type="messages"
    ),
    textbox=gr.Textbox(placeholder="Type your question for LokSundar here...", container=False, scale=7),
    theme="soft",
    examples=[
        ["Who are you?"],
        ["Tell me about Data Engineering Project's you have worked on?"],
        ["Tell me about Yourself?"],
    ],
    cache_examples=False,
)

# --- Launch the Gradio App ---
if __name__ == "__main__":
    if not HF_API_TOKEN or HF_API_TOKEN == "YOUR_HUGGING_FACE_API_TOKEN_HERE":
        print("CRITICAL ERROR: HF_API_TOKEN is not set. Please edit the script to include your token.")
        print("The application will likely fail to connect to your Hugging Face Space.")
    
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Gradio on 0.0.0.0:{port}")
    LokGenix_chat_interface.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False  # optional, and prevents Gradio from trying to open a tunnel
    )