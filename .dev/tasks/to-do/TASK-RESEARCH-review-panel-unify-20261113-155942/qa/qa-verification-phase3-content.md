# QA Report — Phase 3 Research Gate: Content Verification (qualitative)

**Topic:** Unified Review Panel investigation — research-gate fixes, cycle 1
**Date:** 2026-11-13
**Phase:** research-gate (verification, qualitative) / fix-cycle
**Fix cycle:** 1
**Fix authorization:** false (report only; no file edited except this report)
**Inputs:** `qa/qa-consolidated-findings-phase3.md` (cycle 1, |F_1| = 7), `qa/qa-fix-log-phase3.md`, research files 02, 04, 05, 07, 08, 09, 10, 11 (edited) and 13 (new, commissioned for P3-B1)

---

## Findings

| # | Severity | File | Finding | Evidence |
|---|----------|------|---------|----------|
| 1 | IMPORTANT | `research/09-consumer-plugpoints.md` §5 Corollaries, line 177 | P3-B1 is not fully resolved in file 09. The fix updated §4.2 (lines 153, 161: the post gate runs `ensemble.py`, not the `/sc:reflect` skill), but the §5 corollary still says the tasklist post gate "always" reaches Tier 2 "via the wrapper and UC-2, where `--t2-engine` is 'accepted and ignored until Stage 5' (`SKILL.md:311`)". It sits under the §5 answer (line 174) that Tier 2 means "the legacy reviewer rotation (§7.1) plus the `sc-adversarial-protocol` merge". Both are skill-path facts. The post gate never invokes the skill, so `SKILL.md:311` does not apply to it, and its reviewers are the `T2Model0N` pool, not the §7.1 rotation. The file now contradicts itself (line 161 vs line 177) on exactly the point P3-B1 was raised for, and a synthesis that reads §5 would carry the old error forward. Required fix: rewrite the line 177 corollary to say that the post gate always reaches Tier 2 through the code engine `ensemble.py` (`runner.py:538-545`), not the skill, so `SKILL.md:311` and the §7.1 rotation do not apply (see §4.2, research/13 §2.1). | `research/09`:161 vs :174, :177; `runner.py:538-545` (re-read: `run_tier2_ensemble(config)` then `rc = 0`); `commands.py:253-258` (`click.Choice(["standard","deep"])`); `research/13`:86 |
| 2 | MINOR | `research/05-blocking-calibration.md` §5.2 :180 | "142/142 clustered findings calibrated over 13 runs with a `clusters.json`": the table above it (:166-179) lists 14 runs with a `clusters.json` value (shadow02-15; shadow12 is 0/0). The intended meaning is "13 runs with findings". This was already there before the fix and does not affect P3-B3, which is correct. | `research/05`:162-180; `stat` of `.dev/reflect/pre-*-shadow*/panel/cards/` shows 14 directories with cards |
| 3 | MINOR | `research/07-reflect-merge-contract.md` §8a :404 / §9 C5 :425 vs `research/13` §9.2 :334 | The two files frame C5 differently: file 13 says "Yes, blocking" (moving this caller to a unified panel would be a UC-2 panel, which C5 defers to Stage 5), while file 07 says C5 "does not describe" or "does not govern" this path. Both are true in their own frame, and file 07's §8a key takeaway still lists C5 among the conflicts to resolve. Wording only; synthesis should use file 13's framing. | `research/07`:404, :411, :425; `research/13`:334, :346 |

## Per-finding verification (checks a-d)

