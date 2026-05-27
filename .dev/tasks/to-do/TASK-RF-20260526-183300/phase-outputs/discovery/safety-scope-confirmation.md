# Safety and Scope Confirmation

**Captured:** 2026-05-26
**Step:** Phase 1, Step 1.2
**Inputs read:**

- `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md` lines 3-9 (Decision) and lines 477-489 (Rollback Recommendation)
- `src/superclaude/commands/brainstorm.md` (full file inspected; gating search performed)
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (full file inspected; gating search performed)

## Live Exposure Assessment

The current live `/sc:brainstorm` behavior **is the default user-facing behavior**. Evidence:

- `src/superclaude/commands/brainstorm.md` has no `experimental`, `preview`, `beta`, `disabled`, or top-level rollout gate. The only `flag-gated` references are for handoff (Wave 4) — i.e., what to do AFTER brainstorm completes — not for whether brainstorm executes its live synthesis behavior.
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` has no opt-in flag for the live synthesis behavior. The merged-requirements contract, seed-brief schema, and adversarial merge pipeline are unconditional.
- The command is registered, the skill is loaded, and any user invoking `/sc:brainstorm <topic>` today triggers the live behavior under audit in the remediation plan.

**Implication:** The lossy synthesis behavior the remediation plan flags (lost concrete anchors, generic-over-concrete merges, missing provenance, fit-to-intent drift) is reaching users right now.

## Rollback / Gating Documentation Required?

Per the remediation plan (lines 477-489), if the current live implementation is affecting normal users, the recommended posture is:

1. Temporarily roll it back or gate it
2. Preserve live outputs and eval artifacts as regression evidence
3. Reintroduce live improvements only after contract, provenance, and context-retention fixes land

**This task does NOT perform that rollback.** This task is targeted remediation that fixes the protocol IN PLACE (Phases 2-4) and validates the fix against cases 4-11 (Phase 6) before accepting the new state.

The remediation plan's "Decision" section (lines 5-9) explicitly says: "Keep iteration-2 baseline as the quality bar, freeze or roll back live as the default, then selectively reintroduce live's useful improvements behind stricter provenance, context-retention, and fit-to-intent gates. This is not a full discard. Live has useful ideas, but its current synthesis behavior is too lossy."

So the project-level disposition has two paths:

- **Path A (this task):** Remediate in-place. Update protocol contracts, merge rules, and eval gates so the next user `/sc:brainstorm` invocation gets the fixed behavior. Cases 4-11 acceptance gate (Phase 6) verifies the fix landed.
- **Path B (separate follow-up):** Temporary rollback/gating of `/sc:brainstorm` while Path A is in flight, so users don't experience the lossy behavior in the meantime. **This task does not implement Path B**, but Path B is identified as a separate follow-up requirement and should be tracked.

**Required follow-up (logged separately):** A separate rollback/gating task is needed if Path A's remediation lands slowly. Suggested form: feature flag in `src/superclaude/commands/brainstorm.md` that defaults `/sc:brainstorm` to the iteration-2 behavior baseline until cases 4-11 acceptance passes; OR a temporary disable of the live synthesis path. Decision deferred to operator.

## Non-Rollback Statement

**This task is not a blanket rollback.** Confirmed:

- Phases 2-4 EDIT the protocol contracts, merge rules, and eval logic in-place — they do not delete or revert files.
- The remediation plan explicitly preserves useful live improvements: governance/safety framing, source-of-truth safeguards, rollback/purge/disablement controls, lifecycle taxonomies, policy-first framing, and proof gates.
- Phase 3 adversarial merge updates require concrete-over-generic precedence, threshold preservation, and dropped-anchor rationale — these AUGMENT existing live behavior rather than removing it.
- Phase 4 eval assertion updates do not delete existing eval cases or rollback comparison logic — they extend assertions to catch the failure modes documented in the comparison JSON.

## Live Improvements to Preserve (Explicit List)

From the remediation plan, these live improvements are preserved as augmentation, not removed:

1. Governance/safety framing in seed and merge protocols
2. Source-of-truth safeguards (UV-only, no generated mirror staging)
3. Rollback/purge/disablement control vocabulary in merged requirements
4. Lifecycle taxonomies (e.g., proposal → review → approval → execution)
5. Policy-first framing for safety-critical merges
6. Proof gates (acceptance criteria with measurable thresholds)

Phase 2 protocol-contract edits must preserve these as augmentation. Phase 3 adversarial merge updates must allow these to remain in merged output. Phase 4 eval assertion updates do not remove existing assertions covering these.

## Decisions and Verdicts

| Decision | Verdict | Evidence |
|----------|---------|----------|
| Live exposure: default-user-facing? | **Yes** | No gating flag in `commands/brainstorm.md` or `skills/sc-brainstorm-protocol/SKILL.md` |
| Rollback/gating documentation required before promotion? | **Yes (separate follow-up)** | Remediation plan lines 479-483 |
| This task IS a rollback? | **No** | This task does targeted in-place remediation; rollback is a separate follow-up |
| Useful live improvements preserved? | **Yes** | List above; Phases 2-4 augment rather than remove |
| Phase 2 may proceed after PG-1 PASS? | **Yes (no blocker)** | Per Phase 1 Findings — no contradictions found |

## Scope Note

**Verified inputs:**

- `.dev/tasks/to-do/TASK-RF-20260526-183300/research/03-eval-and-validation-targets.md` lines 52-56 (compare_live_runs.py `CASE_IDS = set(range(4, 12))`, case 12 excluded from current comparison; live-run error artifact exists for case 12)
- `.dev/tasks/to-do/TASK-RF-20260526-183300/research/05-gap-fill-research-gate-remediation.md` lines 44-55 (case 12 error artifact details, exact blocker text, intentional deferral rationale)
- `.dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-plan.md` lines 419-427 (acceptance metrics for cases 4-11)

**Cases 4-11 are the quality acceptance scope for this remediation.** The metrics that govern PG-6 (qualitative acceptance) are:

- Structural pass rate ≥ 95%, target 100%
- Qualitative baseline wins ≤ 2 of 8
- Live average ≥ 52/60
- Provenance average ≥ 8.50
- Concreteness average ≥ 8.50
- No missing dedicated Provenance sections
- No critical seed anchors dropped without rationale

**Case 12 is intentionally excluded unless command/skill registry compatibility is brought into scope.** The case 12 blocker is the literal error string:

> `Unknown skill: sc:brainstorm-protocol`

…captured in `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-graphql-public-api/live-run-error.md` lines 6-10 per research/05 lines 50-53. The case failed BEFORE protocol execution — no synthesis artifacts were produced. This is a command-dispatch / skill-registry compatibility issue (the dispatcher could not locate the protocol skill under that name), not a synthesis-quality issue addressable by Phase 2-4 protocol-contract / merge-rule / eval-assertion edits.

**This task does not silently drop case 12.** Its exclusion is explicitly rationale-documented per research/05 line 55 ("case 12 should remain explicitly deferred unless the remediation scope includes command/skill registry compatibility"). `compare_live_runs.py` Phase 4 Step 4.3 edit must keep `CASE_IDS` at `set(range(4, 12))` and document the exclusion in-script. Phase 6 acceptance metrics apply to cases 4-11 only.

**This task does not broaden into registry compatibility work.** Investigating and fixing `Unknown skill: sc:brainstorm-protocol` requires examining command dispatcher behavior, skill name registration, and possibly the `sc:` / `sc-` skill-name convention split — none of which is in scope here. A separate task is required if the operator decides to bring case 12 into the acceptance scope. This task does not preemptively allocate effort or fabricate any case 12 results.
