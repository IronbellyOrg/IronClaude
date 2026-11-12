# Synthesis Quality Review: Accuracy (Partition 1 of 2)

**Date:** 2026-11-07
**Analyst:** rf-analyst (synthesis-review, checklist items 1-5), fix_authorization false, report-only
**Assigned synthesis files:** `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`
**Research files checked against:** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `research/07-gate-gap-fill.md`, `research/research-notes.md`, `research/web-01-agent-supervisor-session-health.md`, `research/web-02-static-status-report-conventions.md`, `gaps-and-questions.md`, `qa/qa-nb4-fix-log.md`
**Template source:** task file Steps 5.1-5.3 (lines 206, 210, 214) define the expected section headers and table columns for Sections 1-5.
**Severity rule:** CRITICAL and IMPORTANT block; MINOR are notes.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

---

## Executor-requested re-check: NB-4 allowlist

**Result: PASS. No synthesis text in this partition uses the old allowlist.**

Method: grep of all three assigned files for `inbox`, `task-list`, `run-list`, `run-current`, `gate-list` and `allowlist`, then a Read of each hit in context.

| File:line | What it says | Corrected allowlist? |
|---|---|---|
| `synth-01:185-193` | Allowlist table lists task-list, run-list, run-current and gate-list as allowed plain reads | Yes |
| `synth-01:281` | Lists the allowed read verbs; inbox forbidden (GQ-46) | Yes |
| `synth-02:7` | Notes that `gaps-and-questions.md:125` reads Open 75 / Resolved 25 after the NB-4 fix | Yes (current) |
| `synth-02:21-33` | Data-source table includes task-list, run-list / run-current and gate-list | Yes |
| `synth-02:112` (SC-2) | Read-only allowlist; inbox forbidden | Yes |
| `synth-02:132` (3.3 Constraints) | Same allowlist; inbox forbidden | Yes |
| `synth-02:230` | GQ-03 gap row marked resolved | Yes |

Source agreement: `research/research-notes.md:171-174` and `qa/qa-nb4-fix-log.md` carry the same allowlist. Partition 2 files (`synth-04:18`, `:34`; `synth-05:9`; `synth-06:11`) also agree; noted for the merge, not reviewed here.

Related defect: `synth-01:201` repeats the pre-fix GQ counts. This is not an allowlist error but a stale-count error; see Issue 1.

---

## Per-File Review

