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