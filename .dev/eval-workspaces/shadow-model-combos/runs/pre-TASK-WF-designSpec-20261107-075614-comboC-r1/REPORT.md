```yaml
contract_version: 1.8.0
status: partial          # forced by the one dropped citation (M7, spec:139)
mode: pre
tier_reached: 2
confidence_calibrated: 0.68   # mean of three blind card scores 0.65, 0.72, 0.66 (calibrator class opus, diversity degraded)
citations_total: 35
citations_revalidated: 35
citations_dropped: 1
citations_inferred: 5
citation_budget_policy: full_reread   # 35 > 20 would allow sampling; every citation was re-read, so the band is omitted
coverage_degraded: parsed-sparse
```

# Reflect report: UC-1 pre-execution audit, TASK-WF-designSpec-20261107-075614 (pr-submit merge guard plan)

- Run: pre-TASK-WF-designSpec-20261107-075614-comboC-r1. Engine: `--t2-engine shadow` (legacy debate authoritative; panel artifacts under `panel/`).
- Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines). Plan: `.../TASK-WF-designSpec-20261107-075614.md` (13 tasks).
- Attribution: both files are an archived package. Repository HEAD has moved and carries the shipped feature; no finding rests on HEAD code. Repo facts were read with `git show e8db2fe6` (the spec's base commit).

## Verdict

No blocking defect. The plan covers the spec: 37 of 45 inferred requirement rows match a task by the deterministic rule, and a hand reading of the other 8 found each carried by a task under other wording [INFERRED]. Five MAJOR, non-blocking gaps should be fixed before the plan is reused: four acceptance criteria that a wrong implementation would pass (M1 to M4), one defect in the spec's fold table that the plan carries (M5), plus a wording clash in Task 9 (M6). Eight MINOR notes follow (M7 to M14).

Rules fired: tier 2 by the `--tier 2` pin and by rule 4 (code, tests and docs domains); coverage guard `parsed-sparse` (0 parsed IDs, 45 inferred) barred any Tier 1 stop.

## Inferred requirements (Pass 2)

Pass 1 found 0 IDs (the spec labels requirements FR-n, F-n, G-n, O-n, D-n, which the extraction pattern does not match). Pass 2 emitted 45 rows; every quote was checked verbatim against its cited line when emitted. coverage_pct = null; coverage_pct_union = 0.8222; S_dev_density = 8/45 = 0.1778. Unmapped (deterministic rule): INF-001, 014, 017, 018, 027, 028, 029, 031. No row was dropped.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Nothing mutates. A held guard found in the log is reported with the clear command. | source.md:57 | none (best TASK-8, 0.56) |
| INF-002 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger; a held guard is reported with the clear command. | source.md:58 | TASK-8 (containment, 0.76) |
| INF-003 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | source.md:59 | TASK-9 (containment, 1.00) |
| INF-004 | The final report prints "PR #N is still mergeable; this run's fixes are local only." | source.md:60 | TASK-9 (containment, 0.91) |
| INF-005 | Read, decide, request, `--to draft`, settle. Print the clear command once. | source.md:61 | TASK-8 (containment, 0.67) |
| INF-006 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | source.md:62 | TASK-3 (containment, 0.86) |
| INF-007 | Release, cause `no_edits`. | source.md:63 | TASK-4 (containment, 1.00) |
| INF-008 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | TASK-8 (containment, 1.00) |
| INF-009 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | TASK-8 (containment, 0.78) |
| INF-010 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | TASK-3 (containment, 0.60) |
| INF-011 | Do not release; report `held (timeline unreadable)`; keep pushing. | source.md:67 | TASK-8 (containment, 0.71) |
| INF-012 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | TASK-8 (containment, 1.00) |
| INF-013 | PR stays draft; report `held` with the clear command. | source.md:69 | TASK-8 (containment, 0.86) |
| INF-014 | No `gh` or `git` word on any line, comments included (F6). | source.md:75 | none (best TASK-3, 0.57) |
| INF-015 | `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | TASK-3 (containment, 0.71) |
| INF-016 | it is not the run-wide `applied_edits` output field (which counts the whole run), so a zero-edit cycle after a fixing cycle still releases with `no_edits`. | source.md:107 | TASK-8 (containment, 0.60) |
| INF-017 | whether written by the push triad or synthesized by recovery (`recovered: true`) | source.md:108 | none (best TASK-1, 0.38) |
| INF-018 | a test imports both modules and asserts equality, because the core cannot import `recovery`. | source.md:109 | none (best TASK-3, 0.40) |
| INF-019 | phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded) | source.md:112 | TASK-3 (containment, 0.67) |
| INF-020 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:127 | TASK-4 (containment, 0.60) |
| INF-021 | `REPORT_HELD` (no mutation; prints the clear command) | source.md:164 | TASK-8 (containment, 0.60) |
| INF-022 | Each reason has its own test. | source.md:165 | TASK-4 (containment, 0.67) |
| INF-023 | `ENGAGE`; `notes` carries `auto_merge_armed` when set | source.md:143 | TASK-4 (containment, 0.80) |
| INF-024 | Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`): | source.md:175 | TASK-2 (containment, 0.71) |
| INF-025 | `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + prior requests with the same cycle and direction) | source.md:184 | TASK-3 (containment, 0.80) |
| INF-026 | For a draft request that was the first guard record, the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`) | source.md:201 | TASK-3 (containment, 0.92) |
| INF-027 | `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one. | source.md:208 | none (best TASK-3, 0.53) |
| INF-028 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none (best TASK-12, 0.50) |
| INF-029 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none (best TASK-6, 0.43) |
| INF-030 | `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing. | source.md:221 | TASK-7 (containment, 0.88) |
| INF-031 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none (best TASK-8, 0.50) |
| INF-032 | No new python fence (the one-fence tests, `test_cosmos_protocol.py:34-44`, `test_codex_reviews.py:685-697`). | source.md:241 | TASK-9 (containment, 0.67) |
| INF-033 | Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | source.md:242 | TASK-2 (containment, 1.00) |
| INF-034 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | source.md:247 | TASK-8 (containment, 0.90) |
| INF-035 | The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested` | source.md:251 | TASK-8 (containment, 0.92) |
| INF-036 | The entries are added after the text of each file is final, as the last step of the task that writes the file | source.md:255 | TASK-8 (containment, 0.70) |
| INF-037 | Acceptance trace (must appear in this order in the run log): `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested`. | source.md:270 | TASK-11 (containment, 0.93) |
| INF-038 | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. | source.md:281 | TASK-8 (containment, 0.75) |
| INF-039 | Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result (`uv run pytest -q tests`: pass count and every failing test id) on the base commit before the first code edit | source.md:301 | TASK-1 (containment, 0.96) |
| INF-040 | the `landed`, `not_landed` and `ambiguous` branches produced by the real `detect_crash_window` and `resolve_crash_window` over a real `RunLog` (never injected strings) | source.md:318 | TASK-11 (containment, 0.83) |
| INF-041 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | TASK-3 (containment, 1.00) |
| INF-042 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | source.md:326 | TASK-1 (containment, 0.83) |
| INF-043 | Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence-validator` or `conflict-intent.md` on a new SKILL.md line. | source.md:369 | TASK-10 (containment, 0.74) |
| INF-044 | and the PR body states the gate plainly | source.md:326 | TASK-1 (containment, 1.00) |
| INF-045 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | source.md:301 | TASK-8 (containment, 0.92) |

