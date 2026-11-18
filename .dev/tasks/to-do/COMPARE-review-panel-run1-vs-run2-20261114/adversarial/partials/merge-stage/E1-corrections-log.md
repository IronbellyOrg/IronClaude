# E1 Corrections Log (merge executor E1 of 4, step 5)

- Scope: M-01 (V2:5 only; title V2:1 left for the other executor), M-12, M-13, M-24 items 1-14 of `adversarial/refactor-plan.md`.
- Input: `adversarial/variant-2-original.md` (5,098 lines; byte-unchanged, asserted by the script).
- Output: `adversarial/partials/merge-stage/base-corrected.md` (5,098 lines, same order; 78 lines changed, 80 edits).
- Script: `adversarial/partials/merge-scripts/e1_base_corrections.py` (exact-text replacement addressed by ORIGINAL line number; every old text asserted to occur exactly once in its line; one provenance comment appended at the end of each modified line). Machine log of every edit with full before/after text: `adversarial/partials/merge-stage/e1-edits.json`.
- All line numbers below are ORIGINAL base lines (`V2:n`). Line count is unchanged, so they are also the lines in `base-corrected.md`.
- Recurring inserted texts (exact text in the script constants): KE (item 1 rewrite, plan wording), KN (item 1 short bracketed note), WD (item 2 marker, plan wording), CAL / CALN (item 3), PR47 = `[corrected from 50: \`tests/pr_submit\` has 47 test files, 49 tracked \`.py\`]`, RO_FULL / RO_SHORT (item 5), K6, K7, K10, K11, K12, K13, K14 (items 6, 7, 10, 11, 12, 13, 14; plan wording).

## Read-only checks run by E1 (all read-only, logged with result)

| # | Command or file | Result |
|---|---|---|
| E1-1 | Read `src/superclaude/cli/review/findings.py:100-107, 184-193, 344-350` | `:104` `_check_flat(obj.get("anchor"), "anchor", 12, 200)`; `:188-192` `_check_finding` error -> `ok=False`, `continue`; `:349` `locate(text, finding["anchor"])` |
| E1-2 | `grep -o '[56]-dimension'` in `agents/confidence-calibrator.md`, `skills/sc-reflect-protocol/SKILL.md`; Read calibrator `:61` | `:3` 6-dimension; `:61` "the 6 dimensions"; SKILL `:1262`, `:1835` 5-dimension |
| E1-3 | `ls tests/pr_submit/test_*.py \| wc -l`; `git ls-files 'tests/pr_submit/*.py' \| wc -l`; `git ls-files tests/pr_submit \| wc -l` | 47; 49; 91 (fixtures included) |
| E1-4 | `sed -n` `pipeline/process.py:145-154`, `reflect/runner.py:566`, `reflect/ensemble.py:548`; `claude --version`; `claude --help \| grep` | `reviewer_profile` drops the permission flag and `--tools default`; `reviewer_profile=True` at both call sites; 2.1.325; `--restricted` help mentions `--strict-mcp-config to skip MCP servers` |
| E1-5 | `sed -n '363p;833,834p' reflect/ensemble.py` | `:363` comment `t2_fallback=None` default; `:833-834` key added only when not None |
| E1-6 | `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` (lines, files, SKILL.md split); `grep -c` / `grep -o` `superclaude review` in reflect `SKILL.md` | 52 lines, 11 files, 44 lines in 8 SKILL.md; 5 lines, 7 occurrences |
| E1-7 | `git rev-parse --short=9 HEAD origin/master`; merge-base; `rev-list --count`; `git log -1 --format=%ci origin/master`; `rev-list --count 6c09843..e2f2ac268`; `git ls-files` for the two pin files | `ad8f57560`, `d4d1662a8`; merge-base `d2d8a2d16`; 3 and 5 commits past it; 2026-11-14 12:42; 7; `tests/skills/test_worker_contract.py`, `src/superclaude/output-styles/pragmatic.md` |
| E1-8 | `ls .dev/reflect/*shadow09*`; `grep cluster_agreement` in its `panel/clusters*.json` | `clusters.json` and `clusters_kept.json` hold 0.9328358208955224 |
| E1-9 | `git log --format='%h %s' -- src/superclaude/cli/reflect/ensemble.py` PR numbers; `git diff --stat origin/master HEAD -- ensemble.py` | PRs #199, #203, #213, #214, #220, #323, #329; no diff |
| E1-10 | `git cat-file -s ad8f57560:<synth-08 path>`; `git log -1 -- <path>`; `git show --stat ad8f57560 -- <path>` | 2,024,775 bytes; last commit `ad8f57560`; added there (6,127 insertions) |
| E1-11 | `sed -n 76p` run 2 `qa/qa-consolidated-findings-phase6.md` | P6-054: 2606.19544 withdrawn by arXiv Admin 2026-11-03; 2510.27106 "Accepted at EMNLP 2025" |

