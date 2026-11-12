# QA Report — Report Lens: Domain Accuracy

**Topic:** Orchestrator mode Phase 1 (issue #339)
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Date:** 2026-11-07
**Phase:** report-lens-domain-accuracy (single dimension)
**Fix cycle:** N/A
**Fix authorization:** false

---

## Domain-Accuracy QA Report

Whole report read (:1-1651, at most 150 lines per Read). Lines :390-395 sit inside a code fence (mock output) and were treated as content, not headers. Both [CONTRADICTION] markers and the NB-4 exception record were judged under this lens and left in place.

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | 3.1 rule 2 (:353-354), 2.3 (:162), 5.10 R2 (:848), GQ-26 row 70 (:1520) vs 2.1 table (:56), 3.3 (:446), 5.1 (:650) | WC-10 is applied wrongly, and the report contradicts itself. Rule 2 and R2 count a "turn PROVED final" or a "proved-final transcript turn without `worker_done`" as stall proof. That evidence comes from the transcript or ccsession, not from Orca. `WORKER-CONTRACT.md:45` (WC-10) says the coordinator "acts only on Orca's stall proofs", and `:74` (WC-6) says "after Orca's positive stall proof". 5.1 :650 says "only `exited` liveness or an observed process exit counts", which contradicts R2 inside the same report. 2.3 :162 likewise allows "separate final-turn proof" from transcript evidence. The 2.1 rule table (:56) drops the word "Orca's" ("Act only on stall proofs"), while 3.3 :446 quotes the rule correctly. | Limit rule 2, :162 and R2 to Orca-sourced evidence: liveness `exited` or an Orca-observed exit. Move a final transcript turn with no Orca proof to "could not determine", or show it only as a note. Restore "Orca's" in the :56 table row so it matches `WORKER-CONTRACT.md:45`. |
| 2 | MINOR | 2.1 (template range) | The report says the template sits at `WORKER-CONTRACT.md:166-203`. `wc -l` gives 203 because the file has no trailing newline, so the "203 lines" count is consistent with `wc`. The Read tool shows a 204th content line, the `/sc:workflow` row, and the :166-203 range leaves it out. | Cite the template range as :166-204, or note that the line count is a newline count. |
| 3 | (withdrawn) | 2.3 (SKILL.md line count) | Checked and found correct: `wc -l` gives 157 for `sc-crash-recovery/SKILL.md`, which matches the report. `bootstrap_scan.sh` (170), `parse_session_log.py` (128) and `ccsession` (1975) also match. This row is kept so the numbering stays stable, and it does not count toward the totals. | None. |
| 4 | IMPORTANT | 2.3 (:157, :164), 3.3 (:456), C4 (:555), S-09 (:583), GQ-26 rows 15 (:1455), 50 (:1491), S-08/S-09 (:1541), 90 C4 (:1553) | The A4 rejection overstates the path defect. In `SKILL.md`, `~/workspace/` is hardcoded only for `--all` fleet mode (:25, :36, :53) and for one dev-fallback allowlist entry (:4, `Bash(~/workspace/IronClaude/.claude/skills/...)`). Default mode resolves the project from cwd (:49-50), and the installed path `Bash(~/.claude/skills/sc-crash-recovery/scripts/*)` is also allowed (:4). So the :157 claim "it finds none of them" holds only for `--all`. C4 cites `SKILL.md:25-27` as evidence that "this host uses ~/workspaces/", but the skill cannot show the host's layout. The point is presented as [CODE-CONTRADICTED] support for rejecting A4, so it is a false code claim, not a wording issue. The A4 rejection still stands on `Bash(git stash *)` (:4) and the `bootstrap_scan.sh` defects. | Narrow the claim to "`--all` and the dev-fallback allowlist entry hardcode `~/workspace/`; single-project mode uses cwd". Cite the host layout to a host observation (for example this worktree's path), not to `SKILL.md:25-27`. |
| 5 | MINOR | 2.1 (brief range) | The report says the brief spans `WORKER-CONTRACT.md:77-97`. The file has "What the coordinator owes" at :77-89 and "Brief layout" at :91-99, so :77-97 ends inside the layout section. | Cite the two ranges :77-89 and :91-99. |
| 6 | MINOR | :961 (conflicts citation) | :961 cites `sc-crash-recovery/SKILL.md:120-125` for the conflicts edge case. In SKILL.md, :120-125 is pipeline knowledge and output style, and the conflicts edge case is at :134. The :120-125 range belongs to `report-template.md`. The claim itself is true; only the citation is wrong. | Cite `SKILL.md:134`, or keep :120-125 and give `report-template.md` as the file. |
| 7 | MINOR | 6 R-1 (:1004) | R-1 puts the `~/workspace` script path into the read-only claim about the reused crash-recovery scripts. The path concern applies only to `--all` and the dev-fallback allowlist entry (see row 4), so including it here repeats the row-4 overstatement on a point of wording. | Remove the `~/workspace` clause from R-1, or narrow it to `--all`. |
| 8 | MINOR | [CONTRADICTION] at :1078 | The marker sets HOW-WE-WORK `:314-337` against `:318-337`. Both ranges contain the whole "Other commands" table: heading :314, begin marker :318, table :320-333, end marker :337. The two citations differ only in where the range starts. No fact contradicts another, so under the domain lens this is a citation-range discrepancy, not a real contradiction. Left in place as instructed. | Resolve the marker by using :318-337 (marker to end marker) everywhere, or :320-333 for the table body. Record that the two ranges agree on content. |
| 9 | IMPORTANT | 3.1 (:329), Step 1.15 (:1198), :961 | :329 tags `sc-reflect-protocol/SKILL.md:63-64` [CODE-VERIFIED] as precedent for running PATH-first with a `uv run` fallback and listing both forms in allowed-tools. Lines 63-64 contain only bare `superclaude reflect contract-status` lines. sc-reflect-protocol has no `uv run superclaude` anywhere, and its allowed-tools (:5) is a bare `Bash`. The only `uv run` form, `Bash(uv run superclaude swarm *)`, is in `sc-swarm-wizard-protocol/SKILL.md:7`, which has no bare form. No primitive pairs the two forms, so this is a false [CODE-VERIFIED] claim about existing code. | Drop the [CODE-VERIFIED] tag and present B-19 (PATH-first plus `uv run` fallback) as a new design. Cite reflect only for the bare form and swarm-wizard only for the `uv run` form. |
| 10 | IMPORTANT | [CONTRADICTION] at :1507; GQ-26 row 21 (:1461) vs Step 1.15 (:1198), :329 | Row 21 uses the colon form `Bash(superclaude sweep:*)`, while Step 1.15 and :329 use the space form `Bash(superclaude sweep *)`. Repo precedent uses the space form (`sc-crash-recovery/SKILL.md:4`, `sc-swarm-wizard-protocol/SKILL.md:7`), and the planned SC-16 static test pins the exact strings. A builder would follow one form and fail the test on the other. This is a real contradiction, so it is graded IMPORTANT. | Use the space form throughout and correct :1461. Keep the marker until the fix is made. |
| 11 | MINOR | Appendix (:1650) | :1650 says "`qa/` (24 files)", but `qa/` holds 54 files. The listed categories leave out the 18 Phase 5 synthesis-gate QA files: analyst-synthesis-accuracy and analyst-synthesis-tracing (1-2), the 12 qa-synthesis-* files, and qa-consolidated-findings-phase5 with its cycle1 file. | Correct the count to 54 and add the Phase 5 synthesis-gate category. |

