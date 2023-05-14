import requests
import json
from typing import Dict, List

def _chatgpt_call(prompt: str, token: str, model: str = "gpt-3.5-turbo") -> str:
    """The function takes prompt and token for the chatgpt and returns the response of the query as
    a string."""

    response = requests.post(
        "https://openai-api.meetings.bio/api/openai/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    if response.ok:
        content = response.json()["choices"][0]["message"]["content"]
        
        print(len(content.split()))
        
        return content

def generate_trip(plan: List[Dict], preferences: List[str], token: str,
                  model: str = "gpt-3.5-turbo") -> Dict[str, List[str]]:
    """Returns the schedule by days for the entire trip with 3 recommendations for each day. The
    return format is a dict or string (if format is incorrect)"""
    
    prompt = f"""
    Plan a trip with the information provided the text delimited by triple backticks. The 
    information will be in a list of json structures with field dates and location which 
    represents the where a person will be on the specified date. The output should a json 
    structure wth one key plan that has a value list of json objects of the same structure as the 
    input with an additional field activities with up to three 
    suggestions (in one sentence) for that a person could do on that location. You will also be 
    provided with a list of interests which can be taken into account when choosing activities. 
    The interests are listed inside <> list interests in response. Do not include backticks, 
    newlines or tabs in response.

    ```{str(plan)}```

    <{", ".join(preferences)}>
    """

    print(len(prompt.split()))

    resp = _chatgpt_call(prompt, token, model)

    try:
        r_dict = json.loads(resp.replace("`", ""))
        return r_dict
    except:
        print("Incorrect format of api response", flush=True)
        return resp