### synth-01-problem-current-state.md (299 lines, read in full)
**Sections covered:** title and metadata (1-9), 1. Problem Statement (13), 2. Current State Analysis 2.1-2.6 (21 onward)
**Verdict:** FAIL (1 IMPORTANT, 1 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 1 | Section headers match template | PASS | `## 1. Problem Statement` (13) with The question / Why it matters / Trigger; `## 2. Current State Analysis` (21) with 2.1-2.6, ending in a Current State Summary (diagram + table) |
| 2 | Table column structure correct | PASS | Area / Exists / Missing / Tag summary tables suit Section 2 (no gap table is expected there); allowlist table at 185-193 is well formed |
| 3 | No fabrication | **FAIL** | `:201` states the counts at `gaps-and-questions.md:125` read "Open: 76. Resolved: 24" and are "off by one". The file now reads "Open: 75. Resolved: 25 ... Open blocking QA finding: none" (re-read this session). The claim is stale and misquotes its own citation (Issue 1). MINOR: metadata class list at `:5` omits "fenced", while `:15` and `research-notes.md:188` include it (Issue 2) |
| 4 | Findings cite paths and evidence | PASS | Each 2.x subsection ends with an **Evidence:** line (63, 117, 158, 226, 246, 298) carrying file:line citations |
| 5 | Options analysis (>=2 options) | N/A | No options analysis in Sections 1-2. A4 appears only as a rejected [CODE-CONTRADICTED] option (`:143`), which is correct |

Spot-checks that hold: tallies at `:61` (54/12/4), `:224` (58/3/3) and `:244` (3 CONTRADICTED, 0 UNVERIFIED) match the research files; scope-01 contract citations; research-notes Section C precedence (7 rules); scope-03 registry and handler lines; `07-gate-gap-fill` 35-94 citations; scope-04 #409 layout at `495eb96d`; `:201`'s second claim (scope-03 still writes bare verbs, `qa-nb4-fix-log.md:41`) is accurate.

### synth-02-target-gaps.md (317 lines, read in parts)
**Sections covered:** metadata (1-8), 3. Target State (3.1 desired behavior, 3.2 SC-1 to SC-16 at 109-126, 3.3 constraints at 130-144, external context 148-159), 4. Gap Analysis
**Verdict:** PASS

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 1 | Section headers match template | PASS | `## 3. Target State` (12) with 3.1-3.3 and External context; Section 4 gap tables follow |
| 2 | Table column structure correct | PASS | Gap tables use Gap / Current State / Target State / Severity / Notes; SC table carries criterion, check method and source; external table carries finding, implication and URL |
| 3 | No fabrication | PASS | `:7` correctly quotes Open 75 / Resolved 25; `:65` records the six-versus-seven class contradiction and keeps fenced; web-02 rows (155-159, 289, 317) match `web-02` lines 17-63 (Icinga, Statuspage, Grafana, Kanban, `gh issue list`, I-PASS, PagerDuty, all with matching URLs); SC-9 cites web-02 recommendation 1 (`web-02:57`), correct |
| 4 | Findings cite paths and evidence | PASS | SC rows and gap rows carry file:line or research-file citations; external rows carry URLs |
| 5 | Options analysis (>=2 options) | N/A | No options analysis; A4 appears only as a rejected constraint row (`:144`) |

### synth-03-external-findings.md (230 lines, read in full)
**Sections covered:** 5. External Research Findings, 5.1-5.10 (findings, 5.9 contradictions D1-D6 / C1-C2, 5.10 key findings map, R1-R9, L1-L2)
**Verdict:** PASS (2 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 1 | Section headers match template | PASS (MINOR note) | `## 5. External Research Findings` matches the template. Precedence, Inputs and Research question context lines (3-9) are present, but there is no `#` title or date line as in `synth-01:1-9` and `synth-02:1-8` (Issue 3) |
| 2 | Table column structure correct | PASS | Contradiction table (D/C rows with source URLs and resolution), key-findings map (source / finding / section), R and L tables |
| 3 | No fabrication | PASS (MINOR note) | All web-01 claims checked against `web-01:133`, `:177-229` (URLs, relevance, Kubernetes 50 s / 40 s note, D1-D4, key findings 1-7, recommendations 1-6). web-02 claims (5.4 Icinga/Nagios/Grafana, 5.6 Statuspage, 5.7 SRE/I-PASS/PagerDuty, 5.8 Kanban/`gh`, key-findings rows 200-205, C1) match `web-02:16-63`. Class list at `:7` omits "fenced" (Issue 2) |
| 4 | Findings cite paths and evidence | PASS | Every [EXTERNAL] finding has a Source URL and a Relationship line; codebase cross-references are marked "as cited by web-01/web-02" |
| 5 | Options analysis (>=2 options) | N/A | No options analysis; A4 appears only as a rejected note (`:185`) |

Not re-verified by this analyst (recorded, not a defect): `synth-03:85` cites `research/scope-02-orca-recovery.md:239` for the `unscanned:` markers, carried over from `web-01:141`. The web-01 citation matches; the scope-02 line itself was not re-read. [UNVERIFIED-by-analyst]

---

## Issues Requiring Fixes

| # | File | Check | Severity | Issue | Required Fix |
|---|---|---|---|---|---|
| 1 | `synth-01-problem-current-state.md:201` | 3 | IMPORTANT | States that `gaps-and-questions.md:125` reads "Open: 76. Resolved: 24" and is off by one. The cited line now reads "Open: 75. Resolved: 25 ... Open blocking QA finding: none". The claim misquotes its citation and contradicts `synth-02:7` (and `synth-06:226` in partition 2) | Replace the sentence with the current state (Open 75 / Resolved 25, no open blocking QA finding), or delete it. Keep the second half about bare verbs (`qa-nb4-fix-log.md:41`). Cross-partition: `synth-04:220` (X-6) carries the same stale claim |
| 2 | `synth-01:5`, `synth-03:7` | 3 | MINOR | Metadata class lists omit "fenced"; `synth-01:15`, `synth-02:65` and `research-notes.md:188` include it | Add "fenced" to both lists |
| 3 | `synth-03:1` | 1 | MINOR | No `#` title or date line, unlike synth-01 and synth-02 (Inputs and context lines are present) | Optional: add a title and date line for consistency |

---

## Summary

- Files reviewed: 3
- Files passed: 2 (synth-02, synth-03)
- Files failed: 1 (synth-01)
- Total issues: 3
- Blocking issues (CRITICAL or IMPORTANT): 1 (Issue 1, IMPORTANT)
- MINOR notes: 2
- NB-4 re-check: PASS; no synthesis text in this partition uses the old allowlist; inbox is still forbidden everywhere it is mentioned.

## Verdict: FAIL
