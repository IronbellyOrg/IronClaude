# Wave 1.6 Branch B: log-config inspection (returned by troubleshoot-analyst; persisted by parent, condensed)

branch: B; degraded: true (auggie unavailable; Grep/Read only; nothing executed, so runtime claims are source-derived). Paths relative to templates/VSCode-AIDev02/image/ unless absolute.

## Config / sink hits
- /tmp/catalogue-bmad.log (file, hard-coded): catalogue/bmad/install.sh:7,13 `exec > >(tee -a "${LOG}") 2>&1`, no level gate.
- Same file, second writer: scripts/startup.sh:1174-1176 `( source ~/.aienv && bash install.sh ) > "${aidev_cat_log}" 2>&1` (truncating `>`, log path assigned :1095). Non-bmad slugs: startup.sh:917-918 via aidev_cat_install.
- Startup-appended lines: startup.sh:1236-1238 (install.sh exit code), welcome text :1193-1206, missing manifest :1131-1132, bad scope :1259-1261.
- Startup stdout/stderr (coder_script `aidev-startup`, templates/VSCode-AIDev02/startup.tf:42-63): summary lines only; for bmad "installed." (:1184) or "install failed (exit N) ... See /tmp/catalogue-bmad.log" (:1239). Coder agent's log file path not defined in this repo (unobserved).
- ~/.aidev/status/spec2-health/bmad.health.v1: state plus last 5 sanitized lines of probe `bmad --version` (manifest.yaml:24-25; scripts/lib/spec2-health.sh:340-355, 373-472; startup.sh:1187-1188). Failure path writes state=install-failed with empty diag (startup.sh:1240-1243; guard spec2-health.sh:345): the install log tail is never copied.
- ~/.aidev/status/readiness: one row per slug `bmad selected|deselected|project` only (startup.sh:1142,1273,1313-1327): no outcome or configured state.
- ~/.aidev/status/welcome/bmad.txt: static manifest text; says "If this workspace has a seed repo, BMad is already set up there" even when install.sh took the "no seed repo recorded" branch.
- /tmp/initial-repos.log, ~/.aidev/status/seed-repo-outcome, ~/.aidev/status/seed-repo-path: startup.sh:649-682; seed-repo-path written only for cloned|preserved-valid and removed otherwise.
- Env controls: none controls bmad/section-9 install verbosity. Existing: AIDEV_CAT_ROOT (:715), AIDEV_SPEC2_HEALTH_LIB (:740), SPEC2_HEALTH_STATUS_DIR (spec2-health.sh:12), AIDEV_HEALTH_TIMEOUT_SECONDS (spec2-health.sh:46-54), AIDEV_PROFILE (:1068). AIDEV_DEBUG gates only lib/aidev/log.sh:24 (not used in install.sh or section 9).
- FR30 contract: catalogue/README.md:176,186-193 (tee all output to /tmp/catalogue-<slug>.log; marker only after verification; static gates do not execute install.sh). test-57 bmad assertions at 434, 443, 451 check only the marker, never the log; test-46 asserts nothing about a bmad install log.
- bmad CLI baked: Dockerfile.coder:133-143.

## Reachability verdicts
- install.sh lines 15, 18, 23, 25, 40, 42, 43, 46, 50, 54, 60: reaches_sink (only sink: /tmp/catalogue-bmad.log); startup.sh:1175: reaches_sink; startup.sh:1240 (failure health record diag): filtered_out (diag empty by construction).

## Worker notes
- install.sh:23 and :25 reach the log only; then :58-60 write the marker and exit 0; startup.sh:1183-1188 counts it installed and records healthy from `bmad --version`. Health and readiness cannot tell "configured the seed repo" from "configured nothing".
- With REPO_URL empty (outcome `skipped`, startup.sh:653) seed-repo-path is removed, so install.sh always takes the :23 branch: BMAD installed, never configured anywhere; user must run the per-repo install by hand (manifest welcome text).
- Sinks are persisted but ephemeral: /tmp log truncated every boot; whether /tmp survives a restart was not observed.
- Unverified inferences: the two writers (startup.sh:1176 plain `>` and install.sh:13 `tee -a`) share the file via different open descriptions and may overlap; coder_script log path unobserved; bmad branch at startup.sh:1174-1176 has no outer timeout (only install.sh:42 `timeout 120`).
- Not read: body of test-46 beyond grep hits; any .github workflow capturing /tmp/catalogue-bmad.log.
