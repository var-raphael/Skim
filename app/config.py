import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v2"
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MISTRAL_MODEL = "mistral-large-latest"

if not FIRECRAWL_API_KEY:
    raise RuntimeError("Missing FIRECRAWL_API_KEY in .env")
if not MISTRAL_API_KEY:
    raise RuntimeError("Missing MISTRAL_API_KEY in .env")
