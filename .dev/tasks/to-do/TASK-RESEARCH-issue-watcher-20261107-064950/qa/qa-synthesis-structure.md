# QA Report - Synthesis Gate (structure lens)

**Topic:** GitHub issue watcher research (issue 331)
**Date:** 2026-11-07
**Phase:** synthesis-gate
**Fix cycle:** N/A (first review)
**Fix authorization:** false (report only)
**Status:** Complete
**Verdict:** FAIL (1 blocking finding, B-1; 4 minor notes)

---

## Progress log

(Findings are appended below as each checklist item is verified.)

### Inventory
- Glob of `synthesis/synth-*.md` returned exactly 4 files: synth-01-problem-current-state.md (508 lines), synth-02-target-gaps-external.md (468), synth-03-options-recommendation.md (539), synth-04-plan-questions-evidence.md (551). All four were read completely (paged Reads), together with research/research-notes.md (both addenda).

### Item 1 - Section headers: PASS
`## 1. Problem Statement`, `## 2. Current State Analysis` (synth-01); `## 3. Target State`, `## 4. Gap Analysis`, `## 5. External Research Findings` (synth-02); `## 6. Options Analysis`, `## 7. Recommendation` (synth-03); `## 8. Implementation Plan`, `## 9. Open Questions`, `## 10. Evidence Trail` (synth-04). All ten present once, in order, with the expected names.

### Item 2 - Table column structures: PASS
Gap Analysis (synth-02 4.1) is Gap / Current State / Target State / Severity / Notes. Options Comparison (synth-03) is Criterion / A / B / C / D (superset). Implementation steps (synth-04 Phases 1-7) are Step / Action / Files / Details. Open Questions (synth-04 9.2) are # / Question / Impact / Suggested Resolution.

### Item 3 - No fabrication: PASS (spot-verified against source, not against other reports)
Claims traced to code or research and found true:
- `src/superclaude/commands/issue.md`: :15 (stops, never runs next steps), :24 (explicit only), :29/:37 (usage, option), :43 (no repo/dry-run option), :45-51 (STOP rules), :68 (outputs), :71, :79, :83, :89-93 all match.
- `refs/claim.md` (read in full, 91 lines): :14-16 prerequisites, :20 "No GitHub or ClickUp write happens before Wave 3", :26, :29, :37-43, :47, :48-50, :54-60, :78-80, :84-90 all match the wave table in synth-01 2.1.
- `origin_repo.py`: :74 `_NUMBER`, :66-69 origin patterns, :45-50 exit table, :86-99 `parse_origin_url`, :102-153 `check_claim`, :135 case-insensitive compare, :156-174 `read_origin` (no cwd), :177 `main`, :14 only `gh` mention. All match.
- `WORKER-CONTRACT.md`: :11 worker run definition, :23 never-as-worker list, :39 WC-8, :40 WC-9, :61 WC-13, :93 "never starts with /sc:" all match.
- `ci.py:1-15`: imports only `re`, `.classifier`, `.models`; pure classifier. Matches the CODE-CONTRADICTED statement.
- `docs/designs/sc-issue-launch-level-hook.md`: :6, :17, :23 ("One script ... enforces"), :32, :34 ("current claim code does not implement"), :40 ("proposed") match; Glob `**/launch-level-guard*` returns nothing; `hooks.json:101` registers only `launch-job-identity.sh`; `launch-job-identity.sh` is 566 lines.
- `main.py:519-565`: eleven deferred registrations in the order and line ranges stated; `reflect` at 559-561, `__main__` at 564-565.
- `tests/cli/test_cli_registration.py:28-49`: 15 names, comment "frozen snapshot", `swarm` and `reflect` absent. Matches C5/G29.
- Workflows: Glob shows exactly README.md, boundary-guard.yml, contract3-generator-constraint-lint.yml, test.yml; Grep finds no `schedule:`/`cron:`/`issues:`/`workflow_run`/`pull_request_target`; `workflow_dispatch` only at test.yml:8; `test-summary` needs at :194; pytest command at :47, `make sync-dev` at :38, `uv pip install` at :29.
- Other cited anchors confirmed: `fallback.py:39`, `notify.py:21`, `tool_orchestrator.py:105`, `batch_retry.py:87`, `init_lite.py:221` (`_atomic_write`) and 359 lines, `cleanup_audit/commands.py:86` dry-run, `recommend/__init__.py:1,12`, `tasklist/__init__.py:1,9`, `recommend/commands.py:34`, 12 files in `cli/recommend/`, `test_conflict_e2e.py:118,132,178`, `test_issue_repo_resolution.py:281`, `conftest.py:29-33` fixture loader, `poll-augment-review.sh:53-55` (`--method GET -F per_page=100`), `ccsession:137` and README:534-535, `orca-capabilities.md:66`, Orca `bundled-skill-guides.js:2413,3158`, `agent-launch-recovery.js`/`agent-launch-request.js`/`handlers/agent-launch.js` present under /opt/Orca, `.dev/issues/331/analysis/analyze-sc-issue-protocol.md:34-36` (F3, F4, F5), `labels.md:7,27-42`.
- Research cross-references (R01 sections 1-13, R02 1-7 plus 2b/2c/3.1-3.4, R03 1-7, W01 1-14.5, W02 A1-K) all exist as headings; gaps-and-questions.md has 24 rows.
- Arithmetic re-done: 12/5000 = 0.24 percent; 288 runs x 30 days x 1 min x $0.006 = about $52; 5 workspaces x 3 calls x 12 = 180 = 3.6 percent; Requirement Scoring tally recounted for A, B, C, D and matches (2/8, 5/5, 6/4, 3/7).
No fabricated fact found. See finding M-2 for one wording inconsistency.

