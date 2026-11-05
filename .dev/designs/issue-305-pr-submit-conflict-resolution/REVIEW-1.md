# REVIEW-1: DESIGN.md (issue #305 conflict resolution)

Verdict: FAIL (3 BLOCKING, 14 MINOR)

## Summary

The design is well grounded. Of the more than 40 `file:line` and behaviour claims spot-checked in sections 3, 6 and 12.2, all hold except one citation that has shifted by a few lines. The event count of 41 and every site where it is stated or pinned are correct. The 74-row research map matches `03-roi-scored-list.md` ID for ID and score for score, in order, with 69 adopted and 5 rejected. The binding scope (Precursor + P0 + P1 + P2 dark, P3 out) is respected: no `merge_state` field and no second Wave 8a trigger leak in. No planned text trips the force-push regex. No planned `gh` line lacks `--repo` or a `repos/` path. No stash appears anywhere, and `push_parent_ok` and `evaluate_push_decision` are left untouched.

Three problems block implementation as written:

- **B1:** the ordinal-monotonicity property that section 12.1 pins contradicts the routing table, so the planned test cannot pass.
- **B2:** crash-recovered conflict pushes never close their conflict cycle. A later `--resume` in the same run can then be routed by the stale open cycle, which skips a later crash window.
- **B3:** the resume restart directives cannot call the router or the push builder, because the Wave 8 entering outcome is never recorded for a cycle that has no push record.

## BLOCKING findings

| ID | Section | Finding | Evidence (file:line) | Required fix |
|---|---|---|---|---|
| B1 | 4.4, 12.1 | **The ordinal-monotonicity property contradicts the router table.** Two cases break it.<br>(1) `wave8a`, Tier 1, with a preserved terminal `P`, cap >= 1, under cap: L1 gives `propose` (rank 2) and L2 gives `report` / `tier1_l2_preserved` (rank 1), so rank(L1) > rank(L2).<br>(2) `c_initial`: the domain guard sends L1 and L2 to the default `halt` (rank 1), while L3 Tier 0 and Tier 1 give `none` (rank 0).<br>Section 12.1 requires the property "over the full input product (hooks x tiers x ordinals x entering ...)", so that test fails against the table section 4.4 specifies. INV-010 / OQ-21 relies on this property. | DESIGN.md:228-229 (L1 propose with no `P` condition; L2+`P` report), :236 (rank order and property), :190 (guard: `c_initial` at an ordinal other than 3 goes to the default row), :211-212 (`c_initial` Tier 0/1 give `none`), :1221 (property test over all hooks) | Choose one rule and state it: (a) at L1 with `P`, Tier 1 returns `report` (`tier1_l1_preserved`); or (b) state the property exactly, excluding `c_initial` (its domain is L3 only) and the `P`-preserved rows. Then make the 12.1 test match. |
| B2 | 4.8, 6.3, 6.4 | **Crash-recovered conflict pushes never append `sync_concluded`, so the cycle stays open.** The fold opens a cycle on `sync_started` and closes it only on `sync_concluded`. Section 4.8 appends `sync_concluded{pushed}` only on the `complete_after_push` row. It appends none after `crash_window` -> `resolve_crash_window_plan`, either after Branch A (where `resolve_crash_window` appends a recovered `push_completed`) or after the Branch B re-drive. `open_conflict_cycle` therefore stays set for the rest of the run, and `sync_outcome` is wrong.<br>On any later `--resume` in the same run (for example a crash during a later fix-cycle push), `conflict_resume_plan` row 4 ("the open cycle has a `push_completed`") matches before row 2 and row 4b. The run then resumes at S5a for the old merge cycle, or at the CI wait for the old sync cycle. It never settles the fix push's dangling `push_initiated` through the three-way remote check. | DESIGN.md:328-329 (rows 4 and 4b), :337-345 (crash plan has no `sync_concluded`), :599-604 (fold opens/pops only on `sync_started` / `sync_concluded`); recovery.py:112-120 (Branch A appends `push_completed` only) | Every crash-plan directive for kinds `sync` and `merge` must append `sync_concluded{pushed, merge_sha}`: Branch A right after the recovered `push_completed`, and Branch B after the re-driven push lands. Alternatively, row 4 must apply only when no later `push_initiated` with a different key exists. Add a test: a conflict crash window recovered, then a later fix-push crash window, resumes into the fix crash window. |
| B3 | 4.7, 4.8 | **The resume restart directives lack an input they need.** Rows 5 (`abort_and_restart`) and 7 (`restart`) restart the cycle "at step 1". At Wave 8a, step 2 calls `conflict_action(hook="wave8a", entering=...)`, and step 11 passes `review_terminal` to `build_push_triad`. Both need the Wave 8 entering outcome. The `sync_started` payload does not record it, and no push record exists in these rows, so the value has no defined source. The router's domain guard would turn every such restart into `router_unreachable`. That fails closed, but it contradicts the stated restart behaviour. | DESIGN.md:282 (`sync_started` payload: no `review_terminal` / `entering`), :330, :332 (restart rows), :261, :270 (router call and triad need it), :190 (guard on `entering`) | Add `review_terminal` (the Wave 8 entering outcome, null at `c_initial`) to the `sync_started` payload and to the fold's open-cycle entry. Make rows 5 and 7 read it, and halt `resume_unrepresentable` when it is missing. Add a test row. |

