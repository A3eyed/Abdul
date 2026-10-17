# Abdul Desktop (Windows + macOS)

Cross-platform personal assistant shell. **No heavy LLM on the laptop.**

```
[Abdul Desktop UI]  -->  [Core API on localhost or VPS]  -->  [Grok API and/or remote open models]
```

## What you get

- Native-feeling window on **Windows and Mac** (via Tauri)
- Chat UI in this folder
- Core stays separate so the laptop does not freeze

## Quick try (UI in browser while developing)

Terminal 1 — core:
```bash
cd Abdul
cp .env.example .env
# set XAI_API_KEY for bootstrap brain (optional if remote open models later)
python -m core.main
```

Terminal 2 — desktop UI:
```bash
cd desktop
npm install
npm run dev
```
Open http://localhost:1420

## Native app (Windows + Mac)

Requires [Rust](https://rustup.rs/) + [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/).

```bash
cd desktop
npm install
# After full Tauri Rust project is completed:
# npm run tauri dev
# npm run tauri build   # .msi/.exe on Windows, .app/.dmg on Mac
```

`src-tauri/tauri.conf.json` targets both OS families.

## Next

- Complete Tauri Rust side (tray, permissions)
- Settings for brain URL
- Local tools from the desktop process
