# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** Fix reflect-wrapper marker leakage — strip SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE from §6.1 step 5.5 verification subprocess only
**Date:** 2026-06-11
**Phase:** task-integrity
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | B2 5-component completeness | FAIL | Read task file lines 155-240 and Template 02 research lines 159-166. Most items include context/action/output/verification/completion, but Step 4.10 and 4.11 omit a concrete absolute input set by using "all files changed by the fix agent" instead of restating the changed-file scope. |
| 2 | No reliance on prior-item context | FAIL | Step 4.10 and Step 4.11 depend on Step 4.9's dynamic results without restating the actual possible changed files or the report path contract inside the agent prompt (task lines 221-228). |
| 3 | Agent-spawning prompts fully embedded | FAIL | Steps 4.2-4.7 contain full lens prompts, but Step 4.9's fix-agent prompt uses relative/dynamic references (`qa-consolidated-findings.md`, `this MDTM task file`, `the sibling contract`, `qa-fix-agent-report.md`) and Steps 4.10-4.11 use "all files changed by the fix agent" (task lines 221-228). |
| 4 | Absolute path specificity | FAIL | Multiple checklist items/prompts use non-absolute/dynamic references: "this task file" (lines 201, 210), "modified source/test/contract files" (line 207), "the research files" (line 213), "this MDTM task file" and `qa-fix-agent-report.md` (line 222), and "all files changed by the fix agent" (lines 225, 228). |
| 5 | Measurable verification criteria | FAIL | Several agent-spawn verification clauses are measurable, but Step 4.10 and 4.11 cannot be measured against a fixed input scope because the changed-file set is not enumerated, and Step 4.14 requires determining whether failure is "solely because" of skill-load-path without a measurable diagnostic method (lines 225, 228, 237). |
| 6 | No batch / over-broad items | FAIL | Step 4.14 combines reading three sources, running the POST gate, capturing raw output, writing a summary, conditional sync/install, one rerun, and fallback acceptance evidence in one checklist item (line 237). This exceeds atomic B2 execution. |
| 7 | CODE-VERIFIED research grounding | FAIL | Step 4.14 says to read research/04 "for the skill-load-path caveat" (line 237), but research/04 lines 147-169 discuss POST self-recursion and staging caveats and do not substantiate a skill-load-path fallback. |
| 8 | TB-Add placeholder scan | PASS with note | Grep for `TBD|TODO|FIXME` returned no hits. Grep found `[To be completed by executor]` placeholders in Task Log lines 250, 253, 256, 259, 262, 265, 268; these are non-checklist task-log placeholders that Step 4.13 is intended to populate, so they are not a TB-Add-1 checklist-item failure. |
| 9 | TB-Add blocked/Open Questions adjacency | PASS | Open questions/operator-awareness are in lines 98-101; no checklist item is explicitly marked blocked by an open question, and each conditional failure path logs blockers to phase findings. |
| 10 | TB-Add Execution Context Source Areas | PASS | Source Areas are listed at lines 112-118. Grep confirmed each source area reappears in checklist contexts or agent-review scopes (e.g., lines 162, 167, 170, 173, 176, 198, 201, 213, 222). The Source Areas block contains absolute paths but no `path.py:NN` line citations. |
| 11 | Checklist format / item count | PASS | Grep count found 27 `- [ ]` items and 27 `**Step` headers; all checklist entries use `- [ ]`. |

