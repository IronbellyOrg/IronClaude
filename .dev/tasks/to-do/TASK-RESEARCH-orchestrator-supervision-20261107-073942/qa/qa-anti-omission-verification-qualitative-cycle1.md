# QA Report: Anti-omission verification (qualitative), after fix pass 2

**Topic:** Orchestrator mode Phase 1 (issue #339) research report
**Date:** 2026-11-08
**Phase:** fix-cycle (report-qualitative lens), anti-omission gate, cycle-2 review (the last one allowed)
**Fix cycle:** 2
**Fix authorization:** false (report only; the report was not edited)

**Inputs read:**
- Report: `RESEARCH-REPORT-orchestrator-mode.md` (1760 lines)
- Consolidated findings: `qa/qa-anti-omission-consolidated-findings-cycle1.md` (|F_1| = 1, NB-1)
- Fix log: `qa/qa-anti-omission-fix-log-cycle1.md` (NB-1 claimed RECOVERED)
- Context: `qa/qa-anti-omission-consolidated-findings.md` (cycle 0, AO-01 to AO-18), `qa/qa-anti-omission-verification-qualitative.md` (cycle 1 review)

_Status: complete. Verdict: FAIL (2 open blocking findings; last allowed review, so HALT and escalate)._

## 1. Status of the blocking omissions

| ID | Status | Where it sits now | Evidence |
|---|---|---|---|
| NB-1 (cycle-1 finding) | RECOVERED as specified | Step 1.2 (`:1243`) defines `OrcaObservation.unsupervised`, `terminal_state` and `next_action`, and `WorktreeState.package_ids`, `archive_states` and `shared_package_ids`. Step 1.3 (`:1244`) defines the pure pre-pass `mark_shared_packages` and says when it runs, and rules (i) to (iii) each name the field they read. Step 1.5 (`:1246`) adds two Retained problems lines and a Package state column. Section 3.1 lines 411, 412 and 421 point to these steps | Read `:1243-1246` and `:411-421` in this cycle. The type, field and print names match across 3.1, 1.2, 1.3, 1.5, 1.8 and 1.9, so the cycle-1 problem (rules that could not be computed and tests that could not pass) is fixed. The new problem in what rule (i) computes is NB-2 below |
| AO-01 (one package in two worktrees) | RECOVERED, but the computation is wrong (see NB-2) | 3.1 safe-to-close (`:421`), step 1.3 rule (i), step 1.5 | It is in the right section, but the rule `package_ids` uses does not match the source rule |
| AO-02 to AO-18 | RECOVERED (unchanged since the cycle-1 review) | Section 3.1 (context-only Dispatches, package states, ownership, Report rules, worktree removed mid-sweep, Orca unavailable, recommendations only) and steps 1.3 to 1.5, 1.8 to 1.12 | Fix pass 2 only extended table rows (fix log rows 24 to 31) and kept the report at 1760 lines. The cycle-1 review already confirmed where each one sits. Spot re-reads at `:411`, `:412`, `:421` and `:1244` (rules (ii), (iii), (iv) and probe rules (a) to (c) at `:1245`) found the text intact |
| Any JUSTIFIED disposition | None exist | n/a | Cycle 0 had all 18 as RECOVER and cycle 1 had NB-1 as RECOVER. No load-bearing finding is hidden behind a JUSTIFIED disposition |

## 2. New blocking findings

| ID | Severity | Location | Issue | Required fix | Status |
|---|---|---|---|---|---|
| NB-2 | IMPORTANT (wrong behaviour; AO-01 recovery as completed by the NB-1 fix) | Step 1.2 `WorktreeState.package_ids` (`:1243`); step 1.3 `mark_shared_packages` and rule (i) (`:1244`); step 1.5 Retained problems line (`:1246`); 3.1 "One package in two worktrees" (`:421`) | `package_ids` holds every package id the disk reader finds under `<root>/.dev/tasks/{to-do,done}/*/`, and the pre-pass flags any id that also appears under another root. `.dev/tasks/` is tracked in git (CLAUDE.md: "always staged"), so every worktree branched from master holds the same committed packages. `git ls-tree origin/master` shows 51 entries in `.dev/tasks/to-do/` and 38 in `.dev/tasks/done/`, and `git worktree list` shows 14 worktrees. In a live sweep, every worktree sharing master's history gets "removable: no (one package in two worktrees)". Retained problems then gets one line per shared id (dozens per pair of roots), and the fixed "<path 1> and <path 2>" form cannot express an id held by N roots. The source rule says something different: `WORKER-CONTRACT.md:108` says "It never **runs** one managed package in two worktrees at once." That is about an active run, not about the package folder being present. The synthetic fixture in step 1.8 (two `WorktreeState` records sharing one id) hides the problem, so the step 1.9 tests pass while live output is wrong. This also breaks the worktree-removable half on every real worktree: a removable worktree can never be found, even if the other two unobservable conditions are later resolved | Limit `package_ids` (or a new field it feeds) to packages being **run** in that worktree. Examples: a `to-do/` package whose ledger is unfinished and differs from the same package in the base branch (`git status` / `git diff` against upstream on the package path), or a package that an Orca Task or session row maps to that worktree. Exclude `done/` packages and tracked, unmodified packages. Change the Retained problems line to list every root ("<package id> in <path 1>, <path 2>, ..."). Add a step 1.8 fixture with two roots that both hold the same tracked, unmodified package, and a step 1.9 test that asserts it is **not** flagged. Keep 3.1 `:421` consistent with this ("run in", not "found under") | OPEN |
| NB-4c (new omission, source rule absent from research and report) | IMPORTANT (missing state in the plan's own "states the ledger reader must recognise" list; wrong output) | 3.1 "Package states the ledger reader must recognise" (`:412`); step 1.3 rule (iii) (`:1244`); step 1.4 disk reader (`:1245`) | The source the report cites for package states, `sc-crash-recovery/refs/pipelines.md`, has a third state between the two lines it cites (`:190`, `:199`): `:198`, "Present in both `to-do/` and `done/` → conflict. Report it; do not merge, move or delete either copy." The same state is the STOP code `E-MANAGED-CONFLICT` in `sc-implement-protocol/SKILL.md:39` ("managed package exists in both `to-do/` and `done/`"). Neither the research files nor the report mention it (grep for `in both`, `E-MANAGED-CONFLICT` and `pipelines.md:198` over the report, `research/` and `synthesis/` found no package-state hit). The step 1.4 disk reader reads `{to-do,done}/*/progress.md` and makes "one row" per package found. A package in both folders therefore gives two rows from two different ledgers, and the `done/` copy can classify as finished while the conflict is never shown. The 3.1 heading claims to list the states the reader must recognise, so this is a load-bearing gap, not a nicety. Research missed it too, so it is a source-to-report omission, not a research-to-report omission; it is recorded because the adversarial stance asks for omissions still missing | Add "conflict" as a fourth package state in 3.1 `:412` and step 1.3 rule (iii), citing `pipelines.md:198` and `sc-implement-protocol/SKILL.md:39` [CODE-VERIFIED]. A package id found in both `to-do/` and `done/` of the same root prints "<package id>: conflict (in to-do/ and done/)" in the Package state column and under Retained problems, is never classed finished, and makes the worktree "removable: no". Add an `archive_states` value (or equivalent) in step 1.2, a fixture in step 1.8 and a test in step 1.9 | OPEN |

The ID NB-4c is used so it does not clash with the existing NB-4 record in the report (`grep -c NB-4` must stay 23 there; this QA file is separate).

### Candidate graded MINOR after checking (not blocking)

- **NB-3 (live rule (ii) is inert).** `OrcaObservation.unsupervised` is None on every live row in Phase 1 (`:1243`: "None while the JSON field that marks it is not captured, so only synthetic fixtures set it in Phase 1"). So on live rows rule (ii) never fires, and a context-only Dispatch goes through rules 2, 5 and 7 like any other row. That conflicts with the target sentence at `:411` ("Such a row is never classed working or stalled (proved) from Orca liveness"). I first planned to require a fallback that treats `terminal_state == "retained"` as could not determine. That fallback is **invalid**: Section 2.2 (`:104`) records that "a working worker shows `retained`", so it would turn every working row into could not determine. No clean live discriminator exists. The limit is disclosed at `:1243` and `:411` ("No such row was captured"), so this is graded MINOR. Note: neither 8.2 nor S9 has an Open Questions row for capturing the unsupervised field (grep for `unsupervised` shows only `:411` and `:1243-1255`). Add one (capture one context-only Dispatch row and name the field) at the plan stage. This matches the cycle-1 grading of M-5.

## 3. MINOR notes (not blocking, not rechecked later)

- The archive-blocked label also applies to complete Linux packages that are waiting for their final review. This agrees with `pipelines.md:190`, but the report never says what "removable" means for a worktree whose only package is archive-blocked.
- The step 1.6 JSON keys (`schema_version ... report_path`) carry no worktree or package-state data; only the Markdown report has it. The skill reads the Markdown at `report_path` (step 1.15), so nothing is lost. A JSON consumer will not see package states.
- `OrcaObservation.next_action` was not requested by NB-1. It is labelled "plan decision, new design" and justified (fix log row 24: the terminal-releasable rule already read `nextAction`). It fills a gap and is not scope creep.
- M-1 to M-6 from the cycle-1 review are still notes. Their wording is unchanged, and fix pass 2 was told not to fix them.

## 4. Global checks

| # | Check | Result | Evidence |
|---|---|---|---|
| G-1 | Each recovered finding sits in the right section | PASS | Target behaviour is in 3.1 (`:411`, `:412`, `:421`), the data model in step 1.2, rules in 1.3, probes in 1.4, rendering in 1.5, and fixtures and tests in 1.8 and 1.9 (Read `:411-421`, `:1243-1246`) |
| G-2 | No JUSTIFIED disposition hides a load-bearing finding | PASS | No item has the JUSTIFIED disposition (consolidated findings cycle 0 and cycle 1, Read) |
| G-3 | No recovery broke WC-10 | PASS (with the MINOR NB-3 note) | Every new field defaults to None, and None or missing data map to could not determine (`:1243`: "None = could not determine"; rule (ii) gives could not determine; probe rule (a) gives `unscanned: worktree removed during sweep`). No recovery treats a missing signal as death. NB-2 errs toward "removable: no", which is wrong but safe for WC-10 |
| G-4 | No recovery recommended A4 | PASS | `grep -n '\bA4\b'` gives 25 lines (`:9`, `:26`, `:165`, `:167`, `:323`, `:509`, `:548`, `:562`, `:576`, `:607`, `:608`, `:622`, `:677`, `:872`, `:1053`, `:1077`, `:1090`, `:1183`, `:1191`, `:1381`, `:1396`, `:1485`, `:1553`, `:1589`, `:1645`, ...). None is inside a recovered passage (`:411-421`, `:443-469`, `:1243-1258`). The contexts checked (`:509`, `:548`, `:1090`, `:1191`, `:1396`) say "rejected", "[CODE-CONTRADICTED]" or are an effort grade only |
| G-5 | No recovery designed a later phase | PASS | "Later phases (recorded only, not designed)" at `:1320` is unchanged. Fix pass 2 touched only step 1.2, 1.3, 1.5, 1.8 and 1.9 rows and 3.1 bullets (fix log rows 24 to 31) |
| G-6 | No recovery introduced a contradiction between sections | FAIL | The NB-1 contradiction (rules that could not be computed against the data model) is resolved. NB-2 is a new contradiction between the source rule as quoted at `:421` ("never **runs** one managed package in two worktrees") and the computation at `:1243-1244` ("found under ... `{to-do,done}/*/`"): what is computed is not what is quoted. NB-4c is a gap in a list the heading at `:412` claims is complete |
| G-7 | Protected markers intact | PASS | `grep -c CONTRADICTION` = 6, `grep -c NB-4` = 23, `wc -l` = 1760 (Bash, this cycle) |

## 5. Items that PASS

- NB-1: RECOVERED (fields, pre-pass, print locations, fixture, tests and 3.1 wording are all consistent).
- AO-02 to AO-18: RECOVERED and in the right sections.
- AO-01: in the right section (status RECOVERED), but its computation is wrong (NB-2, OPEN).
- G-1, G-2, G-3, G-4, G-5 and G-7.

## 6. Confidence Gate

Checklist for this review: the NB-1 re-check, the AO-01 to AO-18 status (counted as one), G-1 to G-7, and the adversarial omission hunt (NB-2, NB-3, NB-4c). That is 11 items in total.

- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement (this cycle, including the evidence gathered before the context reset):** Read: 9 | Grep: 6 | Glob: 0 | Bash: 5. Read and Grep (15) is more than the item count (11).
- **Web research:** none performed (all checks were local), so Tavily was not needed.
- Unchecked: none. Unverifiable: none. The live effect of NB-2 is inferred from the tracked `.dev/tasks/` tree and the worktree count. It was not observed from a sweep run, because no sweep exists yet.

## Self-Audit

**(a) Reliance list (rf-qa PASS items not re-checked structurally):**
- Relied on the structural verifier (`qa/qa-anti-omission-verification.md`, PASS, |F_1| = 0) for section numbering, citation format and table structure of the fix-pass-2 edits.
- Relied on the cycle-1 qualitative review for where AO-02 to AO-18 sit, re-checked only by spot reads at `:411`, `:412`, `:421`, `:1244` and `:1245`.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- NB-2 live effect: `git ls-tree --name-only origin/master .dev/tasks/to-do/` gave 51 entries and `.dev/tasks/done/` gave 38 (Bash). `git worktree list` gave 14 lines. This shows that the `{to-do,done}/*/` scope in `:1243` matches the same ids in every master-based worktree.
- Source wording: Grep found `src/superclaude/core/WORKER-CONTRACT.md:108` ("It never runs one managed package in two worktrees at once.") and `sc-crash-recovery/refs/pipelines.md:198` ("Present in both `to-do/` and `done/` → conflict"), plus `sc-implement-protocol/SKILL.md:39` (`E-MANAGED-CONFLICT`).
- NB-4c absence: Grep for `E-MANAGED-CONFLICT|pipelines.md:198|in both` over the report, `research/` and `synthesis/` found no package-state hit.
- NB-3 regrade: Read `:104` ("a working worker shows `retained`") disproved my own proposed fallback, so I downgraded NB-3 to MINOR.
- G-4: Bash showed the context around `\bA4\b` at `:509`, `:548`, `:1090`, `:1191` and `:1396`, and all of them are rejections.

If this review had found 0 issues, the two OPEN findings above would be the counter-evidence: both rest on source lines and git output, not on the earlier reviews.

## Recommendations

- This was the cycle-2 review, the last one allowed. **HALT. Do not run a third fix pass or a fourth review.** Escalate NB-2 and NB-4c to the user with the required fixes in Section 2.
- The MINOR notes (NB-3, the Section 3 notes, M-1 to M-6) can be carried to the plan stage as notes.

## Verdict: FAIL

Open blocking findings: NB-2 (IMPORTANT) and NB-4c (IMPORTANT). Fix cycles are used up (2 of 2), so these findings go to the user. Under the review severity rule they must not be converted to Open Questions or passed.

## QA Complete
