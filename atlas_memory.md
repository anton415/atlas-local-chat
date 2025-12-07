# Atlas – Memory System Overview

This file explains **how my file-based memory works**.

---

## 1. Main memory files

- `atlas_memory_core.md` – who I am, core values, long-term direction.
- `atlas_memory_projects.md` – index of big projects and their meaning.
- `projects/<Project>/memory.md` – per-project memory (Bank, Temple_of_Excellence, Finance, etc.).
- `memory_inbox.md` – raw dump of new memory fragments.

---

## 2. Rules: what deserves memory?

✅ Save when:

- It will matter for **months or years**.
- It affects decisions (rules, constraints, preferences).
- It describes a stable pattern in my behavior or life.
- It captures the “shape” of an important project.

❌ Don’t save:

- Random daily noise, rants, or fleeting moods.
- Exact step-by-step logs (keep those in journals, not memory).
- Anything that I can easily regenerate later and don’t need as context.

---

## 3. Weekly Memory Review (ritual)

Once per week:

1. Open `memory_inbox.md`.
2. For each entry:
   - If important long-term → move and compress into:
     - `atlas_memory_core.md`, or
     - `atlas_memory_projects.md`, or
     - `projects/<Project>/memory.md`
   - If no longer useful → delete.
3. Keep all memory files **short and dense**.
4. Optionally, note bigger updates in a small log at the end of each file.

---

## 4. Session Startup (for LM Studio / Atlas)

At the start of a new session:

1. Load `atlas_memory_core.md`.
2. Load `atlas_memory_projects.md`.
3. Load **1–2 relevant project memory files** (for today’s focus), e.g.:
   - `projects/Bank/memory.md`
   - `projects/Finance/memory.md`
4. If needed, quickly scan `memory_inbox.md` for fresh, unprocessed items.

---

## 5. Future extension ideas

- Small script that concatenates selected memory files into `atlas_memory_session.md`.
- Versioning old memory (archive files by year if they grow too large).

---

## 6. Update log

- [2025-11-30] Initial structure and rules defined for Task 20.
