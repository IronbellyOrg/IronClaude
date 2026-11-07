# D-P2-23, option B (alternative): run the gate under --unattended without --fix and without --promote

Under `--unattended` the CLI-mode reflect gate still runs, as `superclaude reflect run <task> --depth deep --no-promote` (no `--fix`), and its staging step is left to the coordinator or replaced by a note. The wrapper writes its report; a Regression or unauthorized Drift is returned as a blocked result (the coordinator decides on a fix) instead of auto-fixing.

Claimed strengths: the independent audit still happens and its report is an artifact the coordinator can read; `--no-promote` is the flag `/sc:reflect` already defines for coordinator-owned folder moves.
Claimed weakness: the wrapper `superclaude reflect run` is a CLI subprocess whose own unattended behaviour and whether it accepts these flags together are unverified; the audit omits never-staged files, so without the staging step the audit may miss new task artifacts; this adds a nested subprocess and more text.

## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
