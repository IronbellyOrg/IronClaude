## Advocate: Variant 1 (sonnet:analyzer)

Path shorthand: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R06 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`.

### Position Summary
Variant 1 is the best-grounded card on citations and external-claim checking, but its "no blocking defect" verdict was too lenient, so I concede the three defects it under-rated or never examined: the unreviewed `--remediate` edits (X-001), the AC-14 test gap (X-006) and the AC-6 test gap (X-007). The lint-gate contradiction (X-008) is real in the text and blocking only if the tree is not already lint-clean (A-004). Everything else Variant 1 raised (R1-001, R1-003, R1-004, R1-005) stands as minor.

### Steelman: Variant 2
Variant 2 (qa, haiku, 0.85) did the one thing the other cards did not: it turned the 25 acceptance criteria into atomic units and asked, for each, which item implements it, which writes the test and which runs it (U-001, U-002). That is the right unit for a pre-execution audit, because a task file fails by leaving a criterion untested, not by mis-citing a line. Its two findings, R2-001 (Step 6.7 FR-011 cases cover closed, assignee, timeout and budget but not lost-label, voided-approval or changed-Project-status re-reads, TF:475) and R2-002 (Step 6.6's AC-14 test injects no append or save failure into `run_cycle`, TF:472), are grounded in text I re-read and match the cited lines. It also declined to accept lexical matches as proof of coverage. Its weaknesses (markdown instead of the requested YAML, a MEDIUM label outside the binary scale) are format faults, not accuracy faults.

### Steelman: Variant 3
Variant 3 (refactorer, opus, 0.85) read the widest slice (INF-105..INF-157) and was the only card to check the commit and gate machinery as a state sequence, which is where the real hazards sit. R3-001 is correct: the POST reflect runs `--remediate` (TF:860-870, "apply the remediations the skill offers under `--remediate`") after the single checkpoint commit authorised by DF-07 (R06:30), and Step 10.7 stages only `.dev/tasks` (TF:875), so source or test edits made by remediation are neither gated nor committed and the task still ends Done. R3-002 is correct on the text: Step 7.8 requires exit 0 (TF:517) while saying a finding in an untouched file is "recorded and NOT fixed", so a dirty baseline leaves no passing path and no halt rule. It also found that several automatic "none" requirement mappings were wrong and showed the items exist (X-009), and it respected declared deviations (DF-05, DF-09, DF-10, DF-29, DF-55). Its minor findings are all true to the text.

### Key Strengths Claimed
- Citation grounding: every Variant 1 finding cites text that exists at or near the cited line, so none is dropped (re-read TF:330, 336, 460, 848, 851, 860-875).
- External-claim verification (U-004): more than 12 claims about real files (`install_user_setup.py`, `main.py`, `swarm/atomic.py`, `Makefile`, `.pre-commit-config.yaml`) were checked rather than assumed.
- Correct T-2 reading: Step 4.1c defines `backoff_elapsed(entry, now)` without the `attempts` < 3 conjunct (TF:336) while D:479 puts the conjunct in the T-2 row; Variant 1 saw both and correctly classified the gap as minor because Step 6.2 applies the cap (TF:460).
- Honest scope disclosure: Variant 1 listed what it did not read (Phases 1-3, Gates A-D, Final and M4 items, research/06).
- Declared deviations were not reported as defects.

### Weaknesses in Variant 2
- The MEDIUM label sits outside the binary scale (S-003) and the card is markdown, not the requested YAML (S-001), so it cannot be merged mechanically.
- It treats X-001 as a non-defect on the strength of "the checkpoint sequence captures BASE before the single commit ... halts on commit/hook failure". That sequence handles commit failure; it says nothing about edits made after the commit by `--remediate`, which is the actual hazard (TF:866, 875).
- It marks INF-124 covered without noting the "exit 0" against "NOT fixed" contradiction (TF:517).
- It reports AC-14 and AC-6 as partially covered but labels them MEDIUM; under the binary rule, "a required behaviour untested" is blocking, so its own evidence supports a stronger label than it gave.
- It does not address T-2 or the withdrawn-commit branch.

### Weaknesses in Variant 3
- R3-003 (no attempt cap on "re-run until PASSED", TF:351, 387) is a loop-design weakness; no command is impossible and a worker can still stop. Minor.
- R3-006 (marker test reads installed `~/.claude` copies) is arguably a declared reading: the test is read-only and only runs if the copies are present (TF:384), and D:791 says "dual surface".
- R3-005 is a true but small design-table departure (TF:330 against D 5.3); it does not break behaviour.
- R3-002 is conditional on A-004, which Variant 3 assumed rather than measured. It did not run or cite a baseline lint result.
- It read neither Gate D nor the bodies of 9.M4-9.M13, so its "covered" rows on the final gates carry less weight (C-011).
- It rates X-006 covered ("audit line on every exit") without finding that no test injects an append or save failure (TF:472).

### Concessions
- X-001: conceded to Variant 3. My R1-002 found the same defect and called it minor. The task can end Done with a working tree that differs from both the commit and the gated tree, so blocking is the better-supported label.
- X-006 and X-007: conceded to Variant 2. Variant 1 never examined AC-14 or AC-6. TF:472 and TF:475 show the test cases that the criteria need are missing.
- X-008: conceded conditionally to Variant 3. The contradiction is in the text (TF:517); it bites only if the tree is not lint-clean. The fix is cheap (a baseline item).
- Variant 1's overall "no blocking defect" verdict (C-010) was too lenient.
- Variant 1 did not read Phases 1-3, Gates A-D, the Final and M4 items or research/06, and the Final-gate range (TF:737-835) was not read in this round either. Its many "not re-read in detail" coverage rows deserve less weight (C-011).
- X-009: Variant 3's mapping corrections are right.
- C-004 to C-009 (Variant 3's minor findings) are true; I concede them to Variant 3 as findings Variant 1 missed.

### Shared Assumption Responses
- A-001: ACCEPT. My spot reads of TF:330, 336, 460, 472, 475, 502, 520, 848, 860-875 matched the cited text; the file was not edited in the interval I observed.
- A-002: ACCEPT. TF:866 tells the worker to apply the remediations the skill offers under `--remediate`, so source and test edits outside `.dev/tasks` are possible.
- A-003: QUALIFY. Item text is dense and Step 9.17 and the Final lenses are backstops, but a scenario no item names is not guaranteed to be written, so a missing test case is a legitimate pre-execution finding.
- A-004: QUALIFY. The lint-clean baseline is unverified by any card; if the tree is not clean, the full-tree lint gates have no passing path. The risk is conditional and the fix is a cheap baseline item.

### Point Positions
| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | MARKDOWN | | brief: output file format "(markdown)"; the merged register is read by humans and the orchestrator, and Variant 2 already used tables | |
| S-002 | UNION | | Variant 2's AC units catch test gaps (TF:472, 475); Variant 1/3 INF rows catch item-level gaps (TF:336, 517) | |
| S-003 | BINARY | | advocate-brief.md:18 - "Binary severity (decide from evidence, not from the reviewer's label)" | |
| S-004 | ENUM | | advocate-brief.md:35 - "ENUM (coverage_gap/contradiction/unexecutable_item/wrong_citation/gate_weakness/sequencing/other)" | |
| C-001 | VALID-MINOR | | TF:848 - "over a base the owner names instead of `plans/base-sha.txt`" | |
| C-002 | VALID-MINOR | | Step 8.10 says "exactly as test.yml:29"; the mechanism differs (`uv pip install` in CI against `uv run --offline --with` in the gate); the gate still runs xdist | |
| C-003 | VALID-MINOR | | TF:851 - `git diff --exit-code pyproject.toml Makefile` sees only unstaged changes; the P10 allowlist check catches staged ones later | |
| C-004 | VALID-MINOR | | TF:351 and TF:387 - per-phase G-1 runs say "re-run until PASSED" with no attempt cap; no impossible command | V3 (partial) |
| C-005 | VALID-MINOR | | Variant 3 R3-004: final-change-set.md written once in 9.F1; a stale list is caught by the allowlist at P10 | V3 (partial) |
| C-006 | VALID-MINOR | | TF:330 - Step 4.1a lets `record` import `parse_utc`, `format_utc`, `valid_issue_number` from `predicates`; D 5.3 allows types only | V3 |
| C-007 | VALID-MINOR | | TF:384 - the marker test reads the installed `~/.claude` copies read-only, only if present | V3 |
| C-008 | VALID-MINOR | | TF:502 requires the main.py diff to be only the added lines; TF:520 runs pinned ruff format on all of main.py | V3 |
| C-009 | VALID-MINOR | | TF:875 - "a failure of this staging command is logged ... and never reverts the Done status" | V3 |
| C-010 | OTHER | Blocking: R3-001 (X-001), R2-001 (X-007), R2-002 (X-006); R3-002 conditional on A-004. All others minor | TF:866, 472, 475, 517; no card is right on every count | |
| C-011 | YES | | Variant 1 "not re-read in detail" rows; Variant 3 did not read Gate D (619-672) or 9.M4-9.M13 bodies | |
| X-001 | VALID-BLOCKING | | TF:866 "apply the remediations the skill offers under `--remediate`"; TF:875 stages `.dev/tasks` only; R06:30 allows one commit before POST | V3 |
| X-002 | VALID-MINOR | partially_covered | D:479 "now >= `updated_at` + 10 min and `attempts` < 3"; TF:336 `backoff_elapsed(entry, now)` without it; TF:460 applies attempts < 3 in the cycle | |
| X-003 | partially_covered | | R06:28 - DF-05: "Locally run the named affected subset ... The final-gate item records "full suite: CI only"." | |
| X-004 | partially_covered | | R06:28 - DF-05 replaces `make test` locally with the affected subset; section 13 gates are met in part | |
| X-005 | partially_covered | | Variant 1 card INF-016 row: only NG-2 has an explicit guard (argv scan); NG-1, 3, 4, 5 are guarded by absence | |
| X-006 | VALID-BLOCKING | INF-146 partially_covered | TF:472 - Step 6.6's AC-14 test has no append or save failure injection into `run_cycle` | V2 |
| X-007 | VALID-BLOCKING | AC-6 partially_covered | TF:475 - Step 6.7 FR-011 cases cover closed, assignee, timeout and budget; no lost-label, voided-approval or Project-status cases | V2 |
| X-008 | VALID-BLOCKING (conditional on A-004) | | TF:517 - "exit 0 required"; "a finding in a file this task did not touch is recorded and NOT fixed" | V3 |
| X-009 | YES | | Variant 3 corrections (INF-108, INF-122, INF-135, INF-147, INF-153) point to items that exist | V3 |
| A-001 | ACCEPT | | TF:330, 336, 460, 472, 475, 848, 860-875 matched the cited text on re-read | |
| A-002 | ACCEPT | | TF:866 - "apply the remediations the skill offers under `--remediate`" | |
| A-003 | QUALIFY | | Step 9.17 and Final lenses back-stop but do not guarantee an unnamed scenario is written | |
| A-004 | QUALIFY | | TF:517 "exit 0" gate with no baseline item; no card measured lint status | |
