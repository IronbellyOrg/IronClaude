# Architecture analysis: ccsession shim startup

Governing structure: /sc:analyze, Output and Behavioral Flow sections. Command: `/sc:analyze src/superclaude/skills/ccsession-tag --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/352/analyze`.

## Scope and metrics
Quick static architecture review at HEAD `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` on 2026-11-23. The narrow source package contains the Bash launcher and six graph-indexed Python files. Inspection concentrated on launcher startup, the proxy health endpoint, and supporting tier tests, not unrelated session storage. No source was changed or executed. Dynamic tests and live load experiments are outside this command's static-analysis boundary.

## Severity-rated findings
### Medium: startup still has a short polling budget, but causation is UNVERIFIED

`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/ccsession:1252-1265` starts the proxy with output discarded, then checks the listening port ten times with 0.3-second sleeps and exits if no listener appears. This is about three seconds of explicit sleeps, not a strict three-second wall-clock deadline: process scheduling and listener probes add time. A separate ten-check health-match loop follows at lines 1267-1276. The launcher still cannot explain from its startup error alone whether the child crashed, started slowly, or lost a port race. This is a diagnostic and reliability gap, not proof that increasing a wait fixes issue #352.

Historical corroboration: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/done/TASK-WF-fixIronbellyOrgI-20261108-110741/artifacts/t5-runs.md:18-29` records a base+101 startup failure after the gateway-port pairing fix under 28-worker execution; lines 31-48 retain passing reruns without erasing that failure. It explicitly leaves slow startup versus port contention UNVERIFIED.

### Architecture safeguards to preserve

The launcher leaves incompatible existing shims running rather than terminating sessions, checks health identity before exporting the URL, and refuses non-shim owners of the preferred port. Read scope: launcher lines 1181-1283. The existing health endpoint exposes code/settings identity and PID at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:627-659`. Graph calls, callees and impact place that endpoint behind `Handler.do_GET` within the proxy. Bash startup is not graph-indexed, so its relationships were read directly.

## Security and performance
No new exploitable security defect was established by this narrow review. Credential-routing checks must not be weakened to silence a test failure. Performance risk is startup latency under scheduling pressure; its contribution to reported failures remains UNVERIFIED. Maintainability concern: launcher-backed tests and directly started proxy fixtures use different waiting behavior. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/unit/test_ccsession_tiers.py:846-880` polls the HTTP health endpoint up to 50 times; `_real_launch` at lines 1809-1853 instead inherits the environment and invokes the real launcher. No project-wide coverage or complexity score was calculated.

## Recommendations
Keep issue #352 open. In a separate authorized diagnostic run, reproduce whole-file failures under controlled load, retaining child stderr, selected ports, process exit state, inherited shim settings, and health responses. Distinguish delayed readiness, child crashes and port contention before changing the wait. Reuse the existing health endpoint if a readiness fix is supported; add a deterministic delayed-start/crash regression test and retain existing busy-shim and credential-routing assertions. Then meet the issue's repeated under-load whole-file criterion and check CI. No fix or dynamic experiment was attempted here.

## Codegraph
Codegraph: index_state=fresh, checked_at=2026-11-23T23:02:51Z; degraded: none.

Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. One status check reported zero source changes; discovery, proxy outline, health body, callers, callees and impact were consulted. `do_GET` to `_handle_health` call site was confirmed by Read at lines 627-630. The Bash launcher was inspected directly because it was absent from the indexed package file list. Report writes do not alter the reviewed source.