## M-01 (V2:5 research-files line)

- Pattern: line 5 (`**Research files:**`). Hits: V2:5.
- V2:5 edited. Before: `**Research files:** 24 codebase + 4 web research (+ 12 scope slices)`. After: `**Research files:** Run 2: 24 codebase + 4 web research files (12 scope slices listed, not opened, V2:108). Run 1: 13 codebase + 4 web research files, plus 6 scope slices S00-S05 used as evidence (V1:113).` (plan wording; the `**Research files:**` label kept). V2:1 (title) not touched.

## M-12 (Section 8 heading and lead)

- Hits: V2:4234 (heading), V2:4236 (lead); V2:4235, 4237 are blank and unchanged.
- V2:4234 edited: `## 8. Value Inventory and Inputs for a Later Plan` -> `## 8. Value Inventory, Migration and Value-Capture Content, and Inputs for a Later Plan`.
- V2:4236 edited: lead now keeps run 2's 8.1/8.2 description, states "For what this document adds there is no roadmap, no branch plan, no PR plan, no risk register, no estimate and no schedule", and states that 8.3-8.8 carry run 1's value-capture and migration content as content (inventory rows, steps with status against the adopted design, gates, risk inputs), which orders no work and is not a plan.
- WARNING for M-26 (ToC executor): per the instruction, the provenance comment is at the END of the heading line V2:4234. The ToC script must strip `<!-- ... -->` from heading text before building entries and anchors.

## M-13 (8.1 value-inventory pointer)

- Pattern: `synth-08-value-inventory`. Hits: V2:4240 (carrying note), 4242 (source-note label), 4280 (8.1.2 pointer), 4922, 4931 (Section 10), 5074 (Appendix A).
- V2:4280 edited (the pointer in 8.1): after "...in **Appendix A**, which is the file `<path>` (2,024,775 bytes, 6,127 lines, unchanged)." the sentence "Appendix A is part of the report package." is replaced by the plan text: "The 5,950 rows live in `<path>`, committed at `ad8f57560`; the pointer is `ad8f57560:<path>`, which still resolves if the task folder moves (R25-INV-023). Run 2's Q-35 asked whether its `.dev/tasks` output may be committed; it was committed at `ad8f57560`; whether it was pushed is not checked here." The plan's `<that path>` is written out as the full path so the pointer resolves. Pointer to Appendix A kept. Check E1-10.
- Not edited: V2:4240, 4242 (describe the carrying rule, not the pointer), 4922, 4931 (Section 10), 5074 (Appendix A; outside 8.1).

## M-24 item 1 (KeyError path)

- Pattern: `grep -n KeyError`; extra pattern for the same claim without the word: `crash|DR-113|P-a` near the ledger path.
- Hits (`KeyError`): 545, 940, 1177, 1236, 1334, 1437, 2177, 3329, 3411, 3487, 3637, 3666, 3882, 4312, 4508, 4677. Extra-pattern hits read: 508, 531, 580, 584, 716, 870, 874, 998, 1134, 1236, 1277, 1376, 2188, 2226, 2235, 2236, 2256, 2263, 3636, 3771, 3793, 3939, 4193, 5085.

