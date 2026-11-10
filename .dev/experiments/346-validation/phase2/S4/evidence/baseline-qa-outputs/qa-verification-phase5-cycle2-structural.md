# QA Report - Gate 2 Fix Cycle 2 Verification (Structural)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Phase:** fix-cycle (cycle 2, last), fix_authorization: false

---

## Inputs read

- Embedded prompt, task file line 348 (Read offset=348 limit=1).
- `qa/qa-consolidated-findings-phase5-cycle2.md` (27 lines, BLOCKING_COUNT: 3, rows 1 to 3 all Blocking = yes).
- `qa/qa-fix-log-phase5-cycle2.md` (63 lines; claims 3 fixes, 0 unfixed).

## Check (a) Finding 1: synth-02 CLI reading mapped to "evaluates the predicate, then installs"

- synth-02 line 31 (Read): CLI-reading row now says "no new mechanism: the existing `bmad install` already creates the directories ... wrapper must pass `install`, `--version` and `--help` through unchanged ... Stage 0 only (Section 7); option C ... only if the owner asks for such a command"; Options cell "A (documentation half, with the rest of Stage 0); C only for a new command name"; Source "R02 s6.2; R03 A3 C.5".
- synth-02 line 107 (F-01 Notes): "C only for a new, separately named command; under the CLI reading Stage 0 alone, with no trigger built".
- synth-02 line 198 (Owner Q2): "Stage 0 only, because `bmad install` already creates the directories; C only for a new, separately named command".
- synth-02 line 443 (Option C bullet, section 5): "matters only for a new, separately named command ... Stage 0 only, Section 7".
- Grep of `synthesis/` for "evaluates the predicate|then installs|predicate, then|runs the install" (case-insensitive): only hits are synth-02:442 (Option B, a stub running the install through a permission prompt, correct for B), synth-03:123 (Option C Description), synth-03:146 and synth-04:122 (long lines, inspected below).
- Residual R-1 (graded in the Issues section): synth-03:123 (Option C Description) still says the wrapper "`/usr/local/bin/bmad` ... or a new command name next to it evaluates FIRST_USE(P) ... and runs the common install command before doing what the user asked", while Option C step 2 (synth-03:130) says the wrapper must pass `install`, `--version`, `--help` through unchanged and C can add something only for a new, separately named command.
- Traced the changed claim to research: `research/03-startup-flow-home-and-user-level-claude.md` line 327 (inside heading `### A3.` at line 305, item C step 5): "the wrapper must pass `bmad install` and `bmad --version`/`--help` through unchanged ... Subcommands that exist in 6.9.0: `install`, `status`, `uninstall`". The new synth text restates exactly this; no new fact added.
- Result Finding 1: FIXED (all four stale places corrected: synth-02 lines 31, 107, 198, 443).

## Check (a) Finding 3: synth-03 "Option A alone fails the decision" versus "Stage 0 only satisfies the CLI reading"

Read every cited location after the edit:
- synth-03 line 86 (Option A Cons): "Option A (its documentation half) satisfies that reading only together with the rest of Stage 0 (Section 7). Under the slash-skill and session-open readings it fails the 2026-11-07 decision".
- synth-03 line 262 (Table 1, Which-reading row, A cell): same statement.
- synth-03 lines 310-313 (Section 7 reading table row (1)): "Stage 0 only: existing `bmad install` already counts; C only for a new, separately named command".
- synth-03 line 331 (Rationale 1; was 330, one line of drift from earlier edits): same statement; "A stays as the documentation half of Stage 0".
- synth-03 line 365 (Dependence table row 1): "Stage 0 only ... Option A alone, without the rest of Stage 0, does not, and A fails the decision for the slash-skill and session-open readings (Rationale 1)".
- synth-04 line 344 (Open Questions row 2, reading (a)): same sentence; line 343 (row 1 impact) and line 345 (row 3 impact) carry the Stage 0 only / C for a new name wording.
- Grep of `synthesis/` for "fails the decision|A alone|A fails|so A": hits only at synth-03:86, :262, :331, :365 and synth-04:344, all uniform. The old text ("so A alone fails") is gone.
- Q1 and Q2 stay unanswered in every place (synth-04 lines 343-344, synth-03 line 361).
- Result Finding 3: FIXED.

