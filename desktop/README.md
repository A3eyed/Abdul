# Abdul Desktop

Personal SI shell for your **laptop** — interactive assistant, not a frozen Ollama session.

## Goals

- Lightweight desktop app (tray + main window + optional overlay)
- Local tools: files, shell (permissioned), browser automation hooks, schedules
- Talks to remote brain (your VPS and/or Grok API) so the laptop stays responsive
- Learns work patterns into a private profile you control

## Planned stack

- **Tauri 2** + Rust backend commands for system access
- **Frontend:** HTML/TS or lightweight React/Svelte UI
- Connects to Abdul core API (`http://127.0.0.1:8080` when core runs locally, or your VPS URL)

## Why not heavy models on the laptop

Large local LLMs freeze or slow some machines. Abdul Desktop is the **control plane**:

```
[Desktop UI + local tools]  ↔  [Brain on VPS / API]
```

## Status

Scaffold only. Next: Tauri project init, tray, chat UI, secure config for brain URL + keys.

## Run core alongside (for now)

Until the desktop shell is complete, use the existing FastAPI core:

```bash
# from repo root
cp .env.example .env
python -m core.main
# open http://localhost:8080
```

Desktop will embed or attach to that API.
