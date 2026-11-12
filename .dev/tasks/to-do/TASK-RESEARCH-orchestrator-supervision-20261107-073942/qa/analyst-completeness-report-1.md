# Research Completeness Verification (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339): read-only coordinator `/sc:sweep` and coordinator-loop rule
**Date:** 2026-11-07
**Analysis type:** completeness-verification (checklist items 1, 4 and 5 only)
**Task directory:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`
**Scope file read first:** `research/research-notes.md` (306 lines by `wc -l`; EXISTING_FILES, gaps G-A and G-B)
**Assigned files (each read in full; line counts by `wc -l`):**
- `research/scope-01-contract.md` (152 lines)
- `research/scope-02-orca-recovery.md` (235 lines)
- `research/05-orca-row-schema.md` (201 lines)
**Depth tier:** Deep
**Fix authorization:** false (no research file was edited)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.] Rows of EXISTING_FILES cited only by S3 (`scope-03-cli-patterns.md`) or S4 (`scope-04-409-layout.md`) belong to the other partition and are listed as out of scope, not as gaps.

Method: every assigned file read in full; selected claims re-checked against the cited sources on 2026-11-07 (captures read with Read, help text read with `--help` only, tag counts by Grep). No state-changing Orca, ccsession, sweep or close command was run.

---

## Checklist item 1: Coverage audit

Source of scope: `research-notes.md` EXISTING_FILES, rows tagged S1 or S2 (plus 05, which was planned under RECOMMENDED_OUTPUTS). "Investigated" means the file reads the source and states findings about it; "cited only" means the source is named but not examined.

| Scope item (EXISTING_FILES) | Covered by | Status |
|---|---|---|
| `src/superclaude/core/orca/WORKER-CONTRACT.md` | scope-01 (contract quotes at :11, :20, :23, :39-46, :57, :60, :70-74, :105-108, :112-117, :122-129, :133-136, :156, :158; all re-checked, all hold) | COVERED |
| `src/superclaude/core/HOW-WE-WORK.md`, `core/CLAUDE.md` (Orca session launches, :45) | scope-01 | COVERED |
| `tests/core/test_orca_session_launch_guidance.py` | scope-01 (:112, pins at :10-31) | COVERED |
| `src/superclaude/cli/install_core.py`, `tests/commands/test_help_command.py`, root `CLAUDE.md` | scope-01 (cited in body; missing from its "Files read" table) | COVERED (table incomplete; see F5) |
| `.dev/issues/339/` issue body and analysis (F1-F14, S1-S5) | scope-01 | COVERED |
| `orca-capabilities.md` (worker-list, worker-show, status, liveness, runtime_unavailable) | scope-02 (:149, :151, :184 and others), 05 (:8, :10-21, :97-102) | COVERED |
| `orca-ide orchestration worker-list --help`, `worker-show --help`, `status --help` (Orca 1.4.245) | scope-02, 05 (re-run read-only with `--help`; flag lines 10-11 and 13-16, notes 19-22, worker-show line 16 all hold) | COVERED |
| Captures lc16, lc17, lc01, lc01-step7 | 05 (all line ranges re-checked and correct), scope-02 (lc17) | COVERED |
| `skills/ccsession-tag/README.md` ("Orca launch text", S1) | scope-01 :112 names it as a second pin location only; no file reads its launch text | GAP (cited only; see F5) |
| `.dev/orca-command-refactor/changes/CR-01...` | Named by the issue analysis that scope-01 reads; no assigned file reads CR-01 itself, although AMBIGUITY 11 in the notes depends on it | GAP (see F5) |
| `APPROVED.md` | research-notes itself records "not read by any scope" | GAP (see F5) |
| Seed brief (`.dev/brainstorms/20261107-073115-orchestrator-mode/`) | Marked "input" in the notes; no assigned file cites it | GAP, MINOR (input document, not code) |
| S3-only and S4-only rows (CLI patterns, #409 layout) | Partition 2 | OUT OF SCOPE |

Result: every S1/S2 code or contract source that the Phase 1 design depends on is investigated by at least one assigned file. Four named sources are cited only (or not at all). None of them is code the sweep would call, so the coverage gaps are MINOR; they are listed under F5.

---

## Checklist item 4: Completeness

The spawn prompt fixes the gaps-section name per file (`## Open questions` in the scope files, `## Gaps and Questions` in 05) and requires Key Takeaways only in 05.