### Item 4 - Evidence citations use real file paths: PASS
Every repo path cited above exists (Glob/Read). Citations carry file:line. No vague "the system handles X" claims found in the four files.

### Item 5 - Options analysis: PASS
synth-03 documents four options (A, B, C, D) each with description, step table, ASCII diagram, effort/risk/reuse/files/pros/cons, answers to Q-a/Q-b/Q-c, a 10-row Requirement Scoring table, an Options Comparison table and nine revisit conditions.

### Item 6 - Implementation plan specificity: PASS
synth-04 Phases 1-7 name concrete paths (`src/superclaude/cli/issue_watch/{__init__,commands,runner,models,github,selection,launch,state,cycle}.py`, `tests/issue_watch/*`, `docs/designs/issue-watcher.md`, the `main.py` block after l.561), function signatures, argv lists, exit codes, defaults and test scenarios. No generic "create a service" steps.

### Item 7 - Cross-section consistency: PASS (with notes M-1, M-2)
- Gaps G1-G30 (synth-02) each map to a plan phase, a Section 9 question or a Section 9.3 correction: G1/G2/G3/G12/G24 to Phases 2-6; G5/G6/G7/G9 to Phases 4-5 and Q4/Q10/Q13; G8 to Q14; G10 to Q7; G11 to Phase 7 and Q9; G13 to Q12; G14 to Q6; G15 to Q21; G16/G17 to follow-up table and C1; G18 to D5; G19 to Q15; G20 to Q1; G21 to Q5; G23 to Phase 5 step 13 (audit record); G25 to Q17; G26-G30 to C2/C3/C5/C6/C7.
- Options in Section 6 cite Section 2 evidence; Recommendation (7.1) is option A and agrees with the Requirement Scoring tally, which 7.2 reports honestly (B and C score higher by count; reasons given).
- Section 9 questions are not answered elsewhere as fact; the plan marks each dependent detail `open: ... (Qn)` and every Qn used in Section 8 exists in 9.2 (checked Q1-Q4, Q6-Q15, Q17, Q21, Q23).

### Item 8 - No doc-only claims in Sections 2, 6, 7, 8: PASS (note M-4)
Section 2 doc-sourced items are tagged `[UNVERIFIED - doc-only]` and kept out of the 2.5 diagram. Vendor-documentation facts used in 6.1 and 8 (coder_script cron) are tagged EXTERNAL-VERIFIED and the missing template facts are carried as open questions.

### Item 9 - Stale docs surfaced: PASS
Stale/contradicted items (private-fork claim, launch-level present-tense wording, hooks README, test comments, ci.py wrapper claim, `launch-job-identity.sh` not installed) appear in synth-02 G26-G30 and G2, in synth-04 9.3 C1-C11, and in synth-01 2.3/2.4.

### Item 10 - Content rules: PASS
Multi-item data is in tables; ASCII flow diagrams exist in synth-01 2.5, synth-02 3.1, synth-03 6.1-6.4, synth-04 8.2; no full source reproductions (only short argv lists and two one-line jq filters).

### Item 11 - No placeholders: PASS
Grep (case-insensitive) of `synthesis/` for the uppercase tokens T-O-D-O, T-B-D, F-I-X-M-E, X-X-X and for the phrase "pending owner decision" returned no match.

### Item 12 - No hallucinated paths: PASS (note M-3)
Glob for `**/*issue_watch*` (repo) and `**/*issue-watch*` (src) returned nothing, so no NEW name collides with an existing file. Parents exist: `docs/designs/` (3 files), `src/superclaude/cli/`, `tests/`. NEW paths are labelled NEW in 8.3 and in most steps (see M-3 for the exceptions).

