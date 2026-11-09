# Wave 1.6 Branch A: log-call inspection (returned by troubleshoot-analyst; persisted by parent, condensed to load-bearing rows)

branch: A; degraded: true (auggie unavailable; shell not indexed by codegraph; Read/Grep used); captured_bytes: null (none supplied)
query_target: templates/VSCode-AIDev02/image/catalogue/bmad/install.sh + scripts/startup.sh section 9 (about 1086-1278) + scripts/lib/spec2-health.sh bmad case (paths relative to templates/VSCode-AIDev02/image/)

## Hits (file:line | type | note)
- catalogue/bmad/install.sh:13 | tee to log | all output to /tmp/catalogue-bmad.log; startup.sh:1174-1176 redirects the same file with `>` (truncates each boot)
- install.sh:15 | echo | "install.sh start: <date>" gives WHEN; no repo path or profile
- install.sh:18 | echo+exit 2 | CLI missing; only distinct exit code
- install.sh:21 | `|| true` (silent) | missing/empty seed-repo-path becomes D="" with no log of the file's absence
- install.sh:22 | stderr discarded (silent) | one condition covers four causes: path file absent, empty, not a directory, not a git repo
- install.sh:23 | echo | "no seed repo recorded; nothing to configure": the symptom line for a repo-less boot; exits 0 and falls through to the marker
- install.sh:24-25 | guard+echo | existing/partial `_bmad` counts as configured; no auto-repair (comment line 41)
- install.sh:28-34 | silent state change | edits the repo's info/exclude with no log line
- install.sh:40-46 | echo/handler | target dir not printed; `timeout 120` exit 124 not distinguished; FAIL lines exit 1 with no marker
- install.sh:51 | diff on git status change | rich
- install.sh:54 | echo | "seed repo configured; git status unchanged": only success line proving configuration; D not printed
- install.sh:58-60 | marker write+echo | marker is written on skip (23), untouched (25) and configured (54), same content; prints "install ok" after the line-23 no-op
- scripts/startup.sh:664-671 | printf | §8 outcome (cloned, preserved-valid, skipped, rejected-input, destination-conflict, runner-unavailable) goes to /tmp/initial-repos.log and ~/.aidev/status/seed-repo-outcome; install.sh never reads them
- startup.sh:678-679 | silent | seed-repo-path written only for cloned/preserved-valid; removed otherwise with no log
- startup.sh:1165,1169 | echo | unresolved profile / out-of-profile skips BMAD; no health record
- startup.sh:1174-1176 | subshell redirect | BMAD runs without the 30 s watchdog; output only in /tmp (not persistent across restarts)
- startup.sh:1184 | echo | "installed." fires on exit 0 including the line-23 no-op: reads as success with no repo configured
- startup.sh:1187 | `|| true` | health outcome swallowed (still persisted/echoed by spec2_health_run)
- startup.sh:1217-1243 | handler | install-failed path gives exit code, log path, install-failed health record (exit 1/2 only, not the exit-0 skip)
- scripts/lib/spec2-health.sh:77,99-112 | health requirement | `seed-config` observed only if `<seed>/_bmad/_config/manifest.yaml` exists or tracked `.claude/skills/bmad-*/SKILL.md`; seed repo only
- spec2-health.sh:143 | classify | repo-less boot => configured_state=Installed-not-Configured, stored in ~/.aidev/status/spec2-health/bmad.health.v1: the right signal for this symptom
- spec2-health.sh:469 | echo | prints state healthy (probe is `bmad --version`) without configured_state

## Operator questions
- WHEN configured in repo X: partly, seed repo only; marker is written for success, skip and untouched alike.
- WHERE: not answerable; install.sh never prints D and no message mentions any non-seed repo.
- WHY not configured: partly; line 23 collapses four causes; the real reason is in ~/.aidev/status/seed-repo-outcome and /tmp/initial-repos.log.
- Which message reveals the requirement gap: only configured_state=Installed-not-Configured and the conditional welcome text (manifest.yaml:12-14).

## Unverified (worker)
- startup.sh around :431 (aidev_seed_dest derivation) not read; whether ~/.aienv exists at boot not checked; runtime contents of /tmp/catalogue-bmad.log, seed-repo-outcome and bmad.health.v1 not inspected.
