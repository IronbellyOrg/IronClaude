# Round 1 advocate statement: Variant 1 (owner-approved user-level reinstall at the merge commit)

Persona: devops (delivery, reliability, operational speed). Depth: quick. Facts checked read-only on 2026-11-14.

## Position summary

Variant 1 is the only route that changes the binary the coordinator actually runs on this host, and it does so within minutes of the PR #539 merge, at a pinned and reviewed commit. The Coder template route (Variant 2) is the right long-term channel, but on this host it cannot pass SWEEP-RUNNABLE by itself, because the shadowing user-level install lives on a persistent home volume. Variant 1 should be adopted with its open item closed: the user-level install is removed once the Coder pin bump reaches this workspace.

## Steelman of Variant 2

Variant 2 follows the owner's own stated rule word for word: "nobody updates IronClaude in place; updates reach workspaces only through the Coder template and workspace updates" (`~/.claude/projects/-home-coder-workspaces-IronClaude/memory/ironclaude-updates-only-via-coder.md`, line 11). It needs no exception and leaves no drift between workspaces. Its delivery path is also the better-engineered one: the image pins a 40-hex SHA with provenance gates (`Dockerfile.coder` lines 288 and the FR-PROV checks after it), and the monitor proves the candidate SHA at the real `uv tool install` boundary before it even opens the bump PR (`ironclaude-upstream-monitor.yml`, the "Build/install-boundary proof PASSED" PR body near lines 325-345). Its `workflow_dispatch` trigger (line 13) removes the daily wait (U-002). Every engineer ends up on the same reviewed CLI, and Variant 2 honestly names the shadowing install as its own risk (variant-2 line 23).

## Steelman of Variant 3

Variant 3 spends nothing and risks nothing now. Q29 sits in W3 (`merged-requirements.md:523`, `:556`), so the gate is not on the critical path today. The Coder monitor runs daily (`ironclaude-upstream-monitor.yml` line 12), so the template may deliver the sweep with nobody acting (U-003), and the question would then be asked with real, current facts instead of forecasts. It keeps the owner rule intact and is the spec's stated default (`question.md` line 15), so it is also the zero-decision fallback.

## Key strengths claimed

1. It is the only variant that reaches the binary the coordinator runs. `which -a superclaude` prints `/home/coder/.local/bin/superclaude` before `/usr/local/bin/superclaude`, and `PATH` lists `/home/coder/.local/bin` before `/usr/local/bin` (checked 2026-11-14). The user-level receipt pins `d2d8a2d16` with entry points `ic` and `superclaude` (`~/.local/share/uv/tools/superclaude/uv-receipt.toml`). Replacing that install is the change that matters.
2. New evidence: the shadow survives a workspace update. `/home/coder` is a per-workspace named Docker volume (`Coder/templates/VSCode-AIDev02/main.tf:174-176` `docker_volume "home"`, mounted at `/home/coder` at `main.tf:594-596`), and the template's own comment says "every `coder update` ... while /home/coder persisted" (`main.tf:584-585`). So `~/.local/bin/superclaude` stays after a template update, and the image install keeps losing on `PATH`. This turns the UNVERIFIED in `question.md` fact 7 and Variant 2 line 27 into a verified fact against Variants 2 and 3.
3. Speed: SWEEP-RUNNABLE within minutes of SW-05, so XC-04 can run the same day (variant-1 lines 12, 16).
4. Provenance discipline: the install is pinned to the merge commit, never a branch (variant-1 line 23, U-001). That is the same `git+https://github.com/IronbellyOrg/IronClaude@<sha>` form the image uses (`Dockerfile.coder` install URL line) and the same form the existing user receipt already records.
5. No restart of running sessions. The `main.tf:583-587` comment shows a template update gives the container a new identity and once "left Orca down after each template update". A user-level reinstall touches neither the container nor Orca.
6. The gate check is defined and cheap: `superclaude sweep --help` exits 0 and `/sc:sweep` writes one report (`merged-requirements.md:601`). The sweep skill's first step calls plain `superclaude sweep run` (`sc-sweep-protocol/SKILL.md:23`), which resolves to the reinstalled binary.

## Weaknesses identified in Variant 2

1. It does not pass the gate on this host. Because `/home/coder` persists (`main.tf:594-596`), the template update leaves `~/.local/bin/superclaude` at `d2d8a2d16` first on `PATH`, so `superclaude sweep --help` still prints "No such command" and the `/sc:sweep` fallback does not fire on that error (`SKILL.md:24`). Variant 2 admits this (line 23) but proposes no step to fix it, so as written it fails its own step 3.
2. Removing the shadowing install is itself a host change made outside the template. Once that step is added, Variant 2 is no longer "template only" either; the difference from Variant 1 shrinks to which way the host change goes (remove versus replace).
3. Slowest path with the most hand-offs: monitor run, Coder PR review, contract build ("reviewers should require the AIDev02 contract build ... to pass before merging", monitor PR body), image build, template push, workspace update.
4. The workspace update very likely ends running sessions: a new container per `coder update` is strongly indicated by `main.tf:583-587`. That the coordinator and Orca processes end is an inference, not observed (UNVERIFIED).

