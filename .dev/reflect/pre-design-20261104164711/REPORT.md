# sc:reflect UC-1 report: issue #305 plan (TASK-WF-design-20261104-164423)

<!-- Rendered from refs/report-template.md. Wave 5 renders the validated merged card; it does not re-judge it. -->

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.807
citations_total: 117
citations_revalidated: 117
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: null
```

## Summary

- **Verdict:** ready-with-fixes (merged by sc:adversarial Mode A, `merge_method: adversarial`, base card opus:refactorer).
- **Convergence:** 0.852 (23 of 27 diff points; PASS under the reflect routing, 0.75 or higher). The invariant gate blocked once on 3 HIGH findings and cleared after one resolution round.
- **Findings:** 23 (5 Medium, 18 Low). No regression and no invented functional requirement.
- **Main risk:** Task 4 must split into 4a and 4b, with 4b placed between Task 7 and Task 8, because `/sc:implement` runs tasks in document order and ignores `Depends on`. The other dependency-edge fixes are Low only while execution stays sequential in document order.
- **Advisory only:** reflect never edits the plan (sc:workflow Wave 4). These findings go to the implementer.
- **Reviewers:** sonnet analyzer, glm-5.3 (haiku alias) qa, opus refactorer; blind-calibrated 0.82 / 0.78 / 0.82 (`calibrator_diversity: degraded`, all three classes were reviewers).

## Coverage (UC-1)

- `coverage_pct` (parsed only): 1.0 (574 of 574 parsed requirements mapped).
- `coverage_pct_union` (parsed + inferred): 0.9655 (13 of 34 inferred rows mapped; 21 unmapped).
- `best_practice_grade`: 4 of 5 (Tier 1 card).
- Partial mappings: 6.5-site-1, 6.5-site-2, sec-8, sec-12, sec-12.5, 13-step-14.
- Out of scope (15): OOS-P3-#361, FR-25, 2.1-out-live-gates, 2.1-out-default-flip, V1, V2, V3, V4, V5, V6, V7, V8, 11-8-R-19, 11-9-R-20, 11-31-R-161.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Proof in this release is hermetic real-git tests in pytest temporary directories (local bare repository as `origin`, `gh` stubbed, no network). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:55 | unmapped |
| INF-002 | No new agent, template, FSM state or idempotency set. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:57 | unmapped |
| INF-003 | Everything in spec section 11 ("Out of scope") stays out: rebasing, history rewriting, PR splitting, external merge tools, rerere, cross-repo heads, resolving in another worktree, a user-override channel, `gh pr update-branch`, migration/submodule/binary/protected/unknown-lockfile resolution. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:69 | unmapped |
| INF-004 | A nested `pkg/uv.lock` fails rule 7 (not the exact root path) and lands in rule 8. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:196 | mapped (Task 3) |
| INF-005 | **Plan tier** (`conflict_plan`, first matching row): | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:198 | mapped (Task 3) |
| INF-006 | `regen:*` paths do not count toward `TIER2_MAX_FILES` (OQ-9). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:212 | unmapped |
| INF-007 | In a Tier 2 cycle, `regen:*` paths are handled by their rule after the text paths are resolved and staged (manifest first, R-58), so a conflicted `pyproject.toml` plus `uv.lock` is Tier 2 (OQ-10). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:212 | unmapped |
| INF-008 | **Escalation is monotone inside a cycle**: a cycle that starts as Tier 1 or 2 can escalate to Tier 3 (halt) at any step and never de-escalates or retries in the same run. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:214 | unmapped |
| INF-009 | **`c_initial`** (ordinal 3 only; entered only after a `wave0` result of `tier2_planned`; the plan is the fresh re-probe): | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:236 | unmapped |
| INF-010 | **`wave8a`** (ordinals 1 to 3; `skip_ci` is true on every row except the two marked): | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:249 | mapped (Task 4) |
| INF-011 | Properties pinned by tests (section 12.1): every reachable row is asserted; the default row is reached by each domain violation; | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:267 | mapped (Task 4) |
| INF-012 | Tier 2 is acted on only at L3 at `C-initial`; at L1 and L2 Tier 2 is reported and never resolved (OQ-21). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:267 | unmapped |
| INF-013 | The `status` enum (`SKILL.md:236`) gains no member. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:282 | unmapped |
| INF-014 | Revert of a pushed merge commit is always a new commit, `git revert -m 1 <merge_sha>`; the L2 and L3 reports print it (K13). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:307 | unmapped |
| INF-015 | **Two new event types (41 to 43), used by both conflict tiers** (OQ-17 / C-029 / X-011): | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:311 | unmapped |
| INF-016 | Report-only detection writes no event (the plan is printed); every halt reuses `terminal_halted` with a `reason` (section 9). No other event type is added. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:325 | unmapped |
| INF-017 | For `sync` and `ci`: a missing or unknown `review_terminal`, or (for `sync`) a missing 40-hex `base_sha`, gives `halt`, `resume_unrepresentable`. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:398 | mapped (Task 4) |
| INF-018 | `sync` and `ci` never resume into `S4_PUSHING`, S5a or S5 (INV-001). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:398 | mapped (Task 8) |
| INF-019 | Kinds `fix`, `ci` and absent have no conflict cycle and append nothing new (byte-equal to today for `fix` / absent). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:409 | mapped (Task 8) |
| INF-020 | The wrapper finds the cycle by the dangling record's `cycle_id` and appends only when `is_conflict_cycle(cycle_id)` and that cycle is open in `rebuild_state()`; it never appends twice. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:409 | mapped (Task 8) |
| INF-021 | Exit: `0` on any completed probe; `2` with `PROBE_FAIL <reason>` for `usage`, `not_a_worktree`, `origin_mismatch`, `bad_base`, `fetch_failed`, `no_merge_base`, `merge_tree_failed`. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:793 | unmapped |
| INF-022 | The SKILL calls it with `--program uv` (the programs of `MECHANICAL_RULES`). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:793 | unmapped |
| INF-023 | Commit mode, in order: | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:812 | mapped (Task 11) |
| INF-024 | Token to halt reason: `no_merge_head` and `foreign_merge` to `sync_foreign_operation`; `unmerged` to `sync_unmerged_left`; `markers` to `sync_marker_left`; | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:824 | unmapped |
| INF-025 | The SKILL passes `--out <output-dir>/sync/<cycle_id>/<n>/` (`<n>` = the path's 1-based position in `plan.text_paths`). `EVIDENCE_FAIL` of any kind escalates the cycle to Tier 3 (`sync_tier3`). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:844 | unmapped |
| INF-026 | Header comment (`:3-12`) gains the usage and output lines for the new mode. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:859 | unmapped |
| INF-027 | The existing `src/superclaude/` header line (`:14`) is pre-existing; this change adds no new one. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:859 | mapped (Task 13) |
| INF-028 | Line budget: E1 1 + E3 3 + E4 3 + E6 1 + E10 1 + E11 2 + E12 4 = 15; E2, E5, E7, E8, E9, E13 change no line count. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:981 | mapped (Task 17) |
| INF-029 | (The arrow glyphs are the ones the file already uses at `:104`; no em dash.) | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1056 | unmapped |
| INF-030 | Both `gh api` lines carry a `repos/<owner/repo>/` path, so they satisfy `_repo_scoped` (`test_static_grep.py:103-129`). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1082 | mapped (Task 16) |
| INF-031 | Whether a reason halts is decided by the `ConflictAction.status` of the row, never by the reason string. | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1129 | unmapped |
| INF-032 | CI-side report reasons: `pr_conflicting` (CI wait skipped), `ci_not_started` (CI expiry with no registered check). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1129 | unmapped |
| INF-033 | The spec's byte-identical fragments (spec section 8.4), asserted in `test_conflict_sync_protocol.py` as one regression test: | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1348 | mapped (Task 18) |
| INF-034 | Manual verification is never reported as a test pass (section 14 lists it separately). | .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1404 | unmapped |

POSTSCRIPT: the evidence-validator checked all 34 INF rows against their cited source.md lines and dropped none (artifacts/evidence-validation.yaml).

## Deviations

### Deviation D-01 (CF-01, low): tests/pr_submit/test_conflict_scripts.py is created by Task 10 and appended to by Tasks 11, 12 and 13

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:186
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:186; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:196; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:207; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:215-217; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1424
- **Claim:** tests/pr_submit/test_conflict_scripts.py is created by Task 10 and appended to by Tasks 11, 12 and 13. Task 13 has no Depends-on line, and Tasks 11 and 12 are siblings (both depend only on Task 10), so a graph-ordered or parallel executor hits a missing file or conflicting appends.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-4, A A-1, B Q-2, debate C-001
- **Default remediation:** P:207 Task 12 becomes "Depends on: Task 11"; insert "Depends on: Task 12" under the Task 13 heading (P:215). This gives the chain 10 -> 11 -> 12 -> 13. Verify: every task that edits tests/pr_submit/test_conflict_scripts.py has a path to every earlier editor.
- **Qualifier:** Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97; the plan has no independent or parallel marker). Under a graph-order or parallel executor this row reverts to Medium.

### Deviation D-02 (CF-02, low): Task 15 depends only on Task 12 (chain 12 -> 10 -> 3 -> 2), but its record check calls parse_resolution_record and resolution_record_ok, which Task 4 creates (Task 4a after the split)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:239
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:239; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:241; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:245; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:91; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:590-591
- **Claim:** Task 15 depends only on Task 12 (chain 12 -> 10 -> 3 -> 2), but its record check calls parse_resolution_record and resolution_record_ok, which Task 4 creates (Task 4a after the split).
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-5 part a, A A-2, B Q-3
- **Default remediation:** P:239 Task 15 becomes "Depends on: Task 4a, Task 12". P:241 "from Task 4" becomes "from Task 4a". Verify: Task 15's closure contains Task 4a.
- **Qualifier:** Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97). Under a graph-order or parallel executor this row reverts to Medium.

### Deviation D-03 (CF-03, medium): Task 16 depends only on Task 2, but its ci-poll.md item 4 fences "scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>" and documents ci.expect_checks_after_push, which Task 13 and Task 6 create

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:248-256
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:248-256; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1063-1080; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1425
- **Claim:** Task 16 depends only on Task 2, but its ci-poll.md item 4 fences "scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>" and documents ci.expect_checks_after_push, which Task 13 and Task 6 create. Spec step 10 (refs) depends on step 9 (scripts), and S:1070 names both functions. No test compares the fenced line with the script header. The header check is the Medium part; the missing edge is the Low part.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-3, B Q-4 (grep), A A-3, debate C-002
- **Default remediation:** P:250 Task 16 becomes "Depends on: Task 2, Task 6, Task 13". Add a Task 16 AC: grep that the fenced `scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>` line in ci-poll.md matches the script header, with output saved under ./artifacts/. Verify: no ref task runs before the script or function its text names, and the grep output file exists.
- **Qualifier:** The Low rating applies to the edge part only (round-inv A and C: "only the edge part is lowered"); the header-match check stays Medium. The edge part is Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97); under a graph-order or parallel executor it reverts to Medium.

### Deviation D-04 (CF-04, low): Task 20 (spec step 14 depends on all steps, S:1429) has a closure through Tasks 18 and 19 that omits Task 6 and Task 9, which are graph leaves

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:298-300
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:298-300; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:124-135; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:169-178; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1429
- **Claim:** Task 20 (spec step 14 depends on all steps, S:1429) has a closure through Tasks 18 and 19 that omits Task 6 and Task 9, which are graph leaves.
- **Classification:** drift
- **Classification rationale:** merged from A A-4, B Q-8, C (base) F-5 part b ('9 suffices' conceded by C in R2), debate C-003
- **Default remediation:** P:300 Task 20 becomes "Depends on: Task 6, Task 9, Task 18, Task 19". Verify: Task 20's closure covers Tasks 1, 2, 3, 4a, 4b and 5-19.
- **Qualifier:** Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97). Under a graph-order or parallel executor this row reverts to Medium.

### Deviation D-05 (CF-05, low): Task 4's Resume tests build `state` dicts by hand (P:93) and run before the run-log fold (Task 7), while spec step 7 places the resume rows after the fold (S:1422)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:92-93
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:92-93; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:106; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:151; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:153-155; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:171; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:594; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:671-678; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:741-749; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1418; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1422; ~/.claude/skills/sc-implement-protocol/SKILL.md:79; ~/.claude/skills/sc-implement-protocol/SKILL.md:97
- **Claim:** Task 4's Resume tests build `state` dicts by hand (P:93) and run before the run-log fold (Task 7), while spec step 7 places the resume rows after the fold (S:1422). After the split, the resume planners (4b) must sit in the document between Task 7 and Task 8, because /sc:implement runs tasks in document order and ignores depends-on. The edges must also leave no 4b -> 5 -> 4b cycle (INV-001) and must put the 4b planners in Task 9's closure, because the package __init__ exports them (S:744; INV-002).
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-1b, A R2 (4b on Task 5), B R2 (Task 8 -> 4b), C R2 fallback (5 -> 4a, 9 -> 4b), R-INV round-inv-advocate-A/B/C, debate C-004
- **Default remediation:** the nine plan edits listed under recommendation R for CF-05

### Deviation D-06 (CF-06, low): Task 4 is too large for one QA verdict and mixes functions that belong before the run-log fold (router, gates, cycle ids, records, message) with the resume planners that need RunLog.rebuild_state() and so belong after Task 7

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:84-100
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:84-100; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1418; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1422
- **Claim:** Task 4 is too large for one QA verdict and mixes functions that belong before the run-log fold (router, gates, cycle ids, records, message) with the resume planners that need RunLog.rebuild_state() and so belong after Task 7.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-1a, A R2 (adopted C's split), debate C-005
- **Default remediation:** Split Task 4 into 4a (the non-resume functions of source section 5.3 with their tests; depends on Task 3) and 4b (crash_resume_plan, conflict_resume_plan and the Resume tests; after Task 7). The exact edits are items 1 and 3 to 6 of the CF-05 recommendation. Verify: the logs ./artifacts/t4a-tests.log and ./artifacts/t4b-tests.log both exist; the Router, Gates, Cycle ids and Record cases are in 4a and the Resume cases are in 4b.

### Deviation D-07 (CF-07, low): Tasks 8, 17 and 18 are large for a single QA verdict

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:153-167
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:153-167; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:263-273; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:277-285; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1422; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1426; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1427
- **Claim:** Tasks 8, 17 and 18 are large for a single QA verdict. This is advisory only: they mirror spec steps 7, 11 and 12 (S:1422, S:1426, S:1427).
- **Classification:** advisory (not a deviation) (as merged; outside the four-class taxonomy, rendered verbatim)
- **Classification rationale:** merged from A A-10b
- **Default remediation:** Optional per-family log sections for Tasks 8, 17 and 18. No plan change is required. Verify: n/a (advisory).

### Deviation D-08 (CF-08, medium): The constraint at P:27 says .dev/tasks is always staged and only exact paths are staged, and spec step 14 requires staging src/, tests/, CHANGELOG.md and .dev/tasks/ only (S:1429), but no task stages anything

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:27
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:27; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:302; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:307; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1429
- **Claim:** The constraint at P:27 says .dev/tasks is always staged and only exact paths are staged, and spec step 14 requires staging src/, tests/, CHANGELOG.md and .dev/tasks/ only (S:1429), but no task stages anything. Task 20's check "no staged .claude/ path other than .claude/settings.json" (P:307) is therefore vacuously true on an empty staged set.
- **Classification:** drift
- **Classification rationale:** merged from A A-6b, B Q-7 / U-014, debate C-006
- **Default remediation:** Add a staging step to Task 20 after the `make sync-dev` instruction (P:302): `git add -- src tests CHANGELOG.md` and `git add .dev/tasks`, and no commit. Add an AC that `git diff --cached --name-only` lists only those paths, which makes P:307's "no staged .claude/ path" check non-vacuous. Verify: the `git diff --cached --name-only` output is saved to ./artifacts/t20-checks.log.

### Deviation D-09 (CF-09, medium): Task 10's AC says `git ls-files -s` shows mode 100755 (P:191), but a newly created file that no task has staged has no index entry, so the check cannot be observed

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:191
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:191; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:27; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:298-307; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:863; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1429
- **Claim:** Task 10's AC says `git ls-files -s` shows mode 100755 (P:191), but a newly created file that no task has staged has no index entry, so the check cannot be observed. Tasks 11 and 12 create scripts with the same mode rule.
- **Classification:** drift
- **Classification rationale:** merged from A A-6a / U-002
- **Default remediation:** P:191 Task 10 AC: replace "`git ls-files -s` shows mode 100755" with `test -x <path>`. Apply the same check to the scripts of Tasks 11 and 12. Use a `git ls-files -s` mode check only after the CF-08 staging. Verify: `test -x` exits 0 for each new script.

### Deviation D-10 (CF-10, low): The pinned-phrase, order-pin and prohibition criteria of Tasks 10, 11, 14 and 15 have no command that can fail until Task 18 adds the static tests

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:191
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:191; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:202; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:232-235; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:243-246; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1003; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1022; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1324
- **Claim:** The pinned-phrase, order-pin and prohibition criteria of Tasks 10, 11, 14 and 15 have no command that can fail until Task 18 adds the static tests.
- **Classification:** drift
- **Classification rationale:** merged from A A-7 / U-006
- **Default remediation:** Tasks 10, 11, 14, 15: one literal `grep -cF` per pinned phrase, ascending line numbers for order pins, and forbidden-regex greps with no hits, saved under ./artifacts/. Verify: the grep files exist and have the expected counts.

### Deviation D-11 (CF-11, medium): Task 10 gives its real-git tests a module-level capability skip (skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository, P:186), but Task 19's real-git end-to-end tests carry only the `uv`-absent skip (P:291)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:186
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:186; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:291; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1316
- **Claim:** Task 10 gives its real-git tests a module-level capability skip (skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository, P:186), but Task 19's real-git end-to-end tests carry only the `uv`-absent skip (P:291). Source section 12 requires the capability skip at the start of each real-git module (S:1316), so X1 to X3 error instead of skipping where merge-tree is unsupported.
- **Classification:** drift
- **Classification rationale:** merged from B Q-5b, A A-8a
- **Default remediation:** P:291 Task 19: add Task 10's module-level capability skip (skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository) alongside the `uv`-absent skip. Verify: X1 to X3 skip, rather than error, where merge-tree is unsupported.

### Deviation D-12 (CF-12, medium): The real-git test constraint at P:29 drops the fixed author and committer that source section 12 requires (S:1316)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:29
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:29; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:186; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1316
- **Claim:** The real-git test constraint at P:29 drops the fixed author and committer that source section 12 requires (S:1316). With GIT_CONFIG_GLOBAL=/dev/null, `git commit` has no identity and fails, which breaks F9, F10, X1 and X3.
- **Classification:** drift
- **Classification rationale:** merged from B Q-5a, A A-8b
- **Default remediation:** P:29: add a fixed GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL to the real-git test constraint. Verify: F9, F10, X1 and X3 commit under GIT_CONFIG_GLOBAL=/dev/null.

### Deviation D-13 (CF-13, low): Task 2 drops the clause that source section 6.5 adds to both models.py docstrings: "plus the two conflict-cycle events `sync_started` and `sync_concluded`" (S:728)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:51
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:51; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:728; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:729; src/superclaude/pr_submit/models.py:3
- **Claim:** Task 2 drops the clause that source section 6.5 adds to both models.py docstrings: "plus the two conflict-cycle events `sync_started` and `sync_concluded`" (S:728).
- **Classification:** drift
- **Classification rationale:** merged from A A-8c, B Q-6a
- **Default remediation:** P:51 Task 2: quote the S:728 clause "plus the two conflict-cycle events `sync_started` and `sync_concluded`" for both docstrings. Verify: a grep of the models.py docstrings finds the clause.

### Deviation D-14 (CF-14, low): P:53 cites loop-guard.md:86-99, copied from S:731, but the event list ends at line 103

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:53
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:53; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:731; src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:86; src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:103
- **Claim:** P:53 cites loop-guard.md:86-99, copied from S:731, but the event list ends at line 103. The defect is in the spec, and the plan inherits it.
- **Classification:** spec defect (as merged; outside the four-class taxonomy, rendered verbatim)
- **Classification rationale:** merged from A A-8d, B Q-6b
- **Default remediation:** P:53: cite `loop-guard.md:86-103`. Verify: n/a (citation fix).

### Deviation D-15 (CF-15, low): Dropping `make test` from Task 20 is an explicit orchestrator constraint (P:28), so the drop is authorized

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:28
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:28; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:306; src/superclaude/cli/reflect/commands.py:99; tests/cli/reflect/test_contract_status_cli.py:18; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1408
- **Claim:** Dropping `make test` from Task 20 is an explicit orchestrator constraint (P:28), so the drop is authorized. The residual is that tests/cli/reflect/test_contract_status_cli.py, the only test outside tests/pr_submit that exercises superclaude.pr_submit (src/superclaude/cli/reflect/commands.py:99 imports pr_submit.contract_setup), is outside every task's verification run. An __init__ import failure already breaks every tests/pr_submit test, so only the CLI path is unexercised.
- **Classification:** authorized
- **Classification rationale:** merged from C (base) F-6, A A-9, B Q-1, debate C-009
- **Default remediation:** P:306: add tests/cli/reflect/test_contract_status_cli.py to Task 20's pytest run. The first line of ./artifacts/t20-checks.log reads "make test (VG-2) not run per orchestrator brief". Verify: t20-checks.log shows the reflect test passing.

### Deviation D-16 (CF-16, low): The plan adds light verification artifacts beyond the spec (Task 15 sample-record check, Task 18 negative check, Task 17 diffstat with "at most 15 lines")

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:31
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:31; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:245; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:270; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:285; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:867; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1324
- **Claim:** The plan adds light verification artifacts beyond the spec (Task 15 sample-record check, Task 18 negative check, Task 17 diffstat with "at most 15 lines"). No functional requirement is invented.
- **Classification:** authorized
- **Classification rationale:** merged from C (base) F-11, A A-11, debate C-010
- **Default remediation:** No change. Verify: n/a.

### Deviation D-17 (CF-17, low): Task 19 (X1) replays the mechanical ref steps, whose step 11 calls poll-ci-checks.sh --evidence-sha (Task 13), but Task 19 depends only on Tasks 5, 8, 11 and 12

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:289
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:289; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:291; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1400; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1424; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1428
- **Claim:** Task 19 (X1) replays the mechanical ref steps, whose step 11 calls poll-ci-checks.sh --evidence-sha (Task 13), but Task 19 depends only on Tasks 5, 8, 11 and 12. Spec step 13 depends on all of step 9 (S:1428, S:1424), so Task 19 has no path to Task 13. Only the Task 13 edge is required: X1's command list (S:1400) omits expect_checks_after_push.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-2 (reduced), debate U-001
- **Default remediation:** P:289 Task 19 becomes "Depends on: Task 5, Task 8, Task 11, Task 12, Task 13". The Task 6 and Task 14 edges are optional. Verify: Task 19's closure includes Tasks 10-13.
- **Qualifier:** Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97). Under a graph-order or parallel executor this row reverts to Medium.

### Deviation D-18 (CF-18, low): Spec step 9 requires test_skill_forbids_force_push to be green over the new files (S:1424), but Tasks 11 and 12 run only test_conflict_scripts.py

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:203
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:203; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:213; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1424; tests/pr_submit/test_static_grep.py:773-776
- **Claim:** Spec step 9 requires test_skill_forbids_force_push to be green over the new files (S:1424), but Tasks 11 and 12 run only test_conflict_scripts.py.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-7, debate U-003
- **Default remediation:** P:203 and P:213: add tests/pr_submit/test_static_grep.py to the pytest commands of Task 11 and Task 12. Verify: the logs include test_skill_forbids_force_push.

### Deviation D-19 (CF-19, low): poll-ci-checks.sh:30 exits 2 when --pr is missing, and no acceptance criterion runs C1 to C4 without --pr, so C4's exit 2 could pass for the wrong reason

- **Location:** src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:30
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:30; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:217; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:220; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1394
- **Claim:** poll-ci-checks.sh:30 exits 2 when --pr is missing, and no acceptance criterion runs C1 to C4 without --pr, so C4's exit 2 could pass for the wrong reason.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-8, debate U-005
- **Default remediation:** Task 13 AC (P:220): C1 to C4 invoke the script with `--evidence-sha` and `--repo` only (no `--pr`); C4 asserts that stderr names the invalid SHA. Verify: the C-case argument lists contain no `--pr`.

### Deviation D-20 (CF-20, low): E5 and E12 are split between Task 1 and Task 17 (the spec splits them itself, S:1416 and S:1426)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:39
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:39; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:267; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:901-909; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:961-969; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1416; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1426
- **Claim:** E5 and E12 are split between Task 1 and Task 17 (the spec splits them itself, S:1416 and S:1426). After Task 1 the E5 old substring is gone, and Task 17 does not name where the operation-check sentence and the E12 rows 3 to 5 go.
- **Classification:** drift
- **Classification rationale:** merged from C (base) F-9, debate X-003
- **Default remediation:** Task 17 (P:267): the E5 operation-check sentence goes right after Task 1's text ending "so report how many commits it is behind instead)."; E12 rows 3-5 go after the "Behind base branch (create path at L1+, or `--pr`)" row. AC: the final Wave 0 substring equals the full E5 replacement in source section 8.1. Verify: the substring check is recorded in the Task 17 evidence.

### Deviation D-21 (CF-21, low): Only Task 9 -> Task 6 is stricter than spec section 13 (step 8 depends on steps 3 and 4, S:1423)

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:106
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:106; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:155; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:171-173; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:178; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1419; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1423
- **Claim:** Only Task 9 -> Task 6 is stricter than spec section 13 (step 8 depends on steps 3 and 4, S:1423). Task 5 and Task 8 on Task 4 are spec-required (step 3 = Tasks 3 + 4). The Task 9 -> Task 6 edge is justified because Task 9's AC collects test_ci_classify.py (P:178).
- **Classification:** necessary
- **Classification rationale:** merged from C (base) F-10 (claim corrected), debate X-004
- **Default remediation:** Keep the edge Task 9 -> Task 6 (P:171). No change. Verify: n/a.

### Deviation D-22 (CF-22, low): No card audited the consumers of Task 4 functions that spec test cases cite by ID

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:184
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:184; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:196; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:91; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1345; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1388; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1390
- **Claim:** No card audited the consumers of Task 4 functions that spec test cases cite by ID. Task 11 (F10 merge_parent_ok, F12 merge_preflight_ok; S:1388, S:1390) and Task 18 (S:1345) need Task 4a functions but do not depend on it, and Task 10 depends only on Task 3.
- **Classification:** drift
- **Classification rationale:** merged from calibration-t2.yaml missed lists (reviewer-1, reviewer-2), debate A-001
- **Default remediation:** P:184 Task 10 becomes "Depends on: Task 3, Task 4a". Verify: Task 11 (F10 merge_parent_ok, F12 merge_preflight_ok; S:1388, S:1390), Task 15 and Task 18 (S:1345) all reach Task 4a.
- **Qualifier:** Low only while /sc:implement runs sequentially in document order with no parallel-marked set (IMPL:79, IMPL:97). Under a graph-order or parallel executor this row reverts to Medium.

### Deviation D-23 (INV-007, low): Tasks 1 and 3 both edit tests/pr_submit/test_static_grep.py (Task 1 rewrites :654-661, P:40; Task 3 adds conflicts.py to CORE_PURE_FILES, P:75) and no edge orders them

- **Location:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:40
- **Mapped tasklist item:** see claim
- **Spec section:** see evidence (source.md lines)
- **Evidence:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:40; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:66; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:75; .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:281; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1416; .dev/tasks/to-do/TASK-WF-design-20261104-164423/source.md:1418
- **Claim:** Tasks 1 and 3 both edit tests/pr_submit/test_static_grep.py (Task 1 rewrites :654-661, P:40; Task 3 adds conflicts.py to CORE_PURE_FILES, P:75) and no edge orders them. The spec has the same gap (step 1 depends on none, S:1416; step 3 depends on step 2, S:1418). The problem is latent under document order.
- **Classification:** unassigned (not assigned in debate; the spec carries the same gap) (as merged; outside the four-class taxonomy, rendered verbatim)
- **Classification rationale:** merged from invariant probe INV-007, R-INV E4 (accepted by A, B and C)
- **Default remediation:** P:66 Task 3 becomes "Depends on: Task 1, Task 2". Verify: Task 1 and Task 3 (both edit test_static_grep.py, P:40, P:75) are ordered; Task 18, which also edits the file (P:281), is already ordered after both.

## Grounding Gaps

Dropped by the evidence-validator (section 11.2; detail in artifacts/evidence-validation.yaml). The citation is removed from D-16 above; the claim still stands on its other citations (P:245, P:270, P:285).

### Gap G-01

- **Hunk ref:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md:176
- **Original claim (D-16, CF-16):** The plan adds light verification artifacts beyond the spec (Task 15 sample-record check, Task 18 negative check, Task 17 diffstat with "at most 15 lines").
- **Evidence missing:** line 176 is Task 9's import check, which repeats the spec's own step-8 done-when (S:1423) and is none of the three named items.
- **Why not classifiable:** the line does not support an "addition beyond the spec" claim.
- **Next evidence needed:** none; the three named items are cited at P:245, P:270 and P:285 and hold.

Validator notes (true claims, small line offsets, kept): D-08 cites P:27 for "only exact paths are staged", which is at P:25; D-03's "S:1070 names both functions" holds only for the range S:1063-1080 (the script line is S:1075); D-04 calls Task 6 a graph leaf, but Task 9 depends on it (the closure omission still holds).

## Unresolved debate points

- **S-004** (Finding order (L1 surface)): No advocate argued it, so no position formed (50%). Presentation only. The merged card keeps the base order (consensus-table order CF-01 to CF-22, then INV-007).
- **S-005** (Evidence paths and recommendation shape (L1 surface)): No advocate argued it (50%). The merged card keeps the base format: repo-relative evidence paths and a Verify clause on every recommendation.
- **S-006** (Provenance header (L1 surface)): No advocate argued it (50%). The cards' headers are orchestrator-written. This card carries the provenance header above.
- **C-013** (Summary caveats: B's 21 unmapped-union INF rows could not be resolved to spec sections): Only C's advocate supported it (R1, as A-005 QUALIFY) and no majority formed (50%). It is not imported as consensus; it is reported to the sc:reflect orchestrator as an open coverage caveat.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 117` = 0.00

