import sys, json, collections
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
before = len(s.encode())
E = []
def e(fid, old, new): E.append((fid, old, new))

e('M6', "(`--output` / `--output-dir`). It follows",
  "(`--output` / `--output-dir`). Exception: adversarial writes `<output>/adversarial/return-contract.yaml`, the path its section 3.1 row names (its artifacts sit under `adversarial/`, `INV-A:35`) (M6). It follows")
e('M7', "(`--output` / `--output-dir`). Exception:",
  "(`--output` / `--output-dir`). When `--output` is a file (tdd, init-lite) the contract is `<output-file>.return-contract.yaml`; cleanup-audit and index-repo have fixed output locations, so theirs are `.claude-audit/return-contract.yaml` and `PROJECT_INDEX.return-contract.yaml` at the repository root (M7). Exception:")
e('M1', "including stops before any other output exists. Commands that already",
  "including stops before any other output exists. Workflow is the one command whose path is not known before dispatch: it holds an id the run generates (`.dev/tasks/to-do/<id>/return-contract.yaml`, `INV-B:272`), so the worker takes the single such file created after dispatch, and a workflow stop before the package exists writes no contract (the worker sends `--outcome failed`, WC-5) (M1). Commands that already")
e('M1', "\"Contract\" means the WC-4 file `<output-dir>/return-contract.yaml`.", "\"Contract\" means the WC-4 file, at the path WC-4 gives.")
e('M2', "Every changed command also gains the `## Unattended mode` section (section 2.1).",
  "Every command whose row names an unattended-mode change in P1-P3 also gains the `## Unattended mode` section (section 2.1); brainstorm and init-lite (no change), load (usage line only) and the P4 commands (decisions D2-D4) do not gain it in P1-P3 (M2).")
e('M5', "the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4);",
  "the exact command line, with `--unattended` only for a command that already has the section (P0 runs without it) and every flag section 3 lists as required; the contract path from WC-4, so the report path is known before dispatch (M5);")
e('M2', "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)",
  "the `--unattended` flag accepted by every command whose row names a P1 change (a no-op where a command has no gate)")
e('M8', "load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow |",
  "load (usage line only: no `--unattended`, no section, no contract); fixes to adversarial, cleanup-audit, index-repo |")
e('M1', "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1)",
  "None; its path holds a generated id and a pre-creation STOP writes no contract (WC-4)")
e('M8', "none: use it as a step inside another worker's brief, not as its own Task; separately",
  "none: no `## Unattended mode` section, no `--unattended`, no contract; use it as a step inside another worker's brief, not as its own Task; separately")
e('M1', "adversarial and workflow contract gaps", "the adversarial contract filename")
e('M5', "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1.",
  "each run directly by the worker, without `--unattended` (it arrives in P1); the step-5 transcript search also finds no Agent-tool call wrapping the command | steps 1, 2 and 5-7 pass; in step 3 the report path is the command's existing report file (3.1 \"Report today\" column) and `--outcome` is `succeeded` when it exists; step 4 is `test -s` on that file only, since the contract and its `status` arrive in P1.")
e('M2', "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that",
  "every command in sections 3.1-3.2 whose row names a P1 change (not load, brainstorm, init-lite or the P4 commands) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that")
e('M8', "7.2 live check on each P1 command with `--unattended --output <dir>` |",
  "7.2 live check on each P1 command except load, with `--unattended` and the output flag its row names, if any (contract at the WC-4 path) |")
e('M6', "adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |",
  "adversarial names `<output>/adversarial/return-contract.yaml`, the WC-4 exception path |")
e('M6', " and the workflow return-contract ref |", " |")
e('M9', "Gate-trigger run per P2 command: a 7.2 live check", "Gate-trigger run per P2 command whose row resolves a gate as blocked (cli-eval, cli-portify, recommend, review-translation, release-split, tdd, troubleshoot, task, and spec-panel with a TDD input): a 7.2 live check")
e('M9', "step 2 never shows `agentWait` |",
  "step 2 never shows `agentWait`. The other six (auggie-review, cleanup, improve, research, reflect, tasklist) never write `blocked`: auggie-review is checked by AC-2.4; cleanup and improve by a run whose contract lists the \"Approval Required\" items unapplied; research, reflect and tasklist by AC-2.3, with step 2 never showing `agentWait` |")

stats = collections.defaultdict(lambda: [0,0,0])
for fid, old, new in E:
    assert s.count(old) == 1, (fid, old[:60], s.count(old))
    s = s.replace(old, new)
    stats[fid][0] += len(new.encode()); stats[fid][1] += len(old.encode())
open(p, 'w', encoding='utf-8').write(s)
print(before, len(s.encode()))
for k in sorted(stats): print(k, stats[k][0], stats[k][1])
