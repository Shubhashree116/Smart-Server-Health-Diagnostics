import os

import psutil


def get_system_metrics():
    """Collect CPU, memory, and disk utilization percentages."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(os.path.abspath(os.sep)).percent,
    }


def get_system_status(metrics):
    """Return the overall status using the assignment thresholds."""
    if (
        metrics["cpu_percent"] > 85
        or metrics["memory_percent"] > 85
        or metrics["disk_percent"] > 85
    ):
        return "CRITICAL"

    if (
        metrics["cpu_percent"] > 70
        or metrics["memory_percent"] > 70
        or metrics["disk_percent"] > 70
    ):
        return "WARNING"

    return "HEALTHY"
