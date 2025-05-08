
import os
from dotenv.main import load_dotenv


load_dotenv()

API_URL = os.getenv("API_URL")
META_FOLDER = os.getenv("META_FOLDER")

class WordpressComponent:
      def __init__(self):
            pass