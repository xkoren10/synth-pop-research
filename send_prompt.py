import requests
import os
from dotenv import load_dotenv

load_dotenv()

GPT4V_KEY = os.getenv('GPT4V_KEY')
GPT4V_ENDPOINT = os.getenv('GPT4V_ENDPOINT')

headers = {
    "Content-Type": "application/json",
    "Authorization": GPT4V_KEY,
}

# Initialize the conversation history
conversation_history = []


def send_prompt(content: str, temperature: float):
    global conversation_history

    # Append the new user message to the conversation history
    conversation_history.append({"role": "user", "content": content})

    # Payload for the request
    payload = {
        "messages": conversation_history,
        "temperature": temperature,
        "max_tokens": 1200,
    }
    response = requests.Response

    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
        response_data = response.json()

        # Get the assistant's reply and add it to the conversation history
        assistant_message = response_data["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message
    except Exception as e:
        print(response.status_code if response else f"No response - {response.text}")
        print(e)
        return None




