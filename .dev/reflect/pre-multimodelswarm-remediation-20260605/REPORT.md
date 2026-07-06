# /sc:reflect — UC-1 Pre-Execution Coverage Audit

**Target (proposed strategy):** `.dev/tasks/build-requests/BUILD-REQUEST-multimodelswarm-remediation.md`
**Driving spec (requirements):** `.dev/releases/current/MultiModelSwarm/tasklist/validation/deep/AMALGAMATED-REMEDIATION.md`
**Mode:** pre (UC-1) · **Tier reached:** 2 (forced by `--depth deep`) · **Date:** 2026-06-05

## Verdict

`status: partial` — **coverage ≈ 0.93** (above the 0.90 floor), evidence base is sound (3/3 load-bearing
CRITICAL/HIGH code claims VERIFIED against live SwarmPost source — no phantom fixes), but the BUILD-REQUEST
**omits two genuine human-decision points from its mandatory HALT list**, the more serious of which directly
violates the project rule `feedback_human_decision_items_must_halt`. Fixable with ~4 surgical edits to the
BUILD-REQUEST before it reaches task-builder.

**Calibrated confidence:** 0.92 · **Ensemble:** full model + vendor diversity (claude-opus-4-8 / gpt-5.5 / qwen3.6-plus)

## Ensemble & calibration

| Reviewer | Model class → vendor | Lens | Self-conf | Calibrated |
|---|---|---|---|---|
| R1 | haiku → qwen3.6-plus (Qwen) | coverage completeness | — | 0.90 |
| R2 | sonnet → gpt-5.5 (OpenAI) | HALT/constraint discipline | 0.92 | 0.88 (F-P9-3 down-graded HIGH→MED) |
| R3 | opus → claude-opus-4-8 (Anthropic) | coherence + evidence grounding | — | 0.95 |

`t2_model_class_diversity: full` · `t2_vendor_diversity: multi` · `calibrator_diversity: full`

## Findings (deviation taxonomy — "proposed strategy vs spec")

### F1 — HIGH (Drift→Regression-class against project rule): F-P9-2 human-gated sign-offs missing from HALT list

- **Evidence:** AMALGAMATED:163 explicitly requires `T09.01` (ops-reviewer exercise), `T09.04`/`T09.08`
  (sign-off capture), `T09.05` (tabletop rehearsal + sign-off) to **"HALT + write PENDING rather than
  auto-fill a date/sign-off line"** (cites `feedback_human_decision_items_must_halt`).
- **Gap:** BUILD-REQUEST:34-40 (the mandatory HALT list) enumerates only F-P1-3, RW-3, F-P3-4, F-P7-1, F-P9-1.
  **F-P9-2 is absent.** Scope item 9 (BUILD-REQUEST:27) collapses it into a generic "F-P9-1..5: Phase 9 PLAN
  edits" blob, losing the HALT designation entirely.
- **Why asymmetric-cost:** auto-filling a sign-off/date fabricates a false record of human approval. The cost
  of halting is operator-review latency; the cost of NOT halting is an unauthorized release/process attestation.
  Converged across R1 (MED) and R2 (CRITICAL); calibrated to **HIGH**.
- **Fix:** add an F-P9-2 entry to the BUILD-REQUEST HALT list naming the four task IDs.

### F2 — MEDIUM (Drift): F-P9-3 OPS-003/OPS-001 ownership decision neither HALT-listed nor pre-resolved

- **Evidence:** AMALGAMATED:164 — *"decide whether OPS-003 or OPS-001 owns the `return-contract.yaml`
  troubleshooting recipe; reconcile the roadmap AC."* "Decide" = open decision; the fix mutates a roadmap
  acceptance criterion.
- **Gap:** present in scope item 9 as a fix, but not in the HALT list (BUILD-REQUEST:34-40) and not resolved by
  the spec. A roadmap-AC mutation applied without a human ruling is the same failure class as F1, lower stakes.
- **Single-reviewer finding (R2 only; R1 marked it COVERED-grouped, R3 did not flag)** — surfaced because it
  withstood calibration, severity reduced from R2's HIGH to MEDIUM.
- **Fix:** either add F-P9-3 to the HALT list, or have the BUILD-REQUEST pre-state the ownership choice.

### F3 — LOW (Drift): F-P8-1 "author vs reconcile/rename" is a latent decision, not a settled fix