| Line | Action | Before (short) | After (short) |
|---|---|---|---|
| 545 | no change | probe P-a is a direct `annotate()` call; mechanism refinement already stated | (plan: keep) |
| 940 | edited | "raises `KeyError: 'anchor'` in v1 `annotate` ..., so it cannot enter the v1 ledger path" | "cannot enter the v1 ledger path: " + KE + " (probe P-a is a direct `annotate` call)" |
| 1177 | edited (note appended, criterion kept) | SC-01 criterion | + "[mechanism note: today such a line never reaches `annotate` ...]" |
| 1236 | edited | "raises `KeyError` in `findings.annotate` ..., which `ledger.merge_round` calls" | KE |
| 1334 | edited | "`ledger.merge_round` -> `annotate` raises `KeyError`" | "but on the ledger path " + KE |
| 1437 | edited (note) | "(`annotate` `KeyError`)" | + KN |
| 2177 | edited | "crashes the v1 ledger path (`KeyError` ...)" | KE |
| 2226 | edited, EXTRA SITE (note) | "a citation-only finding crashes the v1 ledger path (R01 P-a)" | + KN |
| 3329 | edited | "raises `KeyError` in `annotate`, so v2 findings cannot enter ..." | KE + "; so v2 findings cannot enter ..." |
| 3411 | edited | "raises `KeyError` in `annotate`, so location type blocks ..." | KE + "; so location type blocks ..." |
| 3487 | edited | "raises `KeyError` in `annotate`;" | KE |
| 3636 | edited, EXTRA SITE (note) | "a citation-only finding crashes the v1 ledger path," | + KN |
| 3637 | edited | "crashes the v1 ledger path with `KeyError 'anchor'` (..., REPRODUCED)" | KE + "(..., REPRODUCED as a direct `annotate` call)" |
| 3666 | edited | "raises `KeyError` in `annotate` (r01 §3 P-a)" | KE + " (r01 §3 P-a)" |
| 3882 | edited | "raises `KeyError 'anchor'` in the ledger path" | KE |
| 4312 | no change | inventory row quoted as context | (plan: keep) |
| 4508 | edited | "`merge_round` calls `annotate` on every parsed finding ..., so the finding raises `KeyError`" | "but " + KE + " (`annotate` does `locate(...)` with no default)" |
| 4677 | edited (note) | OQ14 "`KeyError 'anchor'` on the ledger path" | + KN |
| 508, 531, 584, 716, 870, 874, 998, 1134, 2235, 2236, 2263, 3771, 3793, 3939 | no change | name probe P-a / DR-113 or state "`annotate` needs `anchor`"; true as written | - |
| 2188 | no change | "`merge_round` calls `annotate` on every parsed finding"; true (parsed = accepted by the v1 parser) | - |
| 2256 | no change | "v2 citation-only finding crashes v1 `annotate`"; true for `annotate` itself | - |
| 5085 | no change | Appendix B already carries the Gate 1 mechanism refinement | - |
| 580, 1277, 1376, 4193 | no change | "crash" in another sense (exit test, verifier) | - |

Plan wording differences: none for KE (plan text verbatim, tag `[CODE-VERIFIED by the compare orchestrator at HEAD ad8f57560]`). Basis: diff-analysis "Orchestrator Verification" row X-020/X-049/X-053; fault-finder row 11; check E1-1.

## M-24 item 2 (withdrawn paper arXiv 2606.19544)

- Pattern: `2606\.19544|2510\.27106|33-41|33 to 41`; extra pattern `Reliability without Validity|541,000|21 judges|14 positions|[Vv]erbosity|AE-1`.
- Hits: 1647, 1648, 2829; extra-pattern hits 1559, 1561, 1576, 1650, 1655, 1681, 2044, 2072, 2078, 4535; plus plan-listed 2049.

