# QA Report — Research-Gate Qualitative Review (Partition 1 of 2)

**Report reviewed:** research files 01-06 under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/research/`
**Lens:** research-depth
**QA phase:** research-gate
**Date:** 2026-11-13
**Fix authorization:** false (report only)
**Assigned files:** `01-finding-contract.md`, `02-ledger-merge-verdict.md`, `03-clustering.md`, `04-panel-resolution-identity.md`, `05-blocking-calibration.md`, `06-input-contract-briefs.md`

[PARTITION NOTE: Cross-file checks limited to assigned subset (01-06). Full cross-file verification requires merging with partition 2 (07-12).]

---

## Findings

| # | Severity | File | Section | Finding | Proposed remedy |
|---|---|---|---|---|---|
| 1 | IMPORTANT | `05-blocking-calibration.md` | §5.3 ("Reading" paragraph), feeding §5 Key Takeaways and the §14 calibrator-weighted row | The per-finding calibration tally (142 findings, 16 blocking, mean 0.801 vs 0.661) is dated "runs recorded 2026-11-0x to 2026-11-11 (run ids)". That date is wrong. The dates in the run ids are the dates of the source workflow packages (for example `...-20261102-034618-shadow02`), not the run dates. The shadow runs were executed 2026-11-12 22:22 to 2026-11-13 02:42 (`panel/clusters.json` mtimes in all 14 `.dev/reflect/pre-*-shadow*/` dirs, checked this review). `06-input-contract-briefs.md` §2.4 gives the correct window (brief mtimes 2026-11-12 20:02 to 2026-11-13 02:35 UTC). The research notes require model-behaviour evidence to carry a date. The date matters here because the 2026-11-13 gateway routing served the "haiku" class with `gpt-6.1-sol` (04 §7.2), so it decides which calibrator models produced these numbers. | Replace the date with "shadow runs executed 2026-11-12 ~20:00 to 2026-11-13 ~02:45 UTC (artifact mtimes; run-id dates are source-package dates)". Add a note that calibrator models were not checked and that gateway class routing on that date was non-Anthropic for haiku (04 §7.2). |
| 2 | IMPORTANT | `05-blocking-calibration.md` | §14 options table, **Debate** row, "Evidence against" cell | The table lists "scope 04 reports 6.70% merged-verdict agreement with the cluster replay" as evidence against debate as the blocking decider. The source does not support that reading. `stage0a-report.md:295-297` defines agreement as the share of the debate's merged-verdict findings that fall inside a non-chained multi-reviewer `cluster_v2` cluster (24/358). It was computed on converted legacy cards with no calibration, and the report itself calls it "descriptive and seeds no gate". Low overlap between the two mechanisms says nothing about which one is right; if anything it counts equally against the cluster replay. The cell is the design input for the "who decides blocking" conflict, so this tilts that conflict against the reflect legacy path, which is authoritative today and avoids a contract bump. | Remove the 6.70% figure from "Evidence against" for Debate, or move it to a neutral note: "debate output and cluster_v2 overlap on 6.7% of merged findings (24/358, converted legacy cards, descriptive); this measures overlap between mechanisms, not the correctness of either". Keep "no ground-truth evaluation of debate blocking" as the real evidence gap. |
| 3 | MINOR | `05-blocking-calibration.md` | §5.3 and §14 calibrator-weighted "Evidence for" | All 16 reviewer-blocking findings come from only 3 of the 13 runs (shadow02: 4, shadow04: 4, shadow09: 8; grep of `"blocking": true` over `panel/cards/*.md` this review). So the 0.80 vs 0.66 gap may reflect per-run calibrator or model differences rather than blocking status. The file hedges against the missing ground truth but does not state this concentration. | Add "blocking findings are concentrated in 3 runs (02, 04, 09); the association is not controlled for run or calibrator model". |
| 4 | MINOR | `04-panel-resolution-identity.md` | §8 E2 best-panel bullets | The E2 panel statistics are quoted without replicate counts: "+0.83 control found (p 0.004 Welch, 0.048 permutation)", "haiku + 2x luna 1.2/8 real blocking", "~2.5/14 ceiling". The n per panel (4-6 replicates, 3 packages, 71 valid-era rows) appears only in 05 §11. The dates are present. | Add the replicate count per cited panel (from CR:303-337) and "3 packages, 71 valid-era rows" next to the §8 statistics. |
| 5 | MINOR | `01-finding-contract.md` (Gaps 1-2, §14.2) and `02-ledger-merge-verdict.md` (Gaps 8, §5.3 step 2) | Gaps and Questions | Both files leave two points [UNVERIFIED] that partition file 03 has since settled. (a) `cluster_cmd` does persist per-line errors (`cluster_cmd.py:161`, 03 §3). (b) `verify-citations` does check `line_end` against the file length (`verify_cmd.py:66-67`, confirmed by Read this review). Neither file is wrong, but synthesis could carry the stale "unverified" forward. [PARTITION NOTE: cross-file within 01-06 only.] | In synthesis, take the answers from 03 §3-§4; optionally annotate 01 and 02 gaps as "resolved by 03". |

## Per-file depth rating

Each file was read in full. The six questions in the prompt were applied to each: (1) actionable, (2) beyond surface reading, (3) design input concrete, (4) E1/E2/E3 choices distinguished, (5) numbers carry n and date, (6) proportionate.

| File | Rating | One-line reason |
|---|---|---|
| `01-finding-contract.md` | Deep | Rule-by-rule validator tables for v1 and v2, consumer effects traced (one bad v2 line drops the whole reviewer via `cluster.py:256-257`, confirmed), and a 7-shape superset table and a rejection matrix built by meaning. It contradicts the prompt's "card_convert counts truncation" premise with code (the `MINOR_WORDS` / `MAX_CLAIM` lines were confirmed). Design input (§17-18) offers concrete options. |
| `02-ledger-merge-verdict.md` | Deep | `merge_round` traced step by step. D2, D3, D4 and D16 are re-verified, including the finding that one reviewer can un-block a row (`ledger.py:216-218`, confirmed) and that clearing ignores `block_ok` (`ledger.py:254-258`, confirmed). The E2 audit-D numbers are re-derived, with the 3-vs-4 flip correction. The pinning tests are mapped, the three ledger philosophies are compared side by side, and the "partial runs, no success verdict" caveat is stated. |
| `03-clustering.md` | Deep | The two clusterers are compared step by step. D7 is confirmed by an executed probe. The "section always empty" over-merge path is explained mechanically. The 0.84/0.95 figures are correctly framed as AI-labelled, chain-excluded sample figures, with a sampler-design critique. Two upstream summaries are corrected (195-of-1398 denominator, `cluster_agreement` null vs 1.0). Q9 gives 8 concrete design inputs. |
| `04-panel-resolution-identity.md` | Deep | Resolver behaviour verified by actual `panel resolve` runs (D11 duplicate reproduced; gateway + reflect hard error). Dispatch collapse and the haiku-served-by-Sol mechanism are traced to env aliases. The E2 `expected_model` overwrite and two new runner defects are found. The identity-triple and distinctness-policy design input is concrete. Only a minor gap: replicate counts are missing on the E2 statistics (finding 4). |
| `05-blocking-calibration.md` | Deep, with 2 blocking accuracy and proportion defects | Strong code-level analysis: the contract halts on any Drift (`contract.py:380-381`, confirmed); the calibrator is a 6-dim troubleshoot agent with no rubric override; `unauthorized_deviation_present` has no producer; Rule A and Rule B conflict. There is a per-finding rule derivation (§13) and a 5-option table. The 16-blocking and 42-MAJOR counts were confirmed by grep. Blocking defects: the shadow evidence is misdated (finding 1), and a descriptive overlap statistic is used as evidence against debate (finding 2). |
| `06-input-contract-briefs.md` | Deep | D8 is confirmed in the prompt file: there are only 5 placeholders, `{{SOURCE}}` is absent, and the grep was re-run this review. All 45 recorded briefs were audited (23 break the C7 shape; 0 carry the verbatim shadow line). The one-line-`source.md` mechanism behind W-3 is shown. Test-pin compatibility for a `{{SOURCE}}` change is worked out line by line. The 6-consumer input matrix and the code-rendered template are concrete design input. |

## Verdict

**Verdict: FAIL**: 2 blocking findings (IMPORTANT #1 and #2, both in `05-blocking-calibration.md`), plus 3 MINOR notes. Files 01, 02, 03, 04 and 06 have no blocking finding. Both blocking fixes are local edits to 05 (§5.3 date line; §14 Debate row).

---

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for the structural re-check):**
- No `## Inherited Structural Verdict` block was in the spawn prompt. The sibling rf-qa evidence reports (`qa/qa-research-evidence-report-1.md`) were not relied on; no structural reliance.

**(b) Independent semantic checks (≥1 required, INV-019):**
- 05 §5.3 dating: verified by `ls -l` on 15 `.dev/reflect/*shadow*` dirs and 14 `panel/clusters.json` mtimes (2026-11-12T22:22 to 2026-11-13T02:42). This contradicts "2026-11-0x to 2026-11-11" → finding 1.
- 05 §14 Debate row: Read `stage0a-report.md:292-299`; the agreement formula measures overlap, not correctness → finding 2.
- 05 §5.3 counts: Grep `"blocking": true` = 16 in 9 card files across 3 runs; Grep `"severity": "MAJOR"` = 42. The counts match the file; the run concentration → finding 3.
- 01/05 card_convert severity claims: Read `card_convert.py:71-86` (`important`/`medium` in `MINOR_WORDS`; `MAX_CLAIM = 300`; no counter).
- 01/02/03 v2 whole-reviewer drop: Read `cluster.py:250-259` (`if not r["valid"]: continue`).
- 02 D2/D4: Read `ledger.py:210-219` (un-block by current round) and `:250-258` (clearing ignores `block_ok`).
- 04 D11: Read `panel.py:536-544` (`if hard: raise` else `pool = candidates`).
- 05 drift halts: Read `contract.py:361-382`.
- 05 Rule B: Read `findings_v2.py:155-164`.
- 03/05 verify-citations range check: Read `verify_cmd.py:44-73` (out-of-range at :66-67) → finding 5.
- 06 D8: Grep `\{\{[A-Z]+\}\}` in `document_review_loop_prompts.md` gives only CANDIDATE, BASELINE, PRIOR, N and IDS.

**Self-audit answers:**
1. Claims independently verified against source: 14, from the tool calls above. That covers 12 code or artifact lines and counts, plus 2 cross-file reconciliations.
2. Files read: the six assigned research files in full, `research/research-notes.md`, `card_convert.py`, `cluster.py`, `contract.py`, `verify_cmd.py`, `ledger.py`, `panel.py`, `findings_v2.py`, `stage0a-report.md`, the shadow run dirs and cards (by ls and grep), and `document_review_loop_prompts.md` (by grep).
3. Not a zero-issue report: 2 blocking and 3 minor findings, each with tool evidence.
4. No web research was needed: the lens is local research-depth. Tavily was not used, so there was no fallback.

## Confidence Gate

- **Confidence:** Verified: 6/6 per-file checks (36 question-cells) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 3 | Glob: 1 | Bash: 2
- Unchecked items: none.
- Unverifiable items: none. The E2 figures (`COMBO-REPORT.md`, audit-D) were judged on whether the research files hedge and cite them; `git show` was not re-run on E2 in this review. The E2 numbers themselves are checked by the partition rf-qa evidence agents.
- Residual risk: line-level spot checks covered about 12 of several hundred citations in 01-06. A wrong line number elsewhere would be an rf-qa (evidence) concern and does not affect depth.

## QA Complete

