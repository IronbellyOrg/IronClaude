# QA Report - Synthesis Gate (structure + content-quality), Partition 2

**Topic:** IronClaude issue-to-work pipeline technical reference
**Phase:** synthesis-gate (lenses: structure + content-quality)
**Partition:** 2 (synth-04, synth-05, synth-06)
**Date:** 2026-11-20
**Fix authorization:** false
**Status:** Complete

## Per-file notes (appended as each file was checked)

### synth-04 (Sections 5.2, 5.3, 5.4) - checked first
- Headers `### 5.2`, `### 5.3`, `### 5.4` present; no PR 686 or rewrite text; no placeholders.
- Verified against the snapshot (read-only): `IR7_REFUSE = False` at orca_worktree.py:822 and the refusal branch at :1757; guard version line `GD:10`; approval regex `GD:347` accepts only `/sc:implement` and `/task`; `GD:409` is `implement | task | cleanup`; `launch-prompt.md:23` does name `/sc:task` (the CODE-CONTRADICTED row is true); decision grid `GD:783-803` matches the 16-cell matrix and the class rows; marker regex `GD:318`; `.take-` rename `GD:372-376`; line counts (guard 808, identity 582, pre-push 208, hooks.json 192 and plugin 154, WORKER-CONTRACT 339, issue.md 117, SKILL.md 197, orca_worktree.py 1906, clickup_claim.py 270, origin_repo.py 195, install_hooks.py 614, agents 35 each); 15 templates; WC rule lines (WC-16 at :287, never-as-worker list at :23); no caller of `orca_worktree.py pending` in src or plugins; no `pipeline.json` or `IR-3` text in src; `orca-ide` absent from the guard and present at probes.py:43 and install_user_setup.py:36; the plugin hooks.json diff (missing ccsession-tag entries, missing pragmatic-subagent.js, `async: true` on freshness-subagent-start) and byte-identical scripts; the architecture-reference lines :83, :196, :208, :268, :285 and CHANGELOG.md:17.
- No blocking defect found in synth-04.

### synth-05 (Sections 8, 9, 10, 11, Appendix A)
- `## 8.`, `## 9.`, `## 10.`, `## 11.` and `## Appendix A: Test-Pin Matrix` headings match the prompt. Subsection titles are tailored (see M-1).
- Verified: every budget/constant in 11.1 against cycle.py:34-47, github.py:37-49/376/486, record.py:434-443, audit.py:106-107, runner.py:15, cli.py:34-38, predicates.py:17, orca_worktree.py:88-91/798-799; `_TOP_KEYS` is exactly the eight keys listed; REASON_TABLE counts (27 cycle, 17 skip, 9 entry, 1 note, 4 warning, 1 operator = 59) match audit.py:26-102 member for member; hooks.json table rows (events, matchers, timeouts, line ranges) match the file; every `Lines` and `Tests` number in Appendix A (48 rows) matches `wc -l` and `grep -c def test_` on the snapshot; fixture folder holds 19 files / 12,059 bytes, all labelled `_assumed_shape`; cited test names and line numbers exist (test_issue_l2_install.py:639, test_cycle.py:1607/1623, test_github.py:575-583, conftest.py:126/352, and the named tests in the claim and guard files).
- No blocking defect found in synth-05.

### synth-06 (Sections 12, 13, 14, Appendix B)
- Headings `## 12.`, `## 13.`, `## 14.`, `## Appendix B: Removed on 2026-11-20` exact. 14.2 opens with the required no-remediation sentence verbatim. 14.1.2 has the six required columns (ID | Doc path:line | Doc claim | Code reality | Tag | Research file) and KW-1..KW-8. 14.2 has ID | Capability | Declaring doc path:line | Code evidence | Status word | Note plus an extra Class column; every item the prompt listed has a D-row (D-01, D-19, D-22, D-18, D-27, D-21, D-04/D-16, D-05, D-16).
- Appendix B verified read-only with `git show 01e7a9e23^:`: ten package files and line counts (1,597 total), 350-line contract and 811-line guard, verb list and click options, WC-17 at old :59, "Issue pipeline duties" at old :291-300, G2 rule 1 comment and case at old :441-444, release.py refusal words, approval regex, test files (10 files, 2,391 lines, 116 tests; plus the 1-test registration file), diff stat of the removal commit (PR 682, 2026-11-19 18:02 -0600).
- Finding B-1 below.

