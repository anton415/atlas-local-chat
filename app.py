import os
import json

from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from memory import (
    MEMORY_ROOT,
    DEFAULT_PROJECTS,
    append_to_file,
    build_initial_messages,
)

# Базовая папка проекта (там, где лежит app.py)
BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "ui" / "templates"),
    static_folder=str(BASE_DIR / "ui" / "static"),
)

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
    return render_template(
        "chat.html",
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

