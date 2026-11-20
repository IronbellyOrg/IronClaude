# Qualitative scoring, pass 2 (reverse order: V3, V2, V1)

Evaluator: neutral, pass 2. qual-pass-1.md was not read.
Method: 30-criterion additive binary rubric, Claim-Evidence-Verdict. MET (M) needs a quote or section reference from the variant's own text; otherwise NOT MET (N). No partial credit.

Inputs read: AD/variant-3-original.md, AD/variant-2-original.md, AD/variant-1-original.md; spec `.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/source.md`; plan `.../TASK-WF-stage3CRequest-20261119-143901.md`; card conventions `src/superclaude/agents/reflect-reviewer.md:71-123`; debate rounds AD/rounds/r2-*.md (used only for facts the advocates verified).

Facts from the debate used here (each checked against the variant's own text):
- V2's "their limited automated coverage is **not** an additional plan deviation" (variant-2:33) was conceded wrong (r2-v2.md:94, :101): the plan drops source.md:24's sha256.
- V1 row 4 is over-graded Medium on spec-inherited wording (conceded, r2-v1.md:16); V1's paragraph at variant-1:25 is garbled and outside the table (conceded, r2-v1.md:24).
- V3's "no artifact backs" the 83-test claim (variant-3:37) is right for the chosen passage; the only 83-passed record is the carry-scope variant's (r2-v1.md:30).
- I re-ran V1's grep: a case-insensitive grep of the plan for `branch|origin/master|summary` returns no match, so V1 row 1's evidence holds.

## Completeness

| Criterion | V3 verdict | V3 evidence | V2 verdict | V2 evidence | V1 verdict | V1 evidence |
|---|---|---|---|---|---|---|
| 1. Covers all explicit requirements | M | Adherence summary lists 30 units across run condition, go gate, entry, Task 1 parts, both acceptance sets, exclusions, limits and carried constraints (variant-3:24); Notes check exclusions and entry (variant-3:35-36) | M | 45 units from the 43-unit matrix plus two (variant-2:23); "change instructions, both exact test needles, test-discovery record, final verification record, staging restrictions and scope exclusions are carried" (variant-2:33) | N | 22 units listed (variant-1:29) omit the owner go gate and the "Constraints to carry" section (source.md:71-77) |
| 2. Edge cases and failure scenarios | M | Row 1 "Every acceptance line still passes there"; row 3 "a wrong grade token ... passes all three greps and both test needles" | M | Row 1 "Following the plan on an existing branch can satisfy every acceptance check without satisfying this execution condition" | M | Row 3 "A middle error such as a wrong grade token still passes them"; "`uv run pytest` passes whether or not they are there" |
| 3. Dependencies and prerequisites | M | "Entry condition. The plan's added `FINAL: pass` claim (plan:19) holds: ...progress.md:7"; "Whether PR #605 is merged" under Not verified | M | "Merge status, recorded owner approval and the historical 83-test result were not independently verified" (variant-2:37) | M | Units include "entry condition" (variant-1:29); "I did not check whether PR #605 was merged" (variant-1:43) |
| 4. Success / completion criteria | N | Closing line states which findings block (variant-3:41) but never states what must change for the plan to pass | M | "**Verdict**: FAIL — two blocking omissions" (variant-2:12); "Next: resolve findings 1 and 2 before execution" (variant-2:35) | M | "Fixes for both blocking rows are added text in the plan: a branch line, and a summary section carrying the three limits. No task steps need to change." (variant-1:47) |
| 5. Explicitly out of scope | M | "Diff scope: none. This is a UC-1 pre-execution audit"; "I ran no tests and made no git calls" | M | "'Adherent' here means carried by the plan or the current preparation/review procedure, not proven implementation success" (variant-2:27) | M | "Diff scope: none (plan against spec, nothing implemented)" (variant-1:9) |

Subtotals: V3 4/5, V2 5/5, V1 4/5.

## Correctness

| Criterion | V3 verdict | V3 evidence | V2 verdict | V2 evidence | V1 verdict | V1 evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors | M | Claims check out: anchor once at agent:122, test at test:214-228, sha prefix/suffix match source.md:24, "no artifact backs" 83 is true for the chosen passage | N | "their limited automated coverage is **not** an additional plan deviation" (variant-2:33) is wrong: the plan drops source.md:24's sha256 and variant path (conceded) | N | "Spec units audited: 22" but its own list (4+6+3+5+3+1+1) sums to 23 (variant-1:29); "5 'not to be done' items" against source.md's 4 bullets |
| 2. Feasible approach within constraints | M | Row 4: "`make sync-dev` writes only under `.claude/` (Makefile:109-163), so the src/plugins check holds after Task 2"; read-only method stated | M | Read-only method stated: "No files were changed and no tests or shell commands were run"; remedy "resolve findings 1 and 2 before execution" | M | "Fixes for both blocking rows are added text in the plan" (variant-1:47); fallback "Codegraph was stale, so I used Read and Grep only" |
| 3. Terminology consistent and accurate | M | Grades, labels and categories line up: Blocking rows HIGH, Medium row MEDIUM, Note row LOW, plan additions called Authorized expansion | N | Rows graded "Blocking (Missing)" carry Severity MEDIUM, which agent:71 defines as "unjustified drift with real impact"; label and grade pull in different directions | N | Row 4 is categorised "Drift" while the same cell says "The wording comes from the spec"; Drift means a divergence from the spec |
| 4. No internal contradictions | M | "Total deviations: 4 (3 Drift, 1 Authorized expansion)" matches the table; 25 adherent + 5 units in Drift = 30; expansion "consumes no unit" | M | 40 adherent + 5 non-adherent = 45; Total deviations 2 matches the table and the Drift count | N | Row 4 Drift vs "wording comes from the spec" in the same cell; stated 22 units vs a 23-item list |
| 5. Claims supported by evidence | M | Evidence column cites file:line for every row; Notes cite test:112-125, 408-423, 444, 487, 306-310 | M | Every row's Evidence cell cites spec and plan spans with line numbers | M | Evidence column for every row, plus "a case-insensitive Grep of the plan ... returns no match" (re-run: holds) |

Subtotals: V3 5/5, V2 3/5, V1 2/5.

## Structure

| Criterion | V3 verdict | V3 evidence | V2 verdict | V2 evidence | V1 verdict | V1 evidence |
|---|---|---|---|---|---|---|
| 1. Logical section ordering | M | Header, Deviations, Adherence summary, Notes, closing line | M | Header with Verdict, Deviations, Adherence summary, Notes ending in Next | N | Stray paragraph "Not found, so no row: the paragraph above is a note on form only" sits between the table and the Adherence summary (variant-1:25), referring to a paragraph that is below it |
| 2. Consistent hierarchy depth | M | `#` title, `##` sections, nested bullets in Notes used uniformly | M | `#` title, `##` sections, flat Notes bullets | M | `#` title, `##` sections, Notes split into two bullet lists |
| 3. Clear separation of concerns | M | Notes split into "Checked with no finding", "Not verified", "Notes I agree with", "Structural risk" | M | Notes separate the coverage-matrix note, INF-036, carried items, grounding root and Next | M | Notes split into "I verified these directly" and "Not verified" |
| 4. Navigation aids | M | Cross-references "finding 3" (variant-3:37), "first-pass card", short-form cites plan:/source.md:/agent:/test: | M | INF ids tied to findings: "INF-001, INF-034 ... grouped into the two findings above"; "Next: resolve findings 1 and 2" | M | Full Spec and Plan paths given once (variant-1:13-14) as the key for later short cites |
| 5. Follows card conventions and grade-prefix rule | M | Every row begins with a grade (`Blocking (Missing):`, `Medium:`, `Note:`), Blocking rows name the affected action, minor items in the table per agent:122 | N | A graded "Note, non-gating" finding is kept in Notes, not the table (variant-2:31); Blocking rows labelled MEDIUM (conceded form defect) | N | A finding graded "`Note:`" is placed outside the table (variant-1:25); row 4 graded Medium for spec wording, which agent:120 makes a Note |

Subtotals: V3 5/5, V2 4/5, V1 3/5.

## Clarity

| Criterion | V3 verdict | V3 evidence | V2 verdict | V2 evidence | V1 verdict | V1 evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language | M | Plain statements, e.g. "In this worktree that branch is `feature/blocker-classification-stage3b`, which holds the stage 3b commits" | M | Row texts are direct, e.g. "The spec requires a fresh branch made from `origin/master`" | N | "Not found, so no row: the paragraph above is a note on form only" (variant-1:25) is garbled (conceded) |
| 2. Concrete rather than abstract | M | Names the exact missing limits: "one sonnet model, three reviewers per arm, one scorer, no second reader" | M | "the qualification that the codepoint-order blocker is a judgment affecting digits and apostrophes rather than lowercase letters" | M | "one model (sonnet), three reviewers per arm, one scorer, no second reader, coverage hints in the briefs" |
| 3. Each section has a clear purpose | M | Bold sub-heads in Notes state each purpose | M | Verdict line, table, counts, Notes with a closing Next | M | Spec/Plan key, table, counts, verified / not-verified lists |
| 4. Acronyms and terms defined on first use | N | "UC-1", "F1-F6", "B/E re-runs" used undefined | N | "UC-1", "INF-001" and "the matrix" used undefined | N | "UC-1" and "the T1 card" used undefined |
| 5. Actionable next steps / decision points | M | "Findings 1 and 2 block, finding 3 is Medium, and finding 4 is a Note" names the gating decision | M | "Next: resolve findings 1 and 2 before execution. The coverage-inventory note does not independently block." | M | "Fixes for both blocking rows are added text in the plan: a branch line, and a summary section carrying the three limits" |

Subtotals: V3 4/5, V2 4/5, V1 3/5.

## Risk coverage

| Criterion | V3 verdict | V3 evidence | V2 verdict | V2 evidence | V1 verdict | V1 evidence |
|---|---|---|---|---|---|---|
| 1. At least 3 risks with probability and impact | N | Impact via Severity per row, likelihood only for row 3 ("a faithful executor gets the right result") and "Structural risk to the agent file is low"; not three risks with both | N | Two risks, impact only; no probability | N | Four rows with impact labels; no probability stated |
| 2. Mitigation for each risk | N | No fix named for rows 1 and 2 | N | Only the generic "resolve findings 1 and 2" | N | Fixes named for the two blocking rows only (variant-1:47); none for rows 3 and 4 |
| 3. Failure modes and recovery | N | Failure modes described (mid-passage mis-copy, wrong branch) but no recovery step given | M | Failure mode in row 1; recovery "resolve findings 1 and 2 before execution" (variant-2:35) | M | Failure modes in rows 1 and 3; recovery "a branch line, and a summary section carrying the three limits" |
| 4. External dependencies and their failure | M | "Whether `origin/master`'s line 122 equals this worktree's line 122; if it differs, both the anchor and the whole-file sha256 equality in finding 3 may fail on a fresh branch" | M | "The brief supplied a live grounding root rather than an isolated snapshot. Findings describe the files as read; no snapshot-isolation claim is made." | M | "Codegraph was stale, so I used Read and Grep only"; PR #605 merge unchecked |
| 5. Monitoring / validation mechanism | M | "Checked with no finding" list with grep validations (variant-3:30-36) | M | Validates the coverage matrix: "The INF-036 containment match is not semantic coverage" | M | "I verified these directly: ... A Grep count returned 1." |

Subtotals: V3 2/5, V2 3/5, V1 3/5.

## Invariant & edge case

| Criterion | V3 verdict | V3 evidence | V2 verdict | V2 evidence | V1 verdict | V1 evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries (empty, single, max) | M | "The anchor sentence occurs once"; plan:61 "requires that only `src/superclaude/agents/reflect-reviewer.md` is listed" | N | No collection boundary discussed | M | "occurs exactly once in the agent. A Grep count returned 1." |
| 2. State interactions across component boundaries | M | Row 4: `make sync-dev` writes only under `.claude/`, so the src/plugins status check holds after Task 2 | M | Row 1: branch state vs acceptance checks, "can satisfy every acceptance check without satisfying this execution condition" | M | Row 1: "`/sc:implement` edits whatever is checked out ... and every acceptance check still passes" |
| 3. Guard condition gaps | M | Row 3: greps pin only opening, last sentence and join | M | Row 1: no acceptance check guards the branch condition | M | Row 3: "Nothing checks that the two new needles were added to the test tuple" |
| 4. Count divergence | M | Reconciles "Drift: 3 rows covering 5 units"; flags plan:39's "83 tests" as unbacked; finds `git grep` names two test files beyond the four | M | Reconciles "45 — the matrix's 43 inferred units, plus two"; 40 + 5 = 45 | N | Own count diverges: 22 stated vs 23 listed (variant-1:29) |
| 5. Interaction effects when components combine | M | Passage vs whole-tree scans: "the line also contains 'Blocking', which exempts it from F1-F6 under test:444" | N | None identified | M | Row 4: `git grep` output combined with "run every test file" picks up YAML fixtures that cannot run |

Subtotals: V3 5/5, V2 3/5, V1 4/5.

## Totals

| Dimension | V3 | V2 | V1 |
|---|---|---|---|
| Completeness | 4 | 5 | 4 |
| Correctness | 5 | 3 | 2 |
| Structure | 5 | 4 | 3 |
| Clarity | 4 | 4 | 3 |
| Risk coverage | 2 | 3 | 3 |
| Invariant & edge case | 5 | 3 | 4 |
| **Met / 30** | **25** | **22** | **19** |
| **qual_score** | **0.833** | **0.733** | **0.633** |
