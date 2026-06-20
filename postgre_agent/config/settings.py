from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_MODEL = "gpt-4o-mini"

DATABASE_URI = os.getenv("DATABASE_URI")