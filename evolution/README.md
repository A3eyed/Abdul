# Abdul Evolution

## Policy

- Abdul **proposes** code changes (rewrites, improvements).
- **You** inspect the pull request and approve or reject.
- **No auto-merge.** Nothing lands on `main` without your OK.

## How it runs

1. GitHub Action `Abdul Self-Evolution` runs on a schedule or manually.
2. `run_evolution.py` applies proposal changes on a branch.
3. A PR is opened labeled `needs-human-review`.
4. You review the diff → merge or close.

## Goals

- Independence first (offline brain, less paid API dependence)
- Better tools, memory, reliability
- Safe, reviewable diffs

## Manual trigger

GitHub → Actions → **Abdul Self-Evolution** → **Run workflow**
