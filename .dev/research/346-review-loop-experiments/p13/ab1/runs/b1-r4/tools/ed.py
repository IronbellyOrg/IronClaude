import sys, json
P=sys.argv[1]
s=open(P,encoding='utf-8').read()
E=[]
def r(fid, old, new):
    global s
    assert s.count(old)==1, (fid, old[:60], s.count(old))
    s=s.replace(old,new)
    E.append((fid,len(old.encode()),len(new.encode())))

# L1 WC-1 quantify
r("L1","Any such prompt must fall back on its own well inside the readiness limit (default 60 s).","Any such prompt must fall back on its own within 30 s (the readiness limit defaults to 60 s).")
# WC-3
r("L1","the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag. On an","the session may instead, after the contract with `status: blocked` is written, ask the coordinator once with the preamble's `ask` command for the value of a flag section 3 lists, wait, then re-invoke the command with that flag (the contract is rewritten). It never relays an answer as a `/sc:implement` Ruling (D2). If no answer comes, it sends `worker_done --outcome failed` with that contract. On an")
# WC-4
r("L1","In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows","In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output-dir`), or the parent directory of the file passed as `--output <file>`; a command whose section 3 row names a different fixed path (adversarial) uses that path. With no output given in the brief the command stops before doing work. For `/sc:workflow` the path holds a generated id, so the coordinator learns it from `worker_done --report-path`, not before dispatch. It follows")
r("L1","carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command`","carries at least: `contract_version` (`1`), `status` (one of `succeeded`, `partial`, `failed`, `blocked`; an existing contract's own status values are mapped to these), `command`")
r("L1","including stops before any other output exists. Commands that","including stops before any other output exists, and is complete before `worker_done` is sent. Commands that")
# WC-5
r("L1","`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including","`--outcome failed` when the report says `failed` or `blocked`, or no report exists, or its `status` is missing or not one of the four; `--outcome succeeded` otherwise, including")
# WC-6
r("L1","writes each run into a fresh output directory so a re-run starts clean. Section 3","writes each run into a fresh output directory so a re-run starts clean; the retry's brief names that directory, so the contract path is known (WC-4). Section 3")
# WC-10
r("L1","A command step that blocks a single tool call for longer than 5 minutes (a poll wait, a long eval) must","A command step that can block a single tool call for longer than 4 minutes (a poll wait, a long eval) must")
# WC-12
r("L1","if `check` returns `consumer_fenced` it stops","if `check` returns `consumer_fenced` (an empty result is not that) it stops")
# 2.3
r("L1","every flag section 3 lists as required; the output directory","every flag the section 3 row names as required (the \"Brief must pass\" column in 3.1, the gate-resolution cell in 3.2); the output directory")
r("L1","After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).","The worker's permission mode must allow the command's tools without a prompt, since a permission prompt is a person-only prompt (7.2 step 2 shows it). After `worker_done`, the coordinator opens the report file before it starts any dependent Task (Orca records `partial` as completed, WC-5), then releases or reuses the worker (`CAPS:107-113`). It retries a blocked Task only with a brief that answers the `blocked_question`.")
# 3.1 intro
r("L5","the worker reports the named file until Phase 1 adds the contract.","the worker reports the named file until the phase in its row adds the contract.")
r("L1","| `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Re-run overwrites its marked report | None |","| `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Fresh `--output` file per attempt (WC-6) | None (P1) |")
r("L1","dispatch only inside an IronClaude checkout (hardcoded template path)","brief rule, no edit: dispatch only inside an IronClaude checkout (hardcoded template path)")
# Phase table
r("L1","the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow |","the `## Unattended mode` section and `--unattended` flag for the commands listed here only (a command with a gate gets the flag in the phase of its section 3 row, so none accepts it before its gates convert); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only, no section); adversarial, brainstorm, cleanup-audit, index-repo, init-lite (adds its contract), workflow |")
r("L5","Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval. |","Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval; for release-split, tdd and troubleshoot the section also adds the WC-4 contract pointing at their named report file. |")
# AC-C1 .. move to block
r("L4","| AC-C1 | `grep -rnE '\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \\| grep -v '^src/superclaude/skills/ccsession-tag/'` | prints nothing (SA-2, WC-8) |","| AC-C1 | The command in the block under this table (alternation written with plain `|`) | prints nothing (SA-2, WC-8) |")
r("L2","| AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \\| grep -E '^-[^-]'` | prints nothing: edits are additive |","| AC-C5 | For every command file the phase edits without a named defect fix (SA-4): `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \\| grep -E '^-' \\| grep -v '^--- a/'` | prints nothing: edits are additive (a deleted line that starts with a dash still shows) |")
r("L4","| prints nothing: edits are additive (a deleted line that starts with a dash still shows) |\n","| prints nothing: edits are additive (a deleted line that starts with a dash still shows) |\n\nAC-C1 command (L4: the pattern uses plain `|`, which `grep -E` reads as alternation; it covers the other `orca` verbs and skips the contract file and routing guide where SA-2 and P0 allow Orca text):\n```bash\ngrep -rnE '\\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent|status|open|skills)\\b' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core | grep -v -e '^src/superclaude/skills/ccsession-tag/' -e '^src/superclaude/core/WORKER-CONTRACT.md' -e '^src/superclaude/core/HOW-WE-WORK.md'\n```\n")
# 7.2
r("L1","its report path is the WC-4 contract path.","its report path is the WC-4 contract path (in P0, the command's existing report file).")
r("L1","and search the transcript for `AskUserQuestion`. **Pass:** no `AskUserQuestion` call.","and search the transcript for `AskUserQuestion` and for an Agent-tool call that runs the command. **Pass:** neither appears.")
r("L2","`git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \\| grep -E '^-[^-]'` | prints nothing","`git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \\| grep -E '^-' \\| grep -v '^--- a/'` | prints nothing")
r("L1","the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one","the test asserts that every command listed in the P1 row of section 6 (except `/sc:load`) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command and not `/sc:load` has one; each later phase extends the list to its own commands")
open(P,'w',encoding='utf-8').write(s)
agg={}
for f,a,b in E:
    d=agg.setdefault(f,[0,0]); d[0]+=b; d[1]+=a
print(json.dumps(agg))
