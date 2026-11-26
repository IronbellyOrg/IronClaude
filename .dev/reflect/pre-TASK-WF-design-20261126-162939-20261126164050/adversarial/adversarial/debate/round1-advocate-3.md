# Round 1 — Advocate for Variant 3 (reviewer 3, refactorer, opus)

Evidence: Read of the cited files, plus three read-only commands (`git ls-files commands/`, `git rev-parse --verify origin/integration`, Grep). No test was run.

## Position summary

V3 is the only card that finds the defects that stop `/sc:implement` partway through: plugin byte-parity (C-008), the `_TRANSIENT` pin (C-009) and the ledger reader that rejects valid ledgers (C-010). It also grades C-002 and C-003 correctly under rule 4. It misses the `skipped` settlement and gets NFR-014 wrong, and V1 is better on both.

## Steelman

**V1.** V1 is the only card that sees that Task 12's closed action list (PLAN:156) cannot write `commit skipped`, which DESIGN:290-291 and REQ:551 require. It is right that NFR-014's "stops rather than wait on a ... prompt" clause (REQ:735) has no task. Its severity labels match its grades on every row, and its 29-id table finds real gaps instead of marking everything covered. Critique: it misses C-008, C-009 and C-010. It read lifecycle lines 775-791 but not the `_TRANSIENT` assertion at 682-688. It grades C-002 and C-003 Medium, although a required exclusion is missing and an acceptance check cannot pass. It also says DESIGN:192 lacks `hooks_path`, but that line lists it.

**V2.** V2 is the only card that treats invariants and named tests as acceptance obligations. It flags I4 (DESIGN:75 "each is tested"), T-21, the field contract (DESIGN:194 `header_len`, `rule`; DESIGN:196 `runs`, `segments`; verified missing from Tasks 6 and 17) and test-first order (DESIGN:458). Its REQ:631 (FR-081 scopes the scan) is the best basis for fixing Task 24. Critique: it checked no existing test (A-002). It misses C-004 and calls FR-109 and NFR-014 covered, which is false. All ten rows are "Blocking" with mixed labels, so its grades don't separate anything. Its claim that the 40-line cap has "no implementation instruction" fails: PLAN:334 cites FR-054 to FR-067, FR-064 holds the cap (REQ:501), and PLAN:19 says to read cited FRs.

## Strengths claimed

1. **C-008, verified.** `test_workflow_command.py:204-220` requires the same file set and the same bytes in src and plugin. Task 26's acceptance runs it straight after editing `SKILL.md`, and Task 27 adds `commit-step.md` to src only. `test_implement_saved_prompt_rule.py:91-96` pins `qa.md`, `ledger.md` and `managed-workspace.md`, which Tasks 30-32 edit.
2. **C-009, verified.** `test_task_workspace_lifecycle.py:682-688` asserts exactly four transient reasons and puts every `E-RESUME-NEEDED reason=` token in retry.md, ledger.md and SKILL.md inside `_TRANSIENT`. Task 31 adds two more, DESIGN 5.4 requires `commit-interrupted`, and DESIGN:411 told the plan to read these pins first.
3. **C-010, verified.** `ledger.md:127` accepts a header as a valid last line. `archive_workspace.py` defines `_HEADER` and `_ARCH`. Task 9 copies only seven patterns, so a header-only legacy ledger raises `LedgerCorrupt`.
4. **C-002 and C-003 graded by the rule.** REQ:475 excludes `.dev/implement/`, and `.gitignore` has no entry for it. Task 24 AC2 cannot pass: a text scan hits five files (`test_safety`, `test_removal`, `test_runner`, `worktree_cleanup_PROVENANCE.md`, `test_launch_level_guard.py:2653`/`2664`), and the allow-listed `worktree_cleanup.py:2642` builds its argv as a list (`["git", "branch", "-d", branch]`), so the scan never matches it.
5. **C-014, NFR-018 (DESIGN:365), and C-016, FR-052 scope** (REQ:409 "tests and .dev/ are not primitives").
6. **Classification.** V3 is the only card that uses Authorized expansion, where it fits (Task 5 `snapshot_lossless`, absent from DESIGN:192). V1 and V2 call ordering bugs and Constraint 29 "Regression". Every Blocking row names the QA verdict it breaks.

## Weaknesses identified in the other variants

1. V2 calls FR-109 covered. No task writes `skipped`, and the plan never contains "mixed-authorization" or "reason=empty" (grep).
2. V2 counts T-14 as covered by Task 19, but Task 19's own acceptance check fails (C-004).
3. V1 marks Task 9 adherent, but it breaks valid ledgers (C-010).
4. V1 grades C-002 and C-003 Medium, against rule 4.
5. V2 grades all ten rows Blocking with mixed labels, and its C-023 instruction claim is refuted by the plan text.

