# QA Report — Synthesis Gate, content-quality lens (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), orchestrator supervision research
**Date:** 2026-11-07
**Phase:** synthesis-gate (checklist items 7-12)
**Fix cycle:** N/A
**Fix authorization:** false (report only; no synthesis file modified)
**Assigned files:** `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`
**Extra executor check:** NB-4 re-check (corrected read-only Orca allowlist carried into synthesis)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Baseline sha256 of the three assigned files, taken before review:

| File | sha256 |
|---|---|
| synth-01 | `3dcdfc7774b71f7651c1984c991a4916484c19b4beb256670a505d338048db9f` |
| synth-02 | `e2ebb96d1c782205ee6a1ba0ba18cff60263ff5f0fa693ed7e602eba3f0bca9f` |
| synth-03 | `01e6435fb838a84bdebdea889e97e5e319646cd2c09fedd5bea4ed19d5905e53` |

---

## Working notes (appended during review)

- NB-4: I grepped all six synth files for the allowlist verbs. Each one carries the corrected allowlist: `task-list`, `run-list`, `run-current` and `gate-list` are allowed and `inbox` is still forbidden. The table at synth-01:185-193 matches `research/scope-03-cli-patterns.md:99`. I found no synthesis text that still uses the old allowlist.
- I re-read `gaps-and-questions.md:125` (task-folder root) just before writing this. It says "Row count: 100 rows. Open: 75. Resolved: 25 ... Open blocking QA finding: none". synth-01:201, re-read at the same time, says the line reads "Open: 76. Resolved: 24" and calls those counts "off by one". That claim is false today. synth-02:7 and :230 give the correct 75/25.
- `qa/qa-nb4-fix-log.md:39` recorded the off-by-one when the fix log was written. `gaps-and-questions.md:125` has been updated since then, so synth-01 is repeating a statement that is no longer true.
- I checked every repo path cited in the three files with Glob or Bash. All of them exist, and the files cited as absent (sweep.md, sc-sweep-protocol, cli/sweep) are absent. I checked the #409 paths with `git show 495eb96d:<path>`: canvas.py, layouts/agent_focus.py, concepts.md, data-dictionary.md, DESIGN-CONTRACT.md, integration-gaps.md and fixtures.py are all there. The Orca handler files exist under `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/`.
- web-01:8 and web-02:6 both confirm the Tavily-unavailable note at synth-03:5. I treated web-02 as a normal source.

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 7 | Cross-section consistency | FAIL | synth-01:201 gives `gaps-and-questions.md:125` as 76/24 and says the counts are off by one. The source line says 75/25 with no open blocking finding, and synth-02:7 and :230 also say 75/25. Notes: the class list has six classes at synth-01:5 and synth-03:7 but seven at synth-01:15 and in synth-02; the GQ-84 cite at synth-02:251 is wrong. Gap IDs in Section 4 are carried by Partition 2 (synth-05), so the gap-to-step mapping is outside this partition. |
| 8 | No doc-only claims in Section 2 | PASS (notes) | synth-01 Section 2 claims cite code (WORKER-CONTRACT.md anchors :9/:26/:48/:64/:68/:154/:158/:166, crash-recovery SKILL.md:4/:25/:26/:53, ccsession:224, main.py:521-561, pyproject.toml:54, install_core.py:27), and I confirmed each by Read or Grep. The guide-text claims at :79, :89 and :98-99 are tagged [UNVERIFIED] and routed to GQs. |
| 9 | Stale docs surfaced in Section 4 or 9 | PASS | The [STALE DOC] and [CODE-CONTRADICTED] items appear in synth-02 4.6 (CC table) and 4.7 (S-01..S-14). That covers orca-capabilities.md (synth-01:67), the crash-recovery read-only claim, the ccsession --list read-only claim and the recommend `python -m` docstring (S-12). |
| 10 | Content rules | PASS | Multi-item data is in tables, ASCII diagrams are present, there are no full source-code reproductions, and evidence is cited inline throughout. |
| 11 | Completeness, no placeholders | PASS | synth-01 covers Sections 1 and 2.1-2.6, synth-02 covers 3 and 4.1-4.9, and synth-03 covers 5.1-5.10. All are populated, and I found no TBD, TODO or placeholder text. |
| 12 | No hallucinated file paths | PASS | Every cited path or parent directory exists, as listed in the working notes. Line counts I checked: WORKER-CONTRACT.md 203, crash-recovery SKILL.md 157, bootstrap_scan.sh 170, parse_session_log.py 128, ccsession 1975, test_how_we_work_routing_table.py 1202, test_worker_contract.py 41 test functions. |
| NB-4 | Corrected allowlist carried | PASS | All six synth files carry the corrected allowlist, and none uses the old one. |