## Recommendations

### Recommendation R-01 (CF-03): P1 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:250 Task 16 becomes "Depends on: Task 2, Task 6, Task 13". Add a Task 16 AC: grep that the fenced `scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>` line in ci-poll.md matches the script header, with output saved under ./artifacts/.
- **Verifier:** no ref task runs before the script or function its text names, and the grep output file exists.
- **Linked deviation(s):** CF-03
- **Priority:** P1

### Recommendation R-02 (CF-08): P1 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** Add a staging step to Task 20 after the `make sync-dev` instruction (P:302): `git add -- src tests CHANGELOG.md` and `git add .dev/tasks`, and no commit. Add an AC that `git diff --cached --name-only` lists only those paths, which makes P:307's "no staged .claude/ path" check non-vacuous.
- **Verifier:** the `git diff --cached --name-only` output is saved to ./artifacts/t20-checks.log.
- **Linked deviation(s):** CF-08
- **Priority:** P1

### Recommendation R-03 (CF-09): P1 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:191 Task 10 AC: replace "`git ls-files -s` shows mode 100755" with `test -x <path>`. Apply the same check to the scripts of Tasks 11 and 12. Use a `git ls-files -s` mode check only after the CF-08 staging.
- **Verifier:** `test -x` exits 0 for each new script.
- **Linked deviation(s):** CF-09
- **Priority:** P1

