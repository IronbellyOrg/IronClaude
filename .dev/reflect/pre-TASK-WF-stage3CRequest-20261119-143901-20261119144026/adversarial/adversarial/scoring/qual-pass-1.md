# Qualitative scoring: pass 1 (input order V1, V2, V3)

- Evaluator role: neutral, not an advocate. Step 3 (base selection), qualitative layer, pass 1.
- Variants: `variant-1-original.md` (analyzer, sonnet), `variant-2-original.md` (qa, haiku), `variant-3-original.md` (refactorer, opus).
- Source input: `.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/source.md` (spec); work under audit: the plan `TASK-WF-stage3CRequest-20261119-143901.md` in the same folder.
- Artifact conventions: card template and `## Review severity rule` of `src/superclaude/agents/reflect-reviewer.md:71-123` (grade prefix first in "What diverged", affected action named on Blocking rows, label is not the grade, form-only defects are Notes).
- Method: 30 binary criteria, Claim-Evidence-Verdict. MET needs a quote or section reference from that variant's own text; no partial credit. Debate rounds (`rounds/r1-*.md`, `rounds/r2-*.md`) were used only for facts the advocates verified or conceded.
- Facts taken from the debate: V1 row 4 is over-graded (should be Note; conceded r2-v1.md:16); V1's paragraph at variant-1:25 is a misplaced, garbled Note (conceded r2-v1.md:18, :24); V2's "not an additional plan deviation" (variant-2:33) was conceded wrong (r2-v2.md:25, :32); V2's 45-unit count was conceded padded and its adherent count corrected (r2-v2.md:19); V3's "drops the spec's way of checking byte identity" (variant-3:19) was conceded an overstatement, since source.md:24 is provenance, not an acceptance check (r2-v3.md:20); the only "83 passed" record belongs to the carry-scope variant, so V3's "no artifact backs it" (variant-3:37) is correct (r2-v1.md:64, r2-v2.md:74).
- Facts checked directly by this evaluator: source.md:58-63 has 4 "not to be done" bullets; V1's unit list (variant-1:29) sums to 4+6+3+5+3+1+1 = 23, not the stated 22; V3's unit list (variant-3:24) sums to 2+1+6+5+5+4+3+4 = 30, matching its stated 30 and 25 + 5 = 30.

## Completeness

| Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence | V3 verdict | V3 evidence |
|---|---|---|---|---|---|---|
| Comp.1 Audits every spec requirement | NOT MET | Unit list (variant-1:29) is "4 changes ... 6 Task 1 acceptance ... 3 Task 2 acceptance ... 5 not to be done ... 3 known limits, branch, entry condition"; the "Constraints to carry" section (source.md:71-77) and the owner-go gate (source.md:3) are not audited anywhere in the card | MET | "Spec units audited: 45 — the matrix's 43 inferred units, plus two omitted preparation/review requirements" (variant-2:23); "staging restrictions and scope exclusions are carried" (variant-2:33) | MET | "the run condition and the go gate (2), the entry condition (1) ... the known limits (3) and the carried constraints (4, with the fifth counted under acceptance)" (variant-3:24) |
| Comp.2 Edge cases and failure scenarios | MET | Row 1: "edits whatever is checked out ... and every acceptance check still passes"; row 3: "A middle error such as a wrong grade token still passes them" (variant-1:20, :22) | MET | Row 1: "Following the plan on an existing branch can satisfy every acceptance check without satisfying this execution condition" (variant-2:18) | MET | Row 3: "A copy with a wrong token in the middle ... passes all three greps and both test needles"; "if it differs, both the anchor and the whole-file sha256 equality ... may fail on a fresh branch" (variant-3:19, :37) |
| Comp.3 Dependencies and prerequisites | MET | "entry condition" audited as a unit (variant-1:29); "I did not check whether PR #605 was merged" (variant-1:43) | MET | "Merge status, recorded owner approval ... were not independently verified" (variant-2:37); matrix "inventories only the branch and owner-go requirements" (variant-2:31) | MET | "Entry condition. The plan's added `FINAL: pass` claim (plan:19) holds: ...progress.md:7" (variant-3:36); dependent test checks (variant-3:33-34) |
| Comp.4 Success / completion criteria | MET | "Fixes for both blocking rows are added text in the plan: a branch line, and a summary section carrying the three limits. No task steps need to change." (variant-1:47) | MET | "**Verdict**: FAIL — two blocking omissions" (variant-2:12); "Next: resolve findings 1 and 2 before execution. The coverage-inventory note does not independently block." (variant-2:35) | NOT MET | Only "Findings 1 and 2 block, finding 3 is Medium, and finding 4 is a Note" (variant-3:41); no statement of what makes the plan pass or what fix closes a finding |
| Comp.5 Explicit out of scope | MET | "Not verified: ... I did not run pytest ... I made no git or GitHub calls" (variant-1:41-45) | MET | "No files were changed and no tests or shell commands were run"; "no snapshot-isolation claim is made" (variant-2:37, :34) | MET | "Not verified. Whether PR #605 is merged (no git or GitHub calls)"; "I ran no tests and made no git calls" (variant-3:37, :41) |

