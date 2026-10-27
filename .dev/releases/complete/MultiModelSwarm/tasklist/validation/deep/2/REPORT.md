# `/sc:reflect` Post-Execution Audit — Phase 2 / M2

**Mode:** post  
**Depth:** deep / Tier 2-style review with independent subagent review + calibration  
**Scope:** Phase 2 only — M2 "Preflight, Schema, Lens Registry & Injection Guard (Wave 0)" deliverables from `phase-2-tasklist.md`  
**Diff input:** `git diff HEAD` in worktree `/config/workspace/IronClaude/.claude/worktrees/SwarmPost`  
**Status:** **FAILED** — Phase 2 implementation has verified exit blockers and two in-scope behavioral/persistence defects.

## Executive Verdict

Phase 2 is **not ready to mark complete**.

Positive evidence:

- The targeted Phase 2 validation suite passed: `382 passed` for schema, preflight guard, custom prompt helper, injection guard, pool guards, lens registry/validator, validate subcommands, normalizer strategy, auto-inject guard, prompt neutralization, no-Claude-isms, and CallerMetadata tests.
- `uv run superclaude swarm validate-lenses` returned `validate-lenses: registry OK (8 entries inspected, 7 validated)`.

Blocking evidence:

1. `custom_prompt_dir` is implemented as a helper/test surface but is **not consumed by the production `swarm run` / `run_preflight` path**, so a spec with a missing custom prompt directory can still reach `preflight_ok`.
2. T02.25 requires the Manifest to capture resolved `CallerMetadata`, but the `Manifest` dataclass has no `caller_metadata` field; resolved metadata currently lives on `PreflightResult` only.
3. T02.29 requires `phase-2-cp5.md` and `make verify-sync`; CP5 is absent and `make verify-sync` currently fails.

## Verification Commands Run

| Command | Result | Scope |
|---|---:|---|
| `uv run pytest tests/swarm -q` | **9 failed, 2134 passed, 29 skipped** | Full swarm suite; failures include later-phase/out-of-scope blockers |
| `uv run pytest <20 Phase-2 test files> -q` | **382 passed** | Targeted Phase 2 validation set |
| `uv run superclaude swarm validate-lenses` | **PASS** | T02.20 / T02.29 validate-lenses gate |
| `make verify-sync` | **FAIL** | T02.29 exit gate |

## Deviation Register

### R1 — `custom_prompt_dir` is not wired into the production preflight/run path

**Class:** `regression`  
**Confidence:** 0.88 calibrated  
**Affected tasks:** T02.05, T02.07, T02.29  
**Severity:** HIGH

**Expected:** T02.05 requires `read_custom_prompt_dir(path) -> (system, user, meta)`, missing prompt files to produce a structured failed contract, and the three custom prompt files to round-trip into the Manifest snapshot (`phase-2-tasklist.md:157-169`). T02.07 requires the §11.5 guard across the lens, JSON-Schema, and custom-prompt-dir paths and says all three paths share a single enforcement path (`phase-2-tasklist.md:209-220`).

**Observed:** `commands.run_cmd` explicitly does not consume the `auto_inject_guard` / custom-prompt-dir wiring and deletes the option (`src/superclaude/cli/swarm/commands.py:1132-1136`). `run_preflight` enforces the guard only against `job.prompt.system` (`src/superclaude/cli/swarm/preflight.py:1670-1683`); it does not read `job.custom_prompt_dir` or call `read_custom_prompt_dir` in the production path.

**Runtime probe:** A spec with `lens="custom"` and `custom_prompt_dir="/definitely/missing/custom-prompts"` returned `preflight_ok custom` instead of failing on the missing directory.

**Why this matters:** The helper and tests prove the helper works, but the actual preflight entrypoint can accept a missing custom-prompt directory. That leaves one of the three promised prompt-input paths outside production enforcement.

**Recommended remediation:** Wire `custom_prompt_dir` consumption before `run_preflight` guard evaluation: when `lens == "custom"` and `custom_prompt_dir` is set, call `read_custom_prompt_dir(..., required_substring=..., auto_inject_guard=...)`, populate `job.prompt.system`, `job.prompt.user_template`, and variables/meta, and fail with structured `PreflightError` on missing files or missing §11.5 substring.

---

### R2 — Resolved `CallerMetadata` is not captured in the Manifest

**Class:** `regression`  
**Confidence:** 0.86 calibrated  
**Affected task:** T02.25  
**Severity:** MEDIUM

**Expected:** T02.25 acceptance explicitly requires `models.py::CallerMetadata`, OQ-009 precedence, and that the **Manifest captures resolved CallerMetadata** (`phase-2-tasklist.md:728-736`). CP4 repeats that the Manifest must capture resolved CallerMetadata so downstream stages can audit which side wins per job (`phase-2-cp4.md:192-196`).