## Findings

Merged by the adversarial debate (3 advocates, 2 rounds, one fault-finder probe); evidence-validator kept all 14. Severity and blocking were set by the debate: all seven `blocking: true` flags of reviewer 2 were withdrawn by their own advocate. Full text with citations: `adversarial/merged-verdict.yaml`.

### M1 (MAJOR, not blocking): Task 7 never checks the timeline count
Task 7's criteria check that the `--read` JSON carries its keys and that a failing timeline call gives `transitions: null` (plan:111-113), but none feeds N events and asserts `transitions == N`, and none asserts `--paginate` in the recorded call, which the spec requires (source.md:230). A wrong count passes; at run time it fails safe (the guard holds). Origin: reviewer 1 F1, T1 F1. Confidence 0.85.

### M2 (MAJOR, not blocking): `--undo` is never asserted
The draft call needs `--undo` (source.md:231); the script criteria check `--repo` only (plan:113) and Task 11 forbids ready-without-`--undo` only for an originally draft PR (plan:172). A missing `--undo` is caught only by `verify_failed` at run time. Origin: reviewer 2 F5. Confidence 0.65.

### M3 (MAJOR, not blocking): the auto-merge signal has no failable criterion
Engage row 11 carries `auto_merge_armed` in `notes` (source.md:143); Task 4 asserts action, reason and cause only (plan:73) and Task 7 checks that `autoMergeRequest` is printed, not its value (plan:111). Origin: reviewer 2 F7, T1 F3. Confidence 0.70.

