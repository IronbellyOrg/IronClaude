```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.68
citations_total: 101
citations_revalidated: 101
citations_dropped: 3
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (UC-1 pre, Tier 2, shadow engine): TASK-WF-designSpec-20261107-075614

Run `pre-TASK-WF-designSpec-20261107-075614-comboE-r3`. Spec: `source.md` (design of the pr-submit merge guard, issue #375). Plan: `TASK-WF-designSpec-20261107-075614.md` (13 tasks). Paths are under `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/` (S = spec, P = plan).

## Verdict

The plan has **no blocking defect**. The audit produced 14 merged findings: 2 MAJOR non-blocking (spec holes the plan copies) and 12 MINOR (acceptance criteria that under-assert behaviour the task prose states, or small spec ambiguities). Status is `partial` only because the evidence validator dropped 3 citations (listed below).

Attribution note: this package already executed (commit 0b8a5801d, parent 0e486ab8d). At the parent, `models.py` says "exactly 43 members" and `merge_guard.py` does not exist; at HEAD it does. All citations below are to plan and spec text, not to HEAD code.

> Citation budget: full re-read. All 101 citations (40 in merged findings, 61 inferred-requirement rows) were re-read by the evidence-validator agent, which exceeds the sampling minimum (more than 20 citations would allow sampling).

## Coverage (Step 1B.0)

- Pass 1 (ID regex): 0 parsed IDs (the spec labels are FR, F, G, O). `coverage_pct` is null.
- Pass 2: 61 inferred rows. Containment matching (>= 0.6 content-word ratio against one task section): 54 matched, `coverage_pct_union` = 0.8852, `S_dev_density` = 0.1148.
- `inferred_count` 61 > `parsed_count` 0, so `coverage_degraded: parsed-sparse` and no Tier-1 stop was allowed. The run was also pinned to Tier 2 (`--tier 2`).
- Unmapped union rows (7): INF-004, INF-013, INF-018, INF-023, INF-042, INF-056, INF-057. Six are matcher noise (the behaviour is in Task 3, 6, 8 or 11 text); INF-057 (no `file:NNN` pointers) is a real constraint without an AC (finding M-011).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | engage at the first verified Medium-or-higher finding routed to a fix; default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:6 | Task 8 (0.7333) |
| INF-002 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | Task 8 (0.8889) |
| INF-003 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | Task 8 (0.7778) |
| INF-004 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none (0.5556) |
| INF-005 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger | source.md:58 | Task 8 (0.7143) |
| INF-006 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | source.md:59 | Task 9 (1.0) |
| INF-007 | PR #N is still mergeable; this run's fixes are local only. | source.md:60 | Task 9 (1.0) |
| INF-008 | Read, decide, request, `--to draft`, settle. Print the clear command once. | source.md:61 | Task 8 (0.6667) |
| INF-009 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | Task 3 (0.8571) |
| INF-010 | Release, cause `no_edits`. | source.md:63 | Task 4 (1.0) |
| INF-011 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | Task 8 (1.0) |
| INF-012 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | Task 8 (0.75) |
| INF-013 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none (0.5455) |
| INF-014 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | Task 8 (0.7143) |
| INF-015 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | Task 8 (1.0) |
| INF-016 | PR stays draft; report `held` with the clear command. | source.md:69 | Task 8 (0.8571) |
| INF-017 | No `gh` or `git` word on any line, comments included (F6). | source.md:75 | Task 3 (0.625) |
| INF-018 | `ValueError` otherwise or when `n < 1`. | source.md:101 | none (0.5) |
| INF-019 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | source.md:102 | Task 3 (0.7143) |
| INF-020 | Returns `None` when the log holds no guard record. | source.md:103 | Task 3 (0.8333) |
| INF-021 | Guard requests with no matching settle, matched by `idempotency_key` | source.md:104 | Task 3 (0.8333) |
| INF-022 | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id` | source.md:108 | Task 3 (0.7778) |
| INF-023 | a test imports both modules and asserts equality, because the core cannot import `recovery`. | source.md:109 | none (0.4545) |
| INF-024 | `mode == OFF` or `ordinal < 3` with no guard record gives `off`; no guard record gives `released` | source.md:112 | Task 3 (1.0) |
| INF-025 | if observed < guard.run_toggles: | source.md:120 | Task 4 (1.0) |
| INF-026 | if observed > guard.run_toggles + slack: | source.md:121 | Task 4 (0.75) |
| INF-027 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:127 | Task 4 (0.6) |
| INF-028 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:133 | Task 3 (1.0) |
| INF-029 | `read.state != "OPEN"` \| `HALT_PR_NOT_OPEN` | source.md:136 | Task 1 (0.75) |
| INF-030 | `guard` exists and `classify_toggles == "foreign"` \| `SKIP_USER_OVERRIDE` | source.md:141 | Task 4 (0.6) |
| INF-031 | `guard is None` and `read.is_draft` \| `SKIP_ALREADY_DRAFT` | source.md:142 | Task 3 (0.6) |
| INF-032 | `applied_edits == 0` \| `RELEASE(cause=no_edits)` | source.md:155 | Task 4 (1.0) |
| INF-033 | `push_completed` and `read.head_sha == target_sha` \| `RELEASE(cause=pushed)` | source.md:156 | Task 4 (0.7143) |
| INF-034 | `REPORT_HELD` (no mutation; prints the clear command) | source.md:164 | Task 8 (0.6) |
| INF-035 | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` | source.md:165 | Task 4 (1.0) |
| INF-036 | re-enter `release_decision` with `push_completed=True` | source.md:166 | Task 4 (1.0) |
| INF-037 | appended and fsynced BEFORE the draft/ready call | source.md:178 | Task 7 (0.6) |
| INF-038 | `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` | source.md:184 | Task 3 (0.75) |
| INF-039 | the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`) | source.md:201 | Task 3 (0.8889) |
| INF-040 | `original_is_draft` is never read from GitHub after the first record | source.md:208 | Task 3 (0.8333) |
| INF-041 | `DEFAULT_MERGE_GUARD = "draft"` | source.md:214 | Task 6 (1.0) |
| INF-042 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none (0.4286) |
| INF-043 | exit 127 when `gh` or `jq` is missing. | source.md:221 | Task 7 (1.0) |
| INF-044 | gh api --paginate "repos/${REPO}/issues/${PR}/timeline" | source.md:230 | Task 7 (0.875) |
| INF-045 | Exit codes: 0 success; 1 `gh` failure or failed verification (the JSON line is still printed with `ok:false`); 2 usage; 127 missing dependency. | source.md:234 | Task 7 (0.7059) |
| INF-046 | No new python fence | source.md:241 | Task 9 (1.0) |
| INF-047 | the enum has 43 members; update it to 45 | source.md:242 | Task 2 (1.0) |
| INF-048 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247 | Task 8 (0.8889) |
| INF-049 | The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested` | source.md:251 | Task 8 (0.8333) |
| INF-050 | needs one entry in `WRITE_VERB_CLASSIFICATION` | source.md:255 | Task 9 (1.0) |
| INF-051 | Acceptance trace (must appear in this order in the run log) | source.md:270 | Task 11 (0.8333) |
| INF-052 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed | source.md:281 | Task 8 (0.625) |
| INF-053 | the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record | source.md:301 | Task 1 (0.8571) |
| INF-054 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | Task 1 (0.8333) |
| INF-055 | Cite tests and constants by symbol name | source.md:362 | Task 1 (0.6) |
| INF-056 | Declare dependencies completely, one `Depends on:` line per dependency | source.md:363 | none (0.5) |
| INF-057 | Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | none (0.5556) |
| INF-058 | its acceptance criterion is a test that the literal line is in `SKILL.md` | source.md:374 | Task 1 (0.8571) |
| INF-059 | the crash scenario tests derive branches from a real `RunLog` | source.md:375 | Task 11 (0.7143) |
| INF-060 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | source.md:377 | Task 11 (0.7273) |
| INF-061 | the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition | source.md:378 | Task 9 (1.0) |

Postscript: all 61 rows were re-read by the evidence validator (Set C): 61 founded, 0 dropped. `coverage_pct_union`, `unmapped_requirements_union` and `S_dev_density` therefore stand unrecomputed.

## Findings (gap registry)

Severity scale: MAJOR non-blocking = a real hole an implementer would have to resolve by guessing, with a traced outcome that is fail-safe; MINOR = an acceptance criterion that under-asserts prose that states the behaviour, or a small spec ambiguity. Blocking requires a concrete wrong outcome an implementer would produce from the plan as written; none qualified.

### Finding M-001: Resume row 4 and RETRY_RELEASE re-enter release_decision, which needs target_sha and appli...

- **Severity / blocking:** MAJOR / false
- **Category:** missing-requirement
- **Sources:** V1-F2, V1-F13
- **Claim:** Resume row 4 and RETRY_RELEASE re-enter release_decision, which needs target_sha and applied_edits, but resume_decision's signature has neither and Task 4 AC does not say where they come from; outcome is fail-safe (HOLD or a completed push), so under-specified, not forced-wrong.
- **Evidence (re-read by the validator):**
  - spec source.md:107 "`release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)`"
  - spec source.md:109 "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
  - spec source.md:166 "re-enter `release_decision` with `push_completed=True`"
  - plan TASK-WF-designSpec-20261107-075614.md:77 "each re-enter `release_decision` with `push_completed=True`"

### Finding M-002: After a failed engage the fold leaves RELEASE_PENDING with owned_draft false, engage row 6...

- **Severity / blocking:** MAJOR / false
- **Category:** missing-requirement
- **Sources:** PROBE-INV-002
- **Claim:** After a failed engage the fold leaves RELEASE_PENDING with owned_draft false, engage row 6 returns HOLD(ownership_unproven) and never ENGAGE, and neither spec nor plan says what the SKILL does with HOLD at engage; a literal reading could edit on a ready PR. Spec hole the plan copies.
- **Evidence (re-read by the validator):**
  - spec source.md:138 "`HOLD(ownership_unproven)`"
  - spec source.md:199 "`phase = RELEASE_PENDING`, `failed_mutations += 1`, `owned_draft` unchanged"
  - plan TASK-WF-designSpec-20261107-075614.md:70 "`engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows"

