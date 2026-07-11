# Skim

A small AI tool that summarizes PDFs page-by-page based on what you tell it to look for — built for students and teachers who need to skim dense material fast.

Upload a PDF, describe what you want extracted (e.g. *"extract the top points on electrolysis"* or *"summarize each chapter"*), and Skim returns a clear, structured summary.

**Live demo:** _https://skim.onrender.com_

---

## How it works

1. User uploads a PDF and types a prompt describing what they want extracted
2. Flask backend sends the PDF to **Firecrawl's `/parse`** endpoint, capped at the first 10 pages, and gets back clean markdown
3. The parsed text + user's prompt are sent to **Mistral** for summarization
4. The summary is returned to the frontend and displayed
5. The frontend saves the summary to `localStorage` so past summaries persist across sessions — no server-side storage involved

---

## Stack

- **Frontend:** single-file HTML + Tailwind CSS (via CDN) + vanilla JavaScript — no build step, no framework
- **Backend:** Python + Flask
- **PDF parsing:** [Firecrawl](https://firecrawl.dev) `/parse` endpoint
- **Summarization:** [Mistral AI](https://mistral.ai) chat completions
- **Hosting:** Render (backend + static frontend served together)

The frontend deliberately skips a JS framework here — this project sits alongside other portfolio projects built with Next.js/TypeScript, so this one leans into plain HTML/CSS/JS to show range and comfort working without tooling.

---

## Running locally

### Backend

```bash
cd skim
python -m venv venv
source venv/bin/activate          # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
FIRECRAWL_API_KEY=fc-your-key-here
MISTRAL_API_KEY=your-mistral-key-here
```

Run the server:

```bash
python -m app.main
```

Visit `http://localhost:5000` — Flask serves the frontend directly from `static/index.html`.

---

## Project structure

```
skim/
├── app/
│   ├── main.py              # Flask app + routes
│   ├── config.py            # env vars / settings
│   └── services/
│       ├── firecrawl.py     # PDF parsing via Firecrawl
│       └── mistral.py       # summarization via Mistral
├── static/
│   └── index.html           # entire frontend — HTML, Tailwind, JS
├── requirements.txt
└── .env                     # not committed — see .gitignore
```

---

## Known limitations

- PDFs are capped at 5MB and the first 10 pages — larger documents will be summarized partially, with a note shown in the UI
- No backend storage — the Flask API is a stateless pass-through between the frontend, Firecrawl, and Mistral
- No user accounts — summary history is per-browser via `localStorage`, not synced across devices
- No rate limiting — not intended for public production traffic
- Scanned/image-heavy PDFs depend on Firecrawl's OCR quality

