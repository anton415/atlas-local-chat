# Atlas – Local Chat (LM Studio)

Local-only chat UI for my personal AI assistant **Atlas**, running on top of **LM Studio** and a local LLM.

Atlas loads long-term memory from Markdown files and routes new “memory writes” into project-specific files (`Bank`, `Finance`, `Temple_of_Excellence`) via an OpenAI-style **tool**.

> ⚠️ This is a personal project and learning tool, **not** a production-ready app.

---

## Features

* **Local-only backend**

  * Talks to LM Studio (or any OpenAI-compatible server) at `http://127.0.0.1:1234/v1`.
  * No external API calls.

* **File-based long-term memory**

  * Loads:

    * `atlas_memory_core.md` – core, long-term facts about Anton.
    * `atlas_memory_projects.md` – overview of big projects.
    * `projects/*/memory.md` – per-project memory (Bank / Finance / Temple_of_Excellence).
  * Writes via `write_memory(file, content)` into files under `MEMORY_ROOT` (see below).

* **Project awareness**

  * Detects which project a memory write belongs to from the file path.
  * Updates the “current project” indicator (`Bank`, `Finance`, `Temple_of_Excellence`, or `General`).
  * Shows short `[memory] → Project (file)` lines in the chat.

* **Simple web UI**

  * Single chat page at `http://127.0.0.1:5050`.
  * Shows model name, backend URL, current project, and the conversation log.

* **Alternative frontends**

  * `atlas_chat.py` – terminal (CLI) chat with file-based memory.
  * `atlas_gui.py` – minimal Tkinter desktop window for chatting with Atlas.

---

## Requirements

* Python **3.9+**
* **LM Studio** (or another OpenAI-compatible server) running locally
* A downloaded chat model (default: `qwen2-7b-instruct`)
* macOS is assumed for the default `MEMORY_ROOT` (iCloud Drive path), but the code is cross-platform if you adjust the paths.

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Quick start (web UI)

1. **Start LM Studio**

   * Open LM Studio.
   * Load the model `qwen2-7b-instruct` (or any other chat-capable model).
   * Start the server on `http://127.0.0.1:1234`.

2. **Run the Flask app**

   ```bash
   python3 app.py
   ```

3. **Open the browser**

   * Visit: [http://127.0.0.1:5050](http://127.0.0.1:5050)

4. **Start chatting**

   * Type a message as Anton and send it.
   * Atlas may occasionally call the `write_memory` tool and append Markdown into your Atlas memory folder.

---

## Alternative frontends

### CLI chat (`atlas_chat.py`)

Simple terminal interface using the same memory system and `write_memory` tool.

```bash
python3 atlas_chat.py
```

You can also control which project memories are loaded at startup:

```bash
python3 atlas_chat.py --projects Bank Finance
```

If `--projects` is omitted, the default projects from `DEFAULT_PROJECTS` are loaded (see the script).

### Tkinter GUI (`atlas_gui.py`)

Minimal desktop window (single text area + input field + Send button):

```bash
python3 atlas_gui.py
```

This uses the same memory layout and tool as the CLI and web versions.

---

## Configuration

At the moment, configuration is mostly done via **constants in the code**:

* **LM backend URL**

  * `LM_BACKEND_URL` in `app.py` (web).
  * `base_url` in `atlas_chat.py` and `atlas_gui.py`.
  * Default: `http://127.0.0.1:1234`.

* **Model name**

  * `MODEL_NAME` in `app.py`, `atlas_chat.py`, `atlas_gui.py`.
  * Default: `"qwen2-7b-instruct"`.

* **Memory root folder**

  * `MEMORY_ROOT` in `memory.py`, `atlas_chat.py`, `atlas_gui.py`.
  * Default (macOS + iCloud Drive):

    ```text
    ~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Atlas
    ```

To point Atlas at another folder or model, edit these constants for now.
(A future step in the roadmap is to move these into a single config file / env variables.)

---

## Memory layout

The repository includes example memory files matching the expected structure:

* `atlas_memory.md` – overview of how the memory system works.
* `atlas_memory_core.md` – stable, long-term facts about Anton.
* `atlas_memory_projects.md` – index of big projects and their meaning.
* `projects/Bank/memory.md` – Bank project memory.
* `projects/Finance/memory.md` – Finance project memory.
* `projects/Temple_of_Excellence/memory.md` – Temple of Excellence memory.
* `memory_inbox.md` – append-only “inbox” for raw notes and session summaries.

At runtime:

1. `build_initial_messages()` in `memory.py` concatenates the core/project files and passes them as **system messages**.
2. Each client (web / CLI / GUI) exposes the same `write_memory(file, content)` tool.
3. When the model calls the tool:

   * `content` is appended to the target file under `MEMORY_ROOT`;
   * the web UI logs `[memory] → Project (file)` and updates the current project indicator.

For details and rules about what to save, see [`atlas_memory.md`](atlas_memory.md).

---

## Repository layout

High-level structure:

* **Core code**

  * `app.py` – Flask web app, LM Studio integration, tool handling.
  * `memory.py` – shared helpers for file-based memory and initial messages.
  * `atlas_chat.py` – CLI chat client.
  * `atlas_gui.py` – Tkinter GUI client.

* **UI**

  * `ui/templates/chat.html` – current chat page template.
  * `ui/static/` – static assets (CSS/JS) – currently empty, to be filled.

* **Memory & prompts**

  * `atlas_memory*.md`, `memory_inbox.md` – core memory system files.
  * `projects/**/memory.md` – per-project memory.
  * Other `atlas_*.md` – behavior prompts (Clarity Engine, Habit Engine, etc.).

    * These will eventually move into a dedicated `prompts/` folder (see roadmap).

* **Meta**

  * `requirements.txt` – Python dependencies.
  * `.gitignore` – basic Python/OS ignores.
  * `LICENSE` – MIT.

---

## Documentation

Additional docs live under `docs/`:

* [`docs/usage.md`](docs/usage.md) – how to run Atlas Local Chat (web, CLI, GUI) and how memory behaves.
* [`docs/roadmap.md`](docs/roadmap.md) – project roadmap, docs layout, and prompts layout.

---

## Screenshots

*Planned*: add 1–2 small screenshots of the web UI once the HTML/CSS stabilizes.

* Suggested location: `ui/screenshots/atlas-local-chat.png`
* Suggested snippet for this README once the file exists:

  ```markdown
  ![Atlas – Local Chat screenshot](ui/screenshots/atlas-local-chat.png)
  ```

---

## Roadmap (short version)

See [`docs/roadmap.md`](docs/roadmap.md) for details.
Upcoming themes:

* Clean DX baseline (docs, Makefile, simple CI).
* Proper HTML/CSS for the chat UI (dark theme, better layout).
* Centralized configuration for model/backend/memory.
* Small tests + GitHub Actions smoke checks.

---

## License

This project is licensed under the **MIT License** – see [`LICENSE`](LICENSE).