| Research file | Status | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| `scope-01-contract.md` | `**Status:** Complete` (line 2) | Y (`## Summary`, line 150) | Y (`## Open questions`, line 140) | N/A (not required) | Complete |
| `scope-02-orca-recovery.md` | `**Status:** Complete` | Y (`## Summary`, line 227) | Y (`## Open questions`, line 215) | N/A (not required) | Complete |
| `05-orca-row-schema.md` | `**Status:** Complete` | Y (`## Summary`, line 199) | Y (`## Gaps and Questions`, line 180) | Y (several "Key Takeaways:" labels in the body) | Complete |

All three files pass item 4 as stated. Two quality notes that do not change the ratings:
- scope-01's heading "Issue-339 conflicts F1-F12" is stale; the analysis now has F1-F14 plus S1-S5. The body says so, but the heading does not.
- scope-01's Summary claims 54 CODE-VERIFIED, 12 CODE-CONTRADICTED and 4 UNVERIFIED tags. A Grep of the file finds more raw occurrences of each tag, so the counts depend on an unstated counting rule (see F6).

The research-notes file is not an assigned file, but its own record of these files is stale (see F4): line 9 gives old line counts (147/220/197; actual 152/235/200 for scope-01/02/03), lines 235-238 say scope-01 has no Summary heading (it has one at line 150), and line 215 still lists 05 as MISSING.

---

## Checklist item 5: Cross-reference check

Cross-cutting concerns that appear in more than one assigned file, and whether each file points at the others:

| Concern | scope-01 | scope-02 | 05 | Cross-referenced? |
|---|---|---|---|---|
| Meaning of "finished" | Contract read and admitted (`WORKER-CONTRACT.md:122-129`) | outcome succeeded/failed plus settled | outcome only | NO; the definitions conflict (F1) |
| Meaning of "idle" | not defined | no idle class | "settled and `resource.terminalState` retained or released" | NO; conflicts with notes Section C, where idle is a person-started session with no Orca Task (F1) |
| Safe to close | all five refusal conditions (`WORKER-CONTRACT.md:108`) cleared | `reclaimable` + `nextAction release` (classifier table and Summary line 230) | reclaimable mapping | NO; scope-02 never cites the :108 refusal list (F2) |
| Row schema (envelope, projection, `stage.activity`, `agentWait`, liveness, paging) | open question 1 defers to `orca-capabilities.md` | open questions 1-2 left open | answers them from captures lc16/lc17/lc01/step7 | NO; 05 never names scope-02, scope-01 open question 1 does not point at 05 or scope-02 (F3) |
| Command name `orca-ide orchestration worker-list` | n/a | tables and Summary lead with `orca-ide worker-list` / `orca worker-list`; a CODE-CONTRADICTED note was added in the body only | uses the correct name | PARTIAL; correction did not reach scope-02's Summary or research-notes line 168 (F3) |
| WC-10 (absence is never death), WC-6 (retry is a new Task) | defined with contract lines | used for `unverifiable` handling | used in liveness mapping | YES, both cite the contract |

### Findings

**F1 — IMPORTANT (item 5, contradiction).** "finished" and "idle" mean different things in different files and no file points at the others.
- 05's classifier table defines idle as a settled Orca row whose `resource.terminalState` is retained or released. research-notes Section C (lines 184-193) defines idle as a person-started session with no Orca Task. scope-02 has no idle class.
- 05 marks a row finished from `outcome` alone. scope-01 (contract `:122-129`) and notes Section C require the return contract to be read and admitted first. scope-02 uses outcome plus settled.
- Why it matters: the sweep's class vocabulary is the core Phase 1 output; a synthesis that takes 05's table as written would report unread workers as finished and settled Orca rows as idle.
- Remediation: 05 should rename its "idle" row (for example "settled, resource retained") and cite notes Section C; 05 and scope-02 should state that their "finished" is only the Orca half and cite `WORKER-CONTRACT.md:122-129` via scope-01. Synthesis must use the Section C vocabulary.

**F2 — IMPORTANT (item 5).** scope-02's safe-to-close rule (`reclaimable` + `nextAction release`, repeated in its Summary at line 230) does not cite the five refusal conditions in `WORKER-CONTRACT.md:108` that scope-01 records. Notes Section C reconciles the two, so the synthesis input is correct, but scope-02 read alone gives an unsafe rule for a close decision.
- Remediation: add one sentence to scope-02's classifier and Summary: "Orca `reclaimable` + `release` is necessary, not sufficient; all five refusal conditions in `WORKER-CONTRACT.md:108` (scope-01) must also be clear."

