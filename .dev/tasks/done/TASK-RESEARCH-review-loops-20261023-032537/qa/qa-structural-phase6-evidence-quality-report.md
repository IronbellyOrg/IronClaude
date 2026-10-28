# QA Report: Phase 6 Gate, Evidence Quality

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks (TASK-RESEARCH-review-loops-20261023-032537)
**Date:** 2026-10-24
**Phase:** phase-gate (Phase 6, final state after the report, fidelity and anti-omission gates)
**Lens:** Evidence quality (structural)
**Fix cycle:** N/A (report-only, `fix_authorization: false`)
**Target:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md`. It has 1,316 lines and sha256 `41145b5e9660967e6f6498efb90da18bbfcd51eb3a81a0850fbdcde29fca40a0`, which matches the expected prefix `41145b5e9660967e…`.

---

## Overall Verdict: FAIL

Verdict: FAIL

The report has 2 new defects, both MINOR. The rest of the citation layer held up under a check of every citation, with no sampling: all 389 package-internal `path:line` citations resolve and the cited lines support the claims. This lens requires FAIL for a defect of any severity.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Report identity and size | PASS | `wc -l` gave 1316. `sha256sum` gave `41145b5e…fca40a0`. |
| 2 | Every package-internal `path:line` citation exists and is within the file's bounds | PASS | A scripted extractor, run once over the full report, resolved 448 `path:line` tokens. These include bare `:N` continuations and "evidence deck `:N`" forms, and the aliases `ADV/`, bare `return-contract.md`, `merged-root-cause-analysis.md`, `merge-log.md` and `scope-0N.md`. 389 are package-internal. None is missing and none is out of range. The evidence deck has 900 lines (`wc -l`); the cited maximum is :890. |
| 3 | Each cited package line supports its claim | PASS | I printed every target line for every one of the 389 citations next to its claim (first and last lines for ranges) and judged each one. The extractor attached six continuations to the wrong file, and I resolved those by hand: Report:256 `(:8)`/`(:3)` are the CI merged verdict and consensus summary; Report:256 `(:146)` is `research/04-session-43582de1.md:146`, the M-18 row; Report:896 "credential case `:381`" is `research/06-session-0690ee9f.md:381`; Report:896 "rendering and baseline case `:173-178`" is `research/03-session-6f744b87.md:173-178`; Report:1116 `:161-163` is `ADV/merge-log.md:161-163`, read directly and supporting the claim. I found no unsupported package citation. |
| 4 | Textual line and section citations | PASS | 14 "line N" forms checked, for example Report:875 lines 227, 170 and 410, Report:876 line 210, Report:479 SKILL.md 779 and 1393, and Report:1305 card headings. 14 "`file`, section N" forms checked against the actual `^## ` headings of case files 01, 03, 04 and 05 and hypothesis-01. All match. |
| 5 | No hallucinated paths: every path token exists | FAIL (E-01) | I checked existence for 221 distinct path tokens. 4 did not resolve. (a) The original CI plan `…/ci-followup/.dev/tasks/to-do/TASK-WF-spec-20261022-211556/…md` at Report:851 is gone; this is known defect L3. (b, c) `agent-aba0ed57846538ad4.jsonl` and `agent-a815d047710b89c22.jsonl` at Report:1116 are E-01. (d) `variant-1..5-original.md` at Report:1092 is range shorthand, and all five files exist. |
| 6 | External paths (existence only) | PASS (L3 known) | 48 external `path:line` tokens, covering the src/superclaude protocol refs, the CI second-review `REPORT.md`/`adversarial/*`, the `t12-review-*.md` files, the Orca `coverage-matrix.yaml`/`merged-verdict.yaml` and the ci-followup `progress.md`. All exist and are in range, except the L3 plan. I did not judge the content of external lines, as the brief instructs. |
| 7 | Session-log record citations (JSONL) | UNVERIFIABLE (content); FAIL on locatability (E-01) | The brief says not to open session `.jsonl` logs. Existence only: the 6 credential nested logs exist in the `0690ee9f…/subagents/` directory, and so do `43582de1…jsonl` and `agent-ascope-review-rules-…jsonl`. Record numbers, timestamps and UUIDs were checked only indirectly, through the case files that carry them. |
| 8 | Git-dependent claims | UNVERIFIABLE here | `git show 2165ae25:…` line pins, "byte-identical to `c6009cd3`" (Report:209) and the `6dc56b1a`/`00448800` hashes (Report:229) need Git, so they cannot be checked here. The report labels them as source reads with dates, not as observed history. I ran no Git command. |
| 9 | Provenance and identity statements (hashes, mtimes, task-log entries, counts) | FAIL (E-02) | Task-log entries `[05:24Z]`, `[05:35Z]`, `[06:32Z]`, `[07:09Z]`, `[03:52Z]` and `[03:45Z, actual user clarification]` exist and say what the report claims. The deck mtime is 16:51:42, as claimed. There are 23 research files and 11 synthesis files, all five cards have ten chapters plus a 10.5 record and the "Post-debate" header, there are 15 deck questions and 18 applicability questions, and the before/after rubric strings in `historical-review-rules.json` match Report:231. The component-change note at Report:1257 is incomplete: see E-02. |
| 10 | No unverified assertion presented as fact | PASS | Self-reports are labelled as such (Report:471, :781, :1297-1316). The uncited claim in Report:8 that no Git command was run in report-gate cycle 2 or by the cycle-3 fixer is backed by `qa/qa-fix-log-cycle2.md:21,67,134`. Current-rule statements are dated and kept separate from historical loads. |
| 11 | Citations in the other deliverables (bounds and existence) | PASS (E-01 mirror) | synth-01 through synth-06 have 386 tokens and gaps-and-questions.md has 10; none is out of range. The three report-gate tokens the script flagged (`qa-fix-verification-cycle3.md:1235`, `:1287`, `…qualitative-cycle3.md:901`) are false positives, because those `Report:NNN` continuations point at the report. The fidelity and anti-omission gate decisions contain no `path:line` tokens, and all their paths exist. synth-06 has the same E-01 bare names at :177. |

