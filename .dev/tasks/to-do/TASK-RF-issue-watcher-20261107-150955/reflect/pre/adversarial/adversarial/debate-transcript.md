# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus the Round 2.5 invariant probe)
- Convergence achieved: 100% (28/28 diff points agreed)
- Convergence threshold: 80%
- Convergence status: BLOCKED_BY_INVARIANTS (3 HIGH-severity UNADDRESSED invariants; see invariant-probe.md)
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (v1 sonnet:analyzer, v2 haiku:qa, v3 opus:refactorer)
- Advocate brief: advocate-brief.md (binary severity rule, authority rule, verdict tokens)
- Round 1: parallel, all three advocates. Round 2: sequential in input order (v1, then v2, then v3), each advocate given the earlier rebuttals.
- The orchestrator took no position. Each advocate's text below is its own output, reproduced verbatim from the round files.

## Round 1

The three Round 1 statements follow, reproduced verbatim from round1-advocate-v1.md, round1-advocate-v2.md and round1-advocate-v3.md. Each has a Position Summary, Steelman, Key Strengths, Weaknesses, Concessions, Shared Assumption Responses and Point Positions.


### Advocate v1 (Round 1, verbatim from round1-advocate-v1.md)

#### Advocate: Variant 1 (sonnet:analyzer)