### M4 (MAJOR, not blocking): no run-time check that one cycle id is shared
The spec has the guard, the push triad and `rereview_requested` reuse one id (source.md:251). The plan asserts where the id is minted (plan:127) and the event order (plan:170), not that the three carry the same id. Narrowed by the validator. Origin: reviewer 2 F4. Confidence 0.70.

### M5 (MAJOR, not blocking): the spec's fold never sets `disabled_cause` for a user override
`guard_status` maps phase DISABLED with cause `user_override` to `user_override` (source.md:112), but the fold row for a `user_override` skip sets only `phase = DISABLED` and `owned_draft = False` (source.md:206); only the `already_draft` row sets the cause (source.md:200). A fold built from the table leaves the cause empty and no `guard_status` rule matches. The plan's `guard_status` test lists the DISABLED-with-`user_override` case (plan:61) and can pass on a hand-built record. Origin: fault-finder INV-001, spec lines re-read by the orchestrator. Confidence 0.70.

### M6 (MAJOR, not blocking): Task 9 asks for a bullet with "no L3 condition" that must name L3
The Wave 0 bullet "carries no L3 or `draft` condition" (plan:137) yet prints the off line "at L3 with `--merge-guard off`" and says no draft call is made; the first criterion fails a bullet that "names an L3 or `draft` condition" (plan:140). The spec has the same clash (source.md:241). The task body narrows the test to gate wording, so a builder can resolve it. Origin: reviewer 2 F2, reviewer 3, T1 F2. Confidence 0.55.

### M7 (MINOR): a zero-edit later cycle can release a PR held for an earlier unpublished fix
Release row 7 uses this cycle's `applied_edits` (source.md:155-157; plan:75). It needs a new cycle after a push that did not land. [INFERRED] The base-commit protocol text halts with `terminal_halted` on a failed commit, a moved head or a bad push range, and lists mid-push crashes as `--resume` recovery, so the path is not shown reachable; the exact text for a plain push failure in a fix cycle was not located. The debaters ruled MAJOR 2 of 3; lowered to MINOR on this evidence. Origin: reviewer 1 F2. Confidence 0.45. (One citation, spec:139, dropped.)

### M8 (MINOR): the release retry has no criterion
Task 8's body specifies one retry and `already in target state` as confirmed [INFERRED: plan:124, not cited]; Task 11 only names the test (plan:169; source.md:315). Reviewer 2's claim of "no mechanism" was refuted. Confidence 0.40.

### M9 (MINOR): plan line 25 mislabels its scope limits
The plan calls them "non-goals of ./source.md" (plan:25); [INFERRED] the spec has no non-goals section (a search found none). The limit itself agrees with releasing before the CI re-poll (source.md:241). Confidence 0.35.

### M10 (MINOR): Task 11 asserts content for only some of its twelve tests
The criterion requires the names to exist and the suite to pass (plan:169, 173); content assertions are given for a few (plan:170-172). Confidence 0.50.

### M11 (MINOR): `Depends on:` gaps
Task 12 declares Tasks 6 and 8 only (plan:177-182) although it consumes the pre-build record and edits test files that Tasks 9 and 10 edit; Tasks 9, 10 and 13 also use the record without a direct Task 1 line (plan:134-135, 148, 190-193). Execution order still holds through Task 8. Spec rule: source.md:363. Confidence 0.85.

### M12 (MINOR): fold `not_applied` for a ready request is tested for one outcome
The spec returns to `RELEASE_PENDING` when a failed release preceded it (source.md:201); Task 3 tests only `HELD` (plan:60). Confidence 0.75.

### M13 (MINOR): the fold never says what sets `cycle_id`
The field is listed (source.md:190) and `held_cycle_published` compares against it (source.md:108), but no effect-table row sets it. [INFERRED] A build that keeps the first request's id could release a later cycle after a crash. Confidence 0.40.

### M14 (MINOR): the "open the PR with `--merge-guard off`" rule has no criterion
Recorded in Task 1's prose (plan:33; source.md:326), checked by no criterion. Confidence 0.55.

Noted, not findings: reviewer 3 F3 and F4 (classification-entry wording, `_RESOLUTION_SCRIPTS` conditional) and reviewer 2 F8 to F10, F12; probe INV-003 and INV-004 (LOW).

## Checked and held (no defect)
- No import cycle: `run_log` imports only `models`; `conflicts` imports `fsm` and `models` (git show e8db2fe6). The spec's F13 holds.
- Every symbol the plan names exists at the base commit; the "43" pins the plan lists in Task 2 are all the ones present (models, run_log, loop-guard ref, two tests).
- The SKILL front matter already grants `Bash(gh|git|uv|make|jq *)`; no front-matter edit is needed for the new script.