- **Evidence:** AMALGAMATED:144 — author `test_subprocess_caller.py` **or** reconcile/rename vs existing
  `tests/swarm/test_non_claude_caller.py` "if intent duplicates."
- **Assessment (R2+R3 converged):** acceptable as non-HALT **iff** the built task is constrained to inspect-first
  and default to the concrete non-spec-mutating deliverable (just author the test). The rename/reconcile branch,
  if it touches the tasklist/roadmap, would need HALT treatment.
- **Fix:** add a one-line construction guard to scope item 7 ("inspect T08.14/T08.02 first; author by default;
  do not auto-rename").

### F4 — LOW (cosmetic): unresolved `F-P3-?` placeholder token

- **Evidence:** BUILD-REQUEST:37 reads `RW-3 / F-P3-? :`. The spec never assigns RW-3 a phase-3 alias (it is
  F-P1-1 in Phase 1, AMALGAMATED:88). Dangling token.
- **Fix:** bind to canonical **RW-3**; drop the `F-P3-?`.

### F5 — LOW: §5 re-run matrix lacks command shapes for P1/P2/P3/P5/P7/P9

- **Evidence:** AMALGAMATED:188-192 defines a re-run matrix; only P8 gets a concrete command (AMALGAMATED:194-197).
  BUILD-REQUEST DoD (line 46) covers intent ("final checkpoint re-runs the per-phase reflects") but no command shapes.
- **Fix (optional):** add per-phase `/sc:reflect --mode post` command templates, or explicitly delegate command
  authoring to task-builder in the DoD.

### F6 — INFO: scope item 5 compresses F-P3-3..7 into one phrase

- Mitigated by BUILD-REQUEST:41 ("each fix task carries its amalgamation ID + file:line + verifier"), which forces
  task-builder to expand into 5 independently-verifiable tasks. No action required; note for task-builder.

## Evidence grounding (corroborating — opus reviewer, live SwarmPost code)

| Claim | Status | Observed |
|---|---|---|
| F-P3-1 (CRITICAL) stub transport no-op | **VERIFIED** | `commands.py:1030-1039` exposes `--transport stub`; `commands.py:1264-1266` calls `dispatch_wave1(..., transport=None)`; `dispatch.py:391-392` `if transport is None: return []`. Code self-documents the no-op at `commands.py:1245-1248`. |
| F-P1-3 (HIGH) DM dataclasses not frozen | **VERIFIED** | `models.py:87-88` plain `@dataclass class JobSpec` — no `frozen=True`. |
| F-P2-1 (HIGH) custom_prompt_dir unwired | **VERIFIED** | `run_preflight` (`preflight.py:1575-1815`) guards only `job.prompt.system` at `:1677-1683`; never reads `custom_prompt_dir`. `read_custom_prompt_dir` (def `:681`) is dead from the production path. |

**Line-drift note:** dispatch.py secondary cite `386-392`→ operative `391-392`; preflight `1670-1683`→ actual `1677-1683`.
Both within the spec's "re-confirm at build time" caveat (AMALGAMATED:10-12, BUILD-REQUEST:41). Findings unaffected.

## What the BUILD-REQUEST does well (no change needed)

- cwd/worktree discipline is explicit and correctly justified (BUILD-REQUEST:11-16) — the single most important
  constraint, since researching from `main` is exactly what invalidated the original Phase-8 reflect.
- Authoritative input pointer, priority order, exclusions (Phase 6 clean; original 8/REPORT.md superseded),
  per-task evidence+verifier mandate (line 41), repo rules (line 42), DoD (44-46) — all present and faithful.
- RW-6-LAST ordering is self-consistent (checkpoints must embed green output → regenerate after gates pass).
- De-dup alias chains (F-P1-1=RW-3, F-P1-2=RW-1, F-P3-2=RW-2, etc.) all resolve; no requirement lost to aliasing.

## Coverage summary

- **34 distinct requirements** (excluding 1 explicitly-excluded optional F-P1-6).
- **COVERED: 31.5** · **PARTIAL: F-P9-2, §5 re-run rows** · **MISSING: 0**.
- **coverage_pct ≈ 0.93** (above 0.90 floor). No requirement is wholly uncovered; the gaps are HALT-designation
  and command-shape completeness, not missing fixes.

## Grounding gaps / human decisions

- `needs_human_decision: true` — F1 (F-P9-2 HALT designation) and F2 (F-P9-3 ownership) are decisions the
  operator must make before the tasklist is built. They are surfaced here, not auto-resolved.
