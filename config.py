import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///my_database.db")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# OpenAI configuration (future use)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Application settings
APP_NAME = "Intelligent DB Query Agent"
VERSION = "0.1.0"