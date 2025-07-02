# config/settings.py
import os
from dotenv import load_dotenv
load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
