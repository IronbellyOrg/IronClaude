# QA Report - Synthesis Gate, Structure and Content-Quality Lens (Partition A)

**Topic:** Observer, sweep and dashboard family technical reference
**Date:** 2026-11-20
**Phase:** synthesis-gate (structure and content-quality lens)
**Fix cycle:** N/A (review 1)
**Status:** Complete
**Partition:** A of 2 (synth-01, synth-02, synth-03, synth-04). [PARTITION NOTE: cross-file checks limited to this subset; Section 8 (synth-06) and Section 14 (synth-07) consistency needs the merged partition reports.]
**Fix authorization:** false (report only; no synthesis file was modified)

---

## Overall Verdict: PASS (with minor notes)

No blocking finding. Every sampled claim traced to the snapshot at `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6), the origin/master `.dev/` files, the checkout design package, or the research files. Seven minor findings are recorded as notes.

## Items Reviewed (per-file checklist)

Legend: P = pass, N = pass with minor note, n/a = not in this file.

| # | Check | synth-01 (S1, S2) | synth-02 (S3, S4) | synth-03 (S5.1, S5.2) | synth-04 (S5.3, S5.4) |
|---|-------|---|---|---|---|
| 1 | Section headers match template | P: `## 1. Overview`, `## 2. Architecture`, 2.1 to 2.4, plus added 2.5 | P: `## 3`, 3.1, `## 4`, 4.1 to 4.3 | P: `### 5.1`, `### 5.2` | P: `### 5.3`, `### 5.4` |
| 2 | Table columns per template | P: 2.2, 2.3, 2.4 match (2.3 last column renamed "TDD Divergence (design or docs)") | P: 3.1, 4.2, 4.3 match exactly | P: Dependencies and Consumers tables match | P: same |
| 3 | No fabrication (sampled) | N: m4 | N: m2 | P | N: m1, m3 |
| 4 | Evidence uses real paths | P | P | P | P |
| 5 | Subsystem depth in budget | n/a | n/a | P: 5.1 about 120 lines, 5.2 about 120 (complex 120-200) | P: 5.3 about 117, 5.4 about 121 |
| 6 | Extension Guide (S13) | n/a | n/a | n/a | n/a (Section 13 is in synth-07) |
| 7 | Cross-section consistency | P: map 5.1 to 5.6 matches headings of 5.1 to 5.4 and key-file line counts | P: Section 3 tree matches 5.x file lists | P | P |
| 8 | No doc-only claims in S2 or S8 | N: m6 | n/a | n/a | n/a |
| 9 | Stale docs surfaced | P: SD-06, 07, 09, 21 to 23, 25, CC-01 to 03 carried | P: SD-08, SD-14, CC-02, CC-03 | P: SD-02, SD-05, CC-01 | P: SD-06, 07, 09, 14, CC-04 |
| 10 | Content rules | N: m5, m7 | N: m7 | P | P: signatures only |
| 11 | No placeholders or empty sections | P: grep for TBD, TODO, FIXME, bracket placeholders found none in all four | P | P | P |
| 12 | No hallucinated paths | P | P | P | P |
| M | Family-at-glance matrix | P: four subjects (Observer, Sweep, Agent-work-report, Dashboard design package) by five columns (data sources, outputs, live vs designed, consumers, overlaps) | n/a | n/a | n/a |
| U | No unification recommendation | P: no match | P: only the disclaimer "no unification recommendation" | P | P: only the disclaimer |

## Verification evidence

Tool use: three-plus batch scripts and parallel greps (all read-only), plus Reads of the template and the four files.

