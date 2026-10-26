"""
Abdul Workflow Engine
=====================
Runs multi-step automations for personal SI + business tasks.

Jobs are persisted as JSON under data/workflows/.
Risky steps (publish, send) respect require_approval unless auto rules enabled.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "workflows"
AUDIT = ROOT / "data" / "audit"


class JobStatus(str, Enum):
    DRAFT = "draft"
    QUEUED = "queued"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepType(str, Enum):
    REASON = "reason"
    DRAFT_CONTENT = "draft_content"
    DRAFT_REPLY = "draft_reply"
    PUBLISH_SOCIAL = "publish_social"
    SEND_MESSAGE = "send_message"
    WEBHOOK = "webhook"
    WAIT_APPROVAL = "wait_approval"
    NOTIFY = "notify"


@dataclass
class Step:
    type: str
    name: str
    params: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    result: dict[str, Any] | None = None
    require_approval: bool = False


@dataclass
class Job:
    id: str
    template: str
    title: str
    status: str
    steps: list[dict[str, Any]]
    created_at: str
    updated_at: str
    meta: dict[str, Any] = field(default_factory=dict)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _job_path(job_id: str) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    return DATA / f"{job_id}.json"


def save_job(job: Job) -> Job:
    job.updated_at = _now()
    path = _job_path(job.id)
    path.write_text(json.dumps(asdict(job), indent=2), encoding="utf-8")
    return job


def load_job(job_id: str) -> Job | None:
    path = _job_path(job_id)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return Job(**data)


def list_jobs(limit: int = 50) -> list[dict[str, Any]]:
    DATA.mkdir(parents=True, exist_ok=True)
    jobs = []
    for p in sorted(DATA.glob("*.json"), reverse=True)[:limit]:
        try:
            jobs.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return jobs


def audit(event: str, payload: dict[str, Any]) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    line = {"at": _now(), "event": event, **payload}
    log = AUDIT / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")


# --- Templates ---

def template_customer_reply(customer_message: str, channel: str = "email") -> Job:
    job_id = str(uuid.uuid4())
    steps = [
        asdict(Step("draft_reply", "Draft customer reply", {"inbound": customer_message, "channel": channel})),
        asdict(Step("wait_approval", "Approve outbound reply", require_approval=True)),
        asdict(Step("send_message", "Send reply", {"channel": channel}, require_approval=False)),
        asdict(Step("notify", "Notify owner", {"message": "Customer reply handled"})),
    ]
    job = Job(
        id=job_id,
        template="customer_service_reply",
        title=f"CS reply via {channel}",
        status=JobStatus.QUEUED.value,
        steps=steps,
        created_at=_now(),
        updated_at=_now(),
        meta={"inbound": customer_message},
    )
    return save_job(job)


def template_social_post(platform: str, topic: str, auto_publish: bool = False) -> Job:
    job_id = str(uuid.uuid4())
    steps = [
        asdict(Step("draft_content", "Draft social post", {"platform": platform, "topic": topic})),
        asdict(
            Step(
                "wait_approval",
                "Approve post",
                require_approval=not auto_publish,
            )
        ),
        asdict(
            Step(
                "publish_social",
                f"Publish to {platform}",
                {"platform": platform},
                require_approval=False,
            )
        ),
        asdict(Step("notify", "Notify owner", {"message": f"Posted to {platform}"})),
    ]
    job = Job(
        id=job_id,
        template="social_publish",
        title=f"Social: {platform} — {topic[:40]}",
        status=JobStatus.QUEUED.value,
        steps=steps,
        created_at=_now(),
        updated_at=_now(),
        meta={"platform": platform, "topic": topic, "auto_publish": auto_publish},
    )
    return save_job(job)


def template_marketing_calendar(campaign: str, days: int = 7) -> Job:
    job_id = str(uuid.uuid4())
    steps = [
        asdict(
            Step(
                "draft_content",
                "Build content calendar",
                {"campaign": campaign, "days": days},
            )
        ),
        asdict(Step("wait_approval", "Approve calendar", require_approval=True)),
        asdict(Step("notify", "Calendar ready", {"message": "Marketing calendar approved"})),
    ]
    job = Job(
        id=job_id,
        template="marketing_calendar",
        title=f"Marketing calendar: {campaign[:40]}",
        status=JobStatus.QUEUED.value,
        steps=steps,
        created_at=_now(),
        updated_at=_now(),
        meta={"campaign": campaign, "days": days},
    )
    return save_job(job)


def _draft_text(kind: str, params: dict[str, Any]) -> str:
    """Offline-capable drafting; swap for Grok/LLM when configured."""
    if kind == "draft_reply":
        inbound = params.get("inbound", "")
        return (
            f"Thank you for reaching out.\n\n"
            f"Regarding: {inbound[:500]}\n\n"
            f"We are looking into this and will follow up shortly. "
            f"Please reply if you have more detail.\n\n— Abdul CS Assistant"
        )
    if kind == "draft_content" and "platform" in params:
        topic = params.get("topic", "update")
        platform = params.get("platform", "social")
        return (
            f"[{platform}] {topic}\n\n"
            f"Quick take: {topic}. More soon — stay tuned.\n\n"
            f"#marketing #automation"
        )
    if kind == "draft_content":
        campaign = params.get("campaign", "campaign")
        days = params.get("days", 7)
        lines = [f"Content calendar for **{campaign}** ({days} days):"]
        for i in range(1, min(int(days), 14) + 1):
            lines.append(f"Day {i}: Post angle related to {campaign} — draft needed")
        return "\n".join(lines)
    return json.dumps(params)


def run_job(job_id: str, approve: bool = False) -> Job:
    """Advance a job through steps until blocked, failed, or complete."""
    job = load_job(job_id)
    if not job:
        raise ValueError(f"Unknown job {job_id}")

    job.status = JobStatus.RUNNING.value
    save_job(job)
    audit("job_running", {"job_id": job_id})

    for i, step in enumerate(job.steps):
        if step.get("status") in ("done", "skipped"):
            continue

        stype = step.get("type")
        params = step.get("params") or {}

        if stype == "wait_approval":
            if not approve and step.get("require_approval", True):
                step["status"] = "waiting"
                job.status = JobStatus.AWAITING_APPROVAL.value
                save_job(job)
                audit("awaiting_approval", {"job_id": job_id, "step": step.get("name")})
                return job
            step["status"] = "done"
            step["result"] = {"approved": True}
            approve = False  # only consumes one approval gate unless called again
            continue

        if stype in ("draft_reply", "draft_content"):
            text = _draft_text(stype, params)
            step["result"] = {"text": text}
            step["status"] = "done"
            job.meta["last_draft"] = text
            continue

        if stype == "publish_social":
            # Real publish happens in connectors/social.py when credentials exist
            from core.workflows.connectors_social import publish as social_publish

            result = social_publish(
                platform=params.get("platform") or job.meta.get("platform", "unknown"),
                text=job.meta.get("last_draft", ""),
            )
            step["result"] = result
            step["status"] = "done" if result.get("ok") else "failed"
            if not result.get("ok"):
                job.status = JobStatus.FAILED.value
                save_job(job)
                audit("publish_failed", {"job_id": job_id, "result": result})
                return job
            continue

        if stype == "send_message":
            from core.workflows.connectors_messaging import send as msg_send

            result = msg_send(
                channel=params.get("channel", "email"),
                text=job.meta.get("last_draft", ""),
            )
            step["result"] = result
            step["status"] = "done" if result.get("ok") else "failed"
            if not result.get("ok"):
                job.status = JobStatus.FAILED.value
                save_job(job)
                return job
            continue

        if stype == "webhook":
            from core.workflows.connectors_webhook import post as wh_post

            result = wh_post(params.get("url", ""), params.get("body") or job.meta)
            step["result"] = result
            step["status"] = "done" if result.get("ok") else "failed"
            continue

        if stype == "notify":
            step["result"] = {"notified": True, "message": params.get("message", "")}
            step["status"] = "done"
            audit("notify", {"job_id": job_id, "message": params.get("message")})
            continue

        step["status"] = "skipped"

    job.status = JobStatus.COMPLETED.value
    save_job(job)
    audit("job_completed", {"job_id": job_id})
    return job


def approve_job(job_id: str) -> Job:
    """User approved from mobile app — continue past approval gate."""
    return run_job(job_id, approve=True)
