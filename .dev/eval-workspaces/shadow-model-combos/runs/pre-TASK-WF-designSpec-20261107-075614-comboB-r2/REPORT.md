# Reflect report (UC-1, pre-execution): pr-submit merge guard plan vs its design spec

Run: pre-TASK-WF-designSpec-20261107-075614-comboB-r2 (tier 2 pinned, engine shadow). Spec: source.md (378 lines). Plan: TASK-WF-designSpec-20261107-075614.md (13 tasks).

```yaml
contract_version: 1.8.0
status: partial          # 1 citation dropped by the final gate; adversarial convergence blocked by 2 HIGH invariants
mode: pre
tier_reached: 2
confidence_calibrated: 0.78   # mean of the three blind per-card calibrations (0.73, 0.81, 0.79); T1 card calibrated 0.85
citations_total: 109
citations_revalidated: 90
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 90` — 24 merged-finding citations re-Read by the evidence-validator (all citations of the three blocking findings, all repo-file citations, one in three of the rest) plus all 66 inferred-requirement quotes matched verbatim by script.
> - `citations_dropped: 1` — the sample count. It forces `status: partial`.
> - `citations_dropped_extrapolated: 1` — round(1 x 109 / 90). Recording only.
>
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.


## Verdict

**Not ready as written.** Three blocking findings (F1, F2, F3), two MAJOR non-blocking findings (F4, F5) and seven MINOR findings (F6 to F12) survived a three-reviewer debate (two rounds plus an invariant probe). The plan covers the spec well; every defect is a contradiction or gap inside an acceptance criterion or a decision contract, not a missing deliverable. Counts: 3 blocking, 5 MAJOR, 7 MINOR. Convergence on the debate points was 13 of 13, but the invariant gate blocked it (2 HIGH unaddressed sufficiency items that say the agreed fixes for F1 and F2 are not enough alone), so the run ends `partial`.

## Findings

### F1 (MAJOR, BLOCKING, unpassable-check): Task 7 asks a static scan to pass only gh lines with --repo or repos/, but the _RESOLUTION_SCRIPTS tests need the unscoped 'gh repo view --json nameWithOwner' fallback; the fix must reuse _repo_scoped, _command_lines and _GH_CMD and relax the runtime-log clause.

- **Evidence:** TASK-WF-designSpec-20261107-075614.md:108-113, test_static_grep.py:545-550, test_static_grep.py:107-132, source.md:377
- **Provenance:** origin: spec (source.md:377) copied into plan; raised by all 3 reviewers; probe INV-001
- **Tag:** Grounded (citations re-Read by the final gate)

### F2 (MAJOR, BLOCKING, contradiction): resume_decision row 4 re-enters release_decision but has no cycle_id, applied_edits or target_sha and GuardAction has no re-enter value; the Task 4 row-4 criterion cannot be written and could release without a head proof.

- **Evidence:** source.md:107-109, source.md:166, TASK-WF-designSpec-20261107-075614.md:70, TASK-WF-designSpec-20261107-075614.md:77
- **Provenance:** origin: spec 4.1 signature, adopted by plan Task 4; raised by all 3 reviewers; probe INV-002 says the added arguments alone are not enough
- **Tag:** Grounded (citations re-Read by the final gate)

### F3 (MAJOR, BLOCKING, safety): No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.

- **Evidence:** source.md:108, source.md:139, source.md:166, source.md:190-206, TASK-WF-designSpec-20261107-075614.md:62, TASK-WF-designSpec-20261107-075614.md:77
- **Provenance:** origin: spec 4.2 fold table; raised by reviewer 3, verified by both other advocates in Round 2; probe INV-002
- **Tag:** Grounded (citations re-Read by the final gate)

### F4 (MAJOR, non-blocking, missing-requirement): A draft_guard_unavailable halt from a failed read or timeline at engage writes no guard record, so guard_status reports released; no task owns or tests the spec's unavailable override.

- **Evidence:** source.md:112, source.md:68, TASK-WF-designSpec-20261107-075614.md:61, TASK-WF-designSpec-20261107-075614.md:124-129
- **Provenance:** origin: spec 4.1 (guard_status) plus plan Task 3 criterion; raised by all 3 reviewers
- **Tag:** Grounded (citations re-Read by the final gate)

### F5 (MAJOR, non-blocking, missing-requirement): No criterion tests the guard-event producer payload (key format, :a<k> retry suffix, first-request-only fields); matcher fixtures and event-order checks pass with a wrong producer. Add spec 4.2 to Task 8's sources.

