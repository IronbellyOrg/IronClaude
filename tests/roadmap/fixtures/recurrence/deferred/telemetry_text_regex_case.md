---
fixture: telemetry_text_regex_case
master_recurrence_row: 16
deferred: true
---

# Recurrence #16 — Telemetry/Text-Regex vs Structured Stream-JSON (DEFER stub)

> **Documented incident** (master:§Recurrence Matrix row #16):
> *"Telemetry/text-regex against structured stream-json (PARTIAL→PASS promotion,
> files_changed=0, last_task_id="", phase-name leading dash)."*
> Partition findings: `A6:F-A6-001`, `A6:F-A6-002`, `A6:F-A6-003`,
> `A6:F-A6-004`.

The cliEval telemetry layer parsed agent output with text-regex instead of the
structured `stream-json` event stream, producing PARTIAL→PASS promotion,
`files_changed=0`, empty `last_task_id`, and phase-name leading-dash artifacts.

This is a **sprint/eval-harness telemetry concern** (A6 cross-cuts A1a/A11), not
a roadmap-pipeline scanner: no roadmap pipeline component consumes a fixture to
reproduce it. Retained as an auditable stub.
