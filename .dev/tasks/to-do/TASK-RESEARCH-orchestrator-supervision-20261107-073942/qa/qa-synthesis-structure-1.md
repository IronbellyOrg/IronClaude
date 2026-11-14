# QA Report — Synthesis Gate, structure lens (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 for issue #339 (`/sc:sweep`, WC-14, #409 report)
**Date:** 2026-11-07
**Phase:** synthesis-gate (structure lens, checklist items 1-6)
**Fix cycle:** N/A
**Fix authorization:** false (report only; no synthesis file modified)
**Assigned files:** `synthesis/synth-01-problem-current-state.md`, `synthesis/synth-02-target-gaps.md`, `synthesis/synth-03-external-findings.md`
**Extra executor checks:** (1) NB-4 allowlist correction carried into the synthesis; (2) `research/web-02-static-status-report-conventions.md` treated as a normal research source.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL (1 blocking finding)

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match the Report Structure template | PASS (with notes) | Template read at `~/.claude/skills/tech-research/SKILL.md:1330-1389`. synth-01: `## 1. Problem Statement` (:13) with The question / Why it matters / Trigger bullets; `## 2. Current State Analysis` (:21) with 2.1-2.5, each followed by an `**Evidence:**` line (:63, :117, :158, :226, :246), ending with `### 2.6 Current State Summary` (:248). synth-02: `## 3. Target State` (:12) and `## 4. Gap Analysis` (:165). synth-03: `## 5. External Research Findings` (:1), 5.1-5.9, ending with `### 5.10 External Research Summary` (:187). Deviations are format only (M1, M2). The `#`/`##` lines at synth-02:74-83 are inside a code fence (fences at :73 and :85), so they are not stray headers. |
| 2 | Table column structures | PASS | All six gap tables in synth-02 (:177, :194, :203, :228, :238, :261) use Gap / Current State / Target State / Severity / Notes (:238 adds "(claim)" / "(correction)" qualifiers, same five columns). No Options or Implementation tables in this partition. |
| 3 | No fabrication (claims trace to research files) | FAIL | One false claim: synth-01:201 (B1). Claims checked and found sourced: every URL in synth-02 and synth-03 appears in web-01 or web-02 (Bash loop over all URLs, every count >= 1; the only zero-count URL is the issue link in synth-01); 100000 of 118034 characters (web-01:62, :216); 50 s grace period and the 40 s inconsistency (web-01:133; web-02:27); 300 s toleration "search result only" (web-01:136, :218); Nagios KB id=72 "should generally NOT be reported as UNKNOWN" (web-01:147, :182); Icinga plugin timeout reports UNKNOWN (web-02:23); I-PASS 403 (web-02:35); seven classes and precedence rules (research-notes.md:188-214); the 6 h activity-only window and the 72 h crash-recovery default (research-notes.md:221); A4 cons (research-notes.md:160); `SKILL.md:4`, `:25-27`, `:53` path claims (scope-02:130-133); `bootstrap_scan.sh` :31 encoding, :73 `.git` file, :136 JSON escaping (scope-02:146-148); `parse_session_log.py` :31-40, :45-55, :85-102 (scope-02:154-156); contract 203 lines (`wc -l` = 203; scope-01:14); 41 test functions (`grep -c` = 41; scope-01:100); `NEVER_AS_WORKER` 8 entries named "all seven" (gaps-and-questions.md:35); GQ-46 inbox row (gaps-and-questions.md:69). |
| 4 | Evidence citations use actual file paths | PASS | Each 2.x Evidence line in synth-01 names full repo paths with line ranges and the research file it came through. synth-02 rows cite `scope-0N:line`, `research-notes.md:line` or `gaps-and-questions.md:line`. synth-03 findings each carry a `Source:` URL (26 Source lines for 26 findings, Bash label count). |
| 5 | Options analysis (2+ options with pros and cons) | N/A | No Options section in this partition (headers listed in check 1). Option A4 appears only as a rejected-option gap row (synth-02:144), which traces to research-notes.md:160. |
| 6 | Implementation plan names specific files | N/A | No Implementation Plan section in this partition (headers listed in check 1). |
| X1 | NB-4 re-check (executor extra 1) | PASS | See the NB-4 section below. |
| X2 | web-02 used as a normal source (executor extra 2) | PASS | web-02 claims used in synth-03 (Icinga :23, Nagios :25, Kubernetes :27, I-PASS :35) match the file. |

## NB-4 Re-check (executor extra 1)

Source of truth: `research/scope-03-cli-patterns.md:99` (allowlist now names `task-list`, `run-list`, `run-current`, `gate-list`; `inbox` forbidden with the read-marking reason) and `qa/qa-nb4-fix-log.md` (3 edits).

| Synthesis location | Text | Result |
|---|---|---|
| synth-01:7 | Allowlist "now includes `orchestration task-list`, `run-list`, `run-current` and `gate-list`; `inbox` stays forbidden" | Corrected form |
| synth-01:185-193 | Allowed column holds worker-list/show/read, `worktree ps` without `--agent-wait`, task-list, run-list, run-current, gate-list; Forbidden column holds `inbox` with the [UNVERIFIED] read-marking reason | Corrected form |
| synth-01:281 | "run-list, run-current, task-list and gate-list allowed (NB-4)"; "`inbox` forbidden (GQ-46)" | Corrected form |
| synth-02:7, :230 | NB-4 fixed; four verbs allowed; `inbox` forbidden | Corrected form |
| synth-02:19-29, :112 (SC-2), :132, :216 | Data sources include the four verbs; SC-2 fails the test on `inbox`; constraints and GQ-46 row keep `inbox` forbidden | Corrected form |
| synth-03 | No allowlist text (Grep `inbox|allowlist` returned no synth-03 line) | N/A |

