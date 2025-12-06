# Atlas – Local Chat (LM Studio)

Local web UI for my personal AI assistant **Atlas**, running on top of LM Studio and a local model (qwen2-7b-instruct).

## Features

- Connects to LM Studio via OpenAI-compatible API (`http://127.0.0.1:1234/v1`).
- Dark, minimal chat UI at `http://127.0.0.1:5050`.
- File-based memory system (Markdown files in iCloud Drive / Atlas).
- Project-aware routing (Bank / Finance / Temple of Excellence / General).
- Manual project focus chips + automatic project detection when memory is written.

## Quick start

1. Start LM Studio server with `qwen2-7b-instruct`.
2. Run:

   ```bash
   python3 app.py
