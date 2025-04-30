# 📄 Bestand: feedback_analyzer.py
# Evalueert GPT-antwoord op mute-aanwijzingen of actiebare inzichten

def extract_actions(gpt_response: str) -> dict:
    lowered = gpt_response.lower()
    return {
        "mute_strategy": any(keyword in lowered for keyword in ["uitschakelen", "deactiveren", "niet betrouwbaar", "te risicovol"]),
        "mute_reason": gpt_response
    }
