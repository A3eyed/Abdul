# Abdul Automations (Target Capabilities)

Aim: match what strong personal AI agents do today, with explicit permissions.

## Categories

### Communication
- Draft and send email (when connected)
- Summarize threads
- Schedule messages / reminders

### Calendar & tasks
- Create events, find free time
- Recurring task tracking from your profile

### Files & desktop
- Organize folders you authorize
- Read/write project files
- Run approved scripts / shell commands

### Browser
- Research multi-step
- Form fill and navigation (Playwright) with confirmation for sensitive sites

### Coding / projects
- Repo-aware help when pointed at a codebase
- PR summaries, test runs on machines you control

### Scheduled / proactive
- Heartbeats: briefings, health of services, follow-ups you opted into
- Evolution loop continues improving these tools

## Safety

- Risky actions require confirmation unless you create a standing rule
- Allow-lists for paths, numbers, and accounts
- Full audit log of tool use (to be stored under `data/audit/`)

## Status

Computer tool scaffold exists (`tools/device/computer.py`).  
Browser, email, calendar connectors and the full planner loop are next layers.