### Item 13 - Addendum conformance: FAIL (one blocking finding, B-1)
Checked against ADDENDUM and ADDENDUM 2 of research-notes.md:
| Requirement | Result | Evidence |
|---|---|---|
| Recommendation is option A "decided by the owner"; "pending owner decision" absent | PASS | synth-03 7.1; grep returned no match for the phrase |
| B and C scored in Requirement Scoring, documented with revisit conditions | PASS | synth-03 Requirement Scoring table, 6.2, 6.3, nine revisit conditions; synth-04 closing table |
| Coder#477 as sibling dependency with repo boundary and "A makes it unnecessary unless B or C revisited" | PASS | synth-01 1.2; synth-02 3.4, G18; synth-03 7.7; synth-04 D5 |
| Integer-only prompt rule stated | PASS | synth-01 1.1 Q3 and 2.2; synth-02 SC-4, G12; synth-03 7.3; synth-04 Phase 1 and step 3.2 |
| Options B and C not excluded by assertion; "no inbound endpoint" not a requirement or pre-filter | PASS | Grep of "no inbound/no listener" shows it only as a description of option A, as a consequence of the owner decision (synth-02 3.4 says so explicitly), and as one scored criterion (synth-03 "Inbound exposure (one scored criterion, not a pre-filter)"); not in SC-1..17 or the 3.3 constraints |
| Sender-authentication, Coder app exposure, contract topics in Section 5 | PASS | synth-02 5.13, 5.14, 5.15 |
| Plan targets option A; claim-only scope decided by owner | PASS | synth-04 8.4 D1-D3, Phases 1-7 |
| `ci.py` is NOT a `gh` wrapper (imports only `re`, `.classifier`, `.models`) and a poller needs its own injectable runner | PASS | synth-01 2.3 (line 242-243); synth-02 G2; synth-04 Phase 2 intro and C4; confirmed by reading `ci.py:10-15` |
| `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` stated to have been corrected on this point | FAIL | Grep `codebase-context|enrichment/` over `synthesis/` returns 0 matches in all four files. The corrected state itself is real (codebase-context.md line 21 carries a CORRECTION note; gaps-and-questions.md:35 says so), but no synthesis file says it. synth-02 G29 states only that "research-notes.md" was corrected |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| B-1 | IMPORTANT (blocking; checklist item 13) | synth-01 section 2.3, bullet starting "[CODE-CONTRADICTED] The earlier claim that `src/superclaude/pr_submit/ci.py`..." (line 242); also synth-02 row G29 last sentence (line 138) and synth-04 section 9.3 row C4 (line 456) | No synthesis file states that `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` carried the same false ci.py claim and has been corrected. Only research-notes.md is named as corrected (synth-02 G29). The addendum conformance rule requires this statement, and the assembler works from the synth files. | Add to synth-01 2.3 (after "never builds or runs a `gh` command."): "The same false claim in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` (line 21) and in `research/research-notes.md` has been corrected." Mirror one clause in synth-02 G29 ("corrected in research-notes.md and in enrichment/codebase-context.md") and in synth-04 C4 "How the plan handles it". Verify by re-grepping `synthesis/` for `codebase-context`. |
| M-1 | MINOR | synth-01 "Carried to Open Questions" (1-21), synth-02 (Q1-Q19), synth-03 (1-20 and 7.9 items 1-15), synth-04 section 9.2 (Q1-Q33) | Four different open-question lists use overlapping labels; synth-02 Q8/Q9 etc. mean something different from synth-04 Q8/Q9. | Assembler must use synth-04 section 9.2 as the only Section 9 table and not carry the other lists' "Qn" labels into the report. Note only. |
| M-2 | MINOR | synth-03 7.3 "Prompt" row; synth-02 SC-4/G12 versus synth-04 step 3.2 | Earlier files say the prompt is built with `str(int(number))`; synth-04 uses a stricter `type(number) is int` plus regex (it explains why). Not contradictory, but the report should state the stricter rule once. | Note only; final report should quote step 3.2. |
| M-3 | MINOR | synth-04 8.3 says every NEW path is labelled NEW "wherever they appear below"; step 6.4 and steps 7.1-7.6 list `docs/designs/issue-watcher.md` without the NEW label | Labelling inconsistency. | Add "(NEW)" or soften the 8.3 sentence. Note only. |
| M-4 | MINOR | synth-03 6.1 step 1 and synth-04 step 7.5 | Hosting of the poller relies on vendor docs (coder_script cron) while the target template is unknown. Already tagged EXTERNAL-VERIFIED and carried as Q15. | No change needed. |

## Summary
- Checks passed: 12 / 13 (items 1-12 PASS; item 13 FAIL on one element)
- Checks failed: 1 (item 13)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 1 (B-1)
- Minor notes: 4 (M-1 to M-4)
- Issues fixed in-place: 0 (fix_authorization false; no synthesis or research file was modified)

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (a verified FAIL counts as verified)
**Tool engagement:** Read: 24 | Grep: 31 | Glob: 10 | Bash: 0
Not checked: line counts of `cli/recommend/` (1,784) and of `ccsession-orca` (249); the Coder#477 issue text (read-only dependency summarized in research-notes, not re-read); web-page content behind the W01/W02 URLs (external; no web tool used, so no Tavily/WebSearch counters apply).

## Actions Taken
None. Report-only run. No synthesis or research file was edited.

## Recommendations
- Apply fix B-1 (three one-clause insertions), then re-run only the item 13 `codebase-context` row of this check. Everything else passes and needs no rework.

## QA Complete

VERDICT: FAIL