### Summary

- CRITICAL: 0
- IMPORTANT: 4 (rows 1, 4, 9, 10). All are blocking.
- MINOR: 6 (rows 2, 5, 6, 7, 8, 11). These are notes and do not block.
- Withdrawn: 1 (row 3, kept for stable numbering).
- Checklist results:
  - (a) Architecture claims: FAIL (rows 4, 9).
  - (b) Orca and ccsession capability claims: PASS. No sweep, close or WC-14 is described as current. Live Orca row shapes are marked [UNVERIFIED] in the report itself.
  - (c) Versions: PASS. These match pyproject.toml and the cited sources: superclaude 5.0.0, Python >=3.10, ruff==0.15.20, orca-ide 1.4.245-aidev02.
  - (d) Integration points and WC-10: FAIL (rows 1, 10).
- [CONTRADICTION] :1078 is a citation-range discrepancy and is graded MINOR (row 8). [CONTRADICTION] :1507 is a real contradiction and is graded IMPORTANT (row 10).
- NB-4 (the research gate passed by exception): the records at :1583 and :1651 agree with the gaps file at :125 ("Open 75 / Resolved 25"). No domain finding.

**Verdict: FAIL**

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check**

- None. The spawn prompt carried no `## Inherited Structural Verdict` block, so this review ran standalone. Every claim below was checked with my own tool calls.

