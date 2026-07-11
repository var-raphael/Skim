import json
import httpx
from app.config import FIRECRAWL_API_KEY, FIRECRAWL_BASE_URL

MAX_PAGES = 10


def parse_pdf(file_bytes: bytes, filename: str) -> tuple[str, dict]:
    """
    Sends a PDF file to Firecrawl's /parse endpoint and returns
    the extracted markdown content, limited to the first MAX_PAGES pages.
    """
    url = f"{FIRECRAWL_BASE_URL}/parse"
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    }

    files = {
        "file": (filename, file_bytes, "application/pdf"),
    }

    options = {
        "formats": ["markdown"],
        "parsers": [{"type": "pdf", "maxPages": MAX_PAGES}],
    }
    data = {
        "options": json.dumps(options),
    }

    with httpx.Client(timeout=180.0) as client:
        response = client.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()

    doc_data = result.get("data", {})
    markdown = doc_data.get("markdown")
    metadata = doc_data.get("metadata", {})

    if not markdown:
        raise ValueError("Firecrawl did not return markdown content")

    return markdown, metadata
