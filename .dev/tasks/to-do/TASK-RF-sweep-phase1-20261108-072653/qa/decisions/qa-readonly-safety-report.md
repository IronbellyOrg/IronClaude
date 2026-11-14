# QA Report - Item 7.24 Read-only safety lens (rf-qa)

**Date:** 2026-11-12
**Phase:** decisions gate, agent 4 of 8, read-only safety lens
**fix_authorization:** false (only this report was written)
**Package:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` (paths below are relative to it unless they start with `docs/`, `src/`, `tests/` or `/`)

## Checks

| Check | Description | Result |
|-------|-------------|--------|
| C1 | Every command in `artifacts/readonly-probe.md` is one of DESIGN 7.3 templates 1 to 8, a file read, or the item's step (6) `echo` and `ls -la` | PASS |
| C2 | No forbidden token was run (`worker-read`, `gate-list`, `check`, `inbox`, `--include-remote`, `git stash`, `run-current --json`) | PASS |
| C3 | `run-current` was issued only in its plain form | PASS |
| C4 | Step 1.0a ran no `--agent-wait` template; `worktree ps` was issued only as `worktree ps --json` | PASS |
| C5 | Before and after `worker-show` and `task-list` reads match (checked by me from the raw files) | PASS (see M1) |
| C6 | Read order was before, middle, after, as item 7.16 requires | PASS (see M5) |
| C7 | DESIGN 7.3 `FORBIDDEN_TOKENS` is exactly `{"--include-remote"}` | PASS |
| C8 | DESIGN 7.3 `ALLOWED_ORCA` holds ten templates; the two `worktree ps --agent-wait` forms are templates 9 and 10 | PASS |
| C9 | R5 edit is consistent across DESIGN 7.3, 11, 12, 13, 15.1, the GQ-109 row and the section 18 `### Fix cycle 3` R5 row | PASS |
| C10 | Fixtures hold no real home path prefix, session id, pane key, terminal handle or account name | PASS (see M4) |
| C11 | Fixtures hold no free-text message bodies, secrets or other sessions' conversation | PASS |
| C12 | Capture created no Run, Task or Dispatch and issued no write command to Orca | PASS |
| C13 | Tab-map reads stayed inside the recorded `orca-tabs/` folder (five files) | PASS (producer record; see Confidence) |
| C14 | OQ-17 refusal is consistent with the allowlist staying at ten and no cursor template | PASS |
| C15 | `artifacts/pr422-409-check.md` ran only read commands, with `--repo IronbellyOrg/IronClaude`, and no fetch, push or upstream call | PASS |
| C16 | The early Markdown style edit touched only `src/superclaude/output-styles/pragmatic.md`; no skill, CLI, test, mirror, sync or install change | PASS |
| C17 | The style edit is not represented as a sweep runtime write, a new probe or an action right | PASS |
| C18 | HOME activation is not inferred from sync | PASS |
| C19 | Execution authorization for 7.10 is separate from the OQ-6 decision and the revision authorization, and covers item 7.10 only | PASS |
| C20 | Process statements in the probe's header and compliance record are accurate | FAIL (MINOR only: M2, M3) |

## Findings

No BLOCKING or MAJOR finding. Six MINOR notes (M1 to M6). Every safety property in the lens holds.

### M1 (MINOR) The before/after rule is met on state, not on raw bytes

- Evidence: `artifacts/readonly-probe.md:767-783`; DESIGN `docs/designs/orchestrator-mode.md:897` ("identical apart from timestamps ... A difference stops the build and goes to the owner"); item 7.16 Verification.
- I re-ran the comparison myself with `jq -S 'del(.id)'` over all seven before/after pairs in `artifacts/readonly-probe-raw/` (5 `worker-show`, `task-list --ready`, `task-list`). All seven payloads are identical. The only differing field in each pair is the top-level envelope `id`, a per-call UUID (`diff` showed only line 5 differing for every pair). No timestamp, status or count differs.
- The executor treated that request id as outside the rule and did not HALT. That is a reading made by the executor, stated openly in the probe with the owner HALT text. `phase-outputs/discovery/1.0a-facts.md` row 11 repeats it. No record shows the owner accepting that reading.
- Why MINOR: a strict byte reading could never pass for any Orca read, so the rule can only mean state. The property that the rule protects (reads change nothing) is shown.
- Smallest fix: when DESIGN 15.1 is next edited, add "and the envelope request id" to the sentence at line 897. Or the owner acknowledges the reading.

