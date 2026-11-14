# QA Report: Report-validation fix verification (qualitative), cycle 1

**Topic:** Unified Review Panel research report (`RESEARCH-REPORT-review-panel-unification.md`, 4282 lines)
**Date:** 2026-11-14
**Phase:** report-qualitative (fix-cycle verification)
**Fix cycle:** 1
**Fix authorization:** false (report only; no file edited except this report)
**Inputs read:** `qa/qa-consolidated-findings-phase6.md` (39 blocking findings), `qa/qa-fix-log.md` (Cycle 1), the report (Sections 1, 2.2, 3, 4, 6 C-03/C-05/C-10/C-11/C-14/C-18, 6.X, 7, 8, 9, 9.5), and the code, tests and skill files the fixes cite.

---

## Overall Verdict: FAIL

Two blocking (IMPORTANT) findings are open (F-1, F-2). The 39 original findings are resolved in substance except where F-1 and F-2 show a fix left a hole. No debate winner was overturned, the four debates still read `partial`, the allowed `[CONTRADICTION]` is the only one left, and the report is still report-only.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Design-content fixes rest on evidence, invent no decision, and open questions have an owner in Section 9 | FAIL (F-1, F-2) | P6-B18: C-11 (L1921) gives route 1 / route 2, derivation rule and fixtures, all [proposed]; cites match `sc-adversarial-protocol/SKILL.md` return contract (fields `merged_output_path`..`unaddressed_invariants`, no `merge_method`) and artifact list (no `merged-verdict.yaml`), `panel_lint.py:288-291` (`adversarial_unavailable`, F2/F3 row) and `contract.py:310-326`; route choice left open as Q-59 (L4192). P6-B19: SC-14 (L538) rewritten, M1-20 and M1-21 added (L3662-3663) with files, fields [proposed] and tests; M4 Dependencies (L3706) corrected. P6-B20: X14 added (L2812) with per-mode rules, thresholds left to Q-60. P6-B21: `cli/review/brief.py` and `review brief --check` [proposed] in M1-11 and M1-15 (L3653, L3657). P6-B22: "pin enforced" now "instructed and audited" (L2768), M1-22 probe added (L3664), G-38/G-45 removed from M1-10 closes list. P6-B24: C-18 open point (L2382) plus Q-61; I re-checked `rf-qa.md:10,133,518,327-328` (Bash declared; only two command mentions, `make`/`pytest`, at :327-328). P6-B27: `lenses.py`/`load_lens`, `--snapshot`/`merge_round(..., snapshot=None)`, `register_check` added with files; I verified `cluster_cmd.py:98-103` has `--snapshot`, `ledger.py:107` signature, `manifest_cmd.py:67-69` required hash options. P6-B38: dispatch site and `grade prep`/`grade apply` sequence match C-05 `proposal-merged.md` lines 243-263 (not invented); `~/.claude/agents/finding-grader.md` exists, no `src/` copy. Holes: F-1 (X14 has no M1 step), F-2 (Q-58 not carried into M3, 9.2 not updated). |
| 2 | No debate winner overturned; four debates still `partial` with HIGH invariants open | PASS | C-03 winner A, `partial`, INV-013/INV-009 (L1382); C-05 winner B (Option D), 11 HIGH (L1540); C-14 winner B, 3 HIGH (L2120); Section 7 risk table (L2680-2683) and 9.5 (L4176) unchanged: 2 + 11 + 10 + 3 = 26; new "Rating of the adopted resolution" lines (C-03 L1380, C-05 L1538, C-11 L1923, C-14 L2118) re-rate effort and risk only and say the winner is unchanged; Options Comparison condition paragraph (L2619) states Option B's risk depends on the four gates and owners O-4, G-59. |
| 3 | New migration steps concrete, in gap-coverage tables where they close gaps | PASS with F-1 | M1-20, M1-21, M1-22 each name files, [proposed] fields and tests (L3662-3664). Gap-coverage table (L3723-3838) carries MS-24 (L3778), BL-11/BL-12 "core part M1-20" (L3790-3791), BL-13 "M1-16", MS-11 and DOC-20 "unknown, not closed" (L3729, L3736). Recount by script of Section 4 rows: 144 matched by id pattern plus the combined DOC-71..77 row = 145; Critical 15, Important 66, Minor 64; tracks M1 56, M2 21, M3 18, M4 16 match 4.2 (L755-770) and Section 9 (L3939). Exception: exposure X14 (see F-1). |
| 4 | Section 8 gate list covers `pr_submit`, plugin mirror, persisted-format rule, replacement assertions | PASS (minor notes N-2, N-3) | G-pr (L3857): `uv run pytest --collect-only -qq -p no:cacheprovider tests/pr_submit` gives 2258 collected; `test_severity_router.py` tests `test_t301`, `test_t302`, `test_t310`-`t312` exist at the cited lines. G-skills (L3858): 1087 collected for the nine files. Plugin mirror: `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` and `plugins/superclaude/commands/spec-panel.md` exist; `test_review_brief_placement.py:129-134` asserts the byte copy; named in M1-11, M3-01, M3-08, G10. Persisted formats: M1 intro rule (L3639), M1-05, M1-07, M1-12, per-track rollback lines, 8.5 risk row (L3909); `reflect_shadow_exit.py:205-235` validates every `pre-*/panel/manifest.json` as claimed. G1-G11 each now carry a replacement assertion or reason. |
| 5 | Report-only; `[CONTRADICTION]` raised openly once; parsed-sparse figure counts only | PASS | `grep CONTRADICTION`: the only flag text is the Section 7.1.3 vocabulary flag (L2777); the rest are echoes (M1-07, M1-08, M1-16, M3-08, L2911, L3371, L3891, L3921, L3929, Q-54). Every "roadmap" hit says report-only or "later roadmap". I re-ran `recount_tier_decision.py`: `non-shadow files: 39`, rule/flag rows as quoted in C-14 Evidence (L2106); "decisive in 0 for certain and at most 1" is attributed to the debate's `escalation_figure_after_check`, not to the script. 18 + 9 + 2 = 29 and 29 + 5 = 34 add up. |
| 6 | One coherent whole: Sections 3, 4, 7, 8, 9 agree on the new items | FAIL (F-1, F-2) | Agree: MS-24 (Sections 3 SC-16, 4, 6 C-11, 7.1.3, 8 M2-02, coverage table, 9.5 Q-59); SC-18..SC-23 to G-new and 8.6; X14 to 7.1.4, SC-14, Q-60; Q-61 to C-18, 7.1.3, M4-06. Disagree: X14 has no M1 step; Q-58 states something Section 8 does not do. |

