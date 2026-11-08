## Advocate: Variant 1 (sonnet:analyzer), Round 2 rebuttal

Path shorthand: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`.

Lines re-read first-hand this round: TF:326-395, 455-524, 595-624, 686-880, 955-970; R:30-31, 180; D:233-242.

### Responses to Criticisms

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

### Updated Assessment

Variant 3's X-001 is the one unconditional blocking defect: Step 10.6 tells the runner to apply `--remediate` edits after the single DF-07 checkpoint commit (TF:866), and Step 10.7 stages only `.dev/tasks` (TF:875), so the final tree is neither gated nor committed. X-008 is blocking only if the tree is not lint-clean, because TF:699 forbids the fix while TF:735 requires every gate row to be PASS. After re-reading TF:848, TF:960, TF:778, R:31, R:180 and the TF:729, 757 and 763 backstops, I reduce C-001, X-006 and X-007 to minor and drop C-007. V3 is the most accurate card overall, and V2's coverage findings stand as real but minor because three review layers and an authorised fixer target the same gap.

### New Evidence

- TF:848 and TF:960 (OQ-51) show that the withdrawn-commit branch is explicitly handled in Step 10.2 and declared as an Open Question (C-001).
- TF:778 shows a HALT on a failing re-run. R:31 declares "with no extra gate". Both limit C-004.
- R:180 (DF-46) declares that the installed marker copy is compared only when present (C-007).
- TF:729, 757, 763 and 769 are backstops for X-006 and X-007. Only the F6 and F8 lenses read assertions.
- TF:735 requires every Step 9.19 gate row to be PASS. This turns the X-008 contradiction into a concrete deadlock if the baseline is dirty.
- D:239 reads "`predicates` (types only, for `Entry` fields that hold an issue number)". TF:968 (OQ-46) only partly discloses the widening (C-006).
- No card ran a lint baseline. A-004 is therefore still unmeasured.

### Shared Assumption Responses

- A-001: QUALIFY. Every excerpt I checked exists, but the cards cite parallel steps (TF:351, 387 and 690 share wording, as do TF:391, 517 and 699), so line numbers differ without any fabrication.
- A-002: QUALIFY. TF:866 tells the runner to "apply the remediations the skill offers under `--remediate`", so out-of-`.dev/tasks` edits are possible; by V3's reading of the skill, the skill itself only authors a corrective task.
- A-003: QUALIFY. Item text is dense and Step 9.17 and the Final lenses (TF:757, 763) are real backstops, but 9.17 matches names, not assertions, so a missing scenario is a legitimate but minor pre-execution finding.
- A-004: REJECT. Nothing proves the tree is lint-clean, and the TF:699 parenthetical about the unpinned local ruff shows the author expected untouched-file findings.

### Point Positions

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