### M2 (MINOR) "Every command ran in its own Bash call" is not what the scratch files show

- Evidence: `artifacts/readonly-probe.md:8`; `/tmp/probe-7-16/` file times.
- The header says each command ran in its own Bash call with an inner `timeout 8`. The scratch timestamps show commands run back to back with 6 to 10 ms gaps. The five `worker-show` and two `task-list` before-reads span 21:37:10.204 to 21:37:11.589, with each `.rc` followed by the next `.err` within about 6 ms. An agent round trip cannot do that, so they ran from one shell loop. The inner `timeout 8` cannot be proved or disproved from disk.
- Impact: none on the command set, read-only effect or runtime (each command finished in about 0.2 s). The item only requires a 30000 ms timeout on every Bash call.
- Smallest fix: reword the sentence to say the reads ran in scripted batches with per-command output capture.

### M3 (MINOR) Extra writes beyond the notes file are disclosed but not listed as a deviation

- Evidence: DESIGN `docs/designs/orchestrator-mode.md:890` ("writes only its own notes file"); item 7.16 Output (one file); `artifacts/readonly-probe.md:8,10`; 16 files in `artifacts/readonly-probe-raw/`; `/tmp/probe-7-16/`.
- The capture also wrote 16 raw files under `artifacts/readonly-probe-raw/` and scratch copies under `/tmp/probe-7-16/`. The header discloses both, and the Deviations section lists only D1. None of it touches Orca. The scratch folder (mode 700) still holds `m-t6-wtps.out`, the raw `worktree ps --json` output that the probe says carries other sessions' prompts and messages.
- Smallest fix: add the raw folder to the Deviations list, and delete `/tmp/probe-7-16/` once nothing needs it.

### M4 (MINOR) Fixtures keep real project and folder names after the home prefix is replaced

- Evidence: `tests/sweep/fixtures/` (for example `captured-worker-list.json` paths `/home/user/workspaces/worktrees/IronClaude/issue-504`; `captured-worktree-ps.json:97,197` `"repo": "Coder"`; `/home/user/workspaces/worktrees/Coder/dashboard-bmad`); `tests/sweep/fixtures/SOURCES.md:7-12`.
- Verified by grep: no `/home/coder`, no account name `coder` as a whole word, no UUID outside the `00000000-0000-4000-8000-` fake range, no real session id, pane key or terminal handle from the probe (all 21 checked ids absent), no key-like or email strings, no non-placeholder `prompt`, `lastAssistantMessage`, `toolInput`, `taskTitle`, `comment` or `spec` values. Task subject lines such as `#504 analyze: ...` remain, and so do project, branch and repo names. The sanitize rules in `SOURCES.md` and item 7.18 only require the home prefix, account name and UUIDs, and those are met. A stricter reading of "no real path" would also want the folder names changed.
- Smallest fix: none needed under the stated rules. Say in `SOURCES.md` that project and branch names are kept on purpose.

### M5 (MINOR, evidence limit) Order of reads is provable only from files outside the package

- The raw before/after copies in the package all carry the same modification time (21:43:30), because they were copied in one step. The deliverable alone cannot show order. The `/tmp/probe-7-16/` file times can: before-reads 21:37:10 to 21:37:11, middle reads (`run-current`, `worker-list`, `worktree ps`, `list`, `current`, fake-Run `worker-list`, fake-Run `task-list`) 21:37:15 to 21:37:16, after-reads 21:37:20 to 21:37:21. That matches item 7.16 Action steps 2 to 4. The `.rc` files hold `exit=0` except the fake-Run `task-list` (`exit=1`), matching the probe's recorded exit codes.

### M6 (MINOR) Deviation D1 is mis-framed, and item 7.15 made extra template 2 reads

