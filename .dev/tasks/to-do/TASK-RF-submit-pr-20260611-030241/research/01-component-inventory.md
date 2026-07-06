# Research: File Inventory / Component Mapping

**Status:** Complete
**Date:** 2026-06-11

---

## Scope

Per-file inventory for the new `sc:submit-pr` skill, derived from merged-spec §2 (Component
Inventory C1–C6), §3 (Build DAG), §6.3 (test layout). For each spec-defined path: EXISTS today
or NEW? Reuse/edit targets get path + line count + key contents.

Repo root: `/config/workspace/IronClaude/`. All paths below are relative to repo root.

---

## Top-level existence gate (the three "must not exist yet" + two "must exist")

| Path | Spec expectation | Verified state | Evidence |
|------|-----------------|----------------|----------|
| `src/superclaude/skills/sc-submit-pr-protocol/` | NEW (must NOT exist) | **ABSENT** ✓ | `ls -ld` → "No such file or directory" |
| `src/superclaude/commands/submit-pr.md` | NEW (must NOT exist) | **ABSENT** ✓ | `ls -l` → "No such file or directory" |
| `tests/submit_pr/` | NEW (must NOT exist) | **ABSENT** ✓ | `ls -ld` → "No such file or directory" |
| `src/superclaude/hooks/scripts/offer-pr-review.sh` | EDIT target (must EXIST) | **EXISTS** ✓ | `-rwxr-xr-x 3409 bytes, 74 lines` |
| `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | REUSE (must EXIST) | **EXISTS** ✓ | `-rw-r--r-- 10768 bytes, 172 lines` |

The `sc-submit-pr-protocol` directory does NOT exist yet (confirmed). Build starts from a clean
slate for the skill package.

---

## Per-component file inventory (C1–C6 + DET/C3a/LG/VAL)

Source tree from spec §2 (lines 89–107) + C-table (lines 109–121). Every NEW file gets its
spec-defined purpose; EXISTS/EDIT/REUSE targets get line counts + key contents.

### C1 — Orchestrator / FSM

| # | Path | Status | Purpose (spec §2 / §5) |
|---|------|--------|------------------------|
| 1 | `src/superclaude/skills/sc-submit-pr-protocol/SKILL.md` | **NEW** | C1 orchestrator: the single FSM + ordinal gates (G-arm/G-edit/G-push) + override; hosts VAL (validator). Build DAG step [1]. |
| 2 | `src/superclaude/skills/sc-submit-pr-protocol/refs/state-machine.md` | **NEW** | The FSM spec (§5) — single source for all ordinals. **Core-purity file**: zero `gh`/`git` tokens (NFR-6/AC-9, T-N50). |
| 3 | `src/superclaude/commands/submit-pr.md` | **NEW** | `/sc:submit-pr` command (frontmatter + triggers). Mirrors `commands/auggie-review.md` convention (exists, 9559 bytes). |

### DET — Detection contract (R1-gated, gates everything)

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 4 | `src/superclaude/skills/sc-submit-pr-protocol/refs/detection-contract.md` | **NEW (R1-gated)** | UNKNOWN BOUNDARY — probe-locked YAML constant (§7). `locked:false` until R1 probe; build BLOCKS while unlocked (AC-8). Build DAG step [0] HARD GATE. |

### C2 — Poller

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 5 | `src/superclaude/skills/sc-submit-pr-protocol/refs/augment-poll.md` | **NEW** | C2 poller contract (interval ≥30s, timeout 1800s default, exp backoff 30→300). |
| 6 | `src/superclaude/skills/sc-submit-pr-protocol/scripts/poll-augment-review.sh` | **NEW** | C2 single poll → emits one JSON line for the Monitor stream. `scripts/` subdir has precedent (see Conventions). |

### C3 / C3a / C3b — Severity router, verify wave, dispatcher

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 7 | `src/superclaude/skills/sc-submit-pr-protocol/refs/severity-routing.md` | **NEW** | C3 re-grade + tier map; **defers to** `severity-rubric.md` (REUSE). Core-purity file (no `gh`/`git`, T-N50). |
| 8 | `src/superclaude/skills/sc-submit-pr-protocol/refs/finding-verify.md` | **NEW** | C3a verify-before-remediate wave (FR-3.5). Read-only grounding; reuses `sc-auggie-review` grounding + `sc-troubleshoot` adversarial discipline. Inside core-purity boundary. |
| 9 | `src/superclaude/skills/sc-submit-pr-protocol/refs/troubleshoot-dispatch.md` | **NEW** | C3b finding→`/sc:troubleshoot` seeding contract (verified findings only). |

### C4 — Reply / resolve helper

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 10 | `src/superclaude/skills/sc-submit-pr-protocol/refs/thread-reply.md` | **NEW** | C4 `gh api` reply + GraphQL `resolveReviewThread` contract. |
| 11 | `src/superclaude/skills/sc-submit-pr-protocol/scripts/reply-resolve-thread.sh` | **NEW** | C4 REST reply + GraphQL `resolveReviewThread` wrapper script. |

### LG — Loop-guard

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 12 | `src/superclaude/skills/sc-submit-pr-protocol/refs/loop-guard.md` | **NEW** | FR-6 round-counter invariants (INV-001) + run-log schema (§11). **Core-purity file** (no `gh`/`git`, T-N50). |

### C5 — Hook EDIT

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 13 | `src/superclaude/hooks/scripts/offer-pr-review.sh` | **EDIT (exists, 74 lines)** | Add `sc:submit-pr --monitor` mention alongside the existing `/sc:auggie-review` offer (FR-7.1). Exact current content captured below. |

### C6 — Tests

| # | Path | Status | Purpose |
|---|------|--------|---------|
| 14 | `tests/submit_pr/` (whole dir: 22 test modules + `conftest.py` + `__init__.py` + `fixtures/` w/ 18 fixtures) | **NEW** | C6 FSM/unit/edge/failure-mode tests + AC fixtures (§6.3, lines 426–469). 115 tests total (§6.1). |

---

## Reuse / Edit target detail (with line counts + key contents)

### REUSE — `severity-rubric.md` (C3 consumes via `severity-routing.md`)

- **Path:** `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`
- **Status:** EXISTS — 172 lines, 10768 bytes.
- **Reuse mode:** C3 (`severity-routing.md`) **defers to** this rubric (spec C-table line 114:
  "**Reuse** `severity-rubric.md`"). Not edited; referenced. QD-6 (§20) wants the rubric tested
  independently (`test_severity_router.py`).
- **Synced copy present:** `.claude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`
  (10768 bytes — byte-identical, confirms sync-dev parity).
- **R3 covers the rubric's content/API in depth** — not duplicated here.

### EDIT — `offer-pr-review.sh` (C5) — EXACT current content

- **Path:** `src/superclaude/hooks/scripts/offer-pr-review.sh`
- **Status:** EXISTS — 74 lines, 3409 bytes, executable (`-rwxr-xr-x`).
- **Hook type:** `PostToolUse(Bash)` — fires after a successful `gh pr create`.
- **Current emission:** a single `<sc-auggie-review-offer source="post-pr-create-hook">` block
  (heredoc, lines 60–72) suggesting only `/sc:auggie-review`.
- **C5 edit (FR-7.1):** must ALSO mention `sc:submit-pr --monitor` in the offer, stay fail-open
  (exit 0 on non-match / failed create — already does, lines 21/39), never spawn a monitor itself,
  never imply level-3 without explicit invocation.
- **Key structural anchors for the edit:**
  - Lines 49–58: the `INVOKE_HINT` / `TARGET_HINT` if/elif/else block (currently sets
    `INVOKE_HINT="/sc:auggie-review $PR_NUM"`). The submit-pr mention likely threads here or in the
    heredoc.
  - Lines 60–72: the `cat <<EOF ... EOF` offer heredoc — the user-facing text to extend.
  - Line 21: cheap prefilter `case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*)` — unchanged.
  - Line 33: regex guard matching `gh ... pr create` (not `pr view`/`pr list`) — unchanged.
- **`.claude/` synced copy:** **ABSENT** — `.claude/hooks/scripts/offer-pr-review.sh` does NOT
  exist. NOTE: hooks are NOT mirrored to `.claude/` the way skills/refs are (only the rubric copy
  was found). After the C5 edit, sync behavior for `hooks/scripts/` should be verified by the build
  (the spec's `make sync-dev` step [6] assumes mirroring; whether hooks sync is an R2/R5 question).
  Flag: **C5 edit is `src/`-only; do NOT `git add .claude/hooks/...`.**

---

## Test file inventory (C6 — spec §6.3, lines 426–469)

`tests/submit_pr/` is entirely **NEW** (dir absent). Per-file breakdown the builder can turn into
one checklist item each:

**Module files (22):**
`__init__.py`, `conftest.py` (fixtures: mock_gh, mock_monitor, fixture_findings, tmp_skill_dir),
`test_skill_parse.py`, `test_pre_pr_checks.py`, `test_monitor_arm.py`,
`test_detection_contract.py`, `test_timeout.py`, `test_severity_router.py`,
`test_finding_verify.py`, `test_troubleshoot_seed.py`, `test_autonomy_gates.py`,
`test_validation_gate.py`, `test_loop_guard.py`, `test_reply_resolve.py`,
`test_idempotency.py`, `test_rate_limit.py`, `test_run_log.py`, `test_crash_recovery.py`,
`test_edge_cases.py`, `test_hook_update.py`, `test_static_grep.py`,
`test_validated_not_verified.py`.

**Fixtures (18) under `tests/submit_pr/fixtures/`:**
`finding-medium.json`, `finding-high.json`, `finding-medium-high.json`, `finding-empty.json`,
`finding-max.json`, `finding-duplicate.json`, `finding-fresh-comment-id.json`,
`finding-needs-human.json`, `finding-malformed.json`, `finding-ungroundable.json`,
`review-clean.json`, `review-with-findings.json`, `review-non-augment.json`,
`review-interleaved.json`, `round-sequence-2.json`, `round-sequence-residual-x3.json`,
`crash-after-push-before-completed.json`, `behavioral-drift.json`.

(R4 owns test infra + the deterministic-core-module question — coverage-matrix → test mapping and
the question of whether a Python core module backs these tests is R4's, not duplicated here.)

---

## Conventions / precedents relevant to file placement (evidence)

- **`scripts/` subdir precedent EXISTS** — C2/C4 introduce `scripts/` under the skill. Three
  existing skills already use it: `sc-crash-recovery/scripts`, `sc-bare-review/scripts`,
  `sc-cleanup-audit-protocol/scripts`. So C2/C4 follow established layout (R2 owns the full
  structural-convention analysis).
- **`commands/` dir EXISTS** (`src/superclaude/commands/`); `auggie-review.md` (9559 bytes) is the
  nearest sibling for `submit-pr.md` frontmatter/trigger convention.
- **Test dir naming:** spec uses `tests/submit_pr/` (underscore). Underscore precedent:
  `tests/cli_portify/`. Most sibling test dirs use hyphens (`tests/audit-trail`, `tests/sc-roadmap`).
  `conftest.py` is an established per-suite convention (9 existing suites have one).
- **No existing test references `offer-pr-review`** (`grep -rl` → none) — C6's `test_hook_update.py`
  is the FIRST test of this hook; no existing hook test to extend or collide with.

---

## Summary Table — every spec-defined path, one row each (builder → one checklist item per row)

| # | Path | C-ID | Status | Evidence |
|---|------|------|--------|----------|
| 1 | `src/superclaude/skills/sc-submit-pr-protocol/SKILL.md` | C1 | NEW | dir absent |
| 2 | `src/superclaude/skills/sc-submit-pr-protocol/refs/state-machine.md` | C1/FSM | NEW (core-pure) | dir absent |
| 3 | `src/superclaude/skills/sc-submit-pr-protocol/refs/detection-contract.md` | DET | NEW (R1-gated) | dir absent |
| 4 | `src/superclaude/skills/sc-submit-pr-protocol/refs/augment-poll.md` | C2 | NEW | dir absent |
| 5 | `src/superclaude/skills/sc-submit-pr-protocol/refs/severity-routing.md` | C3 | NEW (core-pure) | dir absent |
| 6 | `src/superclaude/skills/sc-submit-pr-protocol/refs/finding-verify.md` | C3a | NEW | dir absent |
| 7 | `src/superclaude/skills/sc-submit-pr-protocol/refs/troubleshoot-dispatch.md` | C3b | NEW | dir absent |
| 8 | `src/superclaude/skills/sc-submit-pr-protocol/refs/thread-reply.md` | C4 | NEW | dir absent |
| 9 | `src/superclaude/skills/sc-submit-pr-protocol/refs/loop-guard.md` | LG | NEW (core-pure) | dir absent |
| 10 | `src/superclaude/skills/sc-submit-pr-protocol/scripts/poll-augment-review.sh` | C2 | NEW | dir absent; `scripts/` has precedent |
| 11 | `src/superclaude/skills/sc-submit-pr-protocol/scripts/reply-resolve-thread.sh` | C4 | NEW | dir absent; `scripts/` has precedent |
| 12 | `src/superclaude/commands/submit-pr.md` | C1 | NEW | absent; `commands/` dir exists |
| 13 | `src/superclaude/hooks/scripts/offer-pr-review.sh` | C5 | **EDIT** | exists, 74 lines, 3409 B, exec |
| 14 | `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | C3 reuse | **REUSE (no edit)** | exists, 172 lines, 10768 B |
| 15 | `tests/submit_pr/` (24 files: 22 modules + 18 fixtures + `__init__`/`conftest`) | C6 | NEW | dir absent |

**Counts:** 12 NEW skill-package files (incl. command) · 1 EDIT (C5 hook) · 1 REUSE (rubric, no
edit) · 1 NEW test tree (`tests/submit_pr/`, ~42 files: 24 modules/init/conftest + 18 fixtures).

## Flags for the task builder

1. **C5 hook edit is `src/`-only.** `.claude/hooks/scripts/offer-pr-review.sh` does not exist
   (hooks not mirrored to `.claude/` like skill refs are). Never `git add .claude/hooks/...`.
   Confirm whether `make sync-dev` mirrors `hooks/` at all (defer to R5).
2. **`severity-rubric.md` is REUSE, not edit** — C3 references it; do not modify the auggie-review
   skill's rubric.
3. **DET is the hard build gate** (step 0) — `detection-contract.md` must ship with `locked:false`
   and the build must block arming until R1 flips it. It is NEW but R1-empirically-populated.
4. **`scripts/` subdir is a real convention** (3 precedent skills) — C2/C4 scripts belong under
   `src/superclaude/skills/sc-submit-pr-protocol/scripts/`, not loose in the skill root.

**Status:** Complete.