| Line | Action | Detail |
|---|---|---|
| 1647 | edited | WD appended after the "Reliability without Validity" sentence ("... in contrast to the 2023 literature.") |
| 1648 | edited (2 edits) | WD after the 2606.19544 URL; tier correction after "(peer review not confirmed; 2606.19544 carries a mid-2026 id)": "[corrected: arXiv lists 2510.27106 as accepted at EMNLP 2025 (run 2 QA P6-054, `qa-consolidated-findings-phase6.md:76`); 2606.19544 is withdrawn]" (check E1-11) |
| 1650 | no change | uses no figure of 2606.19544; chance-corrected agreement rests on the blogs and 2510.27106; "stability vs correctness" is takeaway 6's point, which the plan says 2510.27106 also supports |
| 1655 | edited | WD after "(AE-1 found it much reduced)" (the verbosity rationale rests on 2606.19544) |
| 2044 | edited | WD after "Verbosity bias appears much smaller in recent judges." |
| 2049 | no change | takeaway 6 is also supported by 2510.27106 (plan) |
| 2072 | edited | status cell: "Included (AE-1's figures from arXiv 2606.19544 are marked " + WD + ")" |
| 2078 | edited | same note on "Included as source option" |
| 2829 | edited | WD after the 33-41 points sentence "(W01 AE-1; external, transfer unverified)." |
| 1559, 1561, 1576, 1681 | no change | verbosity bias from MT-Bench, CALM, CARE (other sources) |
| 4535 | no change | `AE-1` there is a different id (acceptance condition, ground-truth registry) |

## M-24 item 3 (calibrator 6 vs 5 dimensions)

- Pattern: `confidence-calibrator|5-dimension|6-dimension|calibrator.*dimension`. Hits: 177, 635, 640, 891, 1033, 2701, 3323, 3474, 4763.

| Line | Action | Detail |
|---|---|---|
| 891 | edited | "reflect's 5 [UNVERIFIED]" -> "reflect's 5 " + CAL (`[CODE-VERIFIED: confidence-calibrator.md:3,61 ... SKILL.md:1262,1835 ...; diff-analysis X-030]`); the other [UNVERIFIED] tags on the line (DO3, E3i) are untouched |
| 3323 | edited (narrower than the plan) | the row's `[UNVERIFIED]` covers both the vocabulary claim and the calibrator claim; changing the tag wholesale would also certify the vocabulary claim, which no check covers. So the tag is kept and "; the calibrator part is now " + CAL is appended. |
| 1033 | edited | CALN appended after "(6 against 5 dimensions)" |
| 3474 | edited | CALN appended after "5- versus 6-dimension calibrator" |
| 177, 635, 640, 2701, 4763 | no change | name the agent, state no dimension count |

## M-24 item 4 (`tests/pr_submit` test-file count)

- Pattern: `grep -nE '\b50\b.{0,40}(test|tests/pr_submit)'`; extra `pr_submit.{0,60}\b50\b|\b50 files`.
- Hits: 710, 1202, 1335, 2973, 3357, 3496, 3735, 3797, 3804, 4436, 4479, 4593.

| Line | Action | Before -> after |
|---|---|---|
| 710 | edited | "50 `tests/pr_submit/` files" -> "47 `tests/pr_submit/` test files " + PR47 |
| 1202 | edited | "50 `tests/pr_submit/` files green" -> "47 ... test files " + PR47 + " green" |
| 1335 | edited | "has 50 test files" -> "has 47 test files " + PR47 |
| 2973 | edited | "50 test files pin" -> "47 test files " + PR47 + " pin" |
| 3357 | edited | "the 50 `tests/pr_submit` files" -> "the 47 ... test files " + PR47 |
| 3496 | edited | same as 3357 |
| 3735 | edited | "50 test files under" -> "47 test files " + PR47 + " under" |
| 3797 | edited, EXTRA SITE (DEVIATES from the plan's example) | "(50 files, 47 `test_*.py`)" kept and annotated "[corrected: 49 tracked `.py` files, 47 of them `test_*.py`; 91 tracked files including fixtures; no count gives 50]". The plan names V2:3797 as an extra locator hit not to edit (it carries U-122's 47), but its "50 files" is wrong under every unit checked (E1-3); the 47 is kept. |
| 3804 | edited | "50 test files under" -> "47 test files " + PR47 + " under" |
| 4436 | no change | `:50-62` is a line range, not a count (plan) |
| 4479 | edited | "(50 test files plus `conftest.py` and `__init__.py`)" -> "(47 test files " + PR47 + " plus ...)" (47 + 2 = 49 `.py`, consistent) |
| 4593 | edited | "(50 test files)" -> "(47 test files " + PR47 + ")" |