## Check (a) Finding 2: synth-04 closes F-01 only through Phase 4

Read every cited location after the edit:
- synth-04 line 25 (gap map F-01): CLI reading = Stage 0 only, no shipped block, no Phase 4 branch; Phase 4 "only when one is built".
- synth-04 line 114 (Phase 3 Dependencies): "Conditional on a built branch ... steps 3.1 to 3.6 then stay a documented specification (Stage 0 (c))".
- synth-04 line 178 (Phase 5 intro): steps 5.1 and 5.6 under every reading; steps 5.2 to 5.5 need a built branch. Step titles at lines 185, 186, 187 carry the condition; line 188 (5.5) says "For 4B and 4D only".
- synth-04 line 246 (6.1) and line 252 (6.7): conditional on a built branch.
- synth-04 integration checklist lines 319, 320, 327, 328, 329, 330, 331, 333, 334: all conditional or carry the Stage 0 only remark.
- Branch table line 134 says "No branch (Stage 0 only); 4C only if the owner asks for a new, separately named command".
- Result Finding 2: FIXED.

## Check (b) New blocking issues introduced by the fixes

- Fabrication: every added sentence traces to synth-03 Option C step 2 (line 130), synth-03 Section 7 Stage 0 and Stage 1 (lines 321-322) or research 03 line 327. No new file path, line number, test name or number was added by the fixes (compared the fix log's list of edits with the text read). No new hallucinated path.
- Doc-only claims in Sections 2, 6, 7, 8: none added; the added text cites code-derived facts only (the doc-only W01 items keep their `doc-only` tags where they already appeared, for example synth-04 lines 135, 149, 169).
- Broken tables: rows edited in synth-02 line 31 (5 cells), synth-03 lines 86, 262, 365, synth-04 lines 25, 186-188, 246, 252, 343-345 keep their column counts; headings and separators are intact (heading Grep lists every expected `##`/`###`).
- Placeholders: Grep of `synthesis/` for TODO|TBD|FIXME|PLACEHOLDER|[fill|lorem|XXX: only the self-audit sentence at synth-01:506 and the legitimate phrase "placeholder trees" (test fixtures) at synth-02:69 and :110.
- Lost sections: none; see check (c).
- Result: no new blocking issue. Three MINOR residuals found (listed under Issues Found).

## Check (c) Section-to-file mapping

Heading Grep of all four synth files: synth-01 has `## 1. Problem Statement` (line 10) and `## 2. Current State Analysis` (line 26, subsections 2.1 to 2.6); synth-02 has `## 3. Target State` (12), `## 4. Gap Analysis` (99), `## 5. External Research Findings` (232); synth-03 has `## 6. Options Analysis` (11) and `## 7. Recommendation` (301); synth-04 has `## 8. Implementation Plan` (13), `## 9. Open Questions` (337), `## 10. Evidence Trail` (398). Mapping intact; synth-01 (the file the fix log says was edited then restored) still has its line 479 reading "the choice among B, C, D cannot yet be determined" and Sections 1 and 2 headings in place.

## Issues Found

No CRITICAL and no IMPORTANT (blocking) issue. Three MINOR notes, not rechecked by the rule of this cycle:

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | MINOR | `synthesis/synth-03-options-recommendation.md:123` (Option C Description) | Residual phrasing of the same family as cycle-2 Finding 1: it says the wrapper `/usr/local/bin/bmad` "or a new command name next to it evaluates FIRST_USE(P) ... and runs the common install command before doing what the user asked". Step 2 at line 130 (7 lines later) says the wrapper must pass `install`, `--version`, `--help` through unchanged and that only a new, separately named command can carry the logic. The tension is resolved in the same option, so it is not a false mapping of the CLI reading. | Reword the Description to "a new, separately named command next to the pass-through wrapper evaluates FIRST_USE(P) ..." |
| 2 | MINOR | `synthesis/synth-04-plan-questions-evidence.md:19` | Says "Phases 1 to 3 and 5 to 7 do not depend on the answers". After this cycle's fixes, Phase 3's shipped block (line 114), steps 5.2 to 5.5 (line 178), step 6.1 test row and 6.7 (lines 246, 252) depend on whether a Phase 4 branch is built, which depends on the answers. Phase 3 line 114 already names Section 9 rows 5 and 6 as owner inputs. | Say "Phases 1 and 2, step 5.1, step 5.6 and the specification of Phase 3 do not depend on the answers; the shipped block and steps 5.2 to 5.5 do". |
| 3 | MINOR | `synthesis/synth-04-plan-questions-evidence.md:200` (Table 5.1 row `test-57:327-329, 331-336`) | Row says "The new writer must be byte-idempotent (step 5.3 case f)" and "Applies to: all"; step 5.3 now exists only if a branch is built. | Change "Applies to" to "all; case f only if a branch is built". |

These add to the MINOR notes already in the consolidated findings (M-1, M-2, N1, N3, N4); none changes a conclusion or contradicts a blocking fix.

## Self-Audit

What I actively checked (tool evidence):
- Read: the embedded prompt (task file line 348); the cycle-2 consolidated findings (27 lines) and fix log (63 lines) in full; synth-02 lines 1-261 and 421-466 (all of Sections 3 and 4 and 5.3 including every edited place: 31, 107, 198, 443); synth-03 lines 1-400 in full (all edited places: 86, 262, 310-313, 331, 365); synth-04 lines 1-474 in full (all edited places: 25, 114, 178, 185-188, 246, 252, 319-334, 343-345); `research/03-...md` lines 322-331 for the changed claim (line 327) and Grep for its `### A3.` heading (line 305); synth-01 lines 470-481 (the file the fix log says it edited and restored).
- Grep over `synthesis/`: stale mechanism phrases ("evaluates the predicate|then installs|predicate, then|runs the install"); "fails the decision|A alone|A fails|so A"; "chosen subcommands|Stage 0 only|new, separately named" counts (4, 11, 6 per file, consistent with the fix log's 11 for synth-04); headings of all four synth files (section mapping); placeholder tokens; "wrapper|CLI reading" in synth-01.
- Reproduced: the three blocking findings are fixed at every cited line and at the extra places the fix log lists; the changed claims trace to research 03 line 327 and to synth-03 steps already in the file.
- Why I believe the count is right: I looked specifically for (1) leftover stale phrases (found one weak residual, issue 1, graded MINOR because step 2 of the same option states the constraint), (2) places where a Phase 3 to Phase 6 step is still unconditional after the F-01 fix (found the summary sentence at synth-04:19 and one table cell at :200, both MINOR; every step, checklist and gap-map line the finding named is conditional), (3) wording of A versus the CLI reading (uniform in all five places), (4) fabricated or moved paths, tables and sections (none). Not observed: I did not re-run any test, installer or CI, and did not re-open product code (the fixes add no product-code citations); those are UNVERIFIED and out of scope here. I did not recheck the older MINOR rows (rule of this cycle). I did not open synth-01 beyond lines 470-481 and its heading list, because no fix targeted it and the fix log says it is byte-restored; whether it is byte-identical to the pre-edit text is UNVERIFIED (no copy to diff against), but its content at the touched line is coherent.
- Tool engagement: Read: 15 | Grep: 11 | Glob: 1 | Bash: 0. Every call targets one of the checks above.

Confidence: Verified: 6/6 checks (3 blocking findings, new-issue scan, section mapping, fix-log honesty) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for the scope of this cycle (blocking findings only; MINOR items not rechecked).

## Verdict

**PASS** (all 3 blocking findings fixed; no new blocking issue).

Counts: blocking findings checked 3, fixed 3, unfixed 0; new blocking issues 0; CRITICAL 0, IMPORTANT 0, MINOR 3 (new notes).

Gate 2 fix cycle 2, verification agent 1 of 2 (structural): PASS.

## QA Complete