## Summary
- Checks passed: 4 / 6 (checks 2, 3-with-note, 4, 5 pass; checks 1 and 6 fail)
- Checks failed: 2
- Critical issues: 0
- Blocking (IMPORTANT) issues: 2
- Minor notes: 5

## Issues Found (blocking)

| # | Severity | Section | Finding | Evidence |
|---|---|---|---|---|
| F-1 | IMPORTANT | 3 SC-14 (L538), 6.X Option B (L2581), 7.2 X14 (L2812), 8.2 M1 and M4 Goals (L3705), M1-04, M1-07, M4-07 | The report now says "once M1 delivers exposures X1-X14" and SC-14 (iv) tests "one case per coverage mode (X14)", but no M1 step builds the coverage modes. X14 (coverage mode per slot: `redundant`, `partitioned`, `per-lens`, with per-mode quorum, `degraded` and `support` rules) was added as a core exposure to fix P6-B20, yet the lens entry of M1-04 (fields: severity words, categories, primary location, id grammar, blocking predicate, cap) has no coverage field, and M1-07 defines only the redundant-mode quorum (`min(2, panel_size)`). The only mentions of coverage mode in Section 8 are M4-07 (a consumer declaring its mode) and G-new. This is the same class of defect as P6-B27 (a core interface named in the target with no migration step), so the SC-14 acceptance has no producer and the M4 "no core edit" claim is not backed for rf-qa partitioned runs. Fix: add a `coverage` field to the M1-04 lens entry and the per-mode quorum, `degraded` and `support` rule (marked [proposed], thresholds still Q-60) to M1-07, and keep SC-14 (iv) tied to that step. Axis: omissions. | `grep X14`: hits only at L538, L2581, L2792, L2796, L2812, L3705, L3717, L4057, L4193. `grep "coverage mode"`: M4-07 (L3717) and G-new (L3864) only in Section 8. M1-04 text L3646; M1-07 text L3649 (quorum `min(2, panel_size)` only). |
| F-2 | IMPORTANT | 9.5 Q-58 (L4191), 8.2 M3-01 (L3693), 9.2 (L4062-4066) | Fix for P6-B5 is incomplete and states something false about Section 8. Q-58's Suggested Resolution says "Until then D14 stays Critical as written and the five subcommands are marked [UNVERIFIED] in the M3 steps"; no M3 step carries that mark or names Q-58 (M3-01, which closes D14, has no `UNVERIFIED` and no Q-58). P6-B5 also asked for the id in 9.2; 9.2 lists no Q-58, although it lists other non-gap questions that carry an [UNVERIFIED] claim (Q-45, Q-46). Fix: add "the five subcommands are [UNVERIFIED] until Q-58 is read" to M3-01 Details (and to the SC-12 reachability row, which pins them), and add Q-58 (and Q-61) to the 9.2 [UNVERIFIED] row; or delete the sentence in Q-58. Axis: contradictions (Section 9 vs Section 8). | `grep "Q-58"`: only L582 (Section 4 intro), L601 (D14), L4055 (9.1 index), L4191. M3-01 row L3693 closes "D14, MS-07, G-69, G-70" with no mark. 9.2 table L4062-4066. |

