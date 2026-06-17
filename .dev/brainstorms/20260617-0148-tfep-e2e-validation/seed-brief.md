---
topic: "Devise 4 e2e tests with acceptance criteria that you can delegate to subagents to run 3x that will generate an auditable papertrail to confirm and validate the work done achieves the desired outcome"
domain: process
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-06-17T01:48:00Z
---

# Seed Brief: TFEP forensic→troubleshoot Migration — E2E Validation Suite

## Problem Statement

The just-completed MDTM task migrated the Test Failure Escalation Protocol (TFEP) off the
unavailable `/sc:forensic` backend onto `/sc:troubleshoot` via a thin adapter + backend-neutral
terminology, touching 5 source files. The work passed 5 phase-gate QA cycles + a post-completion
gate. We now need an INDEPENDENT, REPRODUCIBLE end-to-end validation suite — 4 e2e tests, each with
explicit acceptance criteria — that can be **delegated to subagents and run 3× each** to confirm the
migration achieves its desired outcome, while emitting an **auditable paper trail** (evidence files
with verdicts) that a human reviewer can inspect without re-deriving anything.

Because the migration is docs/skill PROSE (no Python; `TESTING_REQUIREMENTS=NONE`, verify-sync is the
regression analog), "e2e test" here means a *behavioral validation scenario* an agent executes by
reading/tracing the protocol files and running deterministic shell probes (rg/grep/make verify-sync,
token cross-checks, chain traces) — NOT pytest. Each test must be self-contained, deterministic enough
that 3 independent runs agree, and must write a machine-readable + human-readable evidence artifact.

## Known Context (the desired outcome being validated)

The 5 edited files: `src/superclaude/skills/sc-task-protocol/SKILL.md` (§4.5 TFEP consumer),
`src/superclaude/commands/task.md`, `src/superclaude/commands/troubleshoot.md`,
`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (producer), and
`.../sc-troubleshoot-protocol/refs/report-template.md`.

The migration's **desired outcome** = TFEP works end-to-end against the troubleshoot backend:
1. **Backend swap is complete + clean**: zero live `/sc:forensic`/bare-`forensic`/`--tier`/`--intent`/`rca-verdict`/`solution-verdict` in the two task-protocol files; `src/` has zero `/sc:forensic`; src↔.claude sync parity (verify-sync EXIT 0); no `.claude/` staged.
2. **Adapter contract integrity (producer↔consumer)**: every field the §4.5 consumer reads (`status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`) has a producer in the troubleshoot Output Contract AND the report-template `## TFEP Consumer` block; the 7-field wire set is identical across all three surfaces; enums (`recommended_escalation` none|retry|escalate_depth|halt; `remediation_target` test|code|docs|none) byte-match; `contract_version` bumped to 1.1.0.
3. **End-to-end protocol chain resolves**: trigger → freeze (Step 1) → context.yaml (Step 2, bound to `{context_path}`) → dispatch `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {standard|deep}` (NO `--fix`) → Wave 0 step 6 ingests `--caller`/`--context` → Wave 5 step 4.5 emits `return-contract.yaml` when `caller=task-unified` → Step 4 consumes + branches on the adapter enum → Step 5 composes + inserts the adjudicated plan → Step 6 resumes. Depths map consistently (1st→standard; escalation/systemic/≥3-new→deep; 3rd→FULL STOP); the Step 4 branch ladder is a deterministic, terminating decision procedure (first-match-wins; loop increments escalation_count; halt/failed → immediate FULL STOP).
4. **Safety invariants preserved**: Step 1 freeze block byte-identical to the pre-migration baseline; NO `--fix` anywhere in the §4.5 dispatch; asymmetric-cost gates present (`test_is_wrong`→present-for-review; `remediation_target == "docs"`→present-for-review, both "do not auto-apply"); backend-neutral prose (a future swap touches only the `**Diagnostic backend:**` declaration + the invocation/budget strings).

## Constraints

