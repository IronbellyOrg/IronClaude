# Reviewer 1 brief (persona: analyzer)

Mode UC-1 (pre-execution). You are read-only: return findings, run nothing, edit nothing.
Persona: analyzer. Audit the plan for defects that would make a task fail, an acceptance criterion unmeetable, or a step contradict a constraint.

## T1 card excerpt

## Deviation / risk section (analyzer slice)

- **F1 (Medium) Plan AC cannot be met as written.** T5.AC2 requires `make verify-sync` to pass (tasklist:82) while the Constraints allow exactly four files (tasklist:19). `verify-sync` diffs `src/superclaude/skills/*` against `.claude/skills/*` (Makefile:171-178), so any edit to `src/.../ccsession-tag/` drifts from the `.claude/` copy until `make sync-dev` runs. The plan has no `make sync-dev` step. The prior run hit this: `.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t5-checks.log:28-35` (Drift detected, then `make sync-dev`, then pass).
- **F2 (Medium) No task captures the baseline for T4.AC4.** T4.AC4 (tasklist:70) compares the pids of the live shims on ports 4013 and 4114 "before and after", but no earlier task says to record the "before" pids. The prior run created `artifacts/live-pids-before.txt` on its own.
- **F3 (minor) Line anchors are stale against HEAD.** Tasklist:64 says ccsession lines 801-804 (HEAD: 1033-1038); tasklist:52 says proxy lines 857-872 (HEAD: `__main__` at 1009); tasklist:29 says `test_a_busy_shim...` near line 1379 (HEAD: 1861), `StandInGateway` 488 (HEAD: 739), `_free_port` 568 (HEAD: 819), `_ask_raw` 1051 (HEAD: 1464), `_real_launch` 1344 (HEAD: 1757); tasklist:21 says `pgrep -f --` at ccsession:722 (HEAD: 932). Symbol names are also given, so the cost is a wasted search, not a wrong edit.
- **F4 (minor) T1.AC3 over-claims.** Tasklist:34 says "no shim or sleep process", but the stated check, `pgrep -f <tmp copy path>`, matches only the shim: the fake `claude` is `exec sleep 60`, whose argv does not contain the copy path.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T20:01Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:19-21

```markdown
- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:52-52

```markdown
In `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` `__main__` (lines 857-872), before `ThreadingServer(LISTEN, Handler)` binds, call `os.setsid()` inside `try/except OSError: pass` (it raises when the process already leads a process group, for example when run by hand in an interactive shell), with a short comment saying why: a shim is shared by many sessions, so terminal or process-group signals aimed at the session that started it must not reach it. No fork, no new import (`os` is already imported), argv and env unchanged.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:64-64

```markdown
In `src/superclaude/skills/ccsession-tag/ccsession` `setup_shim`, wrap the start statement at lines 801-804 (`GW_PROXY_UPSTREAM=... GW_PROXY_PORT=... CCSESSION_DIR=... nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &`) in a `( ... )` subshell so the subshell exits at once and the shim is no longer a descendant of the launching terminal (Orca kills a closed terminal's descendants; issue #341). Update the comment above it (lines 799-800) to say this, keep the env assignments and the redirect, keep bash 3.2 syntax. The listener and health waits that follow (lines 805-824) stay unchanged.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:69-70

```markdown
- Live check against the changed source: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree root> <a private mktemp -d scratch dir>` (starts a throwaway shim on a free port through the real ccsession and kills only processes it started) writes its output to `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/after.txt`, which shows `shim is a descendant of the terminal: False`, `stream finished: True`, the port still answering, and the surviving throwaway shim stopped by its pid; the scratch dir is removed afterwards.
- The live shims on ports 4013 and 4114 report the same pids before and after (`curl -s http://127.0.0.1:<port>/__ccsession_shim`), recorded in ./artifacts/t4-tests.log.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:78-82

```markdown
In `CHANGELOG.md` under `## [Unreleased]`, add a `### ccsession: shim survives its launching terminal (#341)` section with a `#### Fixed` bullet in plain words: the shared gateway shim was started inside the terminal that first launched it, so closing that terminal (Orca kills its descendants) cut every other session's reply and refused new ones until a later launch started a new shim; ccsession now starts it from a subshell and the shim starts its own session, so it keeps running until stopped (`pkill -f local-gateway-alias-proxy.py`).

Acceptance criteria:
- The new section sits directly under `## [Unreleased]`, references #341, and names no file outside the scope.
- Every test file that reads the edited files (found with `grep -rlE "local-gateway-alias-proxy|ccsession-tag" tests/` and listed in ./artifacts/t5-checks.log) passes, and `make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log.
```

### Makefile:166-181

```make
verify-sync:
	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
	@drift=0; \
	echo ""; \
	echo "=== Skills ==="; \
	for skill_dir in src/superclaude/skills/*/; do \
		name=$$(basename "$$skill_dir"); \
		case "$$name" in __*) continue;; esac; \
		if [ ! -d ".claude/skills/$$name" ]; then \
			echo "  ❌ MISSING in .claude/skills/: $$name"; \
			drift=1; \
		else \
			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
			if [ -n "$$changes" ]; then \
				echo "  ⚠️  DIFFERS: $$name"; \
				echo "$$changes" | sed 's/^/      /'; \
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t5-checks.log:23-38

```
$ make verify-sync

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
make: *** [Makefile:168: verify-sync] Error 1
rc=2
$ make sync-dev   # this fresh worktree had no gitignored .claude/ dev copies; sync-dev fills the worktree .claude/ only
   Hooks:     12 files
   Templates: 52 files
rc=0
$ make verify-sync
=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

```

### src/superclaude/skills/ccsession-tag/ccsession:1033-1038

```bash
    (
      GW_PROXY_UPSTREAM="$ANTHROPIC_BASE_URL" \
        GW_PROXY_PORT="$CC_SHIM_PORT" \
        CCSESSION_DIR="$CCSESSION_DIR" \
        nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &
    )
```

### src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1009-1022

```python
if __name__ == "__main__":
    host, port = LISTEN
    # One shim serves every session on its port, so signals aimed at the
    # terminal session or process group that started it must not reach it
    # (issue #341). Run by hand with output on a terminal, it stays there so
    # Ctrl-C still stops it; setsid fails harmlessly for a group leader.
    if not sys.stderr.isatty():
        try:
            os.setsid()
        except OSError:
            pass
    if upstream_is_self():
        print(
            f"[proxy] ERROR: upstream {UPSTREAM} is this shim's own address; "
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| T5.AC2 verify-sync pass | F1 | gap (no sync-dev step) | Makefile:171-178 |
| T4.AC4 live pid before/after | F2 | gap (no baseline step) | tasklist:70 |
| line anchors | F3 | stale | tasklist:29,52,64 |
| T1.AC3 sleep check | F4 | over-claim | tasklist:34 |