Path shorthand: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R06 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`.

##### Position Summary
Variant 1 is the best-grounded card on citations and external-claim checking, but its "no blocking defect" verdict was too lenient, so I concede the three defects it under-rated or never examined: the unreviewed `--remediate` edits (X-001), the AC-14 test gap (X-006) and the AC-6 test gap (X-007). The lint-gate contradiction (X-008) is real in the text and blocking only if the tree is not already lint-clean (A-004). Everything else Variant 1 raised (R1-001, R1-003, R1-004, R1-005) stands as minor.

##### Steelman: Variant 2
Variant 2 (qa, haiku, 0.85) did the one thing the other cards did not: it turned the 25 acceptance criteria into atomic units and asked, for each, which item implements it, which writes the test and which runs it (U-001, U-002). That is the right unit for a pre-execution audit, because a task file fails by leaving a criterion untested, not by mis-citing a line. Its two findings, R2-001 (Step 6.7 FR-011 cases cover closed, assignee, timeout and budget but not lost-label, voided-approval or changed-Project-status re-reads, TF:475) and R2-002 (Step 6.6's AC-14 test injects no append or save failure into `run_cycle`, TF:472), are grounded in text I re-read and match the cited lines. It also declined to accept lexical matches as proof of coverage. Its weaknesses (markdown instead of the requested YAML, a MEDIUM label outside the binary scale) are format faults, not accuracy faults.

##### Steelman: Variant 3
Variant 3 (refactorer, opus, 0.85) read the widest slice (INF-105..INF-157) and was the only card to check the commit and gate machinery as a state sequence, which is where the real hazards sit. R3-001 is correct: the POST reflect runs `--remediate` (TF:860-870, "apply the remediations the skill offers under `--remediate`") after the single checkpoint commit authorised by DF-07 (R06:30), and Step 10.7 stages only `.dev/tasks` (TF:875), so source or test edits made by remediation are neither gated nor committed and the task still ends Done. R3-002 is correct on the text: Step 7.8 requires exit 0 (TF:517) while saying a finding in an untouched file is "recorded and NOT fixed", so a dirty baseline leaves no passing path and no halt rule. It also found that several automatic "none" requirement mappings were wrong and showed the items exist (X-009), and it respected declared deviations (DF-05, DF-09, DF-10, DF-29, DF-55). Its minor findings are all true to the text.

##### Key Strengths Claimed
- Citation grounding: every Variant 1 finding cites text that exists at or near the cited line, so none is dropped (re-read TF:330, 336, 460, 848, 851, 860-875).
- External-claim verification (U-004): more than 12 claims about real files (`install_user_setup.py`, `main.py`, `swarm/atomic.py`, `Makefile`, `.pre-commit-config.yaml`) were checked rather than assumed.
- Correct T-2 reading: Step 4.1c defines `backoff_elapsed(entry, now)` without the `attempts` < 3 conjunct (TF:336) while D:479 puts the conjunct in the T-2 row; Variant 1 saw both and correctly classified the gap as minor because Step 6.2 applies the cap (TF:460).
- Honest scope disclosure: Variant 1 listed what it did not read (Phases 1-3, Gates A-D, Final and M4 items, research/06).
- Declared deviations were not reported as defects.

##### Weaknesses in Variant 2
- The MEDIUM label sits outside the binary scale (S-003) and the card is markdown, not the requested YAML (S-001), so it cannot be merged mechanically.
- It treats X-001 as a non-defect on the strength of "the checkpoint sequence captures BASE before the single commit ... halts on commit/hook failure". That sequence handles commit failure; it says nothing about edits made after the commit by `--remediate`, which is the actual hazard (TF:866, 875).
- It marks INF-124 covered without noting the "exit 0" against "NOT fixed" contradiction (TF:517).
- It reports AC-14 and AC-6 as partially covered but labels them MEDIUM; under the binary rule, "a required behaviour untested" is blocking, so its own evidence supports a stronger label than it gave.
- It does not address T-2 or the withdrawn-commit branch.

##### Weaknesses in Variant 3
- R3-003 (no attempt cap on "re-run until PASSED", TF:351, 387) is a loop-design weakness; no command is impossible and a worker can still stop. Minor.
- R3-006 (marker test reads installed `~/.claude` copies) is arguably a declared reading: the test is read-only and only runs if the copies are present (TF:384), and D:791 says "dual surface".
- R3-005 is a true but small design-table departure (TF:330 against D 5.3); it does not break behaviour.
- R3-002 is conditional on A-004, which Variant 3 assumed rather than measured. It did not run or cite a baseline lint result.
- It read neither Gate D nor the bodies of 9.M4-9.M13, so its "covered" rows on the final gates carry less weight (C-011).
- It rates X-006 covered ("audit line on every exit") without finding that no test injects an append or save failure (TF:472).

##### Concessions
- X-001: conceded to Variant 3. My R1-002 found the same defect and called it minor. The task can end Done with a working tree that differs from both the commit and the gated tree, so blocking is the better-supported label.
- X-006 and X-007: conceded to Variant 2. Variant 1 never examined AC-14 or AC-6. TF:472 and TF:475 show the test cases that the criteria need are missing.
- X-008: conceded conditionally to Variant 3. The contradiction is in the text (TF:517); it bites only if the tree is not lint-clean. The fix is cheap (a baseline item).
- Variant 1's overall "no blocking defect" verdict (C-010) was too lenient.
- Variant 1 did not read Phases 1-3, Gates A-D, the Final and M4 items or research/06, and the Final-gate range (TF:737-835) was not read in this round either. Its many "not re-read in detail" coverage rows deserve less weight (C-011).
- X-009: Variant 3's mapping corrections are right.
- C-004 to C-009 (Variant 3's minor findings) are true; I concede them to Variant 3 as findings Variant 1 missed.

##### Shared Assumption Responses
- A-001: ACCEPT. My spot reads of TF:330, 336, 460, 472, 475, 502, 520, 848, 860-875 matched the cited text; the file was not edited in the interval I observed.
- A-002: ACCEPT. TF:866 tells the worker to apply the remediations the skill offers under `--remediate`, so source and test edits outside `.dev/tasks` are possible.
- A-003: QUALIFY. Item text is dense and Step 9.17 and the Final lenses are backstops, but a scenario no item names is not guaranteed to be written, so a missing test case is a legitimate pre-execution finding.
- A-004: QUALIFY. The lint-clean baseline is unverified by any card; if the tree is not clean, the full-tree lint gates have no passing path. The risk is conditional and the fix is a cheap baseline item.

##### Point Positions
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

### Advocate v2 (Round 1, verbatim from round1-advocate-v2.md)

#### Advocate: Variant 2 (haiku:qa)

##### Position Summary

Variant 2 supplies the strongest scenario-level coverage analysis: its two findings distinguish implementation instructions and helper tests from tests that would detect broken integration, rather than treating directory-wide execution as proof (V2:16–19, 34–51). The merged verdict should nevertheless be OTHER: retain those two planned-test-writing gaps, incorporate the verified sequencing and constraint conflicts below, and do not count authorized substitutions as defects. Blocking here describes deficient task instructions, sometimes on an explicitly identified conditional path—not observed implementation failures or an observed lint-dirty baseline; no commands or tests were run.

##### Steelman: Variant 1

Variant 1's strongest argument is that an executable plan needs exact operational instructions as well as behavioral coverage. It correctly identifies the missing withdrawn-commit prompt arm, the distinction between the xdist version pin and installation mechanism, and G-10's staged-change blind spot while acknowledging the later allowlist safeguard (V1:37–85; T:848–864, 611, 723, 851; CI:29). Its external-anchor checks and disclosure of unread sections make its evidence boundary unusually inspectable (V1:129–156). Its observation that POST remediation can change the tree after the checkpoint is substantive and survives source verification, even though its minor label does not survive the debate's binary severity rule (V1:22–36; T:866, 875; B:19).

##### Steelman: Variant 3

Variant 3's strongest argument is evidence freshness across state changes: a gate, snapshot or checkpoint describes one tree, not every later repaired tree. Its POST-remediation finding and final-change-set freshness finding identify real ordering hazards, while its import analysis notices the design's types-only qualifier that module-edge checks alone do not enforce (V3:6–16, 38–55; T:742, 778, 800, 864–875, 605; D:239). Its wider requirement register also corrects real automatic-mapping errors; the relevant predicate, cycle and AST test-writing items do exist (V3:96–99, 152–155, 188–191, 236–239; T:206, 469, 599, 608, 690). The lint and main.py findings are strongest when framed as conditional error-path instruction conflicts, not claims that this checkout has already failed either formatter (V3:17–28, 66–74; T:502, 520, 699–702).

##### Key Strengths Claimed

1. **Meaningful coverage units.** Variant 2 separates 25 ACs, overlapping requirement rows, and named-test creation/execution mappings; its counts are not additive measures of independent requirements (V2:23–34, 154). Use the union of the cards' units, keeping their identities and overlaps, rather than replacing the scenario analysis with token matches (B:33; V2:30).
2. **R2-001 remains a concrete planned-test-writing gap.** Step 6.2 separately requires lost-label, voided-approval and changed-Project-status rejection at the final reread, but Step 6.7's explicit reread cases name closure, changed assignees, timeout and reserved-call refusal (T:460, 475). A mutant that reuses initial approval or Project evidence can pass initial predicate tests and the enumerated reread cases. Require independently eligible-then-revoked final-read cases asserting the specified reason, no entry and no launch; this is not a claim that such a mutant already exists (V2:16).
3. **R2-002 remains a concrete planned-test-writing gap.** The fallback formatter's unit test and successful cycle appends do not demonstrate that run_cycle calls the formatter when append or the final save fails (T:212, 460, 472). The CLI config-error and reset fallback cases exercise different entry paths, not these cycle integration branches (T:505, 508). Require separate append-failure and final-save-failure injections through run_cycle, checking the five-key fallback, the specified reason/exit and released lock (T:197, 460; V2:17).
4. **Deviation authority changes the baseline.** The affected-subset gate and pinned formatter are declared choices, not unfulfilled literal make-test/unpinned-format requirements (R:28, 32; T:909, 912). Covered under that authorized baseline does not mean equivalent to full-suite local execution (V2:151–152).
5. **Evidence boundary.** These are judgments about instructions and planned tests, not passing implementation results (V2:10, 34, 149). Later semantic tracing and mutation-oriented QA are genuine recovery mechanisms, not evidence that the particular missing tests have already been written (T:729, 757, 763).

##### Weaknesses in Variant 1

- **T-2 is not absent just because its literal token is absent from a helper description.** Step 4.4 explicitly assigns one test per T-1..T-13 row, Step 6.2 applies attempts below 3, and Step 6.7 requires retry/backoff and third-failure abandonment behavior (T:345, 460, 475). Drop R1-001 as a requirement-coverage defect; a request to repeat the conjunct beside the helper would be a clarity preference, not proof of missing behavior (V1:10–14).
- **Conditional does not automatically mean minor.** The withdrawn-commit branch is expressly supported, but Step 10.6 still requires the skipped branch's base-sha.txt and permits only a SHA substitution in the unchanged BASE..HEAD prompt (T:848, 860–864, 960). OQ-51 authorizes the alternate change-set choice; it does not supply compatible verbatim instructions. R1-003 is blocking on that branch, as is ungated source remediation under R1-002 (B:19; T:866, 875).
- **Local gate weakness is not total absence of protection.** Retain R1-005 as a minor redundant-check weakness, not an assertion that the normal checkpoint can commit protected files: Step 10.3's explicit allowlist HALTs on them (T:723, 851; V1:78).
- **A new xdist preflight is not established as missing evidence.** The mechanism wording is inaccurate, but the register already records successful offline resolution on this host (T:611; CI:29; R:48). Keep the wording correction; do not assert an observed cache failure or invent a new mandatory preflight.
- **Reading limits affect weight, not automatic admissibility.** The card itself says some coverage judgments were based on item purpose rather than line-level inspection and that research/06 was unread (V1:149–156). Such rows need source verification before overruling verified scenario-level findings.

##### Weaknesses in Variant 3

- **Two covered audit/revalidation rows are too coarse.** An ordinary audit line for every exit does not prove fallback wiring, and one closed-issue reread case does not prove approval and Project evidence are recomputed (V3:200–203, 232–235; T:460, 472, 475). Preserve Variant 2's partially_covered judgments for the concrete planned tests.
- **The marker comparison is authorized.** DF-46 explicitly prescribes installed/project comparisons only when present (R:180; T:384). The generic no-real-HOME adequacy lens deserves an exception clarification, but R3-006 cannot be retained as an unauthorized behavioral departure or used to replace the mandated comparison (T:757; B:10, 21).
- **R3-003 combines different issues.** A new lens gate after every repair is expressly unnecessary under DF-08, and the cited postfix branch actually contains HALT if the rerun cannot pass (R:31; T:778, 793). Raw test-repair loops lacking a numerical cap are not themselves proof of deadlock, nor proof that the two-cycle independent QA cap is absent (T:690, 739). Drop this composite finding; retain the separately evidenced snapshot-freshness defect C-005 instead.
- **R3-005 must be narrowed.** OQ-46 records predicates.parse_utc and format_utc as the timestamp-parsing choice, so calling all three helper imports undeclared is inaccurate (T:968). The remaining valid_issue_number function import is not named in that exception and conflicts with the types-only design rule (T:330; D:239). Retain only that residual constraint conflict, not a demand to undo the recorded UTC-helper choice; the module-edge test alone does not enforce the distinction (T:605).
- **Conditional lint conflicts must not become invented execution evidence.** The text requires exit zero, prohibits fixing untouched-file findings, and requires every final row PASS (T:699, 702, 735). Retain the unresolved nonzero-baseline branch as a blocking instruction conflict, but do not claim an observed baseline failure, unconditional impossibility, or absence of every HALT elsewhere: T:778 explicitly supplies one for later postfix reruns. Likewise C-008 concerns a possible out-of-registration formatter hit; none was observed (T:502, 520).

##### Concessions

- Variant 2 returned Markdown instead of the requested YAML, and its MEDIUM/Drift fields are not the merge's binary-severity/category-enum schema (V2:1, 14–17; B:18–21, 32–35). Normalize the merged register to YAML, BINARY and ENUM; retain authorization/deviation status as separate explanatory metadata.
- Variant 2's praise of the normal checkpoint was not a rebuttal to post-commit remediation, and it missed the withdrawn-commit arm (V2:153; T:848, 860–875). The comparison's description of Variant 2 as affirmatively finding “Not a defect” overstates that sentence: silence and normal-path praise are not an examined rejection.
- The two Variant 2 findings are blocking **at the concrete planned-test-writing boundary** under B:19. This is not a prediction that every executor will omit the tests: Step 9.17, the adequacy lens and the AC lens can discover and repair both gaps (T:729, 757, 763). The merged register should preserve that counterevidence rather than claim the whole plan has no coverage backstop.
- R3-004 is more than a cosmetic line-count issue: the aggregate embeds the main.py diff and coverage/gate tables before later fixes/reruns, and M4 is directed to it as the full change set (T:742, 778, 800). A required final evidence artifact can therefore describe an older tree. M4 also opens current implementation paths, so this does not prove that all repaired code escapes review.
- R3-008 identifies a completion-contract problem: explicitly retaining Done after staging fails is incompatible with the required staged task package (T:875; R:30). The correction needs neither a second commit nor rollback of implementation: failed required staging must remain an unmet completion condition.
- The blocking set is C-001, C-005, C-006 (valid_issue_number only), C-008, C-009, X-001, X-006, X-007 and X-008. C-008 and X-008 are conditional instruction conflicts; no failing formatter baseline is asserted. The strict binary rubric upgrades actual constraint/required-evidence gaps even where the originating reviewer called them minor (B:19–20).

##### Shared Assumption Responses

- **A-001 — QUALIFY.** The disputed passages used here were checked against the current task/design/register; that does not establish unchanged history or validate every citation in every card (B:24).
- **A-002 — ACCEPT.** Step 10.6 explicitly directs applying remediation for Regression or unauthorized Drift, after the checkpoint; it does not restrict those fixes to reports (T:864–866, 872).
- **A-003 — QUALIFY.** Item text supports assessing explicit planned coverage, but an unnamed scenario is not guaranteed to remain unwritten: semantic tracing and mutation-oriented lenses can require the missing test later (T:729, 757, 763).
- **A-004 — REJECT.** No lint/format baseline was executed in this review, so cleanliness is unestablished; reject assuming it, without asserting the opposite (R:49–50; T:699–702).

##### Point Positions

Citation key: each alias below resolves to the exact absolute path shown; quoted evidence cells contain at most 25 words in total per row. “Covered” means assigned under the authorized plan baseline, never implemented or passing.

- B = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md
- T = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- D = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md
- R = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md
- V1 = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/variant-1-original.md
- V2 = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/variant-2-original.md
- V3 = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/variant-3-original.md
- CI = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.github/workflows/test.yml

| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | YAML | Normalize the merged register, not this required Markdown statement | V2:1 — “the reviewer returned markdown instead of the requested YAML” | V1/V3 |
| S-002 | UNION | Preserve AC, INF, T and test-file mappings; deduplicate overlaps | V2:30 — “Coverage-slice rows overlap those criteria and are not counted again.” | V3 breadth; V2 granularity |
| S-003 | BINARY | Reclassify from evidence, not MEDIUM or originating labels | B:18 — “Binary severity (decide from evidence, not from the reviewer's label)” | V1/V3 schema |
| S-004 | ENUM | Keep authorization/deviation as separate metadata | B:35 — “coverage_gap/contradiction/unexecutable_item/wrong_citation/gate_weakness/sequencing/other” | V1/V3 schema |
| C-001 | VALID-BLOCKING | R1-003; withdrawn-commit prompt arm is not executable as specified | T:848 — “skip Steps 10.2 to 10.4”; T:860 — “first read the SHA from” | V1 finding; not its severity |
| C-002 | VALID-MINOR | R1-004; same version pin, different installation mechanism | T:611 — “supplied ad hoc exactly as”; CI:29 — `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"` | V1 |
| C-003 | VALID-MINOR | R1-005; local blind spot, later normal-path allowlist prevents commit | T:723 — `git diff --exit-code pyproject.toml Makefile`; T:851 — “IF the check fails, HALT” | V1 |
| C-004 | DROP | R3-003; extra-gate absence authorized; cited postfix HALT exists | R:31 — “with no extra gate”; T:778 — “IF it cannot be made to pass, HALT” | — |
| C-005 | VALID-BLOCKING | R3-004; required final aggregate can become stale after fixes | T:742 — “the main.py diff verbatim”; T:778 — “overwriting the `p9-*` files”; T:800 — “the FULL change set listed” | V3 finding; stronger severity |
| C-006 | VALID-BLOCKING | R3-005 narrowed to valid_issue_number; UTC helpers exempted by OQ-46 | D:239 — “`predicates` (types only, for `Entry` fields that hold an issue number)”; T:330 — “`parse_utc`, `format_utc`, `valid_issue_number`” | V3 residual; reject blanket claim |
| C-007 | DROP | R3-006; DF-46 explicitly authorizes optional installed/project comparisons | R:180 — “The installed copy and the project `.claude/` copy are compared only when present.” | — |
| C-008 | VALID-BLOCKING | R3-007; conditional out-of-registration formatting conflict, not observed failure | T:502 — “nothing else in the file changed”; T:520 — “fix any finding inside those files” | V3 finding; stronger conditional severity |
| C-009 | VALID-BLOCKING | R3-008; failed required staging cannot satisfy completion | T:875 — “a failure of this staging command is logged in that section and never reverts the Done status” | V3 finding; stronger severity |
| C-010 | OTHER | Blocking: C-001, C-005, C-006 (narrowed), C-008, C-009, X-001, X-006, X-007, X-008 | B:19 — “break a stated constraint, leave a required behaviour untested or unbuilt”; T:866 — “apply the remediations” | V1/V3 additions; retain V2 gaps |
| C-011 | YES | Weight evidence passage by passage, not by persona/model alone | V1:150 — “Several INF rows were judged from item purpose, not from a line-level read of the item and its test.” | V1 disclosure |
| X-001 | VALID-BLOCKING | Deduplicate R1-002/R3-001; remediated tree lacks explicit renewed gate/stage contract | T:866 — “apply the remediations the skill offers under `--remediate`”; T:875 — “staging only: no second commit” | V3 severity; V1 discovery |
| X-002 | DROP | covered | T:345 — “one test case per transition row T-1 to T-13”; T:460 — “attempts below 3” | V2/V3 |
| X-003 | covered | INF-123 under DF-05; full-suite local equivalence not claimed | T:909 — “the local gate is the named test subset (G-2) plus `make lint`, not `make test`” | V2 |
| X-004 | covered | INF-155 under authorized gate substitutions; lint error-path finding tracked separately | R:32 — “on changed files at P3-P8 and on `src/ tests/` once at P9” | V2 |
| X-005 | covered | INF-016; scope plus read-only and no-automatic-retry checks | D:70 — “no daemon mode, no in-cycle retry, no automatic Orca retry”; T:590 — “no argv anywhere is a POST to a REST path” | V2/V3 |
| X-006 | VALID-BLOCKING | partially_covered | T:472 — “appends exactly one parseable cycle line”; D:887 — “or the stderr fallback” | V2 |
| X-007 | VALID-BLOCKING | partially_covered | T:460 — “a lost label, a voided approval or a changed Project status”; T:475 — “a re-read showing the issue closed” | V2 |
| X-008 | VALID-BLOCKING | R3-002 narrowed to unresolved nonzero-baseline branch; actual failure unobserved | T:699 — “ensuring exit 0”; T:699 — “recorded and NOT fixed”; T:735 — “every row is PASS” | V3 conditional conflict, not unconditional claim |
| X-009 | YES | INF-108/122/135/147/153 items exist; existence is not complete behavioral proof | T:206 — “the approval and unchanged-since cases”; T:599 — “includes mutation-guard tests”; T:469 — “over every pair” | V3 |
| A-001 | QUALIFY | Verified disputed passages, not every historical/card citation | B:24 — “Verify before you argue.” | All cards require verification |
| A-002 | ACCEPT | Task explicitly authorizes applying substantive remediation after checkpoint | T:866 — “If the skill surfaces any Regression or any unauthorized Drift, apply the remediations” | V1/V3 |
| A-003 | QUALIFY | Explicit coverage assessable; later executor/lens recovery remains possible | T:729 — “a GAP is fixed by adding the missing test”; T:757 — “reason about concrete mutations” | V2 caveat; later guards |
| A-004 | REJECT | Clean baseline not established; no contrary runtime claim | R:49 — “a ruff finding in a file this task did not touch is recorded, not fixed” | No card has execution evidence |

