## Advocate: Variant 3 (opus:refactorer), Round 2 rebuttal

Abbreviations: TF = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; D = `docs/designs/issue-watcher.md`; R06 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`; RSK = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`; CI = `.github/workflows/test.yml`; QA-B2 = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/qa-task-validation-b2-report-part1.md`; QA-C = `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/qa-task-validation-consolidated.md`.

Lines re-read first-hand this round (read-only; no git, no lint, no tests run): TF:194, 330, 336, 345, 384, 460, 472, 475, 502, 520, 611, 690, 699, 702, 723, 729, 735, 742, 745, 757, 763, 778, 800, 848, 864-875, 909, 955-970; D:220, 231-243, 479, 791, 798, 879, 887; R06:28, 30, 31, 32, 180; RSK:318-324; CI:29, 96-106; Makefile:47-50, 362; pyproject.toml:50-54; QA-B2:76, 121; QA-C:51; variant-1:35, 109, 144, 155; variant-2:1, 16, 36, 66, 85, 153; variant-3:200, 232, 287, 291, 306.

### Responses to Criticisms

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

### Updated Assessment

Only X-001 and X-008 are blocking: X-001 because Step 10.6 tells the runner to "apply the remediations" after the only commit with no gate re-run (TF:866, 875), although the reflect skill only authors a remediation task (RSK:321, 324); X-008 because a lint pass rule the plan itself expects to be broken (TF:699, 735, 745, 778) leaves no consistent passing path, fixed by a P1 lint baseline and a PASS-baseline verdict. C-006 and C-009 stay minor: C-006 is an unrecorded reading of a design clause whose named issue-number type does not exist (D:220, 239), and C-009 is an escalation gap on an explicitly handled failure branch (TF:875). X-006 and X-007 are real coverage gaps, but three in-plan lenses target them (TF:729, 757, 763), so they are minor. I concede C-007 to DROP because DF-46 (R06:180) declares the optional installed-copy comparison, and I correct my own Round 1 Makefile citation (the card's Makefile:50 was right).

### New Evidence

- **No issue-number type exists in `predicates`.** D:220 and TF:194 list `predicates`' dataclasses, and none of them is an issue-number type; `Entry.issue` is an `int` (TF:330). This empties D:239's "types only, for `Entry` fields that hold an issue number" of any satisfiable content, which supports reading C-006 as a recording defect.
- **The C-006 standard is inconsistent.** `parse_utc` and `format_utc` are functions (TF:194), exactly like `valid_issue_number`. OQ-46 (TF:968) mentions them without recording a D:239 departure. A blocking rule based on the constraint would cover all three names, not one.
- **Earlier QA graded C-006 minor:** QA-B2:76 ("MINOR ... OQ-46 mentions it but does not record it as a departure"), with its fix at QA-B2:121, and QA-C:51 ("note").
- **X-008 risk sits in G-4, not G-5.** CI pins ruff 0.15.20 (pyproject.toml:54) and enforces check and format over `src/ tests/` (CI:100-106). The unpinned, whole-repo `uv run ruff check .` (Makefile:50) is the exposed gate.
- **The X-008 fix pattern already exists in the plan.** TF:745 exempts a known pre-existing skip: "exists on master, is outside this change set and is not a finding".
- **C-009 ordering.** Staging is "the FINAL action of this item, in either branch and after the status line and the Execution Log entry are written" (TF:875). Done's preconditions do not include staging, so keeping Done is not a false claim.
- **C-007 declared.** R06:180 (DF-46): "The installed copy and the project `.claude/` copy are compared only when present." TF:384 implements exactly that.
- **X-001 still undeclared.** R06 contains zero occurrences of "remediat". R06:30 declares only "staging only; no second commit".
- **Task-file timing.** The task file is timestamped 18:43, before the `reflect/` folder (18:44) and the variant copies (19:15). This is consistent with no edit during the review, but does not prove it.

### Shared Assumption Responses

- **A-001: QUALIFY.** Every card excerpt I re-checked exists at its cited line now (list above), and the task file's 18:43 timestamp predates the review folder. That it was never edited during the review is consistent with this but unproved, and my own Round 1 Makefile:49 miscite shows why each line must be re-read rather than assumed.
- **A-002: QUALIFY.** The skill only authors remediation: "reflect AUTHORS but NEVER runs `/task` or `/sc:implement`" (RSK:324). Edits outside `.dev/tasks` arise only from the runner's "apply the remediations" instruction (TF:866), which is why X-001 is retained.
- **A-003: QUALIFY.** Scenario gaps upstream of TF:729, 757 and 763 are recoverable, so they are minor. Defects inside a gate's own pass rule (X-008) or after every gate (X-001) are not recoverable.
- **A-004: REJECT.** A clean tree was never measured. CI's pinned check makes G-5 likely clean (pyproject.toml:54; CI:100-106), but G-4's unpinned `uv run ruff check .` over the whole repository (Makefile:50) is unverified, and TF:699 expects it to differ.

### Point Positions

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