## Findings

| ID | Severity | Synth file and location | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| B-1 | BLOCKING | synth-06, 13.1.4 (`--pipeline` level), 13.1.7 (worker tier or template); partly 13.1.6 (hook script) | The Extension Guide entries have no minimal skeleton and do not say "not determinable from research". 13.1.4 and 13.1.7 name no function or code shape at all (only line ranges, constants and test names); 13.1.6 gives a prose "Registration row" but no hooks.json or `_FRESHNESS_SCRIPTS` skeleton. The synth-06 prompt (rule 12 and the Section 13 content requirement) and this gate's check (6) require each entry to carry exact file, function, registration point, minimal skeleton and pinning test, or the words "not determinable from research". 13.1.1, 13.1.2, 13.1.3 and 13.1.8 do have skeletons; 13.1.5 has only two comment lines. | synth-06 lines 96-100 (13.1.4: Files / Pinned by / Pitfall only), lines 110-114 (13.1.6), lines 116-120 (13.1.7); `grep` for "not determinable" in the section finds it only at line 128 (13.1.8, about a plugin copy of the contract) | Add a short skeleton to each: 13.1.4 (a `<!-- block:<name> -->` section in templates/launch-prompt.md, the three `choices=[...]` edits in orca_worktree.py `build_parser` at :1873/:1883/:1891, and the new level word in GD:264-269 and the GD:785-803 grid); 13.1.6 (a hooks.json group `{"matcher": "...", "hooks": [{"type": "command", "command": "~/.claude/hooks/<name>.sh", "timeout": 5}]}` and the `_FRESHNESS_SCRIPTS` entry); 13.1.7 (the agent frontmatter lines `name`, `tools`, `model`, and the `WORKERS` entry), each citing lines already in the research, or state "not determinable from research" for the part the research does not give. |
| M-1 | MINOR | synth-05, Sections 8-11 subsection titles | Subsections do not use the template names: 8.1-8.5 (template 8.1 API Endpoints Used, 8.2 Internal Integration Points, 8.3 External Service Dependencies), 9.1-9.4 (Configuration Files, Environment Variables, Feature Flags), 10.1-10.4 (Error Handling Patterns, Known Edge Cases, Graceful Degradation), 11.1-11.2 (Performance Profile, Performance-Critical Code). No table is named "Known Edge Cases" or "Graceful Degradation", but the content is present (10.1 note on unreachable exit combinations, 10.3 recovery and fail-safe table, 11 states that no measured latency exists). | synth-05 lines 15, 59, 74, 90, 106, 119-169, 186-245, 260-291 | Optional: assembler may rename or add the template subsection titles; no content is missing. |
| M-2 | MINOR | synth-05, Appendix A rows | Four rows beyond the files named in research-notes.md EXISTING_FILES (test_require_orca_worktree_agent_governed.py, test_freshness_subagent_start_policy.py, test_clickup_claim.py, test_model_alias_policy.py), marked "(added ...)" and disclosed in the closing total line; all four exist and their counts are correct. Every named file has exactly one row (48 rows = 44 named + 4 added). | synth-05 lines 346-347, 360-361, 375 | None required; assembler decides whether to keep them. |
| M-3 | MINOR | synth-04 lines 192, 213, 315, 316, 378; synth-06 line 217 | The files cite `docs/designs/orchestrator.md:116, :117, :991` as the recorded decisions. If the owner treats that design as "the rewrite design", this is a mention that BUILD-REQUEST (g) restricts to one sentence in Section 1. The run's own gap log (gaps-and-questions.md C-63, D-28, Q-11) and prompt rule F require a cited decision path:line, so the citations follow the plan; the cited lines say what the files claim (verified). synth-04 line 383 also replaces the architecture reference's words "the orchestrator design replaces them" with "[its replacement]", so the files are not consistent about this. | grep of the three files for `orchestrator.md` | Owner or assembler to confirm that a bare decision citation is allowed; no wording change needed if it is. |
| M-4 | MINOR | synth-05 (and 04) citation form | Several rows cite a bare file name (`orca_worktree.py:1776`, `clickup_claim.py:232`, `origin_repo.py:45`, `issue.md:36`) or a shorthand key (`P/`, `HK/`, `SK/`, `GD`, `OW`) instead of the repository-relative path; synth-05 defines only `P`, `SK`, `HK` and uses `OW`-style bare names elsewhere. All names are unique in the repo, so they resolve. Appendix B line citations carry the label @01e7a9e23^ through the section intro and the column headers, not on every citation (B.4 and B.7 inline citations). 13.1 uses bullets instead of the template's Task / Steps / Files / Pitfalls table. | synth-05 lines 7, 41-47; synth-06 lines 60-128, 346-394 | Assembler to expand shorthand into one path key in the final document. |

