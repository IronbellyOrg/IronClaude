# Refactoring Plan

## Overview

- **Base**: V3 (devops) — strongest on audit mechanics, tasklist actionability, query strings
- **Incorporated variants**: V1 (architect), V4 (field study)
- **Planned changes**: 12 (5 from V1, 7 from V4)
- **Rejected non-base alternatives**: 3 (V4 scope/placement/mechanism positions per settled-fork lock)
- **Overall risk**: Low — base provides full mechanical coverage; incorporations are additive or compromise refinements

## Planned Changes

### Change 1 — Restore symptom-coverage scoring as orchestrator synthesis logic

- **Source**: V1 Audit Mechanics → Branch F (symptom-coverage audit)
- **Target in base**: `refs/diagnosability-audit.md` Section 4 (Sufficiency Rubric)
- **Integration approach**: V3's base does not have an explicit 3-W's (when/where/why) cross-reference step. Append the V1 Branch F logic as a synthesis step within Section 4: after Branches A+B return, the Wave 1.6 orchestrator computes `{ when_answerable, where_answerable, why_answerable }` against the Branch A inventory + Branch B reachability before applying the sufficiency rubric.
- **Rationale**: Debate Axis 1 verdict — branch count is 2, but the symptom-coverage analytical content is preserved.
- **Risk level**: Low (additive synthesis step; no new MCP call)

### Change 2 — `--depth deep` does NOT force hard-stop (V1 position with Round-2 refinement)

- **Source**: V1 Off-Ramp UX → `--depth deep` interaction
- **Target in base**: V3's `Off-Ramp UX` section (`--depth deep` interaction subsection)
- **Integration approach**: Replace V3's "forces hard-stop on insufficient" with V1's "does not force hard-stop" — BUT add the Round-2 compromise: under `--depth deep`, the soft-warn path is mandatory and cannot be suppressed; REPORT.md gains a prominent "Your hypothesis depth was constrained by insufficient evidence" banner when `verdict ∈ {insufficient, partial}`.
- **Rationale**: Debate Axis 4 verdict
- **Risk level**: Low (purely UX; banner is additive)

### Change 3 — `--no-escalate` suppresses hard-stop (V1 position)

- **Source**: V1 Off-Ramp UX → `--no-escalate` interaction
- **Target in base**: V3's `Off-Ramp UX` section
- **Integration approach**: V3 already aligned on this (suppresses hard-stop). No change needed; V1's framing of "the hard-stop IS an escalation in spirit" adopted as the rationale text.
- **Rationale**: V1+V3 convergence, V1's framing slightly sharper
- **Risk level**: Low

### Change 4 — Comprehensive SKILL.md diff sketch (V1's table)

- **Source**: V1 SKILL.md Diff Sketch
- **Target in base**: V3's `SKILL.md Diff Sketch` section
- **Integration approach**: V3's diff sketch is high-level (11 numbered changes, prose). V1's is a structured table with current line ranges per change. Replace V3's section with V1's table, substituting V1's contract-field set with V3's (4 fields, no `status` enum extension).
- **Rationale**: V1 has higher fidelity for the maintainer who will eventually apply the diff
- **Risk level**: Low (documentation refinement)

### Change 5 — Hypothesis-card-template note (V1 only)

- **Source**: V1 Ref-File Changes → Modified ref `refs/hypothesis-card-template.md`
- **Target in base**: V3's Ref-File Changes section (which lists only `refs/diagnosability-audit.md` as new + `refs/report-template.md` as modified)
- **Integration approach**: Append V1's one-line addition under `## Grounding gaps` for cross-referencing the diagnosability card when verdict ∈ {partial, insufficient}.
- **Rationale**: Tightens the coupling between Wave 1.6 verdict and Wave 1.7 hypothesis grounding
- **Risk level**: Low (one-line addition)

### Change 6 — Byte-count metric (V4 additive)

