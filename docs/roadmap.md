# Roadmap – Atlas Local Chat

This document describes how I plan to evolve **Atlas – Local Chat**:

* keep it **simple** and local-only,
* make it **pleasant to work on** (DX),
* avoid over-engineering.

It also defines where documentation and prompts should live in this repo.

---

## 0. Current status (Dec 2025)

* Working pieces:

  * Web app (`app.py`) with minimal template (`ui/templates/chat.html`).
  * CLI client (`atlas_chat.py`) and Tkinter GUI (`atlas_gui.py`).
  * Shared file-based memory system (`memory.py`).
  * Core memory files and project memory files under `Atlas` folder.
* Missing / weak:

  * No proper HTML/CSS layout for the web UI.
  * No tests, no CI.
  * Configuration duplicated across several scripts.
  * Docs scattered (`atlas_memory*.md`, `atlas_*_engine.md`, etc. in repo root).

---

## 1. Documentation & prompts layout

### 1.1. Docs (`docs/`)

Use `docs/` for **how-to and architecture docs**:

* `docs/usage.md` – how to run Atlas Local Chat (web / CLI / GUI), how memory behaves.
* `docs/roadmap.md` – this file.
* Future ideas:

  * `docs/architecture.md` – high-level description of components and data flow.
  * `docs/dev-notes.md` – notes about local dev setup, common pitfalls, etc.

### 1.2. Prompts (`prompts/`)

Use a dedicated `prompts/` folder for **reusable system prompts** that Atlas can load, but which are not “memory”:

* `prompts/atlas_clarity_engine.md`
* `prompts/atlas_emotion_protocol.md`
* `prompts/atlas_emotional_timeline.md`
* `prompts/atlas_habits.md`
* `prompts/atlas_planning.md`
* `prompts/atlas_projects.md`
* etc.

Later, Atlas can dynamically choose which prompt to load based on the current mode (Clarity Engine, Focus Engine, etc.).

### 1.3. Memory files (stay as “memory”)

Keep memory files where they are conceptually:

* `atlas_memory*.md`, `memory_inbox.md`
* `projects/*/memory.md`

These represent **long-term facts and project history**, not behavior prompts.

> Rule of thumb:
>
> * “How Atlas should behave” → `prompts/`
> * “What Anton’s life/project looks like” → memory files.

---

## 2. Short-term plan (v0.2 – DX baseline)

Focus: make the project **comfortable to work on** without changing core behavior.

**Goals**

* Clear entry points and docs.
* Minimal but useful automation.

**Planned tasks (convert each line into a GitHub Issue):**

* [ ] README v2 with:

  * clear overview, requirements, configuration section,
  * links to `docs/usage.md` and `docs/roadmap.md`.
* [ ] Add `docs/usage.md` and `docs/roadmap.md` (this roadmap).
* [ ] Create a `prompts/` folder and move `atlas_*_engine.md`-style files there.
* [ ] Add a small `Makefile` with common commands:

  * `make run-web` → `python3 app.py`
  * `make chat` → `python3 atlas_chat.py`
  * `make gui` → `python3 atlas_gui.py`
  * `make lint` / `make format` (to be wired once tools are chosen).
* [ ] Tighten `.gitignore` only if needed (for now `.venv/`, `__pycache__/`, `*.pyc`, `.DS_Store` are enough).

---

## 3. Medium-term plan (v0.3 – UI & configuration)

Focus: make the UI pleasant and centralize configuration.

**UI / UX**

* [ ] Replace `ui/templates/chat.html` with a proper HTML layout:

  * Header bar (title, model, backend, current project).
  * Scrollable chat area with clear styling for Anton / Atlas / System.
  * Input area + Send button at the bottom.
* [ ] Add basic CSS in `ui/static/styles.css`:

  * Dark theme compatible with macOS dark mode.
  * Reasonable font sizes and spacing.
* [ ] Optional: add a lightweight indicator when Atlas is “thinking”.

**Configuration**

* [ ] Create a small config module (e.g. `config.py`) or `.env` loading:

  * backend URL,
  * default model name,
  * memory root path,
  * default projects.
* [ ] Update `app.py`, `atlas_chat.py`, `atlas_gui.py`, `memory.py` to import from that single config instead of duplicating constants.

---

## 4. Longer-term ideas (v0.4+ – testing, CI, niceties)

Focus: confidence and automation, without turning this into a huge framework.

**Testing & CI**

* [ ] Add a `tests/` folder with at least:

  * a smoke test that imports `app.py` and checks that the Flask app can be created,
  * a test for `load_memory()` (using temporary files instead of real iCloud).
* [ ] Add a GitHub Actions workflow:

  * install dependencies,
  * run `python -m compileall .` as a very cheap syntax check,
  * run tests (if present).

**Developer experience**

* [ ] Decide on a minimal lint/format combo (e.g. `ruff` + `black`) and wire them into:

  * `Makefile` targets,
  * optional `pre-commit` hook.
* [ ] Add a short `docs/dev-notes.md` describing the usual dev loop.

**Possible future features (only if they clearly help Anton)**

* [ ] Ability to select a “mode” (Clarity Engine, Focus Engine, etc.) in the UI, which picks a system prompt from `prompts/`.
* [ ] Option to choose which projects to load from the web UI (not only via CLI).
* [ ] Support for multiple models or backends (e.g. “fast” vs “deep” models).

---

## 5. What not to do (anti-goals)

To keep the project realistic and maintainable:

* ❌ No multi-user support, auth, or accounts.
* ❌ No heavy frontend framework (React, Vue, etc.) unless it becomes clearly necessary.
* ❌ No attempt to turn this into a general-purpose chat platform.
* ❌ No complex plugin system inside this repo (Atlas-level complexity belongs in Atlas itself, not in this small web/CLI wrapper).

This roadmap should stay short and practical.
If something feels like “a big platform,” it probably belongs in the **Atlas OS** vision, not in this repo.