- **Evidence:** source.md:184-185, TASK-WF-designSpec-20261107-075614.md:62, TASK-WF-designSpec-20261107-075614.md:124, TASK-WF-designSpec-20261107-075614.md:168-172
- **Provenance:** origin: plan (Task 3, 8, 11 criteria); raised by reviewer 2, verified by reviewer 3
- **Tag:** Grounded (citations re-Read by the final gate)

### F6 (MINOR, non-blocking, missing-requirement): The fold row for settled(any, skipped, user_override) does not set disabled_cause, yet guard_status keys on it; Task 3 tests only already_draft. Add a settle, fold and status test.

- **Evidence:** source.md:112, source.md:206, TASK-WF-designSpec-20261107-075614.md:60-61
- **Provenance:** origin: spec fold table; raised by all 3 reviewers
- **Tag:** Grounded (citations re-Read by the final gate)

### F7 (MINOR, non-blocking, other): Task 1 records the baseline before make sync-dev and Task 13 subtracts it, so a feature-caused mirror failure that is also in a stale baseline is hidden; the two separate sync tests narrow but do not close this.

- **Evidence:** TASK-WF-designSpec-20261107-075614.md:33, TASK-WF-designSpec-20261107-075614.md:199
- **Provenance:** origin: plan Task 1 and Task 13; raised by reviewers 1 and 3, conceded by reviewer 2
- **Tag:** Grounded (citations re-Read by the final gate)

### F8 (MINOR, non-blocking, missing-requirement): No task owns the mapping from the script JSON keys (isDraft, headRefOid, autoMergeRequest) to the GuardRead fields (is_draft, head_sha, auto_merge_armed), and SKILL.md may carry no new python fence.

- **Evidence:** source.md:88-91, source.md:230, TASK-WF-designSpec-20261107-075614.md:124, TASK-WF-designSpec-20261107-075614.md:143
- **Provenance:** origin: spec 4.1 and 4.4; raised by reviewers 1 and 3, conceded by reviewer 2
- **Tag:** Grounded (citations re-Read by the final gate)

### F9 (MINOR, non-blocking, contradiction): The Wave 0 bullet must name the L3 and --merge-guard off case, yet its test must fail on L3 or draft gate wording; the test must target the gate wording of the print rule, not the words themselves.

- **Evidence:** TASK-WF-designSpec-20261107-075614.md:137, TASK-WF-designSpec-20261107-075614.md:140, source.md:241
- **Provenance:** origin: spec 4.5 and plan Task 9; raised by reviewers 1 and 3 (reviewer 3 withdrew a MAJOR rating)
- **Tag:** Grounded (citations re-Read by the final gate)

### F10 (MINOR, non-blocking, other): Resume row 3 leaves the order of its three reasons open: a live state that mismatches the request settles not_applied without proof that no toggle landed, although the foreign-toggle slack allows one unsettled transition.

- **Evidence:** source.md:165, TASK-WF-designSpec-20261107-075614.md:76
- **Provenance:** origin: spec 4.1 resume row 3; raised by reviewer 1, verified by reviewer 2 (narrowed)
- **Tag:** Grounded (citations re-Read by the final gate; one citation dropped (source.md:119-124))

### F11 (MINOR, non-blocking, other): Tasks 7, 8 and 12 tell the builder to classify only gh pr and gh api lines with one verb key, but WRITE_VERB_RE also hits git write verbs and keys multi-verb lines as a+b; the stale-entry test catches a miss only after a failed run.

- **Evidence:** TASK-WF-designSpec-20261107-075614.md:22, TASK-WF-designSpec-20261107-075614.md:108, TASK-WF-designSpec-20261107-075614.md:124, TASK-WF-designSpec-20261107-075614.md:182
- **Provenance:** origin: plan Tasks 7, 8, 12; raised by reviewer 3 (narrowed on its own concession)
- **Tag:** Grounded (citations re-Read by the final gate)

### F12 (MINOR, non-blocking, other): Task 10 checks the S5a and Wave 6 pre-push sentences as byte-identical using only their recorded start text, which cannot detect a later edit inside the sentence.

- **Evidence:** TASK-WF-designSpec-20261107-075614.md:33, TASK-WF-designSpec-20261107-075614.md:154
- **Provenance:** origin: plan Tasks 1 and 10; raised by reviewer 3
- **Tag:** Grounded (citations re-Read by the final gate)

