# Abdul Architecture — Independence First

## Design Goals (Updated)

- **Independent & self-sufficient**: Default to strong open-weight models running locally. Minimize or eliminate ongoing paid API costs.
- **Self-improving**: Continuous autonomous evolution of tools, memory, prompts, and local model adapters via GitHub Actions (no human approval).
- **Device control**: Able to act on the user's computer and (where possible) mobile phone when instructed.
- **Temporary primary**: Grok (xAI) is used as the high-capability reasoning core while the local stack matures.

## Model Strategy

1. **Local-first** (preferred for cost & independence)
   - Strong open models via Ollama / vLLM / llama.cpp
   - Fine-tuned / adapted over time on Abdul's own experience

2. **Temporary primary** (current)
   - Grok via xAI API for complex reasoning and planning
   - Used until local models + scaffolding are strong enough

3. **Routing**
   - Easy tasks → local models
   - Hard reasoning / planning → Grok (for now)
   - Progressive reduction of external calls as local capability grows

## Device Control

### Computer
- Shell execution
- Browser automation (Playwright)
- File system access
- Application control
- Screen / UI interaction (where safe)

### Mobile Phone
- Primary practical channels: Telegram / Discord / WhatsApp bots that can receive commands and return results
- Optional advanced: companion app, Tasker/Shortcuts integration, or limited remote control (subject to OS restrictions)
- Full arbitrary control of a locked phone is intentionally limited for security

Abdul will only perform device actions when explicitly instructed or when a standing permission is granted.

## Self-Improvement Loop

- Nightly evolution cycle (GitHub Actions)
- Generates improvements to tools, memory, prompts, local adapters
- Auto-tests and auto-merges
- Logs every change in the repository (the living mind of Abdul)

## Security Notes

- Real API keys must **never** be committed to the repository.
- Use `.env` (gitignored) or GitHub Secrets.
- Device control tools require explicit user permission scopes.