## Minor notes (never fail, not rechecked)

| # | Section | Note |
|---|---|---|
| N-1 | 7.4.1 (L2878), 8.3 G8 (L3853) | The list of edits that fall outside the C6 allowed sections names M2-02 (`:714`) and M2-09 (`:1955`, `:1958`) but not the new M1-10 edit at `SKILL.md:646` (section 7.1), which M1-10 itself flags. The G8 cell names section 7.1 in general, so the gate still works. |
| N-2 | 8.3 G-skills (L3858) | Marked UNVERIFIED ("whether any of these suites pins the Wave 4 or Stage 10.5 review text was not read"). A grep shows it does: `tests/commands/test_workflow_command.py:245-261` asserts the exact Wave 4 call string `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` in the skill and the command, and `tests/tasklist/test_tasklist_cli.py:576-580` pins "BEFORE Stage 10.5". M3-02 changes that Wave 4 text, so the replacement assertion could be named now. |
| N-3 | C-11 (L1921) | The derivation rule requires a non-null `convergence_score` for `adversarial`, and the next sentences say a null score "is not a `merge_method` question: the wrapper degrades it". Both can be true (debate return contract versus reflect contract) but the wording reads as a conflict. |
| N-4 | 3 SC-14 (iii) (L538) | The test case uses a `verify-only` kind, while M1-07 says the verify-only port is not built before the C-13 gate. State that the case runs only if C-13 selects the kind. |
| N-5 | 6.X Option B "How it works" (L2573) | Still says "the core exposes the 13 exposures X1-X13"; the Pros cell (L2581) and 7.2 say X1-X14. Section 7.2 explains X14 is added by the report, so make L2573 say so. |

## Inherited Structural Verdict: Reliance Audit

No `## Inherited Structural Verdict` block was supplied; standalone behaviour applied (no structural PASS was relied on).

## Self-Audit

**(a) Reliance list:** none. The fix log's own claims ("checked by script", "ran the command") were not relied on; each was re-run or re-read below.

**(b) Independent semantic checks (>= 1 required):**
- Section 4 gap table recount (145 rows; Critical 15, Important 66, Minor 64; tracks M1 56, M2 21, M3 18, M4 16, none 34): script over the report; matches 4.2, 4.3, Section 1 and Section 9.
- G-pr and G-skills collected counts re-run: 2258 and 1087 tests collected, as stated.
- C14 recount script re-run: 39 non-shadow files, key `coverage_degraded` present in all 39 files.
- Code and test cites re-read: `manifest_cmd.py:55-75`, `ledger.py:107`, `cluster_cmd.py:96-104`, `findings.py:345-351`, `ledger_cmd.py:13`, `reflect_shadow_exit.py:205-235`, `test_review_severity_mapping.py:45-62`, `test_review_brief_placement.py:125-136`, `sc-adversarial-protocol/SKILL.md:365-452`, `panel_lint.py:280-295`, `contract.py:310-326`, `rf-qa.md:10,133,327-328,518`, `sc-tasklist-protocol/SKILL.md:1625-1637`, `sc-workflow-protocol/SKILL.md:87-91`, `sc-reflect-protocol/SKILL.md:87,311,340-348,714`, `tests/pr_submit/test_severity_router.py:30-65`, C-05 `proposal-merged.md:186-263`.
- F-1 and F-2 were found by tracing each new item (X14, Q-58) through Sections 3, 7, 8 and 9 with `grep`, which the fix log's scripted checks (column counts, row counts) do not cover.

**Confidence:** Verified: 6/6 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% on the six checks as read. Limits: I did not re-read all 4282 lines, only the fixed sections and the text around them, and I did not re-verify the wording-only or count-only fixes (P6-B1 to B4, B6 to B9, B14, B16, B29, B30, B39) beyond spot checks of B1, B3, B6, B8, B14 against Sections 2.2, 4 and 9.
**Tool engagement:** Read: 22 | Grep: 8 | Glob: 1 | Bash: 14 (Read + Grep + Glob = 31, above the 6 checks)
**Web research:** none; Tavily not needed.

## Recommendations
- Fix F-1 and F-2 (small edits to Sections 8, 9.2 and 9.5; no debate winner is touched), then re-verify those two items in cycle 2.
- N-1 to N-5 may be applied at the same time; they are not rechecked.

## QA Complete
