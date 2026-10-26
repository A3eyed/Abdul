"""Workflow REST API — used by mobile app and desktop."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.workflows.engine import (
    approve_job,
    list_jobs,
    load_job,
    run_job,
    template_customer_reply,
    template_marketing_calendar,
    template_social_post,
)

router = APIRouter(prefix="/workflows", tags=["workflows"])


class CSRequest(BaseModel):
    message: str
    channel: str = "email"
    run: bool = True


class SocialRequest(BaseModel):
    platform: str = Field(description="x | facebook | instagram | linkedin")
    topic: str
    auto_publish: bool = False
    run: bool = True


class MarketingRequest(BaseModel):
    campaign: str
    days: int = 7
    run: bool = True


@router.get("")
def get_jobs():
    return {"jobs": list_jobs()}


@router.get("/{job_id}")
def get_job(job_id: str):
    job = load_job(job_id)
    if not job:
        raise HTTPException(404, "job not found")
    return job


@router.post("/customer-service")
def create_cs(req: CSRequest):
    job = template_customer_reply(req.message, req.channel)
    if req.run:
        job = run_job(job.id)
    return job


@router.post("/social")
def create_social(req: SocialRequest):
    job = template_social_post(req.platform, req.topic, auto_publish=req.auto_publish)
    if req.run:
        job = run_job(job.id)
    return job


@router.post("/marketing-calendar")
def create_marketing(req: MarketingRequest):
    job = template_marketing_calendar(req.campaign, req.days)
    if req.run:
        job = run_job(job.id)
    return job


@router.post("/{job_id}/approve")
def approve(job_id: str):
    job = load_job(job_id)
    if not job:
        raise HTTPException(404, "job not found")
    return approve_job(job_id)


@router.post("/{job_id}/run")
def run(job_id: str):
    job = load_job(job_id)
    if not job:
        raise HTTPException(404, "job not found")
    return run_job(job_id)
