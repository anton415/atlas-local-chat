import os
import json
from tkinter import Tk, Text, Entry, Button, END, DISABLED, NORMAL
from tkinter.scrolledtext import ScrolledText

from openai import OpenAI

# === CONFIG ===

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",  # LM Studio local server
    api_key="lm-studio",                  # any string
)

MODEL_NAME = "qwen2-7b-instruct"

# Путь к папке Atlas (как в прошлых скриптах)
MEMORY_ROOT = "~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Atlas"

# Какие проекты грузим по умолчанию
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


# === GUI APP ===

class AtlasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Atlas – Local Chat")

        # История чата
        self.chat = ScrolledText(root, wrap="word", state=DISABLED, width=80, height=24)
        self.chat.pack(padx=8, pady=8)

        # Поле ввода
        self.entry = Entry(root, width=70)
        self.entry.pack(side="left", padx=(8, 0), pady=(0, 8))
        self.entry.bind("<Return>", self.on_send)

        # Кнопка отправки
        self.send_button = Button(root, text="Send", command=self.send_message)
        self.send_button.pack(side="left", padx=8, pady=(0, 8))

        # Сообщения для модели
        self.messages = build_initial_messages()

        self.log("Atlas initialized with file-based memory.\n")

    def log(self, text: str):
        self.chat.config(state=NORMAL)
        self.chat.insert(END, text)
        self.chat.see(END)
        self.chat.config(state=DISABLED)

    def on_send(self, event):
        self.send_message()

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        # Показать пользователя в чате
        self.log(f"Anton: {user_text}\n")
        self.entry.delete(0, END)

        # Добавить в историю сообщений
        self.messages.append({"role": "user", "content": user_text})

        # Вызвать модель
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.messages,
                tools=TOOLS,
                tool_choice="auto",
            )
        except Exception as e:
            self.log(f"Atlas (error): {e}\n\n")
            return

        msg = resp.choices[0].message

        # Показать ответ ассистента
        if msg.content:
            self.log(f"Atlas: {msg.content}\n\n")

        # Сохранить сообщение в историю
        self.messages.append(
            {
                "role": msg.role,
                "content": msg.content,
                "tool_calls": msg.tool_calls,
            }
        )

        # Обработать tool_calls (write_memory)
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments or "{}")

                if name == "write_memory":
                    file = args["file"]
                    content = args["content"]
                    append_to_file(file, content)
                    self.log(f"[memory] appended to {file}\n")

            # Если хочешь, можно сделать второй запрос, чтобы Atlas отреагировал
            # на результат tools, но для памяти это не обязательно.

    def run(self):
        self.root.mainloop()


def main():
    root = Tk()
    app = AtlasApp(root)
    app.run()


if __name__ == "__main__":
    main()

