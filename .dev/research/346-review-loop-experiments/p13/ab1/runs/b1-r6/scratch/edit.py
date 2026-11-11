import json,sys,collections
P='/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md'
s=open(P,encoding='utf-8').read()
before=len(s.encode())
E=[]
def e(i,o,n): E.append((i,o,n))

# ---- L1
e('L1','These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract. The only command changes are the small fixes in the last column.',
 'These run as workers now if the brief uses the stated flags and no `--unattended` (the flag arrives in P1); the worker reports the named file until Phase 1 adds the contract. Besides the P1 flag and section, the only command changes are the small fixes in the last column (L1).')
e('L1','Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)','State the contract filename as `<output>/adversarial/return-contract.yaml`, the directory the skill already writes to (WC-4 exception, L1) (P1)')
e('L1','the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4);',
 'the exact command line including every flag section 3 lists as required, plus `--unattended` from P1 on (L1); a fresh output directory for every Task and every retry, so the report path is known before dispatch and a retry never meets an earlier contract (WC-4, WC-6, L1); for a Task that may stop `blocked`, no dependents are created until the coordinator has read the contract, and a `blocked` Task is not re-dispatched without a new answer in the brief (WC-5, L1);')
e('L1','In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`).',
 'In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`), except: adversarial writes it in `<output>/adversarial/`; where the output flag takes a file (tdd, init-lite) `<output-dir>` is the directory holding that file; workflow generates its directory, so the worker takes the path from the command\'s final message (L1). If the brief gives no output location, the command writes nothing and stops with a chat reply that says so, which WC-5 maps to `failed` (L1).')
e('L1','`status` (one of `succeeded`, `partial`, `failed`, `blocked`)','`status` (one of `succeeded`, `partial`, `failed`, `blocked`; a command whose own status uses other values adds this field beside them, L1)')
e('L1','Orca does not check the file, so the coordinator opens it.','Whether Orca checks the file is UNVERIFIED (`CAPS:79`), so the coordinator opens it (L1).')
e('L1','`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise, including `partial`',
 '`--outcome failed` when the report says `failed` or `blocked`, or no report exists, or its `status` is missing, unknown or unparseable (L1); `--outcome succeeded` otherwise, including `partial`')
e('L1','The worker sends `worker_done` exactly once from its own top-level session.','The worker sends `worker_done` exactly once from its own top-level session; after a lost response it repeats the call with `--retry-request` (`CAPS:117`, L1).')
e('L1','A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean.',
 'A command either resumes from its on-disk state (when given its resume flag, or implicitly where section 3 says so, as for implement), or, if it has none, writes each run into a fresh output directory the brief passes, so a re-run starts clean (L1).')
e('L1','steps 1-3 and 5-7 pass; step 4 uses the command\'s existing report file, since the contract arrives in P1.',
 'the commands are run without `--unattended` and with the P0 flags of section 3.1; steps 1, 2 and 5-7 pass; in steps 3 and 4 the report is the command\'s existing report file and the `--outcome` is checked against it, since the contract and flag arrive in P1 (L1).')
e('L1','each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)','each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript by finding the command line in the worker\'s own turn and no Agent or Task call that carries it, L1)')
e('L1','the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)','the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (a no-op where a command has no gate; load is not its own Task, L1)')
e('L1','every command in sections 3.1-3.2 has a `## Unattended mode` section','every command in sections 3.1-3.2 except load has a `## Unattended mode` section')
e('L1','adversarial names one fixed path;','adversarial names the one path `<output>/adversarial/return-contract.yaml`;')

# ---- L2
e('L2','Any such prompt must fall back on its own well inside the readiness limit (default 60 s).','Any such prompt must fall back on its own within 30 s, inside the readiness limit (default 60 s) (L2).')
e('L2','No person-blocking step in unattended mode.** Under `--unattended` the command never calls',
 'No person-blocking step in unattended mode.** WC-2 to WC-12 apply only under `--unattended`; without it SA-1 governs (L2). A tool-permission approval is also a person-blocking step the command cannot remove; the brief or launch setup must pre-approve the tools the command needs, else the stall shows as `agentWait` (L2). A brief that passes both `--unattended` and `--interactive` makes the command stop `blocked`, and the flag counts only on the command line, not inside quoted content (L2). Under `--unattended` the command never calls')
