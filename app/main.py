from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI

from app.metrics import get_system_metrics, get_system_status
from app.ai_diagnostics import get_ai_analysis

# Load settings from the local .env file, if it exists.
load_dotenv()

app = FastAPI(
    title="Smart Server Health Diagnostics API",
    description="Checks system health and provides AI-generated diagnostics.",
    version="1.0.0",
)


@app.get("/api/health-report")
def health_report():
    """Return live system metrics, status, and AI diagnostics."""
    metrics = get_system_metrics()
    status = get_system_status(metrics)
    ai_analysis = get_ai_analysis(metrics, status)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "metrics": metrics,
        "ai_analysis": ai_analysis,
    }
