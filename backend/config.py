import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.load_environment_variables()
        

    def load_environment_variables(self):
        """Load environment variables from a .env file."""
        load_dotenv()

    def get_gemini_api_key(self):
        """Get the Gemini API key from environment variables."""
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
        return self.gemini_api_key

