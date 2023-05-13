from dotenv import load_dotenv
import os

from src.utils.chatgpt_call import chatgpt_call

prompt = "Write Haiku about Dragonhack"

load_dotenv()

token = os.getenv("CHATGPT_KEY")

chatgpt_call(prompt, token)