Grep for `inbox|allowlist` over all three files found no text that uses the old allowlist (no row that omits the four verbs, no row that allows `inbox`). NB-4 is carried correctly. The only NB-4-related defect is the stale count sentence at synth-01:201 (B1), which is about the gaps register summary, not the allowlist.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | IMPORTANT (blocking) | synth-01:201 (section 2.4, after the allowlist table) | False claim. It says `gaps-and-questions.md:125` reads "Open: 76. Resolved: 24" and that those counts "predate the fix and are off by one". The file actually reads "Open: 75. Resolved: 25 ... Open blocking QA finding: none; GQ-03 (NB-4) was fixed" (Grep on gaps-and-questions.md:125). The register (mtime 20:23:08) was updated before synth-01 was written, so the sentence was already wrong. It also contradicts synth-02:7 and synth-02:230, which state the correct 75/25, so the assembled report would contradict itself. | Replace the sentence with: "`gaps-and-questions.md:125` now reads Open: 75. Resolved: 25, with no open blocking QA finding." Or delete the off-by-one clause. Keep the rest of :201 (the bare-verb note citing `qa/qa-nb4-fix-log.md:41` is correct). |
| M1 | MINOR | synth-02:12-163 | Template section 3 uses three bullets (Desired behavior / Success criteria / Constraints, SKILL.md:1360-1362). synth-02 uses subsections `### 3.1`-`### 3.3` with tables. Same content, different form. | Optional: keep, or let the assembler note the form. |
| M2 | MINOR | synth-03, all 26 findings | Template field is "Relationship to codebase:" (SKILL.md:1386); synth-03 uses "Relationship:" (26 times) and adds a "WC-10 / read-only:" field. Relevance values are all HIGH/MEDIUM/LOW (15/9/2), as required. | Optional: rename the label at assembly. |
| M3 | MINOR | synth-03:230 (source reliability note) | Lists the partial fetch of the Kubernetes probe page but omits that the node-status page was also fetched only in part ("first 100000 of 100733 chars", web-01:217). | Add the node-status page to the partly-fetched list. |
| M4 | MINOR | synth-02:172 (R-2) and the Critical rows in 4.2 | R-2 adopts the C8 "unwired capability = Critical" rule, but C8 (SKILL.md:1374) also asks that such a gap carry or link a remediation task; synth-02 has no link (Grep `remediation|.dev/tasks/to-do` returned nothing). C8 strictly targets spec-named shipped capabilities, and these are planned builds, so this is a note; the Section 8 plan in the other partition should map each R-2 row to a step. | Cross-partition: confirm at merge that every R-2 Critical row has a Section 8 step. |
| M5 | MINOR, [OUT-OF-SCOPE] | research/scope-02-orca-recovery.md:241 | Research file (not assigned) attributes the `.git`-is-a-file bug to ":31, :73" and path encoding to ":136", while its own detail lines :146-148 put encoding at :31, the `.git` bug at :73 and JSON escaping at :136. synth-02:144 follows the correct detail lines. | None for the synthesis; noted for the research owner. |

## Summary

- Checks passed: 5 of 6 assigned checks (1, 2, 4 pass; 5 and 6 N/A with header evidence), plus both executor extras (X1, X2)
- Checks failed: 1 (check 3, no fabrication: B1)
- Blocking issues: 1 (CRITICAL: 0, IMPORTANT: 1)
- Minor notes: 5 (M1-M5; M5 is out of scope)
- Issues fixed in-place: 0 (fix_authorization false)

## Actions Taken

None. Report only; no synthesis or research file was modified.

## Confidence Gate

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Limitation on check 3:** claims were traced by targeted reads and greps of the cited research lines, not one by one for every sentence. Sampled sources: research-notes.md (Sections B and C), scope-01, scope-02, scope-03, gaps-and-questions.md, qa-nb4-fix-log.md, web-01, web-02, and every URL. Not re-traced line by line: the synth-01 section 2.5 #409 layout details (scope-04:330-373) and the synth-01 section 2.2 Orca capture details (05, 06). A false claim there would not be caught by this pass.
- **Tool engagement:** this segment: Read: 6 | Grep: 9 | Glob: 0 | Bash: 7. Earlier in the same run, before a context compaction: Reads of the task file (:230, :240), all three synthesis files, `qa/qa-nb4-fix-log.md`, `gaps-and-questions.md:1-130` and `research/scope-03-cli-patterns.md:60-215` (exact counts not retained). No web research was performed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).

## Recommendations

- Fix B1 in synth-01:201 before assembly, then re-run this gate for that line only.
- At partition merge, check M4 against the Section 8 plan.
- M1-M3 can be handled at assembly; they do not block.

## QA Complete

## Verdict: FAIL
