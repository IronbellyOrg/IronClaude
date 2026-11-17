```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.62
citations_total: 72
citations_revalidated: 72
citations_dropped: 0
citations_inferred: 2
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
t2_engine_requested: shadow
t2_engine_effective: shadow
```

# Reflect report: pre-execution audit of the pr-submit merge-guard plan (UC-1, Tier 2, shadow panel, model combo D)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`. Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks).

**Verdict: the plan has 1 blocking gap, 5 non-blocking MAJOR gaps and 7 MINOR gaps.** Every spec requirement span has an owning task (coverage_pct_union 0.925 by the matcher, 1.0 by reading). The defects are in what the acceptance criteria and source citations let an executor skip, not in missing tasks. The debate converged at 0.9444 (17 of 18 diff points). Calibrated confidence is low (0.62, mean of the three reviewer-card calibrations), so treat the MINOR items as leads.

## Run facts (combo D: Luna in the opus slot)

- Reviewers (served model per each card's self-report; the panel record shows the pins): reviewer 1 analyzer `claude-gw-tier1b` (Sonnet class); reviewer 2 qa `claude-haiku-5-5`; reviewer 3 refactorer `gpt-6-luna` (pinned as `claude-opus-5-5` in `panel/resolution.json`). Calibrator and orchestrator: `claude-gw-tier1b` (calibrator_diversity degraded; same class as reviewer 1). Judge: orchestrator, inline.
- Executor class unknown (no flag, env or hint). Vendor diversity: two vendors among the aliases (Anthropic and OpenAI-compatible) if the Luna self-report is right.
- This repository already holds the landed implementation of the plan. Findings rest on plan text against spec text; plan-referenced tests and constants were checked to exist.

## Inferred requirements (Pass 2)

Pass 1 found 0 requirement ids in the spec (its labels FR-n, F-n, G-n, O-n do not match the id regex), so `coverage_pct` is null and `coverage_degraded: parsed-sparse` forced Tier 2. The 40 rows below were all re-read by the evidence-validator and none was dropped. Three rows (INF-004, INF-005, INF-007) are matcher misses on short quotes: manual reading shows Task 3 and Task 4 cover them. Three matches pick a worse task than reading would (INF-037 is Task 5, INF-040 is Task 11, INF-034 spans Task 1).

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | draft not label; engage at the first verified Medium-or-higher finding routed to a fix; default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:6-6 | containment -> Task 8 (0.69) |
| INF-002 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6-6 | containment -> Task 8 (0.90) |
| INF-003 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6-6 | containment -> Task 8 (0.78) |
| INF-004 | No `gh` or `git` word on any line, comments included (F6). | source.md:75-75 | none (best T3 0.57) |
| INF-005 | `ValueError` otherwise or when `n < 1` | source.md:101-101 | none (best T3 0.50) |
| INF-006 | phase `DISABLED` with cause `already_draft` gives `off` | source.md:112-112 | containment -> Task 3 (1.00) |
| INF-007 | the only foreign-toggle test; no actor identity, F11 | source.md:114-114 | none (best T8 0.57) |
| INF-008 | `engage_decision`, first matching row wins | source.md:129-129 | containment -> Task 4 (0.80) |
| INF-009 | `release_decision`, first matching row wins | source.md:145-145 | containment -> Task 4 (0.80) |
| INF-010 | `resume_decision`, first matching row wins | source.md:159-159 | containment -> Task 4 (0.80) |
| INF-011 | update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117` | source.md:175-175 | containment -> Task 2 (0.70) |
| INF-012 | `run_log.rebuild_state()` stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`) | source.md:187-187 | containment -> Task 5 (0.78) |
| INF-013 | the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`) | source.md:201-201 | containment -> Task 3 (0.89) |
| INF-014 | `--merge-guard` with `dest="merge_guard"`, `choices=["draft", "off"]` | source.md:214-214 | containment -> Task 6 (1.00) |
| INF-015 | `off` makes the skill print one line: "Remediation is unprotected: --merge-guard off." | source.md:216-216 | containment -> Task 9 (0.90) |
| INF-016 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing | source.md:221-221 | containment -> Task 7 (0.88) |
| INF-017 | A verification mismatch after a mutation is `ok:false, error:"verify_failed"` | source.md:234-234 | containment -> Task 7 (0.88) |
| INF-018 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240-240 | containment -> Task 8 (0.75) |
| INF-019 | The Wave 0 bullet applies at every ordinal and in both modes | source.md:241-241 | containment -> Task 9 (1.00) |
| INF-020 | which also carries the literal L2 line | source.md:241-241 | containment -> Task 8 (1.00) |
| INF-021 | update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | source.md:242-242 | containment -> Task 2 (1.00) |
| INF-022 | the guard phases are fold values, not `MonitorState` members | source.md:243-243 | containment -> Task 10 (0.83) |
| INF-023 | `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling" | source.md:244-244 | containment -> Task 12 (1.00) |
| INF-024 | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | source.md:245-245 | containment -> Task 13 (0.78) |
| INF-025 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247-247 | containment -> Task 8 (0.89) |
| INF-026 | The build must first confirm where the SKILL assigns a fix cycle's id today and keep exactly one source for it (open item O1). | source.md:251-251 | containment -> Task 1 (0.71) |
| INF-027 | needs one entry in `WRITE_VERB_CLASSIFICATION` | source.md:255-255 | containment -> Task 9 (1.00) |
| INF-028 | Acceptance trace (must appear in this order in the run log) | source.md:270-270 | containment -> Task 11 (0.83) |
| INF-029 | the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record | source.md:301-301 | containment -> Task 1 (0.86) |
| INF-030 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | source.md:301-301 | containment -> Task 8 (0.92) |
| INF-031 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326-326 | containment -> Task 1 (0.83) |
| INF-032 | the script test for a missing `jq` (exit 127) | source.md:322-322 | containment -> Task 7 (1.00) |
| INF-033 | the `landed`, `not_landed` and `ambiguous` branches produced by the real `detect_crash_window` and `resolve_crash_window` over a real `RunLog` (never injected strings) | source.md:318-318 | containment -> Task 11 (0.85) |
| INF-034 | Cite tests and constants by symbol name | source.md:362-362 | containment -> Task 1 (0.60) |
| INF-035 | The L2 line is written into the SKILL.md output table | source.md:374-374 | containment -> Task 9 (1.00) |
| INF-036 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | source.md:377-377 | containment -> Task 11 (0.73) |
| INF-037 | `merge_guard.py` into the zero-token file set | source.md:299-299 | containment -> Task 8 (0.83) |
| INF-038 | export the public guard names | source.md:291-291 | containment -> Task 5 (1.00) |
| INF-039 | `tests/cli/test_verify_sync_hooks.py` runs `make verify-sync` inside the full suite | source.md:301-301 | containment -> Task 13 (0.91) |
| INF-040 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:281-281 | containment -> Task 8 (0.75) |