### Recommendation R-04 (CF-11): P1 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:291 Task 19: add Task 10's module-level capability skip (skip unless `git merge-tree --write-tree HEAD HEAD` works in a scratch repository) alongside the `uv`-absent skip.
- **Verifier:** X1 to X3 skip, rather than error, where merge-tree is unsupported.
- **Linked deviation(s):** CF-11
- **Priority:** P1

### Recommendation R-05 (CF-12): P1 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:29: add a fixed GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL to the real-git test constraint.
- **Verifier:** F9, F10, X1 and X3 commit under GIT_CONFIG_GLOBAL=/dev/null.
- **Linked deviation(s):** CF-12
- **Priority:** P1

### Recommendation R-06 (CF-01): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:207 Task 12 becomes "Depends on: Task 11"; insert "Depends on: Task 12" under the Task 13 heading (P:215). This gives the chain 10 -> 11 -> 12 -> 13.
- **Verifier:** every task that edits tests/pr_submit/test_conflict_scripts.py has a path to every earlier editor.
- **Linked deviation(s):** CF-01
- **Priority:** P2

### Recommendation R-07 (CF-02): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:239 Task 15 becomes "Depends on: Task 4a, Task 12". P:241 "from Task 4" becomes "from Task 4a".
- **Verifier:** Task 15's closure contains Task 4a.
- **Linked deviation(s):** CF-02
- **Priority:** P2

