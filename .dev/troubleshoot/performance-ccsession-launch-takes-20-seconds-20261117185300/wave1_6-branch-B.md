# Wave 1.6 Branch B (log-config inspection), persisted by the parent on receipt

Returned by troubleshoot-analyst; condensed by the parent (the worker's list of 13 config items is kept in substance). I = /home/coder/.claude/skills/ccsession-tag/ccsession (2072 lines = origin/master 10f6ec670).

Result: `timing_or_debug_switch_exists: false`.

Config items found (none is a debug, verbose or timing switch for the listing path):

- NO_COLOR, I:1711: colour only.
- CCSESSION_ASK_TIMEOUT, I:1736: default 30 s limit on the question; it starts after the list is printed (show_saved at I:1732), so it does not bound the listing.
- CCSESSION_MODELS_VERBOSE=1, I:1873: only inside `--refresh-models`.
- CCSESSION_MODELS_REFRESH / CCSESSION_MODELS_WAIT, I:1930-1931: launch-time model-data refresh, default wait 2 s. Worker did not check whether `--here`/`--ask` (I:1887, 1897) run before or after that block.
- CCSESSION_AUTO_NAME_STAMP I:691 (test hook), CCSESSION_PROFILES_DIR I:871, CCSESSION_ENV_FILE I:902, CCSESSION_PERMISSIONS I:135, CCSESSION_LAUNCH_ID/LAUNCH_CWD/TOPIC_CWD/NAME_KEY I:1985, tier/compaction variables I:1279; ccsession-orca CCSESSION_AUTOSTART :147 and CCSESSION_NAME :130; ccsession.env.example names (lines 15-29), README-only variables (README:640, 649, 272): none is a log setting.

Worker note: greps of ccsession and ccsession-orca for `set -x`, xtrace, PS4, BASH_XTRACEFD, DEBUG, TRACE, VERBOSE and TIMING found nothing for the listing path; the only time-related hits are fixed limits (curl --max-time 2 at I:979, a lock timeout at I:449-458, the ask timeout) and the birth/mtime `stat` calls (I:1485-1516). The worker read ccsession-orca matches from grep output only, did not read past I:1583 of list_sessions, and says README:648 was omitted for length. To measure the 27 s the parent must use an external measurement (bash -x with PS4 including EPOCHREALTIME), which the parent has already done (tier1-observation.md).
