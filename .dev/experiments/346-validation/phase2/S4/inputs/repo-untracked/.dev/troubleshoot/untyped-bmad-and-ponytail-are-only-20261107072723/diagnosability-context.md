# Diagnosability Context Card

**Issue**: BMAD and Ponytail are only accessible on projects where the user has previously installed them but are not installed by default on all projects or available globally; BMAD in a never-installed project should create the directories it needs.
**failing_component**: templates/VSCode-AIDev02/image/catalogue/bmad/install.sh (called from templates/VSCode-AIDev02/image/scripts/startup.sh section 9)
**Verdict**: partial
**Complexity**: trivial (score 0: no intermittent/perf/security keywords, no --scope, no stack trace, cause class not in {race, stale state, performance, substituted primitive})
**Hard-stop fired**: false
**Round**: 0 of 3 (no tasklist with discriminator-required: yes; counter not incremented)
**Captured bytes (failing run)**: n/a (audit-time only; no failing-run log supplied)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | partial | install.sh:15 prints a timestamp; marker is written for success, skip and untouched alike (install.sh:58-60); only the /tmp log (truncated each boot, startup.sh:1176) shows which branch ran. |
| Where | no | install.sh never prints D; no message names any repo other than the seed path read from seed-repo-path. |
| Why   | partial | install.sh:23 merges four causes; the real reason is in ~/.aidev/status/seed-repo-outcome and /tmp/initial-repos.log (startup.sh:664-671); the health record carries configured_state=Installed-not-Configured (spec2-health.sh:143). |

## Branch A: Log-call inventory

About 40 echo/printf/handler sites across install.sh, startup.sh section 9 and spec2-health.sh (see wave1_6-branch-A.md). Types: echo/printf status lines dominate; silent constructs at install.sh:21,22,28,58 and startup.sh:678-679,1187. Exception-handler richness: rich 2 (install.sh:51, startup.sh:1217-1243), minimal 3, silent 6+. `degraded`: true.

## Branch B: Log-config reachability

Single sink for install.sh output: /tmp/catalogue-bmad.log (install.sh:13; truncated each boot at startup.sh:1176). Health record carries state, not configure result (spec2-health.sh:340-355). No env var controls verbosity. Reachability: every install.sh emission reaches the log (source-level); failure-path health diag is empty by construction (startup.sh:1240-1243; spec2-health.sh:345). `degraded`: true.

## Sufficiency rubric application

Row fired: S9 (only echo/print statements, no structured logger), deterministic, so `partial`. Reason: the symptom is a deterministic design behaviour (no seed repo means nothing configured), and the facts needed for diagnosis are static (code, specs), not runtime-only; but the runtime evidence for a specific user's boot (which branch ran, which profile, whether Ponytail loaded) is not captured in any persistent artifact. S14 not applicable: the disputed datum is code behaviour, not a value hidden by a filter layer. Auggie unavailable, so the verdict is capped at `partial` anyway.

## Implication for diagnosis confidence

Existing instrumentation: install.sh echoes to an ephemeral /tmp log; health record shows Installed-not-Configured. Gap: no persistent record of which repo, profile or branch applied, and none of Ponytail's activation. Consequence: the diagnosis below rests on static code and owner-decision documents, not on a captured failing boot; runtime claims about a specific workspace stay UNVERIFIED. Next step: proceed; to verify at runtime, read the existing artifacts listed in the tasklist on an affected workspace.

## Tasklist reference

/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/diagnosability-tasklist.md