| ID | (a) Resolved in substance | (b) Depth kept | (c) New research | (d) Proportionate | Result |
|---|---|---|---|---|---|
| P3-B1 | Mostly. `research/13` (400 lines, Status: Complete) covers `ensemble.py`, `runner.py`, CLI and config, compares with `contract.py`, checks the `panel_lint` lists, reads the tests and checks the post gate. File 07 now has §8a, scoped the C5/C16 rows and Q1/Q6/Q8 item 9, and closed its gaps. File 08 has a writer table and closed Gaps 5/15. File 09 §4.2 traced `executor_model_class`. **Residual: file 09 §5 line 177 left stale (finding 1).** | Yes. The skill-path analysis in 07 is kept; the new text adds scope corrections rather than replacing it | Yes. Answers the commissioned gap with code citations; effort tags on section headings and every Key Takeaway | Yes. D1/D2 "Critical" rest on verified code: the scorer is score-only (`ensemble.py:557-561`), deviation fields are clean defaults (:442-471), `_halted_reason` inputs never change (`contract.py:361-382`), and reviewers see only the tasklist body (:619-630) | FAIL (finding 1) |
| P3-B2 | Yes. 0 bullet or numbered lines without an `[E1-3]` tag (grep); 172 tagged lines. Spot-checked provenance with `git log -S`: `--hard-exclude-class` and `_REFLECT_PREFIX` came in `d2d8a2d16` (E1); `select_env` came in `9163bd1c7` (E3). Matches the tags | Yes, tags only | n/a | Yes | PASS |
| P3-B3 | Yes. `stat` of card mtimes: earliest shadow02 2026-11-12 22:22:58, latest shadow12 2026-11-13 02:42:28. Matches the new text exactly. The cards are tracked, but their mtimes predate the commit `792cf8c52` (15:11), so they are the original write times | Yes | n/a | Yes | PASS |
| P3-B4 | Yes. The 6.70% figure is restated as a descriptive overlap figure; `stage0a-report.md:295` says "descriptive and seeds no gate", and :297 gives 24/358. No research file now uses it against debate (grep) | Yes; the gap entry was replaced by its resolution | n/a | Yes. The row now says no evidence measures debate correctness | PASS |
| P3-B5 | Yes, in both 02:145 and 08:331/:465/:484. `git show 4a22d742:.../audit-D/audit2.py`: `rows_total += 1` at :140 comes before `if len(mem) < 3: continue` at :145, and `chain_total` is at :154 | Yes | n/a | Yes | PASS |
| P3-B6 | Yes. Rows 7a-c, 17a-b and 25a-b each state their own fix authorization. An awk recount gives 43 rows, 32 Yes. The non-Yes breakdown 3 read-only (#1, #14, #38) + 4 followed by a fix (#5, #13, #32, #35) + 2 UNVERIFIED (#18, #22) = 9 checks out. Cited lines `task/SKILL.md:211-213, :225, :241, :254, :256`, `tech-reference/SKILL.md:537-539` and `readme/SKILL.md:584, :600-601, :604, :607` were re-read and match. No stale 39/28 left | Yes | n/a | Yes | PASS |
| P3-B7 | Yes. I re-ran `uv run python scripts/reflect_shadow_exit.py`: exit 1, 73 lines. The fenced block in file 11 §8 matches byte for byte, except for one added `EXIT_CODE=1` line, which is labelled as the exit code | Yes; the summary bullets are kept | n/a | Yes | PASS |

## Summary

- Fixed findings checked: 7 of 7. Fully resolved: 6 (P3-B2..B7). Partially resolved: 1 (P3-B1; one stale sentence in file 09).
- New research file `research/13-gap-fill-reflect-ensemble.md`: meets its commission. Every load-bearing claim I sampled matches the source.
- Blocking: 1 (IMPORTANT). Minor: 2 (notes only).
- |F| after cycle 1: 1 open blocking finding (down from 7).

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No `## Inherited Structural Verdict` was supplied, so I worked standalone. I relied on the fix log only for *where* each edit was made, never for *whether* it is correct.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- P3-B1 core claims re-read in source: `ensemble.py:74, :423-426, :442-471, :540-580, :601-630, :772-773, :789, :817, :886-895`; `runner.py:538-546`; `commands.py:253-258, :365`; `config.py:316-320, :334-335`; `contract.py:225-260, :276-300, :361-382`. Grep found 0 `executor_model|panel_lint|cli.review` hits in `ensemble.py`. `git diff --stat origin/master` on the 5 reflect files is empty (confirms file 13 §1.7).
- I re-ran `uv run pytest tests/cli/reflect/ -k ensemble -q -p no:cacheprovider`: 58 passed, 295 deselected; the `test_ensemble_*` files total 2036 lines (confirms file 13 §7).
- P3-B7: I re-ran the shadow-exit script and diffed its output.
- P3-B3: `stat` of all 14 card directories. P3-B5: `git show` of `audit2.py`. P3-B6: awk recount, plus re-reads of the cited SKILL.md lines.
- Cross-file sweep for stale claims about which route the post gate takes, across research files 01-06, 10-12 and research-notes: none outside file 09 §5.

1. Claims independently verified against source: about 45.
2. Files read: `ensemble.py`, `runner.py`, `commands.py`, `config.py`, `contract.py`, `scripts/reflect_shadow_exit.py`, `audit2.py` (git show), `stage0a-report.md`, `sc-tasklist-protocol/SKILL.md`, `task/SKILL.md`, `tech-reference/SKILL.md`, `readme/SKILL.md`, research files 02, 04, 05, 07, 08, 09, 10, 11 and 13, plus the consolidated findings and the fix log.
3. Not a zero-finding report. Finding 1 was found by cross-reading file 09 beyond the lines the fixer edited.
4. No web research was needed. Tavily was not used and there was no fallback.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 4 | Glob: 0 | Bash: 14

## Verdict

**Verdict: FAIL** — 1 IMPORTANT finding open (finding 1, `research/09-consumer-plugpoints.md:177`, a stale corollary from P3-B1). It is a one-sentence fix, and no new research is needed. The 2 MINOR findings are notes only.

## QA Complete
