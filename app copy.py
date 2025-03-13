import chainlit as cl
import requests

# OpenAI-compatible API endpoint
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"

# Store model name globally
MODEL_NAME = "llama3.2:1b"

# Configure the avatar once at the module level
@cl.set_avatar
def avatar_setup():
    # Return the URL or path to your avatar image
    return "https://blessl.in/assets/img/logo/logo.png"

@cl.on_chat_start
async def start():
    # Use the global model name
    await cl.Message(content=f"Welcome to Blessl Ai Chat! I am {MODEL_NAME}. How can I assist you?").send()

@cl.on_message
async def on_message(message):
    # OpenAI-compatible format
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": message.content}
        ]
    }

    try:
        response = requests.post(OLLAMA_URL, json=data).json()

        # Print response for debugging
        print("Ollama API Response:", response)

        # Parse response from OpenAI-compatible API
        if "choices" in response and len(response["choices"]) > 0 and "message" in response["choices"][0]:
            await cl.Message(content=response["choices"][0]["message"]["content"]).send()
        else:
            await cl.Message(content="Error: Invalid response from Ollama.").send()

    except Exception as e:
        print("Error:", e)
        await cl.Message(content="Error communicating with Ollama.").send()