## MINOR findings

- **M1 (10.1 OQ-8):** labelled "(Spec)", but the spec recommends "Probe at run time like the CI preflight" (merged-requirements.md:861), while the design adopts "No capability probe". This is a departure; mark it "Changed" and give the reason.
- **M2 (6.3):** spec FR-16 names the state key `sync_cycles` (merged-requirements.md:641, :428); the design uses `conflict_cycles` with no section 10 entry. Record the rename.
- **M3 (12):** the FR-19 acceptance criterion "a report-contract test shows pushes-by-kind can be reconstructed from the report (QA-2)" (merged-requirements.md:644) has no test in section 12. Add one.
- **M4 (12):** the FR-27 acceptance criterion "a merge left in progress and GitHub reading `MERGEABLE` halts before any fix cycle" (merged-requirements.md:652) has no named test. P7 covers only the script; `conflict_resume_plan` row 3 covers only resume.
- **M5 (12.2):** FR-31's acceptance criterion says `test_static_grep.py:649-657` stays unchanged (merged-requirements.md:656). The design rewrites the comment at :654-655 (DESIGN.md:1236). The assertions are kept, so only the letter of the criterion is broken. Keep the comment, or note the deviation.
- **M6 (4.6 step 12):** the rejected-push record `push_aborted_or_not_landed{rejected, stderr_tail}` does not say it carries `idempotency_key`. `detect_crash_window` skips events without a key (recovery.py:66-68), and `test_rejected_push_record_is_not_a_crash_window` (DESIGN.md:1239) depends on it. State that the record copies the triad's key and common fields.
- **M7 (7.2 vs 4.6):** `finish-merge.sh --precheck` usage requires `--manifest` and `--merge-tree-oid` (DESIGN.md:710), but step 9 is where the manifest is written (:268), after the step 5 precheck (:264). Either make `--manifest` optional in precheck mode or write the manifest at step 5.
- **M8 (5.3):** `crash_resume_plan` takes "`branch` one of `recovery.BRANCH_*`" (DESIGN.md:519). `conflicts.py` cannot import `recovery`, because `recovery` imports `conflicts`, and the allowed-import list (:351) excludes it. State that the three literal values `landed` / `not_landed` / `ambiguous` are compared by string, and pin their equality in a test.
- **M9 (5.2, 9):** `REPORT_REASONS` and `HALT_REASONS` are "every non-halt / every halt reason of section 9". `tier_above_cap`, `conflict_tier3`, `probe_failed`, `merge_tree_unsupported` and `github_disagrees` appear on both lists (DESIGN.md:1007-1011, :1028). Say whether the sets may overlap.
- **M10 (8.1):** the head-binding HALT message at SKILL.md:268 still says "a branch Wave 0 rebased needs a force-push". After the Precursor this cannot happen: head binding is L1+ only, and L1+ no longer rebases. The design does not edit this line. Note it, or reword it without changing the line count.
- **M11 (11):** R-54 (show both sides), R-56 (show both pinned submodule SHAs) and R-57 (file type and size) are marked "Adopt", but the Tier 3 template (DESIGN.md:892) shows only path and class, and at Wave 0 it omits the side sentences. Mark them "Adopt (partial)", or add the SHAs and size to the template.
- **M12 (7.1):** the probe CLI departs from spec 5.3 (merged-requirements.md:347: `--pr`, `--head-branch`). The design drops both and adds `--program` and `--ops-only`. Section 10.4 note 3 justifies only the output change; add the CLI change.
- **M13 (12.2):** the citation "pins at `test_ci_classify.py:36-42`" points at `test_classify_empty` / `test_classify_empty_polling_is_not_clean`, which sit at :35-41. The claim is true; the line numbers are slightly off.
- **M14 (11 row 57):** `pr_branch_ok` is cited at `fsm.py:525`, which is the `_BAD_BRANCH_NAMES` line; the definition is at :528. The claim is true.