- `coverage_pct_union`: 0.925 (37 of 40). `unmapped_requirements_union`: INF-004, INF-005, INF-007 (matcher misses). `S_dev_density` (union): 0.075.

## Gaps found (merged verdict)

Each block cites plan lines (`TASK-WF-designSpec-20261107-075614.md`) and spec lines (`source.md`). Source cards: R1 = reviewer 1, R2 = reviewer 2, R3 = reviewer 3, FF = invariant-probe fault-finder.

### Gap G1 (MAJOR, BLOCKING): Task 8 drops spec section 4.2 from the protocol ref

- **Location:** plan 124, 126-130; spec 182-185, 240. Sources: R1-F1, R3-F1.
- **Evidence:** plan 124 builds `refs/merge-guard.md` "from ./source.md sections 3, 4.1, 4.5, 4.6 and 5". The spec's own file table says the ref carries "The procedure of sections 3 and 4.1 to 4.4" (source 240). Section 4.2 holds the only definition of the event fields (`timeline_baseline` and `original_is_draft` on the first request only, the `idempotency_key` and its `k`). No Task 8 criterion names an event field.
- **Classification:** missing requirement, plan departs from the spec's file table. R1 first rated it non-blocking (Task 3 builds the fold from 4.2); after the verified source 240 line all three advocates agreed it is blocking, narrowly: 4.3 and 4.4 are recoverable from Tasks 6 and 7, the 4.2 protocol wording is not.
- **Remediation:** see R-001.