- D1 (`artifacts/readonly-probe.md:1071`) calls the fake-Run `task-list --run` call outside the item's allowance. DESIGN 15.1 capture item 8 (`docs/designs/orchestrator-mode.md:911`) asks for exactly that error shape, so the call fits the design. It is template 5 either way and read-only.
- `phase-outputs/plans/OQ-8-run-id-decision.md:31-44` records template 2 reads against nine other Run ids, made in item 7.15 and not in the probe. They are read-only template 2 commands, not mentioned in the probe's compliance record.

## Evidence by lens duty

- **Commands (C1 to C4).** `grep -o 'orca-ide ...'` over the probe returned only the shapes of templates 1 to 8. The other recorded commands are the Orca `package.json` read, the tab-map `echo` and `ls -la`, and five tab-map file reads. The item 7.16 grep (`worker-read|gate-list|inbox|include-remote|stash|run-current --json`) returns exit 1 over the whole file. `agent-wait` does not appear anywhere in the probe. `run-current` appears twice, both plain. The `check` hits are the words "before/after check".
- **DESIGN 7.3 (C7, C8).** `docs/designs/orchestrator-mode.md:526-537` lists ten tuples in order: `run-current`; `worker-list`; `worker-show`; `task-list --ready`; `task-list`; `worktree ps --json`; `worktree list --json`; `worktree current --json`; `worktree ps --agent-wait`; `worktree ps --agent-wait --json`. Line 539 reads `FORBIDDEN_TOKENS = frozenset({"--include-remote"})`. Line 895 says step 1.0a issues only templates 1 to 8 and does not run `--agent-wait`.
- **R5 spread (C9).** Ten-template wording at lines 66 (GQ-109), 537, 759, 815, 837 (D10), 851 and 895; the section 18 R5 row is at line 1047. No leftover "eight templates" or "never carries --agent-wait" text outside the D10 history cell.
- **No writes to Orca (C12).** Run state is unchanged: 5 workers and 5 tasks before and after, all payloads identical, the fake-Run `worker-list` returned an empty list, and the fake-Run `task-list` returned `run_not_found`.
- **OQ-17 and OQ-18 (C14).** `phase-outputs/plans/OQ-17-cursor-template-decision.md` is RESOLVED with "Keep the 10 commands". No OQ-18 file exists, and the facts file row 3 shows `run-current` needing `--json` was not established.
- **Pre-PR check (C15).** `artifacts/pr422-409-check.md` ran `gh pr view 422 --repo IronbellyOrg/IronClaude --json ...` and two `git merge-base --is-ancestor` calls. No fetch, push or upstream call.
- **Style edit (C16 to C19).** `git status --short` shows ` M src/superclaude/output-styles/pragmatic.md` as the only change under `src/` and `tests/` besides untracked `tests/sweep/fixtures/`; nothing under `.claude` or `plugins`; no sweep skill, CLI entry or test exists. `src/superclaude/output-styles/pragmatic.md:22-26` shows the Scope bullet: chat-presentation only, no change to trigger, tool allowlist, execution authority, worker rule, permission, scheduler or JSON, and "not a runtime detector, identity probe, environment flag". Line 25 adds "Formatting never authorizes advice the sweep skill prohibits." The Makefile `sync-dev` recipe (`Makefile:109-158`) copies only skills, agents, commands, hooks and templates, not output styles. `~/.claude/output-styles/pragmatic.md` differs from the repo copy (`cmp` reports a difference at line 22) and its mtime (16:25) is before the edit, so the installed style is not activated. `phase-outputs/test-results/step-7.10-style-exception.md:85,98` disclaims HOME activation. The owner's execution message ("Accepted, I accepted, but it reported a decline.  Proceed") is in the session transcript at 2026-11-11T20:26:41Z (I confirmed one matching user message), and the result file limits it to item 7.10. `artifacts/owner-decisions.md:19-33` keeps decision, revision and execution permission apart.

## Confidence

Verified: 19/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 95.0%
(C20 is the one failed check, a MINOR documentation finding; C13 rests on the producer's record of which files were read, because file read history is not on disk.)

Tool engagement: Read: 26 | Grep: 11 | Glob: 4 | Bash: 10 (all read-only: grep, jq, cmp, ls)
Web research: none.

Verdict: PASS
Blocking count: 0
