# Phase 2 Correction Verification

**Date:** 2026-10-23
**Purpose:** Prepared assignment instructions, not a verification result
**Governing source:** Task skill Verification Round and Standard QA Report Output Format
**Task root:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/
**Launch condition:** Parent confirms actual correction application complete and research writers stopped. Not authorized to begin before that condition.

## Shared Independent Verification Contract
You are a FRESH independent verifier that did not produce the research, consolidate findings or propose/apply fixes. Assume mistakes remain or corrections caused regressions. fix_authorization:false. Read the live correction targets and primary evidence, not just the fix log's claims. Check (a) every relevant original finding and enumerated subcheck is resolved, (b) edits are correct with no garbled/lost meaning, (c) no new issue was introduced, (d) previously passing checks remain true. Any real issue of any severity gives FAIL; no conditional passes, no invented quota findings. Zero findings requires a concrete tool-backed Self-Audit.

This is one partition of a targeted correction-verification round, not a new full review panel or a new task phase. Six contexts provide one structural and one content verifier for each existing a/b/c partition, each with at most five target files. Supporting sources outside the assigned group may be inspected, but do not silently claim complete verification of other partitions. No target edits, fixes, task boxes, production changes, original log/package changes, extra agents/gates/debate, tests, Git, moves/archive/delete or external publication. UV only for Python and bounded original-log extraction; no giant parent investigation log or full debate/base/score bodies. Honest unavailable historical evidence stays explicit, not fabricated.

## Scope and Original Checks
Read phase-outputs/reviews/phase2-review-dispatch.md for exact a/b/c target lists and relevant actual task acceptance paragraphs. Read qa/qa-phase-2-consolidated-findings.md IN FULL, qa/qa-phase-2-fix-log.md, actual applied-patch evidence/citation mappings if present, and the initial lens reports for your assigned type/partition. Read governing Task report/verification templates and your prewritten output stub before gathering findings.

| Partition | Relevant consolidated findings (all subchecks mandatory) |
|---|---|
| a | P2-F01, P2-F02, P2-F08, P2-F09 |
| b | P2-F03, P2-F04, P2-F05, P2-F10, P2-F11 |
| c | P2-F06, P2-F07, P2-F12, P2-F13, P2-F14 |

Both verifier types must check resolution of ALL findings relevant to their partition, not only their original lens. Structural emphasis: section/list/summary conformance, all named omissions, factual correction, real references and no lost content. Content emphasis: faithful causal dispositions, original validity, counterevidence, observation/criterion shifts, reviewer identities, historical/current boundary, research-only scope and no distortion.

Also re-evaluate each original PASS check in your assigned original type/partition: structural initial reports use qa/qa-structural-phase2-*-<partition>-report.md; content reports use qa/qa-content-phase2-*-<partition>-report.md. Preserve the consolidation's original stable IDs P2.C0.Rxx.Cn when reporting current cycle-1 outcomes. Its inventory maps every report key to source report and original check numbers. Do not rewrite the initial reports or erase their FAILs. Explicitly identify any original PASS check now FAIL, with original check ID, target and evidence; parent applies the regression guard before monotonicity/cap. An additional newly found defect must be separately identified, with whether it changed after the correction or was previously missed stated only when evidence establishes that distinction. Check actual Markdown/citation meaning, not merely marker presence.

## Required Result
Agreed output: qa/qa-phase-2-verification-<structural|content>-<a|b|c>-report.md. Use Task Standard QA Report Output Format, with binary verdict, each original finding/subcheck disposition and evidence, preserved-PASS/current-FAIL table, all new issues, failed lookups/limits and a clean-result Self-Audit. This is cycle 1 unless parent explicitly supplies a later cycle. A group is not resolved while any listed subcheck remains unmet. Do not infer overall gate PASS from your partition result or from the producer's success claim.

If writing your own report is permitted, populate its existing stub incrementally and return ONLY path, literal VERDICT: PASS/FAIL, unresolved/new/regressed-check counts and at most two summary lines. If higher-priority rules prohibit report writes, do not bypass them: return the complete template-shaped report ONLY in final assistant text starting '# QA Report', never SendMessage body. Parent will persist exact final text directly from the transcript into the prepared stub and independently consume the disk report. Never claim a disk write you did not perform. Quoted placeholder syntax inside evidence or a check description is data, not automatically an unfinished report sentinel; actual unresolved report placeholders remain failures.
