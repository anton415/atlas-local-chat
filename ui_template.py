# ui_template.py
# Holds the HTML template for Atlas UI

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Atlas – Local Chat</title>
  <style>
    :root {
      --bg: #020617;
      --bg-elevated: #020617;
      --border-subtle: #1f2937;
      --border-strong: #334155;
      --text-main: #e5e7eb;
      --text-muted: #9ca3af;
      --accent: #22c55e;
      --accent-soft: rgba(34, 197, 94, 0.1);
    }

    body.project-all { --accent: #22c55e; }      /* default teal */
    body.project-bank { --accent: #38bdf8; }     /* blue-ish for Bank */
    body.project-finance { --accent: #22c55e; }  /* green for Finance */
    body.project-temple { --accent: #a855f7; }   /* purple for Temple_of_Excellence */


    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      padding: 24px;
      font-family: -apple-system, system-ui, BlinkMacSystemFont, "SF Pro Text", sans-serif;
      background: radial-gradient(circle at top, #020617 0, #020617 45%, #000 100%);
      color: var(--text-main);
      display: flex;
      justify-content: center;
    }

    main {
      width: 100%;
      max-width: 980px;
    }

    h1 {
      margin: 0 0 6px;
      font-size: 28px;
      letter-spacing: 0.02em;
    }

    .subtitle {
      margin-bottom: 24px;
      color: var(--text-muted);
      font-size: 13px;
      line-height: 1.4;
    }

    .subtitle .meta {
      display: block;
      margin-top: 4px;
      font-size: 12px;
      color: #6b7280;
    }

    .chat-shell {
      border-radius: 18px;
      border: 1px solid var(--border-subtle);
      background: linear-gradient(to bottom right, rgba(15,23,42,0.95), rgba(15,23,42,0.98));
      box-shadow:
        0 18px 40px rgba(0,0,0,0.75),
        0 0 0 1px rgba(15,23,42,0.9);
      padding: 18px 18px 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      min-height: 460px;
    }

    .messages {
      border-radius: 14px;
      padding: 14px 14px 6px;
      border: 1px solid var(--border-subtle);
      background: radial-gradient(circle at top left, rgba(15,23,42,0.9) 0, rgba(15,23,42,1) 60%, #020617 120%);
      overflow-y: auto;
      max-height: 60vh;
      scrollbar-color: #4b5563 #020617;
      scrollbar-width: thin;
    }

    .messages::-webkit-scrollbar {
      width: 6px;
    }
    .messages::-webkit-scrollbar-track {
      background: #020617;
    }
    .messages::-webkit-scrollbar-thumb {
      background: #4b5563;
      border-radius: 999px;
    }

    .bubble {
      margin-bottom: 10px;
      padding: 10px 12px;
      border-radius: 14px;
      font-size: 14px;
      line-height: 1.45;
      white-space: pre-wrap;
    }

    .msg-user {
      align-self: flex-end;
      background: linear-gradient(to bottom right, #0f172a, #020617);
      border: 1px solid var(--border-strong);
    }

    .msg-user strong {
      color: var(--accent);
    }

    .msg-atlas {
      align-self: flex-start;
      background: radial-gradient(circle at top left, var(--accent-soft) 0, rgba(15,23,42,1) 55%);
      border: 1px solid var(--border-strong);
    }

    .msg-atlas strong {
      color: var(--accent);
    }

    .msg-system {
      align-self: center;
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 11px;
      color: var(--text-muted);
      border: 1px dashed var(--border-subtle);
      background: rgba(15,23,42,0.9);
      white-space: pre-wrap;
    }

    form {
      margin-top: 4px;
    }

    textarea {
      width: 100%;
      min-height: 120px; /* bigger input */
      max-height: 220px;
      resize: vertical;
      border-radius: 14px;
      border: 1px solid var(--border-strong);
      background: #020617;
      color: var(--text-main);
      font-size: 14px;
      padding: 10px 12px;
      outline: none;
      font-family: inherit;
      line-height: 1.4;
    }

    textarea:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 1px rgba(34,197,94,0.6);
    }

    .typing {
      display: none;
      align-items: center;
      gap: 6px;
      margin-top: 4px;
      font-size: 11px;
      color: var(--text-muted);
    }

    .dot {
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: var(--accent);
      opacity: 0.4;
      animation: bounce 1.2s infinite ease-in-out;
    }

    .dot:nth-child(1) { animation-delay: 0s; }
    .dot:nth-child(2) { animation-delay: 0.15s; }
    .dot:nth-child(3) { animation-delay: 0.3s; }

    @keyframes bounce {
      0%, 80%, 100% { transform: translateY(0); opacity: 0.2; }
      40% { transform: translateY(-4px); opacity: 1; }
    }

    .typing-text {
      opacity: 0.8;
    }

    .actions-row {
      margin-top: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
      justify-content: flex-end;
    }

    button[type="submit"] {
      border-radius: 999px;
      padding: 7px 16px;
      border: 1px solid transparent;
      background: linear-gradient(to bottom right, #22c55e, #16a34a);
      color: #020617;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 10px 25px rgba(34,197,94,0.45);
      transition: transform 0.06s ease-out, box-shadow 0.06s ease-out, opacity 0.06s;
    }

    button[type="submit"]:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 14px 32px rgba(34,197,94,0.6);
    }

    button[type="submit"]:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: 0 6px 16px rgba(34,197,94,0.45);
    }

    button[type="submit"]:disabled {
      opacity: 0.6;
      cursor: default;
      box-shadow: none;
    }

    .hint {
      font-size: 11px;
      color: var(--text-muted);
      margin-right: auto;
    }

    a {
      color: var(--accent);
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }

    @media (max-width: 768px) {
      body { padding: 16px; }
      .chat-shell { padding: 14px 12px; }
      .messages { max-height: 55vh; }
    }

    .chat-top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .chat-top-bar .status-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: #22c55e;
      box-shadow: 0 0 8px rgba(34,197,94,0.9);
      margin-right: 6px;
    }

    .meta-line {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
      font-size: 11px;
      opacity: 0.8;
    }

    .meta-line .who {
      font-weight: 600;
    }

    .meta-line .time {
      font-variant-numeric: tabular-nums;
      color: var(--text-muted);
    }

    .secondary-btn {
      border-radius: 999px;
      padding: 5px 12px;
      font-size: 11px;
      border: 1px solid var(--border-strong);
      background: #020617;
      color: var(--text-muted);
      cursor: pointer;
      transition: background 0.08s ease-out, color 0.08s ease-out, border-color 0.08s;
    }

    .secondary-btn:hover {
      background: #0b1120;
      color: var(--text-main);
      border-color: var(--accent);
    }

  </style>
</head>
<body class="project-{{ current_project_slug }}">
  <main>
    <h1>Atlas – Local Chat</h1>
    <div class="subtitle">
      Anton: How can you help me today?
      <span class="meta">
        Model: {{ model_name }} · Backend: {{ backend_url }} ·
        Projects: Bank · Finance · Temple of Excellence ·
        Current: {{ current_project.replace('_', ' ') }}
      </span>
    </div>

    <div class="chat-shell">
          <div class="chat-top-bar">
            <div>
              <span class="status-dot"></span>
              <span>Session active</span>
            </div>
            <form method="post" action="{{ url_for('new_session') }}">
              <button type="submit" class="secondary-btn">New session</button>
            </form>
          </div>

      <div class="messages" id="messages">
        {% for msg in conversation %}
          {% if msg.speaker == 'Anton' %}
            <div class="bubble msg-user">
              <div class="meta-line">
                <span class="who">Anton</span>
                <span class="time">{{ msg.time }}</span>
              </div>
              <div>{{ msg.text }}</div>
            </div>
          {% elif msg.speaker == 'Atlas' %}
            <div class="bubble msg-atlas">
              <div class="meta-line">
                <span class="who">Atlas</span>
                <span class="time">{{ msg.time }}</span>
              </div>
              <div>{{ msg.text }}</div>
            </div>
          {% else %}
            <div class="msg-system">
              {{ msg.text }} · {{ msg.time }}
            </div>
          {% endif %}
        {% endfor %}
      </div>


      <div class="typing" id="typing-indicator">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="typing-text">Atlas is thinking…</span>
      </div>

      <form id="chat-form" method="post">
        <textarea
          id="user-input"
          name="user_input"
          autofocus
          placeholder="Type your message…  (Enter = send, Shift+Enter = new line)"
        ></textarea>
        <div class="actions-row">
          <span class="hint">Enter to send · Shift+Enter for new line</span>
          <button type="submit">Send</button>
        </div>
      </form>
    </div>
  </main>

  <script>
    (function () {
      const form = document.getElementById('chat-form');
      const textarea = document.getElementById('user-input');
      const messages = document.getElementById('messages');
      const typing = document.getElementById('typing-indicator');
      const submitBtn = form.querySelector('button[type="submit"]');

      // Auto-scroll to bottom on load
      if (messages) {
        messages.scrollTop = messages.scrollHeight;
      }

      // Keyboard submit: Enter = send, Shift+Enter = newline
      textarea.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          if (textarea.value.trim().length === 0) return;
          if (form.requestSubmit) {
            form.requestSubmit();  // triggers 'submit' event
          } else {
            form.submit();
          }
        }
      });

      // Show "Atlas is thinking…" and disable input on submit
      form.addEventListener('submit', function (e) {
        if (textarea.value.trim().length === 0) {
          e.preventDefault();
          return;
        }
        typing.style.display = 'flex';
        textarea.readOnly = true;
        submitBtn.disabled = true;
      });

      // Focus textarea on load
      textarea.focus();
    })();
  </script>
</body>
</html>
"""