### Finding M-003: One minted fix or ci id must be reused by the push triad and rereview_requested; the plan ...

- **Severity / blocking:** MINOR / false
- **Category:** missing-requirement
- **Sources:** V1-F1, V3-F1, V1-F9, PROBE-INV-003
- **Claim:** One minted fix or ci id must be reused by the push triad and rereview_requested; the plan states it in Task 8 prose but its AC only names the mint place, and the fold lists a cycle_id field no effect row sets. Weak AC, not a missing requirement.
- **Evidence (re-read by the validator):**
  - spec source.md:251 "uses the same id as the `cycle_id` of the push triad"
  - plan TASK-WF-designSpec-20261107-075614.md:124 "reuses it as the `cycle_id` of the push triad and of `rereview_requested`"
  - plan TASK-WF-designSpec-20261107-075614.md:127 "states the single place where the guard-enabled cycle id is minted"
  - spec source.md:190 "phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles,"

### Finding M-004: A ready not_applied may restore RELEASE_PENDING, but Task 3 AC tests only the HELD outcome...

- **Severity / blocking:** MINOR / false
- **Category:** unpassable-check
- **Sources:** V1-F3
- **Claim:** A ready not_applied may restore RELEASE_PENDING, but Task 3 AC tests only the HELD outcome, and no effect row says when phase_before_request is set; an always-HELD fold passes the AC.
- **Evidence (re-read by the validator):**
  - spec source.md:201 "the phase returns to `phase_before_request`"
  - plan TASK-WF-designSpec-20261107-075614.md:60 "a ready request followed by `not_applied` gives phase `HELD` with `unsettled == 0`"

