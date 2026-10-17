# Run Abdul on Localhost

You can run Abdul on your own computer for development and daily use.

## Quick local start

```bash
git clone https://github.com/A3eyed/Abdul.git
cd Abdul
cp .env.example .env
```

Edit `.env` and set at least:

```env
XAI_API_KEY=your_grok_key_here
PREFER_LOCAL=true
ENABLE_COMPUTER_USE=true
ENABLE_WHATSAPP=false          # turn on later when ready to pair
```

### Option A — Docker (recommended)

```bash
docker compose up --build
```

Then open: http://localhost:8080

### Option B — Direct Python (for development)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m core.main
```

## What works on localhost

- Core agent loop (being built)
- Computer control tools (shell, files)
- Health endpoint at `/health`
- Local model routing (when Ollama is running on the same machine)
- WhatsApp pairing (once the bridge is finished — QR will appear in the terminal or a local page)

## Local + Phone at the same time

You can run Abdul on localhost and still connect WhatsApp.  
As long as your computer is on and has internet, you can text Abdul from your phone.  
When you want it available even while the computer is off, move the same setup to a VPS (see `DEPLOY_VPS.md`).

## Stopping

```bash
docker compose down
# or Ctrl+C if running with python
```
