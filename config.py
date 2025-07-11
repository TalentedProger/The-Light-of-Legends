import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OWM_API_KEY = os.getenv("OWM_API_KEY")