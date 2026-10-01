# Research: Doc Source Extraction
**Topic type:** Cross-document content extraction
**Scope:** RECONCILED_DESIGN.md §3.2/§4/§11; merged-output.md §5.3; F-strict-review.md; git log
**Status:** Complete
**Date:** 2026-05-01
---

## 1. RECONCILED_DESIGN.md §3.2 Extraction (Out-of-scope ledger)

**Source file**: `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` lines 105-134.

§3.2 contains **three** sub-buckets, not just SUPERSEDED. The user's BUILD_REQUEST conflated SUPERSEDED with DEFER-TO-BEAT-2. Here is the canonical breakdown.

### 1a. DROP bucket (10 items — already functionally equivalent or invariant)

> Lines 107-119, verbatim:
- `D-008, D-011, D-101, D-102, D-079` — Risk #1 verified resolved 2026-04-30 (P0 probe, `claude 2.1.123`).
- `D-029` — `Popen(stdin=PIPE, stdout=fh, stderr=fh)` already in place at `pipeline/process.py:125-130`.
- `D-033` — `stdin.close()` already present at `pipeline/process.py:143` (will be moved to `finally` per D-108).
- `D-037` — `self.prompt` invariant already holds at `pipeline/process.py:55`.
- `D-038` — `cmd[:3]` debug log shape preserved.
- `D-039` — `setpgrp` hasattr-gating already in place at `pipeline/process.py:131-132`.
- `D-041` — `build_env()` unchanged; CLAUDECODE strip preserved at `pipeline/process.py:108-109`.
- `D-044` — `Popen` + manual stdin manage already chosen over `communicate()`.
- `D-051` — `"-p" not in cmd` for all sizes already pinned by `tests/pipeline/test_process.py:54, :176-177`.
- `D-056` — 200 KB stdin round-trip already pinned by `tests/pipeline/test_process.py:200-219`.
- `D-063` — `--output-format` + value adjacency already pinned by `tests/pipeline/test_process.py:17-37`.

(Note: DROP bullet count = 11 D-NNN bullet rows but the first row aggregates 5 IDs — D-008, D-011, D-101, D-102, D-079 — so total D-NNN IDs in DROP = 15.)

### 1b. SUPERSEDED bucket (4 bullet rows; 14 distinct D-NNN IDs)

> Lines 121-126, verbatim:
- `D-002, D-004` (AC-2/AC-4 byte-identical-argv contract — pre-patch shape obsolete since `4799719`).
- `D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-109` — threshold + `_use_stdin_for_prompt` + `_prompt_anchor_flag(--output-format)` no longer applicable (always-stdin chosen).
- `D-050, D-053, D-054, D-055, D-057` — threshold-boundary tests N/A; "empty → argv with `-p ''`" inverted by always-stdin.
- `D-075` — threshold-tweak rollback mechanism N/A; rollback is now `git revert 4799719`.

**SUPERSEDED count**: 14 distinct D-NNN IDs (D-002, D-004, D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-050, D-053, D-054, D-055, D-057, D-075, D-109).

Wait — re-counting: D-002, D-004 (2) + D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-109 (8) + D-050, D-053, D-054, D-055, D-057 (5) + D-075 (1) = **16 distinct IDs**.

**Cross-check vs merged-output.md §5.4 line 214**: the merged-output text says "12 SUPERSEDED D-NNN items from RECONCILED_DESIGN.md §3.2 (D-002, D-004, D-017-19, D-023, D-024, D-028, D-042, D-050, D-053-55, D-057, D-075, D-109)". That enumeration expanded:
- D-002, D-004 = 2
- D-017, D-018, D-019 = 3
- D-023, D-024, D-028, D-042 = 4
- D-050, D-053, D-054, D-055, D-057 = 5
- D-075, D-109 = 2
- Total = **16 IDs**, but the merged-output banner says "12".

**Discrepancy**: merged-output.md banner ("12 SUPERSEDED") undercounts by 4. The actual ID list inside the parenthetical is 16. Use the verbatim ID list, not the banner number, when populating BEAT_2_BACKLOG.md.

### 1c. DEFER-TO-BEAT-2 bucket (the "15 items" the user's request referenced)

