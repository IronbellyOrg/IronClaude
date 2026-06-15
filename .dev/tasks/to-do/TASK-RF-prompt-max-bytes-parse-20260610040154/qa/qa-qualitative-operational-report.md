# QA Report — Task Qualitative (Operational Correctness)

**Topic:** Defensive parse for SUPERCLAUDE_PROMPT_MAX_BYTES (PR #156 review fix)
**Date:** 2026-06-10
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

Two MINOR issues (stale line-number citations) and one IMPORTANT operational risk
(whole-repo `make lint` failure mode) found. The task is operationally sound at its
core — the fix shape is correct, grounded in real code, and would produce a working
result — but the line-number drift and the lint-scope risk are findings that must be
resolved per the no-leniency / all-severities rule.

The drift axis (AX-1) is ACTIVE: BUILD_REQUEST.GOAL verbatim is reproduced in the task
file at lines 101-102 ("References" block), so a drift baseline exists.

## Items Reviewed (5 Adversarial Axes overlay)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (worktree, pytest, python -c, make) | none | PASS | `origin/fix/pipeline-stdin-large-prompts` exists; `../IronClaude-pr156` absent (Step 1.2 creates it); `tests/cli_portify/` tree present; `make lint`/`make format` targets exist (Makefile L48/L53); current branch is `fix/prd-parallel-gate-advisory` as task claims. |
| 2 | Project convention compliance (src/ only, no .claude/, UV) | none | PASS | Both targets under `src/`+`tests/`; no `.claude/` involvement; all commands use `uv run`; conventional-commit hook (`conventional-pre-commit`, .pre-commit-config L66) satisfied by `fix(pipeline): ...` message. |
| 3 | Intra-phase execution order | none | PASS | Worktree (1.2) → edits (2.1→2.2) → tests (3.x) → lint (4.1) → QA (5.x) → commit/push (6.x) → reflect (7.1). Helper added before assignment swap; assignment-swap references helper from 2.1. No forward dependency. |
| 4 | Function signature / value verification (line numbers, int contract) | AX-1 | FAIL | Assignment is at **process.py:27-29**, not "~24-26" as task states repeatedly (24-26 is the comment block). Verified via `git show ... \| sed -n '19,31p'`. See Issue 1. `_log` at L21, `from typing import Callable, Optional` at L19, `import os`/`import logging` at L15-17 — all confirmed in scope. |
| 5 | Module context analysis | none | PASS | `_log.warning(...)` already the module's logging idiom (used in start()/wait()/terminate()); helper reuses it. `# Default 16 MiB; ...` comment at L24-26 — Step 2.2 correctly says preserve/update it. |
| 6 | Downstream consumer analysis (int contract) | none | PASS | Only consumer of `PROMPT_MAX_BYTES` is the guard in `start()` at process.py:140-143 (`if len(prompt_bytes) > PROMPT_MAX_BYTES`). `git grep` shows no other src consumers. Helper returns `int`; annotation kept `int`; consumer needs no change — confirmed. |
| 7 | Test validity (real helper, real input) | none | PASS | Step 3.1 calls `_parse_prompt_max_bytes` directly with explicit `raw` args (no import-time env coupling), asserts concrete values, bans `assert True`. caplog pattern `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")` matches the module's established pattern (test file L273). |
| 8 | Test coverage of primary use case | none | PASS | Six paths enumerated: non-integer→default+warn, ""→default+warn, "0"→default+warn, "-1"→default+warn, valid→parsed/no-warn, None→default/no-warn. Plus Step 3.3 import-safety repro exercises the real module-import path with a bad env var. |
| 9 | Error path coverage | none | PASS | Helper catches `(TypeError, ValueError)` and the `value <= 0` branch, each with a distinct warning. Step 3.1 asserts both warning variants. |
| 10 | Runtime failure path trace (import → guard) | none | PASS | Trace: bad env → `os.environ.get(...)` returns str → helper `try int()` raises → caught → default returned → module import succeeds → `start()` guard reads int. No remaining import-time raise path. Step 3.3 demonstrates it (`SUPERCLAUDE_PROMPT_MAX_BYTES=16MB uv run python -c "import ...; print(p.PROMPT_MAX_BYTES)"` must print 16777216). |
| 11 | Completion scope honesty | none | PASS | research-notes GAPS = "None blocking"; AMBIGUITIES = "None". No open questions ignored. |
| 12 | Ambient dependency completeness (import of helper) | AX-3 | FAIL | Step 3.1 requires the test to import `_parse_prompt_max_bytes` but does NOT explicitly instruct adding it to the existing `from superclaude.cli.pipeline.process import (...)` block (test L20-23 currently imports only `ClaudeProcess`, `PromptTooLargeForArgv`). Implicit but under-specified. See Issue 3 (MINOR). |
| 13 | Kwarg sequencing | none | PASS | Helper (2.1) defined before its only caller (2.2). `default` param has a value; call site passes only `raw`. No deferred-kwarg pattern. |
| 14 | Function existence claims | none | PASS | All "exists at" claims grep-verified: `_log` (L21), `PROMPT_MAX_BYTES` assignment (L27-29), `from typing import Callable, Optional` (L19), `class TestPromptMaxBytesGuard` (test L123), `start()` guard (L140). `_parse_prompt_max_bytes` correctly described as NOT yet existing (grep finds it only in a different task's docs, not in process.py). |
| 15 | Cross-reference accuracy (no templates) | AX-1 | FAIL | Adapted: line-number cross-refs. "TestPromptMaxBytesGuard ~123-175" — class starts at L123 (correct) but next method `test_prompt_under_cap_passes_guard` is at L152 and `test_huge_prompt_400kb...` at L178, so the "175" upper bound is approximate. "assignment ~24-26" is wrong (it's 27-29). See Issue 1/2. |

## Summary
- Checks passed: 12 / 15
- Checks failed: 3 (items 4, 12, 15)
- Critical issues: 0
- Important issues: 1
- Minor issues: 2
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Task §Overview L67, §Source Areas L107, Step 2.1 L147, Step 2.2 L185, §Key Constraints (implicit) | **Stale line-number citation (AX-1 drift).** Task says the `PROMPT_MAX_BYTES` assignment is at "~lines 24-26" / "around lines 24-26". Actual: the assignment is at **process.py:27-29**; lines 24-26 are the 3-line `# Default 16 MiB; ...` comment block. Verified by direct read of `origin/fix/pipeline-stdin-large-prompts`. Recoverable because the task pins the verbatim string `PROMPT_MAX_BYTES: int = int(os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024))` and hedges with "around", so an executor using string-anchored Edit will still land correctly. | Change every "~lines 24-26" / "around lines 24-26" reference to "lines 27-29 (the assignment; lines 24-26 are the preceding comment block)". |
| 2 | MINOR | Step 3.1 L199, §Source Areas L108 | **Approximate test-class range (AX-1 drift).** `class TestPromptMaxBytesGuard` is cited as "~lines 123-175". The class begins at L123 (correct), but the `~175` upper bound is loose — methods exist at L126, L152, and a `test_huge_prompt_400kb...` at L178. The "around" hedge makes this non-blocking, but the range is imprecise. | Soften to "the `TestPromptMaxBytesGuard` class beginning at L123" rather than asserting a closed `123-175` range, since the exact end shifts. |
| 3 | IMPORTANT | Step 4.1 L217 (`make lint`) | **Whole-repo lint scope risk (AX-3 omission).** `make lint` runs `lint-architecture` then `uv run ruff check .` — i.e., the ENTIRE worktree from cwd, not just the two changed files. If the freshly-created `fix/pipeline-stdin-large-prompts` worktree contains ANY pre-existing ruff violation in an unrelated file, `make lint` exits non-zero, yet Step 4.1's remediation clause says only "fix them in the two modified files" — leaving the executor with a failing gate it is not authorized to fix (a whole-repo lint failure may live outside src/test scope). The two target files are confirmed ruff-clean (candidate helper passes `ruff check`; current `process.py` is "already formatted"), so the change itself is fine — the risk is the gate's blast radius. | Either (a) scope the lint/format commands to the two files — `uv run ruff check src/superclaude/cli/pipeline/process.py tests/pipeline/test_process_stdin.py` and `uv run ruff format <same two>` — or (b) add an explicit clause to Step 4.1: "If `make lint` reports pre-existing violations in files NOT modified by this task, note them as out-of-scope and do not fix; the gate passes if the two target files are clean." |

## Verification Notes (positive confirmations)

- **Core defect & fix are real and correct.** The import-time bare `int(os.environ.get(...))` at process.py:27-29 is exactly the hard-fail; wrapping it in a try/except helper that falls back to default is the right fix. Step 3.3's repro (`SUPERCLAUDE_PROMPT_MAX_BYTES=16MB uv run python -c "import superclaude.cli.pipeline.process as p; print(p.PROMPT_MAX_BYTES)"` → expect `16777216`) would genuinely demonstrate it.
- **int contract preserved.** `start()` guard at L140-143 reads `PROMPT_MAX_BYTES` as a module-global int; helper returns int; annotation kept `int`. No call-site change needed — confirmed by `git grep` (no other src consumers).
- **No new imports needed.** `Optional` (L19), `os` (L15-17), `logging`/`_log` (L21) all in scope. Candidate helper passed `ruff check` (incl. `I` import-sort, `F` unused, `N` naming).
- **caplog pattern is project-canonical.** `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")` is already used in the test file (L273) for the analogous `_stdin_error` warning assertion. `import logging` already present (test L11).
- **Worktree / branch / push targeting all correct.** origin = IronbellyOrg fork; Step 6.3 confirms `git remote -v` and pushes to `origin` only. No `.claude/` staging. Conventional-commit hook satisfied. No required `verify-sync` pre-commit hook (`.pre-commit-config.yaml` L100: "pre-commit must not require" it), so Step 6.2's verify-sync worry is correctly hedged.
- **cli_portify regression target exists.** `tests/cli_portify/` present on the PR branch — Step 3.4's `uv run pytest tests/pipeline/ tests/cli_portify/` will collect.

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 14 distinct claims: assignment location (27-29), `_log` location (21), typing import (19), os/logging imports (15-17), `start()` guard consumer (140-143), no other PROMPT_MAX_BYTES src consumers (git grep), `TestPromptMaxBytesGuard` location (123), test imports (20-23), caplog pattern (273), `import logging` in test (11), worktree/branch state, origin remote topology, `tests/cli_portify/` existence, `make lint`/`format` target bodies + ruff config. Candidate helper independently ruff-checked.
2. **Specific files read:** `git show origin/fix/pipeline-stdin-large-prompts:src/superclaude/cli/pipeline/process.py`, `:tests/pipeline/test_process_stdin.py`, the task file, `research-notes.md`, `Makefile`, `pyproject.toml`, `.pre-commit-config.yaml`; `git worktree list`, `git branch -r`, `git ls-tree`, two `ruff check`/`ruff format --check` runs.
3. **If 0 issues, why trust?** Not applicable — 3 issues found. The line-number drift was caught by reading the real file and counting (`sed -n '19,31p'`), not by trusting the task's self-description; the lint-scope risk was caught by reading the actual `make lint` recipe body (`uv run ruff check .`).
4. **Web research?** None performed — this review is entirely local-file/source-bound. Tavily-first rule not triggered.

## Confidence
Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 3 | Grep (git grep / grep): 4 | Glob: 0 | Bash: 7
(Tool calls ≥ checklist items; each Bash mapped to a specific item: worktree/branch/cli_portify→item 1, line-numbers→items 4/15, consumers→item 6, test structure→items 7/12/14, make/ruff→items 2/4, pre-commit→item 2.)

## Recommendations (before execution)
1. Fix Issue 3 (IMPORTANT) — scope the Phase 4 lint/format commands to the two target files, OR add the out-of-scope-violation clause. This is the one finding that could actually halt a clean execution.
2. Fix Issues 1 & 2 (MINOR) — correct "~24-26" → "27-29" and soften the test-class range. Low risk because of string-anchored edits, but the no-leniency rule requires resolution.
3. Optionally add one sentence to Step 3.1 making the import-line addition explicit ("add `_parse_prompt_max_bytes` to the existing `from superclaude.cli.pipeline.process import (...)` block").

---

VERDICT: FAIL

Issues to resolve:
- [IMPORTANT] Step 4.1 `make lint` runs whole-repo `ruff check .`; a pre-existing unrelated violation would fail the gate with no authorized fix path. Scope to the two files or add an out-of-scope clause.
- [MINOR] Stale citation: `PROMPT_MAX_BYTES` assignment is at process.py:27-29, not the "~24-26" stated throughout (24-26 is the comment block).
- [MINOR] `TestPromptMaxBytesGuard` cited as ~123-175; class starts at L123 but the upper bound is imprecise (methods at L152, L178). Soften the range.

(All findings are recoverable; the core fix design is correct and grounded in verified source. None block the fix from working — they are precision/gate-robustness defects flagged under the all-severities-must-resolve rule.)