## Summary

- Checks passed: 6 / 7 (items 7-12 plus NB-4)
- Checks failed: 1 (item 7)
- Critical issues: 0
- Important (blocking) issues: 1
- Minor notes: 8
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | synth-01:201 | False claim. It says `gaps-and-questions.md:125` reads "Open: 76. Resolved: 24" and that the counts are off by one. The line actually reads "Open: 75. Resolved: 25 ... Open blocking QA finding: none". This contradicts synth-02:7 and :230. | Rewrite the first two sentences of synth-01:201 to say that GQ-03 (NB-4) is resolved and `gaps-and-questions.md:125` now reads Open 75 / Resolved 25. Drop the "predate the fix and are off by one" clause, or rephrase it in the past tense as history from `qa/qa-nb4-fix-log.md:39`. |
| 2 | MINOR | synth-02:251 | The "41 tests" row says "settled by GQ-84 (M1)". GQ-84 (`gaps-and-questions.md:107`) and M1 (`qa/qa-research-verification-cycle1.md:60`) are about the fenced-exclusion edge case, not the test count. | Cite the item that settles the 41-test count. I confirmed 41 test functions in test_worker_contract.py. |
| 3 | MINOR | synth-01:5, synth-03:7 | These lines list six classes and omit "fenced". synth-01:15, synth-02 and research-notes Section C (`research/research-notes.md:188`) all use seven. | Add "fenced" to both lists. |
| 4 | MINOR | synth-01:207 | "14 of 46 command files". The commands directory has 47 `.md` files, including README.md, index.md and index-repo.md. The count of 14 is correct. | Say "14 of 47 `.md` files", or state that README and index are excluded. |
| 5 | MINOR | synth-01:210 | "20 headings". `docs/designs/sc-issue-command.md` has 21 lines that start with `#`. | Correct the count, or say what was counted. |
| 6 | MINOR | synth-03:3 | Calls `orca-capabilities.md:125` a "verified codebase rule". synth-01:67 tags that inventory doc [STALE DOC], and research-notes:186 marks the line as UNVERIFIED guide text. | Drop "verified codebase rule" and cite it as guide text. |
| 7 | MINOR | synth-01:185-193 | The allowlist table omits two items from `research/scope-03-cli-patterns.md:99`: the `check --format` exclusion and the rule against any argv with two or more read modes. Both are implied by "no check at all". | Optionally add both to the forbidden column. |
| 8 | MINOR | synth-01:79, :89, :98-99 vs :288-296 | The Section 2 guide-text claims are tagged [UNVERIFIED] and routed to GQs, which is acceptable. They still sit in tension with the doc-only exclusion statement at :288-296. | Move them under the exclusion note, or label them as context rather than current-state architecture. |
| 9 | MINOR | synth-02:17 | Cites `sc-reflect-protocol/SKILL.md:63-64` as the precedent for running on PATH first. Those lines show only the bare `superclaude reflect contract-status` form, with no `uv run` fallback. | Say the precedent covers the bare form only. |

## Actions Taken

None. Fix authorization is false. The sha256 of all three assigned files matched the baseline after the review, so no synthesis file was modified.

## Recommendations

- Fix issue 1 before assembly. It is the only blocking finding.
- Fix issues 2 to 9 in the same pass if convenient. They are notes, and they do not block on their own.
- The orchestrator should merge this report with the Partition 2 report. The Section 4 to Section 8 gap-to-step mapping and the Section 6 and 8 checks live in synth-04 to synth-06.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 18 | Grep: 7 | Glob: 2 | Bash: 5 (no web research was done, so tavily_search: 0, tavily_extract: 0, web_search_fallback: 0, web_fetch_fallback: 0)
- Unchecked items: none. Unverifiable items: none. Cross-file checks outside this partition are deferred to the merge, per the partition note.

## Verdict: FAIL

1 blocking finding (IMPORTANT, synth-01:201) and 8 minor notes.

## QA Complete
