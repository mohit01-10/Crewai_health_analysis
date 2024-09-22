import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
    MJ_APIKEY_PUBLIC = os.getenv('MJ_APIKEY_PUBLIC')
    MJ_APIKEY_PRIVATE = os.getenv('MJ_APIKEY_PRIVATE')
    EMAIL_FROM = os.getenv('EMAIL_FROM')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
  