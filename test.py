from dotenv import load_dotenv
import os
import json

from src.utils.chatgpt_call import generate_trip

prompt = "Write Haiku about Dragonhack"

load_dotenv()

token = os.getenv("CHATGPT_KEY")

#chatgpt_call(prompt, token)

plan = {
    "19.2.-20.2.": "London",
    "21.2.": "Rome"
}

preferences = ["museums", "theater", "sport", "nature"]

resp = generate_trip(plan, preferences, token)
breakpoint()

try:
    r_dict = json.loads(resp.replace("`", ""))
    print(r_dict)
except:
    pass