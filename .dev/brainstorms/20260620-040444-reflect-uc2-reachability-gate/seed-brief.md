---
topic: "Harden /sc:reflect UC-2 to catch silent runtime-surface / durable-invariant reachability gaps (contracted-sink unreachable + wrong-sink oracle), via a Production Side-Effect Reachability & Oracle Gate"
domain: code
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-20
blind: true
models: [sonnet, haiku]
---

# Seed Brief: reflect-uc2-reachability-gate

## Problem Statement

`/sc:reflect` UC-2 (post-execution audit) cannot catch a **silent runtime-surface / durable-invariant
reachability gap**: a feature passes unit tests and emits a parallel observable (journald), but the
contracted durable sink (an HMAC `audit_log` chain) is **never reached** at the real production entrypoint
because (a) the composition root never binds the process-wide facade (`audit.SetDefault` is missing),
(b) the emitter's error is silently discarded (`_ = audit.EmitSpawn(...)`), and (c) the e2e oracle greps
journald, not the chain (a false-positive oracle). The failure **fails open** — a discarded error on a
never-bound global — so it is invisible to a divergence-first audit.

## Re-grounded gap confirmation (real file:line in THIS checkout)

The §3 gap holds. Evidence opened directly:

- **Evidence chain is symbol/diff/test-oriented, never proves composition-root→sink reachability.**
  `SKILL.md:453-494` (§6.1 Wave-1A chain): steps are `get_symbols_overview`, `find_declaration`,
  `find_symbol`, `find_implementations`, `find_referencing_symbols`, `get_diagnostics_for_file`,
  `execute_shell_command` verification triangle (step 5.5, `SKILL.md:474,490`), re-Read citations,
  `summarize_changes`. None require proof that the production entrypoint → composition root → contracted
  sink is wired.
- **Taxonomy is divergence-first → invisible when code is present + tests green.** `SKILL.md:907-983`
  (§10.1–10.5): every detection signal keys on an *observable* divergence (hunk maps / doesn't map /
  contradicts criterion / has rationale). A *missing* `SetDefault` bind (a non-edit) plus a discarded error
  classifies as nothing.
- **§10.4 Regression signals don't trip on a fail-open discarded error.** `SKILL.md:956-976`: signals are
  (a) hunk contradicts a spec criterion, (b) a previously-passing test now fails (step-5.5 triangle),
  (c) documented invariant violated. A green-tests fail-open trips none.
- **No oracle-admissibility obligation: a journald grep counts as grounded evidence for a durable-HMAC-chain
  requirement.** The step-5.5 triangle (`SKILL.md:490`, §6.1.1 `SKILL.md:496-510`) trusts a passing
  `pytest` exit 0 regardless of whether the test's *sink* equals the requirement's *contracted sink*.
  The exit-code taxonomy (`SKILL.md:962-974`) maps exit codes, not oracle-sink identity.
- **Wave 5 only renders; findings must be injected upstream.** `SKILL.md:155` (Wave 5 = Synthesis +
  evidence-validator + report). Any new finding must enter at Wave 1A/1B, not Wave 5.

## Consumer wiring already exists (decisive architecture fact)

`src/superclaude/cli/reflect/contract.py` is a PURE consumer that already routes the new gate's outputs:

- `regression_present is True` → HALTED / exit 10 (`contract.py:315`)
- `needs_human_decision is True` → HALTED / exit 10 (`contract.py:319`)
- `status: partial` → HALTED (`contract.py:313`)
- `classify_fix`: `regression_present` OR `needs_human_decision` → `human-required` (`contract.py:356-363`)
- Unknown top-level fields are tolerated/read-and-ignored (NFR-8, `contract.py:66-82`).

⇒ The gate is a pure **upstream producer** change. `unreachable`/`oracle_mismatch` → set
`regression_present: true`; `unproven` → grounding-gaps non-empty → `needs_human_decision: true` +
`status: partial`. No consumer code change is *required* (a small fail-closed defense-in-depth trigger is
optional). Existing fixtures `halted_regression.yaml`, `human_required_needs_decision.yaml` prove the routes.

## Cost fact (kills the "drags into Tier 2" worry)

The "real-boot verifier" is just another `execute_shell_command` integration assertion — the **same tool the
step-5.5 verification triangle already runs in Wave 1A / Tier 1** (cost-profile T1 = 3–8k Claude tokens). It
rides the existing T1 machinery; it does not force Tier 2.

## Leading hypothesis (to red-team — strong draft, not gospel)

Mandatory UC-2 "Production Side-Effect Reachability & Oracle Gate": Wave-1A fail-open static scan
(unbound facade / nil-or-default sink / discarded emitter result) + Wave-1B reachability trace + real-boot
verifier (sink observed the effect; unit stubs don't satisfy) + oracle-admissibility rule (oracle sink ==
contracted sink). Emits `runtime-reachability-ledger.yaml`. Fail-closed: `unreachable`/`oracle_mismatch`-while-
done = Regression; `unproven` = Grounding Gap (`status: partial`, `needs_human_decision`). Tier-1 only for
side-effect-bearing requirements; trigger on MUST/SHALL acceptance-criteria semantics + a side-effect taxonomy.

## Constraints / Definition of Done

- Edit `src/superclaude/` → `make sync-dev` → `make verify-sync`. Feature branch only.
- Keep common UC-2 path Tier-1; charge only side-effect-bearing requirements.
- Fail closed: ambiguity → `unproven`/Grounding Gap, never a false Regression, never a silent pass.
- Inject findings upstream of Wave 5.
- Deliver: design note + concrete per-file edits + fail-before/pass-after reflect self-test + risk/rollback.
- Ground every claim in a real `file:line`.

## Open Questions (for red-team)

1. False-positive blast radius on async / env-gated / intentionally-indirect-DI effects — does
   `unproven`→Grounding-Gap actually contain it without flooding human-decision?
2. Trigger precision: keyword grep vs MUST/SHALL semantics vs an explicit tasklist "side-effect requirement" tag.
3. Cost: does the real-boot verifier stay Tier-1 or drag runs into Tier-2 in practice?
4. Reviewer integration: grounding-hunk transport vs a rubric dimension (#4 Risk surface coverage).
5. Generalization beyond audit (DB write / queue publish / file persist / event emit) vs overfit to this incident.
6. Alternatives to re-open: rubric-only; mandatory `--tasklist`; 5th taxonomy category; standalone
   reachability sub-command vs in-line UC-2 gate.
