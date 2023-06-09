from dotenv import load_dotenv
import os
import json

from src.utils.chatgpt_call import generate_trip
from src.utils.city_api import get_city_coordinates

prompt = "Write Haiku about Dragonhack"

load_dotenv()

token = os.getenv("CHATGPT_KEY")
city_token = os.getenv("CITY_API_TOKEN")

#chatgpt_call(prompt, token)

# coords = get_city_coordinates("Ljubljana", city_token)
# print(coords)
plan = [
    {
        "date": "19.2.",
        "location": "London"
    },
    {
        "date": "21.2.",
        "location": "Rome"
    }
]

preferences = ["museums", "theater", "sport", "nature"]

resp = generate_trip(plan, preferences, token)

try:
    r_dict = json.loads(resp.replace("`", ""))
    print(r_dict)
except:
    pass

