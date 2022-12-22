# any configuration should be stored here
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("API_KEY")
HOST = os.getenv("HOST")