### Finding M-005: Task 11 AC requires the twelve test names; its prose and ACs assert nothing for the releas...

- **Severity / blocking:** MINOR / false
- **Category:** unpassable-check
- **Sources:** V2-F1, PROBE-INV-005
- **Claim:** Task 11 AC requires the twelve test names; its prose and ACs assert nothing for the release-failure retry, the unreadable-timeline-never-readies case or the moved-head case, so a test with that name that asserts nothing passes.
- **Evidence (re-read by the validator):**
  - spec source.md:315 "one retry, `already_in_state` counts as confirmed, `release_pending` (FR-16)"
  - plan TASK-WF-designSpec-20261107-075614.md:166 "Cover the cases of the section 5 table"
  - plan TASK-WF-designSpec-20261107-075614.md:169 "The test file defines `test_guard_modes_ordinals_and_resume_authority`"

### Finding M-006: The fold row for a user_override skip sets no disabled_cause while guard_status reads caus...

- **Severity / blocking:** MINOR / false
- **Category:** missing-requirement
- **Sources:** PROBE-INV-001
- **Claim:** The fold row for a user_override skip sets no disabled_cause while guard_status reads cause user_override; a log built by the real fold matches no mapping row.
- **Evidence (re-read by the validator):**
  - spec source.md:206 "`settled(any, skipped, user_override)` | `phase = DISABLED`, `owned_draft = False`"
  - spec source.md:112 "phase `DISABLED` with cause `user_override` gives `user_override`"

