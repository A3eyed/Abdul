# Deploy Abdul on a Free or Cheap Always-On VPS

This is the recommended way to use Abdul from your phone with no computer nearby.

Once Abdul is running on a VPS, you only need your phone (via WhatsApp) to talk to it.

## 1. Choose a provider

| Provider | Free tier? | Notes |
|----------|------------|-------|
| **Oracle Cloud** | Yes (Always Free ARM) | Best free option for many people. 1–4 OCPU + 6–24 GB RAM possible. |
| **Hetzner** | No (very cheap) | Excellent price/performance. CX22 or CAX11 is plenty. |
| **DigitalOcean / Linode / Vultr** | Limited trials | Simple UI. |
| **Google Cloud / AWS** | Limited free credits | More complex. |

**Recommendation:** Start with Oracle Cloud Always Free if you want $0 cost.

## 2. Create the server

- Choose Ubuntu 22.04 or 24.04.
- Minimum: 1–2 vCPU, 2–4 GB RAM (more is better if you want local models).
- Open ports: 22 (SSH), and whatever you need for the web UI if you expose it.
- For WhatsApp only you do **not** need a public web port.

## 3. Basic server setup

```bash
ssh root@YOUR_SERVER_IP

# Update
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker

# Optional but recommended: create a non-root user
adduser abdul
usermod -aG docker abdul
```

## 4. Clone and configure Abdul

```bash
su - abdul
git clone https://github.com/A3eyed/Abdul.git
cd Abdul
cp .env.example .env
nano .env          # put your XAI_API_KEY and other settings here
```

Important `.env` settings for mobile use:
```env
ENABLE_WHATSAPP=true
WHATSAPP_ALLOWED_NUMBERS=+yournumber
PREFER_LOCAL=true
```

## 5. Start Abdul

```bash
docker compose up -d
```

Check logs:
```bash
docker compose logs -f
```

## 6. Connect WhatsApp

When the WhatsApp bridge is fully wired, Abdul will show a QR code (in logs or a simple web page).  
Scan it with the WhatsApp account you want to use for the bot (preferably a secondary number).

After that you can text Abdul from your personal phone.

## 7. Keep it alive

- `restart: unless-stopped` is already in the docker-compose.
- Optional: install `watchtower` to auto-update containers.
- Use the health-check GitHub Action (see `.github/workflows/healthcheck.yml`) so you get notified if it goes down.

## 8. Security basics

- Use SSH keys, disable password login.
- Enable a firewall (`ufw allow 22 && ufw enable`).
- Never commit your real `.env`.
- Prefer Tailscale if you want to reach a web UI privately.

## Cost expectation

- Oracle Always Free: **$0**
- Small Hetzner / similar: roughly **$3–6 per month**

This is currently the most reliable way to have Abdul available from your phone at any time.
