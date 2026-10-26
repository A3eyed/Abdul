# Abdul — Mobile Personal SI & Automation Platform

## Product

Abdul is your **personal Super Intelligence assistant on your phone**, able to:

- Chat and plan like a capable personal AI
- Run **workflows** (multi-step automations)
- Handle **customer service** style replies and queues
- Support **marketing** campaigns and content calendars
- **Publish / schedule social media** content via official APIs
- Expand to any SI-style automation that tools and APIs allow

## Architecture (required for real automation)

Mobile apps alone cannot post to Instagram/Facebook/X/LinkedIn or run 24/7 agents without a backend.

```
┌─────────────────────┐
│  iOS / Android app  │  chat, approvals, notifications, quick actions
└──────────┬──────────┘
           │ HTTPS
┌──────────▼──────────┐
│  Abdul Core API     │  reasoning, memory, workflow engine
│  (VPS / always-on)  │
└──────────┬──────────┘
           │
    ┌──────┼──────┬──────────┬─────────┐
    ▼      ▼      ▼          ▼         ▼
  Social  Email  CRM/Sheets  Browser   Custom
  APIs    SMTP   webhooks    tools     webhooks
```

- **Phone** = control surface (you approve risky actions)
- **Core** = always-on brain + workflow runner
- **Integrations** = what actually publishes and replies

## Automation domains

| Domain | What Abdul can do (with connected accounts) |
|--------|-----------------------------------------------|
| Customer service | Draft/send replies, tag tickets, FAQ flows, escalate to you |
| Marketing | Briefs, calendars, A/B copy, campaign checklists |
| Social publishing | Create posts, schedule, publish via Meta/X/LinkedIn APIs |
| Personal | Reminders, research, file/email tasks when connected |
| Custom | Webhook + script workflows you define |

## Safety

- Publishing and outbound customer messages default to **draft → your approve in app** until you enable auto-send rules.
- Secrets only in server `.env` / vault — never in the mobile app binary.
- Full audit log of every automated action.

## Independence

- Core can run offline SI brain for chat/planning without paid APIs.
- Real social/CS automation needs platform API tokens (Meta, X, etc.) — that is unavoidable for real publishing.
- Optional Grok/open models for stronger copy and reasoning.

## Build phases

1. **Core workflow engine** + job queue + audit log (this repo)
2. **Mobile app** (Flutter) — chat, workflow list, approve/reject
3. **Connectors** — social, email, webhooks
4. **Templates** — CS reply, content calendar, scheduled post
5. **Always-on deploy** — VPS so automations run while phone sleeps
