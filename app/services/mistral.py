import httpx
from app.config import MISTRAL_API_KEY, MISTRAL_BASE_URL, MISTRAL_MODEL


def summarize_text(text: str, user_prompt: str) -> str:
    """
    Sends parsed PDF text + the user's instruction to Mistral
    and returns a page-by-page summary.
    """
    url = f"{MISTRAL_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = (
        "You are Skim, an assistant that summarizes documents for "
        "students and teachers. Summarize the given document content "
        "clearly, page by page where possible. Follow the user's "
        "specific request precisely."
    )

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"User request: {user_prompt}\n\nDocument content:\n{text}",
            },
        ],
        "temperature": 0.3,
    }

    with httpx.Client(timeout=90.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"]