### Gap G2 (MAJOR): Task 4's ok-case test omits the `unsettled` slack term

- **Location:** plan 70, 74; spec 119-120. Source: R1-F2.
- **Evidence:** plan 70 states the slack as `run_toggles + unsettled + failed_mutations`; plan 74 tests `ok` only when observed equals `run_toggles + failed_mutations`. An implementation that drops `unsettled` passes every listed criterion and would read a landed but unsettled request as foreign.

### Gap G3 (MAJOR): no rule or test for how the fold's `cycle_id` advances

- **Location:** spec 108, 187-193; plan 56-62. Sources: R1-F3, FF INV-003.
- **Evidence:** `held_cycle_published` compares a `push_completed` with `guard.cycle_id`; the fold table lists the field with no update rule and no Task 3 criterion covers a second cycle. If the first request's id is kept, a crash after a normal push of cycle 2 leaves the PR draft.

### Gap G4 (MAJOR): Task 9's Wave 0 wording is internally in tension

- **Location:** plan 137, 140; spec 241. Sources: R2-F1, R3-F2, FF INV-001.
- **Evidence:** the bullet must carry "no L3 or `draft` condition" yet say what happens "at L3 with `--merge-guard off`" and "no draft call is made"; the criterion fails the bullet when it "names an L3 or `draft` condition". Plan 137 narrows the test to "`L3 only` or `draft` gate wording", and the spec has the same sentence, so an executor can resolve it. R2 and R3 first called it blocking and both conceded non-blocking in Round 2. Kept so the wording is fixed.

### Gap G5 (MINOR): cycle-id equality is never asserted

- **Location:** spec 251; plan 170-171. Sources: R2-F2, R3-F4. Spec 4.6 requires the minted id to be the `cycle_id` of the push triad and of `rereview_requested`; Task 11 asserts event order only.

### Gap G6 (MINOR): "byte-identical" pins are compared with start text only

- **Location:** plan 154, 33. Source: R2-F4. A prefix constant does not prove the whole sentence is unchanged.

### Gap G7 (MINOR): the Medium-or-higher trigger is phrase-tested only

- **Location:** plan 152-153. Source: R2-F3. The phrases must be present, but nothing checks they gate the engage sentence.

### Gap G8 (MINOR): Phase string values are unpinned in Task 3 but asserted in Task 5

- **Location:** plan 90; spec 80. Source: R1-F4.

### Gap G9 (MINOR): `autoMergeRequest` boolean conversion is untested

- **Location:** plan 111; spec 230. Source: R2-F5.

### Gap G10 (MINOR): classification steps name `gh pr` and `gh api` but not git write verbs

- **Location:** plan 22, 124; spec 255. Source: R2-F6.

### Gap G11 (MINOR): Tasks 9 and 12 read the pre-build record without a Task 1 dependency line

- **Location:** plan 134-137, 179-182; spec 363. Source: R3-F3 (citation corrected during the debate; the original cited plan lines that do not exist). Task 1 is reached through Task 8, so this is a style defect.

### Gap G12 (MAJOR) [INFERRED]: resume release inputs have no derivation

- **Location:** spec 107, 166; plan 77, 124. Source: FF INV-004, INV-005 (not from a reviewer card). `release_decision` also needs `target_sha` and this cycle's `applied_edits`; no task says they come from the `push_initiated` and `fix_applied` events of the guard's cycle. A wrong `applied_edits=0` would release as `no_edits`.

### Gap G13 (MAJOR) [INFERRED]: Task 7's fake `gh` may be too weak for Task 11

- **Location:** plan 108, 111-112, 166. Source: FF INV-006. The validator noted the claim is slightly strong because Task 7's criteria already use scripted output; the open part is state across calls.

## Dropped or withdrawn