- **Source**: V4 §3.3 S0.2 + seed brief additives §1
- **Target in base**: V3's Sufficiency Rubric + `refs/diagnosability-audit.md` Section 4
- **Integration approach**: Add a "captured-bytes" column to the Diagnosability Context Card's "Log-call coverage" table. Branch A's runtime-content sniff (when log file paths are available from the failing-run transcript) populates the column; otherwise marked `n/a (audit-time only)`. Sufficiency rubric promotes `0 bytes captured` from any non-zero-call stream to `insufficient` regardless of static call-density.
- **Rationale**: Phase 0 T4 case study — static call-count alone failed to detect that captured content was zero
- **Risk level**: Low (additive column + one rubric rule)

### Change 7 — Invocation-site-only instrumentation rule (V4 hard constraint)

- **Source**: V4 §5 R2 + seed brief additives §2
- **Target in base**: V3's Tasklist Artifact Format section
- **Integration approach**: Add a top-of-section HARD CONSTRAINT block: "Every task in this tasklist MUST target an invocation site (test script, CI workflow YAML, dev harness, container entrypoint), NEVER the failing component's own source code. Diagnostic code in production source leaks into release artifacts." V3's 5-task worked example is updated: any task currently targeting `src/worker/processor.py` is re-framed as targeting the invocation-site path (e.g., the test script that calls `processor.py`) OR explicitly marked as "instrument via invocation-site config override (e.g., `LOG_LEVEL=DEBUG` env var in the test runner)".
- **Rationale**: Phase 0 §5 R2 — diagnostic source leakage is a documented anti-pattern. This is the highest-impact V4 additive.
- **Risk level**: Medium (V3's worked example needs updating; some tasks may not have a clean invocation-site equivalent — those tasks become "set env var X at invocation site" tasks instead)

### Change 8 — 3-round patch-loop cap (V4 additive)

- **Source**: V4 §3.7 + seed brief additives §3
- **Target in base**: V3's Off-Ramp UX section + Risk Register
- **Integration approach**: Add a new "Re-run loop semantics" subsection to Off-Ramp UX. The Wave 1.6 orchestrator tracks a per-defect patch round count (keyed by the `issue_slug` from Wave 0). After the 3rd round with verdict `insufficient`, the chat-message off-ramp escalates: "This defect has hit the 3-round diagnosability cap. The symptom does not appear observable via cheap log additions; consider structural changes (refactor for testability, add a dedicated diagnostic mode, or escalate to a debugger session). Wave 1.6 will not emit another tasklist for this issue without `--reset-diagnosability-rounds`."
- **Rationale**: Closes Open Question #6 cleanly. Without this cap, agents iterate indefinitely.
- **Risk level**: Low (requires per-issue state tracking — implementable via `<output-dir>/diagnosability-rounds.json` keyed by issue slug)

### Change 9 — Heisenbug fallback (V4 additive)

- **Source**: V4 §5 R3 + seed brief additives §4
- **Target in base**: V3's Risk Register + Off-Ramp UX
- **Integration approach**: Add a new risk entry "R6: Instrumentation alters timing (Heisenbug)". Mitigation: if the user re-runs with the tasklist applied and reports "the symptom no longer reproduces," Wave 1.6's re-entry logic records this as a Heisenbug finding in the audit card and the next-round tasklist is downgraded to env-vars-only (no `--debug` flag changes, no log-level overrides, no additional logger calls — just minimum-perturbation observability).
- **Rationale**: Phase 0 §5 R3 — instrumentation that hides the bug is signal, not failure
- **Risk level**: Low (additive risk + downgrade logic in re-entry path)

### Change 10 — Component-identification step S0.1 (V4 additive)

- **Source**: V4 §3.3 S0.1 + seed brief additives §5
- **Target in base**: V3's Wave 1.6 Placement & Entry/Exit Criteria
- **Integration approach**: Insert a new first step in Wave 1.6's procedure: "S0.1 — Failing-component identification. Before spawning Branches A and B, identify the smallest component whose output the failure asserts against. Use Wave 0's `--scope` if set; otherwise extract from Wave 1's grounding observations (stack-trace bottom frame, named test failure, named subsystem in the issue text). Record the identified component path in the audit log as `failing_component`." Branches A and B then scope their queries to this component first, expanding outward only if no signal is found.
- **Rationale**: Phase 0 §3.3 — relying on `--scope` alone misses cases where `--scope` is set too broadly or not at all
- **Risk level**: Low (additive first step)

### Change 11 — T4 worked example as canonical ref-file illustration (V4 additive)

- **Source**: V4 §4 + seed brief additives §6
- **Target in base**: New section in `refs/diagnosability-audit.md` (Section 8 — Worked Example)
- **Integration approach**: Embed the T4 zellij contract-test case study verbatim from V4 §4 as Section 8 of the new ref file. The example walks through S0.1 → S0.2 → S0.3 → S0.4 → S0.5 with concrete signals and the resulting instrumentation patch. Annotated to show how the section maps to Wave 1.6's Branch A + Branch B + sufficiency rubric.
- **Rationale**: Concrete grounded example > abstract description. Aids future skill maintainers and reviewers.
- **Risk level**: Low (purely illustrative)

### Change 12 — Bypass-is-logged discipline + "no hypothesis in same turn" rhetoric (V4 additives)

- **Source**: V4 §6 R5 + V4 §3.5 + seed brief additives §7
- **Target in base**: V3's Off-Ramp UX + V3's Will Do/Will Not Do (in SKILL.md diff)
- **Integration approach**: (a) When `--no-diagnosability-audit` is used, REPORT.md's header gains a line: `Diagnosability audit: SKIPPED (--no-diagnosability-audit, user-bypassed)`. The bypass is also logged in the audit log. (b) Add to the SKILL.md "Will Do" list: "Halt Waves 1.7-5 when Wave 1.6 fires the hard-stop. No hypothesis work happens in the same turn as an instrumentation patch — the user re-runs after instrumenting."
- **Rationale**: Auditability (R5) + temporal-discipline framing (§3.5)
- **Risk level**: Low

## Changes NOT Being Made (rejected alternatives — transparency)

| # | Alternative | Source | Rejection reason |
|---|-------------|--------|------------------|
| 1 | Broaden scope to include CLI debug flags + OS introspection + doctor commands | V4 §3.3 S0.3 | Settled-fork lock — user maintained "logging only (narrow)" scope (Option A, 2026-05-29). Tracked for v1.1. |
| 2 | Move audit to pre-Wave-1 placement (true "Phase 0") | V4 §3.1 + §5 | Settled-fork lock — user maintained "between 1.5 and 1.7" placement (Option A, 2026-05-29). Tracked for v1.1. |
| 3 | Shell-based discovery (auggie not required) | V4 §3.3 S0.2 | Settled-fork lock — auggie remains primary discovery mechanism for logging-only scope. V4's shell discovery was bundled with broader scope; with scope locked narrow, auggie's static log-call retrieval is sufficient. |
| 4 | Binary verdict (sufficient / insufficient) | V4 §3.4 | V1 + V3 converged on quaternary verdict (`sufficient | partial | insufficient | unknown`). Quaternary provides finer-grained signal for the soft-warn-vs-hard-stop branching and supports the `--no-diagnosability-audit` `unknown` case without conflating "audit skipped" with "audit ran and found nothing." |
| 5 | 3-branch fan-out (D + E + F) | V1 | Debate Axis 1 verdict — folded symptom-coverage (Branch F) into orchestrator synthesis. 2-branch saves ~500-700 Claude tokens with no coverage loss. |
| 6 | `status` enum extension to include `halted_diagnosability` | V1 | Debate Axis 3 verdict — dedicated `diagnosability_hard_stop: bool` field is safer for downstream consumers with exhaustive `status` switches. |
| 7 | Audit card named `diagnosability-audit.md` | V1 | Debate Axis 2 verdict — `diagnosability-context.md` preserves naming-symmetry with Wave 1.5's `doc-context.md`. |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|--------|------|-----------------|----------|
| 1 | Low | Symptom-coverage scoring misses a case the dedicated branch would have caught | Promote to 3rd branch in v1.1 |
| 7 | Medium | V3's 5-task worked example requires re-framing; some tasks may not have clean invocation-site equivalents | Revise worked example; for un-cleanly-relocatable tasks, document as "config-override at invocation site" pattern |
| 8 | Low | Per-issue state tracking adds a small disk-state surface | Drop the cap; revert to no-cap iteration |
| All others | Low | Additive or compromise refinements; revertible by reverting the relevant section | Standard git revert |

## Review Status

Auto-approved (non-interactive mode). Timestamp: 2026-05-29T15:25:00Z.