### Finding M-007: No pure function owns the request-key a<k> count or the --read JSON to GuardRead mapping, ...

- **Severity / blocking:** MINOR / false
- **Category:** missing-requirement
- **Sources:** V1-F4, V1-F6
- **Claim:** No pure function owns the request-key a<k> count or the --read JSON to GuardRead mapping, and the script JSON to settle outcome mapping is unstated; Task 3 AC tests only suffix matching.
- **Evidence (re-read by the validator):**
  - spec source.md:184 "`idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>`"
  - spec source.md:90 "auto_merge_armed: bool; transitions: int | None; complete: bool"
  - plan TASK-WF-designSpec-20261107-075614.md:62 "with retries distinguished by the `:a<k>` suffix"

### Finding M-008: The Wave 0 row promises unsettled requests are reconciled before any edit, but resume row ...

- **Severity / blocking:** MINOR / false
- **Category:** contradiction
- **Sources:** V1-F5
- **Claim:** The Wave 0 row promises unsettled requests are reconciled before any edit, but resume row 2 returns REPORT_HELD with no mutation at ordinal below 3 or mode off, ahead of RECONCILE; the plan codifies row 2 deliberately.
- **Evidence (re-read by the validator):**
  - spec source.md:58 "unsettled requests are reconciled before any edit, release or re-trigger"
  - spec source.md:164 "`REPORT_HELD` (no mutation; prints the clear command)"
  - plan TASK-WF-designSpec-20261107-075614.md:76 "row 2 wins over row 3"

### Finding M-009: The CI-fix engage trigger has no severity: the spec lists the CI-fix cycle under the Mediu...

- **Severity / blocking:** MINOR / false
- **Category:** missing-requirement
- **Sources:** V1-F7
- **Claim:** The CI-fix engage trigger has no severity: the spec lists the CI-fix cycle under the Medium-or-higher routed-finding row, and the Wave 8 bullet engages it with kind ci; the plan copies this.
- **Evidence (re-read by the validator):**
  - spec source.md:61 "or CI-fix cycle from Wave 8"
  - spec source.md:241 "a CI-fix cycle engages with kind `ci`"
  - plan TASK-WF-designSpec-20261107-075614.md:150 "a CI-fix cycle engages with kind `ci`"

### Finding M-010: Task 7 AC lists the autoMergeRequest key but not its type; the spec example prints a boole...

- **Severity / blocking:** MINOR / false
- **Category:** unpassable-check
- **Sources:** V2-F2
- **Claim:** Task 7 AC lists the autoMergeRequest key but not its type; the spec example prints a boolean while gh returns an object or null, so a pass-through script satisfies the AC.
- **Evidence (re-read by the validator):**
  - spec source.md:230 ""autoMergeRequest":false"
  - plan TASK-WF-designSpec-20261107-075614.md:111 "`headRefOid`, `autoMergeRequest`, `transitions`, `complete`"

### Finding M-011: The constraint that protocol prose carries no file:NNN pointers is stated in the Constrain...

- **Severity / blocking:** MINOR / false
- **Category:** missing-requirement
- **Sources:** V2-F3
- **Claim:** The constraint that protocol prose carries no file:NNN pointers is stated in the Constraints block and Task 8 prose, but Task 8 ACs test only src/superclaude, fences and gh scope.
- **Evidence (re-read by the validator):**
  - plan TASK-WF-designSpec-20261107-075614.md:23 "Protocol prose carries no `file:NNN` pointers."
  - plan TASK-WF-designSpec-20261107-075614.md:128 "the ref does not contain `src/superclaude`"

### Finding M-012: Task 7 makes adding the script to _RESOLUTION_SCRIPTS conditional on reading the list's pu...

