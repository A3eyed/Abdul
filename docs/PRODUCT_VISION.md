# Abdul Product Vision (Updated)

## What you asked for

- A **desktop app** on your laptop (interactive, always available, Gideon-like)
- It **studies how you work** (with your permission) on laptop and phone
- Full **personal AI assistant** + top-tier **agent automations**
- **iOS and Android apps** so it lives on your personal phone
- **Independent** long-term, but **laptop must not freeze** (no heavy Ollama on the laptop)

## Hard constraint

Your laptop cannot run large local models reliably. Therefore:

| Layer | Where it runs | Role |
|-------|----------------|------|
| **Desktop app** | Your laptop | UI, presence, local tools, file/automation access, learning sensors |
| **Brain (reasoning)** | VPS and/or Grok API (bootstrap) | Planning, language, hard reasoning |
| **Mobile apps** | iPhone + Android | Chat, notifications, light actions, sensors you allow |
| **Self-improvement** | GitHub Actions + your hosts | Evolves code, tools, memory strategies |

Heavy inference never freezes the laptop. The desktop app is the **body and senses**; the brain can live elsewhere.

## Desktop app (primary experience)

Inspired by interactive personal AIs (Gideon-style presence):

- Always reachable (tray / overlay / main window)
- Chat + voice later
- Sees what you allow: files, calendar, browser context, running apps, clipboard (permissioned)
- Runs automations: scripts, browser tasks, file ops, scheduled jobs
- Builds a **private model of how you work** (routines, projects, preferences)
- Talks to the remote brain securely when needed

Tech direction: **Tauri** or **Electron** shell around the Abdul core (Tauri preferred for lighter resource use).

## Mobile apps (iOS + Android)

Phases:

1. **Now:** WhatsApp (and later iMessage) as the phone interface — zero App Store delay
2. **Next:** Cross-platform app (**Flutter** or **React Native**) for chat, push, quick actions
3. **Later:** Deeper phone integrations (notifications summary, shares, limited automation where OS allows)

iOS will always be more locked down than Android; the app will respect that and use official APIs only.

## “Study me” (learning system)

Private, on-device / on-your-server profile — not sold, not shared.

With explicit permissions, Abdul may learn:

- Work patterns (active hours, frequent apps/files, project folders)
- Communication style and preferences you correct over time
- Recurring tasks and automations you approve
- Phone-side signals the mobile app is allowed to send (not full silent surveillance)

Everything is inspectable and deletable by you.

## Automations (agent capabilities)

Target parity with strong personal agents:

- Research, summarize, draft
- Email / calendar / files (when connected)
- Browser automation
- Shell and scripts on machines you authorize
- Scheduled jobs and reminders
- Multi-step goals with confirmation for risky actions

## Independence path (unchanged doctrine)

- Prefer your VPS + open models for the brain when possible
- Grok API as temporary bootstrap for quality
- Self-evolve tools and memory so fewer external calls are needed
- Never require Ollama on the laptop

## Build order

1. Desktop shell (local app) + permissioned local tools + remote brain
2. User profile / “study me” memory store
3. WhatsApp phone access
4. Flutter/RN mobile app scaffold for iOS + Android
5. Richer automations + evolution of those tools

This is a product, not a single script. It will ship in layers that stay usable at each step.