> Lines 128-133, verbatim:
- `D-016, D-022, D-035, D-064, D-065, D-072, D-073` — sidecar feature (`prompt_sidecar` kwarg, `.prompt` file, caller policy, opt-in tests, off-by-default test, disk-bloat note). Sidecar is observability-only and adds disk-bloat surface; `4799719` already gives us the security improvement of hiding prompts from `ps` for free. Land sidecar in beat 2 once the cap-and-error-surfacing baseline is stable.
- `D-077, D-085, D-087` — vendored monkey-patch in consumer repo (`/config/workspace/Coder` deployment) is a separate operational deliverable downstream of the IronClaude release.
- `D-093, D-095, D-096, D-097` — beat-2 architectural items (`pre_prompt_args`, `--input-format=stream-json`, sidecar rotation, `PromptSource` Protocol).
- `D-098` — `force_prompt_via` per-caller override; superseded under always-stdin.

**DEFER-TO-BEAT-2 count**: D-016, D-022, D-035, D-064, D-065, D-072, D-073 (7) + D-077, D-085, D-087 (3) + D-093, D-095, D-096, D-097 (4) + D-098 (1) = **15 distinct IDs**. Matches the §3.2 banner.

### 1d. Count reconciliation summary

| Bucket | Banner says | Actual D-NNN IDs |
|---|---|---|
| DROP | (no count given) | 15 |
| SUPERSEDED | (no count given in §3.2 banner; merged-output §5.4 says "12") | **16** |
| DEFER-TO-BEAT-2 | "15 items" | 15 |

**The user's BUILD_REQUEST "15 DEFER-TO-BEAT-2 items" is correct.** That is distinct from SUPERSEDED. Both lists go into `BEAT_2_BACKLOG.md` (P-014) per merged-output §5.4 ("Optionally appended to `BEAT_2_BACKLOG.md`").

---

## 2. RECONCILED_DESIGN.md §4 Patch P-004 Acceptance Block (for P-010 amendment)

**Source file**: `RECONCILED_DESIGN.md` lines 303-414. The P-010 patch will append to the **Acceptance** sub-block.

### 2a. Current Acceptance block (lines 409-414, verbatim)

```markdown
**Acceptance**:
- A 400 KB ASCII prompt round-trips byte-identical via stdin (extends current 200 KB test).
- A 200 KB UTF-8 emoji prompt round-trips byte-identical.
- `BrokenPipeError` (child exits early) populates `self._stdin_error` and emits a `WARNING` log line, but does not raise from `start()`.
- A SIGTERM delivered to the parent during the write loop does not hang `start()` indefinitely (the chunk loop exits after the current chunk because the child closes its end).
- `stdin.close()` runs in the `finally`, even if `os.write` raises an unexpected `OSError`.
```

### 2b. P-010 "After" block (Acceptance with appended invariant)

```markdown
**Acceptance**:
- A 400 KB ASCII prompt round-trips byte-identical via stdin (extends current 200 KB test).
- A 200 KB UTF-8 emoji prompt round-trips byte-identical.
- `BrokenPipeError` (child exits early) populates `self._stdin_error` and emits a `WARNING` log line, but does not raise from `start()`.
- A SIGTERM delivered to the parent during the write loop does not hang `start()` indefinitely (the chunk loop exits after the current chunk because the child closes its end).
- `stdin.close()` runs in the `finally`, even if `os.write` raises an unexpected `OSError`.
- Subclasses overriding `terminate()` MUST either call `super().terminate()` or replicate the `_stdin_error` log block verbatim. Pinned by `tests/pipeline/test_subclass_terminate_invariant.py`.
```

### 2c. P-010 diff anchor (for the task file)

- **File**: `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md`
- **Insert at**: line 414, after the existing last bullet (`stdin.close() runs in the finally...`)
- **Insert mode**: append one bullet line; preserve the trailing horizontal-rule (`---`) at line 416.

---

## 3. RECONCILED_DESIGN.md §11 Provenance Map (seed for P-015 TRACEABILITY.md)

**Source file**: `RECONCILED_DESIGN.md` lines 561-587, verbatim.

### 3a. Patch table (§11, lines 565-571)