### Recommendation R-08 (CF-04): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:300 Task 20 becomes "Depends on: Task 6, Task 9, Task 18, Task 19".
- **Verifier:** Task 20's closure covers Tasks 1, 2, 3, 4a, 4b and 5-19.
- **Linked deviation(s):** CF-04
- **Priority:** P2

### Recommendation R-09 (CF-05): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** Apply these nine plan edits (shared by CF-05 and CF-06; the R-INV resolution):
1. Heading 4a. P:84 becomes "## Task 4a: Add routing, gates, records and messages to `conflicts.py`". P:86 stays "Depends on: Task 3". P:88's lead sentence says "the remaining non-resume functions of source section 5.3". P:90 and P:91 stay in 4a.
2. Heading 4b. Insert "## Task 4b: Add the resume planners to `conflicts.py` (after the run-log fold)" after Task 7's last line (P:151) and before "## Task 8" (P:153). It has the line "Depends on: Task 4a, Task 5, Task 7". Add a body sentence saying that 4b extends conflicts.py and sits after Task 7 because its Resume tests build `state` with RunLog.rebuild_state() (IMPL:71 normalizes the heading to T4b; IMPL:75 requires body text). The heading sits under "Phase 3: Changes to the existing core modules" (P:102), and its text names conflicts.py.
3. Split P:92. The crash_resume_plan / conflict_resume_plan bullet moves to 4b.
4. Split P:93. The Router, Gates, Cycle ids, and Record and message cases, plus every listed property (monotonicity, c_initial default row, the Wave 8a Tier 1 column, the merge_parent_ok matrix and disjointness, the evaluate_sync_decision truth tables, branch-literal equality, REPORT_REASONS & HALT_REASONS), stay in 4a. The Resume cases move to 4b. Delete the parenthesis "(resume tests build `state` dicts directly; the run-log integration is Task 8)". 4b builds `state` from RunLog.rebuild_state().
5. Split P:99. The clause `prior_conflict_cycles(["sync-1"], "sync-1") == 0` (a 4a function, P:91) becomes a 4a AC. The conflict_resume_plan directive clause becomes a 4b AC. Add a 4b AC for crash_resume_plan against source section 4.8's second table, because it has no AC today. P:96, P:97 and P:98 stay in 4a.
6. Split P:100. 4a: `uv run pytest tests/pr_submit/test_conflicts_core.py -q`, log ./artifacts/t4a-tests.log. 4b: the same command, log ./artifacts/t4b-tests.log.
7. Re-point edges. P:106 Task 5 "Depends on: Task 4" becomes "Depends on: Task 4a". P:155 Task 8 "Depends on: Task 4, Task 7" becomes "Depends on: Task 4b, Task 7". P:171 Task 9 "Depends on: Task 5, Task 6" becomes "Depends on: Task 4b, Task 5, Task 6".
8. Stale reference. P:241 "from Task 4" becomes "from Task 4a" (the CF-02 and CF-22 edges also name 4a).
9. Task 3 on Task 1 (INV-007). P:66 becomes "Depends on: Task 1, Task 2" (see INV-007).
Resulting document order: 1, 2, 3, 4a, 5, 6, 7, 4b, 8, 9, 10-20. Every edge points to an earlier task, so the graph has no cycle (INV-001). Task 9's closure is {1, 2, 3, 4a, 4b, 5, 6, 7}, which covers the S:744 exports (INV-002). Under /sc:implement the document position is what orders execution (INV-005).
- **Verifier:** `grep -n '^## Task' P` shows "## Task 4b" between "## Task 7" and "## Task 8"; `grep -n 'Task 4\b' P` returns no bare "Task 4"; no Resume test uses a dict literal in place of rebuild_state() output; and each Depends-on target sits above its dependent.
- **Linked deviation(s):** CF-05
- **Priority:** P2

