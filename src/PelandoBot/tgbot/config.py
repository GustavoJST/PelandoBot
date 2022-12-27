import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("API_KEY")
HOST = os.getenv("HOST")
# TODO: Remove this later.
DEV_CHAT_ID = os.getenv("DEV_CHAT_ID")