- Line counts match: observe `.py` total 6,011 and schema 158; sweep 3,759; agent-work-report scripts 5,777 and SKILL.md 194; per-file sweep test counts 94+61+3+10+100+12+43 = 323; observe tests 36 entries, 26 test files, 565 defs; observer fixtures 20 entries, 19 JSON; package 412 files, 6 `.pyc`, 18 scenario files, 360 export files, layouts 637 lines; `render.py` 130, `fixtures.py` 122, `canvas.py` 122.
- Registration `main.py:581-583` (sweep) and `:590-592` (observe); gate constants `commands.py:67` and `:70` both True; exit-code lines (`commands.py` 187-196, 264-268, 364-369, 377-387; `keys.py` signal handlers give 143 and 129 via `128+signal`).
- Adapter facts: 13 forbidden prefixes pinned as a superset in `tests/observe/test_commands.py`; `RUN_ID_PATTERN`; cursor limits; `MAX_CALLS_PER_CYCLE = 5`; `FixtureSource.read_questions` returns FAILED `no-question-fixture`; `_find_orca` `any(...)` over `topics` sits outside the `try`.
- Sweep facts: `ALLOWED_ORCA` is 10 templates, 7 verbs, 6 called and 4 pinned, with call sites at the cited lines; `ALLOWED_GIT`; `Budget(50, 90.0, 10.0)`; `CHECKED_ORCA_VERSION = "1.4.245"`; `SECTIONS` has 12 entries; `CLASSES` unpack at `classify.py:42-51`; rule 5 at `classify.py:251-269`; `worker_done_seen`, `fenced_evidence`, `agent_wait_since` defaults at `models.py:108-112`; `.gitignore:255-256`.
- Docs and design: `CHANGELOG.md:170-171`, `commands.md:619-621`, `cli-groups.md:42`, `README.md:35,136`, `orchestrator-mode.md:27`, `orchestrator.md:3` and `:930`, SPEC lines 103, 106, 231, 232, 238, 251, 274, 338 (origin/master), `stack.md:3`, `release-gates.md:5, 9, 58`, `WORKER-CONTRACT.md:23, 46, 110, 157, 287-289`, `HOW-WE-WORK.md:298, 359`.
- PR facts (#503, #514, #577, #592, #598, #673, #681 to #690) trace to research files 02, 06 and GF-3. Gap IDs cited in the files (G-04 to G-10, G-20, G-35, G-37, U-xx, CC-xx, SD-xx) exist in `gaps-and-questions.md`.
- Not re-run: no test, no `gh` call, no Orca call. Live-run counts (180 of 180, 263 of 264) are research-sourced and tagged UNVERIFIED by the files themselves.

## Issues Found

No blocking issues. All findings are minor (notes only; no fix cycle needed).

| ID | Severity | File | Evidence | Suggested fix |
|----|----------|------|----------|---------------|
| m1 | MINOR | synth-04 (5.3 Key Files, "`_guard` 728"); synth-02 4.3 ("728-779") | `def _guard(` is at `classify.py:741`; 728 falls in the preceding `_Guard` class. 745 (JOIN_PATH read) is correct | Cite `_guard` at 741 |
| m2 | MINOR | synth-02 (callout after Section 3 tree) | `common.py:25` is the `POLL_CONFIG` constant; `orchestrator_repo` is named at `common.py:22` (comment) and `:29-48`. `SKILL.md:14` and `cycle.py:216-220` (unknown-key rejection) are correct | Cite `common.py:22, 40-48` |
| m3 | MINOR | synth-04 (5.3 Key Files) | `Classification` is at `models.py:213`, not 212 | Cite 213 |
| m4 | MINOR | synth-01 2.4 | Versions say "not stated in research" for Rich, jsonschema, pexpect and PyYAML, but `pyproject.toml:37-41` gives `rich>=13.0.0`, `pyyaml>=6.0`, `jsonschema>=4.0.0`, `pexpect>=4.9` | Fill the Version column from `pyproject.toml` |
| m5 | MINOR | synth-01 2.5 (Sweep row) | "6 of 8 classes can print on live data" reads stronger than synth-04, which says idle and person-active print only "rarely" and no live row was found [UNVERIFIED] | Reword to "4 classes confirmed on live data; idle and person-active possible, not seen" |
| m6 | MINOR | synth-01 2.3 (staged release row) | R0 to R4 stage definitions come from `release-gates.md`, but the row carries no "(doc)" mark, unlike synth-03 | Add "(doc)" to the R-stage content |
| m7 | MINOR | synth-02 3.1; synth-01 Section 1 | "19 JSON files" in 3.1 repeats a Section 1 key number, against the template's state-once rule | Drop the count in 3.1 |

## Self-audit

Seven minor findings and zero blocking: the files cite hundreds of line numbers, and the sample found only drift of 1 to 13 lines on true claims. I found no false claim, missing section, placeholder, wrong path, or unification recommendation. The sample covered about 120 distinct claims across all four files. Residual risk: unsampled claims (for example `render.py` layout details and most line numbers inside `tests/sweep/test_classify.py`) rest on the research files.

## Confidence

Verified: 12/12 checklist items plus 2 extra checks (matrix, no-unification) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (on sampled scope)
Tool engagement: Read: 8 | Grep: 5 | Glob: 0 | Bash: 7 (batch scripts, about 80 read-only commands)
Web research: none (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0)

## Actions Taken

None (fix authorization false).

## Recommendations

- Proceed to assembly. Optionally apply m1 to m7 in the fix pass; none blocks.

## QA Complete