**(b) Independent semantic checks (INV-019)**

- **WC-10 / WC-6 wording (row 1).** Read `WORKER-CONTRACT.md` :45 and :74, and compared them with report :56, :162, :353-354, :446, :650, :848 and :1520.
- **Other contract citations.** Checked `WORKER-CONTRACT.md` :23, :60, :108, :126-158, :166-204, :77-89 and :91-99.
- **A4 path defect (row 4).** Read `sc-crash-recovery/SKILL.md` :4, :13, :25, :36, :49-50, :53, :91, :93-97, :120-125, :134, :137, :139-150 and :155. Line counts confirmed with `wc -l`: SKILL.md 157, `bootstrap_scan.sh` 170, `parse_session_log.py` 128, `ccsession` 1975.
- **Script behaviour.** Checked `bootstrap_scan.sh` :31, :73, :82, :136 and `parse_session_log.py` :31-40, :45-55, :85-102.
- **Report-template citations (row 6).** Checked `report-template.md` :120-125 and :127-129.
- **Allowed-tools forms (rows 9, 10).**
  - `sc-reflect-protocol/SKILL.md` :5 is a bare `Bash`, and :63-64 have only bare commands. Grep for `uv run superclaude` in that skill found nothing.
  - `sc-swarm-wizard-protocol/SKILL.md:7` has `Bash(uv run superclaude swarm *)`.
  - `sc-crash-recovery/SKILL.md:4` uses the space form.
  - Report :329, :961, :1198 and :1461 were read against these.
- **CLI architecture.**
  - `cli/main.py` :18-26, :519-561, :564-565.
  - `reflect/config.py` :64-78, :103-109.
  - `recommend/__init__.py`:12-20 imports lazily; `reflect/__init__.py`:17-30 imports eagerly.
  - `reflect/contract.py` :7, :397 and `contracts/__init__.py` :204-206.
- **ccsession capability claims.** Read `ccsession` :144, :175-222 (`name_key`), :285-287 (`ensure_names_migrated`), :564-605, :1301-1302, :1408-1411 (`session_transcript`) and :1787-1788, and compared them with report :179, :444 and :1177.
- **Orca message-check handler.** Checked `message-check-handler.js` :17, :18-19, :30 and :58-71. `check` goes through `callOrchestrationMutation`.
- **Routing and tests.**
  - `HOW-WE-WORK.md` :314, :318, :320-333, :337, :400-406 (row 8).
  - `test_worker_contract.py` :86, :163, :245-254, :379, :398, :446, :541, :545, :588, :1090-1098, :1166.
  - `test_routing_refresh.py` :33, :38-40, :647-648.
  - `test_how_we_work_routing_table.py` :27-40, :291-311, :342-347; the file is 1202 lines.
  - `test_routing_plugin_parity.py` :38 and `test_orca_session_launch_guidance` :14-16.
- **Docs and config.** Checked `commands.md` :105, :115, :347, `sc-issue-command.md` :384, :402, `core/CLAUDE.md` :65-82, `Makefile` :362, :467-476 and `pyproject.toml` :203-206.
- **Versions (checklist c).** `pyproject.toml` gives superclaude 5.0.0, Python >=3.10 and ruff==0.15.20. `orca-ide --version` reports 1.4.245-aidev02; only `--help` and `--version` were run, with no state change.
- **Appendix counts (row 11).** Listed `qa/` and counted 54 files, compared with the 24 claimed at :1650. The research file line counts matched, synth-05 is 310 lines, and the gaps file :125 matches NB-4.

**Unverifiable here.**

- Live Orca row shapes and stall-proof behaviour: confirming them would require state-changing Orca calls, which this review is not allowed to make. The report already marks them [UNVERIFIED].
- How pipx sets up PATH on a fresh install.
- The total count of command files, because the listing was truncated.

None of these unverifiable claims is a checklist item on its own.

**Web research.** None was performed and none was needed. Tavily was not called, and no fallback tool was used.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

The four checklist items (a)-(d) were all checked with tool evidence. The unverifiable sub-claims listed above are recorded, not counted.

**Tool engagement:** Read: 35 | Grep: 13 | Glob: 0 | Bash: 11

These counts are approximate and cover both halves of the session. The total of Read plus Grep plus Glob (48) is well above the number of checklist items (4).

## QA Complete
