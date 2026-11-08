# Phase 4 web research inventory

Files found: 2 of 2 expected. Files with Status: Complete: 2. Missing: none. Total source URLs cited: 98 (34 + 64 distinct URL strings per file via grep; overlap between files not removed). UNVERIFIED mark lines: 94 (50 + 44, grep -c on the word UNVERIFIED, includes gap-list lines). Both agents recorded `provider=WebSearch reason=tavily-unavailable` for every fact (Tavily MCP was not in their tool list); the fetch tool returns summarized page text. No external claim was CODE-CONTRADICTED in either file.

| File | Topic | Status | Line count | URL count | UNVERIFIED count | Key External Findings (one line) |
|---|---|---|---|---|---|---|
| research/web-01-github-events-projects-and-limits.md | GitHub Actions schedule/event limits, Projects v2 access, token types, rate limits, polling | Complete | 233 | 34 | 50 | A scheduled Action runs at most every 5 minutes, can be delayed or dropped, default branch only; no workflow trigger reacts to a Project Status change; reading an org Project needs classic `read:project`, fine-grained org Projects Read, or a GitHub App, and `GITHUB_TOKEN` cannot; 12 polls/hour is about 0.24% of a login's 5,000/hour; only `gh project item-list --query` can filter on Status. |
| research/web-02-coder-claude-dispatch-and-security.md | Coder reachability and APIs, Claude Code headless and Action, dispatchers, prompt injection, at-most-once, sender auth, contract | Complete | 374 | 64 | 44 | `coder_script` with a 6-field cron is the documented 5-minute in-workspace job and runs only while the workspace runs (not counted as activity); `claude -p "/skill-name"` expands custom commands per the official page; no GitHub primitive gives atomic exclusion across logins; push options B/C need sender authentication, app-share levels and a minimal contract (marked proposal) and the listener lives in the Coder repo (#477). |

## UNVERIFIED and CODE-CONTRADICTED items

CODE-CONTRADICTED: none in either file.

### web-01 (13 UNVERIFIED items plus 2 scope notes)
1. Primary-page sentence that `projects_v2_item` is not a workflow trigger (only absence from the trigger list seen).
2. Primary-page statement that repository-scoped `GITHUB_TOKEN` cannot read an organization Project (secondary gh-aw page only).
3. Whether Projects REST `q` and `gh project item-list --query` accept `status:Backlog`, `label:`, `assignee:@me` and custom field filters.
4. Whether `gh issue list --json projectItems` exposes the Status name; gh version.
5. GraphQL conditional requests (ETag/304); Projects REST items ETag/304.
6. Whether `gh` high-level commands can send `If-None-Match`.
7. Organization policies that could block option A's tokens (classic PAT restriction, fine-grained approval, SSO).
8. Whether `GH_TOKEN`-injected logins can add scopes via `gh auth refresh`.
9. Retention of issue events; whether a Projects Status change appears in the timeline; detecting a post-approval body edit.
10. Webhook redelivery window and ordering guarantee.
11. Per-job billing rounding; whether search shares the 5,000/hour bucket; private-repo `schedule` differences.
12. Who besides Triage-or-above can apply labels; permission to edit another user's issue body.
13. Multi-assignee behavior when two logins race.
Scope notes: sender authentication and Coder app sharing are covered in web-02; the fetch tool truncated several long pages.

### web-02 (16 gap-table items)
1. Tavily unavailable; WebFetch returns summarized text (provenance note).
2. Whether a still-running `coder_script` cron job overlaps the next tick and what the agent does with cron when the workspace stops.
3. Whether `$HOME` is on a persistent volume in the target template.
4. systemd or system cron availability in the workspace image; whether a daemonized child of `run_on_start` survives.
5. Whether an Orca-launched interactive Claude session counts as Coder "activity".
6. `coder exec` not found in docs; `coder ssh <workspace> <command>` exists.
7. REST endpoint to start a workspace not read (B/C only).
8. Coder app proxy support for `Coder-Session-Token` for non-browser callers as a documented feature (B/C only).
9. Coder passing client certificates (mTLS) to a workspace listener (B/C only).
10. Whether Coder external auth always uses the workspace owner's identity; token refresh behavior.
11. Copilot assign-issue steps (search snippets only), Codex issue-to-agent path, Sweep not researched.
12. Detecting an issue-body edit after approval; `gh` coverage of issue events.
13. `read:project` scope and the JSON schema of `gh project item-list`.
14. ETag/304 treatment of polling; key rotation of GitHub OIDC keys.
15. `claude -p "/sc:issue --claim <N>"` end-to-end behavior in this repo; the Orca `--prompt` route.
16. [STALE DOC, third party] an old third-party mirror claims slash commands are interactive-only.
