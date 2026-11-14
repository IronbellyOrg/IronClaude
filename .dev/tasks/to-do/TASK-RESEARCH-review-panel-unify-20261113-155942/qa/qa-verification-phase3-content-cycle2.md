# QA Report — Phase 3 Research Gate: Content Verification (qualitative), Cycle 2

**Topic:** Unified Review Panel investigation — research-gate fixes, cycle 2
**Date:** 2026-11-13
**Phase:** research-gate (verification, qualitative) / fix-cycle
**Fix cycle:** 2
**Fix authorization:** false (report only; no file edited except this report)
**Inputs:** `qa/qa-consolidated-findings-phase3.md` `## Cycle 2` (|F_2| = 1, P3-B1-r), `qa/qa-fix-log-phase3.md` `## Cycle 2` (edits at `research/09-consumer-plugpoints.md` :177 and :295, sweep of 07/08/09/10), plus a regression check on the cycle-1 fixes (P3-B1..P3-B7)

---

## Findings

| # | Severity | File | Finding | Evidence |
|---|----------|------|---------|----------|
| 1 | IMPORTANT | `research/09-consumer-plugpoints.md` §5 Key Takeaway line 183 and §8 item 8 line 259 | P3-B1-r is fixed in wording at :177 and :295, but not in substance across file 09. Two conclusions still rest on the old assumption that every consumer reaches Tier 2 through the `/sc:reflect` skill. (a) KT :183: "turning it on for consumers is a reflect flag change (`--t2-engine`), not a consumer change." The corrected corollary two bullets above it (:177) now says the reflect CLI has **no** `--t2-engine` option and the skill switch does not apply to the post gate. So for the only blocking consumer, the tasklist per-phase post gate, turning the panel on is neither a flag change nor a consumer change: it is a code change in `runner.py`/`ensemble.py`. That is what KT :161 says ("A panel that plugs in here replaces `ensemble.py`, not the skill-path Tier 2"). The file contradicts itself again (:183 vs :161/:177). (b) §8 item 8 :259 ("Today the only switch is reflect's `--t2-engine`... putting the engine choice in the panel template or a project default... avoids editing five skills to turn the panel on") is the design input a synthesis will copy. It never says that the post gate has no switch at all and that no template or skill edit reaches it, because `runner.py:540-545` hard-wires `run_tier2_ensemble` whenever `--depth` is `standard` or `deep`. A synthesis built on §8.8 would plan a turn-on path that misses the blocking gate. The cycle-2 sweep missed both lines because it searched only for "post gate" near skill terms, and neither line names the post gate. Required fix: scope :183 and :259 to skill-path consumers (workflow Wave 4, tasklist Stage 10.5, brainstorm and design hooks), and state that the post gate needs a code change in `runner.py:538-545`/`ensemble.py` (no flag exists, `research/13` §2.1, §5.1), with citation. | `research/09`:161, :177, :183, :259; `runner.py:537-545` (re-read: `expected_tier = 2 if config.depth in {"standard", "deep"} else 1`; `run_tier2_ensemble(config)`; `rc = 0`); Grep `t2.engine` over `src/superclaude/cli/reflect/` = 0 matches; `commands.py:254-255` (`click.Choice(["standard","deep"])`); `research/13`:85-86, :204 |
| 2 | MINOR | `research/09-consumer-plugpoints.md` §8 item 4 :255 | "executor class to exclude (tasklist post reads `executor_model_class`)" lists the post gate's executor class as an input the surface must accept, without the §4.2 (:153) qualification that the wrapper reads it but never uses it on the ensemble route. The statement is literally true (the wrapper does read it), so this is a note only. A synthesis should take the qualification from :153. | `research/09`:153 vs :255 |

## Per-finding verification, cycle 2 (checks a-d)

| ID | (a) Resolved in substance | (b) Depth kept | (c) New research | (d) Proportionate | Result |
|---|---|---|---|---|---|
| P3-B1-r (:177) | Yes for this sentence. It now says the post gate always reaches Tier 2 through `run_tier2_ensemble`, never `/sc:reflect`, and that neither the legacy rotation nor `--t2-engine` (`SKILL.md:311`) applies. Re-read `runner.py:538` (`expected_tier = 2 if config.depth in {"standard", "deep"} else 1`) and :540-545 (`run_tier2_ensemble(config)`, `rc = 0`): matches. `SKILL.md:311` holds "accepted and ignored until Stage 5" (Grep). Grep `t2.engine` in `src/superclaude/cli/reflect/` gives 0 matches, which matches the claim. The cited `research/13` §2.1 (:85-86) and §5.1 (:204) say the same thing. Now consistent with :153 and :161 | Yes. The workflow and Stage 10.5 half of the corollary is kept, and the sentence gained a citation | n/a (none commissioned) | Yes. [CODE-VERIFIED] [E1] is justified by the cited code | PASS for the line |
| P3-B1-r (:295) | Yes for this sentence. The Summary now splits the advisory skill-path consumers from the blocking post gate, and says the post gate runs `ensemble.py`. The rest of the paragraph is unchanged | Yes | n/a | Yes | PASS for the line |
| P3-B1-r (sweep, 07/08/09/10) | **No.** File 09 still has two generalized conclusions (:183, :259) built on the skill-only route. See finding 1. My Grep for `t2.engine` over files 07, 08, 09, 10, 13 and research-notes: every hit in 07, 08 and 10 is skill-path or manifest text that is correctly scoped (07 :425 C5 row states its skill-path scope). The only unscoped conclusions are 09 :183 and :259 | — | — | No. The :183 claim that turning the panel on "is a reflect flag change" is stronger than the evidence, because the post-gate route has no flag | **FAIL (finding 1)** |

