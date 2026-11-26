# Re-review findings (reviewer 2, qa, haiku class)

**Verdict (reviewer): FAIL, one blocking regression introduced by the M-10 repair.** `P` = `.dev/tasks/to-do/TASK-WF-design-20261126-180705/TASK-WF-design-20261126-180705.md`; `D` = `.dev/tasks/to-do/TASK-WF-design-20261126-180705/source.md`; `R` = `.dev/brainstorms/20261126-115614-git-pm-workflows-skills/merged-requirements.md` (paths shortened by the orchestrator).

## Prior blockers

"Resolved" means the required plan repair is present, not that the future implementation or tests passed.

| ID | Status | Evidence in the regenerated plan |
|---|---|---|
| M-01 | resolved | P:30 permits forbidden tokens in deny-lists, refusal text and refusal tests while banning their execution or recommendation. |
| M-02 | resolved | P:234-247 moves both the S23 change and the routing-test run to Task 20, after creation of the skill file. |
| M-03 | resolved | P:284-288 restricts the deletion scan to this work's files and removes the impossible repository-wide "only file" assertion. |
| M-04 | resolved | P:294-297 uses filesystem absence and a work-tree file count. |
| M-05 | resolved | P:306-369 assigns implement-side plugin copies and comparisons to Tasks 26-32 before their relevant parity tests. |
| M-06 | resolved | P:316, 356-359 puts the two transient reasons in the new commit-step reference and excludes their reason-code forms from the three files scanned by the existing test. |
| M-07 | resolved | P:306-309, 350, 356-369 includes the severity test in the affected checks and adds the archive-gate allow-list entry, override recorded at P:20. |
| M-08 | resolved | P:38-41, 128-132 adds all nine patterns, header-only and archive-tail cases, expanded fixture grammar; P:20 records the DD-8 override. |
| M-09 | resolved | P:158-161, 216, 336-339 adds `record-skipped`, both reconciliation cases and the procedure's empty/mixed settlement rule. |
| M-10 | regressed | T-04 refusal/no-retry assertions and resolution recovery checks are added at P:192-195, 225, 329, 386, but P:326 changes the required no-key reply rule into unconditional rejection, and the new acceptance checks preserve that wrong rule. |
| M-11 | resolved | P:170-176, 182-185 adds the legacy-run-folder exclusion and explicit path-mode and ledger-mode cases. |

## Deviations

| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| R2-01 | Regression | P:326 | Blocking (Decision): owner resolution rejects a valid reply after disclosure of exactly one boundary. Task 28 says "a reply that carries no key is not a resolution and the STOP is shown again." The design explicitly allows a reply without a key when exactly one key was displayed; after disclosure of one boundary an otherwise valid "abandon this boundary" reply must be eligible for resolution, while the plan requires rejection. Task 28's acceptance and Task 34's static check would preserve the incorrect behavior. Affected actions: owner settlement, subsequent resume, the T-21 acceptance checks. The repair needs two acceptance cases: a qualifying reply without a key is accepted after one displayed boundary and rejected as ambiguous after several. | D:387 permits the single-displayed-key exception; P:326 removes it; P:329, 386 require checks of the resulting "no-key rule"; D:547 asks for coverage of the rule, not a redefinition. | HIGH |

## Disposition of the 26 unnamed IDs

- Inactive or deleted, no task needed: FR-024 to FR-029, FR-083 to FR-089, FR-119 (no active definition); FR-068 and FR-069 (R:520 deletes them in favour of the sidecar); FR-037 is an inactive historical id (R:254 is a provenance comment; the active submodule-default protection rule is R:257, implemented by Task 5, P:83).
- Covered by a task: FR-015 and FR-016 (Tasks 25, 26-32, 35, 38); NFR-004 (Tasks 20, 24); NFR-011 (Tasks 3 and 5; the version claim stays UNVERIFIED at P:87); NFR-016 (Tasks 5, 14, 20, 26, 27); T-14 (Tasks 19, 20, 25, 26-33, 35, 36); T-18 (Tasks 1 and 38).
- Real acceptance-coverage gap, carried forward as non-blocking (first-run M-27): NFR-013, no check that every refusal reports whether HEAD, index and work tree changed (R:734); Tasks 15, 18, 20 cover outcome fields and schemas but not that (P:195, 225-226, 247-248).
- NFR-015: covered by the design and the assigned behavior of Tasks 4, 20, 21, 27, 29; R:736 requires the spec to document the trust boundary (D:134, 186, 380); a missing duplicate statement in an installed file is not by itself a missing deliverable.

## Adherence summary

- Plan inspected: all 38 tasks and the Constraints block against the design body.
- Prior blocking repairs: 10 resolved, 1 regressed. Unnamed-ID dispositions: 17 inactive/deleted/historical, 8 covered, 1 carried-forward non-blocking acceptance gap.
- New or still-blocking deviation classes: Authorized expansion 0, Necessary 0, Drift 0, Regression 1.
- Fully adherent across every atomic requirement: UNVERIFIED.

## Notes

- The coverage slice's statement that FR-037 is an active unnamed requirement is misleading (its named occurrence is provenance; the behavior belongs to active FR-013), so the inactive count is 17, not 16.
- The new T-04 static assertions and the crash-after-resolution idempotency assertions are present; M-10 is marked regressed rather than unfixed because its no-key repair changes the required outcome.
- Prior Medium and Note findings were not reopened as blockers; the DD-11 decision stays explicitly pending at P:158. No tests were run; runtime behavior and the real hook framework remain UNVERIFIED.