## M-24 item 5 (read-only mechanism)

- Pattern: `allowedTools|--tools|--restricted|strict-mcp-config`. Hits: 284, 884, 1725, 1728, 1732, 1787, 1789, 1792, 2054, 2088, 2493, 3123, 3517, 3640, 3658, 4085; plan range V2:1718-1728 read in full.
- Finding: the base never says `--allowedTools` restricts tools (it says the opposite, 1725, 1728, 2054). Its error is incompleteness: `--tools` / `--restricted` are presented as giving a read-only reviewer while MCP servers stay loaded. So the plan's "add" part is applied; no `--allowedTools` text needed replacing.

| Line | Action | Detail |
|---|---|---|
| 1728 | edited | RO_FULL appended after "not `--allowedTools` (a common mistake)." |
| 1792 | edited | RO_SHORT after "(which applies only to Agent-tool subagents)." |
| 2054 | edited | RO_SHORT after "covers only the Agent path." |
| 3517 | edited | RO_SHORT after "(no `--restricted` run on a gateway id exists)" |
| 3640 | edited | RO_FULL after "the CLI flags `--tools` and `--restricted` are named in W02 sections 4, 10)." |
| 3658 | edited | RO_SHORT after "(no `--restricted` run on a gateway id exists)" |
| 4085 | edited | RO_SHORT after "confines file tools to the working directories" |
| 1718, 1725 | no change | accurate statements of the official docs (`system/init` event; `--allowedTools` only pre-approves); the 5.2.4 note sits at 1728 in the same subsection |
| 1732 | no change | subagent frontmatter facts, accurate |
| 1787, 1789 | no change | heading; accurate `--restricted` description (the MCP point is added at 1792) |
| 284, 884 | no change | E2's `run-reviewer.sh` flags, accurate |
| 2088, 3123 | no change | coverage labels only |
| 2493 | no change | lists flags as reusable, makes no read-only claim |

RO_FULL carries: `--strict-mcp-config` also needed; `--restricted` refuses `bypassPermissions` and confines file tools; G2 reads the MCP list from `system/init`; existing restricted child `pipeline/process.py:145-154` `reviewer_profile=True` used at `runner.py:566`, `ensemble.py:548`; reuse-or-replace question; R25-INV-006, R25-INV-007; `claude --help` 2.1.325 (fault-finder row 27). Check E1-4.

## M-24 item 6 (engine-A contract keys)

- Pattern: `\b3[23] (top-level )?keys|\b3[23]-key|\b1[01] (keys )?outside|\b1[01] keys`. Hits: 179, 892, 1255, 1430, 2507, 2703, 4503.
- K6 appended (plan wording) after the "89 of (the) 110 stable names absent" clause at 179, 892, 1255, 1430, 2703; after "10 keys outside the frozen lists" at 2507 (EXTRA SITE); after "lacks 89 of the 110 stable names" at 4503 (EXTRA SITE). No count was rewritten: 32/10 is correct for the default run. Check E1-5.

## M-24 item 7 (rf-* census)

