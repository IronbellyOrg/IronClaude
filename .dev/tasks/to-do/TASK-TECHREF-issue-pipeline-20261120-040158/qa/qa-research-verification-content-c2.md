# QA Report - Gate 1 research-gate fix-cycle verification (qualitative), cycle 2

**Topic:** IronClaude issue-to-work pipeline technical reference, research gap-fill verification
**Date:** 2026-11-20
**Phase:** fix-cycle (research-depth lens, qualitative)
**Fix cycle:** 2
**Status:** In Progress
**Fix authorization:** false (report only)

---

## Previously BLOCKING items (cycle 2 list: one item)

| ID | Research location | FILLED/NOT-FILLED | Justification |
|---|---|---|---|
| N-1 | research/04-claim-flow-and-orca-worktree.md, "Gap-fill c1 F-2" row F-2.1 for `skills/test_model_alias_policy.py`, item (5) (line 554); erratum "Gap-fill c2 N-1" at lines 601-637 | FILLED | The erratum (lines 605-612) says item (5) must read "The other seven tests" and shows the arithmetic: 11 test functions, items (1) to (4) cover four (:83, :104, :191, :247), 11 - 4 = 7, and the seven are the ones the row lists (:139, :164, :176, :183, :199, :217, :231). I read the snapshot file `/home/coder/.cache/ic-snap-20261120/master/tests/skills/test_model_alias_policy.py` in full (249 lines): its `def test_` lines are exactly 83, 104, 139, 164, 176, 183, 191, 199, 217, 231, 247 (decorator at 246 for the parametrized one). Seven is right and "eight" is wrong. The fix is not only a one-word patch: the erratum re-derives every count in both F-2.1 rows and records five wordings that were looser than the test (N-1.3), all of which I re-checked and found true. |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over/new | previously-rated-PASS yes/no |
|---|---|---|---|---|---|
| (none) | | | | | |

For the record, N-1 itself: it was new at cycle 1 (introduced by the F-2 gap-fill text, not in the cycle-1 consolidated list) and was found by the structural verification c1 report. The cycle-1 content verification (qa-research-verification-content-c1.md, F-2 row: FILLED, "Counts and case arithmetic re-checked") rated the F-2 area PASS and did not catch it, so previously-rated-PASS = yes for this lens. It is carried over into cycle 2 and is now FILLED.

## Checks performed

1. Read the cycle-2 consolidated findings (`qa-research-consolidated-findings-c2.md`): one BLOCKING finding, N-1, 0 synthetic. Read BUILD-REQUEST.md (goal, content requirements a-g, the test-pin matrix requirement (d)).
2. Read research/04 lines 540-639 in full (F-2.1 rows, F-2.2 to F-2.4, and the new "Gap-fill c2 N-1" erratum). Confirmed the erratum is append-only (the old row at line 554 still says "eight"; the erratum says it supersedes that word) and that the erratum states the correct word, the evidence list, and the arithmetic.
3. Test-function count of `test_model_alias_policy.py`: Read the whole file (249 lines) and `grep -c '^\s*def test_'` = 11. Names and lines match erratum line 609 one for one, including `test_issue_worker_allow_list_entries_exist` at :247 with decorator :246. The `@pytest.mark.parametrize("pin", sorted(ISSUE_WORKER_PINS))` at :246 runs over three keys, so 10 + 3 = 13 collected cases. Lines 249 (`wc -l`). Result: correct.
4. Item (1) to (4) vs (5) partition: items (1) to (4) are :83, :104, :191, :247 and the rest are :139, :164, :176, :183, :199, :217, :231 (seven). Verified from the file text.
5. `test_clickup_claim.py` counts re-derived: `wc -l` = 569; `grep -c 'def test_'` = 29; one class (`FakeClickUp` :101, a fake, not a test class); five `parametrize` decorators at :336 (2 values), :389 (5), :405 (2), :459 (2), :514 (6 argument lists, read at :517-536). 24 plain functions + 17 cases = 41. Erratum figures right. The ten "Key test names" lines also match the `def` lines from the grep (:277, :298, :311, :343, :372, :406, :500, :539, :548, :561).
6. N-1.3 looser-wording claims re-checked in the snapshot: (a) `test_only_match_on_the_last_allowed_page` :475 has three pages and the match on page index 2; cap "3" gives pages seen [0, 1, 2] and `PAGE_CAP`, cap "4" gives [0, 1, 2, 3] and `assigned` (:459-482): erratum right. (b) The token assertions are `TOKEN not in out/err` (:548-558) plus the PUT url/body asserts; no GET-URL token assertion in the lines I read (:370-570): erratum right. (c) `TEXT_SUFFIXES` at :51 and used at :112: right. (d) `test_mapping_document_states_the_exports_and_tiers_exist` asserts `{"tier1a","tier1b","tier2"} <= set(models["tiers"])` (:243), and `ccsession-models.json` has `tier2b` at line 104, so the test does not check it: right. (e) the frontmatter globs at :86-88 are `glob("*.md")` and `glob("*/SKILL.md")`, not recursive: right.
7. Code-side spot check: `clickup_claim.py` lives at `src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py`; the PUT with `{"assignees": {"add": [user_id]}}` is at lines 232-237 (the `request("PUT", ...)` call; the research row quotes it with `quote(...)` where the code has `urllib.parse.quote(..., safe='')`, a paraphrase, MINOR). `ClickUpError` catch follows at :239-240 as stated.
8. Pins and allow-list claims in the row: `ISSUE_WORKER_PINS` entries at :30-32 (t3 `claude-gw-tier2b`, t2 `claude-gw-tier2`, t1 `claude-gw-tier1b`); `TIER_TEXT_ALLOWED` at :38-44 includes `cli/review/data/` at :43 and that directory exists in the snapshot (review-default.json, review-panel.classic.json, review-panel.live7.json); the three agent files have `model:` on line 6 with the same values. `chains.md` lines 12 and 13 are the only two `/sc:brainstorm` lines and neither has `--models`.
9. Regression check across research files: grep for `test_model_alias_policy` and for "eight", "11 tests", "13 cases" in research/01 to 06: the only mentions are in research/04 (rows, F-2.2 to F-2.4, the erratum) and one in research/05:570 (ccsession-only-as-model-tier-data list), which does not give a count. No contradiction was introduced between the erratum and any other research file. The erratum does not touch the sections the other four errata (01 B-1, 03 F-1, 04 B-2, 05 B-3) cover.
10. Depth check on the erratum itself: it is traced and evidenced (def lines, arithmetic, sibling counts re-verified), not a surface patch. It adds no new claim that the final document would have to guess.

