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
| `tests/`      | Pytest suite (unit, integration, smoke)              |

👉 **Stay inside these folders** when adding or editing code. Avoid creating new top‑level paths unless absolutely necessary.

---

## 2  Dev Environment (setup.sh)

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

> **Note:** Setup scripts run in their **own** Bash session. Environment variables set here (e.g. `export`) will **not** leak to the agent. Persist long‑lived secrets in `~/.bashrc` or populate them inside the agent prompt.

### Proxy configuration

All outbound traffic goes through `http://proxy:8080` and must trust the cert at `$CODEX_PROXY_CERT`. Tools such as pip, curl, npm already respect these variables.

---

## 3  Quality Gates (test.sh)

Run these **exact** commands before committing:

```bash
# 1  Lint & style
ruff check .                # must be 100 % clean
black --check .             # auto‑format if needed

# 2  Static typing
pyright .                   # or mypy . – both must pass

# 3  Tests
pytest -q                   # green test‑suite required
```

If you add or refactor code **you must also add/adjust tests** in `tests/`. Mock all external (OpenAI) calls!

---

## 4  Contribution Workflow

1. **Branching**: work on `dev` or a feature branch `feat/<short-name>`.
2. **Commits** follow Conventional Commits, e.g. `feat: add skill drag‑and‑drop`.
3. **PR title**: `[Need_Analysis] <brief description>`.
4. **CI passes** (lint, type, tests) before merge.
5. **Update docs** (README, AGENTS.md) when public behaviour or API changes.

---

## 5  How Codex Should Work

| Step                      | Action                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------- |
| **Locate code**           | Use the folder map above; grep by function/class names when unsure.                     |
| **Small tasks**           | Large refactors → break into several PRs.                                               |
| **Run gates**             | Always execute the *Quality Gates* exactly as scripted. Stop if any fail, fix, re‑run.  |
| **Verify output**         | For UI work run `streamlit run app.py` headless (CI does this) and ensure no traceback. |
| **Respect style**         | If `ruff` or `black` fail, call auto‑fix then commit.                                   |
| **Add tests**             | Minimum: cover the new branch/bug path; prefer >90 % diff coverage.                     |
| **No hard‑coded secrets** | Read via `os.getenv` or Streamlit secrets.                                              |
| **Proxy trust**           | When making network calls in tests, respect `$CODEX_PROXY_CERT`.                        |

---

## 6  Validation Checklist

* [ ] `ruff check .` passes
* [ ] `black --check .` passes
* [ ] `pyright .` (or `mypy .`) passes
* [ ] `pytest -q` all green
* [ ] docs updated (if public interface changed)
* [ ] no TODOs / print-debug left

---

## 7  Common Commands Cheat‑sheet

```bash
# Start app (local dev)
streamlit run app.py

# Single test case
pytest tests/test_file_tools.py::test_extract_text_from_pdf -q

# Reformat everything
black . && ruff check . --fix
```

---

## 8  Example PR Message Template

```markdown
### 📌 Summary
Refactors trigger_engine to support conditional sub‑sections.

### 🔍 Changes
- Add `get_missing_sections()` util
- Update tests (100 % passing)
- Docs: README + AGENTS.md

### ✅ Checklist
- [x] Lint & black
- [x] Pyright clean
- [x] Tests pass
```

Happy coding 🤖