- R2-F7 (fold rows without a named case): withdrawn by its own advocate; plan 60 says the test "covers every row of the section 4.2 effect table".
- R3-F3's original citations (plan 363-365 and a malformed nested path): replaced by G11. The calibrator found both defects before the debate.
- Invariant probe INV-007 to INV-010 (LOW) stay in `adversarial/adversarial/invariant-probe.md`.

## Recommendations

### Recommendation R-001: Restore spec sections 4.2 to 4.4 in Task 8
- **File:** `TASK-WF-designSpec-20261107-075614.md` (Task 8 paragraph and acceptance criteria)
- **Change:** build the ref from "sections 3 and 4.1 to 4.4, 4.5, 4.6 and 5" and add a criterion that the ref names the `draft_guard_requested` and `draft_guard_settled` fields, the first-request-only `timeline_baseline` and `original_is_draft`, and the `idempotency_key` with its `k` rule; extend the protocol test to assert them.
- **Verifier:** `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q` fails when a named field is removed from the ref.
- **Linked deviation(s):** G1, G12
- **Priority:** P0

### Recommendation R-002: Add the missing criteria to Tasks 3 and 4
- **File:** `TASK-WF-designSpec-20261107-075614.md` (Tasks 3, 4, 5)
- **Change:** add a Task 4 case with `unsettled > 0` that must classify `ok`; add a Task 3 second-cycle case (`fix-1` released, `fix-2` requested) that asserts `cycle_id` advances and `held_cycle_published` is true for `fix-2`; state the `Phase` string values in Task 3.
- **Verifier:** those tests fail on an implementation that drops `unsettled` or keeps the first cycle id.
- **Linked deviation(s):** G2, G3, G8
- **Priority:** P1

### Recommendation R-003: Resolve the Task 9 wording and add the equality and derivation criteria
- **File:** `TASK-WF-designSpec-20261107-075614.md` (Tasks 7, 9, 10, 11)
- **Change:** word the Task 9 test rule once ("no gating clause on L3 or `draft` for the resume load; the off line may mention L3"); assert in Task 11 that the guard, `push_initiated`, `push_completed` and `rereview_requested` events carry the same `cycle_id`; say in Task 8 that `target_sha` and the cycle's `applied_edits` come from the cycle's events; require a scriptable fake `gh` in Task 7.
- **Verifier:** Task 11's trace test asserts equal `cycle_id` values; the Task 9 test passes on the real bullet and fails on a gated one.
- **Linked deviation(s):** G4, G5, G12, G13
- **Priority:** P1

### Recommendation R-004: Tidy the MINOR items
- **File:** `TASK-WF-designSpec-20261107-075614.md`
- **Change:** record whole-sentence constants for the two pinned sentences (G6), an autoMergeRequest boolean case (G9), git write verbs in the classification steps (G10), and Task 1 in the Depends on lines of Tasks 9, 10 and 12 (G11).
- **Verifier:** re-run `/sc:reflect --mode pre` on the revised plan; G6 to G11 do not recur.
- **Linked deviation(s):** G6, G7, G9, G10, G11
- **Priority:** P2

## Inferred-claim audit

- `citations_inferred: 2` (G12, G13)
- Inferred-fraction: `2 / 72` = 0.03

## Caveats

- The adversarial scoring was compact (no reverse-order pass, 30 criteria scored at dimension level) and the merge was inline; `adversarial/adversarial/return-contract.yaml` says `status: partial`, `fallback_mode: true`. `merge_method: adversarial` holds because the merged verdict comes from a real three-advocate, two-round debate.
- The invariant probe returned one HIGH row (INV-001); the orchestrator adjudicated it ADDRESSED with evidence, shown in `invariant-probe.md`. A reader who disagrees should treat G4 as blocking.
- The validator dropped 0 of 72 citations (32 finding citations, 40 inferred rows). A zero-drop pass is a flag, not a clean signal: the merged set was already corrected after two calibrators found bad citations on card 3 and two off-by-one ranges on card 2.
- The verify-citations pre-check flagged 40 of 40 citations as unresolved because the input snapshot stores bare file names; that is a snapshot-path artifact, not a citation failure.
- Identity: pins are recorded, served models come from reviewer self-reports only (`identity_source: requested-pinned`).