- Pattern: `52|44|rf-\*|call site|spawn` on the listed lines; extra `\b43 call|in 11 files|rf-\* (spawn|call)`. Hits: 683, 1341, 2953, 3387, 3736, 3820, 3892, 4602, 4745 (and `18 ... in 11 files` T2bModel01 lines 645, 883, 1011, 1064, 1267, 3069, 3405, 3895, 3942, unrelated).
- K7 appended at 683, 1341, 2953, 3736, 3820, 3892, 4602 (planned) and 3387 (DATA-13 row, EXTRA SITE: same 44-structured-lines claim as 3892). No change at 4745 (mentions the census, states no count) or the T2bModel01 lines. No count was rewritten (run 2's 44/52 are right). Check E1-6.

## M-24 item 8 (`superclaude review` mentions)

- Pattern: ``grep -nF 'SKILL.md` (6)'``; extra `\(6\)` (enumeration markers at 203, 1273, 1280, 1349, 3787, 4145, 4823, unrelated). Hit: 1331.
- 1331 edited: "`sc-reflect-protocol/SKILL.md` (6)" -> "`sc-reflect-protocol/SKILL.md` (5 lines, 7 occurrences [corrected from "(6)"; `grep -c` and `grep -o`])". Check E1-6.

## M-24 item 9 (baseline note)

- Site: Baseline paragraph V2:108 (the plan names no line; the "Baseline" sentence is the natural host). V2:104-123 read in full.
- 108 edited: appended "[Compare-merge baseline note: `origin/master` `d4d1662a8` (2026-11-14) is 3 commits past merge-base `d2d8a2d16`; HEAD `ad8f57560` is 5 commits past it; line numbers in this document are valid at HEAD; on `origin/master` the pins that C14 and C26 cite sit at `tests/skills/test_worker_contract.py:787, :796, :1872` and `src/superclaude/output-styles/pragmatic.md:229, :235` (fault-finder row 3). `e2f2ac268` (E2) is 7 commits after `6c09843` and was not read by either report.]" The plan's `tests/.../` is written out (check E1-7). The original sentence "Code at HEAD `50d4d2b9d`" is kept (code is identical, X-063); M-02's addendum (other executor) may restate (e)/(f).

## M-24 item 10 (`findings_block_compliance_rate` 0.704)

- Pattern: `0\.704`. Hits: 215, 1282, 2370.
- 215 edited: K10 after "mean 0.704 over 9 runs (pilot)". 1282 and 2370 edited as EXTRA SITES (both call the 0.704 mean first-parse / first-pass): K10 appended. Basis: diff-analysis X-027.

## M-24 item 11 (`cluster_agreement`)

- Pattern: `cluster_agreement`. Hits: 216, 874 (twice), 881, 1041, 1283, 1292, 1368, 2192, 3945, 4544, 4752.
- 216 edited: "; " + K11 before the closing cell bar. 874 edited: "; " + K11 after "1.000 over 9 runs [CODE-VERIFIED by execution, R06 section 0]".
- No change: 881, 1041, 2192 (definition/registry mentions); 1283, 1292, 4544 (state the exit script's 9-run 1.000 correctly; the shadow09 note is carried at 216/874); 1368 (shadow02 null); 3945, 4752 (summary / open question). Check E1-8.

## M-24 item 12 (`ensemble.py` provenance)

- Sites: V2:154-171 (2.1 diagram block) and V2:845 (2.9.0 effort table). Both read.
- 154 edited: after the bold lead "**Two Tier 2 engines that share only `contract.py`.**" appended " Provenance: " + K12 + "." (the fenced diagram 156-171 is not touched).
- 845 edited: E1 row, after "behind `superclaude reflect run`)" inserted "; " + K12. Two sites, one sentence each (2.1 and 2.9.0 both attribute engine A to E1). Check E1-9 (the git log also lists #199, #203, #323; the note keeps run 1's four numbers).

## M-24 item 13 (1,398 unit)

- Pattern: `1,?398|\b195\b`. Hits: 874, 1027, 1368, 3743 (other `195` hits at 2248, 3228, 3279, 3340, 3358, 3359, 3361, 3465, 4403, 4760 are line cites or GQ ids).
- Edited: 874 and 1027 "195 of 1,398 rows chained" -> K13; 1368 "195 of 1,398 multi-member rows are chains" -> K13; 3743 "195 of 1,398 multi-member rows chained" -> K13. The surrounding tags (`[UNVERIFIED]`, `[UNVERIFIED here, recomputed count 195]`) are kept. Basis: diff-analysis X-021.

## M-24 item 14 (fail-open wording)

- Pattern: `fail-open|fail-closed|refus|dropped` on V2:3516, 3638; extra `fail-open|closes the fail|fail-closed refusal` over the file (895, 983, 1306, 1344, 2189, 2406, 2459, 2884, 3011, 3305, 3498, 4707: other fail-open paths, not the C-06 refusal).
- 3516 edited: K14 after "a dropped-blocking refusal with an acknowledgement exit". 3638 edited: K14 after "a fail-closed refusal with an acknowledgement exit when a blocking line was dropped".
- Wording: the plan's quoted text is "this narrows, not closes, the fail-open path" but the plan also says "Do not introduce the word 'closes'". K14 uses "this narrows the fail-open path but does not close it", which keeps the meaning and avoids the word. Verified: 0 occurrences of `closes` in all changed lines.

## Summary

| item | sites edited | sites not edited | extra sites |
|---|---|---|---|
| M-01 | 5 | - | - |
| M-12 | 4234, 4236 | 4235, 4237 (blank) | - |
| M-13 | 4280 | 4240, 4242, 4922, 4931, 5074 | - |
| M-24 item 1 | 940, 1177, 1236, 1334, 1437, 2177, 3329, 3411, 3487, 3637, 3666, 3882, 4508, 4677 | 545, 4312 (plan keep); 2188, 2256, 5085 and the P-a/DR-113 mentions (true as written) | 2226, 3636 |
| M-24 item 2 | 1647, 1648 (2 edits), 1655, 2044, 2072, 2078, 2829 | 1650, 2049 (do not rest on 2606.19544 alone); 1559, 1561, 1576, 1681, 4535 | - |
| M-24 item 3 | 891, 3323 (narrower: calibrator part only), 1033, 3474 | 177, 635, 640, 2701, 4763 | - |
| M-24 item 4 | 710, 1202, 1335, 2973, 3357, 3496, 3735, 3804, 4479, 4593 | 4436 (line range) | 3797 (plan said not to edit; "50 files" is wrong) |
| M-24 item 5 | 1728, 1792, 2054, 3517, 3640, 3658, 4085 | 284, 884, 1718, 1725, 1732, 1787, 1789, 2088, 2493, 3123 | - |
| M-24 item 6 | 179, 892, 1255, 1430, 2703 | - | 2507, 4503 |
| M-24 item 7 | 683, 1341, 2953, 3736, 3820, 3892, 4602 | 4745 | 3387 |
| M-24 item 8 | 1331 | enumeration `(6)` lines | - |
| M-24 item 9 | 108 | - | - |
| M-24 item 10 | 215 | - | 1282, 2370 |
| M-24 item 11 | 216, 874 | 881, 1041, 1283, 1292, 1368, 2192, 3945, 4544, 4752 | - |
| M-24 item 12 | 154, 845 | 156-171 (fenced diagram) | - |
| M-24 item 13 | 874, 1027, 1368, 3743 | other `195` hits | - |
| M-24 item 14 | 3516, 3638 | other fail-open paths | - |

Totals: 80 edits on 78 lines (line 874 carries items 11 and 13; line 1648 carries two item-2 edits).

## Verification

Python line diff (`difflib.SequenceMatcher`, plus a direct per-line compare) of `variant-2-original.md` against `base-corrected.md`, run after the final script run:

- Line counts: 5,098 and 5,098; the only opcodes are `replace` (no insertions or deletions; order unchanged).
- Changed lines: 78; changed lines without a trailing `<!-- Source: Base (original, modified) — ... -->`: 0; the script also asserts that the changed-line set equals the tagged-line set and that the base file bytes are unchanged.
- Occurrences of the word `closes` in changed lines: 0.
- Residual `\b50\b.{0,40}(test|tests/pr_submit)` lines without a correction: 4436 only (a line range, by design).
- Residual `KeyError` lines without a provenance comment: 545, 4312 (plan: keep).
- Lines containing `2606.19544` without the `SOURCE WITHDRAWN` marker: none.
- Note for the next executors: the provenance comment on heading line 4234 must be stripped by the ToC script (M-26), and Appendix E (M-29) can take before/after texts from `e1-edits.json`.
