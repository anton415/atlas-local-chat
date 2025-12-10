# Usage – Atlas Local Chat

This document explains how to run **Atlas – Local Chat** with LM Studio, and how the file-based memory behaves across the web, CLI, and Tkinter frontends.

If you haven’t already, read the high-level overview in [`README.md`](../README.md).

---

## 1. Prerequisites

You need:

* Python **3.9+**
* **LM Studio** (or another OpenAI-compatible server) running locally
* A downloaded chat model (default in this repo: `qwen2-7b-instruct`)
* Atlas memory files in a folder matching `MEMORY_ROOT` (by default, your iCloud Drive):

  ```text
  ~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Atlas
  ```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 2. Start the language model backend

1. Open **LM Studio**.
2. Load the model `qwen2-7b-instruct` (or a compatible chat-style model).
3. Start the server on:

   ```text
   http://127.0.0.1:1234
   ```

If you use a different host/port, update `LM_BACKEND_URL` (in `app.py`) and the `base_url` in `atlas_chat.py` / `atlas_gui.py`.

---

## 3. Run the web UI (Flask)

From the project root:

```bash
python3 app.py
```

Then open your browser at:

```text
http://127.0.0.1:5050
```

### 3.1. What you see in the UI

The current `chat.html` template is intentionally minimal:

* A header with:

  * Title: **Atlas – Local Chat**
  * Model name (`MODEL_NAME`)
  * Backend URL (`LM_BACKEND_URL`)
  * A list of projects and the **current project**.
* The conversation log:

  * `Anton` messages (your input).
  * `Atlas` messages (model replies).
  * Occasional `System` messages (errors or memory hints).
* A simple input + “Send” button.
* A “New session” button.

### 3.2. “New session” behavior

The “New session” button hits the `/new` endpoint:

* Clears the **in-memory** conversation log.
* Rebuilds the messages list via `build_initial_messages()` (fresh system + memory).
* Resets the current project to `All`.

It does **not** delete or reset any files under your Atlas memory folder.

---

## 4. CLI chat (`atlas_chat.py`)

The CLI client is useful for quick tests and for using Atlas without the web UI.

Run:

```bash
python3 atlas_chat.py
```

You’ll see:

* A startup message telling you which projects are being loaded.
* A prompt:

  ```text
  Anton:
  ```

Type your message and press **Enter**. Atlas will reply in the terminal.

### 4.1. Choosing which projects to load

You can tell Atlas which project memories to load at startup:

```bash
python3 atlas_chat.py --projects Bank Finance
```

If `--projects` is omitted, `DEFAULT_PROJECTS` from the script are used:

```python
DEFAULT_PROJECTS = ["Bank", "Temple_of_Excellence", "Finance"]
```

---

## 5. Tkinter GUI (`atlas_gui.py`)

The Tkinter client gives you a very small desktop chat window.

Run:

```bash
python3 atlas_gui.py
```

You get:

* A scrollable chat area showing:

  * Your messages (`Anton: ...`)
  * Atlas replies
  * `[memory] appended to ...` when the model writes memory
* A single-line input field + Send button.

This client uses the same memory loading (`build_initial_messages`) and `write_memory` tool as the CLI and web versions.

---

## 6. How the file-based memory works (runtime view)

All three frontends share the same core memory logic from `memory.py`:

1. On startup, they call `build_initial_messages()`:

   * This loads:

     * `atlas_memory_core.md`
     * `atlas_memory_projects.md`
     * `projects/*/memory.md` for each selected project
   * It concatenates them into a single **system message** (`memory_message`).
2. They also send a **behavior system prompt** that explains:

   * What the projects mean (`Bank`, `Finance`, `Temple_of_Excellence`).
   * When the model should use the `write_memory` tool.
3. During the chat:

   * Atlas replies as usual.

   * Sometimes it calls:

     ```text
     write_memory(file, content)
     ```

   * The client appends `content` to the given `file` under `MEMORY_ROOT` using `append_to_file()`.

### 6.1. Where the files live

By default:

* `MEMORY_ROOT` in code:

  ```python
  MEMORY_ROOT = "~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Atlas"
  ```

* Under this folder you should have (at least):

  * `atlas_memory_core.md`
  * `atlas_memory_projects.md`
  * `memory_inbox.md`
  * `projects/Bank/memory.md`
  * `projects/Finance/memory.md`
  * `projects/Temple_of_Excellence/memory.md`

You can keep *example* versions of these files in this repo (as you do now) and periodically sync them with the “real” Atlas folder.

For detailed rules on **what** to save, see [`atlas_memory.md`](../atlas_memory.md).

---

## 7. Project awareness in the web UI

In the web app (`app.py`):

* `project_from_file(file)` infers the project name from the file path:

  * `projects/Bank/...` → `Bank`
  * `projects/Finance/...` → `Finance`
  * `projects/Temple_of_Excellence/...` → `Temple_of_Excellence`
  * anything else → `General`
* When a `write_memory` call succeeds:

  * The web UI logs `[memory] → Project (file)` as a `System` message.
  * `current_project` is updated and displayed in the header.

This gives you a lightweight sense of “where” the last memory write landed, without manually switching projects.

---

## 8. Known limitations (current state)

* Configuration (model, backend URL, memory root) is **hard-coded** in multiple files.
* The HTML template is intentionally minimal and lacks proper layout and styling.
* There are no automated tests yet.
* There is no CI pipeline yet.

The **roadmap** in [`docs/roadmap.md`](docs/roadmap.md) describes planned work to improve these areas.
