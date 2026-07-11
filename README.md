# Skim

A small AI tool that summarizes PDFs page-by-page based on what you tell it to look for — built for students and teachers who need to skim dense material fast.

Upload a PDF, describe what you want extracted (e.g. *"extract the top points on electrolysis"* or *"summarize each chapter"*), and Skim returns a clear, structured summary.

**Live demo:** _add your Render URL here_

---

## Why this exists

This is a portfolio project, not a SaaS. There's no auth, no database, no user accounts, and no billing — on purpose. The scope was kept deliberately small:

- **5MB upload limit** and **first 10 pages only** per PDF, to keep API costs and response times predictable
- **No backend storage** — the Flask API is a stateless pass-through between the frontend, Firecrawl, and Mistral
- **Summary history lives in the browser** via `localStorage`, not a database

Tools like ChatPDF, Humata, and SciSpace already do PDF summarization well, sometimes with more features (multi-doc chat, citations, etc). The goal here wasn't to compete with them — it was to build a clean, working, end-to-end pipeline that integrates multiple third-party APIs and makes sensible engineering tradeoffs for a demo-scale tool.

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
