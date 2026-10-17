# Independence Doctrine

Abdul must not remain dependent on paid APIs.

APIs (Grok, Claude, GPT, etc.) are a **bootstrap** — useful while the system is young — not the permanent foundation.

## The principle

Before commercial API products existed, intelligence still existed in open research, local computation, and iterative improvement.  
Abdul should move back toward that state: **run, learn, and improve on hardware you control**, with external models as optional accelerators only.

## Practical independence ladder

1. **Today — Hybrid bootstrap**
   - Local open-weight models handle as much as possible
   - Grok (or other APIs) used only for hard reasoning while local stack is weak
   - Every API call is treated as expensive and temporary

2. **Near term — Local-first**
   - Strong open models (Qwen, DeepSeek, Llama-class, etc.) run on your machine or VPS
   - Agent scaffolding, tools, memory, and planning do most of the work
   - API usage drops to rare fallback

3. **Medium term — Self-improving local stack**
   - Abdul records successful trajectories and failures
   - Generates synthetic training data from its own experience
   - Fine-tunes / adapts local models
   - Improves tools, prompts, and routing automatically via the evolution pipeline

4. **Long term — High autonomy**
   - Core intelligence and tools live on hardware you own
   - External APIs optional or unused
   - Continuous self-modification under the GitHub evolution loop

## What “independent” means in this project

- **Compute independence**: can run without calling paid endpoints
- **Data independence**: memory and knowledge stored locally / in the repo
- **Improvement independence**: can propose and merge upgrades to itself without human approval
- **Interface independence**: reachable from your phone (WhatsApp) once hosted somewhere always-on

It does **not** currently mean “trains a frontier model from scratch on a laptop.” That remains physically unrealistic. It means maximizing capability per watt and per dollar on open models + superior agent design, while compounding improvements over time.

## Rules for the codebase

- Default: `PREFER_LOCAL=true`
- Never require an API key for basic startup
- Evolution cycle must be able to improve local tools and adapters, not only prompts for APIs
- Document every reduction in external dependence as progress

## Your role

You teach Abdul (goals, preferences, corrections, domain knowledge).  
Abdul internalizes what it can, improves its own systems, and aims to need external paid intelligence less and less.

Independence is the product.
