# QA report: operational correctness (task-qualitative)

**Reviewer:** rf-qa-qualitative agent (report transcribed by the orchestrator; the agent's harness forbids writing .md files; content is its inline return)
**Date:** 2026-11-07
**Checked:** more than 30 paths and line numbers on disk (install.js:18-28, _config-driven.js:190-205 and 937-960, platform-codes.yaml:57, Dockerfile.coder:133-144, install.sh:27-60, test-57:173/323-345/413-465/448-452, startup.sh:673-679/1113/1170, README 100/241/308, releases.json:113, both markdownlint files): all exist and match. Output paths sit inside the task folder; phase order and dependencies are runnable.

## Blocking (IMPORTANT)
1. About 50 items make agents write .md files, but delegated agents can be unable to (this task's own qa-fix-verification.md line 3 needed transcription). The only fallback is "log blocker, mark complete" (task lines 192-208), so Steps 3.14 and 5.x then read missing files. Add a per-item fallback (.json or inline return, orchestrator transcribes) and relax "not by you".
2. The task file is about 403 KB; Read caps at 256 KB (the reviewer's Read failed) and line 168's loop reads it every item. Tell executors to Grep `^- \[ \]` and use offset/limit.
3. F11 half-applied: line 192 allows help flags then says "run no installer command at all" and checks "no installer command was run". Items 196, 204, 208 have no `bmad install` ban; 196(a) asks what `bmad` does with no `_bmad/`. Help flags also run `bmad-cli.js:19-44` (`npm view`): add `NPM_CONFIG_OFFLINE=true`.
4. A STOP-AND-RE-SCOPE report (line 303: no Section 8 plan) cannot pass Gate 3 actionability (378) or Step 6.8 criteria 8 and 21-23 (474). Add a branch for it.

## Minor
"Build context not visible" hardcoded (303, criterion 23) before agent 05 decides it; Step 5.4 "if they exist" can race 5.1-5.2; ticking 7.5/7.6 edits the task file after `git add`; gap-researcher prompts append-only but must edit Gaps (233, 253); longest prompt 9.3 KB (line 192).

## F8-F11 re-check
F8 PASS (retired tag only at 474; new tag consistent). F9 PASS (299, 303, 474). F10 PASS (208, 303, 474). F11 FAIL (finding 3).

Stop condition reachable (299, 303, Section 9); both owner questions carried to Section 9.

## Self-audit
Relied on inherited F1-F7 PASS; insufficient for F5 (finding 3) and F4 (ticks edit the file after staging).

VERDICT: FAIL
