# QA Report — Research Gate Gap Detection

**Topic:** Fix reflect-wrapper marker leakage into the §6.1 step 5.5 verification subprocess (strip marker for verification only)
**Date:** 2026-06-11
**Phase:** research-gate
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

Research is directionally strong and resolves the main `env -u`/verb-allowlist tension, but it is not gap-free. I found one formal inventory failure and two substantive gaps the task builder should fix before relying on this research.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory / status | FAIL | Read all four assigned files. `01`, `03`, and `04` state `Status: Complete`; `02-verification-envelope-surface.md` states `Status: In Progress` at line 3 and only later says `Status: Complete` at line 87, creating an unresolved status contradiction in a required research file. |
| 2 | Evidence density | PASS | Assigned files cite absolute paths and line/function evidence throughout: e.g. R1 lines 21-31 for `commands.py`, R2 lines 61-63 for §6.1.1 edit mechanics, R3 lines 121-125 for reflect CLI tests, R4 lines 56-61 for source-of-truth sync rules. I independently re-read the cited source sections. |
| 3 | Scope coverage | PASS with caveat | No `research-notes.md` exists in the research directory, so the canonical EXISTING_FILES cross-check was unavailable. Within the assigned scope, research covers marker flow, §6.1.1 verification envelope, regression-test surface, source-of-truth/sync conventions, contract §3, and POST-gate recursion. |
| 4 | Documentation cross-validation | PASS | Doc-sourced claims are tied to source paths/lines rather than untagged assertions. I spot-checked `src/superclaude/skills/sc-reflect-protocol/SKILL.md:489-502`, `src/superclaude/skills/task-builder/SKILL.md:2200-2205`, and `reflect-wrapper-contract.md:76-108`; the cited text matches the research. |
| 5 | Contradiction resolution | FAIL | R2 has a formal status contradiction (`Status: In Progress` and `Status: Complete`). No other substantive cross-file contradiction was found. |
| 6 | Gap severity review | FAIL | Research leaves gaps on proving no over-strip of legitimate nested-gate uses and on collision hygiene for the already-modified proposed test file. Details below. |
| 7 | Depth appropriateness | PASS | R1 provides an end-to-end marker leak chain from wrapper export → `ClaudeProcess.build_env()` inheritance → reflect skill verification grandchild → Click guard trip. |
| 8 | Integration point coverage | PASS | R2 identifies §6.1.1 as the fix surface and explicitly rejects Python audit/apply env scrubbing; R4 covers contract §3 and task-builder POST gate integration. |
| 9 | Pattern documentation | PASS | R4 covers Template 02 B2 item style, UV-only commands, sync-dev/verify-sync, `.claude/` staging prohibition, CI parity lint/format, and final POST-gate ordering. |
| 10 | Incremental-writing compliance | PASS with caution | Files are structured by research slice and contain detailed evidence blocks. R2's contradictory status line suggests it was edited incrementally but not cleaned up; this must be fixed before synthesis/task building. |

## Lens-Focus Findings
| Lens question | Result | Evidence |
|---|---|---|
| R2 `env -u` prefix vs §6.1.1 verb allowlist | COVERED | R2 lines 46-51 explicitly state raw `env -u` conflicts with control (b), and R2 lines 58-63 specify validation order: validate the base command against controls (a)/(b)/(c)/mutation gate first, then apply fixed protocol-authored `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <base command>`. This resolves the allowlist mechanism without adding `env` as a user verb. |
| Legitimate marker uses preserved | PARTIAL GAP | R1/R2/R4 correctly say do not strip audit or `/task` child marker (`runner.py` confirms marker export at lines 405-416 and 440-448), but R3's recommended verification command omits the existing marker-suppression tests, so the task would not prove the legitimate nested-gate suppression behavior still passes after the protocol change. |
| `make sync-dev` requirement | COVERED | R4 lines 56-61 and 160-162 require source-first edit, `make sync-dev`, and `make verify-sync`; this matches project source-of-truth rules. |
| POST-gate self-recursion | COVERED | R4 lines 147-154 and 162-169 specify the POST gate must run after the fix/tests/sync as a dogfood proof and must not be placed before the verification-strip fix. |
| Other docs quoting §3.2 / test-file collision | PARTIAL GAP | R4 covers the contract and task-builder POST pattern. I additionally found `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1042-1072` quoting the §3.2 skip guard; research does not say whether this quote needs no change. The proposed regression-test file is also currently staged-modified (`git status --short` reports `M  tests/cli/reflect/test_no_nesting_guard.py`), and research does not instruct the builder to inspect/rebase around that staged edit before appending another test. |
| Applies to all allowlisted verification tools | COVERED | R2 ties the strip to §6.1.1's `execute_shell_command` envelope, whose allowed base verbs are `{pytest, ruff, mypy, make, uv, npm, tsc, cargo}`; it is not pytest-only. |

