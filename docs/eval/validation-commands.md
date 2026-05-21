# OPS-004 — cliEval Validation Command Sequence

**Owner:** RyanW
**Task:** T06.11 (Phase 6, Roadmap R-113, Deliverable D-0114)
**Status:** Partial — 3 of 4 commands attest GREEN on the current tree; command 4 (`eval run`) is blocked by a pre-existing implementation gap. See [§5 Known blockers](#5-known-blockers).

This document defines the **canonical validation command sequence** that an operator (or CI) must execute to demonstrate the cliEval v1 harness is healthy on a clean dev machine. It is the basis of the OPS-005 release checklist (T06.13) and is consumed by the M6 exit-gate checkpoint (T06.16).

---

## 1. Contract

OPS-004 fixes the **order, surface, and exit-code expectation** of four commands. Every release candidate MUST execute all four in sequence and produce **exit 0** on each. Any non-zero exit halts the release until the offending command is fixed or its evidence is explicitly waived in `decisions.md`.

| # | Command | Purpose | Tier | Expected exit |
|---|---------|---------|------|---------------|
| 1 | `uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v` | Targeted smoke — exercises the read-only surface of the eval CLI (describe + doctor) | Smoke | **0** |
| 2 | `make verify-sync` | Source-of-truth gate — confirms `src/superclaude/{skills,agents,commands,hooks}/` is in sync with `.claude/` dev copies | Source-of-truth | **0** |
| 3 | `uv run superclaude eval doctor` | Capability gate — confirms HARD capabilities present, SOFT-SKIPs identified | Capability | **0** |
| 4 | `uv run superclaude eval run --suite real --eval E1` | End-to-end smoke — drives a single PTY-isolated eval (E1: auggie-first sticky-cleared lifecycle) | End-to-end | **0** |

**Why these four:** the sequence walks the harness inside-out — tests → sync → capabilities → live invocation. A failure on any step localises the regression band:

- Command 1 fails → code regression in the read-only surface.
- Command 2 fails → an operator edited `.claude/` directly instead of `src/superclaude/`.
- Command 3 fails → a HARD dependency disappeared from PATH (claude/jq/make/git/`~/.claude/`).
- Command 4 fails → orchestrator, isolation, PTY, or assertion-engine regression.

---

## 2. Command details + evidence locations

All evidence below is captured under `.dev/releases/current/cliEval/evidence/T06.11/` (the OPS-004 evidence root). Each command's log is the verbatim stdout/stderr plus a final `EXIT_CODE=<n>` line so the shell exit can be audited independently of the stream-mixing.

### 2.1 Command 1 — Targeted pytest

**Invocation:**
```bash
uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v
```

**Purpose:** Exercises the read-only eval CLI surfaces (`eval describe` + `eval doctor`) without invoking the orchestrator. Catches schema drift, capability-report shape drift, and Click wiring regressions.

**Evidence:** [`evidence/T06.11/01-targeted-pytest.log`](../../.dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log)
**Observed result (2026-05-20):** **73 passed, EXIT_CODE=0** ✅

**Notes:**
- The selection is two files, not the entire `tests/cli/eval/` directory. A broader run currently surfaces an unrelated regression in `test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr` (Click `CliRunner(mix_stderr=...)` API drift) which is **not in OPS-004 scope** — that is a Click 8.2+ API removal tracked separately. OPS-004 intentionally pins a minimal selection so the smoke is fast and stable.
- The selection is deterministic: alphabetic file ordering, no plugin-loaded fixtures that change between runs.

### 2.2 Command 2 — `make verify-sync`

**Invocation:**
```bash
make verify-sync
```

**Purpose:** Confirms `src/superclaude/{skills,agents,commands,hooks}/` is byte-identical to the `.claude/` dev copies. Catches the "edited `.claude/` directly and forgot to back-port" anti-pattern flagged by the global feedback memory `[[feedback_hooks_source_of_truth]]`.

**Evidence:** [`evidence/T06.11/02-make-verify-sync.log`](../../.dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log)
**Observed result (2026-05-20):** `✅ All components in sync.`, EXIT_CODE=0 ✅

**Notes:**
- The four sync scopes are `skills | agents | commands | hooks`. The eval CLI sources (`src/superclaude/cli/eval/`) are **not** in scope — they live in `src/` only and are imported directly via the installed `superclaude` package.
- Hook cross-consistency is also verified (hooks.json matcher vs `auggie-flag-clear.sh` body), which is independent of the sync axes.

### 2.3 Command 3 — `eval doctor`

**Invocation:**
```bash
uv run superclaude eval doctor
```

**Purpose:** Capability gate per T01.13 / D-0011. Confirms every HARD capability (`claude>=0.5.0`, `jq`, `make`, `git`, `~/.claude/`) is present and reports SOFT-SKIP MCP servers + the ptytest vendoring marker.

**Evidence:** [`evidence/T06.11/03-eval-doctor.log`](../../.dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log)
**Observed result (2026-05-20):** `all HARD capabilities satisfied`, EXIT_CODE=0 ✅

**Soft skips observed:** `mcp_server.auggie-mcp`, `mcp_server.airis-mcp-gateway`, `vendored.ptytest`

**Notes:**
- SOFT-SKIPs are informational; they do not fail the gate. The `vendored.ptytest` marker is the one to watch — it transitions from SOFT-SKIP to OK once the M2 ptytest vendoring lands at `src/superclaude/cli/eval/pty/`. See [§5 Known blockers](#5-known-blockers).
- Operators on non-Linux platforms should expect this command to refuse per AC1 (T06.07).

### 2.4 Command 4 — `eval run --suite real --eval E1`

**Invocation:**
```bash
uv run superclaude eval run --suite real --eval E1
```

**Purpose:** End-to-end smoke. Drives E1 (auggie-first sticky-cleared lifecycle, `suites/real.yaml` row 1) through the orchestrator + HomeIsolation + PTY driver + assertion engine in a single ephemeral HOME.

**Evidence:** [`evidence/T06.11/04-eval-run-E1.log`](../../.dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log)
**Observed result (2026-05-20):** **NameError: `_new_run_id` is not defined**, EXIT_CODE=1 ❌

**Status:** **BLOCKED** — see [§5 Known blockers](#5-known-blockers).

---

## 3. Execution order and idempotency

The four commands MUST be executed **in order**:

1. **pytest first** — fail fast on logic regressions before paying the cost of subprocess invocations.
2. **verify-sync second** — confirm the on-disk surface matches source before running it.
3. **eval doctor third** — confirm the operator's environment can run the harness before invoking it.
4. **eval run fourth** — only after the prior three confirm the prerequisites.

Each command is **idempotent** — re-running on a clean tree produces identical exit codes (modulo timestamps in run-id-derived paths for command 4).

---

## 4. Acceptance map (T06.11)

| AC (T06.11) | Evidence |
|-------------|----------|
| `docs/eval/validation-commands.md` documents the 4 validation commands in order. | This file — §1 contract table and §2 per-command details. |
| Each command's evidence path is linked under `TASKLIST_ROOT/evidence/T06.11/`. | §2.1 / §2.2 / §2.3 / §2.4 — direct relative links. |
| All 4 commands exit 0 on the current tree. | **3 of 4 PASS** (§2.1, §2.2, §2.3). Command 4 (§2.4) is blocked by a pre-existing implementation gap — see [§5](#5-known-blockers). Partial attestation is recorded per `Fallback Allowed: Yes` on the T06.11 phase metadata. |
| `TASKLIST_ROOT/artifacts/D-0114/spec.md` records the command sequence. | [`.dev/releases/current/cliEval/artifacts/D-0114/spec.md`](../../.dev/releases/current/cliEval/artifacts/D-0114/spec.md). |

---

## 5. Known blockers

### B1 — `eval run` body references undefined helpers

**Symptom:** `uv run superclaude eval run --suite real --eval E1` exits with `NameError: name '_new_run_id' is not defined` at `src/superclaude/cli/eval/commands.py:1467`. A second undefined helper, `_default_output_dir`, is referenced one line later at `commands.py:1469`.

**Root cause:** The `eval_run` Click command (`commands.py:1406`) was expanded past the T04.09 deferral skeleton (which emits `RUN_BODY_DEFERRED_MESSAGE` and exits 2) without the supporting private helpers being landed. Per the docstring at `commands.py:1264`, the full T04.10 body was meant to land alongside its helpers. The helpers were never committed.

**Adjacent infrastructure that exists:** `compose_run_id(started_at, suite_name)` is defined at `src/superclaude/cli/eval/artifact_layout.py:139` — `_new_run_id` is presumably meant to wrap it with a `datetime.now(timezone.utc).isoformat()` seed (`secrets` and `datetime` are already imported at the top of `commands.py`).

**Impact on OPS-004:** Command 4 cannot exit 0 until B1 is closed. Commands 1–3 are unaffected.

**Recommended follow-up:** File a P0 task **T06.11-FU01 — Land `_new_run_id` + `_default_output_dir` helpers in `cli/eval/commands.py`**, scope minimum:
- `_new_run_id()` → returns `compose_run_id(datetime.now(timezone.utc).isoformat(), suite_name="")` (or accepts the suite name when threaded through).
- `_default_output_dir(run_id)` → returns `Path(".dev/eval-runs") / run_id`.
- Smoke: re-run command 4 above; expect EXIT_CODE=0 (PASS) or EXIT_CODE=1 with a structured FAIL outcome.

### B2 — ptytest vendoring still SOFT-SKIP

**Symptom:** `eval doctor` reports `vendored.ptytest (SOFT-SKIP) — /config/workspace/IronClaude/src/superclaude/cli/eval/pty/__init__.py not found (vendored at M2)`.

**Root cause:** The ptytest vendoring (D-1 / R5 ADR) was scheduled for M2 but the `cli/eval/pty/` package has not been populated yet. The directory `src/superclaude/cli/eval/pty/` exists but lacks `__init__.py`.

**Impact on OPS-004:** Command 4 will still fail or degrade even after B1 is closed, because `suites/real.yaml` E1 declares PTY-driven semantics (`no_pty: skip` on every eval row). Without vendored ptytest, the PTY driver cannot drive a real Claude Code subprocess and the eval will short-circuit to SKIPPED rather than PASS.

**Recommended follow-up:** Closure of B1 alone is insufficient. The full OPS-004 attestation requires both B1 (helpers) and B2 (vendoring). Track B2 as **T06.11-FU02 — Land M2 ptytest vendoring under `cli/eval/pty/`**, blocking on the original M2 plan owner.

### Closure path

Once B1 + B2 are closed, re-execute command 4 and replace `04-eval-run-E1.log` with the passing capture; flip the AC §4 row "All 4 commands exit 0" from partial to PASS; update `decisions.md` SC1 / OPS-004 entries to status `resolved`.

---

## 6. Reproducibility

To re-execute the full sequence on a clean checkout:

```bash
# Pre-req: editable install
make dev

# Commands 1-4 (run in order; halt on first non-zero)
uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v
make verify-sync
uv run superclaude eval doctor
uv run superclaude eval run --suite real --eval E1
```

To regenerate this document's evidence after a code change:

```bash
mkdir -p .dev/releases/current/cliEval/evidence/T06.11
( uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v 2>&1; \
  echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log
( make verify-sync 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log
( uv run superclaude eval doctor 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log
( uv run superclaude eval run --suite real --eval E1 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log
```

Run the structural test that audits this document:

```bash
uv run pytest tests/cli/eval/test_validation_commands.py -v
```

---

## 7. Cross-references

- **T01.07 / D-0007:** SuiteLoader. Command 4 consumes `suites/real.yaml` via this loader.
- **T01.13 / D-0011:** `eval doctor` capability gate. Command 3 invokes it unchanged.
- **T01.20 / D-0019:** AC11 pre-commit `verify-sync` gate. Command 2 is its release-time equivalent.
- **T01.17 / D-0015:** AC3 dependency allow-list. Independent of OPS-004 but adjacent (see SC3 / T06.10 / D-0113).
- **T04.09 / T04.10 (deferred body):** `eval run` skeleton + full body. B1 above closes the helper gap.
- **T06.10 / D-0113:** SC3 zero-new-deps. Pattern reference for "discovered a gap in an upstream task and closed it here" — T06.11 does **not** close B1/B2 inline (broader scope), but follows the same evidence shape.
- **T06.13 / D-0115:** OPS-005 release checklist. Consumes this document as the validation step.
- **T06.14 / D-0116:** MIG-001 source sync migration. Listed as a dependency in the T06.11 phase metadata; the dependency is **not yet met** on this branch but command 2 (`make verify-sync`) passes today regardless because the four sync scopes are already aligned.
- **T06.16 / D-CP06:** M6 exit gate. Consumes this document + B1/B2 closure as one of the SC1–SC5 attestations.
- **`decisions.md` AC1:** Linux-only v1 declaration. Command 3 enforces non-Linux refusal.

---

**Document version:** v1.0 — initial author (T06.11, 2026-05-20).