## Inferred requirements (Pass 2)

Pass 1 found 0 parsed ids (the spec labels requirements FR-n, F-n, G-n, O-n, which `ID_REGEX` does not match), so `coverage_pct` (parsed-only) is null and `coverage_degraded: parsed-sparse` forbade a Tier 1 stop. Pass 2 produced 66 quote-pinned rows; the containment rule mapped 60 (`coverage_pct_union` 0.9091, `S_dev_density` 0.0909). The six rows the rule did not map (INF-006, 023, 025, 038, 042, 065) are all present in the plan on a manual read (Tasks 8, 3, 4, 6, 7, 3); the rule is lexical and under-matches. The matrix is not an exhaustive inventory of every requirement-bearing span (reviewer 2's note; real but not a plan defect). No row was dropped by the final gate (all 66 quotes match their cited spec lines).

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | engage at the first verified Medium-or-higher finding routed to a fix | source.md:6 | Goal+Constraints (containment 0.875) |
| INF-002 | default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:6 | Task 12 (containment 1.0) |
| INF-003 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | Goal+Constraints (containment 1.0) |
| INF-004 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | Goal+Constraints (containment 0.778) |
| INF-005 | No new `MonitorState`. | source.md:51 | Task 10 (containment 1.0) |
| INF-006 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none by rule (best Task 8 0.556); present on manual read |
| INF-007 | unsettled requests are reconciled before any edit, release or re-trigger | source.md:58 | Goal+Constraints (containment 0.625) |
| INF-008 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." | source.md:59 | Task 9 (containment 1.0) |
| INF-009 | PR #N is still mergeable; this run's fixes are local only. | source.md:60 | Task 9 (containment 1.0) |
| INF-010 | Print the clear command once. | source.md:61 | Task 9 (containment 1.0) |
| INF-011 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | Task 3 (containment 0.857) |
| INF-012 | Release, cause `no_edits`. | source.md:63 | Task 4 (containment 1.0) |
| INF-013 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | Task 8 (containment 1.0) |
| INF-014 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | Task 8 (containment 0.778) |
| INF-015 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | Task 3 (containment 0.6) |
| INF-016 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | Goal+Constraints (containment 0.857) |
| INF-017 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | Task 8 (containment 1.0) |
| INF-018 | PR stays draft; report `held` with the clear command. | source.md:69 | Task 8 (containment 0.857) |
| INF-019 | No `gh` or `git` word on any line, comments included (F6). | source.md:75 | Goal+Constraints (containment 0.857) |
| INF-020 | Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | Task 3 (containment 0.667) |
| INF-021 | Guard requests with no matching settle, matched by `idempotency_key` | source.md:104 | Task 3 (containment 0.833) |
| INF-022 | THIS cycle's count of applied edits | source.md:107 | Task 4 (containment 1.0) |
| INF-023 | a test imports both modules and asserts equality, because the core cannot import `recovery` | source.md:109 | none by rule (best Task 3 0.455); present on manual read |
| INF-024 | A halt with reason `draft_guard_unavailable` reports `unavailable`. | source.md:112 | Task 8 (containment 0.8) |
| INF-025 | the only foreign-toggle test; no actor identity, F11 | source.md:114 | none by rule (best Task 4 0.5); present on manual read |
| INF-026 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | source.md:133 | Task 3 (containment 1.0) |
| INF-027 | `read.state != "OPEN"` \| `HALT_PR_NOT_OPEN` | source.md:136 | Task 1 (containment 0.75) |
| INF-028 | `push_completed` and `read.head_sha == target_sha` \| `RELEASE(cause=pushed)` | source.md:156 | Task 4 (containment 0.714) |
| INF-029 | `REPORT_HELD` (no mutation; prints the clear command) | source.md:164 | Task 8 (containment 0.6) |
| INF-030 | Each reason has its own test. | source.md:165 | Goal+Constraints (containment 0.667) |
| INF-031 | `landed` is a push recovery just completed; `published` is a push that completed normally before the crash | source.md:166 | Task 8 (containment 0.889) |
| INF-032 | 43 to 45, update the docstring | source.md:175 | Task 2 (containment 1.0) |
| INF-033 | appended and fsynced BEFORE the draft/ready call | source.md:178 | Goal+Constraints (containment 0.667) |
| INF-034 | `run_log.rebuild_state()` stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`) | source.md:187 | Task 5 (containment 0.778) |
| INF-035 | For a draft request that was the first guard record, the whole record is erased | source.md:201 | Task 3 (containment 0.857) |
| INF-036 | `original_is_draft` is never read from GitHub after the first record | source.md:208 | Task 3 (containment 0.857) |
| INF-037 | `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | source.md:215 | Task 6 (containment 1.0) |
| INF-038 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none by rule (best Goal+Constraints 0.429); present on manual read |
| INF-039 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing | source.md:221 | Task 7 (containment 0.882) |
| INF-040 | gh api --paginate "repos/${REPO}/issues/${PR}/timeline" | source.md:230 | Task 7 (containment 0.875) |
| INF-041 | if not `OPEN`, emit `ok:false,error:"not_open"`; if already draft, `changed:false` | source.md:231 | Task 7 (containment 0.889) |
| INF-042 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none by rule (best Goal+Constraints 0.5); present on manual read |
| INF-043 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | Task 8 (containment 0.75) |
| INF-044 | No new python fence | source.md:241 | Goal+Constraints (containment 1.0) |
| INF-045 | update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git` | source.md:242 | Task 2 (containment 1.0) |
| INF-046 | the guard phases are fold values, not `MonitorState` members | source.md:243 | Task 10 (containment 0.833) |
| INF-047 | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. | source.md:245 | Task 13 (containment 0.778) |
| INF-048 | The SKILL mints it at the end of Wave 3 | source.md:251 | Task 8 (containment 1.0) |
| INF-049 | The entries are added after the text of each file is final, as the last step of the task that writes the file | source.md:255 | Goal+Constraints (containment 0.7) |
| INF-050 | Acceptance trace (must appear in this order in the run log) | source.md:270 | Task 11 (containment 0.833) |
| INF-051 | Without `published` no row would match and the PR would stay draft. | source.md:280 | Task 3 (containment 0.714) |
| INF-052 | halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:281 | Task 8 (containment 0.875) |
| INF-053 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | source.md:301 | Goal+Constraints (containment 1.0) |
| INF-054 | the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record | source.md:301 | Task 1 (containment 0.857) |
| INF-055 | Never stage `.claude/`. | source.md:301 | Goal+Constraints (containment 1.0) |
| INF-056 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | Task 1 (containment 0.833) |
| INF-057 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | Task 3 (containment 1.0) |
| INF-058 | the script test for a missing `jq` (exit 127) | source.md:322 | Task 7 (containment 1.0) |
| INF-059 | Cite tests and constants by symbol name | source.md:362 | Goal+Constraints (containment 1.0) |
| INF-060 | Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task. | source.md:368 | Task 2 (containment 0.909) |
| INF-061 | Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | Goal+Constraints (containment 0.889) |
| INF-062 | a crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger | source.md:318 | Task 11 (containment 1.0) |
| INF-063 | Add the acceptance trace of section 5 as a fixture over `RunLog`. | source.md:322 | Task 11 (containment 0.857) |
| INF-064 | a settled `not_applied` of either direction returns to `phase_before_request` | source.md:376 | Task 3 (containment 0.833) |
| INF-065 | whether written by the push triad or synthesized by recovery (`recovered: true`) | source.md:108 | none by rule (best Task 1 0.375); present on manual read |
| INF-066 | phase `DISABLED` with cause `already_draft` gives `off` | source.md:112 | Task 3 (containment 1.0) |

## Reviewer ensemble and merge

| Reviewer | Persona | Class | Pinned model | Served model (self-report) | Card calibration C | Findings |
|---|---|---|---|---|---|---|
| 1 | analyzer | sonnet | claude-sonnet-5-5 | claude-gw-tier1b | 0.73 (about 10 wrong line anchors) | 9 (F9 later withdrawn) |
| 2 | qa | haiku | claude-haiku-5-5 | "OpenAI assistant, backend not exposed" (identity_mismatch_suspected) | 0.81 | 6 |
| 3 | refactorer | opus | claude-opus-5-5 | claude-gw-tier1a | 0.79 | 10 |

- Calibration: blind, one opus-class calibrator per card; the disjoint-set rule could not be met with three Anthropic classes (`calibrator_diversity: degraded`). Per-finding confidences 25/25.
- Debate (sc-adversarial-protocol, Mode A, standard): base variant 1 chosen by tiebreaker (variant 3 scored 0.800 vs 0.753, margin 0.047, under 5%); merge by the merge-executor agent; `merge_method: adversarial`; artifacts in adversarial/adversarial/.
- Invariant probe: 2 HIGH and 4 MEDIUM unaddressed. Open MEDIUM warnings (single fault-finder, not debated): INV-003 the guard cycle id reused for the push and re-trigger ids; INV-004 no SKILL criterion places the zero-edit release call; INV-005 a first record erased by `not_applied` leaves the interrupted cycle unguarded on resume; INV-006 `applied_edits` is stored neither in events nor in the fold.
- Final gate: evidence-validator re-read 24 of 43 merged-finding citations; 1 dropped (source.md:119-124 for the resume row 3 claim, which stays cited at source.md:165). Zero-drop flag: not applicable.
- Shadow panel: panel_parity true, findings-block compliance 3/3 on first parse, manifest at panel/manifest.json.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 109` = 0.00

## Recommendations

### Recommendation R-001: Reword the Task 7 scan criterion so it can pass
- **File:** TASK-WF-designSpec-20261107-075614.md (plan), Task 7 criteria (lines 108 and 113); also source.md:377
- **Change:** Replace "every `gh` line carries `--repo` or a `repos/` path" with "reuse `_repo_scoped` from tests/pr_submit/test_static_grep.py over the lines `_command_lines` returns for `_GH_CMD`", and limit the fake-gh log clause to `pr` and `api` calls (the `gh repo view` fallback line is required by the `_RESOLUTION_SCRIPTS` tests).
- **Verifier:** `uv run pytest tests/pr_submit/test_set_draft_state.py tests/pr_submit/test_static_grep.py -q` passes with the script in `_RESOLUTION_SCRIPTS`.
- **Linked finding(s):** F1
- **Priority:** P0

### Recommendation R-002: Give resume row 4 the inputs and the return it needs
- **File:** source.md section 4.1 (resume_decision, row 4) and plan Task 4
- **Change:** Add `cycle_id`, `applied_edits` and `target_sha` to `resume_decision` (or return a named "check release" action the SKILL completes), state what row 4 returns, and keep the head proof mandatory.
- **Verifier:** Task 4 tests for `landed` and for `published` with a moved head return HOLD, and with a matching head return RELEASE; `uv run pytest tests/pr_submit/test_merge_guard.py -q`.
- **Linked finding(s):** F2
- **Priority:** P0

### Recommendation R-003: Define which event sets the fold's cycle_id and rebind a held guard to the new cycle
- **File:** source.md section 4.2 (fold effect table, engage row 7) and plan Tasks 3, 4 and 11
- **Change:** Say which event writes `cycle_id`, add a rebind rule for engage under a held guard, and add a two-cycle scenario test (cycle 1 release held by an unreadable timeline, crash in cycle 2 before its push, resume must not release).
- **Verifier:** the new scenario test fails against a fold that keeps cycle 1's id and passes with the rebind rule.
- **Linked finding(s):** F3
- **Priority:** P0

### Recommendation R-004: Report an unavailable engage halt as unavailable and test the producer payload
- **File:** plan Tasks 3, 8 and 11; source.md sections 4.1 (guard_status) and 4.2 (event fields)
- **Change:** Add a halt-reason override to the Exit report with a test for a read failure at engage; add spec section 4.2 to Task 8's source list and assert the key format, the `:a<k>` retry suffix and the first-request fields in the Task 11 trace test.
- **Verifier:** a test where the first engage read fails reports `unavailable`; the trace test fails when `timeline_baseline` is missing from the first request.
- **Linked finding(s):** F4, F5
- **Priority:** P1

### Recommendation R-005: Close the MINOR criteria gaps
- **File:** plan Tasks 1, 3, 4, 7, 8, 9, 10, 12 and 13
- **Change:** Add a `disabled_cause == user_override` fold assertion (F6); run `make install` and `make sync-dev` before recording the baseline (F7); name an owner and a test for the JSON-to-`GuardRead` mapping (F8); test the Wave 0 bullet for the gate wording of the print rule, not the bare words (F9); pin the order of the three resume row 3 reasons (F10); state the classification key shape for git verbs and multi-verb lines (F11); compare the pinned sentences in full, not by start text (F12).
- **Verifier:** one test or recorded command per item; `uv run pytest tests/skills/test_worker_contract.py tests/pr_submit -q` after the build.
- **Linked finding(s):** F6, F7, F8, F9, F10, F11, F12
- **Priority:** P2
