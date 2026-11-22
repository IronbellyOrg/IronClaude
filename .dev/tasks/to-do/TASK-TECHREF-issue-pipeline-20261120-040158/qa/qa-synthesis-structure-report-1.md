# QA Report - Synthesis Gate (structure + content-quality), Partition 1 of 2

**Topic:** IronClaude issue-to-work pipeline technical reference
**Date:** 2026-11-20
**Phase:** synthesis-gate (lenses: structure + content-quality)
**Partition:** 1 (synth-01, synth-02, synth-03)
**Fix authorization:** false
**Status:** Complete

[PARTITION NOTE: Cross-file checks limited to assigned subset.]

---

## Verdict: FAIL

(1 BLOCKING finding, B-1; 8 MINOR notes. Detail below.)

## Method

Read all three synth files completely. Verified claims against the read-only snapshot `/home/coder/.cache/ic-snap-20261120/master` (source truth) rather than only against research files: line counts (`wc -l`), cited line numbers, constants, argv builders, config keys, `REASON_TABLE` group counts, hook registrations, test file lists, doc line numbers, and the removed package via read-only `git show 01e7a9e23^` / `git ls-tree`. Nothing under the snapshot or outside the task folder was written.

## Findings

| ID | Severity | Synth file and location | Issue | Evidence | Required fix |
|----|----------|-------------------------|-------|----------|--------------|
| B-1 | BLOCKING | synth-02, Section 4.1 table rows 11 and 12, and the bullet "A dry-run runs steps 1 to 11 and returns inside step 12 at L1" (lines 127-128, 139) | False and self-contradictory statement about dry-run behaviour. Row 11 is defined as "Re-read before launch, `_revalidate` (979-1016) ... G7, G3', G6'", yet the bullet says a dry-run "runs steps 1 to 11", and the same bullet then says a dry-run has "no probe, re-read, `pending` write or Orca call". A dry-run does NOT run the re-read. Row 11 is also ordered before the launch step's probe, but in code the order inside `_launch` is: dry-run return, probe (`find_orca`), `build_claim_prompt`, then `_revalidate`. Row 12's own text lists "probe, prompt, re-read, ..." in the correct order, so rows 11 and 12 describe the re-read twice and in two different positions. Section 5.1.1 (synth-03) numbers the same cycle differently (launch = step 11, "dry-run runs steps 1-10"), so the two sections also disagree on step numbers for the same function. | `cycle.py:1026-1035` (`_launch` sets `launching`, then `if self.dry_run: ... return "launched", None` at 1029-1035); `cycle.py:1036-1060` (probe at 1048, prompt at 1054, `_revalidate` call at 1058, all after the dry-run return). synth-03 lines 70-87, 119 and 129 give the correct order. | In synth-02 4.1: merge row 11 into row 12 (the re-read is inside the launch step, after probe and prompt), renumber, and change the bullet to "A dry-run runs steps 1 to 10 and returns at the top of the launch step (`cycle.py:1029-1035`)". Make the step numbering of 4.1 and 5.1.1 agree, or state which numbering is the design's and which is the code's. |
| M-1 | MINOR | synth-02 Section 3 tree (line 16) and synth-03 line 41; synth-01 line 33 | Module count inconsistent: synth-01 says "8 modules ... plus an empty `__init__.py`"; synth-02 tree says "nine modules" (it counts `__init__.py`) and synth-03 says "nine modules" for the boundaries test. On disk: 8 non-empty modules plus `__init__.py`. | `wc -l src/superclaude/cli/issue_watch/*.py` gives 9 files, `__init__.py` 0 lines | Say "eight modules plus an empty `__init__.py`" everywhere. |
| M-2 | MINOR | synth-03 5.1.7 rows for `LaunchOutcome.detail ...` and `prompt_invalid` | Status column uses "dead or write-only" and "practically unreachable", which are not among the four allowed status words. The statements are true (`launch_login` and `launch_account_id` are only written at `cycle.py:1087-1088`; `disabled_present` is only used by tests). | grep of `issue_watch/*.py`; `record.py:748` | Replace with "NOT BUILT (no reader)" or move the wording to the Evidence column. |
| M-3 | MINOR | synth-01 Section 1 statistics row "per-cycle call cap 35 (32 ordinary plus 3 reserved)" vs synth-03 5.1.2 "at most 37 calls per cycle" | The figures describe different things (35 = per-issue cap `CALL_CAP`; 37 = 35 plus the two shared G1/G2 calls). Section 1 says "per-cycle", which reads as the total. Code agrees with synth-03. | `github.py:46, 49, 437-463` (`spend_shared` never refused) | In Section 1 write "per-issue call cap 35 (32 ordinary plus 3 reserved) plus 2 shared calls, 37 at most". |
| M-4 | MINOR | synth-03 5.1 (about 320 lines); synth-02 Section 4 (about 210 lines) | Over the task's depth budgets (5.1 at most 200 lines; Section 4 about 100-150). Form only; all required content items (1) to (9) of the synth-03 item are present. | `wc -l synthesis/synth-03-subsystem-watcher.md` = 331 | Assembler may trim prose; no content is missing. |
| M-5 | MINOR | synth-01 Section 2 sub-headings; synth-02 Sections 3 and 4 sub-headings | Sub-headings differ from template names (template 2.2 Subsystem Map, 2.3 Key Design Decisions, 2.4 Technology Stack; 3.1 File Naming Conventions; 4.2 Data Sources, 4.3 Data Transformations). The Phase 5 items prescribe the sub-headings used, so this is task-directed; the template digest says the assembler must reconcile names. All H2 headers (`## 1.` to `## 7.`) match exactly. | `template-digest.md` lines 13-15; template lines 161-261 | Assembler to reconcile. |
| M-6 | MINOR | synth-02 Section 3 tree | Template digest asks for a tree "without file counts"; the tree carries counts ("(942)", "19 test files", "(19 JSON files)", "(10 files...)"). All numbers verified true. | `wc -l docs/designs/*.md`; `ls tests/issue_watch` | Optional: drop counts from the tree. |
| M-7 | MINOR | synth-01 line 189 onward; synth-02 line 336 onward | Trailing non-document material ("Synthesis notes ... not part of the document"; "Open items carried ...") must be stripped or routed by the assembler; the O-1..O-9 table must feed the Open Questions section. No placeholder text. | file text | Assembler action only. |
| M-8 | MINOR | synth-01 ledger rows 10 and 14 Note column; synth-02 4.4 watcher row | A few cells carry doc-derived statements ("intended every 5 minutes by a cron entry, follow-up FU-2", "deferred behind the live test by the design", "'not governed' ... recorded at orchestrator.md:117") with a doc path but no `[UNVERIFIED - doc-only]` tag. Each is framed as design intent and paired with code evidence of absence; none feeds a diagram or status word. | `docs/designs/issue-watcher.md:15, 33`; `docs/designs/orchestrator.md:117` (text confirmed) | Optional: add the tag. |

