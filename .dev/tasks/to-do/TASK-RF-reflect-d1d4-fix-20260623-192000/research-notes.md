# Research Notes: Fix reflect audit findings D1–D4

**Date:** 2026-06-23
**Scenario:** A (explicit — findings already grounded by the /sc:reflect post-execution audit at `.dev/reflect/post-reflect-reviewer-guard-20260623185200/REPORT.md`)
**Depth Tier:** Standard
**Track Count:** 1 (all changes in the reflect subsystem; cohesive — share the L2 isolation design)

---

## EXISTING_FILES

- `src/superclaude/cli/reflect/ensemble.py` — Tier-2 ensemble dispatch.
  - `run_tier2_ensemble()` (`:168`) — builds worker spec, dispatches swarm, normalizes, emits contract.
  - Recipe `target` substitution (`:218`): `"target": str(config.tasklist_path)` — **the D1 gap**: the live tasklist path, not a snapshot-derived target.
  - `reviewer_isolation` telemetry (`:315-316`): `"snapshot" if config.reviewer_grounding_root else "disabled"` — **overclaims** when only the ClaudeProcess children are grounded.
  - adversarial scorer `cwd=config.reviewer_grounding_root` (`:366`) — correctly snapshot-grounded.
  - `build_worker_prompt()` (`:415`) and `_load_review_target()` (`:433`, reads `config.tasklist_path` at `:438`/`:441`) — the text-in/out worker target source; both reference the LIVE path, never `reviewer_grounding_root`.
- `src/superclaude/cli/reflect/runner.py` — Tier-1 audit child grounded via `cwd=config.reviewer_grounding_root` (`:441-461`); snapshot gate + try/finally teardown (`:605-711`).
- `src/superclaude/cli/reflect/config.py` — `create_review_snapshot` / `teardown_review_snapshot` (`:181-250`); `reviewer_grounding_root` set in runner.
- `src/superclaude/cli/reflect/models.py` — `ReflectConfig.reviewer_grounding_root` (`:362`), `ReflectResult.reviewer_isolation` (`:378`).
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — Step 0.5e item 4 (`:268`): "the text-in/out Tier-2 swarm workers hold NO repo CWD and instead **receive review targets derived from `<snapshot>`**." — the authored spec D1 violates.
- `src/superclaude/agents/reflect-reviewer.md` — "Rationale source" (`:133`) cites the **non-existent** `.dev/analysis/pr199-reflect-hardening-proposal-2026-06-22.md` as primary source — **the D3 gap**.
- `tests/cli/reflect/test_reviewer_isolation_gate.py` — L2 gate tests (asserts snapshot grounding + telemetry); the home for a new D1 swarm-worker-target test.
- `tests/cli/reflect/test_reviewer_finding_parity.py` — TST-4 static-reachability proxy (`:13-17` falsifier-EXEMPT label) — **D4, reclassified AUTHORIZED**; no code fix required.

## PATTERNS_AND_CONVENTIONS

- Source of truth `src/superclaude/`; after any SKILL.md/agent edit run `make sync-dev` then `make verify-sync`. Never stage `.claude/`.
- Tests: `tests/cli/reflect/`, run `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run pytest tests/cli/reflect/` (the env-strip avoids the wrapper-recursion self-suppression seen in §6.1.1(i)).
- Falsifier discipline (project hard rule): every NEW behavioral test must FAIL on the pre-fix tree and PASS after the fix. An invariant lock that passes pre-fix must be labeled falsifier-EXEMPT.
- `needs_human_decision` items must write PENDING + HALT, never auto-default a shipping design choice (memory `feedback_human_decision_items_must_halt`).
- Telemetry honesty: `reviewer_isolation` ∈ `{disabled, snapshot, stopped-precondition}` today; a partial-isolation value (e.g. `snapshot-children-only`) would need adding to models.py + ensemble.py + any test asserting the enum.

## GAPS_AND_QUESTIONS

- **D1 design decision (HALT):** two viable fixes — (a) **full grounding redirect**: make `_load_review_target` / `build_worker_prompt` / the recipe `target` resolve file references under `config.reviewer_grounding_root` (snapshot) when set, so the swarm workers actually read the snapshot; or (b) **telemetry-honesty narrowing**: keep children-only grounding but report `reviewer_isolation: "snapshot-children-only"` so the contract stops overclaiming. (a) closes the stated Step 0.5e item-4 guarantee; (b) is the smaller-blast-radius honest-contract fix. This is a genuine `needs_human_decision` — the executor must write PENDING + HALT, not auto-pick. (Research recommendation, non-binding: (b) is simpler and lower-risk since the swarm workers are text-in/out and the mutation vector is already closed by L1+L1b; (a) is the fuller fix if read-isolation for swarm workers is required.)
- **D2:** the per-phase QA bookkeeping inconsistency lives in the executed task file in the SIBLING worktree `.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-reflect-reviewer-guard-20260622-200400/`. The "fix" is reconciliation/documentation (mark the per-phase-gate items as substituted-by-final-assembly-gate, or record the substitution as an explicit Open Question), NOT a code change. Low value; include as a documentation-reconciliation item.
- **D4:** reclassified AUTHORIZED by the audit (the EXEMPT label is sanctioned by the task's own Key Constraint). No fix. Optional enhancement: add a live restricted-vs-all-tools recall comparison test (heavier, research/05 §4 deferred it). Encode as a NON-BLOCKING verification/clarification item only.

## RECOMMENDED_OUTPUTS

Single MDTM task file. Phases:
1. Setup + falsifier baseline (capture pre-fix test state).
2. **D1 HALT** — precedence/design decision (a) vs (b), write PENDING, HALT.
3. **D1 implementation** — consume the decision; edit ensemble.py (+ models.py/SKILL.md if (b) adds an enum value, or _load_review_target/build_worker_prompt if (a)); add a falsifier-disciplined test under `tests/cli/reflect/`; sync-dev + verify-sync if SKILL.md touched.
4. **D3** — fix reflect-reviewer.md `:133` citation to match the task instruction (cite the round-2 findings / the committed forensics docs, not the non-existent proposal); sync-dev + verify-sync.
5. **D2** — documentation reconciliation of the per-phase-QA bookkeeping (Open Question or explicit substitution note); NON-BLOCKING.
6. **D4** — verification/clarification item (confirm the EXEMPT label is correct + optionally note the live-parity enhancement as a follow-up); NON-BLOCKING.
7. Full verification (`uv run pytest tests/cli/reflect/`, ruff, verify-sync) + final QA gate + POST reflect gate.

## SUGGESTED_PHASES

Template 02 (discovery of swarm-worker wiring → HALT decision → build → test → verify). The D1 fix is the load-bearing phase; D2/D4 are NON-BLOCKING reconciliation/verification; D3 is a one-line documentary fix + sync.

## TEMPLATE_NOTES

Template 02. Standard tier. One `needs_human_decision` HALT (D1 design (a) vs (b)). Falsifier discipline on the new D1 test. POST reflect gate ENABLED (flat wrapper shell-out, penultimate). `executor_model_class: sonnet`. `start_commit` = current merge-base.

## AMBIGUITIES_FOR_USER

- D1 design (a) vs (b) is a real decision → encoded as a HALT, not resolved here.
- "Fix D1–D4": D4 needs no code fix (audit reclassified it Authorized). The task encodes it as a NON-BLOCKING verification item so the user's literal D1–D4 ask is honored without inventing a spurious change.
