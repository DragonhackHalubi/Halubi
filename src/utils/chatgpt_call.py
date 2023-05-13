import requests
from typing import Dict, List

def _chatgpt_call(prompt: str, token: str, model: str = "gpt-3.5-turbo"):
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
        print(len(content.split()))
        print(content)
        return content

def generate_trip(plan: Dict[str, str], preferences: List[str], token: str,
                  model: str = "gpt-3.5-turbo"):
    prompt = f"""
    Plan a trip with the information provided the text delimited by triple backticks. The 
    information will be in json structure where the keys are gonna be dates or range of dates 
    and the value will be the location where we are gonna be that day. The output should be in 
    json format where the keys are dates and the the values are up to three suggestions for that 
    day where each suggestion is one sentence long. You will also be provided with a list of 
    interests which can be taken into account when choosing activities. The interests are listed 
    inside <> list interests in response. Do not include backticks in response.

    ```{str(plan)}```

    <{", ".join(preferences)}>
    """

    print(len(prompt.split()))

    return _chatgpt_call(prompt, token, model)