**Observed:** `PreflightResult` has a `caller_metadata` field (`src/superclaude/cli/swarm/preflight.py:252-266`), but `Manifest` contains only `contract_version`, `job_id`, `resolved_lens_entry`, and `preflight` fields (`src/superclaude/cli/swarm/models.py:1335-1405`). There is no manifest field that can persist a caller override or the final resolved value.

**Why this matters:** A process that rehydrates only `manifest.json` cannot audit the final resolved `CallerMetadata` if a caller override was supplied. The current model preserves lens-side defaults via `ResolvedLensEntry`, but not the resolved metadata value required by T02.25.

**Recommended remediation:** Add a manifest-level `caller_metadata: CallerMetadata` field (or an explicitly versioned manifest extension) and stamp the resolved value during `run_preflight` before writing `manifest.json`. Add a manifest JSON round-trip test that verifies caller override persistence.

---

### R3 — CP5 end-of-phase report is missing

**Class:** `drift`  
**Confidence:** 0.95 calibrated  
**Affected task:** T02.29  
**Severity:** HIGH / exit blocker

**Expected:** T02.29 requires `phase-2-cp5.md` end-of-phase report with sign-off (`phase-2-tasklist.md:842-847`). CP4 states CP5 gates the M2 close-out bracket and M2 exit (`phase-2-cp4.md:210-215`).

**Observed:** Filesystem check found no `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-2-cp5.md`.

**Recommended remediation:** Produce the CP5 report only after R1/R2 and sync issues are resolved, then re-run the Phase 2 exit gate.

---

### R4 — `make verify-sync` fails, blocking T02.29

**Class:** `regression` for the T02.29 exit gate; root cause appears outside Phase 2 swarm surfaces  
**Confidence:** 0.93 calibrated  
**Affected task:** T02.29  
**Severity:** HIGH / exit blocker

**Expected:** T02.29 requires `make verify-sync` to pass (`phase-2-tasklist.md:842-847`).

**Observed:** `make verify-sync` exited 2. The drift report says `DIFFERS: sc-bare-review` and `Only in src/superclaude/skills/sc-bare-review/: scripts`. Git status shows deleted source-side script paths:

- `src/superclaude/skills/sc-bare-review/scripts/t2_dispatch.sh`
- `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py`
- `src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh`

**Scope classification:** This is in-scope as a T02.29 exit blocker because T02.29 requires `make verify-sync`. Its root cause is out-of-scope for Phase 2 schema/preflight/lens correctness because it is under `sc-bare-review` skill migration/script drift.

**Recommended remediation:** Restore or intentionally sync the `sc-bare-review` source/mirror state via the repository source-of-truth workflow (`src/superclaude/` first, then `make sync-dev`, then `make verify-sync`). Do not stage `.claude/` mirrors directly.

## Out-of-Scope / Non-Primary Blockers

The full `tests/swarm -q` run failed 9 tests. These failures should not be used as Phase 2 implementation regressions without separate phase mapping:

- `tests/swarm/test_recipe_bare_review.py` fails because legacy `sc-bare-review/scripts/t2_normalize.py` is missing; that is an M8 migration/parity surface, not an M2 schema/preflight/lens-registry surface.
- `tests/swarm/test_concurrency_python_only.py` flags `tmux.py` / subprocess usage; that is a later detached/session/concurrency surface, not one of the Phase 2 validate/lens registry deliverables.
- `tests/swarm/test_uv_enforcement.py` flags a `python -m` comment in detached-run documentation; that is an AC-001/M7-adjacent cleanup, not direct Phase 2 behavior.

Treat these as repository-level blockers if the release bar is “full swarm suite green,” but keep them separate from M2 correctness.

## Per-Task Verdict Summary

| Task range | Verdict | Notes |
|---|---|---|
| T02.01-T02.04 | `partial` | Schema/helper tests pass; no primary defect retained for helper-only default expansion. |
| T02.05-T02.07 | `failed` | R1: custom-prompt-dir helper not wired into production preflight/run path. |
| T02.08-T02.24 | `success` | Targeted tests and validate-lenses pass; lens reviewer found no confirmed deviations. |
| T02.25 | `failed` | R2: resolved CallerMetadata not persisted in Manifest. |
| T02.26-T02.28 | `success` | Targeted tests pass. |
| T02.29 | `failed` | R3/R4: CP5 missing and verify-sync fails. |

## Return Contract Summary

```yaml
status: failed
mode: post
tier_reached: 2
confidence_calibrated: 0.89
tasklist_completion_pct: 0.86
deviation_count_by_class:
  authorized: 0
  necessary: 0
  drift: 1
  regression: 3
regression_present: true
unauthorized_deviation_present: true
needs_human_decision: false
evidence_validator_ran: true
citations_total: 17
citations_revalidated: 17
citations_dropped: 0
promotion_action: not-applicable
```

## Next Action

Do **not** close Phase 2 yet. Fix R1/R2, restore `make verify-sync`, generate CP5, then rerun:

`/sc:reflect --mode post --depth deep --diff HEAD --tasklist /config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-2-tasklist.md --spec /config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md --output /config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/validation/deep/2-rerun --no-promote`
