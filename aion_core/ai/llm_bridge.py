# 📄 Bestand: llm_bridge.py
# GPT-router met fallback van GPT-4 naar GPT-3.5 bij model errors

import os
import requests
from openai import OpenAI, OpenAIError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_ENDPOINT_URL = os.getenv("LLM_ENDPOINT_URL")  # optioneel lokaal model

def ask_llm(prompt: str, use_local=False) -> str:
    if use_local and LLM_ENDPOINT_URL:
        response = requests.post(
            LLM_ENDPOINT_URL,
            json={"prompt": prompt, "temperature": 0.3, "max_tokens": 500},
            timeout=20
        )
        return response.json().get("response", "Geen antwoord ontvangen van lokaal model.")

    elif OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Je bent een slimme trading-assistent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content

        except OpenAIError as e:
            if "model" in str(e).lower() or "access" in str(e).lower():
                print("⚠️ GPT-4 niet beschikbaar — fallback naar GPT-3.5-turbo")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Je bent een slimme trading-assistent."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            else:
                raise e

    else:
        raise EnvironmentError("Geen geldige LLM configuratie gevonden.")
