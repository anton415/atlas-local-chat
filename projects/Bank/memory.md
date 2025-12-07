# Bank – Project Memory

This file stores **long-term memory** for the Bank project:
what this project is, key decisions, and dated snapshots.

---

## 1. Project identity

- Purpose: personal learning project to understand:
  - Java core / OOP / concurrency / Streams.
  - Spring Boot, DI, Flyway, JPA, etc.
  - Banking system domain (accounts, balances, transactions, ledgers).
- Tools & ecosystem: GitHub, Camunda, Docker.

---

## 2. Constraints & principles

- This is a **learning lab**, not a production bank:
  - It’s allowed to refactor aggressively and redesign architecture.
  - Priority is clarity and understanding, not shipping features fast.
- Prefer:
  - Clean architecture and domain clarity.
  - Keeping scope realistic for one person.

---

## 3. Current focus (Q4 2025 – example, adjust as needed)

- Stabilize core domain model (accounts, customers, transactions).
- Improve Spring configuration and DI usage.

---

## 4. Memory log (dated entries)

Use this template for new entries:

### [YYYY-MM-DD] – Short title

- Key decision:
- Reason:
- Impact on future work:

---

### Example

### [2025-11-30] – Bank project memory file created

- Decision: Bank project will be my main place to practice advanced Java + Spring.
- Reason: Single, consistent domain will help me see patterns and improve mastery.
- Impact: Other “toy” projects are secondary; Bank gets priority for deeper learning.

### [2025-12-01] – Bank project memory file updated

- Decision: Implementing transaction reconciliation system for better accounting insights.
- Reason: The current transaction logging is not detailed enough to support financial analysis and auditing requirements.
- Impact on future work: This will require revisiting the data models, adding new endpoints in REST API, and integrating with existing database systems.
