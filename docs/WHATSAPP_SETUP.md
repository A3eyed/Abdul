# WhatsApp Setup for Abdul

Once the Baileys bridge is fully wired, this is how you connect WhatsApp so you can text Abdul from your phone.

## 1. Prepare

In your local or VPS `.env`:

```env
ENABLE_WHATSAPP=true
WHATSAPP_ALLOWED_NUMBERS=+1234567890     # your personal number (E.164)
WHATSAPP_SESSION_DIR=./data/whatsapp_session
```

Use a **secondary number** for the bot itself if possible. Your personal number goes in the allow-list so only you can talk to it.

## 2. Start Abdul

**Localhost:**
```bash
docker compose up --build
# or: python -m core.main
```

**VPS:** same commands on the server.

## 3. Pair (QR code)

When the WhatsApp bridge starts it will print a QR code in the terminal (or serve it on a local page).

On your phone:
1. Open WhatsApp
2. Go to **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code

The session is stored only on the machine running Abdul. You never need to send your number to anyone.

## 4. Text Abdul

Message the linked number from your personal phone. Abdul will reply through the same channel.

## Current status

- Channel scaffolding: done (`tools/channels/whatsapp.py`)
- Full Baileys sidecar + QR flow: next implementation step
- After that, localhost and VPS will both support phone messaging

## Safety

- Keep `WHATSAPP_ALLOWED_NUMBERS` limited to your own number(s)
- Prefer a dedicated bot number
- Do not expose the session folder publicly
