# Q29 final: how does this host's `superclaude` CLI get the sweep command after PR #539 merges?

Terms used here: PR #539 adds the read-only `superclaude sweep` command and its `/sc:sweep` wrapper. The coordinator is the person-opened Claude session that runs the program; the worker-contract rule WC-16 has it run `/sc:sweep` at most once per 5 minutes. SWEEP-RUNNABLE is the spec's gate that holds once `superclaude sweep --help` exits 0 in the coordinator's own environment and `/sc:sweep` writes one report. XC-04 is the one real-id join comparison, which needs a working sweep. The Coder template is the workspace image definition in the `IronbellyOrg/Coder` repository; it pins which IronClaude commit every workspace gets.

## Debate result

Winner: proposal B (the Coder template), amended with one owner-approved removal of the user-level install that shadows the image's copy on this host. Confidence 70 percent.

Advocate agreement: 2 of 3 advocates picked B amended (the advocates for B and C); the advocate for A picked A with a later removal. On points, 9 of 10 converged (90 percent); A and B won 4 points each. All three agreed that the shadowing install must be removed at some point and that the gate must be checked in the coordinator's own session.

Deciding evidence:
- This host has two installs. `/usr/local/bin/superclaude` is the image install from the Coder template (`/opt/uv/tools`, revision `4ab620d1`); `/home/coder/.local/bin/superclaude` is a user-level install at revision `d2d8a2d16`, written 2026-11-12 22:12, and it comes first on `PATH` (observed 2026-11-14). No Coder template script installs into `~/.local`.
- `/home/coder` is a persistent volume across template updates (`/home/coder/workspaces/Coder/templates/VSCode-AIDev02/main.tf:583-597`). So a template update alone changes nothing the coordinator runs while the user-level install exists: the spec's recommended route fails on this host without a clean-up step.
- The owner's rule (memory `ironclaude-updates-only-via-coder.md`, 2026-11-12): IronClaude reaches workspaces only through the Coder template. All three advocates gave B the point on following it.

Proposal A (in-place reinstall at the merge commit): its strengths are speed (minutes), no container recreation and the only route that, as written, changes what the coordinator runs. Its weaknesses: it needs an exception to the owner's rule, keeps this host out of step with other workspaces, and turns a stray install of unknown origin into a sanctioned one.

Proposal B (Coder template): its strengths are one reviewed, install-proven, pinned delivery path for every workspace and compliance with the owner's rule. Its weaknesses: slower (a Coder PR, image build, template push and workspace update), a workspace update recreates the container and ends running sessions, and as written it leaves the shadowing install in place, so the gate would still fail.

Proposal C (decide later): its strength is that it changes nothing and is the spec's default. Its weakness: its hope that the template delivers on its own cannot come true on this host, so it is only an interim record.

## Final recommendation

Use the Coder template, and once the workspace is updated, approve one removal of the user-level install at `~/.local/bin/superclaude`. Until both steps have run, record the sweep duty as "not runnable" and hold XC-04. After the merge, start the Coder pin-bump workflow by hand instead of waiting for its daily run, and plan the workspace update between sessions. Then check in the coordinator's own session that `which -a superclaude` shows the image install first, `superclaude sweep --help` exits 0 and `/sc:sweep` writes one report. Confidence 70 percent.

Strongest reason: it keeps the owner's single update path and is the only option that actually changes what the coordinator runs on this host without an exception.

Equals the spec's recommended answer: partly. Same route (the Coder template), plus the removal step; without that step the spec's route does not make the sweep runnable on this host.

## What would change the answer

If the sweep is needed sooner than a Coder release can deliver it (for example the join comparison becomes urgent while Orca and the read-capture runner are ready), proposal A becomes the better answer, as a recorded one-time exception with a dated removal.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer applies the owner's own update rule, needs a Coder repository merge that reaches every workspace, and asks the owner to approve removing an install of unknown origin from this host. Those are owner decisions even though the debate converged.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q29/adversarial/` (merged answer: `../merged-output.md`)
- fallback_mode: false (three advocate agents spawned in parallel; diff analysis, scoring, plan and merge done by this worker in-context, recorded in `return-contract.yaml`)
