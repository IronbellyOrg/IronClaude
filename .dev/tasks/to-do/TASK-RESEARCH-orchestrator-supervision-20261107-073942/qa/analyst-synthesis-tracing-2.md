# Synthesis Source-Tracing Review (Partition 2 of 2)

**Analysis type:** synthesis-review (source tracing, checklist items 6-10, plus Section 8 phase split and NB-4 allowlist re-check)
**Date:** 2026-11-07
**Task directory:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`
**Assigned synthesis files:** `synthesis/synth-04-options-recommendation.md` (275 lines), `synthesis/synth-05-implementation-plan.md` (309 lines), `synthesis/synth-06-questions-evidence.md` (231 lines)
**Fix authorization:** false (report only; no synthesis or research file edited)
**Severity rule:** CRITICAL and IMPORTANT block; MINOR are notes.

[PARTITION NOTE: Cross-file checks limited to assigned subset plus the research files it draws on and `synth-02-target-gaps.md` Section 4 (needed for item 7). Full cross-file analysis requires merging both partition reports.]

---

## Method

- Read in full: synth-04 (275 lines) and synth-06 (231 lines). Read synth-05 (309 lines) in two parts, using offset and limit.
- Read the following against them: synth-02 Section 4 (lines 165-317), `gaps-and-questions.md` (359 lines, in parts), `research/scope-03-cli-patterns.md:99` (the NB-4 allowlist), and `qa/qa-nb4-fix-log.md`.
- Ran targeted read-only greps against `research/scope-01..04`, `research/research-notes.md`, `research/web-01`, `research/web-02` and `src/superclaude/core/WORKER-CONTRACT.md`. They were batched under the Bash inspection policy, and both batches returned BATCH_OK.
- Traced every file:line citation in synth-05 Section 8 to a research file. The citations covered `test_worker_contract.py` RULE_PHRASES and NEVER_AS_WORKER, `_POST_REFRESH`, the HOW-WE-WORK markers, `EXPECTED_TOP_LEVEL_COMMANDS`, Makefile Checks 1/2/6/8/9/11, `tests/cli/reflect/conftest.py:58-80`, `FIXTURES_DIR`, `tests/commands/test_issue_command.py:1-60`, the ccsession `parse_session_log` lines, WORKER-CONTRACT `:23,:45,:58,:60,:74,:107,:108,:129,:133-136,:156`, the `orca-capabilities.md` stall proof, and the `worker-read` `source_changed` cursor.
- Every one of those citations exists in research. No codebase claim in Sections 6-8 is fabricated beyond research.
- web-02 was treated as a normal research source. Every external URL in synth-05 8.3 and in the synth-04 external-context table appears in web-01 or web-02. Both web files record a Tavily fallback (web-01:8, web-02:6), and the synthesis labels external content as external.

---

## Per-File Review

### synth-04-options-recommendation.md

**Sections covered:** 6 (options A1-A3, A4 rejected with R-1 to R-4, comparison table), 7 (recommendation A1, contradictions X-1 to X-6, 7 high-level steps, external context, OQ-1 to OQ-10, coverage table)
**Verdict:** FAIL (1 IMPORTANT shared with synth-06, 1 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 6 | Steps name specific files and functions | PASS | The 7 Section 7 steps name `src/superclaude/cli/sweep/` modules, `cli/main.py` registration, `commands/sweep.md`, `skills/sc-sweep-protocol/`, `WORKER-CONTRACT.md` and `tests/skills/test_worker_contract.py`. Detail is deferred to synth-05, which is acceptable for Section 7. |
| 7 | Cross-references consistent | FAIL | A1 diagram `:60` puts `--include-remote` in the default `worker-list` argv. synth-06 row 17 says "keep it off by default" (F2). |
| 8 | No doc-only claims in Sections 6/7 | PASS | The A4 rejection reasons (`git stash *` in allowed-tools, `~/workspace` path, bootstrap bugs) trace to research-notes:52 and scope-02:136-139 and are tagged [CODE-CONTRADICTED] there. The A1-A3 rows trace to research-notes:157-159. |
| 9 | [CODE-CONTRADICTED]/[STALE DOC] surfaced | PASS (note) | The X-1 to X-6 contradictions are surfaced. X-6 (`:220`) restates a stale count claim, "gaps:125 still says Open: 76. Resolved: 24". The file now reads 75/25 (`gaps-and-questions.md:125`) (F4). |
| 10 | Key findings reflected | PASS | WC-14, the Section C precedence, the read-only seams, the #409 DERIVED skeleton and NB-4 are all reflected. |
| Phase split | Later phases recorded only | PASS | Phases 2+ are mentioned only as out of scope. |
| NB-4 | Corrected allowlist | PASS | Allowed: `task-list`, `run-list`, `run-current`, `gate-list`. Forbidden: inbox. No old-allowlist text. |

### synth-05-implementation-plan.md

**Sections covered:** 8 (steps 1.1-1.29 in 1A-1F, later phases 2-6 one line each, 8.1 gap traceability, 8.2 OQ-1 to OQ-12, 8.3 external URLs, 8.4 X-1 to X-12, 8.5 coverage, integration checklist SC-1 to SC-16)
**Verdict:** FAIL (2 IMPORTANT shared with synth-06, 6 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 6 | Steps name specific files and functions | PASS | Every step names a path and, where relevant, a symbol. Examples: 1.2 `cli/sweep/models.py`; 1.4 the `_orca` seam; 1.19 `RULE_PHRASES` under `# Coordinator rules` `:163` plus `NEVER_AS_WORKER`; 1.15 command and skill frontmatter; Makefile Checks 1/2/6/8/9/11 (scope-03:144-150); `EXPECTED_TOP_LEVEL_COMMANDS` (research-notes:81). There are no generic "create a service" steps. |
| 7 | Every synth-02 Section 4 gap has a Section 8 step or a Section 9 entry | FAIL | Six versus seven classes: synth-02 4.8 and OQ-7 route it to Open Questions, but X-7 (`:261`) settles it, and synth-06 has no entry (F1). The scope-01 `:100` row (`:182`) says "Sent to Open Questions", but synth-06 has no entry for it, and synth-02 4.6 `:251` says "settled by GQ-84 (M1)" (F11). G-A, G-B, G1-G7, writer, tests, registries and K1-K4 are each mapped to a step in 8.1. |
| 8 | No doc-only claims in Section 8 | FAIL (partial) | All codebase citations trace to research. Step 1.4 hard-codes `--include-remote` into the default argv, but its cost is [UNVERIFIED] (scope-02:231, gaps GQ-22 `:45`, synth-02 `:215`). That turns an unverified claim into a plan default without a measurement step (F2). |
| 9 | Unresolved [CODE-CONTRADICTED]/[STALE DOC] in Section 9 | PASS (note) | 8.4 X-6 (`:260`) carries the stale "Open: 76 / Resolved: 24" claim and attributes it to C2 (F4). |
| 10 | Key findings reflected | PASS | WC-14 (step 1.17), the seven-plus-idle precedence (1.2/1.3), safe-to-close as a separate REVIEW dimension, the 6 h window bounding activity only, the #409 skeleton pinned at 495eb96d, the AssertionError read-only proof and the argv-allowlist tests are all reflected. |
| Phase split | Later phases recorded only | PASS | Phases 2-6 are one line each, with no steps, files or acceptance criteria. |
| NB-4 | Corrected allowlist | PASS | Step 1.4 and SC rows allow `task-list`, `run-list`, `run-current` and `gate-list`; inbox is forbidden. This matches scope-03:99. |
| Other | Internal consistency with synth-06 | FAIL (notes) | GQ-11 is "decided" here but an owner decision in synth-06 (F5). GQ-35 is pinned here but an owner decision there (F6). GQ-26 uses the space form here and the colon form there (F7). GQ-32 has a different scope line (F8). GQ-48 has a different truncation string (F9). GQ-99 differs (F10). Line 5 says "checklist item 222", which was not verified against the task file and was not raised as a finding. |

