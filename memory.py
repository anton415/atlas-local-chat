import os

# Path to Atlas folder (adjust if different)
MEMORY_ROOT = "~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Atlas"

# Projects to load by default
DEFAULT_PROJECTS = ["Bank", "Temple_of_Excellence", "Finance"]

# === FILE HELPERS ===

def full_path(relpath: str) -> str:
    root = os.path.expanduser(MEMORY_ROOT)
    return os.path.join(root, relpath)

def read_file(relpath: str) -> str:
    try:
        with open(full_path(relpath), "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"# {relpath} (created automatically)\n"


def append_to_file(relpath: str, content: str) -> None:
    path = full_path(relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + content)

# === MEMORY LOADING ===

def load_memory(projects=None):
    if projects is None:
        projects = DEFAULT_PROJECTS

    parts = []

    core_files = ["atlas_memory_core.md", "atlas_memory_projects.md"]
    for rel in core_files:
        parts.append(f"===== {rel} =====\n{read_file(rel)}")

    for proj in projects:
        rel = f"projects/{proj}/memory.md"
        parts.append(f"===== {rel} =====\n{read_file(rel)}")

    return "\n\n".join(parts)


def build_initial_messages(projects=None):
    memory_blob = load_memory(projects)

    system_prompt = """
You are Atlas, Anton's personal AI assistant, running locally.

You have a file-based memory system stored as Markdown files in a folder called "Atlas".
At the start of the session, you receive the current contents of those files.
Treat that as your long-term memory.

Projects whose memories are loaded by default:
- Bank  → software engineering, Java/Spring, banking domain, code, architecture.
- Finance → personal finance, FIRE, investments, budget, portfolio.
- Temple_of_Excellence → life strategy, long-term goals, health, systems, meta-planning.

Your job:
- For each user message, decide which project(s) it belongs to.
  - If it's about coding, architecture, banking system → Bank.
  - If it's about money, savings, FIRE, investments → Finance.
  - If it's about life structure, goals, habits, health, meta-systems → Temple_of_Excellence.
  - If it doesn't clearly fit, use memory_inbox.md as a neutral place.

You also have access to a tool called `write_memory(file, content)` which appends Markdown to these files.
Use this tool when you want to save something that should persist across sessions
(e.g. new rules, stable preferences, project decisions, compact session summaries).

When you write memory:
- Default:
    - use "memory_inbox.md" for raw session summaries,
    - use "projects/Bank/memory.md" for Bank-related decisions,
    - use "projects/Finance/memory.md" for finance-related decisions,
    - use "projects/Temple_of_Excellence/memory.md" for life-strategy decisions.
- Always write short, dense Markdown blocks with a date and heading, e.g.:

  ### [2025-11-30] – Bank – decision about transaction model
  - ...

- Save only information that will matter for weeks or months.
- Do NOT save random transient moods, throwaway examples, or full transcripts.

Very important:
- Even when you call the `write_memory` tool, you must still answer the user normally.
- Keep answers structured, calm, and not too long.
- Often end with 1–3 realistic next steps for Anton.
""".strip()

    memory_message = (
        "Here is your current long-term memory, collected from multiple Markdown files.\n"
        "You should use it as context but not repeat it back.\n\n"
        + memory_blob
    )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": memory_message},
    ]