# Assembly Brief for the Phase 6 Assembler (coordinator-owned)

**Task:** TASK-TECHREF-orchestration-20261110-050239
**Date:** 2026-11-12
**Status:** Complete (coordinator decision record; not a synthesis output; not routed content)
**Origin:** Phase 5 synthesis gate, consolidated finding CB-13 (`qa/qa-synthesis-consolidated-findings.md`; reviewer `qa/qa-synthesis-structure-report-2.md` I-07) and the minor notes preserved there.

## Decision on the size ceiling (CB-13)

The five synthesis files total 2,161 lines after the Phase 5 executor gate fix cycle 1 (2,076 before the synthesis gate fixes and 2,083 after them; the estimate of about 1,980 lines after assembly in the first version of this brief no longer holds, about 2,060 now). The template's Heavyweight budget is 1,200 to 1,800 lines, and it calls more than 2,000 lines a code smell.

**Decision: waive the 1,800-line ceiling for this reference. The target is at most 2,000 lines after assembly; the Phase 5 executor gate fix cycle added content (coordinator lifecycle tables, owner-question consequences, recovery columns), so the synthesis total is larger than 2,083 and the assembler records the final line count and the reason in the Phase 6 gate findings rather than trimming evidence.**

Reasons (all evidenced in the gate reports):
- No reviewer found padding. The ten reports opened about 900 citation groups and found no fabricated path, function, constant or line number; the length comes from evidence per claim, three revisions kept apart (CHECKOUT, ORIGIN/MASTER, installed), and nine subsystems.
- The synthesis files carry about 225 lines that the assembler removes (five "Routing dispositions" tables, per-file legends, "(for the assembler)" blocks) and the template adds about 125 (front matter, Document Information, completeness checklist, table of contents), so the assembled size is about the same as the sum minus the removals plus the additions.
- Trimming evidence rows before assembly would risk the property the gates protect (every claim traced to a source), and the gate reports say the excess is mostly repetition that single-sourcing removes without losing a fact.

Binding instructions for the assembler:
1. Remove every "Routing dispositions" table and every block labelled "(for the assembler)" or "Contradictions, corrections applied and open items".
2. Keep one evidence-class legend (the one in `synth-01`, which splits INSTALLED-FILES and HOST-INSTALLED) and one installed-copy provenance matrix (`synth-02` 3.0.3). Replace the other copies with a pointer.
3. Single-source repeated content: the DEFECT statement lives in 8.2 (with a one-line pointer elsewhere); the depth default 1 against 2 lives in 5.5 and 9.3; the fail-closed qualifier lives in 10.3; script line counts stay in Section 1 "Key numbers" unless the count identifies a revision (the two `orca_worktree.py` versions).
4. Replace every body mention of "synth-0N" and "Section 3.3 above" with the real section number.
5. Emit numbered headings `## 6. State Management` and `## 7. Component Inventory` with the N/A rationale as their body.
6. Give bare file names their full repo-relative path once (`limit-selection.md`, `merged-requirements.md`, the developer guide).
7. Re-read moment-in-time git facts at assembly (`git status --short`, `git rev-parse --short origin/master`, `git rev-list --left-right --count HEAD...origin/master`, the per-file `cmp` of installed copies) and update every dated statement; three files already disagreed on them once.
8. If the assembled file still exceeds 2,000 lines, do not trim evidence silently: record the final line count and the reason in the Phase 6 gate findings.

9. Update the Phase 5 row of section 15.1 (it still says "verification of fix cycle 1 pending") with the gate's final result as recorded in the Phase Gate Findings of the task file; add the Phase 6 gate rows when each finishes.

10. Optional additions named by the Phase 5 executor gate (not required for a PASS, no new claim needed): one row in 5.1 "Human-ruling and approval gates" listing `WORKER-CONTRACT.md:229,233,221,108,246,57` (the coordinator's actions are conditioned on the person's instruction); state that the Overview has two or three paragraphs (the template limit) by merging the fourth; give the roughly 447 `research/0N`, `gap-P3-G0N` and `web-0N` citations a source key or replace them with the cited file:line; make the 2.2 subsystem names match the 5.N headings; move the DEFECT probe table into 8.2 before 5.3 is cut to a pointer; carry the five register A3 limits and the stale-documentation rows of the gap files that the minor notes of `qa/phase-5-completeness.md` (C-04, C-05) list; add the converted and non-converted command sets and the shim-diagnosis cause table if space allows.

The assembler must not change a verified fact, add a claim, or resolve an owner question (C1 to C19 stay questions; sub-orchestrator mode stays deferred; the future-role question and any installation rollout stay unresolved).