## Summary
- Checks passed: 4 / 11
- Checks failed: 7
- Critical issues: 3
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:225` and `:228` | Step 4.10 and Step 4.11 are not B2 self-contained because they tell verification agents to read "all files changed by the fix agent". That is a dynamic prior-item dependency, not a self-contained absolute input set. | Replace the dynamic phrase with a bounded explicit list of possible absolute paths and instruct the agent to read `qa-fix-agent-report.md` only to determine which of those enumerated paths actually changed. |
| 2 | CRITICAL | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:222` | Step 4.9's spawned fix-agent prompt contains non-absolute and ambiguous file references: `qa-consolidated-findings.md`, `this MDTM task file`, `the sibling contract`, `runner.py`, `commands.py`, `process.py`, and `qa-fix-agent-report.md`. Agent prompts must be fully embedded and path-specific. | Rewrite the embedded prompt with absolute paths for the consolidated findings report, task file, sibling contract, forbidden Python files, and output report path. |
| 3 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:201`, `:210` | Steps 4.2 and 4.5 tell agents to review "this task file" rather than embedding the task file's absolute path inside the agent input list. The surrounding checklist item has the path elsewhere, but the spawned prompt/input scope itself is not self-contained. | Replace "this task file" with `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md` in both agent-spawn items. |
| 4 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:207`, `:213` | Steps 4.4 and 4.6 use broad input phrases ("the modified source/test/contract files", "the research files") instead of enumerating the actual absolute files the agents must read. This leaves scope interpretation to the executor. | Expand each phrase to the concrete absolute paths already known from Source Areas and research file inventory. |
| 5 | CRITICAL | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:237`; research support checked at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/research/04-conventions-contract-template.md:147-169` | Step 4.14 cites research/04 "for the skill-load-path caveat", but the cited research section discusses POST self-recursion, staging, and dogfood ordering; it does not provide a code-verified skill-load-path diagnostic or fallback contract. This violates the "act only on CODE-VERIFIED research" lens. | Either add code-verified research supporting skill-load-path resolution and diagnostics, or remove the skill-load-path fallback from Step 4.14 and rely only on the researched dogfood POST behavior. |
| 6 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:237` | Step 4.14 is a batch item: it performs POST gate execution, output capture, summary writing, conditional sync/install, rerun, and fallback acceptance-evidence generation. B2/A3 require atomic, verifiable checklist items. | Split into separate items: prepare/read POST prerequisites; run POST gate and capture output; if needed, resolve documented skill path issue; rerun once; write POST summary/fallback decision. |
| 7 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:237` | Step 4.14's verification criterion "if the gate exit-codes 11 solely because the subprocess loaded an unfixed installed skill path" is not measurable. It gives no command, log field, grep target, or artifact proving which skill path was loaded. | Add a measurable diagnostic: e.g., capture the resolved skill path from the subprocess or require a specific audit/log artifact/grep evidence before classifying the failure as skill-load-path-only. |
| 8 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:225`, `:228` | Step 4.10 and 4.11 prompts are less complete than Steps 4.2-4.7: they do not include the output report path inside the embedded prompt, and their input scope is partly outside the prompt in the checklist wrapper. | Make the prompt itself fully self-contained: include input files, output report path, fix_authorization, exact lens, and PASS/FAIL report requirements inside the backticked prompt. |
| 9 | MINOR | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/TASK-RF-reflect-marker-leak-20260611-175724.md:247-270` | Task Log contains template placeholders `[YYYY-MM-DD]`, `[To be completed by executor]`, and `[Yes/No]`. They are not forbidden `TBD/TODO/FIXME` tokens and are not checklist items, but they are still placeholder text that may confuse a literal placeholder scanner. | Optional: convert these to HTML comments or explicitly mark them as executor-fill templates to avoid false positives in stricter placeholder gates. |

## Actions Taken
- Wrote this QA report only.
- No task-file fixes applied because `fix_authorization: false`.

## Confidence
**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 11 | Grep: 5 | Glob: 0 | Bash: 5 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

Unchecked items: none.

Unverifiable items: none.

## Recommendations
- Must resolve all CRITICAL and IMPORTANT B2 self-containment issues before executing this task.
- Prioritize Steps 4.9-4.11 and 4.14: those are the weakest self-containment surfaces and most likely to cause execution drift or false QA confidence.

## QA Complete

VERDICT: FAIL