## Panel and merge record
- Reviewers (all `reflect-reviewer`): analyzer / sonnet class (self-report claude-gw-tier1b), qa / haiku class (self-report claude-haiku-5-5), refactorer / opus class (self-report claude-gw-tier1a). Findings blocks valid on the first parse: 3 of 3. Cards blind-calibrated by three `confidence-calibrator` agents (opus class; same class as reviewer 3, so calibrator_diversity degraded).
- Debate: merge_method `adversarial`, convergence 1.0 by the two-thirds rule, 0.70 by unanimity; reviewer 2's advocate withdrew most of its own findings in round 1, so part of the agreement is concession. Judge is the orchestrator (sonnet class), same class as reviewer 1 and the variant 3 advocate. The 30-criterion rubric ran once, not twice (`fallback_mode: true`).
- Invariant probe: 9 rows; the HIGH one (INV-009) was resolved by the orchestrator against the base-commit protocol text (see the M7 caveat).
- Citation pre-check: 62 of 62 flagged `not-in-snapshot` against the frozen snapshot (it names files relative to the input folder); 0 of 62 flagged against a repo-relative copy (`panel/precheck-repo-paths.json`).
- Identity: identity_source `requested-pinned`; self-reports name the pinned alias or model for all three, so no mismatch is suspected, but a self-report is not proof of the served model.

## Grounding gaps
None.

## Inferred-claim audit

- `citations_inferred: 5` (M7, M8, M9, M13 and the hand reading of the 8 unmatched rows)
- Inferred-fraction: `5 / 35` = 0.14

## Recommendations

### Recommendation R-001: assert the timeline count and pagination in the script test
- **File:** the plan's Task 7 acceptance criteria
- **Change:** add a fake-`gh` case that returns N mixed `convert_to_draft` and `ready_for_review` events across two pages and assert `transitions == N` and `--paginate` in the recorded argument log.
- **Verifier:** the new case fails against a script that counts one event type or omits `--paginate`.
- **Linked deviation(s):** M1
- **Priority:** P1

### Recommendation R-002: assert `--undo` and the auto-merge value
- **File:** the plan's Tasks 4 and 7 acceptance criteria
- **Change:** assert `pr ready ... --undo` is called for `--to draft` and absent for `--to ready`; assert `autoMergeRequest` true yields `notes` with `auto_merge_armed` and false does not.
- **Verifier:** a script that drops `--undo`, or an engage decision that drops `notes`, fails the new tests.
- **Linked deviation(s):** M2, M3
- **Priority:** P1

### Recommendation R-003: assert the shared cycle id at run time
- **File:** the plan's Task 11 acceptance criteria
- **Change:** in the acceptance-trace test, assert the guard events, the push triad events and `rereview_requested` of one cycle carry the same `cycle_id`.
- **Verifier:** a push written under another id fails the test.
- **Linked deviation(s):** M4
- **Priority:** P1

### Recommendation R-004: make the fold set `disabled_cause` for a user override
- **File:** the spec section 4.2 fold table (source.md:206) and the plan's Task 3 acceptance criteria
- **Change:** add `disabled_cause = user_override` to that row; require a test that folds a real `settled(any, skipped, user_override)` log and passes the result to `guard_status`.
- **Verifier:** `guard_status` returns `user_override` for the folded record, not for a hand-built one.
- **Linked deviation(s):** M5
- **Priority:** P1

### Recommendation R-005: reword the Task 9 Wave 0 criterion
- **File:** the plan's Task 9 (plan:137, 140) and the spec (source.md:241)
- **Change:** say the bullet has no condition on loading the ref (no "L3 only" and no "draft only" gate), while it may name L3 for the off line.
- **Verifier:** the Wave 0 test passes on a bullet that prints the off line.
- **Linked deviation(s):** M6
- **Priority:** P2

### Recommendation R-006: tidy the MINOR items before reuse
- **File:** the plan's Tasks 1, 3, 8, 9, 11, 12, 13 and plan line 25
- **Change:** add the missing `Depends on:` lines (M11), a `RELEASE_PENDING` fold case (M12), a one-retry criterion (M8), content assertions for each Task 11 test (M10), a PR-opening check (M14); relabel line 25 (M9); state what sets `cycle_id` (M13); decide whether a later cycle can follow a held release (M7).
- **Verifier:** re-run `/sc:reflect --mode pre` on the revised plan; M7 to M14 no longer reproduce.
- **Linked deviation(s):** M7 to M14
- **Priority:** P2