e('L2','the session may instead ask the coordinator once with the preamble\'s `ask` command, wait, then re-invoke or resume the command with the answer as a flag.',
 'the session may instead ask the coordinator once with the preamble\'s `ask` command, wait, then re-invoke or resume the command with the answer as the flag its section 3 row names; a row naming no such flag cannot take an answer and stays `blocked`. An answered `ask` replaces the `blocked` outcome by the final run\'s outcome; AC-2.2 runs with no answer given (L2).')
e('L2','so a command run by a worker has the same tools as a command a person runs.','so a command run by a worker has the same tool set as a command a person runs (tool-permission approvals are not evidenced, WC-2, L2).')
e('L2','Default output paths carry a timestamp or the slug the coordinator passes;','Under `--unattended`, default output paths carry a timestamp or the slug the coordinator passes, and a command with a fixed default output (cleanup-audit, index-repo, release-split) runs one Task per worktree (L2);')
e('L2','The worker sends a heartbeat every 5 minutes while working.','The worker sends a heartbeat every 5 minutes while working (its role in liveness is UNVERIFIED, L2).')
e('L2','A command\'s own Agent-tool fan-out stays as it is.','A command\'s own Agent-tool fan-out stays as it is; the coordinator does not read a missing heartbeat as a stall while the worker waits in such a call (L2).')
e('L2','and the worktree placement (`CAPS:115`).','and the worktree placement (`CAPS:115`): a Task whose command writes source files or has a fixed default output gets its own worktree (L2).')
e('L2','Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags.','Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section, which states that it overrides the gate text in the command body under `--unattended`, and new flags (L2).')
e('L2','and each such fix must keep the standalone behaviour or correct a documented defect.','and each such fix must keep the standalone behaviour; SA-3 wins over a fix that would rename a standalone default file, unless section 3 names it (L2).')
e('L2','state that knowledge-base mode does not wait (whether it does is UNVERIFIED)','if knowledge-base mode waits for a person (UNVERIFIED), resolve it as blocked')
e('L2','`worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`','with the worker sending no `ask` (L2): `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`')
e('L2','| Gate-trigger run per P2 command:','| Gate-trigger run per P2 command:')  # no-op placeholder

# ---- L13
e('L13','The only allowed mention of Orca in a changed command is as an example of a caller\'s question channel inside the contract file.',
 'Core files (`HOW-WE-WORK.md`, `WORKER-CONTRACT.md`) may describe Orca; no changed command file mentions it except as an example of a caller\'s question channel (L13).')
e('L13','| AC-C1 | `grep -rnE \'\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b\' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \\| grep -v \'^src/superclaude/skills/ccsession-tag/\'` | prints nothing (SA-2, WC-8) |',
 '| AC-C1 | The command in the block below this table (L13) | prints nothing (SA-2, WC-8) |')
e('L13','| AC-C2 | `make verify-sync`','| AC-C2 | `make verify-sync`')
e('L13','### 7.2 Live worker check (used by P0-P4)',
 '`AC-C1` (L13; written outside the table so the alternation bar is not escaped, and scanning commands, skills and agents only, because SA-2 lets core files describe Orca):\n```bash\ngrep -rnE \'\\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\\b\' src/superclaude/commands src/superclaude/skills src/superclaude/agents | grep -v \'^src/superclaude/skills/ccsession-tag/\'\n```\n\n### 7.2 Live worker check (used by P0-P4)')

tot=collections.defaultdict(lambda:[0,0])
for i,o,n in E:
    if o==n: continue
    assert s.count(o)==1,(i,o[:60],s.count(o))
    s=s.replace(o,n)
    tot[i][0]+=len(n.encode()); tot[i][1]+=len(o.encode())
open(P,'w',encoding='utf-8').write(s)
print(before,len(s.encode()),dict(tot))
