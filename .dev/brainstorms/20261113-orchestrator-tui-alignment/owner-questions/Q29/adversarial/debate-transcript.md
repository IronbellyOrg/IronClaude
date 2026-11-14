# Adversarial Debate Transcript (Q29)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 90% (9 of 10 points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned in parallel (general-purpose, session default model): V1 devops, V2 architect, V3 qa
- Variants: V1 = proposal-A (owner-approved user-level reinstall), V2 = proposal-B (Coder template), V3 = proposal-C (decide later)

## Round 1: Advocate Statements

Full statements: `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round1-advocate-V3.md`. Summaries:

### Variant 1 Advocate (devops)
Only V1 changes the binary the coordinator runs on this host, within minutes, at a pinned commit; the template route cannot pass the gate alone because the shadowing install lives on the persistent home volume. Concedes: needs a recorded exception to the owner's rule; the stray user-level install was written after the owner's statement (rule 2026-11-12 15:02, install 22:12) and V1 would make it deliberate; host drift; `ic` entry point replaced too. Pick: V1 with a dated rule to remove the user-level install once the template pin reaches this workspace.

### Variant 2 Advocate (architect)
V2 keeps one delivery path and one reviewed provenance for every workspace, as the owner stated. Concedes V2 as written does not pass the gate on this host; removing the shadowing install is a required step, ordered after the workspace update so the host does not fall back from `d2d8a2d16` to `4ab620d1`. New evidence: processes started with a worktree's `.venv` active have `<worktree>/.venv/bin` first on `PATH`, and this worktree has `.venv/bin/superclaude` (2026-11-12 22:09), so the gate must be checked with `which -a superclaude` in the coordinator's own environment. Pick: V2 amended (`workflow_dispatch` to cut the wait, update, then one owner-approved removal).

### Variant 3 Advocate (qa)
V3 commits to nothing unsupported and is the spec's default, but its own hope (the template delivers without a decision) fails on this host because of the persistent shadow. The real decision is "who removes `~/.local/bin/superclaude`, and when". Pick: V2 amended with the removal, with V3's "not runnable, XC-04 held" as the interim record.

### Orchestrator verification (2026-11-14, read-only)
- `/home/coder/workspaces/Coder/templates/VSCode-AIDev02/main.tf:583-597`: `/home/coder` is a persistent Docker volume, and each `coder update` produced a new container (the comment records Orca left down after template updates until the machine-id fix). Confirmed: the user-level install survives a template update, and a template update recreates the container (so running sessions end; inference from the container model).
- `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.venv/bin/superclaude` exists (2026-11-12 22:09). Confirmed.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie | 95% | identical structure |
| C-001 | L2 | V1 | V2 | V2 | V2 | 72% | the owner's stated route, with the removal step added |
| C-002 | L2 | V1 | V1 | V1 | V1 | 92% | minutes versus a day plus four steps |
| C-003 | L2 | V2 | V2 | V2 | V2 | 95% | every workspace on the same reviewed pin |
| C-004 | L2 | V1 | V1 | V3 | V1 | 70% | no container recreation (`main.tf:583-588`) |
| X-001 | L2 | V2 | V2 | V2 | V2 | 95% | follows the owner rule and still delivers |
| X-002 | L3 | V1 | V1 | V2 | V1 | 68% | as written only V1 changes what the coordinator runs |
| X-003 | L2 | V2 | V2 | V2 | V2 | 92% | install-proven, image-built pin |
| A-001 | L3 | tie | V2 | V3 | unresolved | 50% | all QUALIFY: the coordinator's `PATH` (Orca shim, worktree `.venv`) is unverified; check in its own environment |
| A-002 | L3 | V1 | V1 | V3 | V1 | 66% | replacing keeps a newer revision; removal must follow the update |

Points won: V1 4 (C-002, C-004, X-002, A-002), V2 4 (C-001, C-003, X-001, X-003), V3 0; A-001 unresolved; S-001 tie.
Shared assumptions: A-001 all QUALIFY; A-002 all QUALIFY; A-003 all ACCEPT; A-004 all ACCEPT.

## Convergence Assessment
- Points resolved: 9 of 10
- Alignment: 90%
- Threshold: 80%
- Taxonomy coverage: L1 1, L2 6, L3 3 (all covered)
- Invariant probe gate: not applied (depth quick)
- Status: CONVERGED
- Unresolved points: A-001
- Overall picks: 2 of 3 advocates (V2, V3) chose V2 amended with removal of the shadowing install; V1's advocate chose V1 with a later removal. All three agree the shadowing user-level install must be removed at some point, and the gate must be checked in the coordinator's own environment.
