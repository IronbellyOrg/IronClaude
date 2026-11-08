## Advocate: Variant 2 (haiku:qa)

### Position Summary

Variant 2 supplies the strongest scenario-level coverage analysis: its two findings distinguish implementation instructions and helper tests from tests that would detect broken integration, rather than treating directory-wide execution as proof (V2:16–19, 34–51). The merged verdict should nevertheless be OTHER: retain those two planned-test-writing gaps, incorporate the verified sequencing and constraint conflicts below, and do not count authorized substitutions as defects. Blocking here describes deficient task instructions, sometimes on an explicitly identified conditional path—not observed implementation failures or an observed lint-dirty baseline; no commands or tests were run.

### Steelman: Variant 1

Variant 1's strongest argument is that an executable plan needs exact operational instructions as well as behavioral coverage. It correctly identifies the missing withdrawn-commit prompt arm, the distinction between the xdist version pin and installation mechanism, and G-10's staged-change blind spot while acknowledging the later allowlist safeguard (V1:37–85; T:848–864, 611, 723, 851; CI:29). Its external-anchor checks and disclosure of unread sections make its evidence boundary unusually inspectable (V1:129–156). Its observation that POST remediation can change the tree after the checkpoint is substantive and survives source verification, even though its minor label does not survive the debate's binary severity rule (V1:22–36; T:866, 875; B:19).

### Steelman: Variant 3

Variant 3's strongest argument is evidence freshness across state changes: a gate, snapshot or checkpoint describes one tree, not every later repaired tree. Its POST-remediation finding and final-change-set freshness finding identify real ordering hazards, while its import analysis notices the design's types-only qualifier that module-edge checks alone do not enforce (V3:6–16, 38–55; T:742, 778, 800, 864–875, 605; D:239). Its wider requirement register also corrects real automatic-mapping errors; the relevant predicate, cycle and AST test-writing items do exist (V3:96–99, 152–155, 188–191, 236–239; T:206, 469, 599, 608, 690). The lint and main.py findings are strongest when framed as conditional error-path instruction conflicts, not claims that this checkout has already failed either formatter (V3:17–28, 66–74; T:502, 520, 699–702).

### Key Strengths Claimed

1. **Meaningful coverage units.** Variant 2 separates 25 ACs, overlapping requirement rows, and named-test creation/execution mappings; its counts are not additive measures of independent requirements (V2:23–34, 154). Use the union of the cards' units, keeping their identities and overlaps, rather than replacing the scenario analysis with token matches (B:33; V2:30).
2. **R2-001 remains a concrete planned-test-writing gap.** Step 6.2 separately requires lost-label, voided-approval and changed-Project-status rejection at the final reread, but Step 6.7's explicit reread cases name closure, changed assignees, timeout and reserved-call refusal (T:460, 475). A mutant that reuses initial approval or Project evidence can pass initial predicate tests and the enumerated reread cases. Require independently eligible-then-revoked final-read cases asserting the specified reason, no entry and no launch; this is not a claim that such a mutant already exists (V2:16).
3. **R2-002 remains a concrete planned-test-writing gap.** The fallback formatter's unit test and successful cycle appends do not demonstrate that run_cycle calls the formatter when append or the final save fails (T:212, 460, 472). The CLI config-error and reset fallback cases exercise different entry paths, not these cycle integration branches (T:505, 508). Require separate append-failure and final-save-failure injections through run_cycle, checking the five-key fallback, the specified reason/exit and released lock (T:197, 460; V2:17).
4. **Deviation authority changes the baseline.** The affected-subset gate and pinned formatter are declared choices, not unfulfilled literal make-test/unpinned-format requirements (R:28, 32; T:909, 912). Covered under that authorized baseline does not mean equivalent to full-suite local execution (V2:151–152).
5. **Evidence boundary.** These are judgments about instructions and planned tests, not passing implementation results (V2:10, 34, 149). Later semantic tracing and mutation-oriented QA are genuine recovery mechanisms, not evidence that the particular missing tests have already been written (T:729, 757, 763).

### Weaknesses in Variant 1

- **T-2 is not absent just because its literal token is absent from a helper description.** Step 4.4 explicitly assigns one test per T-1..T-13 row, Step 6.2 applies attempts below 3, and Step 6.7 requires retry/backoff and third-failure abandonment behavior (T:345, 460, 475). Drop R1-001 as a requirement-coverage defect; a request to repeat the conjunct beside the helper would be a clarity preference, not proof of missing behavior (V1:10–14).
- **Conditional does not automatically mean minor.** The withdrawn-commit branch is expressly supported, but Step 10.6 still requires the skipped branch's base-sha.txt and permits only a SHA substitution in the unchanged BASE..HEAD prompt (T:848, 860–864, 960). OQ-51 authorizes the alternate change-set choice; it does not supply compatible verbatim instructions. R1-003 is blocking on that branch, as is ungated source remediation under R1-002 (B:19; T:866, 875).
- **Local gate weakness is not total absence of protection.** Retain R1-005 as a minor redundant-check weakness, not an assertion that the normal checkpoint can commit protected files: Step 10.3's explicit allowlist HALTs on them (T:723, 851; V1:78).
- **A new xdist preflight is not established as missing evidence.** The mechanism wording is inaccurate, but the register already records successful offline resolution on this host (T:611; CI:29; R:48). Keep the wording correction; do not assert an observed cache failure or invent a new mandatory preflight.
- **Reading limits affect weight, not automatic admissibility.** The card itself says some coverage judgments were based on item purpose rather than line-level inspection and that research/06 was unread (V1:149–156). Such rows need source verification before overruling verified scenario-level findings.