## Self-Audit

What was checked, with evidence read in this session:

1. **Code claims (sections 3, 6, 12.2), more than 40 spot-checks.**
   - `fsm.py`: :36, 50-70, 73-99, 102-134, 173-219, 227-235, 238-288 (common 259-267, predicates 273-279), 453-474 (`run_validation_gates`, needed by `conflict_validation_status`), 525-552, 582-600, 603-610, 716-802 (findings 741-748, pre-gate 729-731, unknown edge 801-802), 1118-1124, 1137.
   - Other modules: `ci.py` 22-46; `models.py` 3-7, 22-90 (exactly 41 members); `run_log.py` 27-35, 108-131 (:111 "41"), 161-260 (198-206, 238-241); `recovery.py` 57-80, 83-171 (tuple 98-110); `__init__.py` 1-108.
   - `SKILL.md`: :4, 218, 220-223, 236, 239, 250, 254-267, 268, 269, 274, 275, 277, 305, 315. All E5, E7, E8 and E9 a-e old substrings exist verbatim.
   - `poll-ci-checks.sh`: 1-14, 22-28, 31-36, 39-43, 64-78.
   - Refs: `state-machine.md` 104, 144-146, 161-179; `ci-poll.md` 21, 28-29; `loop-guard.md` 86-88.
   - `commands/pr-submit.md`: 8, 9, Options table, Will Not.
   - Tests: `test_static_grep.py` 37-51, 103-129, 132-143, 650-661, 689, 694-698, 746-755, 758-776; `test_run_log.py` 165-169, 204; `test_codex_reviews.py` 441, 489, 688; `test_cosmos_protocol.py` 36; `test_idempotency.py` 89; `test_edge_cases.py` 267; `test_ci_classify.py` 20-70; `test_pre_pr_checks.py` 201-230; `test_auggie_fallback.py` 353-379; `test_crash_recovery.py` 263/310/344; `test_augment_review_remediation.py` 145; `test_cli_install.py` 248-262, 496-500; `conftest.py` 117-139, 184-196; `test_impact_command.py` 327-345.
   - Repo files: `.gitignore` 169, 222; `.pre-commit-config.yaml` 19; `pyproject.toml` 7; `CHANGELOG.md` 5.
2. **Internal consistency.**
   - Router rows against sections 4.5, 4.6, 7, 9 and 12, including the monotonicity property (B1).
   - Counting rules (`push_count`, `sync_push_count`, `round_counter`, `rereview_request_count`) are consistent across sections 4.7, 8.1 E3, 8.4 and 15.
   - L0 has no hook; L1 proposes or reports; L2 never commits; L3 pushes.
   - The SKILL.md line budget sums to +15, with one python block.
3. **Safety.**
   - The force regex was run mentally against every planned `git push` line and every prohibition sentence; no hit.
   - The FR-21 regexes were checked against the planned prose (for example, "git configuration" does not match `\bgit\s+config\b`).
   - Every planned `gh` line is `--repo` / `repos/`-scoped.
   - No stash; no hook skip; no new parent loosening (`merge_parent_ok` is disjoint from `push_parent_ok`).
   - Resume paths were traced; B2 and B3 came from this.
4. **Completeness.**
   - The 74 IDs and scores were diffed mechanically: identical, 74 rows, 5 rejected.
   - FR-1 to FR-33 and NFR-1 to NFR-14 of the spec were walked against the design (M1-M5, M12).
5. **Implementability.** Every referenced function, script flag, reason code and fixture was traced to a definition (M6-M9).
6. **Scope.** No P3 item is present. The Precursor, P0, P1 and P2 deliverables are all present, with the default cap of 1.