### Recommendation R-10 (CF-06): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** Split Task 4 into 4a (the non-resume functions of source section 5.3 with their tests; depends on Task 3) and 4b (crash_resume_plan, conflict_resume_plan and the Resume tests; after Task 7). The exact edits are items 1 and 3 to 6 of the CF-05 recommendation.
- **Verifier:** the logs ./artifacts/t4a-tests.log and ./artifacts/t4b-tests.log both exist; the Router, Gates, Cycle ids and Record cases are in 4a and the Resume cases are in 4b.
- **Linked deviation(s):** CF-06
- **Priority:** P2

### Recommendation R-11 (CF-10): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** Tasks 10, 11, 14, 15: one literal `grep -cF` per pinned phrase, ascending line numbers for order pins, and forbidden-regex greps with no hits, saved under ./artifacts/.
- **Verifier:** the grep files exist and have the expected counts.
- **Linked deviation(s):** CF-10
- **Priority:** P2

### Recommendation R-12 (CF-13): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:51 Task 2: quote the S:728 clause "plus the two conflict-cycle events `sync_started` and `sync_concluded`" for both docstrings.
- **Verifier:** a grep of the models.py docstrings finds the clause.
- **Linked deviation(s):** CF-13
- **Priority:** P2

### Recommendation R-13 (CF-14): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:53: cite `loop-guard.md:86-103`.
- **Verifier:** n/a (citation fix).
- **Linked deviation(s):** CF-14
- **Priority:** P2

