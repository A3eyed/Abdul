# Abdul Mobile (iOS + Android)

Your **personal SI assistant on the phone**: chat, run and approve automations for customer service, marketing, and social publishing.

## Architecture

```
Phone app  →  Abdul Core (VPS :8080)  →  Social / Email / Webhooks
```

The app does not embed Meta/X secrets. Core runs workflows 24/7.

## API the app uses

| Action | Endpoint |
|--------|----------|
| Health | `GET /health` |
| Chat | `POST /chat` |
| List jobs | `GET /workflows` |
| CS reply flow | `POST /workflows/customer-service` |
| Social post flow | `POST /workflows/social` |
| Marketing calendar | `POST /workflows/marketing-calendar` |
| Approve step | `POST /workflows/{id}/approve` |

Interactive docs: `http://YOUR_CORE:8080/docs`

## Flutter bootstrap (on your machine)

```bash
# https://docs.flutter.dev/get-started/install
cd mobile
flutter create --org ai.abdul abdul_app
cd abdul_app
flutter run
```

Point the app’s base URL at your core (Tailscale IP or HTTPS VPS).

## Screens (v1)

1. Chat  
2. Workflows list + detail  
3. Approve / reject  
4. Quick actions (CS / Social / Marketing)  
5. Settings (core URL)

## Safety defaults

- Outbound publish/send: **dry-run** until `SOCIAL_DRY_RUN=false` / messaging keys set  
- Approval gates before send/publish unless you enable auto rules  

## Interim (before App Store builds)

Use phone browser → core `/docs`, or WhatsApp when that channel is connected.