| Patch | D-NNN | Adversarial provenance | AC / Risk reference |
|-------|-------|-------------------------|-----------------------|
| P-001 | D-012, D-046, D-047, D-048 | C-003 (A 65%), X-002 (A 60%), U-002 (A only, 70%) | DESIGN.md AC-4 (adapted), Risk #2 |
| P-002 | D-014, D-020, D-021 | U-001 (A only, 95%), U-003 (B only, 90%, Change #1) | DESIGN.md AC-7, Risk #4 |
| P-003 | D-007, D-036 | U-001 (A) + U-003 (B) — pre-spawn cap | DESIGN.md AC-7, Risk #4 |
| P-004 | D-013, D-025, D-026, D-032, D-034, D-040, D-107, D-108 | C-007 (B 75%, Change #3), C-004 (A 85%), INV-002 (HIGH ADDRESSED) | DESIGN.md AC-1, AC-5, AC-6, Risk #3 (reframed), Risk #5 (partial — error surfacing) |
| P-005 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW (Surprise from `B-code-state.md` Surprise #4 / `E-reconciliation-matrix.md` §4.1) | DESIGN.md AC-10 (full suite green) |

### 3b. Test table (§11, lines 573-585)

| Test | D-NNN | Adversarial provenance | AC / Risk reference |
|------|-------|-------------------------|-----------------------|
| T-001 | D-052 | X-001 (A) | DESIGN.md AC-3 |
| T-002 | D-001, D-056 (extended) | C-007 (B), C-001 (A) | DESIGN.md AC-1 |
| T-003 | D-006, D-058 | Change #4 (B§8.2) | DESIGN.md AC-6 |
| T-004 | D-007, D-059 | U-001 (A) + U-003 (B) | DESIGN.md AC-7 |
| T-005 | D-005, D-060 (reframed) | INV-002 | DESIGN.md AC-5, Risk #3 |
| T-006 | D-027 (reframed for always-stdin) | X-003 (B 75%, Change #5) | operational documentation |
| T-007 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW | DESIGN.md AC-10 |
| T-008 | D-049, D-063 | DESIGN-NEW (test contract for U-002) | DESIGN.md AC-4 (adapted) |
| T-009 | D-062 | C-003, X-002 | DESIGN.md AC-4, Risk #2 |
| T-010 | new from P-001 | DESIGN-NEW (regression net) | DESIGN.md Risk #2 |
| T-011 | D-034 | A§3.3 — error surfacing | DESIGN.md Risk #5 (partial) |

### 3c. Commit ↔ Patch ↔ Files map (from `git log --oneline 142ce15..HEAD` + `git show --stat`)

| Commit SHA | Subject | Patch ID | Files Touched |
|---|---|---|---|
| `526a606` | `fix(cli_portify): anchor --add-dir on --output-format instead of dead -p lookup` | P-001 | `src/superclaude/cli/cli_portify/process.py` (14 lines), `tests/pipeline/test_process_stdin.py` (+109) |
| `c42139b` | `feat(pipeline): add PROMPT_MAX_BYTES and PromptTooLargeForArgv exception` | P-002 | `src/superclaude/cli/pipeline/process.py` (+19) |
| `be46520` | `feat(pipeline): pre-spawn size guard + capture encoded prompt for reuse` | P-003 | `src/superclaude/cli/pipeline/process.py` (+10), `tests/pipeline/test_process_stdin.py` (+57/-1) |
| `5a8e5e7` | `fix(pipeline): chunked stdin write with EINTR retry, error capture, finally-close` | P-004 | `src/superclaude/cli/pipeline/process.py` (+67/-8), `tests/pipeline/test_process_stdin.py` (+121) |
| `01cf2ef` | `test(pipeline): pin tool_write_mode contract` | P-005 / T-007 | `tests/pipeline/test_process_stdin.py` (+73) |
| `dda68d9` | `test(pipeline): argv byte-size invariant for huge prompts` | T-001 | `tests/pipeline/test_process_stdin.py` (+35) |
| `fde1431` | `docs: mark DESIGN.md as historical; RECONCILED_DESIGN.md is the actionable plan` | (doc-only) | `.dev/architectural/claude-process-stdin-patch/DESIGN.md` (+18/-1) |
| `db8cffe` | `docs: STRICT-tier verification review of stdin-patch delta` | (doc-only) | `.dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md` (+209) |
| `2c21279` | `docs: /sc:adversarial coverage analysis of stdin-patch delta` | (doc-only) | 16 files under `.dev/architectural/claude-process-stdin-patch/adversarial-recon/` (+3775) |

---

## 4. merged-output.md §5.3 D-FOLLOW Table (13 rows, verbatim)

**Source file**: `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/adversarial-recon/merged-output.md` lines 192-210.

> Header (line 194): "Suggested issue titles (per R3-spec's accountability demand):"

| # | Tracking issue (verbatim) | Owner |
|---|---|---|
| 1 | `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer |
| 2 | `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch author |
| 3 | `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch author (pre-merge) |
| 4 | `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer |
| 5 | `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch author |
| 6 | `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer |
| 7 | `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer |
| 8 | `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch author |
| 9 | `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer |
| 10 | `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer |
| 11 | `[deferred] R-5: add prompt_encode_peak_bytes telemetry hook` | beat-2 owner |
| 12 | `[deferred] T-016: tool_write_mode × BrokenPipe interaction test` | branch author (or maintainer) |
| 13 | `[deferred] T-015: extra_args byte-size invariant test` | branch author (or maintainer) |

Total = **13 rows**.

---

## 5. D-FOLLOW Count Reconciliation (refactor-plan vs merged-output)

**refactor-plan source**: `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/adversarial-recon/adversarial/refactor-plan.md` lines 248-260. The refactor-plan "Changes NOT Being Made" table contains **D-FOLLOW-001..D-FOLLOW-012 plus W-M10/R-5** as a separate row = 13 entries. merged-output §5.3 has 13 rows. Compare:

| refactor-plan ID | refactor-plan owner | merged-output title (verbatim) | merged-output owner | Same item? |
|---|---|---|---|---|
| D-FOLLOW-001 | release-engineer | `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer | YES |
| D-FOLLOW-002 | branch author (PR-comment artefact) | `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch author | YES |
| D-FOLLOW-003 | branch author (PR-description, pre-merge) | `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch author (pre-merge) | YES |
| D-FOLLOW-004 | maintainer (post-merge) | `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer | YES |
| D-FOLLOW-005 | branch author | `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch author | YES |
| D-FOLLOW-006 | maintainer (post-merge) | `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer | YES |
| D-FOLLOW-007 | maintainer (post-merge) | `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer | YES |
| D-FOLLOW-008 | branch author (could land in this PR if cheap) | `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch author | YES |
| D-FOLLOW-009 | maintainer (post-merge) | `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer | YES |
| D-FOLLOW-010 | maintainer (post-merge) | `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer | YES |
| D-FOLLOW-011 | beat-2 owner | (NOT in §5.3 — refactor-plan-only: "15 DEFER-TO-BEAT-2 D-NNN items captured in BEAT_2_BACKLOG.md") | beat-2 owner | NO — covered by P-014 |
| D-FOLLOW-012 | branch author (optional) | (NOT in §5.3 — refactor-plan-only: "12 SUPERSEDED items / record ledger") | branch author | NO — covered by P-014 |
| W-M10 (R-5 telemetry) | beat-2 owner | `[deferred] R-5: add prompt_encode_peak_bytes telemetry hook` | beat-2 owner | YES |
| (none) | (none) | `[deferred] T-016: tool_write_mode × BrokenPipe interaction test` | branch author (or maintainer) | NO — merged-output-only |
| (none) | (none) | `[deferred] T-015: extra_args byte-size invariant test` | branch author (or maintainer) | NO — merged-output-only |

### 5a. Reconciliation result

- **10 items match exactly** between refactor-plan D-FOLLOW-001..010 and merged-output §5.3 rows 1-10.
- **W-M10 (R-5) row matches** merged-output §5.3 row 11 (telemetry hook).
- **2 items only in refactor-plan**: D-FOLLOW-011 (15 DEFER-TO-BEAT-2) and D-FOLLOW-012 (12 SUPERSEDED). These are subsumed under P-014 BEAT_2_BACKLOG.md (the task we're building) — **NOT** re-filed as Phase 5 GH issues.
- **2 items only in merged-output §5.3**: T-015 (extra_args byte-size test) and T-016 (tool_write_mode × BrokenPipe test). These were appended in the merged-output recon pass but missed in the refactor-plan numbering.

### 5b. Canonical Phase 5 GH issue list — 13 items

**Use merged-output §5.3 verbatim** (it's the audit-grade enumeration with the broader test coverage). Drop refactor-plan D-FOLLOW-011/-012 because P-014 already absorbs them.

---

## 6. F-strict-review Severity Cross-Reference (for Researcher 3 calibration grounding)

**Source file**: `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md` lines 1-209.

F-strict-review verdict line 16: **"APPROVED-WITH-NITS — Green-light to merge ... No BLOCKER or HIGH issues."**

| F-finding | F severity | F citation | Maps to merged-output | merged-output severity | Refactor-plan ID | Match? |
|---|---|---|---|---|---|---|
| MEDIUM-1: PrdClaudeProcess.terminate() missing `_stdin_error` surfacing | MEDIUM | F §3 lines 34-42 | A-FINDING-001 (merged §4 HIGH) | HIGH | (in-PR fix; not D-FOLLOW) | **MISMATCH — F=MEDIUM, merged=HIGH** |
| MEDIUM-2: `int(os.environ.get(...))` crash on non-numeric `SUPERCLAUDE_PROMPT_MAX_BYTES` | MEDIUM | F §3 lines 46-72 | A-FINDING-003 (merged §4 MEDIUM) | MEDIUM | D-FOLLOW-005 (INV-011 clamp) | MATCH |
| LOW-1: `_stdin_error` not reset between successive `start()` calls | LOW | F §3 lines 76-82 | (not surfaced as discrete merged finding) | — | — | not tracked |
| LOW-2: `n == 0` from `os.write` breaks loop silently | LOW | F §3 lines 86-98 | A-FINDING-007 (merged §4 MEDIUM) | MEDIUM | (in-PR or D-FOLLOW pending Researcher 3) | **MISMATCH — F=LOW, merged=MEDIUM** |
| NIT-1: T-011 silent no-op on fast machines | NIT | F §3 lines 102-104 | A-FINDING-005 (merged §4 MEDIUM) | MEDIUM | (in-PR fix) | **MISMATCH — F=NIT, merged=MEDIUM** |
| NIT-2: T-005 timer fires before `start()` | NIT | F §3 lines 106-108 | INV-027 / D-FOLLOW-008 | LOW | D-FOLLOW-008 | MATCH |
| NIT-3: `build_command()` called twice per `start()` | NIT | F §3 lines 110-112 | INV-026 / D-FOLLOW-007 | LOW | D-FOLLOW-007 | MATCH |
| §4.1 Sprint test fixtures broken since `4799719` | (pre-existing, not regression) | F §4 lines 118-122 | (separate GH issue) | — | (out-of-scope) | tracked in F only |
| §4.2 cleanup_audit/executor.py is_running()/stop() | (pre-existing) | F §4 lines 124-128 | (separate GH issue) | — | (RECONCILED §3.2 out-of-scope) | tracked in F only |

### 6a. Calibration insights for Researcher 3

The F→merged-output severity discrepancies all bias **the same direction**: merged-output (adversarial pass) escalates 3 findings vs F-strict-review (sub-agent QE pass).

- **MEDIUM-1 vs A-FINDING-001 (HIGH)**: F rationale (line 42) is "MEDIUM not HIGH because base `wait()` still surfaces it". merged-output upgrades to HIGH because the failure mode P-004 was meant to fix (silent BrokenPipe) is regressed by the override. **Use merged-output's HIGH.** Justification: severity should reflect the contract violation, not the partial mitigation through `wait()`.
- **LOW-2 vs A-FINDING-007 (MEDIUM)**: F rationale (line 96) is "near-zero probability". merged-output escalates to MEDIUM because the post-condition (silent truncation, "couldn't parse JSON" downstream) is a debug-time disaster even if rare. **Use merged-output's MEDIUM.**
- **NIT-1 vs A-FINDING-005 (MEDIUM)**: F rationale (line 102-104) treats the soft-assert as "correct (avoids flake)". merged-output flags the lack of fail mode — a passing test that exercises nothing has zero mutation-kill value. **Use merged-output's MEDIUM.**

The two pre-existing items (F §4.1, §4.2) are out-of-scope for this delta but are appropriate Phase 5 GH issues — they predate the branch and align with refactor-plan §5.3 "Existing tech debt" carry-over.

---

## Builder-Usable Content for P-014 (BEAT_2_BACKLOG.md)

Paste the following as the body of `.dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` (created by P-014):

```markdown
# Beat-2 Backlog — Deferred and Superseded Ledger

**Source**: `RECONCILED_DESIGN.md §3.2`
**Beat-1 HEAD at deferral**: `2c21279`
**Created by**: P-014 (TASK-STDIN-RECON-REMEDIATION-20260501)
**Status**: Open until Beat-2 sprint planned

---

## §1. DEFER-TO-BEAT-2 (15 items)

These items were intentionally deferred from Beat-1 (the stdin-patch delta) to a future Beat-2 sprint. Each will be filed as an individual GH issue when Beat-2 is scheduled.

### Sidecar feature (7 items)

- **D-016, D-022, D-035, D-064, D-065, D-072, D-073** — sidecar feature: `prompt_sidecar` kwarg, `.prompt` file, caller policy, opt-in tests, off-by-default test, disk-bloat note. Sidecar is observability-only and adds disk-bloat surface; commit `4799719` already gives the security improvement of hiding prompts from `ps` for free. Land sidecar in Beat-2 once the cap-and-error-surfacing baseline is stable.

### Coder-repo deployment (3 items)

- **D-077, D-085, D-087** — vendored monkey-patch in consumer repo (`/config/workspace/Coder` deployment). Separate operational deliverable downstream of the IronClaude release.

### Beat-2 architectural items (4 items)

- **D-093, D-095, D-096, D-097** — `pre_prompt_args`, `--input-format=stream-json`, sidecar rotation, `PromptSource` Protocol.

### Per-caller override (1 item)

- **D-098** — `force_prompt_via` per-caller override; superseded under always-stdin but retained here in case the design reverses.

---

## §2. SUPERSEDED ledger (16 D-NNN items, recorded for audit)

These items were obsoleted by the always-stdin migration in commit `4799719` (2026-04-20). They are recorded here per merged-output §5.4 ("Optionally appended to `BEAT_2_BACKLOG.md` per P-014 R3 concession").

- **D-002, D-004** — AC-2/AC-4 byte-identical-argv contract (pre-patch shape obsolete since `4799719`).
- **D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-109** — threshold + `_use_stdin_for_prompt` + `_prompt_anchor_flag(--output-format)` no longer applicable (always-stdin chosen).
- **D-050, D-053, D-054, D-055, D-057** — threshold-boundary tests N/A; "empty → argv with `-p ''`" inverted by always-stdin.
- **D-075** — threshold-tweak rollback mechanism N/A; rollback is now `git revert 4799719`.

Audit trail also lives in:
- `git log -- src/superclaude/cli/pipeline/process.py` (history of each line).
- `RECONCILED_DESIGN.md §3.2` (the named ledger).
```

---

## Builder-Usable Content for P-015 (TRACEABILITY.md)

Paste the following as the body of `.dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` (created by P-015):

```markdown
# Traceability Matrix — stdin-patch Delta (Beat-1)

**Branch**: `fix/claude-process-stdin-large-prompts`
**Pre-delta baseline**: `142ce15`
**Beat-1 HEAD**: `2c21279`
**Created by**: P-015 (TASK-STDIN-RECON-REMEDIATION-20260501)
**Source**: `RECONCILED_DESIGN.md §11` + `git log --oneline 142ce15..HEAD`

---

## §1. Patch ↔ D-NNN ↔ Provenance ↔ AC/Risk

| Patch | D-NNN | Adversarial provenance | AC / Risk reference |
|-------|-------|-------------------------|-----------------------|
| P-001 | D-012, D-046, D-047, D-048 | C-003 (A 65%), X-002 (A 60%), U-002 (A only, 70%) | DESIGN.md AC-4 (adapted), Risk #2 |
| P-002 | D-014, D-020, D-021 | U-001 (A only, 95%), U-003 (B only, 90%, Change #1) | DESIGN.md AC-7, Risk #4 |
| P-003 | D-007, D-036 | U-001 (A) + U-003 (B) — pre-spawn cap | DESIGN.md AC-7, Risk #4 |
| P-004 | D-013, D-025, D-026, D-032, D-034, D-040, D-107, D-108 | C-007 (B 75%, Change #3), C-004 (A 85%), INV-002 (HIGH ADDRESSED) | DESIGN.md AC-1, AC-5, AC-6, Risk #3 (reframed), Risk #5 (partial) |
| P-005 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW (Surprise from `B-code-state.md` Surprise #4) | DESIGN.md AC-10 |

## §2. Test ↔ D-NNN ↔ Provenance ↔ AC/Risk

| Test | D-NNN | Adversarial provenance | AC / Risk reference |
|------|-------|-------------------------|-----------------------|
| T-001 | D-052 | X-001 (A) | DESIGN.md AC-3 |
| T-002 | D-001, D-056 (extended) | C-007 (B), C-001 (A) | DESIGN.md AC-1 |
| T-003 | D-006, D-058 | Change #4 (B§8.2) | DESIGN.md AC-6 |
| T-004 | D-007, D-059 | U-001 (A) + U-003 (B) | DESIGN.md AC-7 |
| T-005 | D-005, D-060 (reframed) | INV-002 | DESIGN.md AC-5, Risk #3 |
| T-006 | D-027 (reframed for always-stdin) | X-003 (B 75%, Change #5) | operational documentation |
| T-007 | (orthogonal — `tool_write_mode` regression net) | DESIGN-NEW | DESIGN.md AC-10 |
| T-008 | D-049, D-063 | DESIGN-NEW (test contract for U-002) | DESIGN.md AC-4 (adapted) |
| T-009 | D-062 | C-003, X-002 | DESIGN.md AC-4, Risk #2 |
| T-010 | new from P-001 | DESIGN-NEW (regression net) | DESIGN.md Risk #2 |
| T-011 | D-034 | A§3.3 — error surfacing | DESIGN.md Risk #5 (partial) |

## §3. Commit ↔ Patch ↔ Files Touched

| SHA | Subject | Patch ID | Files Touched |
|---|---|---|---|
| `526a606` | `fix(cli_portify): anchor --add-dir on --output-format instead of dead -p lookup` | P-001 | `src/superclaude/cli/cli_portify/process.py`, `tests/pipeline/test_process_stdin.py` |
| `c42139b` | `feat(pipeline): add PROMPT_MAX_BYTES and PromptTooLargeForArgv exception` | P-002 | `src/superclaude/cli/pipeline/process.py` |
| `be46520` | `feat(pipeline): pre-spawn size guard + capture encoded prompt for reuse` | P-003 | `src/superclaude/cli/pipeline/process.py`, `tests/pipeline/test_process_stdin.py` |
| `5a8e5e7` | `fix(pipeline): chunked stdin write with EINTR retry, error capture, finally-close` | P-004 | `src/superclaude/cli/pipeline/process.py`, `tests/pipeline/test_process_stdin.py` |
| `01cf2ef` | `test(pipeline): pin tool_write_mode contract` | P-005 / T-007 | `tests/pipeline/test_process_stdin.py` |
| `dda68d9` | `test(pipeline): argv byte-size invariant for huge prompts` | T-001 | `tests/pipeline/test_process_stdin.py` |
| `fde1431` | `docs: mark DESIGN.md as historical; RECONCILED_DESIGN.md is the actionable plan` | (doc-only) | `.dev/architectural/claude-process-stdin-patch/DESIGN.md` |
| `db8cffe` | `docs: STRICT-tier verification review of stdin-patch delta` | (doc-only) | `.dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md` |
| `2c21279` | `docs: /sc:adversarial coverage analysis of stdin-patch delta` | (doc-only) | 16 files under `.dev/architectural/claude-process-stdin-patch/adversarial-recon/` |

## §4. Beat-2 Remediation Patches

(Add rows here as remediation P-006 through P-018 are landed by TASK-STDIN-RECON-REMEDIATION-20260501.)
```

---

## Builder-Usable Content for P-010 (RECONCILED_DESIGN.md §4 P-004 amendment)

**File**: `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md`
**Section**: §4 → Patch P-004 → Acceptance sub-block (lines 409-414).

### Before block (verbatim from line 409-414)

```markdown
**Acceptance**:
- A 400 KB ASCII prompt round-trips byte-identical via stdin (extends current 200 KB test).
- A 200 KB UTF-8 emoji prompt round-trips byte-identical.
- `BrokenPipeError` (child exits early) populates `self._stdin_error` and emits a `WARNING` log line, but does not raise from `start()`.
- A SIGTERM delivered to the parent during the write loop does not hang `start()` indefinitely (the chunk loop exits after the current chunk because the child closes its end).
- `stdin.close()` runs in the `finally`, even if `os.write` raises an unexpected `OSError`.
```

### After block (with new invariant bullet appended)

```markdown
**Acceptance**:
- A 400 KB ASCII prompt round-trips byte-identical via stdin (extends current 200 KB test).
- A 200 KB UTF-8 emoji prompt round-trips byte-identical.
- `BrokenPipeError` (child exits early) populates `self._stdin_error` and emits a `WARNING` log line, but does not raise from `start()`.
- A SIGTERM delivered to the parent during the write loop does not hang `start()` indefinitely (the chunk loop exits after the current chunk because the child closes its end).
- `stdin.close()` runs in the `finally`, even if `os.write` raises an unexpected `OSError`.
- Subclasses overriding `terminate()` MUST either call `super().terminate()` or replicate the `_stdin_error` log block verbatim. Pinned by `tests/pipeline/test_subclass_terminate_invariant.py`.
```

**Edit operation**: insert one bullet line at the end of the Acceptance sub-block (i.e., after the existing `stdin.close() runs in the finally...` line, before the `---` separator at line 416).

---

## Phase 5 Canonical D-FOLLOW List (13 items, reconciled)

Use these verbatim as Phase 5 GH issue titles. Source: merged-output.md §5.3 (canonical), reconciled with refactor-plan §5 IDs.

| # | Issue Title (verbatim, paste into GH) | Owner | refactor-plan ID |
|---|---|---|---|
| 1 | `[deferred] D-086: re-run failing 338 KB roadmap on /config/workspace/Coder` | release-engineer | D-FOLLOW-001 |
| 2 | `[deferred] D-067: paste CI link confirming test_process_stdin.py runs in CI` | branch author | D-FOLLOW-002 |
| 3 | `[deferred] U-033/U-034: PR-description amendment with verdict mapping link` | branch author (pre-merge) | D-FOLLOW-003 |
| 4 | `[deferred] INV-005: wrap _stdout_fh/_stderr_fh in start()-level try/except` | maintainer | D-FOLLOW-004 |
| 5 | `[deferred] INV-011: clamp negative SUPERCLAUDE_PROMPT_MAX_BYTES to default` | branch author | D-FOLLOW-005 |
| 6 | `[deferred] INV-024: pin PortifyProcess anchor to first --output-format only` | maintainer | D-FOLLOW-006 |
| 7 | `[deferred] INV-026: cache build_command() result for debug-log reuse` | maintainer | D-FOLLOW-007 |
| 8 | `[deferred] INV-027: reorder T-005 to start() before timer schedule` | branch author | D-FOLLOW-008 |
| 9 | `[deferred] INV-028: capture exception chain depth in _stdin_error` | maintainer | D-FOLLOW-009 |
| 10 | `[deferred] INV-030: gate T-005 on Linux platform marker` | maintainer | D-FOLLOW-010 |
| 11 | `[deferred] R-5: add prompt_encode_peak_bytes telemetry hook` | beat-2 owner | W-M10 |
| 12 | `[deferred] T-016: tool_write_mode × BrokenPipe interaction test` | branch author (or maintainer) | (merged-output only) |
| 13 | `[deferred] T-015: extra_args byte-size invariant test` | branch author (or maintainer) | (merged-output only) |

**Items NOT to file (covered by P-014 BEAT_2_BACKLOG.md)**:
- `D-FOLLOW-011` (15 DEFER-TO-BEAT-2 D-NNN items) — absorbed by §1 of BEAT_2_BACKLOG.md.
- `D-FOLLOW-012` (12/16 SUPERSEDED items) — absorbed by §2 of BEAT_2_BACKLOG.md.

---

## Status: Complete

### Summary
- §3.2 SUPERSEDED bucket = **16 distinct D-NNN IDs** (merged-output banner of "12" undercounts; use the verbatim ID list).
- §3.2 DEFER-TO-BEAT-2 bucket = **15 D-NNN IDs**, matches user's BUILD_REQUEST.
- §3.2 DROP bucket = 15 D-NNN IDs (informational, not in scope for tracking artifacts).
- §11 provenance map captured: 5 patch rows + 11 test rows.
- 9-commit map enriched with files-touched per `git show --stat`.
- merged-output §5.3 D-FOLLOW table: **13 rows verbatim**.
- F-strict-review severity calibration: 3 mismatches all bias toward merged-output escalation (use merged-output severities).
- Phase 5 canonical D-FOLLOW list = **13 issues** (merged-output §5.3); refactor-plan D-FOLLOW-011/-012 are subsumed by P-014.

### Outputs delivered
1. P-014 BEAT_2_BACKLOG.md body (15 DEFER + 16 SUPERSEDED ledger).
2. P-015 TRACEABILITY.md body (5 patches + 11 tests + 9 commits).
3. P-010 RECONCILED_DESIGN.md §4 P-004 Before/After amendment block.
4. Phase 5 canonical 13-item D-FOLLOW list with owners and refactor-plan ID cross-walk.