### Recommendation R-14 (CF-15): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:306: add tests/cli/reflect/test_contract_status_cli.py to Task 20's pytest run. The first line of ./artifacts/t20-checks.log reads "make test (VG-2) not run per orchestrator brief".
- **Verifier:** t20-checks.log shows the reflect test passing.
- **Linked deviation(s):** CF-15
- **Priority:** P2

### Recommendation R-15 (CF-17): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:289 Task 19 becomes "Depends on: Task 5, Task 8, Task 11, Task 12, Task 13". The Task 6 and Task 14 edges are optional.
- **Verifier:** Task 19's closure includes Tasks 10-13.
- **Linked deviation(s):** CF-17
- **Priority:** P2

### Recommendation R-16 (CF-18): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:203 and P:213: add tests/pr_submit/test_static_grep.py to the pytest commands of Task 11 and Task 12.
- **Verifier:** the logs include test_skill_forbids_force_push.
- **Linked deviation(s):** CF-18
- **Priority:** P2

### Recommendation R-17 (CF-19): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** Task 13 AC (P:220): C1 to C4 invoke the script with `--evidence-sha` and `--repo` only (no `--pr`); C4 asserts that stderr names the invalid SHA.
- **Verifier:** the C-case argument lists contain no `--pr`.
- **Linked deviation(s):** CF-19
- **Priority:** P2

