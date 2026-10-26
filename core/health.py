"""
Simple health endpoint for Abdul.
Used by the GitHub Actions health-check workflow and by load balancers / uptime monitors.
"""

from datetime import datetime, timezone

def get_health_status() -> dict:
    return {
        "status": "ok",
        "service": "Abdul SI",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.2.0-si",
        "mode_hint": "independent offline brain available",
    }