### Minor notes (not blocking, not rechecked)

- M-c2-1. research/04 line 607 sentence "The live file disagrees with nothing in the instruction, so it needs no correction" is muddled (it appears right after a [CODE-CONTRADICTED] tag about the word "eight"). The intended meaning is that the live file and the instruction both give seven. The assembler should take the number from the table row plus the erratum, not from that sentence.
- M-c2-2. The old wrong text "eight" remains at line 554 under the erratum (same as M-c1-1); the assembler must read the erratum, not the row, for this word.
- M-c2-3. Paraphrased code at the PUT row (`quote(...)` for `urllib.parse.quote(..., safe='')`): not an argv or constant, no effect on any count.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:** none. The spawn prompt carried no `## Inherited Structural Verdict` section. I did not rely on the structural-c1 or structural-c2 reports that sit in the same folder (the c2 structural file exists in the folder; I did not open it).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- The "seven, not eight" count -> verified by reading `test_model_alias_policy.py` (all 249 lines) and counting `def test_` (11) with grep; partition 4 + 7 = 11.
- The 41 and 13 collected-case arithmetic -> verified by grep of `parametrize` decorators and by reading the argument lists at :336, :389, :405, :459, :514-536.
- Each of the five N-1.3 wording corrections -> verified against test text (:51, :112, :243, :459-482, :548-558, :85-89) and against `ccsession-models.json:104` (tier2b present).
- Cross-file contradiction scan of research/01 to 06 for the counts and test names -> grep, no conflict.

Self-audit answers: (1) about 40 factual claims independently checked (counts, line numbers, pins, paths); (2) files read: the c2 consolidated findings, BUILD-REQUEST.md, research/04 lines 540-639, `test_model_alias_policy.py` (all), `test_clickup_claim.py` (lines 370-570 plus grep of all def/parametrize lines), `clickup_claim.py` 228-240, `ccsession-models.json` tier keys, `chains.md` lines 12-13, the three issue-worker agent `model:` lines, and the cycle-1 verification reports (grep for F-2, N-1, "eight", "seven") only to determine the carried-over/previously-rated-PASS status; (3) zero new BLOCKING findings is supported by the line-level checks listed above, including checks that could have failed (the five N-1.3 wordings and the 41/13 arithmetic); (4) no web research performed, none needed (repo-internal, and the build request forbids sending repository details outside).

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 (including the read-back of my own report header) | Grep: 0 (the Grep tool failed with EACCES on `rg`; fallback was read-only `grep`/`wc` through Bash, recorded here) | Glob: 1 | Bash: 4 successful, 1 rejected by a hook (a mistyped inspection containing a bare `python3` token; re-run without it)

Tool engagement note: Read + Grep + Glob = 9 is below the 10 checklist items by one, so by the engagement rule this review is flagged as suspect on count alone. The four successful Bash calls are multi-grep inspections (def/parametrize listings, line counts, tier keys, chains.md, agent `model:` lines, cross-file consistency greps) and each maps to a specific check above; the count is flagged here rather than padded.

Status: Complete

## Verdict: PASS