### synth-06-questions-evidence.md

**Sections covered:** 9 (9.1 open GQ rows 1-64, 9.2 rows 65-81, 9.3 S-01 to S-14 rows 82-87, 9.4 rows 88-98, 9.5 AMB rows 99-109, 9.6 resolved, 9.7 coverage), 10 (evidence trail)
**Verdict:** FAIL (3 IMPORTANT, 7 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 6 | Steps name files and functions | N/A | Section 9 is not a plan. Its row "Next step" cells are checked under item 8 below. |
| 7 | Cross-references consistent | FAIL | There is no Section 9 row for the six versus seven classes owner decision (synth-02 4.8, OQ-7) (F1). There is no row for scope-01 `:100`, which synth-05 `:182` sends here (F11). Row 17 conflicts with synth-04 `:60` and synth-05 1.4 (F2). Line `:221` says synth-05 is "planned; not yet written" (F12). Row 50 says "Leaning A1", but synth-05 says "Settled as A1" (F13). |
| 8 | No doc-only or unfounded claims | FAIL | Row 49 (GQ-59) "Add a version probe to the header" and row 36 (GQ-41) "Record the CLI version in the report header" both assume a read-only version verb. Research found none (gaps `:82`, 07:70), and none is on the NB-4 allowlist (scope-03:99) (F3). |
| 9 | [CODE-CONTRADICTED]/[STALE DOC] surfaced | PASS | Section 9.3 carries S-01 to S-14 (rows 82-87). Section 9.5 carries AMB 1-11 (rows 99-109). |
| 10 | Key findings reflected | PASS | All 75 open GQ rows are covered by rows 1-64 (verified row by row). The 75/25 counts at `:13` and `:226` match `gaps-and-questions.md:125`. |
| Phase split | N/A | PASS | Rows for later phases are recorded as deferred. |
| NB-4 | Corrected allowlist | PASS | No old-allowlist text. Inbox stays forbidden. |

---

## NB-4 Re-check (executor extra 1)

**Result: PASS.**

- Source of truth: `research/scope-03-cli-patterns.md:99`. It allows `task-list`, `run-list`, `run-current` and `gate-list`, and keeps inbox forbidden, with the reason taken from 07:92 and 06:161.
- `qa/qa-nb4-fix-log.md` records the 3 edits that brought research in line.
- I grepped all six synthesis files (synth-01 to synth-06) for the four verbs and for `inbox`. Every hit in synth-04, synth-05 and synth-06 uses the corrected allowlist. No synthesis text still lists those four verbs as forbidden, and no text allows inbox.
- Side note, out of NB-4 scope: `gaps-and-questions.md:125` now reads "Open: 75. Resolved: 25". The off-by-one that the NB-4 log noted has been fixed in the gaps file. Two synthesis files still quote the old count (F4).

---

## Issues Requiring Fixes

| # | Severity | File(s) and location | Check | Issue | Required Fix |
|---|----------|---------------------|-------|-------|-------------|
| F1 | IMPORTANT | synth-05 8.4 X-7 (`:261`); synth-06 Section 9 (no row); headers synth-04 `:3`, synth-06 `:3` | 7, 9 | The six versus seven session classes question is routed to Open Questions as an owner decision in synth-02 4.8 and OQ-7. synth-05 X-7 instead settles it by fiat ("Section C list (rules 1-7 plus idle) is canonical"), and synth-06 has no Section 9 entry. The file headers also disagree: synth-04 and synth-06 list six classes, while synth-05 lists seven, including fenced. A synth-02 Section 4 gap therefore has neither a Section 9 entry nor an honest Section 8 disposition. | Add a synth-06 Section 9 row for the six versus seven classes owner decision, citing synth-02 4.8 and OQ-7. Reword synth-05 X-7 to "plan default (seven plus idle) pending owner decision; see Section 9". Align the class list in the synth-04 and synth-06 headers with the plan default, or mark them pending. |
| F2 | IMPORTANT | synth-06 row 17 (`:45`) versus synth-04 `:60` and synth-05 step 1.4 (`:62`) | 7, 8 | GQ-22, the cost of `--include-remote`, is [UNVERIFIED] in research (scope-02:231; gaps `:45`; synth-02 `:215`). synth-06 says "keep it off by default", while synth-04 and synth-05 put it in the default `worker-list` argv. The files contradict each other, and the plan turns an unverified cost into a default. | Pick one default across all three files. If the flag stays on, which research favours for the WC remote-row liveness reason (synth-01 `:294`), say so in synth-06 row 17 and add a measurement acceptance criterion to step 1.4. Keep GQ-22 open in Section 9. |
| F3 | IMPORTANT | synth-06 row 49 (`:77`, GQ-59) and row 36 (`:64`, GQ-41) | 8 | "Add a version probe to the header" and "Record the CLI version in the report header" both assume a read-only runtime-version verb. Research reports that none exists (gaps `:82`: "No read-only verb that reports the runtime version was found"; 07:70). No such verb is on the NB-4 allowlist (scope-03:99), so the sweep could not call one without breaking the read-only argv allowlist tests. | Reword both rows: "no read-only version verb is available. Record the capture CLI version only where an artifact already states it; otherwise print `could not determine` in the header. Keep GQ-41 and GQ-59 open." Confirm that synth-05 adds no version call. |
| F4 | MINOR | synth-04 X-6 (`:220`); synth-05 8.4 X-6 (`:260`) | 9 | Both files claim that gaps:125 "still says Open: 76. Resolved: 24". The file now reads 75/25. synth-05 also attributes this to C2, but C2 is a numbering note and not this count. | Drop X-6 or restate it as resolved (gaps:125 now 75/25), and fix the C2 attribution. |
| F5 | MINOR | synth-05 step 1.17 versus synth-06 row 9; gaps `:34` | 7 | GQ-11 is "decided as WC-14" in synth-05, while gaps `:34` and synth-06 say "open (owner decision); WC-14 is the working name". | In synth-05, say "WC-14 (working name; owner decision GQ-11)". |
| F6 | MINOR | synth-05 (GQ-35 pinned) versus synth-06 row 30 (`:58` of gaps) | 7 | synth-05 pins GQ-35 as a plan value, while synth-06 and gaps `:58` list it as an open owner decision. | Mark it as a plan default pending owner decision in synth-05, or close it in synth-06 with a citation. |
| F7 | MINOR | synth-06 row 21 (GQ-26) versus synth-05 step 1.15; gaps `:49` | 7 | synth-06 uses the colon form `Bash(superclaude sweep:*)`, while synth-05 and gaps `:49` (NB-3) use the space form `Bash(superclaude sweep *)`. | Use the space form in synth-06 row 21. |
| F8 | MINOR | synth-06 row 27 (GQ-32) versus synth-05 step 1.5 | 7 | synth-06 says "Print the window and the Run ids", while synth-05 says "Scope: with the root path". The #409 skeleton scope line is different again (scope-04:272: owners / sessions / mapped worktrees). | Make both match the plan's step 1.5 text, citing scope-04:272. |
| F9 | MINOR | synth-05 step 1.5 versus synth-02 4.4 GQ-48 and synth-06 | 7 | The truncation strings differ: synth-05 has "at least 100 (truncated at 100), total could not determine", while synth-02 and synth-06 have "could not determine: message listing truncated at 100". | Choose one literal string, because tests will pin it. |
| F10 | MINOR | synth-06 row 63 (GQ-99) versus synth-05 and synth-02 | 7 | synth-06 says "Batch where the policy allows", while synth-05 and synth-02 say "per-sweep call bound". | Align synth-06 with the call-bound disposition. |
| F11 | MINOR | synth-05 8.1 (`:182`) versus synth-02 4.6 (`:251`); synth-06 (absent) | 7 | synth-05 says scope-01 `:100` is "Sent to Open Questions", but synth-06 has no entry for it, and synth-02 says it is settled by GQ-84 (M1). | Change synth-05 `:182` to "settled by GQ-84 (M1); count only". |
| F12 | MINOR | synth-06 `:221` | 7 | The evidence trail says synth-05 is "planned; not yet written when this file was produced". synth-05 now exists. | Update the line to cite the written file. |
| F13 | MINOR | synth-06 row 50 (`:78`) versus synth-05 | 7 | synth-06 says "Leaning A1", while synth-05 and synth-04 Section 7 say A1 is the recommendation. | Change row 50 to "Recommended: A1 (synth-04 Section 7)", keeping AMB 1 open only if an owner sign-off is still required. |

---

## Summary

- Files reviewed: 3 (partition 2 of 2)
- Files passed: 0
- Files failed: 3 (synth-04 on F2 and F4; synth-05 on F1, F2, F4-F11; synth-06 on F1-F3, F5-F13)
- Total issues: 13
- CRITICAL: 0
- IMPORTANT (blocking): 3 (F1, F2, F3)
- MINOR (notes): 10 (F4-F13)
- Passing dimensions:
  - Item 6 (specific files and functions) passes.
  - The phase split is kept.
  - The NB-4 corrected allowlist passes in all files.
  - Source tracing found no fabricated codebase claim.
  - Every external URL traces to web-01 or web-02.
  - synth-06 covers all 75 open GQ rows.

## Verdict: FAIL

