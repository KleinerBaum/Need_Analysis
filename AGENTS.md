# AGENTS.md – Guide for Codex Agents 🪄

> **Repository:** [https://github.com/KleinerBaum/Need\_Analysis](https://github.com/KleinerBaum/Need_Analysis)
>
> This file explains **where** Codex should work, **how** to set up the environment, **what** quality gates to run, and **how** to submit code changes so they blend in perfectly with the existing project standards.

---

## 1  Code‑map & Key Folders

| Folder        | Purpose                                              |
| ------------- | ---------------------------------------------------- |
| `app.py`      | Streamlit entry point (landing page + wizard)        |
| `pages/`      | Static multipage content (About Us, Impressum…)      |
| `components/` | Re‑usable UI widgets and wizard sections             |
| `logic/`      | Business logic (trigger engine, file parsers)        |
| `services/`   | External services (OpenAI agent, FAISS vector store) |
| `models/`     | Pydantic data‑schemas for vacancy profiles           |
| `state/`      | Session‑state helpers                                |
| `utils/`      | Global config, prompt templates                      |

👉 **Stay inside these folders** when adding or editing code. Avoid creating new top‑level paths unless absolutely necessary.

---

## 2  Dev Environment (setup.sh)

The CI/CD pipeline expects the following tools:

```bash
# Install static type checker
pip install pyright

# Install project dependencies
pip install -r requirements.txt

# → If the repo switches to Poetry, use:
# poetry install --with test

# Optionally: JavaScript helpers
# pnpm install  # only needed if you touch /assets tooling
```

> **Note:** Setup scripts run in their **own** Bash session. Environment variables set here (e.g. `export`) will **not** leak to the agent. Persist long‑lived secrets in `~/.bashrc` or populate them inside the agent prompt.

### Proxy configuration


All outbound traffic goes through `http://proxy:8080` and must trust the cert at `$CODEX_PROXY_CERT`. Tools such as pip, curl, npm already respect these variables.

---

## 3  GitHub Remote & Token

Codex can only push changes if a Git remote and GitHub credentials are configured.

1. Add the project remote:

   ```bash
   git remote add origin https://github.com/KleinerBaum/Need_Analysis.git
   ```

2. Generate a personal access token from GitHub (Settings → **Developer settings** → **Personal access tokens**) and export it so Git can authenticate:

   ```bash
   export GITHUB_TOKEN=<your token>
   ```

   Place the export in `~/.bashrc` if you need it for future sessions.

---


## 5  How Codex Should Work

| Step                      | Action                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------- |
| **Locate code**           | Use the folder map above; grep by function/class names when unsure.                     |
| **Small tasks**           | Large refactors → break into several PRs.                                               |
| **Run gates**             | Always execute the *Quality Gates* exactly as scripted. Stop if any fail, fix, re‑run.  |
| **Verify output**         | For UI work run `streamlit run app.py` headless (CI does this) and ensure no traceback. |
| **Respect style**         | If `ruff` or `black` fail, call auto‑fix then commit.                                   |
| **Add tests**             | Minimum: cover the new branch/bug path; prefer >90 % diff coverage.                     |
| **No hard‑coded secrets** | Read via `os.getenv` or Streamlit secrets.                                              |
| **Proxy trust**           | When making network calls in tests, respect `$CODEX_PROXY_CERT`.                        |

---

