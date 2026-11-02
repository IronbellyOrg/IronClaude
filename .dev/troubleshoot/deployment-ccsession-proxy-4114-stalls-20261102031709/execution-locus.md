# Execution locus card

PRINT-SITE: Claude Code terminal screens of the Orca worker sessions pid 1297298 (pts/9) and pid 2089859 (pts/22) in worktree review-severity-rule: "API Error: Connection lost mid-response" and "Connection refused ... (ECONNREFUSED)".
RUN-SITE: src/superclaude/skills/ccsession-tag/ccsession:801-804 (setup_shim starts `nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &`) and src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:857-872 (`__main__`, serve_forever) @ host coder workspace, process: the shim python3 started as a child of whichever ccsession launch first found the port free (today: pid 2258510, parent claude 2258462, session 2257514 of Orca terminal serve-46e81c2f / term_41eaf7f8, worktree auggie-mcp-regNotConnected).
SAME-ENV: yes (one host, one user; the failing sessions, the shim and this diagnosis all run on the same Coder workspace and are inspected through /proc and ps from this shell).
OBSERVE-VIA: same-shell (read-only /proc, ps, curl of the shim health path, Orca daemon.log reads). Re-run permitted: no for the LIVE shims (hard constraint: never kill or signal pids 1788 / 2258510); yes for a throwaway shim started from this worktree on a free port.

## Arms

- Failing arm: 127.0.0.1:4114 (shim started by an Orca terminal session; dies with it).
  - PRINT-SITE: worker screens above. RUN-SITE: as above. SAME-ENV: yes. OBSERVE-VIA: same-shell.
- Passing arm: 127.0.0.1:4013 (pid 1788, up since 2026-10-31 12:24:43, ppid 1, pgid 369 = Orca's own process group, no controlling tty).
  - CONTROL-PROOF: yes: src/superclaude/skills/ccsession-tag/ccsession:804 (same launch statement; the arm differs only in which process tree it ended up in, observed via ps: ppid 1, pgid 369, tty ?)
