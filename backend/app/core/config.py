from dotenv import load_dotenv
import os

load_dotenv()

# GitHub Configuration
GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional: for higher rate limits (5000/hr vs 60/hr)

# AI API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