## Regression check of cycle-1 fixes

File modification times (`stat -c %y`): research 02 (20:49), 04 (20:51), 05 (20:50), 07 (20:58), 08 (20:58), 10 (20:53), 11 (20:54) and 13 (20:56) were all last written **before** the cycle-1 content verification report (21:03:59). Only `research/09` (21:07:11) and the fix log (21:07:44) changed afterwards. That agrees with the fix log's statement that only file 09 changed in cycle 2. I also re-checked each fix directly:

| Cycle-1 ID | Re-check | Result |
|---|---|---|
| P3-B1 (file 09 parts) | §4.2 :153 (`executor_model_class` traced, gate claim [CODE-CONTRADICTED]), KT :161 (engine is `ensemble.py`) and Gaps :272 (resolved entry) are all intact | no regression |
| P3-B2 | file 04: Grep for bullet or numbered lines without an `[E1-3]` tag returns 0 | no regression |
| P3-B3 | file 05 :190 still has the 2026-11-12 22:22 to 2026-11-13 02:42 UTC window and the per-run times | no regression |
| P3-B4 | file 05 Debate row (:377) still describes 6.70% as a descriptive overlap figure with no correctness claim | no regression |
| P3-B5 | 02 :145 and 08 :331, :465, :484 still have "195 chained rows among 1398 ledger rows in total" with `audit2.py:139-155` | no regression |
| P3-B6 | file 10 :131 and :136 still give 43 call sites and 32 needing a fix. No stale 39 or 28 total remains (Grep) | no regression |
| P3-B7 | file 11 §8 still has the fenced output block (:213-288) with `EXIT_CODE=1`, run date and command line (:209) | no regression |

## Summary

- Cycle-2 blocking finding checked: 1 (P3-B1-r). Both edited lines (:177, :295) are correct and match the source code. In substance, though, the finding is still open: file 09 :183 and :259 still generalize the skill-path turn-on switch to all consumers, which contradicts :161 and :177 (finding 1, IMPORTANT).
- Cycle-1 fixes: no regression (7 of 7 re-checked).
- Blocking: 1 (IMPORTANT). Minor: 1 (note only).
- |F_3| after cycle 2 = 1. That equals |F_2| = 1, so the count did not go down. This was the second and last fix cycle allowed.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No `## Inherited Structural Verdict` was supplied, so I worked standalone. I relied on the fix log only for *where* the edits were made, and on file mtimes only to scope the regression check. Each fix was still re-checked directly.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Read `runner.py:530-548` directly and confirmed the route condition and the unconditional `rc = 0` (lines 538, 540, 544-545).
- Grep over `src/superclaude/cli/reflect/` for `t2.engine`: 0 matches, which confirms the "no `--t2-engine` option" claim. Read `commands.py:250-260` and confirmed `click.Choice(["standard", "deep"])`.
- Grep over `SKILL.md` confirmed the UC-2 "accepted and ignored until Stage 5" text is at :311.
- Read `research/13` :80-90 and :198-210 and confirmed the cross-references cited at :177 and :295.
- Read all of `research/09` §4-§8, Gaps and Summary (:140-296), beyond the two edited lines. That is how I found finding 1.
- Ran a cross-file Grep for `t2.engine` and for turn-on or switch claims over the research files.
- Regression: `stat` of all research files, plus Grep or Read of each cycle-1 fix location.

1. Claims independently verified against source: about 20.
2. Files read: `src/superclaude/cli/reflect/runner.py`, `commands.py`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, research 02, 04, 05, 08, 09, 10, 11 and 13 (fix locations), the consolidated findings, the fix log, the cycle-1 content report and task file line 246.
3. Not a zero-finding report.
4. No web research was needed. Tavily was not used and there was no fallback.

**Confidence:** Verified: 3/3 (two edits plus the sweep) and 7/7 regression rows | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 1 | Glob: 0 | Bash: 4 (one batched read-only inspection script with 13 checks)

## Verdict

**Verdict: FAIL**. One IMPORTANT finding is open (finding 1): `research/09-consumer-plugpoints.md` :183 and :259 still treat turning the panel on as a `--t2-engine` or template switch for every consumer. That contradicts the corrected :161 and :177 for the blocking post gate. This was fix cycle 2 of 2, so under the 2-cycle cap the open finding goes to the user and no third fix cycle runs. The fix is two sentences and needs no new research. The 1 MINOR finding is a note only.

## QA Complete
