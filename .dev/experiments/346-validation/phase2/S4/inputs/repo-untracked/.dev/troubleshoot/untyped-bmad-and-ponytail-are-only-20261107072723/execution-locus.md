# Execution locus card

- PRINT-SITE: none. The report is a requirement gap in the user's own words, not a failing log line. Issue text: "BMAD and Ponytail are only accessible on projects where the user has previously installed them ... not available globally to the user." (GitHub issue IronbellyOrg/Coder#478).
- RUN-SITE: unknown. The behaviour is produced at workspace boot inside the AIDev02 image (`templates/VSCode-AIDev02/image/scripts/startup.sh` section 9 runs `catalogue/<slug>/install.sh`), and at Claude Code session start (user settings / project `.claude/skills`). No single emitting `file:line` for a failing line exists.
- SAME-ENV: unknown. The reported environment (a booted AIDev02 workspace vs. a bare checkout) is not named in the issue.
- OBSERVE-VIA: nobody for a fresh workspace boot. Read access exists only to this already-booted workspace's files (`/home/coder/.claude`, `/opt/uv/tools`, `/opt/nvm`) and the repo, as static reads.

re-run permitted: unknown (no re-run is needed; static diagnosis; the issue forbids product-code edits in this run).
