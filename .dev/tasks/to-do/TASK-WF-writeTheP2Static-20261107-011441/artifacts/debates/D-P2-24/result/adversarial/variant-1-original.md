# D-P2-24, option A (recommended): two call sites that no spec row names are skipped, not nested

1. release-split Part 4 (fidelity verification) says "Skill `sc:analyze` or inline verification" (`src/superclaude/skills/sc-release-split-protocol/SKILL.md` near line 331). Under `--unattended` it uses inline verification and makes no `sc:analyze` call; no nested directory, no nested-list entry.
2. reflect's Wave 1B optional `tech-research` call (`src/superclaude/skills/sc-reflect-protocol/SKILL.md` near line 632, `--depth deep` only) is skipped and recorded, because `tech-research` has no Unattended mode (as D-P2-1 decides for brainstorm).

Claimed strengths: both are optional or have an inline fallback already in the skill; no new nested directory or test pin; the spec's nested list for release-split and reflect stays as written.
Claimed weakness: release-split Part 4 loses the richer `sc:analyze` verification when a coordinator would have liked it; reflect `--depth deep` loses its research enrichment.

## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
