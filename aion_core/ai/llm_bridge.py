import os
import requests
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # via Render environment variables
LLM_ENDPOINT_URL = os.getenv("LLM_ENDPOINT_URL")  # optioneel: lokaal model

def ask_llm(prompt: str, use_local=False) -> str:
    if use_local and LLM_ENDPOINT_URL:
        response = requests.post(
            LLM_ENDPOINT_URL,
            json={"prompt": prompt, "temperature": 0.3, "max_tokens": 500},
            timeout=20
        )
        return response.json().get("response", "Geen antwoord ontvangen van lokaal model.")

    elif OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Je bent een slimme trading-assistent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return chat_response["choices"][0]["message"]["content"]

    else:
        raise EnvironmentError("Geen geldige LLM configuratie gevonden.")
