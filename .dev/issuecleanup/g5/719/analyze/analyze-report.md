# Report-server architecture analysis

## Scope and provenance
Command: `/sc:analyze .dev/issuecleanup/g5/719/source/agent-work-report --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g5/719/analyze`.

Current checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The skill and its tests are absent: the targeted `git ls-tree` on HEAD returned no paths. Local history and merged PR #700 identify removal at `471f10511c8e2e8176c0e2088720ece03beca317`.

The target is a four-file evidence snapshot copied from local archive tag `archive/pr-684-agent-work-report`, commit `d7d645dddd42e49a72a734f9c8b6952bcbcb4527`, not restored production code or a runnable skill installation. The archived tests are preserved separately in the report's source/tests directory. Using this narrow retained source avoids scanning unrelated current skills or silently restoring removed code.

## Findings
1. **P2, excessive serving scope.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/scripts/page.py:318-327` launches generic `http.server` with the whole state directory, not a report-only directory. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/scripts/common.py:59-68` puts state and runs together. There is no application Host check, token or allowlisted request path in this startup. The local standard-library implementation confirms directory listing and arbitrary readable-file serving at `/usr/lib/python3.13/http/server.py:700-734`; this corroborates the mechanism but does not establish which interpreter a different host uses.
2. **P2, no listener identity check.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/scripts/page.py:313-315` and `:334-337` accept a successful response without reading a report marker. A foreign listener returning success for the report URL is reused. A mere listener returning an HTTP error is not accepted, so the issue's phrase 'anything that answers' is too broad.
3. **P2, third-party page load.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/templates/report-template.html:8-10` loads external fonts. The same template already provides a report identity marker at line 7.
4. **P2 restoration acceptance gap.** Searches across the archived 4,005-line test file found no `ensure_server`, `http.server` or `8765` matches. Rendering and link-sanitization tests exist, but no direct server checks were found by those searches. The detached process has no stop handling in the startup function; the archived skill's delivery instructions describe starting/reusing it, not how to stop it. These remain acceptance work, not runtime-tested claims.

## Metrics and impact
Inspected four archived skill files (two Python helpers, one HTML template and the skill instructions), the archived test file by targeted search, current tree/history and live issues/PR metadata. Codegraph identified `open_tab -> ensure_server -> state_dir`; the actual caller at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/719/source/agent-work-report/scripts/page.py:351` was read directly. Graph impact is three symbols in the archived page module; the change also reaches report-copy refresh behavior, URL/tab reuse, the template, instructions and regression tests. Graph search is not proof of absence elsewhere.

No active production server was observed or asserted. Removing the skill from this checkout does not prove that older installed copies or already-detached servers stopped.

## Recommendations
Keep #719 open as a security gate for the parked #720 restore. When that restore is authorized, isolate the served copy of report.html, restrict request paths and Host, disable directory listing, verify the report marker before reuse, drop or bundle fonts, state process lifetime and stopping instructions, and record the URL-token decision. Keep the served copy fresh on both normal generation and living-report refresh. At least the three issue-required rejection tests must run on restored code, with evidence for the listener, fonts and lifetime requirements. Do not build or restore anything in this review run.

## Verification limits
Static quick review only. No UV, tests, server, browser, exploit or skill code was run; no production files, Git index, commits or GitHub state were changed. DNS-rebinding exploitation, Coder forwarding, other installed copies and process lifetimes on other hosts are UNVERIFIED. The allowed gh view fields expose PR descriptions, general comments and review summaries, not the linked inline discussion: its precise resolution and reply are UNVERIFIED independently of the issue's account.

Codegraph: index_state=fresh, checked_at=2026-11-24T14:06:31Z; degraded: none

All graph lookups used the explicit Issuecleanup worktree root. Source and call-site findings were confirmed with Read/Grep. The snapshot is evidence only and omits dependencies needed to run the skill.
