import os
import json

from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for
from openai import OpenAI
from ui_template import TEMPLATE

# === CONFIG ===

LM_BACKEND_URL = "http://127.0.0.1:1234"  # LM Studio server (without /v1)

client = OpenAI(
    base_url=f"{LM_BACKEND_URL}/v1",  # LM Studio local server
    api_key="not-needed",
)

MODEL_NAME = "qwen2-7b-instruct"

PROJECT_SLUGS = {
    "All": "all",
    "General": "all",
    "Bank": "bank",
    "Finance": "finance",
    "Temple_of_Excellence": "temple",
}

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


# === TOOL DEFINITIONS ===

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_memory",
            "description": (
                "Append Markdown content to one of Anton's memory files. "
                "Use this to store long-term facts, decisions, or summaries."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": (
                            "Relative path to the memory file from the Atlas root, "
                            "e.g. 'memory_inbox.md' or 'projects/Bank/memory.md'."
                        ),
                    },
                    "content": {
                        "type": "string",
                        "description": "Markdown content to append. Include date headings yourself.",
                    },
                },
                "required": ["file", "content"],
            },
        },
    }
]


# === WEB APP ===

app = Flask(__name__)

# Conversation + messages in memory (per server run)
conversation = []           # list of dicts: {speaker, text, time}
messages = build_initial_messages()
current_project = "All"     # used only for UI accent

def now_time():
    return datetime.now().strftime("%H:%M")

def project_from_file(file: str) -> str:
    if file.startswith("projects/Bank/") or file == "projects/Bank/memory.md":
        return "Bank"
    if file.startswith("projects/Finance/") or file == "projects/Finance/memory.md":
        return "Finance"
    if file.startswith("projects/Temple_of_Excellence/") or file == "projects/Temple_of_Excellence/memory.md":
        return "Temple_of_Excellence"
    return "General"


def display_project(project: str) -> str:
    # For UI: "Temple_of_Excellence" -> "Temple of Excellence"
    return project.replace("_", " ")


@app.route("/", methods=["GET", "POST"])
def index():
    global messages, conversation, current_project

    if request.method == "POST":
        user_text = (request.form.get("user_input") or "").strip()
        if user_text:
            # Log user message
            conversation.append(
                {
                    "speaker": "Anton",
                    "text": user_text,
                    "time": now_time(),
                }
            )
            messages.append({"role": "user", "content": user_text})

            # Call LM Studio
            try:
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                )
            except Exception as e:
                conversation.append(
                    {
                        "speaker": "System",
                        "text": f"Atlas (error): {e}",
                        "time": now_time(),
                    }
                )
                return redirect(url_for("index"))

            msg = resp.choices[0].message

            # Log Atlas reply
            if msg.content:
                conversation.append(
                    {
                        "speaker": "Atlas",
                        "text": msg.content,
                        "time": now_time(),
                    }
                )

            # Keep full message (incl. tool calls) for next round
            messages.append(
                {
                    "role": msg.role,
                    "content": msg.content,
                    "tool_calls": msg.tool_calls,
                }
            )

            # Handle memory tool calls
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments or "{}")
                    if name == "write_memory":
                        file = args["file"]
                        content = args["content"]
                        append_to_file(file, content)

                        project = project_from_file(file)
                        current_project = project

                        conversation.append(
                            {
                                "speaker": "System",
                                "text": f"[memory] → {display_project(project)} ({file})",
                                "time": now_time(),
                            }
                        )

        return redirect(url_for("index"))

    # GET: render page
    return render_template_string(
        TEMPLATE,
        conversation=conversation,
        model_name=MODEL_NAME,
        backend_url=LM_BACKEND_URL,
        current_project=current_project,
        current_project_slug=PROJECT_SLUGS.get(current_project, "all"),
    )


@app.route("/new", methods=["POST"])
def new_session():
    global conversation, messages, current_project
    conversation = []
    messages = build_initial_messages()
    current_project = "All"
    return redirect(url_for("index"))




if __name__ == "__main__":
    # Run on localhost:5050 (avoid conflicts)
    app.run(host="127.0.0.1", port=5050, debug=False)


