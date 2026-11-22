# Smart Server Health Diagnostics API

A lightweight Python REST API that collects local machine health metrics and
uses an LLM API to generate a short diagnostic summary and recommendation.

## Features

- Collects CPU, memory (RAM), and disk utilization using `psutil`.
- Classifies overall health as `HEALTHY`, `WARNING`, or `CRITICAL`.
- Uses an LLM API to generate a plain-English summary and practical recommendation.
- Returns a fallback response if the API key is missing or the AI service fails.
- Exposes one endpoint: `GET /api/health-report`.

## Project structure

```text
Smart-Server-Health-Diagnostics/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── metrics.py
│   └── ai_diagnostics.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9 or newer
- An LLM API key for AI-generated analysis (optional; fallback works without it)

## Setup and run locally

### 1. Download the project

Download or clone this repository and open the project folder.

### 2. Create a virtual environment (recommended)

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the LLM API

Make a copy of `.env.example` and name the copy `.env`.

Open `.env` and replace `your_api_key_here` with your own API key.
The example configuration uses Google's Gemini API through its OpenAI-compatible chat completions endpoint. The configured model is gemini-2.5-flash. You can change the URL and model if you use another compatible provider.

Do not commit or upload your real `.env` file or API key. The `.gitignore`
file excludes `.env` from Git.

### 5. Start the API

Run this command from the project root folder:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Test the endpoint

Open this URL in a browser:

`http://127.0.0.1:8000/api/health-report`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

You can also test it with curl:

```bash
curl http://127.0.0.1:8000/api/health-report
```

## Example JSON response

The numbers and text below are illustrative. Actual metric values depend on
the machine running the API.

```json
{
  "timestamp": "2026-11-21T16:30:00+00:00",
  "status": "WARNING",
  "metrics": {
    "cpu_percent": 76.5,
    "memory_percent": 68.2,
    "disk_percent": 54.0
  },
  "ai_analysis": {
    "summary": "CPU utilization is elevated, while memory and disk usage are within normal limits.",
    "recommendation": "Check background processes or heavy applications that may be consuming CPU resources."
  }
}
```

## How it works

1. `main.py` defines the FastAPI application and the health-report endpoint.
2. `metrics.py` collects CPU, memory, and disk utilization and classifies system status.
3. `ai_diagnostics.py` sends the metrics and status to the configured LLM API.
4. If the LLM API key is missing or the request fails, a fallback analysis is returned.
5. FastAPI combines the timestamp, status, metrics, and AI analysis into a JSON response.

## Health thresholds

- More than 85% on any metric: `CRITICAL`
- More than 70% on any metric: `WARNING`
- Otherwise: `HEALTHY`

The highest severity among the three metrics determines the overall status.
