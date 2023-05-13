import requests
from typing import Dict, List

def chatgpt_call(prompt: str, token: str, model: str = "gpt-3.5-turbo"):
    response = requests.post(
        "https://openai-api.meetings.bio/api/openai/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    breakpoint()
    if response.ok:
        content = response.json()["choices"][0]["message"]["content"]
        print(content)
        return content

def generate_trip(plan: Dict[str, str], preferences: List[str], token: str, model: str = "gpt-3.5-turbo"):
    prompt = """
    """

    return chatgpt_call(prompt, token, model)