**F3 — IMPORTANT (item 5).** The Orca row-schema work is split across scope-02 and 05 with no link between them.
- 05 answers scope-02's open questions 1 and 2, but never names scope-02; scope-01's open question 1 points only at `orca-capabilities.md`.
- The command-name correction (`orca-ide orchestration worker-list`; top-level `orca-ide worker-list` prints "Unknown command: worker-list", re-checked with `--help` only) did not reach scope-02's Summary or research-notes line 168 (`orca-ide worker-list --include-remote --json`).
- Remediation: add "answered by 05" against scope-02 open questions 1-2 and scope-01 open question 1 (or record it in the gaps log); correct the command name in research-notes line 168 and scope-02's Summary.

**F4 — MINOR (item 4, notes staleness).** research-notes records stale facts about the research files: line counts on line 9 (147/220/197 vs actual 152/235/200), "no Summary heading" for scope-01 at lines 235-238 (it has `## Summary` at line 150), and 05 as MISSING at line 215.
- Remediation: update the notes or record the corrections in the gaps log before synthesis reads them.

**F5 — MINOR (item 1, coverage).** Four sources are cited but not investigated by any assigned file: `skills/ccsession-tag/README.md` (named at scope-01 :112 only), `CR-01` under `.dev/orca-command-refactor/changes/` (AMBIGUITY 11 depends on it), `APPROVED.md` (notes say "not read by any scope") and the seed brief (input, cited only by the notes). scope-01's "Files read" table also omits `install_core.py`, `tests/commands/test_help_command.py` and the root `CLAUDE.md`, all of which it cites (for example `install_core.py:27` at line 26).
- Remediation: list these as known coverage gaps for synthesis, read CR-01 before resolving AMBIGUITY 11, and add the three omitted files to scope-01's table.

**F6 — MINOR (citation precision).**
- 05 answer (4) cites `--pairing-code`/`--environment` at `[H:worker-list] 3, 9-14`; they are at lines 10-11 and line 3 does not contain them.
- scope-02 cites the lc17 attention block as `:162-165`; the block is 161-166.
- 05's declared read range for `orca-capabilities.md` (lines 9-20 and 110-130) does not match what it cites (`:8`, `:10-21`, `:97-102`).
- scope-01's Summary tag counts (54/12/4) are not reproducible by Grep, and its heading "F1-F12" is stale (F1-F14 plus S1-S5 now).
- Remediation: correct the line numbers; state the counting rule or drop the counts; rename the heading.

### Claims checked and holding (evidence for the non-findings)

- Every scope-01 contract quote listed in item 1 matches `WORKER-CONTRACT.md`.
- 05: help is 22 lines with flags at 13-16 and notes at 19-22; worker-show help is 16 lines with `agentWait` on line 16; all capture ranges (lc16 projection 109-160, terminal 161-181, observation 182-186, terminalResource 187-207; lc17 nextAction 152-160, attention 161-166, preview 182, agentWait 187/192, status 190; lc01-step7 workers `[]` at :28, counts :29-31, page :32-37, scope :38-41) are correct; the 16-field projection count is correct; lc16 `dispatch.assigneePaneKey` (:12) equals `tabId:leafId` (:169-170).
- scope-02: remote flags at help lines 10-11 are correct; lc17 resource 145-151 with `reclaimable` at :150 and `activity` "working" at :132 hold. Its "unrelated hits for projection" line is tagged UNVERIFIED and could not be checked further; it is not a finding.

---

## Compiled gaps (assigned files only)

### Critical (block synthesis)
- None.

### Important (affect quality)
- Conflicting "finished" and "idle" definitions (F1): 05, scope-02 vs scope-01 and notes Section C.
- Safe-to-close rule in scope-02 omits the :108 refusal conditions (F2).
- Missing cross-references between scope-02, 05 and scope-01 open question 1; stale command name in notes line 168 and scope-02's Summary (F3).

### Minor (notes; do not block synthesis)
- Stale research-notes facts (F4); cited-only sources and incomplete files-read table (F5); citation imprecision and tag counts (F6).
- Open questions still open in the files themselves: `runtime_unavailable` exit code and JSON shape (scope-02 open question 3, UNVERIFIED); remaining items in 05 `## Gaps and Questions`.

---

## Summary

3 files analyzed; items 1 and 4 pass apart from minor gaps; item 5 fails. Findings: 0 CRITICAL, 3 IMPORTANT (F1-F3), 3 MINOR (F4-F6). No research file was edited.

## Verdict: FAIL