## Summary
- Checks passed: 7 / 10
- Checks failed: 3
- Critical issues: 0
- Important issues: 3
- Minor issues: 1
- Issues fixed in-place: 0 (fix_authorization: false)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 13 | Grep: 0 | Glob: 0 | Bash: 7 | Tavily: 0 | Web fallback: 0

No checklist item remains unchecked. No item was treated as unverifiable; the missing `research-notes.md` was handled as a scoped caveat rather than a blocker because this invocation assigned an explicit four-file subset.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/research/02-verification-envelope-surface.md:3` and `:87` | R2 is internally inconsistent: it begins with `Status: In Progress` but later ends with `Status: Complete`. The research-gate file inventory requires each research file to be clearly complete. | Change the top status to `Status: Complete` or explicitly document why the file remains incomplete and what gap remains. Do not proceed to synthesis while the status is contradictory. |
| 2 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/research/03-test-design.md:239-243` | The recommended verification command runs the new content-contract test plus smoke/promote tests, but omits `tests/cli/reflect/test_marker_suppression.py`. That leaves the task without direct proof that legitimate nested-gate suppression still works after adding the verification-only strip. | Add `tests/cli/reflect/test_marker_suppression.py` to the required targeted pytest command, or add an equivalent explicit verification item that proves marker value `"1"` still suppresses real nested `superclaude reflect run` gates while the verification subprocess strip is limited to step 5.5. |
| 3 | IMPORTANT | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/research/03-test-design.md:206-243`; current git index | R3 recommends adding a test to `tests/cli/reflect/test_no_nesting_guard.py`, but the file is already staged-modified in this worktree (`git status --short` reports `M  tests/cli/reflect/test_no_nesting_guard.py`). Research does not warn the builder to inspect the existing staged diff before editing. This creates a collision/hijack risk with the other recent task's edits to the same file. | Add a task-builder note: before editing `test_no_nesting_guard.py`, inspect current staged/unstaged changes with `git diff --cached -- tests/cli/reflect/test_no_nesting_guard.py` and append the new test without overwriting the existing staged helper migration. |
| 4 | MINOR | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/research/04-conventions-contract-template.md:139-145` | R4 correctly recommends a contract §3 carve-out, but it does not explicitly state that other marker/§3.2 quote surfaces were checked and do not require wording changes. I found at least one relevant quote surface in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1042-1072`. It appears to quote the skip-guard shape rather than the `MUST NOT clear` obligation, but the research should say that. | Add a short cross-reference check listing marker/§3.2 quote surfaces reviewed. State whether `sc-tasklist-protocol/SKILL.md` needs no change because it only emits the skip guard, or include it in the update scope if the carve-out must be mirrored there. |

## Actions Taken
- Wrote this QA report only; no research files were modified because `fix_authorization: false`.
- Independently read all assigned research files and spot-checked the source files they cite.
- Verified the proposed test target currently has a staged modification, making the collision risk concrete rather than hypothetical.

## Recommendations
- Resolve all four findings before synthesis/task building.
- Preserve R2's validated mechanism: validate base command first; add fixed protocol-authored `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <base command>` only after allowlist/metachar/mutation checks pass; do not add `env` to the user-selectable verb allowlist.
- Add no-overstrip verification explicitly: include marker-suppression tests and keep the POST dogfood gate after the fix, sync, and targeted tests.

## QA Complete

VERDICT: FAIL
