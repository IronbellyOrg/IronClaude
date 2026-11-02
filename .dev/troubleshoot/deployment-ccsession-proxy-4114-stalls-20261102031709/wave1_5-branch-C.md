# Wave 1.5 Branch C (semantic-restriction extraction) — returned by troubleshoot-analyst

degraded: true (Grep/Read only; install_ccsession.py has no MUST/NEVER wording; nothing mentions setsid)

| source_file:line | applies_to | quoted_text |
|---|---|---|
| src/superclaude/skills/ccsession-tag/ccsession:762 | setup_shim reuse loop | "Never stop another shim: sessions may be attached to it even when no reply is in flight, and a started reply must never be cut off. A shim with other settings or older code is left running; this launch moves on." |
| src/superclaude/skills/ccsession-tag/ccsession:718 | shim_listener_pid | "Images without lsof (the Coder workspace image): a local connect proves a listener, and the shim is found by its script path. Any other listener is reported as \"other\" so it is never killed." (fix must keep the script path in the command line for `pgrep -f`) |
| src/superclaude/skills/ccsession-tag/ccsession:799 | setup_shim start block | "The shim inherits this session's env (tier settings fallback, show-all, cooldown length); it reads the workspace env file itself on each request." (detach must keep passing the env) |
| src/superclaude/skills/ccsession-tag/ccsession:814 | post-start health wait | "Another launch may have won the port at the same moment: attach only to a shim with this session's settings and code." |
| src/superclaude/skills/ccsession-tag/README.md:504 | user-facing lifecycle | "ccsession never stops a running shim by itself, because other sessions may be using it." |
| src/superclaude/skills/ccsession-tag/README.md:415 | documented lifetime | "After an upgrade, new sessions start a new shim on another port; a shim still used by older sessions keeps running until you stop it (`pkill -f local-gateway-alias-proxy.py` when no session uses it)." |
| src/superclaude/skills/ccsession-tag/README.md:36 | portability | "macOS or Linux only. The optional gateway shim uses `python3`, `curl`, and `lsof`." (no setsid binary on macOS) |
| src/superclaude/skills/ccsession-tag/ccsession:351 | portability precedent | "python3 takes it (macOS has no flock command)." |
| src/superclaude/skills/ccsession-tag/ccsession:97 | older macOS tools | "Plain readlink in a loop because older macOS readlink has no -f." |
| src/superclaude/skills/ccsession-tag/ccsession-orca:32 | older macOS tools | same rule in the Orca wrapper |
| src/superclaude/skills/ccsession-tag/ccsession:1179 | bash 3.2 | "python3, not `read -t 0`: bash 3.2 (macOS) fails that without looking." |
| src/superclaude/skills/ccsession-tag/models.py:791 | shim_port | "the launch then moves to another port and never stops the shim that other sessions may be using." |
| src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:78 | shim reuse | "Fixed for the life of this shim; ccsession gives a show-all session its own shim (port) so other sessions' pickers never change." |
| src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:70 | logging | "Persistent audit file is OPT-IN. Unset (default) => log to the terminal only (ephemeral, never accumulates). Set GW_PROXY_LOGFILE=/path to also persist." |
