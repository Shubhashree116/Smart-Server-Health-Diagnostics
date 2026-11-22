import json
import os

import requests


def get_ai_analysis(metrics, status):
    """Get an AI summary and recommendation, or return a safe fallback."""
    fallback = {
        "summary": (
            f"The system status is {status}. "
            "AI analysis is currently unavailable."
        ),
        "recommendation": (
            "Review the system metrics and monitor resource usage."
        ),
    }

    api_key = os.getenv("LLM_API_KEY")
    api_url = os.getenv("LLM_API_URL")
    model = os.getenv("LLM_MODEL")

    # Do not call the AI service when configuration is missing.
    if not api_key or not api_url or not model:
        return fallback

    prompt = f"""
You are a server health assistant.

Analyze these system metrics:
CPU utilization: {metrics["cpu_percent"]}%
Memory utilization: {metrics["memory_percent"]}%
Disk utilization: {metrics["disk_percent"]}%
Overall status: {status}

Return a JSON object with exactly two string fields:
1. "summary": a plain-English summary in 1-2 sentences.
2. "recommendation": one practical action. If status is HEALTHY,
confirm that no immediate action is needed.

Do not include Markdown formatting.
"""

    try:
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            },
            timeout=20,
        )

        response.raise_for_status()

        response_data = response.json()
        ai_text = response_data["choices"][0]["message"]["content"]
        ai_result = json.loads(ai_text)

        summary = ai_result.get("summary")
        recommendation = ai_result.get("recommendation")

        if not isinstance(summary, str) or not isinstance(recommendation, str):
            return fallback

        return {
            "summary": summary,
            "recommendation": recommendation,
        }

    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
        return fallback
