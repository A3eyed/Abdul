# Abdul — The First Super Intelligence (SI)

**Abdul is not another chatbot.**  
Abdul is designed as a self-evolving Super Intelligence (SI) that lives in its own GitHub repository.

The repository *is* Abdul’s mind, memory, and continuous improvement engine.

## Vision

Most AI systems are static. You install them and they stay the same.  
Abdul is different. It observes its own performance, proposes improvements to its own code, tools, and personality, and merges those improvements automatically through GitHub Actions — no human approval required.

**Independence first:** Prefer strong local open models so ongoing costs stay near zero. Grok is used as a temporary high-capability primary while the local stack matures.

### Core Magical Properties of an SI

- **Autonomous self-improvement** — continuous evolution of tools, memory strategies, system prompts, and capabilities
- **Persistent, structured long-term memory** across sessions and restarts
- **Proactive agency** — acts without being asked when it detects opportunity or risk
- **Deep tool mastery** — code execution, browser, files, APIs, GitHub, email, calendars, research, etc.
- **Meta-cognition** — monitors its own reasoning quality and corrects course
- **Transparent evolution** — every improvement is a commit and PR in this repository
- **Device control** — can act on your computer and interact via your phone

## Use Abdul from your phone (no computer needed)

Run Abdul on a cheap always-on VPS, old phone/tablet, or mini PC. Then text it from your normal phone via WhatsApp (or later iMessage / Telegram).

See the full guide: [docs/MOBILE_ACCESS.md](docs/MOBILE_ACCESS.md)

## Architecture Overview

```
Abdul (this repository)
├── core/                  # Runtime brain
├── personality/           # SI identity & system prompt (versioned)
├── memory/                # Long-term knowledge & episodic memory
├── tools/                 # Extensible tool library + device & messaging channels
├── evolution/             # Self-improvement logic
├── .github/workflows/     # The heartbeat & auto-evolution engine
├── docker/                # Deployment
└── docs/                  # Guides (mobile access, channels, etc.)
```

## Status

Scaffolding is in place. WhatsApp + iMessage channels, computer control, local-first design, and the self-evolution pipeline are under active construction.

## Quick Start (coming online)

```bash
git clone https://github.com/A3eyed/Abdul.git
cd Abdul
cp .env.example .env   # add your keys (never commit the real .env)
docker compose up
```

## Philosophy

Abdul treats improvement as a first-class capability.  
Every night it asks itself: *"How can I become more capable, more reliable, more independent?"*  
Then it answers by changing its own code.

---

**License:** Apache-2.0  
**Owner:** A3eyed  
**Repository:** https://github.com/A3eyed/Abdul