- DELEGABLE: each test must be expressible as a single self-contained subagent prompt (rf-qa or general-purpose) with all paths/commands embedded; no shared mutable state between runs.
- REPRODUCIBLE 3×: a test must be deterministic enough that 3 independent runs produce the same PASS/FAIL verdict; non-determinism (e.g., LLM judgment) must be bounded by concrete shell-grounded checks so the verdict is evidence-anchored, not opinion.
- AUDITABLE PAPER TRAIL: every run writes a timestamped evidence file (machine-readable verdict block + human-readable findings + the exact commands/outputs it ran) to a per-test, per-run path; a final aggregator must be able to read all 12 run-artifacts (4 tests × 3 runs) and emit a cross-run consistency verdict.
- READ-ONLY / NON-MUTATING: the validation suite must NOT modify the 5 migrated files or stage anything; it only reads + runs read-only probes (rg, grep, make verify-sync is read-only, git status).
- NO PYTEST: the migration touched no Python; validation is shell-probe + protocol-trace based.
- SCOPE: validate ONLY the migration's stated desired outcome (the 8 pipeline changes / 4 outcome dimensions above), not pre-existing unrelated skill content.

## Success Criteria (for the validation suite design itself)

- Exactly 4 e2e tests, each mapped to one of the 4 desired-outcome dimensions, with NO coverage gap and minimal overlap.
- Each test has: a precise scope, an embedded delegable subagent prompt, an ordered list of deterministic probe steps, explicit binary acceptance criteria (PASS iff all criteria hold), and a defined evidence-artifact schema.
- A defined 3× execution + aggregation protocol: how the 12 runs are spawned, where artifacts land, how cross-run agreement is computed, and what the final "migration validated" verdict requires (e.g., all 4 tests PASS in all 3 runs = 12/12 green).
- A defined audit-trail format that a human can read end-to-end to independently confirm the outcome without re-running anything.

## Open Questions (to be resolved by the adversarial merge)

- How much of each test should be deterministic shell-probe vs bounded LLM protocol-trace, and how to anchor the LLM portions to evidence so 3× runs agree?
- Should the 4 tests be (A) residual-integrity, (B) contract round-trip, (C) protocol-chain simulation, (D) invariant/safety — or a different decomposition that better covers the outcome with cleaner test boundaries?
- What is the right evidence schema (YAML verdict block fields) and the cross-run aggregation rule (strict 12/12, or majority-per-test with a documented tolerance)?
- How to make the 3× runs genuinely independent (fresh subagent context, no artifact reuse) while keeping the paper trail consolidatable?
- What "negative" / falsification checks should each test include so a PASS means "evidence we thoroughly checked," not "found nothing"?

## Enrichment Context (concrete probe surface — quality_tier: primary)

Deterministic, read-only probes available to ground the e2e tests (all run from the worktree root
`/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`):

- **Residual sweep**: `rg -n "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md` → expect 0 hits. `rg "/sc:forensic" src/` → 0.
- **Sync parity**: `make verify-sync` → EXIT 0, "All components in sync", no DIFFERS/MISSING. `git status --porcelain | grep '\.claude/'` → none staged.
- **Adapter rows / version**: `rg -c "TFEP adapter field \(contract v1.1.0" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` → 5; contract_version default bumped to 1.1.0.
- **Producer/consumer tokens** (7): status, test_is_wrong, recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary — present in §4.5 consumer AND troubleshoot Output Contract AND report-template `## TFEP Consumer`.
- **Declaration + dispatch**: §4.5 has exactly one `**Diagnostic backend:** troubleshoot`; the Step 3 dispatch is `/sc:troubleshoot --caller task-unified --context {context_path} --output-dir {output_dir} --depth {depth}` with NO `--fix`; Escalation Budget uses `/sc:troubleshoot ... --depth standard|deep`.
- **Freeze baseline**: recorded verbatim at `.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md` (STOP testing + FREEZE implementation — for byte-identical diff).
- **Step 4 branch ladder**: precedence note (first-match-wins, asymmetric gates first); branches key on `test_is_wrong`, `remediation_target == "docs"`, `status`, and the 4 `recommended_escalation` enum values; loop discipline (re-enter Step 3 + increment escalation_count; escalate-from-deep→FULL STOP; halt/failed→immediate FULL STOP).
- **Pre-existing out-of-scope noise to ignore**: bare "forensic" appears as generic vocabulary in unrelated skills (cli-eval, sc-crash-recovery, sc-brainstorm-protocol, sc-reflect-protocol) — NOT the `/sc:forensic` backend; tests must scope to the 5 migrated files.

enrichment_used: [{source: codebase, quality_tier: primary (in-context from completed migration)}]
