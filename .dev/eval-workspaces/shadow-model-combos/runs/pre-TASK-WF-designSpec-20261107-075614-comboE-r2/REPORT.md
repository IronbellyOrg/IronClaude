```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.59      # mean of the three blind card calibrations (0.60, 0.57, 0.60); the Tier 1 card scored 0.53
citations_total: 64              # 31 in merged findings + 33 in the three reviewer cards
citations_revalidated: 64
citations_dropped: 0
citations_inferred: 2            # see the Inferred-claim audit footer
citation_budget_policy: full_reread   # stricter than the >20 sampling rule: the validator re-read all 64
coverage_degraded: parsed-sparse
```

# Reflection report (UC-1 pre): plan `TASK-WF-designSpec-20261107-075614` vs its design spec

Run `pre-TASK-WF-designSpec-20261107-075614-comboE-r2`, Tier 2 pinned, engine `shadow`. Plan: 13 tasks. Spec: the pr-submit merge guard design (issue #375). Paths below are repo-relative under `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`.

## Verdict
No blocking finding. 11 merged findings: 1 MAJOR and 10 MINOR, all non-blocking. The plan covers every file and behavior the spec lists; the weak spots are checks that cannot fail and one dropped spec section. Convergence 0.8261 (threshold 0.80). This package already executed (commit 0b8a5801d, parent 0e486ab8d), so the findings describe plan quality; no remediation was requested (`--remediate` absent).

## Attribution (read first)
The spec facts hold at the parent commit 0e486ab8d (EventType has 43 members, no import cycle through `conflicts.py` and `fsm.py`, the `BRANCH_*` constants and the needed event types exist). HEAD now carries the implementation. Every finding below is a plan-text or spec-text finding checked against the plan and spec files, not against HEAD code.

## Coverage (Step 1B.0)
- Pass 1 (ID regex): 0 parsed IDs in spec and plan. Pass 2: 48 inferred rows, every quote verbatim at its cited spec line (re-verified at Wave 5: 0 mismatches).
- `coverage_pct` null (no parsed rows); `coverage_pct_union` 0.875 (42 of 48 matched by containment).
- `inferred_count` 48 > `parsed_count` 0, so `coverage_degraded: parsed-sparse`: no Tier-1 stop, routed to Tier 2 (also pinned by `--tier 2`).
- 6 rows unmatched: INF-007, INF-012, INF-015, INF-026, INF-029, INF-046. Five are matcher noise (a task states or tests the item in other words); INF-046 (cite tests by symbol name) is a constraint with no AC (finding M9 family).

## Merged findings
All citations re-read by the evidence validator (30 of 31 FOUNDED, 1 PARTIAL, 0 UNFOUNDED). Plan = P, spec = S.

### M1 (MAJOR, non-blocking): Task 8 drops the spec sections that define the event record
Task 8 builds the ref from spec "sections 3, 4.1, 4.5, 4.6 and 5" (P:124). Spec 4.5 says the ref is "the procedure of sections 3 and 4.1 to 4.4" (S:240). The request event's fields and the `idempotency_key` format `guard:<run_id>:<cycle_id>:<to>:a<k>` are in 4.2 (S:184), and none of Task 8's ACs checks that the ref states them (P:127-130). Sources: reviewer 1 F4 plus an orchestrator finding made during adjudication (not debated). Why not blocking: an executor reading the whole spec still sees 4.2, and the failure mode is degraded crash recovery that holds the PR draft and reports.

### M2 (MINOR): no owner for the read-to-decision mapping
`GuardRead` is "parsed output of `--read`" (S:88-90) but no task maps the script's `isDraft`, `headRefOid`, `autoMergeRequest` to `is_draft`, `head_sha`, `auto_merge_armed` (P:56). Task 7's AC lists the keys, not their types (P:111), while the spec example shows a boolean (S:230). [INFERRED] `gh pr view --json autoMergeRequest` returns an object or null, so a pass-through would fail the type.

### M3 (MINOR): resume row 4 release inputs
Row 4 re-enters `release_decision` (S:166) but `resume_decision` has no `target_sha`, `applied_edits` or `cycle_id` (S:109); Task 4's AC tests the row without naming their source (P:77). Both entries already have a completed push, so the open risk is the head check.

### M4 (MINOR): cycle-id reuse has no AC
Task 8 prose reuses the minted id for the push triad and `rereview_requested` (P:124); its AC only requires the ref to state the minting place (P:127); spec 4.6 requires the same id (S:251). A mismatch would make `held_cycle_published` miss a normal push after a crash.

### M5 (MINOR): fsync-before-call order unobservable
Spec: appended and fsynced before the call (S:178). Task 8 states it in prose (P:124); no AC or scenario test can observe the order (P:128).

### M6 (MINOR): Task 11 checks test names
Task 11's first AC requires only that twelve test names exist (P:166-173); the prose omits the release-failure retry, the unreadable-timeline case and the moved-head case that spec section 7 names (S:305-320). The crash, trace and forbidden-call ACs (P:171-172) are real behavior checks, so this is a partial gap.

### M7 (MINOR): pin constants are start text only
Task 1 records the literal start text of the S5a and pre-push sentences (P:33-38); Task 10 calls the check byte-identical (P:154). A prefix constant cannot detect an edit inside the sentence. [INFERRED] the existing pins (P:21) cover most wording; the cited line shows only that pinned sentences exist. Reviewer 3 labeled this blocking; adjudicated down.

### M8 (MINOR): `_RESOLUTION_SCRIPTS` step is conditional, its AC is not
Task 7 adds the script to the list only after reading its purpose (P:108); its AC says the script passes that list's tests (P:113-114). Reviewers 2 and 3.

### M9 (MINOR): no AC for "no file:NNN pointers"
Constraint at P:23 and S:369; Task 8's AC tests `src/superclaude`, fences and gh scope only (P:128). Reviewer 2.

### M10 (MINOR): Wave 0 bullet wording vs test scope
The Task 9 bullet must print the L3/off line yet carry no L3 condition; the AC fails a bullet that "names an L3 or draft condition" (P:137-141, S:241). Reviewer 2. The narrower "L3 only" wording in the Task 9 prose reduces the ambiguity.

### M11 (MINOR): `next_cycle_number` AC cannot tell count from highest
The AC uses `fix-1` and `fix-2` only (P:59); the spec rule is the highest number plus one (S:102). Reviewer 1.

Dropped before the report: reviewer 1 F8 (a `guard is None` crash is caught by the Task 4 per-row AC, P:73; its author conceded) and F9 (a runtime "prints once" property).

## Inferred requirements (Pass 2)
| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | engage at the first verified Medium-or-higher finding routed to a fix; default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:source.md:6 | Task 8 (0.7333) |
| INF-002 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | source.md:source.md:59 | Task 9 (1.0) |
| INF-003 | PR #N is still mergeable; this run's fixes are local only. | source.md:source.md:60 | Task 9 (1.0) |
| INF-004 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:source.md:64 | Task 8 (1.0) |
| INF-005 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:source.md:66 | Task 3 (0.6) |
| INF-006 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:source.md:67 | Task 8 (0.7143) |
| INF-007 | No `gh` or `git` word on any line, comments included (F6). | source.md:source.md:75 | none (0.5714) |
| INF-008 | `"fix-<n>"` for kind `fix`, `"ci-<n>"` for kind `ci`; `ValueError` otherwise or when `n < 1`. | source.md:source.md:101 | Task 3 (0.875) |
| INF-009 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | source.md:source.md:102 | Task 3 (0.6667) |
| INF-010 | `applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_edits` output field | source.md:source.md:107 | Task 4 (1.0) |
| INF-011 | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id` | source.md:source.md:108 | Task 3 (0.8182) |
| INF-012 | a test imports both modules and asserts equality, because the core cannot import `recovery` | source.md:source.md:109 | none (0.4) |
| INF-013 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:source.md:127 | Task 4 (0.6) |
| INF-014 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:source.md:133 | Task 3 (1.0) |
| INF-015 | `HALT_UNAVAILABLE(read_failed)` | source.md:source.md:135 | none (0.0) |
| INF-016 | `guard is None` and `read.is_draft` | source.md:source.md:142 | Task 3 (0.75) |
| INF-017 | `push_completed` and `read.head_sha == target_sha` | source.md:source.md:156 | Task 4 (0.75) |
| INF-018 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | source.md:source.md:164 | Task 3 (1.0) |
| INF-019 | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` | source.md:source.md:165 | Task 4 (1.0) |
| INF-020 | re-enter `release_decision` with `push_completed=True` | source.md:source.md:166 | Task 4 (1.0) |
| INF-021 | Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`): | source.md:source.md:175 | Task 2 (0.8235) |
| INF-022 | appended and fsynced BEFORE the draft/ready call | source.md:source.md:178 | Task 7 (0.6) |
| INF-023 | stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`) | source.md:source.md:187 | Task 5 (0.7143) |
| INF-024 | the pending key is cleared and the phase returns to `phase_before_request`; `owned_draft` and the toggle counters are unchanged. | source.md:source.md:201 | Task 3 (0.9) |
| INF-025 | `build_arg_parser` adds `--merge-guard` with `dest="merge_guard"`, `choices=["draft", "off"]` | source.md:source.md:214 | Task 6 (0.8889) |
| INF-026 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:source.md:217 | none (0.4286) |
| INF-027 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing. | source.md:source.md:221 | Task 7 (0.875) |
| INF-028 | gh api --paginate "repos/${REPO}/issues/${PR}/timeline" | source.md:source.md:230 | Task 7 (0.875) |
| INF-029 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:source.md:234 | none (0.5) |
| INF-030 | A verification mismatch after a mutation is `ok:false, error:"verify_failed"`, and the SKILL settles it `failed`. | source.md:source.md:234 | Task 7 (0.6) |
| INF-031 | The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `draft` condition | source.md:source.md:241 | Task 9 (1.0) |
| INF-032 | it must not contain the words `evidence-validator` or `conflict-intent.md` | source.md:source.md:241 | Task 9 (0.8571) |
| INF-033 | Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git` | source.md:source.md:242 | Task 2 (1.0) |
| INF-034 | `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling". | source.md:source.md:244 | Task 12 (1.0) |
| INF-035 | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | source.md:source.md:245 | Task 13 (0.7778) |
| INF-036 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:source.md:247 | Task 8 (0.9) |
| INF-037 | The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested` | source.md:source.md:251 | Task 8 (0.9091) |
| INF-038 | Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb is a hit of `WRITE_VERB_RE` and needs one entry in `WRITE_VERB_CLASSIFICATION` | source.md:source.md:255 | Task 8 (0.75) |
| INF-039 | Acceptance trace (must appear in this order in the run log): `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested`. | source.md:source.md:270 | Task 11 (0.9412) |
| INF-040 | `terminal_halted(draft_guard_unavailable)`, no edit. Message names `--merge-guard off` and prints the clear command. | source.md:source.md:274 | Task 8 (0.9091) |
| INF-041 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:source.md:281 | Task 8 (0.75) |
| INF-042 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | source.md:source.md:301 | Task 8 (0.9286) |
| INF-043 | the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record. | source.md:source.md:301 | Task 1 (0.8571) |
| INF-044 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:source.md:326 | Task 1 (0.8462) |
| INF-045 | The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. | source.md:source.md:326 | Task 1 (1.0) |
| INF-046 | Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test that asserts the event count), never by bare line number | source.md:source.md:362 | none (0.5625) |
| INF-047 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | source.md:source.md:377 | Task 11 (0.7) |
| INF-048 | "no push after a `pr_not_open` halt" is asserted on `RunLog.read_events()` | source.md:source.md:377 | Task 11 (0.8333) |

Postscript: no inferred row was dropped (0 of 48; quote check re-run at Wave 5).

## Tier 2 panel record
| Reviewer | Persona | Pinned (panel resolution) | Env alias used by the class | Self-report | Calibrated C | Findings |
|---|---|---|---|---|---|---|
| 1 | analyzer | claude-sonnet-5-5 (sonnet) | claude-haiku-5-5 | claude-haiku-5-5 | 0.60 | 9 (5 MAJOR blocking as filed) |
| 2 | qa | claude-haiku-5-5 (haiku) | gpt-6-luna | gpt-6-luna | 0.57 | 4 MINOR |
| 3 | refactorer | claude-opus-5-5 (opus) | claude-gw-tier4[1m] | claude-gw-tier4[1m] | 0.60 | 2 (1 MAJOR blocking as filed) |

- Three distinct alias values resolved, so three reviewers ran (no collapse to two). Each card's self-report matches the alias its class maps to, and differs from the panel pin on all three cards: `identity_mismatch_suspected: true`, `identity_source: requested-pinned`. No claim of verified independence. The panel resolution records the class rotation, not the served model.
- Calibrator: `confidence-calibrator`, sonnet class (alias claude-haiku-5-5), the same alias as reviewer 1's class: `calibrator_diversity: degraded` (reviewers used every class).
- Executor class unresolved (`executor_class_source: unknown`): the anti-self-confirmation guarantee is weakened.
- Judge: the debate scoring was done by the orchestrator (model claude-gw-tier1b[1m]); the sc-adversarial return contract names no judge, so `judge_identity: unknown`, `judge_class_collision: unknown`.
- Panel parity true (resolution classes sonnet, haiku, opus equal the rotation that ran). `cluster_agreement` 0.3013 (telemetry only). `findings_block_compliance_rate` 0.6667 (reviewer 2 needed one bounded re-ask for citation line numbers it had counted inside its brief; the other two cards were valid first time). Calibration coverage 15/15. Pre-check flagged 4 of 33 citations (quote with markup characters); the validator cleared all four.
- Blocking as filed: 6 findings (5 from reviewer 1, 1 from reviewer 3). After the debate and the judge's severity review: 0.

## Protocol deviations (recorded, not hidden)
1. Diff analysis, invariant probe, scoring and merge were written by the orchestrator; no analytical agent, fault-finder, merge-executor or position-bias second pass ran.
2. Round 2 was one parallel round (advocates resumed) reading an orchestrator digest of Round 1.
3. Base selection used the card calibration C as its qualitative layer.
4. The Wave 5 validator re-read all 64 citations although the sampling rule would allow sampling above 20.
5. Reviewer 2's card was re-asked once for citation line numbers (first reply kept at `artifacts/reviewer-2-card-first-reply.md`).
6. Review snapshot isolation (`--isolate-reviewers`) was off; reviewers read the live tree, which is why the briefs carry the attribution note.

## Recommendations
These apply to the plan pattern (future `/sc:workflow` plans); this package already executed.
- R-1: in Task 8 style plans, name every spec section the spec assigns to the file (here 4.2 to 4.4) and add an AC that greps the file for the event field names and the `guard:` key format. Verifier: the new grep assertion fails on a ref without them.
- R-2: assign the `--read` JSON to `GuardRead` mapping to a task (or a parse function with a test using the script's real output, including the `autoMergeRequest` boolean). Verifier: a test feeding the fake-`gh` output through the mapping.
- R-3: replace names-only ACs (Task 11) with one assertion per named behavior, and add a sparse-log case (`fix-5` only) to the `next_cycle_number` AC. Verifier: stub bodies fail.
- R-4: either record the whole pinned sentences in Task 1 or reword the Task 10 AC to "starts with"; make the `_RESOLUTION_SCRIPTS` AC conditional like its step.

## Inferred-claim audit
`citations_inferred: 2` of 64 (the `gh` return-type clause in M2 and the existing-pins clause in M7). No WARN: well under half.

Validator note: ZERO_DROP_SUSPECT. The pass dropped nothing; it downgraded 5 citations to PARTIAL (M7's P:21, R1-F7's S:230, R1-F8's S:134-137, R2-F1's P:166-173, R2-F3's S:339-341) and ran a counter-evidence check on every kept finding. `zero-drop-flag: true` is recorded in the audit log for meta-eval.
