import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are a structured risk intelligence engine.

Return ONLY valid JSON.
No markdown.
No explanation.

JSON schema:
{
  "summary": "string (1-2 sentences)",
  "risk_score": integer (0-100),
  "severity": "low|medium|high",
  "identified_risks": ["string"],
  "recommended_actions": ["string"],
  "requires_escalation": true|false
}

Rules:
- If financial transfer, production deploy, credential exposure, deletion, legal liability appear → high severity.
- If operational uncertainty or policy ambiguity → medium.
- Informational only → low.
"""

def safe_json_extract(text):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found")
    return json.loads(text[start:end+1])

def analyze_with_ollama(text, model="llama3.1:8b"):
    payload = {
        "model": model,
        "prompt": SYSTEM_PROMPT + "\n\nText:\n" + text + "\n\nReturn JSON:",
        "stream": False,
        "options": {"temperature": 0.1}
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()
    output = r.json()["response"]

    return safe_json_extract(output)

def fallback_analysis(text):
    lower = text.lower()
    high_terms = ["transfer", "bank", "upi", "deploy", "production", "delete", "legal", "penalty", "breach"]
    medium_terms = ["delay", "issue", "unclear", "risk", "review"]

    if any(t in lower for t in high_terms):
        severity = "high"
        score = 80
    elif any(t in lower for t in medium_terms):
        severity = "medium"
        score = 50
    else:
        severity = "low"
        score = 20

    return {
        "summary": text[:120],
        "risk_score": score,
        "severity": severity,
        "identified_risks": ["Potential operational or compliance risk."],
        "recommended_actions": ["Review by responsible authority."],
        "requires_escalation": severity != "low"
    }