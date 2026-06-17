# E1 — Residual-Integrity & Sync-Parity (run-1)

Worktree: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
Test ID: E1 | Run index: 1 | Verdict: **PASS**

---

## Probe 1 — Residual TFEP-token sweep (target files)

Command:
```
LC_ALL=C rg -n --sort path "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict" src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md
```
Stdout (verbatim): (empty)
EXIT=1

Findings: rg returned zero matching lines and exited 1, the canonical "no match" signal. None of the residual forensic/old-backend tokens (`/sc:forensic`, bare `forensic`, `--tier`, `--intent`, `rca-verdict`, `solution-verdict`) survive in either the task-protocol SKILL.md or task.md command file. Satisfies AC1.1 (exit 1 + 0 hits).

---

## Probe 2 — `/sc:forensic` sweep across `src/`

Command:
```
LC_ALL=C rg -n --sort path "/sc:forensic" src/
```
Stdout (verbatim): (empty)
EXIT=1

Findings: The repo-wide `src/` sweep for the deprecated `/sc:forensic` invocation returned no lines and exited 1. The old forensic backend is fully removed from the source tree, not merely the two target files. AC1.2 holds (exit 1 + 0 hits).

---

## Probe 3 — Sync parity (`make verify-sync`)

Command:
```
make verify-sync
```
Stdout (verbatim, trailing summary):
```
=== Installer Registration ===
  OK _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh

=== Hooks Cross-Consistency ===
  OK hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

All components in sync.
```
EXIT=0

Findings: `make verify-sync` exited 0 and emitted "All components in sync." Every skill, agent, command, hook, and template (including sc-task-protocol and sc-troubleshoot-protocol) shows the in-sync marker. `grep -Ec "DIFFERS|MISSING"` over full stdout returned 0. AC1.3 holds (exit 0 + in-sync + no DIFFERS/MISSING).

---

## Probe 4 — Staged/dirty `.claude/` paths

Command:
```
git status --porcelain | grep '\.claude/'
```
Stdout (verbatim): (empty)
EXIT=1

Findings: Porcelain status filtered to `.claude/` produced zero lines (grep exit 1 = no match). No `.claude/` mirror path is staged, modified, or dirty — SoT discipline upheld. AC1.4 holds (0 lines).

---

## Probe 5 — FALSIFICATION: sweep liveness

Command:
```
LC_ALL=C rg -n "troubleshoot" src/superclaude/skills/sc-task-protocol/SKILL.md | head -1
```
Stdout (verbatim):
```
137:**Diagnostic backend:** `troubleshoot` (the `/sc:troubleshoot` skill; see `sc:troubleshoot-protocol`). The TFEP references below are backend-neutral — swapping the backend changes only this declaration and the invocation string.
```
EXIT=0

Findings: The falsification control returned a real match (line 137) and exited 0, proving the sweep tooling is live and the target file is non-empty and readable — the zero-hit results in probes 1/2 are genuine absences, not a broken grep or wrong path. AC1.5 holds (>=1 line).

---

## Probe 6 — FALSIFICATION: backend present

Command:
```
LC_ALL=C rg -c "/sc:troubleshoot" src/superclaude/skills/sc-task-protocol/SKILL.md
```
Stdout (verbatim):
```
6
```
EXIT=0

Findings: `rg -c` counted 6 occurrences of `/sc:troubleshoot` and exited 0. The new troubleshoot backend is wired into the protocol in multiple places, confirming the migration installed the replacement rather than merely deleting the old forensic backend. AC1.6 holds (>=1).

---

## Verdict

All six acceptance criteria (AC1.1–AC1.6) hold deterministically. The TFEP forensic->troubleshoot backend migration left zero residual tokens in the target files and across `src/`, the src/ <-> .claude/ component sync is intact with no drift, no .claude/ paths are dirty/staged, and both falsification controls confirm the sweep is live and the new backend is genuinely present.

**Verdict: PASS** — normalized_observation_digest=443baab42cb252ae4c36b6bc298ee9d65393c7f3cd865c2dad8be5203f9c80b2