## Per-file checklist (12 items x 3 files)

P = pass, P* = pass with MINOR notes, F = fail (blocking).

| # | Item | synth-01 (Sections 1, 2) | synth-02 (Sections 3, 4, 6, 7) | synth-03 (Section 5.1) |
|---|------|--------------------------|--------------------------------|------------------------|
| 1 | Section headers match template | P ("## 1. Overview", "## 2. Architecture"; sub-names task-directed, M-5) | P* (H2 `## 3.`, `## 4.`, `## 6.`, `## 7.` exact; M-5) | P ("## 5. Subsystem Reference" then "### 5.1 Issue watcher") |
| 2 | Table column structures | P (ledger has exactly Piece / Status word / Evidence / Trigger / Writes to GitHub / Note; integration map; component table has the five required columns) | P (trigger table Piece / What starts it / Who or what runs it / Frequency / Evidence / Live?; writes table Piece / Command / Actor / read-write / File:line / When; gates table; Section 6 store table has all six columns; Section 7 N/A with rationale) | P (key files, G1-G7, exit codes, gate table with "Pinned by", extension points File / Function / What to change / Pinned by) |
| 3 | No fabrication (10+ claims) | P (30+ checked: line counts, 59 words, 12 argv, removed package 10 files = 1,597 lines, commit date and PR #682, hooks.json ranges, WC-2..WC-16, IR7_REFUSE, CHANGELOG:17) | F (B-1 is a false statement; all other checked claims true: constants 34-47, cycle step lines, G1-G7 argv, `claim.md:125` contradiction, `launch-prompt.md:23` vs guard regex, dispatch fields) | P (30+ checked: argv at github.py 175-262, `CallBudget` 437-463, config keys 58-69 and 216-283, REASON_TABLE group counts 4/7/5/2/2/5/1/1/17/9/6 = 59, `_PRECEDENCE`, E1-E14 order vs `_examine` 915-961, `MAX_LAUNCHES_PER_CYCLE` read nowhere) |
| 4 | Evidence citations, paths exist (8+) | P (40+ paths exist) | P (40+ paths exist; `plugins/superclaude/hooks` mirror and 3 byte-identical scripts confirmed with `cmp`) | P (all `P/` modules, `install_user_setup.py:36`, test files exist) |
| 5 | Depth within budget | P (Section 1 about 38 lines; Section 2 about 137 lines) | P* (Section 6 about 25 lines, under 150; Section 4 over guide, M-4) | P* (about 320 lines vs 200, M-4; form only) |
| 6 | Extension-points specific | n/a | n/a | P (6 rows with file, function, change, pinning test; test files exist) |
| 7 | Cross-section consistency | P* (M-3) | P* (B-1 step-number disagreement with 5.1.1; M-1) | P* (M-1) |
| 8 | No doc-only claims in Section 2 / Section 4 flows | P* (M-8; diagram built from code-read sources) | P (doc-derived contradictions tagged `[CODE-CONTRADICTED]`; hand-off prose tagged `[UNVERIFIED - doc-only]`) | P (doc claims in 5.1.8 tagged) |
| 9 | Stale-doc discrepancies surfaced | P (pointers to Section 14; evidence-limits paragraph) | P (4.1, 4.3, Section 6 `[CODE-CONTRADICTED]` bullets; open items O-1..O-9) | P (5.1.8 nine rows) |
| 10 | Content rules | P (tables; no code bodies; statistics once) | P (no source reproductions; short argv quotes; per-file line counts are the task-required 3.1 table) | P (argv and constants only; module line counts are the task-required key-files table) |
| 11 | Completeness, no placeholders | P (grep TBD/TODO/FIXME/PLACEHOLDER: none) | P (none; the one `[...]` hit is quoted code `run([...])`) | P (none) |
| 12 | No hallucinated paths | P | P | P |

## Additional run checks

| Check | Result |
|-------|--------|
| Status words only BUILT-ON / BUILT-OFF (enabled:false) / NOT BUILT / REMOVED | synth-01 PASS; synth-02 uses qualifiers after a valid word ("BUILT-ON as a verb, no production caller"); synth-03 5.1.7 has two non-listed phrases (M-2) |
| Exactly one PR 686 / rewrite-design sentence, in synth-01 Section 1, none elsewhere | PASS (grep `686|rewrite|redesign` over the three files: synth-01 line 44 is the sentence; other hits are `cycle.py:685-686` line ranges and the verb "Rewrites" in a hook description) |
| No memory/chat-sourced "zero-setup watcher", "COORD-", "dispatcher", "grant rows" as fact | PASS (all uses say "not found in snapshot"; `COORD-` grep over snapshot returns 0 files; "grant row" confirmed as prose only at `WORKER-CONTRACT.md:57` and `issue-pipeline-fu1.md:24`) |
| Ledger one row each for watcher, claim, L1 guard, L2 hook, job identity, G2 rule 2, coordinator text, removed package plus the extra rows named in the item | PASS (rows 1-18 cover all, including G2 rule 1, `pending` caller, IR-3, IR-7, OB gate, scheduler, dispatcher/COORD/zero-setup, live-test record, hand-off, binding) |

## Checks performed

- Items checked: 12 checklist items x 3 files = 36; passed 35 (with notes where marked), failed 1 (item 3, synth-02, B-1). Item 6 is n/a for two files (no extension table required there).
- Claims spot-checked against the snapshot or read-only git: about 110 (more than 10 per file; more than 8 cited paths per file confirmed to exist).
- Confidence: Verified: 35/36 | Unverifiable: 0 | Unchecked: 0 | Confidence: 97.2% (the failing item is a verified failure, not an unknown).
- Tool engagement: Read: 16 | Grep: 17 | Glob: 1 | Bash: 7 (four read-only batch scripts under a private /tmp directory removed on exit, plus three single read-only commands). Tavily and web tools: not used (no external lookup was needed).
- Not verified: the research-derived test totals for guard tests (24,388 lines, 921 functions) and the removed-package 116 test count were checked only against the research file arithmetic (`research/05-guard-stack-and-ccsession.md:539`), not recounted; the watcher test totals (19,801 lines, 867 functions) were recounted and match. Unrelated to the verdict.
- Remaining limitation: no live GitHub or Orca behaviour is verifiable from a snapshot; the synth files label those items [UNVERIFIED] and that labelling is correct.

Status: Complete