### Recommendation R-18 (CF-20): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** Task 17 (P:267): the E5 operation-check sentence goes right after Task 1's text ending "so report how many commits it is behind instead)."; E12 rows 3-5 go after the "Behind base branch (create path at L1+, or `--pr`)" row. AC: the final Wave 0 substring equals the full E5 replacement in source section 8.1.
- **Verifier:** the substring check is recorded in the Task 17 evidence.
- **Linked deviation(s):** CF-20
- **Priority:** P2

### Recommendation R-19 (CF-22): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:184 Task 10 becomes "Depends on: Task 3, Task 4a".
- **Verifier:** Task 11 (F10 merge_parent_ok, F12 merge_preflight_ok; S:1388, S:1390), Task 15 and Task 18 (S:1345) all reach Task 4a.
- **Linked deviation(s):** CF-22
- **Priority:** P2

### Recommendation R-20 (INV-007): P2 plan fix

- **File:** .dev/tasks/to-do/TASK-WF-design-20261104-164423/TASK-WF-design-20261104-164423.md
- **Change:** P:66 Task 3 becomes "Depends on: Task 1, Task 2".
- **Verifier:** Task 1 and Task 3 (both edit test_static_grep.py, P:40, P:75) are ordered; Task 18, which also edits the file (P:281), is already ordered after both.
- **Linked deviation(s):** INV-007
- **Priority:** P2