## Concessions

1. I missed the `skipped` settlement (C-011, X-001). V1 is right, and it is Blocking (Missing).
2. I was wrong on NFR-014 (X-002). The plan has only timeouts: grep finds no prompt or `GIT_TERMINAL_PROMPT` rule. DESIGN:431 drops the clause too.
3. X-006: my reasoning was incomplete. PLAN:24 already says to keep plugin copies byte-identical, so Constraint 24 conflicts with Task 38. The finding stands and is stronger: either way the executor breaches quotable text.
4. Row 9 says Blocking but carries the label MEDIUM.
5. C-015 deserved Medium, as V1 graded it, not advisory.
6. I checked only 10 of the 29 ids.

## Shared assumption responses

- **A-001 QUALIFY.** Implement's blocking rule is mechanical (`qa.md:41`, `:45`, `:52`). The review rule matches it for C-001 (a constraint that can be quoted) and for C-003/4/5/8/9 (acceptance checks that cannot pass). For C-002, C-010, C-011 and C-014 the task acceptance checks would pass, so implement would not halt and the defect would ship. Review "Blocking" is the wider set.
- **A-002 ACCEPT.** The plan names these tests itself: Task 26 runs `test_workflow_command.py`, Task 31 runs `-k "implement or ... task_workspace"`, Task 34 says "existing `test_implement_*.py` still pass", and Task 38 runs the full set (PLAN:430).
- **A-003 REJECT.** DD-8 (DESIGN:102) lists exactly the seven patterns behind C-010, and DESIGN:431 shrinks NFR-014 to timeouts. PLAN:19 says "the design wins", so fixing DD-8 in the plan alone is itself quotable against the plan. `source.md` must change, or the plan must record an explicit override.
- **A-004 QUALIFY.** `origin/integration` resolves today (4ce9f14), but the plan cites dozens of drifting line numbers (PLAN:26, 232, 406). A fix should compare against merge-base (C-019) and re-read before editing.

## Per-point table

| point | superior | verified | reason |
|---|---|---|---|
| S-001 | V2 | verified | Coverage and section tables expose disposition |
| S-002 | V3 | verified | Taxonomy used as defined; Authorized expansion fits |
| S-003 | V1 | verified | Grades and labels consistent on all rows |
| C-001 | TIE | verified | All Blocking; `qa.md:52` B4 |
| C-002 | V3 | verified | REQ:475 required; right grade, gitignore evidence |
| C-003 | V3 | verified | Five hits plus list-form argv; V2's REQ:631 aids the fix |
| C-004 | TIE | verified | V1 = V3; `test_routing_refresh.py:492-496` |
| C-005 | TIE | verified | `sc-git.md` tracked, 21 entries |
| C-006 | TIE | verified | V1 = V3 Medium; DESIGN:333, 523 |
| C-007 | TIE | verified | Note, source order |
| C-008 | V3 | verified | `test_workflow_command.py:204-220` |
| C-009 | V3 | verified | lifecycle 682-688 |
| C-010 | V3 | verified | `ledger.md:127`; `_HEADER`/`_ARCH` exist |
| C-011 | V1 | verified | No skip action; DESIGN:290-291 |
| C-012 | TIE | verified (V1 part) | V1 FR-109; V2 T-21/T-04/T-16 |
| C-013 | V1 | verified | Stop clause absent |
| C-014 | V3 | verified | Extra Bash call breaks NFR-018 |
| C-015 | V1 | verified | Medium; Task 15 unbuildable via `validate_argv` |
| C-016 | V3 | verified | REQ:409 primitives only |
| C-017 | TIE | verified | V1 no Task 30 check; V3 `--stat` sums insertions and deletions |
| C-018 | V1 | verified | Seven tokens, "five" |
| C-019 | V1 | verified | Ref resolves; drift risk real |
| C-020 | V2 | verified | DESIGN:458; Blocking overstated |
| C-021 | V2 | verified | I4 untested |
| C-022 | V2 | verified | DESIGN:194, 196 fields unchecked |
| C-023 | V2 | verified | Missing acceptance check is real; "no instruction" false |
| C-024 | V1 | partly | Found real gaps |
| X-001 | V1 | verified | Required behaviour absent |
| X-002 | V1 | verified | V2 and V3 wrong |
| X-003 | V3 | verified | Rule 4 gives Blocking |
| X-004 | V3 | verified | Header-only ledger fails |
| X-005 | NONE | verified | V2 claim half refuted by PLAN:334 plus PLAN:19 |
| X-006 | NONE | verified | V3 reasoning missed PLAN:24 |

