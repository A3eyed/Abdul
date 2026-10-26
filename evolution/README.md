# Abdul Evolution

## Policy (current)

- Abdul **proposes and applies** code improvements via GitHub Actions.
- Pull requests are **auto-merged** after the evolution cycle (owner preference).
- Independence-first changes preferred.

## How it runs

1. Action `Abdul Self-Evolution` runs on a schedule or manually.
2. `run_evolution.py` writes proposal changes on a branch.
3. A PR is opened and **merged automatically**.
4. Branch is deleted after merge.

## Manual trigger

GitHub → Actions → **Abdul Self-Evolution** → **Run workflow**

## If auto-merge fails

Enable under **Settings → Actions → General → Workflow permissions**:
- Read and write permissions
- Allow GitHub Actions to create and approve pull requests
