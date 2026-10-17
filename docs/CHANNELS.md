# Messaging Channels for Abdul

You asked for WhatsApp and iMessage so you can text Abdul from the apps you already use.

## WhatsApp (Ready to implement)

**Method:** Baileys (unofficial WhatsApp Web multi-device protocol)

### What you need
- A phone number (strongly recommended: a **secondary / dedicated** number)
- Node.js environment for the Baileys sidecar (or a Python bridge later)
- One-time QR code scan (same as WhatsApp Web)

### Risks
- Unofficial. Meta can temporarily restrict accounts that look like bots.
- Keep usage personal and low-volume.
- Do not use your primary personal number if you are risk-averse.

### Status in Abdul
Scaffolding is in `tools/channels/whatsapp.py`. Full Baileys wiring is the next implementation step.

## iMessage (Requires a Mac)

Apple provides no public API. All reliable self-hosted solutions need a Mac signed into Messages.app.

### Recommended path
1. Run **BlueBubbles** server on a Mac that stays signed into your Apple ID / Messages.
2. Abdul connects to BlueBubbles via its REST API + webhooks.

Alternative: newer `imsg` CLI style bridges used by advanced agent frameworks (also requires the Mac).

### Without a Mac
Reliable pure self-hosted iMessage is currently not practical. Cloud/managed services exist but add cost and external dependency.

### Status in Abdul
Scaffolding is in `tools/channels/imessage.py`.

## Priority Order (as requested)
1. WhatsApp
2. iMessage
3. Telegram (later, when you want it)

## Security
- Only allow your own numbers / handles via the allow-lists in `.env`.
- Never expose the WhatsApp session or BlueBubbles server to the public internet without strong authentication.