## Checks performed (counts)

- Source claims spot-checked against the snapshot or `git show 01e7a9e23^:` (not against research files alone): about 120 distinct claims across the three files (at least 35 per file), covering constants, line ranges, counts, command text, doc line quotes, test names and line numbers, and the removed-package facts. Zero wrong values found.
- Path existence: 31 repository paths cited in the three files checked with `ls`; all exist except `docs/designs/issue-watcher-live-test.md`, which the files correctly state is absent.
- Template headers: all section numbers and names owned by the three files match; subsection names vary in synth-05 (M-1).
- Required run checks: Appendix A rows (OK, see M-2); 14.2 opening sentence (OK); status words only BUILT-ON / BUILT-OFF (enabled:false) / NOT BUILT / REMOVED (OK; qualifiers follow the word); Appendix B heading (OK); PR 686 text: grep for "686" finds only line-number ranges such as `:685-686`, no PR reference (OK); rewrite design: see M-3; placeholders (`TODO`, `TBD`, `PLACEHOLDER`, empty brackets): none.
- Extension Guide: 5 of 8 entries complete (13.1.1, 13.1.2, 13.1.3, 13.1.8 fully; 13.1.5 with a two-line comment skeleton); 3 lack a skeleton (B-1).
- Not run (by design): no test was executed; guard and identity behaviour were not re-run.

## Checklist by file (PASS / MINOR / FAIL / N/A)

| # | Check | synth-04 | synth-05 | synth-06 |
|---|---|---|---|---|
| 1 | Section headers | PASS | PASS (M-1) | PASS |
| 2 | Table columns | PASS | PASS | PASS |
| 3 | No fabrication (10+ claims each) | PASS | PASS | PASS |
| 4 | Evidence citations and paths (8+ each) | PASS | PASS (M-4) | PASS (M-4) |
| 5 | Depth within budget (form only) | PASS | PASS | PASS |
| 6 | Extension Guide actionability | N/A | N/A | FAIL (B-1) |
| 7 | Cross-section consistency | PASS | PASS | PASS |
| 8 | No doc-only claims in Section 8 | N/A | PASS | N/A |
| 9 | Stale docs surfaced in Section 14 | PASS | PASS | PASS |
| 10 | Content rules | PASS | PASS | PASS |
| 11 | No placeholders or empty sections | PASS | PASS | PASS |
| 12 | No hallucinated paths | PASS | PASS | PASS |

Confidence: Verified 31 / 33 applicable cells | Unverifiable 0 | Unchecked 0 | Confidence: 93.9% on cells; the one failing cell is B-1 and is a verified defect, so the verdict is FAIL on that finding alone.
Tool engagement: Read: 15 | Grep: 22 | Glob: 0 | Bash: 12 (all read-only; nothing written under the snapshot).

## Verdict

Status: Complete

## Verdict: FAIL

Blocking findings: 1 (B-1). All other findings are MINOR notes.

