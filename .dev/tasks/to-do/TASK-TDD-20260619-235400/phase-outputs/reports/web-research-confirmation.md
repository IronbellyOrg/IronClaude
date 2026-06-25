# Web Research Confirmation (Step 4.1) — TASK-TDD-20260619-235400

**Date:** 2026-06-20

- **Web file exists & non-empty:** YES — `research/web-01-inprocess-import-vs-subprocess-fanout.md` (164 lines, Status: Complete, Tavily-sourced).
- **HIGH-relevance findings (with source URLs):**
  - A1 — Nested sub-agent spawning silently fails; flat/in-process is the remedy. https://github.com/anthropics/claude-code/issues/61993
  - A2 — In-process contexts may lack the spawn primitive entirely. https://github.com/anthropics/claude-code/issues/31977
  - A3 — "import is generally vastly preferable to spawning a separate process." https://stackoverflow.com/questions/48862112/subprocess-or-import-to-invoke-a-script-in-python
  - B1 — ThreadPoolExecutor is the recommended executor for I/O-bound fan-out. https://docs.python.org/3/library/concurrent.futures.html
  - B2 — submit + as_completed + per-future try/except fan-out/fan-in. https://stackoverflow.com/questions/79390382/parallelize-a-list-of-subsequent-api-calls-in-python
  - C1 — OpenAI-compatible proxy: one client, swap model=, fan out over N models. https://www.truefoundry.com/blog/what-is-multi-model-orchestration
  - C2 — LiteLLM batch_completion_models (off-the-shelf parallel multi-model). https://docs.litellm.ai/docs/completion/batching
- **Usable for:** §21 Alternatives Considered (validates in-process-import-over-subprocess thesis A1/A2/A3; frames the 3-option table) and §6 design-decision rationale.
- **Residual external gap for synthesis to flag:** none material. The aggregation policy is settled by the spec (`/sc:adversarial` Mode A is the scorer, not statistical voting); the only open external note is to validate any library/proxy config against `~/.aienv` without probing the proxy API — already a §22 hygiene note. Single-backend (Tavily only) caveat noted, non-blocking for an internal-infra TDD.

**Status:** Web research available and synthesis-ready. No additional external agents required.