Subtotals: V1 4/5, V2 5/5, V3 4/5.

## Correctness

| Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence | V3 verdict | V3 evidence |
|---|---|---|---|---|---|---|
| Corr.1 No factual errors | NOT MET | "Spec units audited: 22" with a list that sums to 23, and "5 'not to be done' items" where source.md:58-63 has 4 bullets (variant-1:29) | NOT MET | "their limited automated coverage is **not** an additional plan deviation" (variant-2:33), conceded wrong (r2-v2.md:25); "Fully adherent ...: 40" of 45 (variant-2:23-24), conceded padded and recounted (r2-v2.md:19) | NOT MET | "the plan drops the spec's way of checking byte identity" (variant-3:19); source.md:24 is provenance, not a check; conceded overstatement (r2-v3.md:20) |
| Corr.2 Feasible technical approach | MET | Remedy "a branch line, and a summary section" is plan text only, "No task steps need to change" (variant-1:47) | MET | "resolve findings 1 and 2 before execution"; "The full passage is reachable through the explicit source-block reference" (variant-2:35, :33) | MET | "`make sync-dev` writes only under `.claude/` (Makefile:109-163), so the src/plugins check holds after Task 2" (variant-3:20) |
| Corr.3 Consistent terminology | MET | Category (Drift), grade (Blocking (Missing) / Medium) and label (HIGH/MEDIUM) used per agent:122 in every row (variant-1:20-23) | MET | Category, grade and label kept distinct; "Finding counts: Authorized expansion: 0 | ... Drift: 2" (variant-2:26) | MET | "Total deviations: 4 (3 Drift, 1 Authorized expansion)" matches the table and summary (variant-3:11, :26) |
| Corr.4 No internal contradictions | NOT MET | Row 4 is categorized "Drift" yet says "The wording comes from the spec" (variant-1:23); unit list sums to 23 against the stated 22 (variant-1:29) | MET | 45 = 40 adherent + 5 non-adherent; Notes keep the coverage note non-gating, consistent with verdict (variant-2:23-25, :35) | MET | "Drift: 3 rows covering 5 units" and 25 + 5 = 30 (variant-3:25-26); row 3's "faithful executor gets the right result" is about outcome, the finding about detection |
| Corr.5 Claims supported by evidence | MET | Every row has an Evidence cell, e.g. "a case-insensitive Grep of the plan for `branch\|origin/master\|summary` returns no match" (variant-1:20); verified vs not verified split (variant-1:35-45) | MET | Full-path citations for both rows, e.g. "source.md:65-69" (variant-2:19); INF ids for non-adherent units (variant-2:25) | MET | Test-file line cites for every scan constant, e.g. "`BANNED_SEVERITY_PHRASES` (test:112-125)" (variant-3:33) |

Subtotals: V1 3/5, V2 4/5, V3 4/5.

## Structure

| Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence | V3 verdict | V3 evidence |
|---|---|---|---|---|---|---|
| Str.1 Logical section ordering | NOT MET | A stray Note paragraph sits between the Deviations table and the Adherence summary (variant-1:25); conceded "in the wrong place" (r2-v1.md:24) | MET | Header, Deviations, Adherence summary, Notes, in template order (variant-2:5-37) | MET | Header, Deviations, Adherence summary, Notes, in template order (variant-3:5-41) |
| Str.2 Consistent hierarchy depth | MET | H1 then three H2 sections (variant-1:5, :16, :27, :33) | MET | H1 then three H2 sections (variant-2:5, :14, :21, :29) | MET | H1, three H2 sections, Notes with one nested bullet level (variant-3:5-41) |
| Str.3 Separation of concerns | MET | Notes split into "I verified these directly" and "Not verified" (variant-1:35, :41) | MET | Blocking rows in the table, the coverage note marked "Note, non-gating" in Notes (variant-2:18-19, :31) | MET | Notes split into "Checked with no finding", "Not verified", "Notes I agree with", structural risk (variant-3:30-39) |
| Str.4 Navigation aids | MET | Full spec and plan paths once (variant-1:13-14), then `plan:N` / `source.md:N` cross-refs | MET | Absolute paths in every cell; INF ids; "grouped into the two findings above" (variant-2:25) | MET | Finding cross-refs ("finding 3", variant-3:37); `plan:N`, `test:N`, `Makefile:N` cites |
| Str.5 Follows card / grade-prefix conventions | NOT MET | Row 4 graded `Medium:` for a spec-inherited form-only item (variant-1:23), which agent:120 makes a Note (conceded r2-v1.md:16); a graded `Note:` left outside the table (variant-1:25) | MET | Each row starts with the grade and names the affected action: "**Blocking (Missing):** affected action: selecting the branch" (variant-2:18) | MET | Every row starts with its grade, including "Note:" on the Authorized-expansion row; Blocking rows name "The affected action" (variant-3:17-20) |

Subtotals: V1 3/5, V2 5/5, V3 5/5.

## Clarity

| Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence | V3 verdict | V3 evidence |
|---|---|---|---|---|---|---|
| Cl.1 Unambiguous language | NOT MET | "Not found, so no row: the paragraph above is a note on form only." (variant-1:25) refers to a paragraph that does not exist above it; conceded garbled (r2-v1.md:24) | MET | "'Adherent' here means carried by the plan or the current preparation/review procedure, not proven implementation success." (variant-2:27) | MET | "Findings 1 and 2 block, finding 3 is Medium, and finding 4 is a Note." (variant-3:41) |
| Cl.2 Concrete, not abstract | MET | "for example `feature/blocker-classification-stage3b`" (variant-1:20) | MET | "a judgment affecting digits and apostrophes rather than lowercase letters" (variant-2:19) | MET | Names the extra files: "tests/skills/test_worker_contract.py (line 2923) and tests/unit/test_cli_install.py (line 63)" (variant-3:38) |
| Cl.3 Each section has a clear purpose | MET | Header, table, summary and Notes each carry one job; Notes split by verified status (variant-1:33-47) | MET | Notes end with "Next:" and a scope statement (variant-2:35, :37) | MET | Notes sub-headed by purpose (variant-3:30, :37, :38, :39) |
| Cl.4 Terms defined on first use | NOT MET | "I rely on the T1 card's simulation" (variant-1:44): "T1 card" never defined | NOT MET | "the matrix's 43 inferred units" and "INF-001, INF-034 ..." (variant-2:23, :25) before the matrix is identified at :31; INF ids never explained | NOT MET | "SWEEP_PHRASES and F1-F6" (variant-3:33) and "the first-pass card" (variant-3:38) used without definition |
| Cl.5 Actionable next steps / decision points | MET | "Fixes for both blocking rows are added text in the plan: a branch line, and a summary section" (variant-1:47) | MET | "**Next:** resolve findings 1 and 2 before execution." (variant-2:35) | MET | Gating decision stated: "Findings 1 and 2 block" (variant-3:41) |

Subtotals: V1 3/5, V2 4/5, V3 4/5.

## Risk coverage

| Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence | V3 verdict | V3 evidence |
|---|---|---|---|---|---|---|
| Risk.1 >=3 risks with probability and impact | NOT MET | Impacts named ("Affected action: ..."), but no probability given for any risk (variant-1:20-23) | NOT MET | Impacts named, no probability (variant-2:18-19) | NOT MET | One likelihood statement only ("Structural risk to the agent file is low", variant-3:39); the other risks carry no probability |
| Risk.2 Mitigation for each risk | NOT MET | Mitigations given for rows 1-2 only (variant-1:47); rows 3-4 have none | NOT MET | "resolve findings 1 and 2" (variant-2:35) names no mitigation for either | NOT MET | No mitigation stated for any finding |
| Risk.3 Failure modes and recovery | MET | Failure: wrong-branch edit (variant-1:20); recovery: "a branch line, and a summary section" (variant-1:47) | MET | Failure: "Following the plan on an existing branch" (variant-2:18); recovery: "resolve findings 1 and 2 before execution" (variant-2:35) | NOT MET | Failure modes named (variant-3:17, :19, :37) but no recovery path for any of them |
| Risk.4 External dependencies and their failure | MET | "Codegraph was stale, so I used Read and Grep only" (variant-1:45) | NOT MET | Merge status listed as not verified (variant-2:37) with no failure scenario | MET | "Whether `origin/master`'s line 122 equals this worktree's line 122; if it differs, both the anchor and the whole-file sha256 equality ... may fail on a fresh branch" (variant-3:37) |
| Risk.5 Monitoring / validation mechanism | MET | Grep validations used and stated: "A Grep count returned 1" (variant-1:36); "a case-insensitive Grep of the plan ... returns no match" (variant-1:20) | NOT MET | "no tests or shell commands were run" (variant-2:37); no validation mechanism used or proposed | MET | "I confirmed that line 122 of the variant file matches the current agent's line 122 with the fenced passage inserted" (variant-3:19); Glob/Grep checks (variant-3:31, :34) |

Subtotals: V1 3/5, V2 1/5, V3 2/5.

## Invariant and edge case

| Criterion | V1 verdict | V1 evidence | V2 verdict | V2 evidence | V3 verdict | V3 evidence |
|---|---|---|---|---|---|---|
| Inv.1 Collection boundaries (empty, single, max) | MET | Empty: Grep "returns no match" (variant-1:20); single: anchor "occurs exactly once" (variant-1:36) | NOT MET | No boundary condition examined | MET | Single: "The anchor sentence occurs once"; empty: "There is no plugin copy" (variant-3:31) |
| Inv.2 State interactions across component boundaries | MET | "Nothing checks that the two new needles were added to the test tuple: `uv run pytest` passes whether or not they are there" (variant-1:22) | MET | Checked-out branch state versus acceptance checks: "can satisfy every acceptance check without satisfying this execution condition" (variant-2:18) | MET | "`make sync-dev` writes only under `.claude/` ..., so the src/plugins check holds after Task 2" (variant-3:20) |
| Inv.3 Guard condition gaps | MET | Row 3: greps "fix only the opening, the last sentence and the join" (variant-1:22) | MET | Row 1: no constraint or task carries the branch condition (variant-2:18) | MET | Row 1: "nothing in the plan catches this" (variant-3:17) |
| Inv.4 Count divergence | NOT MET | Identifies none; its own unit list sums to 23 against the stated 22 (variant-1:29) | NOT MET | Identifies none in the plan; its own 45/40 count was conceded wrong (r2-v2.md:19) | MET | `git grep` "also names two test files beyond the four" (variant-3:38); "3 rows covering 5 units" reconciles 25 + 5 = 30 (variant-3:26) |
| Inv.5 Interaction effects when components combine | MET | Greps, needles and diff together still miss a middle error: "Only the `git diff` line would catch it, and only if a reviewer compares ... by eye" (variant-1:22) | NOT MET | "limited automated coverage is not an additional plan deviation" (variant-2:33) dismisses the combination without stating its effect | MET | "passes all three greps and both test needles" (variant-3:19); "the line also contains 'Blocking', which exempts it from F1-F6 under test:444" (variant-3:33) |

Subtotals: V1 4/5, V2 2/5, V3 5/5.

## Totals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 5 | 4 |
| Correctness | 3 | 4 | 4 |
| Structure | 3 | 5 | 5 |
| Clarity | 3 | 4 | 4 |
| Risk coverage | 3 | 1 | 2 |
| Invariant and edge case | 4 | 2 | 5 |
| **Met** | **20** | **21** | **24** |
| **qual_score** | **20/30 = 0.667** | **21/30 = 0.700** | **24/30 = 0.800** |