### Advocate v3 (Round 1, verbatim from round1-advocate-v3.md)

#### Advocate: Variant 3 (opus:refactorer)

Abbreviations: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R06 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`; RSK = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. Every TF line cited below was re-read for this statement (read-only); no command other than read-only `sed`/`grep` was run, and lint was NOT run.

##### Position Summary

Variant 3 is the most accurate card on blocking defects. It found the two defects that no later item in the plan can catch: the POST-reflect `--remediate` step (TF:864-866), which sits after every gate and the only commit, and the full-tree lint rule (TF:699/702 against TF:735/745), which cannot pass as written. Every one of its 20 citations still matches the task file. I concede that Variant 2's two coverage gaps (R2-001, R2-002) are real, that Variant 3 wrongly marked INF-146 and INF-138 as covered, and that R3-001's mechanism has to be narrowed: the reflect skill never edits source itself, so the risk comes from the runner being told to "apply" the remediation task the skill writes.

##### Steelman: Variant 1

Variant 1 (analyzer, sonnet) checked more than 12 external claims against real repo files (install_user_setup.py, main.py, atomic.py, test.yml:29, .pre-commit-config.yaml), so its findings about the outside world are the best grounded of the three. It found the same POST-reflect hazard independently (R1-002, TF:864/875), which corroborates X-001. It is the only card that raised the withdrawn-commit argument gap (R1-003), the "exactly as test.yml:29" mechanism mismatch (R1-004, confirmed: `.github/workflows/test.yml:29` is `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"`, while TF:611 uses `uv run --offline --with`), and the G-10 staged-change blind spot (R1-005, TF:723). It reports its reading limits openly (variant-1:155).

##### Steelman: Variant 2

Variant 2 (qa, haiku) is the only card that tracks each AC-1..AC-25 through its implementation, test-writing and test-running items (variant-2:36-62), and it lists all 19 named test files (variant-2:121-141). Both of its findings hold on reading:
- R2-001: Step 6.2 requires that "a lost label, a voided approval or a changed Project status gives `revalidation_failed`" (TF:460). Step 6.7 tests only a closed issue, assignee changes, a timeout and a refused reserved call (TF:475). A grep of TF:475 for "label", "voided" and "Project status" finds none of the three revocation cases.
- R2-002: TF:460 implements "a failing save giving exit 6 `state_dir_unwritable` through `audit.stderr_fallback`", but Step 6.6 (TF:472) never injects an append failure or a save failure into `run_cycle`. The only fallback test is at the CLI level (TF:508).

Variant 2 also states the right principle: "Lexical matches were not accepted as proof" (variant-2:66).

##### Key Strengths Claimed

1. **X-001 / R3-001 sits after every gate.** Step 10.6 passes `--mode post --remediate --diff <BASE SHA>..HEAD` (TF:864). Its item 3 says "apply the remediations the skill offers under `--remediate`" (TF:866). Step 10.7 then stages only `.dev/tasks`, with "no second commit" (TF:875), and R06:30 declares only that staging ("staging only; no second commit"). It does not declare `--remediate`; a grep of R06 for "remediat" returns nothing.
   - **Narrowed mechanism:** with `--depth deep`, the skill takes the MDTM route: "`task-builder` builds the MDTM task file; the user runs `/task <path>`" (RSK:321), and "reflect AUTHORS but NEVER runs `/task` or `/sc:implement`" (RSK:324). Acceptance is "interactive" or headless `--print` (RSK:324), and a `bypassPermissions` subagent is neither.
   - **Why it is still blocking:** item 3 can then only be read two ways. (a) The runner executes the authored task, editing source after the only commit with no G-1..G-11 re-run, and Step 10.7 marks Done. (b) The instruction cannot be executed as written. Either reading is blocking under the brief, and no lens, gate or verifier runs after Step 10.6.
2. **X-008 / R3-002: the lint gate has no passing path.** Step 9.7 requires "ensuring exit 0; a finding in a file this task did not touch (the local `uv run ruff` is not the pinned 0.15.20) is recorded and NOT fixed" (TF:699). Step 9.8 says the same (TF:702). Step 9.19 requires that "every row is PASS (a FAIL is fixed and its step re-run" (TF:735), and the Final gate agent counts "Any command that fails" as a finding (TF:745).
   - The parenthetical at TF:699 shows the plan's author expected findings in untouched files, because DF-09 records that bare `uv run ruff` resolves to 0.17.3 (R06, row DF-09). `make lint` runs `uv run ruff check .` (Makefile:49).
   - One such finding leaves the gate with no way to pass and no HALT rule. That is a deadlock, and no later in-plan lens can fix it, because the gate rule itself is the defect.
3. **Citations hold.** All 20 Variant 3 citations were re-read and match: TF:330, 336, 384, 502, 520, 690, 699, 702, 735, 742, 745, 757, 778, 800, 864, 866 and 875; D:239 and D:791; Makefile lint (one line off: the command is at Makefile:49, under the `lint:` target at :47). Variant 3's T-2 note, "the attempts < 3 check is applied in run_cycle", is verified by TF:460: "a `failed` entry past backoff with attempts below 3".
4. **Its automatic-mapping corrections (X-009) are right.** They are corroborated independently by Variant 2's test-file table: INF-108 maps to 5.6-5.8, 6.9 and 8.2-8.8, and INF-153 maps to 8.6 (variant-2:129-141).
5. **Severity rule applied consistently.** A defect that an in-plan guard will catch later is minor; a defect downstream of every guard, or inside a gate's own pass rule, is blocking. This one rule separates X-001 and X-008 (blocking) from R1-001, R2-001 and R2-002 (minor, because the Final test-adequacy lens at TF:757 is told to flag "missing negative and boundary cases" for every "rule, table row, transition, reason, exit code").

##### Weaknesses in Variant 1

- It rates R1-002 as only minor, although by its own account nothing re-gates the tree before Done ("No item re-runs G-1 to G-11 after remediation"). Its fix (variant-1:35) would add a HALT, which is a blocking-class remedy.
- Its claim "Gate commands executable as written" (variant-1:144) misses the TF:699/735 contradiction. It also did not read the Final gate items TF:737-837 (variant-1:155), which is exactly where the TF:745 no-carve-out rule sits.
- R1-001 is real but very small. `fail` abandons the entry at attempts 3 (TF:336), and `run_cycle` already applies "attempts below 3" (TF:460), so a `backoff_elapsed` without the conjunct behaves the same on every reachable state.
- R1-003 is partly a declared deviation. TF:848 points to OQ-51 for the working-tree case, so only the argument-text gap is left.

##### Weaknesses in Variant 2

- It did not use the requested YAML format and used a non-binary MEDIUM severity (variant-2:1, :16), which makes it harder to merge.
- It cleared X-001 with "The checkpoint sequence captures BASE before the single commit" (variant-2:153). That is true, but it does not answer the question: the hazard is what happens after the commit, at TF:866/875.
- It judged INF-124 covered (variant-2:85) without noticing that the exit-0 rule contradicts the rule for untouched files (TF:699).
- It labelled pre-execution plan gaps "Drift", a post-execution category, which is the wrong vocabulary for a plan review.

##### Concessions

1. R2-001 and R2-002 are valid. Variant 3 marked INF-138 "covered" and INF-146 "covered" (variant-3:200-235), and both should be partially_covered.
2. R3-001 overstated the mechanism: the skill does not edit source itself (RSK:324). The defect stands only through the runner's "apply" instruction at TF:866.
3. R3-002 depends on at least one lint finding in an untouched file existing. I did not run `make lint`, so this is inferred from TF:699 and DF-09, not observed.
4. R3-005 is partly disclosed in OQ-46 (TF:968: "who parses the store's own timestamps (`predicates.parse_utc` and `format_utc`)"). It is still not recorded as a departure from D:239.
5. R3-006 follows the design itself (D:791, "read through the dual surface"), so the conflict is with the lens rule, not with the design. Minor.
6. Variant 3 did not read the Gate D items or the bodies of 9.M4-9.M13 (variant-3:306).
7. The Makefile citation is one line off (:50 instead of :49).

##### Shared Assumption Responses

- **A-001: ACCEPT.** I re-read about 25 cited lines (TF:330-875, D:239/479/791/879/887, R06:30, test.yml:29). Every excerpt exists at its cited line.
- **A-002: QUALIFY.** The skill never edits source; it only authors a corrective task file (RSK:321, :324). But TF:866 tells the runner to "apply the remediations", and the only way to apply them is a nested `/task` run, which would edit source after the commit. So X-001 stands on that instruction, not on the skill.
- **A-003: QUALIFY.** In-plan backstops (the TF:757 test-adequacy lens and Step 9.17) make test-scenario gaps minor. They cannot rescue defects that sit after every gate (TF:866) or inside a gate's own pass rule (TF:699/735/745).
- **A-004: REJECT.** The plan's own text anticipates findings in untouched files from the unpinned ruff (TF:699 parenthetical; DF-09: bare `uv run ruff` resolves to 0.17.3). A lint-clean tree was never verified and cannot be assumed.

##### Point Positions

| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | YAML | - | variant-2:1 - "the reviewer returned markdown instead of the requested YAML" | - |
| S-002 | UNION | V2 AC table + V3 INF register | variant-2:36 - "Criterion \| Judgement \| Implementation items \| Test-writing items" | V2 (AC rows) |
| S-003 | BINARY | - | advocate-brief:18 - "Binary severity (decide from evidence, not from the reviewer's label)" | - |
| S-004 | ENUM | V2 "Drift" maps to coverage_gap | RSK:40 - "UC-2 (post-execution): input is completed agent work" (the taxonomy is for completed work) | - |
| C-001 | VALID-MINOR | OQ-51 declares the working-tree case | TF:848 - "run Step 10.6 over a base the owner names ... documented as an Open Question; see OQ-51" | V1 |
| C-002 | VALID-MINOR | - | TF:611 - "supplied ad hoc exactly as `.github/workflows/test.yml:29` does"; test.yml:29 - "uv pip install -e" | V1 |
| C-003 | VALID-MINOR | P10 allowlist backstop | TF:723 - "`git diff --exit-code pyproject.toml Makefile; echo \"EXIT=$?\"`" | V1 |
| C-004 | VALID-MINOR | - | TF:690 - "IF FAILED, fix the cause (never weaken an assertion) and re-run until PASSED" | - |
| C-005 | VALID-MINOR | - | TF:800 - "OUTPUT UNDER REVIEW: the FULL change set listed in ... final-change-set.md" | - |
| C-006 | VALID-MINOR | partly disclosed in OQ-46 | D:239 - "`predicates` (types only, for `Entry` fields that hold an issue number)"; TF:330 - "(`parse_utc`, `format_utc`, `valid_issue_number`)" | - |
| C-007 | VALID-MINOR | design mandates the dual surface | TF:384 - "the installed `~/.claude/skills/sc-issue-protocol/` copies also contain the marker" | - |
| C-008 | VALID-MINOR | - | TF:502 - "shows only these added lines"; TF:520 - "fix any finding inside those files" | - |
| C-009 | VALID-MINOR | - | TF:875 - "a failure of this staging command is logged in that section and never reverts the Done status" | - |
| C-010 | V3 | blocking: X-001, X-008; add R2-001 and R2-002 as minor | TF:735 - "every row is PASS (a FAIL is fixed and its step re-run" | V2 (two minor gaps) |
| C-011 | YES | - | variant-1:109 - "The Phase 3 items were not re-read in this session" | - |
| X-001 | VALID-BLOCKING | mechanism narrowed to the runner's "apply" | TF:866 - "apply the remediations the skill offers under `--remediate`"; RSK:324 - "reflect AUTHORS but NEVER runs `/task`" | V1 (co-finder) |
| X-002 | VALID-MINOR | T-2 covered | TF:460 - "a `failed` entry past backoff with attempts below 3 first checks the day cap" | - |
| X-003 | partially_covered | not a defect (declared DF-05) | TF:735 - "\"full suite: CI only\" (the whole `make test` run is left to CI, decision DF-05)" | - |
| X-004 | partially_covered | not a defect (DF-05) | TF:735 - "the whole `make test` run is left to CI, decision DF-05" | - |
| X-005 | covered | - | variant-3:291 - "No in-cycle or Orca retry is asserted; no daemon mode exists by construction." | - |
| X-006 | VALID-MINOR | INF-146 partially_covered | TF:460 - "a failing save giving exit 6 `state_dir_unwritable` through `audit.stderr_fallback`" (no cycle test at TF:472) | V2 |
| X-007 | VALID-MINOR | AC-6 partially_covered | TF:460 - "a lost label, a voided approval or a changed Project status gives `revalidation_failed`" (absent from TF:475) | V2 |
| X-008 | VALID-BLOCKING | - | TF:699 - "ensuring exit 0; a finding in a file this task did not touch ... is recorded and NOT fixed" | - |
| X-009 | YES | corroborated by V2 | variant-2:129-141 - test-file table names 5.6-5.8, 6.9, 8.2-8.8 as creating items | - |
| A-001 | ACCEPT | verified, not assumed | TF:864 - "--mode post --remediate --diff <BASE SHA>..HEAD" (matches every card's citation) | - |
| A-002 | QUALIFY | - | RSK:321 - "`--remediate --depth deep` → MDTM route: `task-builder` builds the MDTM task file; the user runs `/task <path>`" | V2 (in part) |
| A-003 | QUALIFY | - | TF:757 - "flag ... missing negative and boundary cases" | - |
| A-004 | REJECT | - | TF:699 - "(the local `uv run ruff` is not the pinned 0.15.20)" | - |

## Round 2: Rebuttals

Round 2 ran sequentially (v1, v2, v3). Each statement below is verbatim from round2-advocate-v{1,2,3}.md.

### Advocate v1 (Round 2, verbatim from round2-advocate-v1.md)

#### Advocate: Variant 1 (sonnet:analyzer), Round 2 rebuttal

Path shorthand: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`.

Lines re-read first-hand this round: TF:326-395, 455-524, 595-624, 686-880, 955-970; R:30-31, 180; D:233-242.

##### Responses to Criticisms

**Round 1 line-number discrepancies (TF:517, 851, 351, 387 versus 699, 723, 690).** Neither side fabricated a citation. My cites are real lines in the Phase 4-7 gate steps. TF:351, 387 and 690 share the wording "re-run until PASSED, recording each fix". TF:391, 517 and 699 share the "ensuring exit 0" sentence, and only TF:699 carries the parenthetical "(the local `uv run ruff` is not the pinned 0.15.20)". TF:851 is the Step 10.3 post-staging G-10 run, and TF:723 is the Step 9.15 unstaged G-10 run. For G-4 and G-10 I now use the Phase 9 cites (TF:699, 723) as the better anchors.

**V2 and V3: my "no blocking defect" verdict was too lenient.**
- X-001: conceded and kept (see X-001 below).
- X-008: conceded as conditional blocking. The deadlock needs a non-clean baseline, and nobody measured one.
- X-006 and X-007: I conceded these in Round 1. After re-reading the backstops I withdraw the blocking label and keep the coverage finding (see X-006 and X-007 below).
- X-005: conceded (covered).
- Net: Round 1 was too lenient on X-001. Round 2 is stricter than Round 1 on X-001 and X-008 and less strict than Round 1's concession on X-006 and X-007.

**V2 on X-002 (R1-001): DROP, citing TF:345 "one test case per transition row T-1 to T-13" and TF:460 "attempts below 3".**
- Not DROP. The cited text exists. TF:336 defines `backoff_elapsed(entry, now)` as "now >= `updated_at` + 10 min" with no `attempts` conjunct, while D:479 puts the conjunct in the T-2 row.
- T-2 itself is covered, because TF:460 applies attempts < 3 in `run_cycle`. The residual is a token that is missing from the helper's definition. That is a wording nit, so I keep VALID-MINOR and concede the T-2 coverage point to V2 and V3.

**V2 on C-001 (R1-003): BLOCKING. V3: OQ-51 may make it a declared deviation.**
- I had planned to upgrade this to blocking. The fresh read of TF:848 and TF:960 reverses that.
- Step 10.2 itself says: skip Steps 10.2 to 10.4, run Step 10.6 "over a base the owner names instead of `plans/base-sha.txt`", and when the owner names none, use the working-tree diff against HEAD.
- OQ-51 (TF:960) declares this as a weaker change-set definition.
- The only residual is that the literal `--diff <BASE SHA>..HEAD` form for the "no base named" sub-branch is not spelled out. That is a conditional branch that needs an owner withdrawal first. VALID-MINOR, conceded to V3 (declared by OQ-51). I reject V2's blocking label.

**V2 and V3 on INF-016 (X-005): covered.** Conceded. Guard-by-absence satisfies NG-1, 3, 4 and 5, and NG-2 has the explicit argv scan.

**V2 on C-004 (cites TF:778 "IF it cannot be made to pass, HALT" and R:31 "with no extra gate").**
- TF:778 confirms a HALT for the Final-gate re-run, so "no HALT" is false for that gate.
- R:31 confirms that "A fix made after a gate passes ... is re-checked by re-running G-4 and G-5, with no extra gate". The "post-gate fixes unreviewed" half of R3-003 is therefore a declared choice (DF-08).
- What remains is that the per-phase loops at TF:351, 387 and 690 have no cap. Every item has the escape hatch "If unable to complete ... log the blocker ... then mark this item complete", so nothing deadlocks. That is a nit: VALID-MINOR (I had planned DROP). Conceded to V2 on the declared half.

**V2 on C-007 (cites R:180 / DF-46): DROP.** Confirmed. R:180 (DF-46) says "The installed copy and the project `.claude/` copy are compared only when present." This is a declared deviation. Conceded to V2, and I withdraw my Round 1 acceptance of R3-006.

**C-006 (OQ-46 partly discloses).** TF:968 (OQ-46) records that `predicates.parse_utc` and `format_utc` are used by the record. That covers two of the three names in TF:330. `valid_issue_number` is undisclosed, and D:239 says "types only". The widening is explicit in the item and the module-boundary test is derived from the design table (TF:751), so it is a nit. VALID-MINOR.

**C-005, C-008, C-009.**
- C-005: TF:742 builds the list by Glob at one moment. The M4 prompt (TF:800) names directories as well as the list, so a late file is still in scope. VALID-MINOR.
- C-008: TF:520 allows fixes only "inside those files" and TF:502 requires a diff of added lines only, so the two are reconcilable. VALID-MINOR, conditional, and nothing was observed.
- C-009: TF:875 makes the staging failure non-reverting by design, and Step 10.1 and the allowlist have already run. VALID-MINOR.

**X-006 and X-007: does the binary "leave a required behaviour untested" rule apply, or do TF:729 and TF:757 make them minor?**
- Backstops, all read this round:
  - TF:729 (Step 9.17): each AC must map to a test that "really prove[s] the criterion", and "a GAP is fixed by adding the missing test".
  - TF:757 (9.F6): for every rule the lens must decide "whether a test exists that would FAIL if the behaviour broke".
  - TF:763 (9.F8): the exact argv, exit codes and reasons "must each be asserted".
  - TF:769 (9.F10): a fix agent is authorised to "add the missing case".
- The plan therefore contains three review layers and a fixer that target exactly this failure mode. The coverage finding is real (TF:472 has no append or save-failure injection; TF:475 lacks lost-label, voided-approval and Project-status re-read cases). A worker who follows the whole file will not finish with the behaviour untested unless all three layers miss it.
- I move both to VALID-MINOR with coverage `partially_covered`. This is the only point on which I now disagree with V2, and it is a severity disagreement.
- Weak spot, stated openly: Step 9.17 matches test names by Grep and could mark PASS on an AC-14 test whose name matches. Only the F6 and F8 lenses read assertions.

**X-008 (V3: blocking; V2: INF-124 covered).**
- The text contradicts itself. TF:699 says exit 0 is required, but a finding "in a file this task did not touch ... is recorded and NOT fixed".
- TF:735 (Step 9.19) then requires "every row is PASS (a FAIL is fixed and its step re-run ...)".
- If the baseline is dirty, G-4 cannot be PASS and the fix is forbidden. That is a real deadlock with a cheap fix (a baseline item).
- The parenthetical about the unpinned local ruff shows the author expected untouched-file findings. I keep VALID-BLOCKING, conditional on A-004, conceded to V3.

##### Updated Assessment

Variant 3's X-001 is the one unconditional blocking defect: Step 10.6 tells the runner to apply `--remediate` edits after the single DF-07 checkpoint commit (TF:866), and Step 10.7 stages only `.dev/tasks` (TF:875), so the final tree is neither gated nor committed. X-008 is blocking only if the tree is not lint-clean, because TF:699 forbids the fix while TF:735 requires every gate row to be PASS. After re-reading TF:848, TF:960, TF:778, R:31, R:180 and the TF:729, 757 and 763 backstops, I reduce C-001, X-006 and X-007 to minor and drop C-007. V3 is the most accurate card overall, and V2's coverage findings stand as real but minor because three review layers and an authorised fixer target the same gap.

##### New Evidence

- TF:848 and TF:960 (OQ-51) show that the withdrawn-commit branch is explicitly handled in Step 10.2 and declared as an Open Question (C-001).
- TF:778 shows a HALT on a failing re-run. R:31 declares "with no extra gate". Both limit C-004.
- R:180 (DF-46) declares that the installed marker copy is compared only when present (C-007).
- TF:729, 757, 763 and 769 are backstops for X-006 and X-007. Only the F6 and F8 lenses read assertions.
- TF:735 requires every Step 9.19 gate row to be PASS. This turns the X-008 contradiction into a concrete deadlock if the baseline is dirty.
- D:239 reads "`predicates` (types only, for `Entry` fields that hold an issue number)". TF:968 (OQ-46) only partly discloses the widening (C-006).
- No card ran a lint baseline. A-004 is therefore still unmeasured.

##### Shared Assumption Responses

- A-001: QUALIFY. Every excerpt I checked exists, but the cards cite parallel steps (TF:351, 387 and 690 share wording, as do TF:391, 517 and 699), so line numbers differ without any fabrication.
- A-002: QUALIFY. TF:866 tells the runner to "apply the remediations the skill offers under `--remediate`", so out-of-`.dev/tasks` edits are possible; by V3's reading of the skill, the skill itself only authors a corrective task.
- A-003: QUALIFY. Item text is dense and Step 9.17 and the Final lenses (TF:757, 763) are real backstops, but 9.17 matches names, not assertions, so a missing scenario is a legitimate but minor pre-execution finding.
- A-004: REJECT. Nothing proves the tree is lint-clean, and the TF:699 parenthetical about the unpinned local ruff shows the author expected untouched-file findings.

##### Point Positions

| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | YAML | | diff-analysis.md:20 - "Markdown tables (reviewer returned markdown instead of the requested YAML)" | V3 |
| S-002 | UNION | | diff-analysis.md:21 - "AC-1..AC-25 as atomic units, plus 46 coverage-slice rows and a 19-row named-test-file table" | |
| S-003 | BINARY | | advocate-brief.md:18 - "Binary severity (decide from evidence, not from the reviewer's label)" | |
| S-004 | ENUM | | advocate-brief.md:35 - "ENUM (coverage_gap/contradiction/unexecutable_item/wrong_citation/gate_weakness/sequencing/other)" | |
| C-001 | VALID-MINOR | | TF:848 - "over a base the owner names instead of `plans/base-sha.txt` (when the owner names none, the POST reflect runs with the working-tree diff against HEAD" | V3 |
| C-002 | VALID-MINOR | | TF:611 - "supplied ad hoc exactly as `.github/workflows/test.yml:29` does" | |
| C-003 | VALID-MINOR | | TF:851 - "`git diff --exit-code pyproject.toml Makefile` and `git diff --exit-code -- .github/` (gate G-10 after staging)" | |
| C-004 | VALID-MINOR | | TF:778 - "IF it cannot be made to pass, HALT, write the failing output to the Task Log and do not release the next phase" | V2 |
| C-005 | VALID-MINOR | | TF:742 - "ensuring the file list is discovered by Glob (not typed from memory)" | V3 |
| C-006 | VALID-MINOR | | D:239 - "`predicates` (types only, for `Entry` fields that hold an issue number)" | V3 |
| C-007 | DROP | | R:180 - "The installed copy and the project `.claude/` copy are compared only when present." | V2 |
| C-008 | VALID-MINOR | | TF:520 - "fix any finding inside those files" | |
| C-009 | VALID-MINOR | | TF:875 - "a failure of this staging command is logged in that section and never reverts the Done status" | |
| C-010 | OTHER | Blocking: X-001 (unconditional); X-008 (conditional on A-004). Everything else minor or DROP | TF:866 - "apply the remediations the skill offers under `--remediate`"; V3 is the most accurate card | V3 |
| C-011 | YES | | diff-analysis.md:39 - "Did not read Gate D (619-672), bodies of 9.M4-9.M13, BUILD-REQUEST.md" | |
| X-001 | VALID-BLOCKING | | TF:875 - "staging only: no second commit, no push, no PR" | V3 |
| X-002 | VALID-MINOR | covered | TF:336 - "`backoff_elapsed(entry, now)` (now >= `updated_at` + 10 min)" | V2 |
| X-003 | partially_covered | | TF:735 - "the whole `make test` run is left to CI, decision DF-05" | |
| X-004 | partially_covered | | TF:735 - "the whole `make test` run is left to CI, decision DF-05" | |
| X-005 | covered | | diff-analysis.md:49 - "partially_covered: only NG-2 has an explicit guard" | V2 |
| X-006 | VALID-MINOR | partially_covered | TF:729 - "a GAP is fixed by adding the missing test (or the missing id in the test name) to the right file" | |
| X-007 | VALID-MINOR | partially_covered | TF:763 - "the exact argv, exit codes, reasons, counts and byte-identity claims of the criterion must each be asserted" | |
| X-008 | VALID-BLOCKING | conditional on A-004 | TF:699 - "a finding in a file this task did not touch (the local `uv run ruff` is not the pinned 0.15.20) is recorded and NOT fixed" | V3 |
| X-009 | YES | | diff-analysis.md:53 - "Several automatic "none" mappings declared wrong (INF-108, INF-122, INF-135, INF-147, INF-153)" | V3 |
| A-001 | QUALIFY | | TF:351 - "re-run until PASSED, recording each fix" | |
| A-002 | QUALIFY | | TF:866 - "apply the remediations the skill offers under `--remediate`" | |
| A-003 | QUALIFY | | TF:757 - "decide whether a test exists that would FAIL if the behaviour broke" | |
| A-004 | REJECT | | TF:699 - "(the local `uv run ruff` is not the pinned 0.15.20)" | |

### Advocate v2 (Round 2, verbatim from round2-advocate-v2.md)

#### Advocate: Variant 2 (haiku:qa), Round 2 rebuttal

Citation aliases used in prose (the table uses absolute paths):
- TF = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- D = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md
- R = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md
- B = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md
- V1, V2, V3 = respectively /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/variant-1-original.md, /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/variant-2-original.md, and /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/variant-3-original.md.
- V1R2 = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/round2-advocate-v1.md
- RS = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/skills/sc-reflect-protocol/SKILL.md
- CI = /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.github/workflows/test.yml

##### Responses to Criticisms

**Steelman Variant 1 before responding.** Its strongest Round 2 argument is that the executor follows the whole plan, not merely the first test-writing item: semantic tracing, mutation-oriented adequacy review and assertion-level AC review all explicitly require meaningful coverage (V1R2:44-52; TF:729,757,763). Its fresh recognition of OQ-51 also distinguishes an authorized change-set choice from incomplete argument wording (V1R2:22-26; TF:848,960). I accept both arguments and change the corresponding positions below.

**Steelman Variant 3 before responding.** Its strongest distinction is between recoverable omissions upstream of verification and changes downstream of the last verification (its Round 1 statement: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/round1-advocate-v3.md:23-31). Its narrowed POST mechanism is also correct: reflect authors remediation; it does not itself execute that remediation (RS:321-324). I retain the POST finding through the runner's explicit instruction to apply fixes, not through an invented source-editing behavior of the skill (TF:866,872,875).

**C-001 — concede VALID-MINOR.** The working-tree case is expressly declared, not missing: Step 10.2 permits an owner-named base or the working-tree diff, and OQ-51 repeats that override (TF:848,960). My Round 1 claim treated the ordinary verbatim prompt as if the explicit alternate branch had no authority. The remaining defect is failure to spell out that branch's argument substitution beside the ordinary prompt, not a demonstrated impossible workflow after honoring the declared override (TF:860,864). I cannot establish blocking severity without disregarding OQ-51.

**C-005 — concede VALID-MINOR.** The aggregate can become stale: Step 9.F1 copies line counts, the registry diff and gate/coverage tables; postfix reruns overwrite result files without explicitly rebuilding that aggregate (TF:742,778,793). But the M4 instruction independently names the complete implementation directories and runbook, not only an immutable file list (TF:800). I have no evidence that this bookkeeping defect omits a required code deliverable or forces an incorrect implementation; my earlier assertion of a blocking final-deliverable failure was too strong. This remains an evidence-refresh note, not proof that repaired code escapes M4.

**C-006 — retain VALID-BLOCKING, narrowed to the remaining value import.** The opponents' best case is that reusing validation is behaviorally sensible and the UTC helpers are disclosed in OQ-46 (TF:968; V1R2:37). I concede those two helpers. The remaining permission explicitly allows a runtime import of `valid_issue_number` from `predicates` into `record` (TF:330); that name is a function, not a type (TF:194), while the binding import table permits `predicates` for “types only” (D:239). A concrete permitted implementation using that import therefore breaks a stated constraint, which B:19 explicitly calls blocking; this conclusion does not require an observed runtime failure and does not assert that every possible implementation uses the import. The prescribed boundary test only checks the permitted module edges and would admit that value import (TF:605). OQ-46 names the UTC pair, not `valid_issue_number`; the M4 exemption does not add the third function (TF:968,800). Later generic fidelity review may discover this contradiction, but discovery alone cannot authorize the import: unlike an omitted test, this explicit permission conflicts with the binding import restriction. My disagreement with V1/V3 is therefore about the brief's explicit constraint-breaking threshold, not validation correctness.

**C-008 — concede VALID-MINOR.** Step 7.3 constrains the diff to registration lines, while Step 7.9 checks all of the file and permits fixes inside it (TF:502,520). The item runs `format --check`, not an automatic whole-file rewrite; it even preserves the long import comment (TF:520). No unrelated formatter hunk was observed or identified, so I cannot demonstrate a concrete wrong change solely from the whole-file target. Keep the conditional scope clarification, not my earlier separate blocking finding. This is narrower than X-008's explicit failing-gate pass-policy conflict (TF:699,702,735).

**C-009 — retain VALID-BLOCKING on the failed-staging branch.** Yes, “never reverts the Done status” is an explicit operational choice (TF:875), and the preceding implementation may be correct. But the same item says the task folder is “always staged” and requires the post-checkpoint log and reflect edits to stay staged; DF-07 requires the final staging action for exactly that purpose (TF:875; R:30). On the branch in which that action fails before staging those new edits, a worker is expressly told to retain Done with that requirement unmet and only log the error (TF:875). That is the concrete broken constraint; no source-code regression or second commit is needed to establish it. I do not treat every failure-policy sentence as an authorized deviation: B:10 identifies research/06 and Open Questions as the authority, and neither DF-07 nor OQ-7/OQ-51 waives successful staging (R:30; TF:911,960). This failure is after the review gates, so unlike the missing test cases it has no later recovery step (TF:875). This is a conditional completion defect, not a claim that staging actually failed here.

**X-006 and X-007 — concede both to VALID-MINOR, retain partially_covered.** The original planned-test omissions remain real: the cycle fallback is specified in Step 6.2 but the audit-exit test item lists ordinary appends; the final-read implementation lists three revocation cases that the test item does not enumerate (TF:460,472,475). D:887 includes the fallback and D:879 requires re-read failures to skip. However, Step 9.17 requires tests that “really prove the criterion” and fixes a GAP by adding a test; the adequacy lens reasons about concrete mutations and missing negative cases; the AC lens opens the assertions rather than accepting matching names (TF:729,757,763). Those are executable coverage-repair instructions, not merely hopeful directory-wide test execution. A worker following all of them must repair these omissions; my earlier “blocking at the test-writing boundary” artificially ended the task before its required verification. The residual is incomplete scenario enumeration in the early items, recoverable within the plan, not established final untested behavior. Neither concession asserts that those tests already exist.

**S-001 — YAML remains my answer.** Variant 2 did return Markdown rather than requested YAML (V2:1). I already conceded YAML in Round 1; the Markdown format of this requested debate statement does not change the merged register's required format (B:32,48). MEDIUM and Drift must likewise be normalized to the binary severity and category enumeration (V2:14-17; B:18,35).

**X-002 — concede VALID-MINOR; T-2 remains covered.** The helper definition omits the attempts conjunct (TF:336 versus D:479), so DROP was too dismissive. Nevertheless, the transition-test range includes all thirteen rows, and the cycle explicitly applies attempts below three (TF:345,460). The range instruction covers T-2 without spelling its token separately, so a missing literal token is not a separate coverage failure (TF:345; V1:10). Keep a helper-contract wording correction, not a missing T-2 behavior.

**X-003/X-004 — concede partially_covered relative to the literal design.** D:798 requires `make test`, and AC-23 incorporates section 13 (D:896). DF-05 substitutes the affected local selection and explicitly leaves the full suite to CI (R:28; TF:735,909). My “covered under the authorized baseline” was a defensible alternative baseline description, but it obscured incomplete literal local gate coverage. Use partially_covered with an explicit “authorized; not a defect” annotation; do not count either row as an unauthorized omission.

**C-004/C-007 — separate valid residue from declared choices.** I change C-004 from DROP to VALID-MINOR only for uncapped per-phase rerun wording (TF:351,387,690). Its alleged missing postfix HALT is false, and extra post-gate review is expressly waived (TF:778,793; R:31). C-007 remains DROP because optional installed/project marker comparisons are explicitly prescribed by DF-46 (R:180; TF:384), rather than an undeclared dependency invented by the executor.

##### Updated Assessment

I reduce C-001, C-005, C-008, X-006 and X-007 to minor, while retaining C-006 and C-009 as explicit constraint conflicts (TF:330,875; D:239). The final blocking set is C-006 (only the undisclosed value import), C-009 (failed staging), X-001 (applying post-checkpoint remediation without renewed gates) and X-008 (conditional on an untouched-file lint/format failure) (TF:330,605,699,702,735,866,875). The two Variant 2 scenario gaps remain partially_covered, but the later repair instructions prevent treating them as necessarily untested final behavior (TF:729,757,763). This is a document-only assessment: no baseline lint/test result or actual staging failure is claimed.

##### New Evidence

- **Citation re-verification completed.** I re-read all the source lines cited by my Round 1 prose/table: TF:197,206,212,330,336,345,384,460,469,472,475,502,505,508,520,590,599,605,608,611,690,699,702,723,729,735,739,742,757,763,778,793,800,848,851,860-875,909,912,960,968; D:70,239,879,887; R:28,30-32,48-50,180; CI:29; B:10,18-21,24,32-35. The original V1/V2/V3 files were also read in full to check the card citations, not inferred from their advocates' summaries (V1:10-156; V2:1-154; V3:6-306). This confirms the current excerpts, not unchanged historical file state.
- **The import qualification matters.** `valid_issue_number` is explicitly a pure validation function (TF:194). Combining that fact with TF:330 and the literal types-only limit (D:239) establishes a concrete constraint conflict rather than just a preference for a different dependency style.
- **The staging exception is downstream.** The checkpoint allowlist and commit stop rules precede the new reflect/log changes (TF:851,854,872,875). They cannot make a failed final staging action succeed. DF-07 authorizes staging after Done, not abandonment of staging on failure (R:30).
- **The aggregate is not the review boundary.** M4's explicit “everything under” directory scope limits the stale-snapshot finding (TF:800), whereas the POST runner's application instruction is after that gate (TF:866). This supports downgrading C-005 without dismissing X-001.
- **Correction to the remediation mechanism.** RS:321-324 says deep remediation authors a task and the user runs it. The task's runner is separately instructed to apply remediations (TF:866); the retained risk belongs to that instruction, not to automatic source modification by reflect.
- **C-002 remains wording only.** The gate uses ad-hoc offline resolution while CI installs the same pin (TF:611; CI:29). Offline resolution was already recorded as checked in the decision register; no cache failure was observed in this review (R:48).

##### Shared Assumption Responses

- **A-001 — QUALIFY.** Current cited excerpts were re-read; that does not establish that every historical card was generated from an unchanged file (B:24; TF:848,860,875).
- **A-002 — QUALIFY.** Reflect itself only authors the corrective artifact (RS:321-324). Out-of-task-folder changes arise if the runner follows the separate instruction to apply it after the checkpoint (TF:866,875).
- **A-003 — QUALIFY.** Early item text supports identifying specific omissions, but not assuming later mandatory assertion-level review fails; the trace and lenses make the two scenario gaps recoverable (TF:729,757,763).
- **A-004 — REJECT.** Do not assume an unmeasured clean baseline. The written pass policy conflicts on an untouched-file finding, but neither the version note nor this review proves such a finding actually occurs (TF:699,702,735; R:49-50).

##### Point Positions

| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | YAML | Merged register; this rebuttal is Markdown by request | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/diff-analysis.md:20 — “reviewer returned markdown instead of the requested YAML” | V1/V3; already conceded in Round 1 |
| S-002 | UNION | Deduplicate overlapping AC, INF, T and test-file units | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/diff-analysis.md:21 — “AC-1..AC-25 as atomic units, plus 46 coverage-slice rows and a 19-row named-test-file table” | V2 granularity; V3 breadth |
| S-003 | BINARY | Decide severity from evidence | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md:18 — “Binary severity (decide from evidence, not from the reviewer's label)” | V1/V3 schema |
| S-004 | ENUM | Authorization stays separate | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md:35 — “coverage_gap/contradiction/unexecutable_item/wrong_citation/gate_weakness/sequencing/other” | V1/V3 schema |
| C-001 | VALID-MINOR | Authorized alternative; residual prompt wording | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:848 — “run Step 10.6 over a base the owner names instead of `plans/base-sha.txt`” | V1/V3 |
| C-002 | VALID-MINOR | Same pin, different supply mechanism | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:611 — “supplied ad hoc exactly as `.github/workflows/test.yml:29` does” | V1 |
| C-003 | VALID-MINOR | Later staged-path allowlist catches it | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:851 — “IF the check fails, HALT” | V1 |
| C-004 | VALID-MINOR | Uncapped-loop residue only; postfix HALT exists | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:690 — “re-run until PASSED, recording each fix” | V1/V3, narrowed |
| C-005 | VALID-MINOR | Stale aggregate; current directories remain in scope | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:800 — “everything under src/superclaude/cli/issue_watch/” | V1/V3 |
| C-006 | VALID-BLOCKING | Only valid_issue_number; UTC pair disclosed | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:239 — “`predicates` (types only, for `Entry` fields that hold an issue number)” | V1/V3 on narrowing, not severity |
| C-007 | DROP | Optional installed-copy reading is prescribed | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:180 — “The installed copy and the project `.claude/` copy are compared only when present.” | — |
| C-008 | VALID-MINOR | Conditional scope wording; no unrelated hunk observed | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:520 — “format --check”; “a long import line with a trailing comment is kept as the neighbours have it” | V1/V3 |
| C-009 | VALID-BLOCKING | Failed-staging branch breaks required staged state | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:875 — “the `.dev/tasks` folder is always staged”; “never reverts the Done status” | V1/V3 on explicit policy, not authorization |
| C-010 | OTHER | Blocking: C-006, C-009, X-001; X-008 conditional | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md:19 — “break a stated constraint” | V1/V3 on recoverable test gaps |
| C-011 | YES | Weight checked evidence over unverified assumptions | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md:24 — “Verify before you argue.” | All cards need verification |
| X-001 | VALID-BLOCKING | Runner applies fixes after checkpoint; skill itself only authors | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:866 — “apply the remediations the skill offers under `--remediate`” | V3 severity and mechanism; V1 co-finder |
| X-002 | VALID-MINOR | covered | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:336 — “`backoff_elapsed(entry, now)` (now >= `updated_at` + 10 min)” | V1/V3 on wording; retain covered |
| X-003 | partially_covered | INF-123; authorized DF-05, not a defect | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:735 — “the whole `make test` run is left to CI, decision DF-05” | V1/V3 |
| X-004 | partially_covered | INF-155; authorized DF-05, not a defect | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:909 — “the local gate is the named test subset (G-2) plus `make lint`, not `make test`” | V1/V3 |
| X-005 | covered | Scope/absence plus explicit write guards suffice | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:70 — “no daemon mode, no in-cycle retry, no automatic Orca retry” | V2/V3 |
| X-006 | VALID-MINOR | partially_covered; later coverage repair required | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:729 — “a GAP is fixed by adding the missing test” | V1 Round 2/V3 |
| X-007 | VALID-MINOR | partially_covered; later assertion-level review required | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:763 — “the exact argv, exit codes, reasons, counts and byte-identity claims of the criterion must each be asserted” | V1 Round 2/V3 |
| X-008 | VALID-BLOCKING | Conditional on untouched-file lint/format failure; unobserved | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:699 — “ensuring exit 0”; “recorded and NOT fixed”; :735 — “every row is PASS” | V3, qualified |
| X-009 | YES | Mapping corrections establish items, not runtime passes | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:599 — “includes mutation-guard tests”; :469 — “over every pair”; :206 — “the approval and unchanged-since cases” | V3 |
| A-001 | QUALIFY | Current excerpts verified, historical immutability unproved | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial/advocate-brief.md:24 — “A finding whose cited text does not exist is dropped.” | Verification, not assumption |
| A-002 | QUALIFY | Runner application, not automatic skill source edits | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:866 — “apply the remediations” | V1/V3 narrowed mechanism |
| A-003 | QUALIFY | Early omissions do not prove final missing tests | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:757 — “decide whether a test exists that would FAIL if the behaviour broke” | V1 Round 2/V3 |
| A-004 | REJECT | Neither cleanliness nor an actual failure was measured | /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:699 — “the local `uv run ruff` is not the pinned 0.15.20” | No runtime claim |

### Advocate v3 (Round 2, verbatim from round2-advocate-v3.md)

#### Advocate: Variant 3 (opus:refactorer), Round 2 rebuttal

Abbreviations: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R06 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`; RSK = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`; CI = `.github/workflows/test.yml`; QA-B2 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/qa-task-validation-b2-report-part1.md`; QA-C = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/qa-task-validation-consolidated.md`.

Lines re-read first-hand this round (read-only; no git, no lint, no tests run): TF:194, 330, 336, 345, 384, 460, 472, 475, 502, 520, 611, 690, 699, 702, 723, 729, 735, 742, 745, 757, 763, 778, 800, 848, 864-875, 909, 955-970; D:220, 231-243, 479, 791, 798, 879, 887; R06:28, 30, 31, 32, 180; RSK:318-324; CI:29, 96-106; Makefile:47-50, 362; pyproject.toml:50-54; QA-B2:76, 121; QA-C:51; variant-1:35, 109, 144, 155; variant-2:1, 16, 36, 66, 85, 153; variant-3:200, 232, 287, 291, 306.

##### Responses to Criticisms

**C-006 (R3-005): Variant 2 says VALID-BLOCKING, narrowed to `valid_issue_number`. I hold VALID-MINOR.**

- *Steelman Variant 2.* TF:330 explicitly lets `record` import `predicates` "(`parse_utc`, `format_utc`, `valid_issue_number`)". TF:194 defines `valid_issue_number(value) -> bool`, which is a function. D:239 allows `predicates` "types only". A worker following TF:330 therefore writes an import that the design's text forbids. OQ-46 (TF:968) names only `predicates.parse_utc` and `format_utc`, not the third function.
- *What the evidence also shows:*
  1. **The design names a type that does not exist.** D:239 limits the import to "types only, for `Entry` fields that hold an issue number". The design's own `predicates` row (D:220) lists the dataclasses `Login`, `DiscoveredIssue`, `LabelEvent`, `IssueSnapshot`, `ProjectItem`, `MarkerEvidence` and `EditEvidence`. None of them is an issue-number type. The plan's `predicates` (TF:194) has none either, and `Entry.issue` is a plain `int` (TF:330: "`issue` equals its key", keys "converted to int"). Nothing in `predicates` can satisfy "types only, for an issue number". `valid_issue_number` (with `MAX_ISSUE_NUMBER`) is the only issue-number item there is. TF:330 is the closest workable reading of an under-specified design clause, not an invention.
  2. **The design's own enforcement accepts the import.** D:231 says `test_module_boundaries.py` "fails on any other `superclaude.*` import". The check works at module level, and `record -> predicates` is an allowed edge. No cycle can form, because `predicates` imports nothing (D:236).
  3. **Variant 2's line is drawn on disclosure, but its argument is about the constraint.** `parse_utc` and `format_utc` are functions too (TF:194), so "types only" excludes them as much as it excludes `valid_issue_number`. OQ-46 mentions them only as a folded-in note ("who parses the store's own timestamps"). It does not record a departure from D:239, and an Open Questions mention is not an authorization to break the design. If "explicit permission conflicts with binding restriction" makes the import blocking, it makes all three blocking. If the OQ-46 mention is enough for two of them, the defect is a missing deviation record, which is minor.
  4. **Earlier QA rated it minor.** QA-B2:76 graded the same finding MINOR ("OQ-46 mentions it but does not record it as a departure"), and QA-C:51 carried it as "note". Neither is binding, but both agree.
- *Verdict:* not DROP, because the departure is undeclared. Not blocking: no wrong code results, no cycle, the design's enforcement passes, and no design type exists that could be imported instead. **VALID-MINOR. Fix:** add one OQ line, as QA-B2:121 proposes: "`record` imports `parse_utc`, `format_utc` and `valid_issue_number` from `predicates`; this is the task's reading of D:239 'types only', because `predicates` defines no issue-number type (D:220)."

**C-009 (R3-008): Variant 2 says VALID-BLOCKING. I hold VALID-MINOR.**

- *Steelman Variant 2.* TF:875 says the `.dev/tasks` folder "is always staged". The project rule requires that state, and DF-07 (R06:30) adds the final staging "so the Task Log lines written after the commit stay staged". On the failed-staging branch, the worker keeps Done while that state is unmet, and no later step can repair it.
- *Why this is minor:*
  1. **The non-revert does not cause the unmet state.** If `git add .dev/tasks` fails, the paths stay unstaged whatever the status says. Reverting to Blocked would itself be another unstaged edit to the task file. The status label cannot satisfy or break the staging constraint. Only the failed command breaks it, and that is an environmental failure, not something the worker is told to do.
  2. **Done makes no false claim.** Each precondition of Done at TF:875 still holds on that branch: every item complete, `reflect_post` non-empty, `commit-result.md` exit 0, no unresolved blocking OQ. Staging is ordered "As the FINAL action of this item, in either branch", after the status is set. It is not a precondition of Done.
  3. **The branch is handled.** The failure "is logged in that section", and the `??` check (TF:875: "ensuring no `.dev/tasks` path shows `??`") is what detects it. The real gap is that the owner might not see the log line. That is an escalation weakness (gate_weakness), not wrong code, a deadlock or an unsafe action.
- *Contrast with X-008:* there, a reachable branch gets two contradictory rules and no resolution. Here, the branch gets one explicit, consistent rule.
- *Verdict:* **VALID-MINOR. Fix:** on a staging failure, re-run `git add .dev/tasks` once. If it fails again, put "staging failed: <stderr>; run `git add .dev/tasks` before `/sc:pr-submit`" as the first owner action in the Phase 10 note.

**X-006 and X-007: confirmed VALID-MINOR (my Round 1 position), coverage partially_covered.**

- The gaps are real:
  - TF:460 implements "a lost label, a voided approval or a changed Project status gives `revalidation_failed`". A search of TF:475 for "lost label", "voided" and "Project status" returns zero hits.
  - TF:460 implements "a failing save giving exit 6 `state_dir_unwritable` through `audit.stderr_fallback`". A search of TF:472 for "stderr_fallback", "unwritable", "failing save" and "append fail" returns zero hits.
- Three in-plan layers target exactly this omission:
  - TF:729: "a GAP is fixed by adding the missing test", followed by re-running G-1..G-11.
  - TF:757: decide "whether a test exists that would FAIL if the behaviour broke", and flag "missing negative and boundary cases".
  - TF:763: "the exact argv, exit codes, reasons ... must each be asserted".
- Both gaps sit upstream of those layers, so under my Round 1 rule (an omission that an in-plan guard catches is minor) they are minor. Variant 1's caveat stands: TF:729 matches tests by name through Grep, so only TF:757 and TF:763 read assertions. That is still two independent assertion-level lenses.

**X-005 (INF-016): confirmed covered.**

- NG-2 has an explicit argv scan "over every runner argv recorded across an idle, an eligible, a claimed, a rate-limited and a dry-run cycle" (TF:590). That scan also covers NG-3 ("no Project writes", D:70), because a Project write needs a non-GET call or a GraphQL `mutation`, and NG-2 forbids both.
- NG-1, NG-4 and NG-5 ("no daemon mode, no in-cycle retry, no automatic Orca retry", D:70) are guarded by absence: nothing in the plan builds them (variant-3:291).

**X-008: still VALID-BLOCKING. "Conditional" does not lower it under the binary rule.**

- *Why it is blocking:* the brief judges what "a worker following the task file would" do (advocate-brief:19). The defect is in the plan's text, not in a runtime event: the plan gives no consistent instruction for a reachable branch. The plan's author expected that branch, as the TF:699 parenthetical shows: "(the local `uv run ruff` is not the pinned 0.15.20)". DF-09 (R06:32) records that "bare `uv run ruff` resolves to 0.17.3". An unhandled branch that the plan itself expects is a plan defect whether or not it fires. Every plan branch is conditional in this sense, so "conditional" is not a severity level.
- *Precise failure path:*
  1. TF:699 requires "ensuring exit 0" but says an untouched-file finding is "recorded and NOT fixed".
  2. TF:735 requires "every row is PASS (a FAIL is fixed and its step re-run".
  3. TF:745 counts "Any command that fails" as a finding.
  4. TF:778: "IF it cannot be made to pass, HALT".
  - The worker therefore either records a false PASS (a false claim, which is blocking) or HALTs the whole task on a pre-existing condition outside its change set. The per-item escape hatch ("log the blocker ... mark this item complete") does not help, because TF:735 and TF:778 re-impose the PASS rule.
- *Narrowing (new evidence):* the risk sits almost entirely in G-4, not G-5.
  - CI runs `ruff check src/ tests/` and `ruff format --check src/ tests/` (CI:100-106) with dev dependencies that pin `"ruff==0.15.20"` (pyproject.toml:54). On a green master, G-5's pinned `uvx --offline ruff@0.15.20 format --check src/ tests/` (TF:702) is therefore expected to pass.
  - G-4 is `make lint` = `lint-architecture` + `uv run ruff check .` (Makefile:48-50). It runs an unpinned version over the whole repository, a wider path set than CI lints.
  - I did not run it. Whether it fails is unmeasured.
- *Concrete fix (smallest complete change):* the plan already uses this pattern for the known skip at `tests/swarm/test_cli_registration.py:127` (TF:745).
  1. Add one P1 item that runs `make lint 2>&1; echo "EXIT=$?"` and `uvx --offline ruff@0.15.20 format --check src/ tests/` on the unchanged tree and writes the output to `phase-outputs/test-results/p1-lint-baseline.txt`.
  2. In TF:699 and TF:702, define PASS as "exit 0, OR every finding is in a file listed in `p1-lint-baseline.txt` and outside the change set (verdict PASS-baseline)".
  3. In TF:735, accept PASS-baseline as PASS.
  4. In the TF:745 prompt, add "a lint finding listed in `p1-lint-baseline.txt` is not a finding", next to the existing skip carve-out.

**X-002: confirmed. VALID-MINOR, T-2 covered.**

- TF:336 defines `backoff_elapsed(entry, now)` as "(now >= `updated_at` + 10 min)", without D:479's "and `attempts` < 3". That is a helper-contract wording defect.
- The behaviour is still covered. TF:460 applies "a `failed` entry past backoff with attempts below 3", `fail` abandons at 3 (TF:336), and the transition tests span "T-1 to T-13" (TF:345). This matches Variant 2's "covered with a minor wording defect".

**Citation re-verification (my Round 1 statement).**

- Every TF, D, R06, RSK, CI and variant citation in my Round 1 statement matches the current files, with one exception.
- **Correction:** my Round 1 statement put the lint command at "Makefile:49" and the `lint:` target at ":47", and then "conceded" that the card was one line off. That concession was backwards. The `lint:` target is at Makefile:48 and `uv run ruff check .` is at Makefile:50. Variant 3's card cites Makefile:50 (variant-3:26, :327), which is correct. The error was in my advocate statement, not in the card.

##### Updated Assessment

Only X-001 and X-008 are blocking: X-001 because Step 10.6 tells the runner to "apply the remediations" after the only commit with no gate re-run (TF:866, 875), although the reflect skill only authors a remediation task (RSK:321, 324); X-008 because a lint pass rule the plan itself expects to be broken (TF:699, 735, 745, 778) leaves no consistent passing path, fixed by a P1 lint baseline and a PASS-baseline verdict. C-006 and C-009 stay minor: C-006 is an unrecorded reading of a design clause whose named issue-number type does not exist (D:220, 239), and C-009 is an escalation gap on an explicitly handled failure branch (TF:875). X-006 and X-007 are real coverage gaps, but three in-plan lenses target them (TF:729, 757, 763), so they are minor. I concede C-007 to DROP because DF-46 (R06:180) declares the optional installed-copy comparison, and I correct my own Round 1 Makefile citation (the card's Makefile:50 was right).

##### New Evidence

- **No issue-number type exists in `predicates`.** D:220 and TF:194 list `predicates`' dataclasses, and none of them is an issue-number type; `Entry.issue` is an `int` (TF:330). This empties D:239's "types only, for `Entry` fields that hold an issue number" of any satisfiable content, which supports reading C-006 as a recording defect.
- **The C-006 standard is inconsistent.** `parse_utc` and `format_utc` are functions (TF:194), exactly like `valid_issue_number`. OQ-46 (TF:968) mentions them without recording a D:239 departure. A blocking rule based on the constraint would cover all three names, not one.
- **Earlier QA graded C-006 minor:** QA-B2:76 ("MINOR ... OQ-46 mentions it but does not record it as a departure"), with its fix at QA-B2:121, and QA-C:51 ("note").
- **X-008 risk sits in G-4, not G-5.** CI pins ruff 0.15.20 (pyproject.toml:54) and enforces check and format over `src/ tests/` (CI:100-106). The unpinned, whole-repo `uv run ruff check .` (Makefile:50) is the exposed gate.
- **The X-008 fix pattern already exists in the plan.** TF:745 exempts a known pre-existing skip: "exists on master, is outside this change set and is not a finding".
- **C-009 ordering.** Staging is "the FINAL action of this item, in either branch and after the status line and the Execution Log entry are written" (TF:875). Done's preconditions do not include staging, so keeping Done is not a false claim.
- **C-007 declared.** R06:180 (DF-46): "The installed copy and the project `.claude/` copy are compared only when present." TF:384 implements exactly that.
- **X-001 still undeclared.** R06 contains zero occurrences of "remediat". R06:30 declares only "staging only; no second commit".
- **Task-file timing.** The task file is timestamped 18:43, before the `reflect/` folder (18:44) and the variant copies (19:15). This is consistent with no edit during the review, but does not prove it.

##### Shared Assumption Responses

- **A-001: QUALIFY.** Every card excerpt I re-checked exists at its cited line now (list above), and the task file's 18:43 timestamp predates the review folder. That it was never edited during the review is consistent with this but unproved, and my own Round 1 Makefile:49 miscite shows why each line must be re-read rather than assumed.
- **A-002: QUALIFY.** The skill only authors remediation: "reflect AUTHORS but NEVER runs `/task` or `/sc:implement`" (RSK:324). Edits outside `.dev/tasks` arise only from the runner's "apply the remediations" instruction (TF:866), which is why X-001 is retained.
- **A-003: QUALIFY.** Scenario gaps upstream of TF:729, 757 and 763 are recoverable, so they are minor. Defects inside a gate's own pass rule (X-008) or after every gate (X-001) are not recoverable.
- **A-004: REJECT.** A clean tree was never measured. CI's pinned check makes G-5 likely clean (pyproject.toml:54; CI:100-106), but G-4's unpinned `uv run ruff check .` over the whole repository (Makefile:50) is unverified, and TF:699 expects it to differ.

##### Point Positions

| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
|---|---|---|---|---|
| S-001 | YAML | - | variant-2:1 - "the reviewer returned markdown instead of the requested YAML" | - |
| S-002 | UNION | V2 AC rows + V3 INF register, deduplicated | variant-2:36 - "Criterion \| Judgement \| Implementation items \| Test-writing items" | V2 (AC granularity) |
| S-003 | BINARY | - | advocate-brief:18 - "Binary severity (decide from evidence, not from the reviewer's label)" | - |
| S-004 | ENUM | V2 "Drift" maps to coverage_gap | RSK:324 - "reflect AUTHORS but NEVER runs `/task` or `/sc:implement`" (the taxonomy audits completed work; this is a plan) | - |
| C-001 | VALID-MINOR | OQ-51 declares the working-tree branch | TF:848 - "run Step 10.6 over a base the owner names instead of `plans/base-sha.txt`" | V1 |
| C-002 | VALID-MINOR | same pin, different supply mechanism | TF:611 - "supplied ad hoc exactly as `.github/workflows/test.yml:29` does"; CI:29 - "uv pip install -e" | V1 |
| C-003 | VALID-MINOR | P10 staged allowlist backstop | TF:723 - "`git diff --exit-code pyproject.toml Makefile; echo \"EXIT=$?\"`" | V1 |
| C-004 | VALID-MINOR | uncapped per-phase loops only; Final re-run HALTs | TF:690 - "IF FAILED, fix the cause (never weaken an assertion) and re-run until PASSED" | V2 (postfix HALT exists, TF:778) |
| C-005 | VALID-MINOR | M4 prompt names whole directories | TF:800 - "everything under src/superclaude/cli/issue_watch/, the two registration lines" | - |
| C-006 | VALID-MINOR | undeclared reading; no issue-number type exists (D:220) | D:239 - "`predicates` (types only, for `Entry` fields that hold an issue number)"; TF:330 - "(`parse_utc`, `format_utc`, `valid_issue_number`)" | - |
| C-007 | DROP | declared by DF-46 | R06:180 - "The installed copy and the project `.claude/` copy are compared only when present." | V1, V2 |
| C-008 | VALID-MINOR | conditional; no unrelated hunk identified | TF:502 - "shows only these added lines"; TF:520 - "fix any finding inside those files" | - |
| C-009 | VALID-MINOR | handled branch; escalation gap only | TF:875 - "a failure of this staging command is logged in that section and never reverts the Done status" | - |
| C-010 | V3 | blocking: X-001, X-008; minor: R2-001, R2-002, C-006, C-009, rest | TF:735 - "every row is PASS (a FAIL is fixed and its step re-run" | V2 (two minor gaps); V1/V2 (C-007 DROP) |
| C-011 | YES | - | variant-1:109 - "The Phase 3 items were not re-read in this session" | - |
| X-001 | VALID-BLOCKING | runner's "apply", not the skill, edits source | TF:866 - "apply the remediations the skill offers under `--remediate`"; RSK:324 - "reflect AUTHORS but NEVER runs `/task`" | V1 (co-finder) |
| X-002 | VALID-MINOR | T-2 covered | TF:460 - "a `failed` entry past backoff with attempts below 3 first checks the day cap" | V2 (wording-defect framing) |
| X-003 | partially_covered | authorized DF-05, not a defect | TF:735 - "the whole `make test` run is left to CI, decision DF-05" | - |
| X-004 | partially_covered | authorized DF-05, not a defect | TF:909 - "the local gate is the named test subset (G-2) plus `make lint`, not `make test`" | - |
| X-005 | covered | NG-2/NG-3 argv scan; NG-1/4/5 by absence | D:70 - "NG-5 no daemon mode, no in-cycle retry, no automatic Orca retry" | - |
| X-006 | VALID-MINOR | INF-146 partially_covered | TF:460 - "a failing save giving exit 6 `state_dir_unwritable` through `audit.stderr_fallback`" (absent from TF:472) | V2 (gap real) |
| X-007 | VALID-MINOR | AC-6 partially_covered | TF:460 - "a lost label, a voided approval or a changed Project status gives `revalidation_failed`" (absent from TF:475) | V2 (gap real) |
| X-008 | VALID-BLOCKING | fix: P1 lint baseline + PASS-baseline verdict; risk is G-4 | TF:699 - "ensuring exit 0; a finding in a file this task did not touch ... is recorded and NOT fixed" | - |
| X-009 | YES | corroborated by V2 test-file table | diff-analysis:53 - "Several automatic \"none\" mappings declared wrong (INF-108, INF-122, INF-135, INF-147, INF-153)" | - |
| A-001 | QUALIFY | current excerpts verified; immutability unproved; my Makefile:49 cite corrected to :50 | TF:864 - "--mode post --remediate --diff <BASE SHA>..HEAD" | - |
| A-002 | QUALIFY | - | RSK:321 - "`--remediate --depth deep` → **MDTM route**: `task-builder` builds the MDTM task file; the user runs `/task <path>`" | V2 (in part) |
| A-003 | QUALIFY | - | TF:757 - "decide whether a test exists that would FAIL if the behaviour broke" | - |
| A-004 | REJECT | G-5 likely clean via CI pin; G-4 unmeasured | Makefile:50 - "uv run ruff check ."; TF:699 - "(the local `uv run ruff` is not the pinned 0.15.20)" | - |

## Round 2.5 — Invariant Probe

Fault-finder: opus, read-only. It returned 15 findings (2 ADDRESSED, 13 UNADDRESSED: 3 HIGH, 5 MEDIUM, 5 LOW). The full table is in invariant-probe.md.
- HIGH UNADDRESSED: INV-001 (the X-001 fix options do not converge, and only report-only plus HALT preserves DF-07), INV-004 (the X-008 rule pair recurs at per-phase, Gate A-D and Final/M4 re-run sites beyond TF:699/702/735/745), INV-005 (G-2 at TF:693 has the same exit-0 versus recorded-not-fixed contradiction).
- MEDIUM UNADDRESSED (warnings): INV-002, INV-003, INV-006, INV-008, INV-010.

## Round 3: Final Arguments

Round 3 skipped: depth=standard

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | v1, v3 (YAML card schema) | 95% | Unanimous. v2's own card records that the reviewer returned markdown instead of the requested YAML (variant-2:1). |
| S-002 | Union (v2 AC rows + v3 INF register + v1 T rows) | 95% | Unanimous UNION. Overlapping AC, INF and T units are deduplicated in the merged coverage_resolution. |
| S-003 | v3 (binary blocking/minor) | 95% | Unanimous BINARY. The advocate brief requires severity decided from evidence on a binary scale (advocate-brief:18). |
| S-004 | v1, v3 (brief category enum) | 95% | Unanimous ENUM. v2's "Drift" maps to coverage_gap, and the deviation taxonomy stays separate from category. |
| C-001 | v1 (R1-003 minor) | 95% | Unanimous VALID-MINOR. TF:848 names a base the owner chooses, but the Step 10.6 verbatim prompt has no substitution text. OQ-51 declares the branch itself. |
| C-002 | v1 (R1-004 minor) | 95% | Unanimous VALID-MINOR. Same pin, different supply mechanism (TF:611 against test.yml:29). |
| C-003 | v1 (R1-005 minor) | 95% | Unanimous VALID-MINOR. The P10 staged-path allowlist backstops the G-10 blind spot (confirmed ADDRESSED by INV-014). |
| C-004 | v3 (R3-003 minor) | 95% | Unanimous VALID-MINOR. Per-phase loops are uncapped (TF:690), while the Final post-fix re-run HALTs (TF:778). |
| C-005 | v3 (R3-004 minor) | 95% | Unanimous VALID-MINOR. final-change-set.md is written once (TF:742) and reviewed as the full set by M4 (TF:800). |
| C-006 | v3 (R3-005 minor) | 67% | Majority 2/3 MINOR (v1, v3). v2 held BLOCKING for valid_issue_number and did not concede. D:239 "types only" against TF:330. |
| C-007 | v1, v2 (not a defect; R3-006 dropped) | 95% | Unanimous DROP, conceded by v3. Declared by DF-46 (R06:180), "compared only when present". |
| C-008 | v3 (R3-007 minor) | 95% | Unanimous VALID-MINOR. Conditional on a pre-existing format hit in main.py (TF:502 against TF:520). |
| C-009 | v3 (R3-008 minor) | 67% | Majority 2/3 MINOR (v1, v3). v2 held BLOCKING ("always staged") and did not concede. Done's preconditions exclude staging (TF:875). |
| C-010 | v3 (blocking set X-001, X-008) | 67% | v1 and v2 used the OTHER token and v3 used V3. In substance v1 and v3 name the same blocking set (X-001, X-008), which is a 2/3 majority. v2 adds C-006 and C-009, outvoted on those points. |
| C-011 | All (disclosures valid; weight checked evidence) | 95% | Unanimous YES. v1 discloses unread Phases 1-3 (variant-1:155) and v3 discloses unread Gate D (variant-3:306). |
| X-001 | v3 (R3-001 blocking; R1-002 co-source) | 95% | Unanimous VALID-BLOCKING, conceded by v1 and v2. The runner's "apply the remediations" (TF:866) after the single commit, with staging limited to .dev/tasks (TF:875). |
| X-002 | v1 (R1-001 minor finding); v2, v3 (T-2 covered) | 95% | Unanimous VALID-MINOR with T-2 covered. TF:460 applies attempts below 3 in the cycle, and Step 4.1c's wording drops the conjunct. |
| X-003 | v1, v3 (INF-123 partially_covered) | 95% | Unanimous partially_covered, conceded by v2. Declared DF-05, not a defect (TF:735). |
| X-004 | v3 (INF-155 partially_covered) | 95% | Unanimous partially_covered, conceded by v2. Declared DF-05 (TF:909). |
| X-005 | v2, v3 (INF-016 covered) | 95% | Unanimous covered, conceded by v1. NG-2/NG-3 argv scan, NG-1/4/5 by absence (D:70). |
| X-006 | v2 (R2-002 minor; INF-146/AC-14 partially_covered) | 95% | Unanimous VALID-MINOR. TF:460 names the stderr fallback, which is absent from the TF:472 test list. INV-008 (MEDIUM) challenges whether the backstop fires. |
| X-007 | v2 (R2-001 minor; AC-6 partially_covered) | 95% | Unanimous VALID-MINOR. TF:460 lists the revocation cases, which are absent from TF:475. INV-008 and INV-009 apply. |
| X-008 | v3 (R3-002 blocking) | 95% | Unanimous VALID-BLOCKING (v1 and v2 conditional on A-004, which was rejected 3/3). TF:699 "ensuring exit 0" against "recorded and NOT fixed", plus TF:735 every row PASS. |
| X-009 | v3 (automatic mapping corrections) | 95% | Unanimous YES, corroborated by v2's test-file table. |
| A-001 | QUALIFY (shared) | 90% | Unanimous QUALIFY. Current excerpts verified, immutability during review unproved, so the merge-executor re-Reads every cited line. |
| A-002 | QUALIFY (shared) | 90% | Unanimous QUALIFY. The skill only authors remediation (RSK:324), and source edits come from the runner's apply instruction (TF:866). |
| A-003 | QUALIFY (shared) | 90% | Unanimous QUALIFY. Scenario gaps upstream of the TF:729/757/763 backstops are recoverable, and gate-rule defects are not. |
| A-004 | REJECT (shared; supports v3) | 95% | Unanimous REJECT. A lint-clean tree was never measured, and G-4's unpinned `uv run ruff check .` (Makefile:50) is unverified. |

## Convergence Assessment
- Points resolved: 28 of 28 (U-001..U-005 are excluded from the denominator)
- Alignment: 100% (25 unanimous, 3 majority 2/3: C-006, C-009, C-010)
- Threshold: 80%
- Taxonomy coverage: L1 covered (S-001, S-003, S-004, C-002), L2 covered, L3 covered
- Invariant gate: CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-001, INV-004, INV-005
- Warning: 5 MEDIUM-severity UNADDRESSED invariant(s) detected. Items: INV-002, INV-003, INV-006, INV-008, INV-010
- Status: BLOCKED_BY_INVARIANTS (agreement 1.00 >= 0.80 and taxonomy covered, but HIGH-severity UNADDRESSED invariants exist; no further round is available at depth=standard)
- Unresolved points: no diff point is unresolved. Unresolved invariants: INV-001, INV-004, INV-005
- Termination: Convergence: 100% (max rounds reached for depth=standard)
