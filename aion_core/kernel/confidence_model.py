def compute_confidence(setup: dict) -> tuple[float, str]:
    # Placeholder confidence logic
    score = 0.0
    reasons = []

    if setup.get("has_bos") and setup.get("has_fvg"):
        score += 0.4
        reasons.append("confluence: BOS + FVG")

    if setup.get("bias") == "bullish":
        score += 0.2
        reasons.append("bias: bullish")

    if setup.get("rsi") and setup["rsi"] < 30:
        score += 0.2
        reasons.append("RSI oversold")

    score = min(score, 1.0)
    reason_text = ", ".join(reasons) or "no confluence"
    return round(score, 2), reason_text