### Weaknesses in Variant 3

- **Two covered audit/revalidation rows are too coarse.** An ordinary audit line for every exit does not prove fallback wiring, and one closed-issue reread case does not prove approval and Project evidence are recomputed (V3:200–203, 232–235; T:460, 472, 475). Preserve Variant 2's partially_covered judgments for the concrete planned tests.
- **The marker comparison is authorized.** DF-46 explicitly prescribes installed/project comparisons only when present (R:180; T:384). The generic no-real-HOME adequacy lens deserves an exception clarification, but R3-006 cannot be retained as an unauthorized behavioral departure or used to replace the mandated comparison (T:757; B:10, 21).
- **R3-003 combines different issues.** A new lens gate after every repair is expressly unnecessary under DF-08, and the cited postfix branch actually contains HALT if the rerun cannot pass (R:31; T:778, 793). Raw test-repair loops lacking a numerical cap are not themselves proof of deadlock, nor proof that the two-cycle independent QA cap is absent (T:690, 739). Drop this composite finding; retain the separately evidenced snapshot-freshness defect C-005 instead.
- **R3-005 must be narrowed.** OQ-46 records predicates.parse_utc and format_utc as the timestamp-parsing choice, so calling all three helper imports undeclared is inaccurate (T:968). The remaining valid_issue_number function import is not named in that exception and conflicts with the types-only design rule (T:330; D:239). Retain only that residual constraint conflict, not a demand to undo the recorded UTC-helper choice; the module-edge test alone does not enforce the distinction (T:605).
- **Conditional lint conflicts must not become invented execution evidence.** The text requires exit zero, prohibits fixing untouched-file findings, and requires every final row PASS (T:699, 702, 735). Retain the unresolved nonzero-baseline branch as a blocking instruction conflict, but do not claim an observed baseline failure, unconditional impossibility, or absence of every HALT elsewhere: T:778 explicitly supplies one for later postfix reruns. Likewise C-008 concerns a possible out-of-registration formatter hit; none was observed (T:502, 520).

### Concessions

- Variant 2 returned Markdown instead of the requested YAML, and its MEDIUM/Drift fields are not the merge's binary-severity/category-enum schema (V2:1, 14–17; B:18–21, 32–35). Normalize the merged register to YAML, BINARY and ENUM; retain authorization/deviation status as separate explanatory metadata.
- Variant 2's praise of the normal checkpoint was not a rebuttal to post-commit remediation, and it missed the withdrawn-commit arm (V2:153; T:848, 860–875). The comparison's description of Variant 2 as affirmatively finding “Not a defect” overstates that sentence: silence and normal-path praise are not an examined rejection.
- The two Variant 2 findings are blocking **at the concrete planned-test-writing boundary** under B:19. This is not a prediction that every executor will omit the tests: Step 9.17, the adequacy lens and the AC lens can discover and repair both gaps (T:729, 757, 763). The merged register should preserve that counterevidence rather than claim the whole plan has no coverage backstop.
- R3-004 is more than a cosmetic line-count issue: the aggregate embeds the main.py diff and coverage/gate tables before later fixes/reruns, and M4 is directed to it as the full change set (T:742, 778, 800). A required final evidence artifact can therefore describe an older tree. M4 also opens current implementation paths, so this does not prove that all repaired code escapes review.
- R3-008 identifies a completion-contract problem: explicitly retaining Done after staging fails is incompatible with the required staged task package (T:875; R:30). The correction needs neither a second commit nor rollback of implementation: failed required staging must remain an unmet completion condition.
- The blocking set is C-001, C-005, C-006 (valid_issue_number only), C-008, C-009, X-001, X-006, X-007 and X-008. C-008 and X-008 are conditional instruction conflicts; no failing formatter baseline is asserted. The strict binary rubric upgrades actual constraint/required-evidence gaps even where the originating reviewer called them minor (B:19–20).

### Shared Assumption Responses

- **A-001 — QUALIFY.** The disputed passages used here were checked against the current task/design/register; that does not establish unchanged history or validate every citation in every card (B:24).
- **A-002 — ACCEPT.** Step 10.6 explicitly directs applying remediation for Regression or unauthorized Drift, after the checkpoint; it does not restrict those fixes to reports (T:864–866, 872).
- **A-003 — QUALIFY.** Item text supports assessing explicit planned coverage, but an unnamed scenario is not guaranteed to remain unwritten: semantic tracing and mutation-oriented lenses can require the missing test later (T:729, 757, 763).
- **A-004 — REJECT.** No lint/format baseline was executed in this review, so cleanliness is unestablished; reject assuming it, without asserting the opposite (R:49–50; T:699–702).

### Point Positions

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