- **Severity / blocking:** MINOR / false
- **Category:** other
- **Sources:** V3-F2
- **Claim:** Task 7 makes adding the script to _RESOLUTION_SCRIPTS conditional on reading the list's purpose, while its AC states the script passes the _RESOLUTION_SCRIPTS origin-URL resolution tests.
- **Evidence (re-read by the validator):**
  - plan TASK-WF-designSpec-20261107-075614.md:108 "only after reading the purpose of that list"
  - plan TASK-WF-designSpec-20261107-075614.md:113 "the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests"

### Finding M-013: Task 9 requires the Wave 0 bullet to carry no L3 or draft condition yet to say 'at L3 with...

- **Severity / blocking:** MINOR / false
- **Category:** contradiction
- **Sources:** PROBE-INV-007
- **Claim:** Task 9 requires the Wave 0 bullet to carry no L3 or draft condition yet to say 'at L3 with --merge-guard off'; its AC fails the bullet when it names an L3 or draft condition, so literal text can fail its own test.
- **Evidence (re-read by the validator):**
  - plan TASK-WF-designSpec-20261107-075614.md:137 "carries no L3 or `draft` condition"
  - plan TASK-WF-designSpec-20261107-075614.md:140 "when it names an L3 or `draft` condition"

### Finding M-014: The spec gives the Phase members no string values, while Task 5 asserts the persisted stri...

- **Severity / blocking:** MINOR / false
- **Category:** other
- **Sources:** V1-F10
- **Claim:** The spec gives the Phase members no string values, while Task 5 asserts the persisted strings held and engage_pending.
- **Evidence (re-read by the validator):**
  - spec source.md:80 "ENGAGE_PENDING; HELD; RELEASE_PENDING; RELEASED; DISABLED"
  - plan TASK-WF-designSpec-20261107-075614.md:90 "returns `unsettled == 1` and phase `engage_pending`"

[INFERRED] Finding M-002 reads `owned_draft` as false after a failed engage; the validator confirmed spec 199 leaves `owned_draft` unchanged but "false" follows only from the absence of an earlier confirmed settle, which the spec does not show in that path.

## Evidence validation

- Set A (14 merged findings, 40 citations): 37 founded, 3 unfounded and dropped with the sub-claims they carried:
  - M-002 citation 1 (S:68): the halt row does not support a claim about the fold state or HOLD at engage.
  - M-006 citation 3 (P:61): the line says the `guard_status` test covers DISABLED plus `user_override`, so it contradicts the "tests only already_draft" sub-claim; the sub-claim was removed.
  - M-014 citation 2 (S:234): the line gives `ok:false` for any gh failure, so "timeline `ok` value is unstated" was removed; the related reviewer-1 findings F8 (unsettled check at engage) and F14 (timeline ok value) are not carried into the report.
- Set B (8 pre-check flagged reviewer-card citations, classification only): 5 founded (3 are formatting-only: backticks, capitalisation, ellipsis), 3 unfounded (reviewer-2 F1 quote spanning three lines, reviewer-2 F1 path with a doubled prefix, reviewer-2 F2 plan lines 517-518). None of these three is in this report; the merged versions use corrected lines.
- Set C (61 inferred rows): 61 founded.
- `zero-drop-flag`: false (the validator dropped items).

## Tier 2 panel