## Weaknesses identified in Variant 3

1. On this host the gate cannot pass "on its own": the persistent home volume keeps the shadow (same evidence as above), so Variant 3 step 3 ("the gate holds without a decision") will not happen, and the question returns with the same options plus lost time.
2. The coordinator runs without its designed WC-16 duty, and XC-04 and everything downstream wait for an unbounded time (variant-3 line 21; `merged-requirements.md:601`).
3. It resolves nothing ("Everything Q29 asks", variant-3 line 27), so the owner pays the decision cost later with no new information that changes the options.

## Concessions

1. Variant 1 breaks the owner's stated rule and needs an explicit, recorded exception (variant-1 line 21). This is the real cost, and the owner may rightly refuse it.
2. The owner rule was written at 2026-11-12 15:02 (memory `modified`), and the existing user-level install was written 2026-11-12 22:12 (`question.md` fact 3; `~/.local/bin/superclaude` link time Nov 12 22:12). Who made it is UNVERIFIED. Variant 1 builds on an install the owner may not have sanctioned, and it would make that stray install deliberate.
3. Variant 1 leaves host drift: this host runs a newer CLI than other workspaces until the pin bump lands. Variant 1's "What stays unresolved" (line 27) leaves the cleanup undated; it should be closed by a concrete rule: remove the user-level install (`uv tool uninstall superclaude`, owner-approved) once the image pin is at or past the merge commit and the workspace is updated. That command is a recommendation, not run here.
4. `--force` replaces the `ic` entry point too; whether anything depends on `ic` at `d2d8a2d16` is UNVERIFIED (A-002).
5. Variant 2's provenance (install-boundary proof plus contract build) is stronger than one hand-run install.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 (coordinator resolves `superclaude` through the same `PATH`) | QUALIFY | Likely but not proven. This shell's `PATH` has `~/.local/bin` before `/usr/local/bin` (checked 2026-11-14), and ccsession requires `~/.local/bin` on `PATH` (`~/.claude/skills/ccsession-tag/README.md:38`, `:737`). An Orca-started session's `PATH` was not inspected (UNVERIFIED). The SWEEP-RUNNABLE check must run in the coordinator's own session, as `merged-requirements.md:601` already says, whichever route is picked. |
| A-002 (replacing or removing the user-level install is safe) | QUALIFY | The receipt lists only `ic` and `superclaude` (`uv-receipt.toml`). Both routes touch it: V1 replaces it, V2 must remove it. Nothing found that depends on `ic`, but no full search was run (UNVERIFIED). A one-line grep for `ic ` callers before the change is cheap insurance. |
| A-003 (neither `superclaude install` nor `make sync-dev` upgrades the CLI) | ACCEPT | `merged-requirements.md:1154` states it, and those commands copy primitives, not the uv tool venv. |
| A-004 (the `uv run` fallback does not fire on "No such command") | ACCEPT | `sc-sweep-protocol/SKILL.md:24`: "Only when step 1 fails with 'command not found' ... No other failure leads to this step." |

## Per-point verdicts

| Point | Superior variant | One-line reason |
|---|---|---|
| S-001 | Tie | All three share the same five sections and four steps; no structural edge. |
| C-001 | V1 | The only route that changes the binary first on `PATH`; V2 alone leaves the persistent shadow in place (`main.tf:594-596`). |
| C-002 | V1 | Minutes versus a day plus a PR, build and update (V2) or unbounded (V3). |
| C-003 | V2 | Every workspace gets the same reviewed pin; V1 drifts this host until cleanup. |
| C-004 | V1 | No container recreate; `main.tf:583-587` indicates a template update gives a new container that once left Orca down. |
| X-001 | V2 | It follows the owner rule outright; V1 needs an exception and V3 follows it only by doing nothing. |
| X-002 | V1 | V1 is the only variant whose route actually changes what the coordinator runs; V2 and V3 both concede the template alone does not. |
| X-003 | V2 | Image-built, install-proven, reviewed pin beats one hand-run install, even pinned. |
| A-001 | Tie (all exposed) | All three reason from the observed `PATH`; the gate check in the coordinator's own session covers every variant equally. |
| A-002 | V1 (slightly) | V1 replaces like with like (same tool, same entry points); V2 must remove it with no replacement on `~/.local/bin`, and still needs the same safety check. |

## Overall pick

Variant 1, with a recorded owner exception and a dated rule to remove the user-level install once the Coder pin bump reaches this workspace; Variant 2 stays the long-term channel.
