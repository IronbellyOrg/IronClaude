# Fix log: task-file validation A.10 (findings F1-F7)

**Status:** Complete
**Date:** 2026-11-07
**Target:** TASK-RESEARCH-bmad-first-use-20261107-075901.md (only file edited besides this log)
**Input:** qa/qa-task-validation-consolidated.md

---

## F5 (Step 2.1 OBSERVED RUN)
- Step 2.1: struck the OBSERVED RUN clause (scratch dir, scratch HOME, `bmad install`). Replaced with EXISTING-INSTALL EVIDENCE: read this worktree's `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` as the observed output of a real install; rows tagged OBSERVED-FROM-EXISTING-INSTALL or UNVERIFIED; no installer command run. Scope guard sentence ("two optional scratch directories") and the verification clause of Step 2.1 updated to match.
- Open Questions item 3: rewritten from the builder decision about the observed run to an evidence-limit note; fresh-install-only facts stay UNVERIFIED and go to report Section 9.
- Key Constraints: added a NO INSTALLER RUN bullet.
- Steps 3.5 and 3.10: added "run NO installer command" to the fix agent scope guard and the gap researcher scope guard.

## F6 (Execution Context)
- References: removed `Dockerfile.coder:133-144` from the GOAL line (replaced by a description of the wrapper); GOAL label no longer says "verbatim".
- Source areas: added `.github/workflows/` and `docs/`, `README.md`, `CHANGELOG.md`, `SECURITY.md` (and `docs/generated/PROJECT_INDEX.md`) as named areas.

## F3 (Step 3.5 gap researchers)
- Step 3.5: embedded a complete GAP RESEARCHER PROMPT (Incremental File Writing Protocol, Documentation Staleness Protocol, scope guard, placeholders <GAP>, <TARGET FILE>, <FILES TO INVESTIGATE>). Step 3.10 carries the same prompt with "fix cycle 2".

## F1 (cycle-2 items, full prompt inline)
- Step 3.10 (fix cycle 2 agent): done, full prompt inline (copied from 3.5 with cycle-2 substitutions and the LAST fix cycle sentence).
- Step 3.11: done (copied from 3.6, cycle-2 paths).
- Step 3.12: done (copied from 3.7, cycle-2 paths).
- Steps 5.14, 5.15, 5.16 (Gate 2 cycle 2): done, full prompts inline (copied from 5.9, 5.10, 5.11, cycle-2 paths and LAST fix cycle sentence).
- Step 6.6 cycle-2 items (three: fix agent, rf-qa verification, rf-qa-qualitative verification): done, full prompts inline (copied from the 6.5 fix item and the two 6.6 cycle-1 verification items).
- Step 6.7 cycle-2 items (three: fidelity fix agent, structural verification, content verification): done, full prompts inline.
- Step 6.7b cycle-2 items (three: anti-omission fix agent, structural verification, content verification): done, full prompts inline.
- Total 15 items now carry full prompt text; Grep for "EXACTLY the", "embedded in Step" and "above, changing only" returns no match. Embedded prompt count went from 44 to 61 (44 + 15 + 2 new F7 agent items).
- Builder note 3: the sentence defending "EXACTLY the cycle-1 prompt" was deleted; the rest of the note (explicit fix-cycle items) is kept and now says every cycle-2 item embeds its complete prompt. The note was reworded, not removed, so note numbering and references stay stable.

## F2 (Gate 3 lens N)
- Steps 6.2, 6.3, 6.4 (seven lens items: template-conformance, internal-consistency, evidence-quality, actionability, domain-accuracy, crossref-chain, finding-reproducibility): each ADVERSARIAL STANCE sentence now carries the rule inside the prompt: "First compute N yourself: Grep pattern `^` output_mode count on the report path above, N = larger of 5 and line count / 100 rounded up; write N at the top of your report." The paragraph under Step 6.2 is now informational only.

## F4 (staging order)
- Old Step 7.2 (staging) removed from its position. Phase 7 is now: 7.1 verify, 7.2 present summary, 7.3 task summary, 7.4 mark Done, 7.5 stage `.dev/tasks` (new position, last file-writing item, staging only, no commit, checks that no `??` or unstaged ` M` entry remains under `.dev/tasks/`, re-stage if logging edits the task file), 7.6 non-blocking suggestion. Reference in the Task Summary comment updated to Step 7.3; Step 7.3 text no longer mentions a scratch `bmad install`.

## F7 (Gates 4 and 5 now 3 agents each)
- Step 6.7 (Gate 4): heading and intro say 3 rf-qa fidelity agents; partition by research file: agent 1 = research 01, 02; agent 2 = research 03, 04 (startup.sh, ~/.claude, superclaude, tests 57/46/19/49/52); agent 3 = research 05 (test-startup-boot.sh, README files, manifest welcome text, owner-decision documents, docs/). New item for agent 3 writes qa/qa-source-fidelity-report-3.md. Agent 2 prompt trimmed to its slice. Consolidation item reads all three reports and three verdicts; Gate 4 decision item reads three verdicts.
- Step 6.7b (Gate 5): heading and intro say 3 rf-analyst agents over the 12 input files: agent 1 = research 01, 02 + synth-01, synth-02; agent 2 = research 03, 04 + synth-03 + gaps-and-questions.md; agent 3 = research 05, web-01, web-02 + synth-04. Every file is in exactly one slice. New item for agent 3 writes qa/qa-anti-omission-report-3.md. Consolidation item reads all three reports; Gate 5 decision item reads three verdicts.
- Counts updated: Task Overview ("3, 3, 7, 3 and 3 report-only agents"), Key Objective 6, Key Constraints (Gate 4 = 3 rf-qa, Gate 5 = 3 rf-analyst, with the reason), builder notes 2, 4, 5, new note 12 (91 checklist items, was 89). Grep count of unchecked items is 91.
- Fix and verification items did not name the agent count, so they needed no change other than the F1 inlining.

## Notes
- Two mistaken tool calls happened during the work: one Edit with a placeholder replacement string that failed to match, and one Edit on a non-existent path. Neither changed any file (verified by Grep for the placeholder: 0 hits).
- Not touched: all minor findings (completion-gate sentences on Steps 1.1, 1.2, 7.x items, ADVERSARIAL STANCE on fix agents, web-agent staleness clause, relative paths, etc.), per the instructions.
- Nothing outside the task file and this log was edited. No commit, push or staging was done.
