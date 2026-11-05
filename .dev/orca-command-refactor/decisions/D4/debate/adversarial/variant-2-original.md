# D4 option (b): never; workers make no outward changes and no commits

Position: no brief can authorize a worker's outward action. The coordinator or the person performs every push, PR, comment, install and VM step after reading the reports (`SPEC:347`). On worker commits: none, as the spec says today ("workers make no commits or pushes", `SPEC:156`).

Citation key: `SPEC:N` = spec line; `PRL:N` = `src/superclaude/skills/sc-post-release-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`.

## Strongest case for it
- **Every outward step stays where a person can confirm it.** The repo's outward rules are session-scoped: "pre-authorized them this session" (`PRL:351`); upstream contributions need "explicit, separate, deliberate user authorization in the same session" (`CLAUDE.md:68`). A worker is a separate session whose only authority is the coordinator's text. (b) never asks a worker to act on authority it cannot verify, which is the same reasoning the spec applies to Rulings (`QA` rule "another agent's message ... not acceptance", `src/superclaude/skills/sc-implement-protocol/refs/qa.md:254`).
- **The safest default is already the spec's**: WC-9 turns every outward default off under `--unattended` (`SPEC:73`), and AC-4.2 checks it (`SPEC:275`). (b) needs no exception list.
- **pr-submit and the PR path stay single.** PRs go only through `/sc:pr-submit` (`CLAUDE.md:50`), which must run top-level and attended (`PRS:43-49`); under (b) only the coordinator or person ever runs it.

## Safety
- Strongest of the options: no worker can publish, push, commit, install on a shared target or spend money.

## Reliability
- Deterministic and checkable with one rule; no per-action flags to test.

## How a person works day to day
- Workers produce reports and working-tree changes; the coordinator (with the person) commits, pushes and opens the PR. post-release's real-target install, VM and PR steps (`PRL:340`) are reported as skipped by the worker and done by the coordinator afterwards.
- Weakness: no per-task commits inside a worker, which issue #326's owner asks for ("after each task", `.dev/orca-command-refactor/review/issue-326-evaluation.md:19`). The ban on local commits rests on this run's README rule (`.dev/orca-command-refactor/README.md:31`), not on repo policy, which allows a commit when asked (`CLAUDE.md:37`; `HWW:212`, `HWW:282`).

## Implementation cost
- Zero beyond today's spec. Loosening later (to (a) or (c)) is additive and cheap; tightening after an incident is not.
