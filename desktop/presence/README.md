# Abdul Presence UI

Interactive desktop presence layer (Gideon-inspired):

- Animated galaxy / star field
- Orb that reacts while listening / speaking
- **Cam** — optional camera sense (browser permission)
- **Listen** — speech-to-text
- **Speak** — text-to-speech replies
- Chat connected to Abdul core API

## Run locally

Terminal 1 — core:
```bash
cd Abdul
FORCE_OFFLINE=1 python3 demo_server.py   # or full core with valid XAI_API_KEY from console.x.ai
```

Terminal 2 — presence UI:
```bash
cd desktop_ui   # or serve desktop/presence files
python3 -m http.server 1420
```

Open http://localhost:1420

## Grok-level reasoning

Use a real API key from https://console.x.ai (not Cursor-prefixed keys).  
Set `XAI_API_KEY` and unset `FORCE_OFFLINE` for full Grok reasoning through the same UI.