- Reviewers (class, resolved pin, served model per self-report): reviewer 1 analyzer sonnet / claude-sonnet-5-5 / claude-haiku-5-5; reviewer 2 qa haiku / claude-haiku-5-5 / gpt-6-luna; reviewer 3 refactorer opus / claude-opus-5-5 / claude-gw-tier4[1m]. The pins are the requested class rotation; the self-reports agree with the three env aliases, not with the pins, so `identity_mismatch_suspected: true` and `identity_source: requested-pinned` (no verified-independence claim).
- Blind calibration (opus class; `calibrator_diversity: degraded`, all three classes are reviewers): T1 card C = 0.68; reviewer cards 0.81, 0.79, 0.85.
- Findings: reviewer 1 filed 14 (6 blocking MAJOR), reviewer 2 filed 3, reviewer 3 filed 2. First-parse findings-block compliance 0.3333 (reviewers 2 and 3 cited brief-offset line numbers and needed one bounded re-ask; reviewer 2's re-ask left two bad citations).
- Debate (`sc-adversarial-protocol`, Mode A, depth standard; three general-purpose advocates, two rounds): Round 1 winners agreed on every point; Round 2 withdrew every blocking flag. The invariant probe returned 8 items, 2 HIGH, which blocked convergence; a resolution round with all three advocates downgraded both (no HIGH survives). Convergence 1.0, base variant reviewer 1. Judge identity is not named by the skill's return contract: `judge_identity: unknown`. Caution: the advocates ran on one model context, and unanimity followed the base advocate conceding most severities, so 1.0 is weaker evidence than it looks. The merge itself was done inline by the orchestrator, not by the merge-executor agent.
- Shadow telemetry: `panel_parity` true, `cluster_agreement` 0.3184, `calibration_coverage` 19/19, `findings_block_compliance_rate` 0.3333, `t2_floor_unmet` false.

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 101` = 0.01

## Recommendations

### Recommendation R-001: Give resume_decision the inputs its row 4 needs
- **File:** TASK-WF-designSpec-20261107-075614.md (Task 4) and source.md section 4.1
- **Change:** State where `target_sha`, `applied_edits` and `cycle_id` come from when `resume_decision` row 4 and `RETRY_RELEASE` re-enter `release_decision`, and add them to the signature or to the AC.
- **Verifier:** an AC in Task 4 that fails when row 4 is built with a hard-coded `applied_edits=0`; re-read S:107-109 and P:77.
- **Linked deviation(s):** M-001
- **Priority:** P1

### Recommendation R-002: Define what HOLD at engage does
- **File:** source.md section 3 and 4.1 (engage row 6), Task 4 AC
- **Change:** State that a `HOLD` at engage halts before any edit (like `HALT_UNAVAILABLE`), and add a test for resume after a failed engage.
- **Verifier:** a Task 4 or Task 11 test that engages after `settled(draft, failed)` and asserts no edit proceeds; re-read S:68, S:138, S:199.
- **Linked deviation(s):** M-002
- **Priority:** P1

### Recommendation R-003: Turn name-only and prose-only constraints into assertions
- **File:** TASK-WF-designSpec-20261107-075614.md (Task 11 AC at line 169, Task 8 AC at line 128, Task 7 AC at line 111)
- **Change:** Add one assertion each for the release-failure retry, the unreadable-timeline never-readies case and the moved-head case; the no-`file:NNN` constraint; the boolean type of `autoMergeRequest`.
- **Verifier:** each new AC fails against an implementation that omits the behaviour; re-read P:111, P:128, P:169.
- **Linked deviation(s):** M-005, M-010, M-011
- **Priority:** P1

### Recommendation R-004: Assert cycle-id reuse and the fold's cycle_id and disabled_cause rows
- **File:** TASK-WF-designSpec-20261107-075614.md (Task 3 AC at lines 60-61, Task 8 AC at line 127, Task 11 AC at line 170)
- **Change:** Add an AC that the push triad and `rereview_requested` carry the id the guard minted; add effect rows for `cycle_id` and for `disabled_cause = user_override`; test the ready `not_applied` case that restores `RELEASE_PENDING`.
- **Verifier:** fold tests that fail when the cause is empty after a `user_override` skip or when a ready `not_applied` always returns `HELD`; re-read S:190, S:201, S:206.
- **Linked deviation(s):** M-003, M-004, M-006
- **Priority:** P2

### Recommendation R-005: Resolve the small plan-wording conflicts
- **File:** TASK-WF-designSpec-20261107-075614.md (Task 7 lines 108 and 113, Task 9 lines 137 and 140) and source.md lines 58, 61, 164
- **Change:** Make the `_RESOLUTION_SCRIPTS` inclusion unconditional or the AC conditional; reword the Wave 0 bullet test so required "at L3" text does not trip the L3-condition check; reconcile the Wave 0 reconcile promise with resume row 2; give the CI-fix engage a stated trigger; name the owner of the request-key `a<k>` count and of the `--read` JSON mapping.
- **Verifier:** re-read P:108/113 and P:137/140 for consistency; `grep` the ref for the owner sentence.
- **Linked deviation(s):** M-007, M-008, M-009, M-012, M-013, M-014
- **Priority:** P2

## Remediation

Not requested (`--remediate` was not passed). The package already executed, so these findings describe the plan as an audit target, not open work.