**Counts:** 448 report `path:line` tokens (389 package-internal content-checked, 48 external existence-checked, 11 session-log existence-only); 221 distinct report path tokens existence-checked; 28 textual line or section citations; 396 citation tokens in the other deliverables bounds-checked.

**Known user-accepted defects (recorded, not new):** J1 is the stale status lines (Report:5, :1241, and the 10.10 status wording). L1 is the incomplete Git disclosure. L2 is that case-06's Git use is described too narrowly. L3 is that the original CI plan cited at Report:851 (formerly :848) no longer exists. Ranks and order are unchanged: V1 > V3 > V2 > V5 > V4.

## Summary

- Checks passed: 8 / 11 (items 1-4, 6, 8, 10, 11; items 6 and 11 carry the known L3 or the E-01 mirror)
- Checks failed: 2 (items 5 and 9; item 7 also fails on locatability, from the same E-01 defect)
- Unverifiable: 2 (item 7 record contents, item 8 Git-only claims), because the brief forbids opening logs and running Git
- Critical issues: 0. Important: 0. Minor: 2.
- Issues fixed in-place: 0 (report-only)
- **Confidence:** Verified: 9/11 | Unverifiable: 2 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 15 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 42 (read-only inspection plus one `uv run python` citation resolver in a private `/tmp/ironclaude-batch.*` directory, removed afterwards). No Git, no session-log content opened, no package file edited, no web research.

## Issues Found

| ID | Severity | Location path:line | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| E-01 | MINOR | `RESEARCH-REPORT-review-loops.md:1116`; mirror `synthesis/synth-06-questions-evidence.md:177` | The report cites two nested reviewer logs, `agent-aba0ed57846538ad4.jsonl` (record 79) and `agent-a815d047710b89c22.jsonl` (record 38), by bare name with no directory. The report's only rule for bare nested `agent-*.jsonl` names (Report:483) places them in the credential session's `subagents/` directory, but neither file is there. A reader following the report's own key cannot find them. | `ls` in the credential directory `…issue-358-litellm-key-env/0690ee9f-…/subagents/` found neither file. `find /config/.claude/projects` found both under `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/`. Only the cited `ADV/merge-log.md:165-166` gives that directory, and the report row does not. | Add the `bbddbf85-…/subagents/` directory to both names in Report:1116 and synth-06:177. Alternatively, add an explicit note to 10.5 that its bare nested names resolve under that directory, not under the credential directory in the Section 6 path key. |
| E-02 | MINOR | `RESEARCH-REPORT-review-loops.md:1257` | The note under the assembly component-identity table says which components changed after assembly. It names only Task Step 6.18 (synth-01, 04, 05) and Steps 6.29/6.32 (synth-01, 02, 04). It leaves out report-gate cycle 2 (synth-04), the Step 6.39 anti-omission recovery (all six components, including synth-03 and synth-06) and Step 6.42 (synth-01, 04, 06). Read alone, it implies that synth-03 and synth-06 still match their listed hashes. They do not. | Live sha256: synth-03 `b0a561a5…` against the table's `ca519125…`; synth-06 `bdf94b0d…` against `bcffe37a…`. The fix logs patched them: `qa/qa-anti-omission-fix-log.md:127,130,198-199,212-213` and `qa/qa-anti-omission-fix-log-cycle2.md:88`. Report:1293 (10.10) discloses these steps, so the two passages disagree. | Complete the list at Report:1257, or replace it with "all six components have changed since assembly; see 10.10, last row, for each step". |

## Actions Taken

None. This was a report-only review. I edited no package file. The only file written was a temporary resolver script in a private `/tmp` directory, deleted at the end (cleanup confirmed).

## Recommendations

- Route E-01 and E-02 to the single serialized fixer for this gate. Both are one-line wording corrections; neither changes a rank, a count or a causal claim.
- Keep J1, L1, L2 and L3 recorded as known, user-accepted defects. This lens found nothing new in those families.

| Status | Result |
|---|---|
| DONE | Checked all 389 package-internal citations in the report against their cited lines. All resolve and support their claims. |
| DONE | Checked existence for 221 report path tokens and 396 citation tokens in the other deliverables. The only gaps are E-01 and the known L3. |
| DONE | Found 2 new MINOR defects (E-01 directory missing from the bare log names; E-02 incomplete component-change note). |
| NEXT | The fixer applies E-01 (Report:1116, synth-06:177) and E-02 (Report:1257); a fresh verifier then re-checks both. |

## QA Complete

## Erratum: Summary Recount (Phase 6 /task gate, 2026-10-24, finding G6-49)

**Attribution:** appended by the Phase 6 /task phase-gate fixer, applied by the parent. The lens text above is unchanged.

Item 8 (Git-dependent claims) is UNVERIFIABLE in the Items Reviewed table (`:29`), but the Summary lists it among the passed checks (`:40`) and also among the unverifiable ones (`:42`). Recount from the table: 7 of 11 passed (items 1-4, 6, 10 and 11); 2 failed (items 5 and 9), with item 7 also failing on locatability from the same E-01 defect; 2 unverifiable (item 7's record contents and item 8). The Confidence line's "Verified: 9/11 | Unverifiable: 2" agrees with this recount (7 PASS plus 2 FAIL verified). The verdict (FAIL) and the two issues are unchanged.
