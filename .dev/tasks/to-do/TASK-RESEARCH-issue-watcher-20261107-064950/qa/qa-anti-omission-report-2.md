# Anti-Omission Report 2 (web-01, web-02, synth-02, synth-03, synth-04)

Status: Complete
Date: 2026-11-07
VERDICT: PASS

## Anti-Omission Report

Report reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (2,176 lines)
Input files checked: web-01 (233 lines), web-02 (374 lines), synth-02 (467 lines), synth-03 (540 lines), synth-04 (553 lines); plus research-notes.md addenda for conformance.
Date: 2026-11-07

Method: coverage judged by meaning, not by ID citation. Enumeration is appended per input file below. Report line numbers (L) refer to RESEARCH-REPORT-issue-watcher.md as read on 2026-11-07. Classification: R = REPRESENTED, D = COVERED-BY-DEDUP, O = OMITTED. Severity of each omission: CRITICAL (distinct foundational finding), IMPORTANT (distinct secondary finding), MINOR (redundant or low-relevance detail). Verdict rule: FAIL only for an unjustified omission rated CRITICAL or IMPORTANT of a distinct finding; MINOR omissions are listed and flagged but are not blocking.

## Part 1: web-01-github-events-projects-and-limits.md (233 lines)

| ID | Finding (web-01 section) | Class | Where in report / note |
|---|---|---|---|
| W1-01 | Schedule floor of 5 minutes (s1) | R | 5.1 L762 |
| W1-02 | Schedule can be delayed; queued jobs may be dropped (s1) | R | 5.1 L762 |
| W1-03 | Scheduled workflows only on default branch, file must exist there (s1) | R | 5.1 L763 |
| W1-04 | Public repo schedules auto-disabled after 60 days inactivity; fork is public (s1) | R | 5.1 L763 |
| W1-05 | No private-repo-specific schedule rule stated [UNVERIFIED] (s1) | R | 5.1 L763 |
| W1-06 | Repo has no schedule workflow; consistent (s1) | R | 5.1 L762, 2.3 L319 |
| W1-07 | Full `issues` activity-type list (s2) | R | 5.1 L764 |
| W1-08 | No issues activity type for Project Status change (s2) | R | 5.1 L764 |
| W1-09 | `field_added`/`field_removed` meaning UNVERIFIED (s2) | R | 5.1 L764 |
| W1-10 | `issue_comment` types and `label` event semantics (s2) | R | 5.1 L765 |
| W1-11 | Webhook permission for issues events (App Issues read; repo/org/App webhooks) (s2) | R | 5.2 L775 |
| W1-12 | `projects_v2_item`: org availability, App needs Projects read, actions list, `changes` object, sibling events (s3) | R | 5.2 L772 |
| W1-13 | `projects_v2_item` not a workflow trigger (absence evidence; explicit sentence UNVERIFIED) (s3) | R | 5.2 L773 |
| W1-14 | Three ways to react to a Status change (poll, org webhook/App, scheduled Action with PAT/App token) (s3) | R | 5.2 L774 |
| W1-15 | User primary REST limit 5,000/h shared across tokens/apps (s4) | R | 5.4 L796 |
| W1-16 | Enterprise Cloud user limit 15,000/h and the note that higher-limit app traffic still consumes the user's lower allowance (s4) | O | Not found (L796 mentions Enterprise Cloud only as a cap qualifier). MINOR (source relevance LOW) |
| W1-17 | GitHub App installation 5,000 base, +50 per repo and per org user beyond 20, cap 12,500 (s4) | R | 5.4 L796 (cap stated; the +50 scaling rule not stated: part of the same row, MINOR) |
| W1-18 | Actions GITHUB_TOKEN 1,000/h per repo (s4) | R | 5.4 L796 |
| W1-19 | REST secondary limits (100 concurrent, 900 pts/min REST, 2,000 GraphQL, point costs, content creation 80/min 500/h) (s4) | R | 5.4 L797 |
| W1-20 | Rate-limit response headers, honor retry-after, wait for reset (s4) | R | 5.4 L797 |
| W1-21 | ETag / if-none-match; 304 consumes no primary allowance (s5) | R | 5.4 L799 |
| W1-22 | Polling guidance: webhooks preferred, regular cadence, `x-poll-interval`, stable filters (s5) | R | 5.4 L799 |
| W1-23 | Secondary-limit precautions: sequential, 1 s between writes, backoff with cap (s5) | R | 5.4 L799 |
| W1-24 | GraphQL primary limits by credential type (s6) | R | 5.4 L798 (Enterprise Cloud org 10,000 not stated: MINOR) |
| W1-25 | GraphQL point-cost formula, first/last 1..100, 500,000 nodes cap (s6) | R | 5.4 L798 |
| W1-26 | `rateLimit` object fields / headers (s6) | R | 5.4 L798 |
| W1-27 | GraphQL secondary: CPU budget 90 s per 60 s (60 s for GraphQL), unpublished restrictions may apply (s6) | O | Concurrency/points are in L797; the CPU-time budget and "unpublished restrictions" sentence are absent. MINOR |
| W1-28 | GraphQL conditional requests undocumented [UNVERIFIED]; GraphQL poll always pays points (s6) | R | 5.4 L798, L800 |
| W1-29 | `gh project item-list` flags, default limit 30 truncates silently (s7) | R | 5.3 L781 |
| W1-30 | Manual page states no required scope / no schema (s7) | R | 5.3 L781 |
| W1-31 | Projects API auth: classic read:project/project, App token, `gh auth login --scopes` (s7) | R | 5.3 L782 |
| W1-32 | Fine-grained PAT / GITHUB_TOKEN not addressed on that page (s7) | R | 5.3 L784, L786 |
| W1-33 | Org Project GraphQL example (items/fieldValues/content query) and that the Projects page does not show cursor pagination (`pageInfo`) (s7) | O | The cost arithmetic is at L789 and REST cursors at L787, but the example query shape and the note that the page gives no GraphQL pagination are absent. MINOR (plan paginates explicitly, L1615-1624) |
| W1-34 | GraphQL cost of the example (about 2 and 9 points) [DERIVED] (s7) | R | 5.3 L789 |
| W1-35 | Project filter syntax (status:, label:, assignee:, no:, is:, comma = OR, no cross-field OR, hyphen negation, @me); UI-only evidence (s8) | R | 5.3 L788 |
| W1-36 | REST projectsV2 routes; `q`, `fields` (omitted gives title only), `per_page` 30/100, before/after cursors (s8) | R | 5.3 L787 |
| W1-37 | `gh project item-list --query` uses same syntax if host supports it; server-side Status filter in one call (s8) | R | 5.3 L781, L788; 5.5 L809 |
| W1-38 | Items route ETag/304 behavior UNVERIFIED (s8) | R | Stated in 7.6 L1409 ("ETag behavior of the Projects items route is [UNVERIFIED]") and Q23 L1876; caveat on gh high-level commands at L799 |
| W1-39 | Classic PAT scopes; `repo` additionally needed for private-repo items (gh-aw, secondary) (s9) | O | Scope names at L782; the private-repo `repo` note is absent. MINOR (repo is public) |
| W1-40 | Fine-grained PAT: org Projects Read, resource owner = org, plus repo Issues Read; org approval policy UNVERIFIED (s9) | R | 5.3 L784 |
| W1-41 | GitHub App: org Projects read, UAT and IAT; who may create an App UNVERIFIED (s9) | R | 5.3 L785 |
| W1-42 | GITHUB_TOKEN has no projects permission; explicit sentence only from secondary gh-aw (s9) | R | 5.3 L786 |
| W1-43 | Developer's own `gh` login can read org Project with read:project; `gh auth refresh -s read:project` form (s9, s13, s14.1) | R | 5.3 L782-783; 4.1 G10 L692 |
| W1-44 | Issue search qualifiers; no Project Status qualifier (s10) | R | 5.5 L806 |
| W1-45 | Search endpoint: 30/min, 1,000 matches, per_page 100, `incomplete_results`; shared-bucket question (s10) | R | 5.5 L807 (the 10/min limit for code and semantic search is not stated: MINOR) |
| W1-46 | `gh issue list` flags and JSON fields; default limit 30; projectItems Status payload UNVERIFIED (s10) | R | 5.5 L808 |
| W1-47 | `gh issue list --search` cost unknown, assume 1 call (s10) | D | Covered by cost model L800 and L809 |
| W1-48 | Issue events: mandatory actor, labeled event label object, pagination; repo-wide list may have null actor (s11) | R | 5.6 L815 (null-actor remark for the repo-wide list not stated: MINOR) |
| W1-49 | No retention period stated for events (s11) | R | 5.6 L815 |
| W1-50 | Timeline events: label add/remove with actor, comments with author_association, Project additions; Projects v2 status change in timeline UNVERIFIED; `exclude` param, status codes (s11) | R | 5.6 L816 (exclude param and status codes: MINOR) |
| W1-51 | Post-approval edit detection: no documented field; design rule compare updated_at/body hash (s11) | R | 5.6 L818 |
| W1-52 | Triage lowest role to apply labels; Read can open issues and comment; org owners/body-edit UNVERIFIED (s11) | R | 5.6 L817 |
| W1-53 | Webhook signature header details, constant-time compare (s12) | R | 5.13 L893 |
| W1-54 | X-GitHub-Delivery/Event/Hook-ID, 25 MB, dedupe by delivery id, redelivery keeps id (s12) | R | 5.13 L898 |
| W1-55 | Return 2XX within 10 seconds, queue heavy work (s12) | R | 5.13 L898 |
| W1-56 | No automatic redelivery of failed deliveries; stopped workspace loses events (s12) | R | 5.13 L898; 5.15 L968 |
| W1-57 | Redelivery window and ordering guarantee UNVERIFIED; design for out-of-order (s12) | R | 5.13 L898 (design-for-out-of-order advice not stated: MINOR) |
| W1-58 | Webhooks need a reachable URL, the cost B/C carry and A avoids (s12) | R | 5.13 L898 end |
| W1-59 | Actions billing: public free, private credits, $0.006/min Linux, self-hosted free, 288 runs/day, $52 derived (s13) | R | 5.1 L766 (credit amounts $12/$18/$300 not stated: MINOR) |
| W1-60 | `gh auth refresh -s`; GH_TOKEN-injected workspace may not refresh [UNVERIFIED] (s13) | R | 5.3 L783 |
| W1-61 | `--query` status example only via search summary; cli/cli #11412 projectItems.status; #8216 schema change; gh version pin (s13) | R | 5.3 L790 |
| W1-62 | 14.1 Yes the dev login can read with read:project; least-privilege choices; org approval/SSO UNVERIFIED (s14.1) | R | 5.3 L782-786; 4.1 G10 L692 |
| W1-63 | 14.2 cost arithmetic (12/h, 36/h, 5 workspaces 180/h, 1,000-item Project 120/h and 1,080 pts/h, exhaustion 400 calls/poll) (s14.2) | R | 5.4 L800 |
| W1-64 | 14.2 interval comparison (1 min = 60/h 1.2%, 15 min = 4/h 0.08%) (s14.2) | O | Only the 5-minute figure is carried (L800); the 1-minute and 15-minute comparison is absent. MINOR (derived arithmetic) |
| W1-65 | 14.2 idle polls free with ETag on REST; `gh` high-level commands expose no ETag handling [UNVERIFIED] (s14.2) | R | 5.4 L799 |
| W1-66 | 14.2 sequential calls, per-cycle cap, retry cap (s14.2) | R | 5.4 L797-799; SC-10 |
| W1-67 | 14.3 cheapest correct filter: Project items query covers tagged+Project+Backlog; human-approved derived from label event actor; 1+k+k calls (s14.3) | R | 5.5 L809 |
| W1-68 | 14.3 label-only fallback via issue search losing Status check (s14.3) | R | 5.5 L809; 4.1 G10 L692 |
| W1-69 | 14.4 four intended-owner candidates with costs/risks (assignee:@me, per-person label, Project field, unassigned first come) (s14.4) | R | 4.3 L723-733; 7.4 L1368-1382 |
| W1-70 | 14.4 evidence-only recommendation: candidates 1/2 cost nothing extra, 3 adds cost and unverified filter, 4 only racy one (s14.4) | R | 4.3 L729-732 (re-checked against 7.4 in Part 3) |
| W1-71 | 14.5 revisit triggers: token cannot read Project; latency; rate-limit exhaustion; workspace availability; change history; shared ledger; scheduled-Action C-lite (s14.5) | R | 5.15 L956-968 (conditions 1-9, "facts that cut against") |
| W1-72 | Recommendations 1-7 (A supported; one server-side filter call with explicit limit; approver from labeled actor; owner filter choice; poller hygiene; B/C triggers; do not use scheduled Action) | R | 5.5 L809, 5.6, 5.4, 5.15 L968, 7.x (verified in Part 3) |
| W1-73 | Gaps 1-15 (UNVERIFIED items) carried as open questions | R | Verified in Part 3 against 9.2 and Appendix A.2 |

web-01 tally (row-level classification; sub-detail MINOR notes inside R rows are listed separately in the omissions table): 73 enumerated, R 67, D 1 (W1-47), O 5 (W1-16, W1-27, W1-33, W1-39, W1-64). W1-72 and W1-73 were confirmed in Part 3: the seven web-01 recommendations are in 5.5 L809, 5.3, 5.4 L797-799, 7.4 L1368-1381, 7.6 L1409, 5.15 L968; web-01 gaps 1-15 map to Q8, Q7, Q11, Q23, Q24, Q25, Q26, Q27, Q28, Q14 and A.2 Q18 (L1876-1884, L2061).

## Part 2: web-02-coder-claude-dispatch-and-security.md (374 lines)

| ID | Finding (web-02 section) | Class | Where in report / note |
|---|---|---|---|
| W2-01 | `coder_script` cron six fields seconds first; `run_on_start` must exit; `run_on_stop`; `timeout`; `log_path`; scripts concurrent unless `coder_script_order` (v2.39) (A1) | R | 5.7 L824 |
| W2-02 | Provider example is a 5-minute health check `cron = "0 */5 * * * *"` (A1) | R | 5.7 L824; 6.1 L1065 |
| W2-03 | `start_blocks_login` argument of `coder_script` (A1) | O | Absent. MINOR (argument list detail) |
| W2-04 | Overview page: `coder_script` for periodic jobs, replaces `startup_script`; cron overlap/stop behavior UNVERIFIED; poller takes own lock (`flock`) (A1) | R | 5.7 L825; 6.1 L1065 |
| W2-05 | `coder_script` lives in Coder repo; IronClaude ships poller plus setup instruction (A1) | R | 5.7 L824; 7.7 L1413 |
| W2-06 | Resource persistence: default persistent; disposable via `count`; ephemeral destroyed on restart (A2) | R | 5.7 L826 |
| W2-07 | Inference: stop kills agent and cron; start resumes; stopped workspace polls nothing; latency boundary must be in design doc (A2) | R | 5.7 L827; 6.1 L1112 |
| W2-08 | Agent/children killed on stop is template-dependent (A2) | D | Folded into L826-827 (ephemeral resources / inference marked PROPOSAL) |
| W2-09 | Autostop facts: admin permission for autostart, 1 h activity bump, qualifying activity list, non-qualifying list (A3) | R | 5.7 L828 |
| W2-10 | Premium mandatory stops, dormancy (auto start blocked), deletion of dormant workspaces (A3) | R | 5.7 L828 |
| W2-11 | Consequence (d): with dormancy the poller is silent until a human reactivates (A3) | O | L828 lists dormancy but not the consequence for the poller. MINOR |
| W2-12 | Consequences (a)-(c): cron not activity; idle workspace stops with poller; Orca-launched session activity UNVERIFIED (A3) | R | 5.7 L828 |
| W2-13 | Durable state tiers: GitHub, home volume file with atomic write, never /tmp; lost record fails safe (A4) | R | 5.7 L829 |
| W2-14 | Whether target template mounts `$HOME` persistently UNVERIFIED (A4) | R | 5.7 L826; 7.9 item 7 L1429 |
| W2-15 | systemd/system cron not established; daemonized child of run_on_start UNVERIFIED; prefer cron (A5) | R | 5.7 L830 |
| W2-16 | Agents connect outbound to `CODER_ACCESS_URL`; no fixed inbound port; WireGuard, STUN UDP 3478, DERP; no direct browser connections; E2E encryption (B1) | R | 5.8 L836 |
| W2-17 | Proxies must support WebSocket (B1) | O | Absent. MINOR (deployment detail) |
| W2-18 | External system can only reach a workspace through control plane with Coder token: basis for choosing pull (B1) | R | 5.8 L836; 6.1 L1111 |
| W2-19 | Architecture page does not state connection direction (B1) | R | 5.8 L836 |
| W2-20 | `coder ssh` usage, remote command, auto-start unless `--disable-autostart`; `--no-wait`/`--wait`; `--` before flags; no pty unless -t (B2) | R | 5.8 L837 (`--no-wait`, `--`, `-t` details: MINOR) |
| W2-21 | `coder port-forward` flags; reverse via `coder ssh -R` (B2) | R | 5.8 L837 |
| W2-22 | `coder exec` not found; use `coder ssh <ws> <cmd>` (B2) | R | 5.8 L837 |
| W2-23 | `coder external-auth access-token` behavior, exit codes, flags; agent token is workspace credential (B2) | R | 5.8 L838 |
| W2-24 | External auth: per-user OAuth token, `coder_external_auth`, `GIT_ASKPASS`; owner-identity guarantee UNVERIFIED; poller reads own login (B3) | R | 5.8 L839; 4.1 G4 L686 |
| W2-25 | Coder REST API header/base path; users create own tokens; Owner role for others; scopes `--scope`/`--allow`; child tokens; `CODER_MAX_TOKEN_LIFETIME`; build endpoint not read (B4) | R | 5.8 L840 |
| W2-26 | `claude -p` expands custom commands; exact statement; stale third-party mirror; answers gap 8 at doc level not gap 1 (C1) | R | 5.9 L846; 4.4 L742 |
| W2-27 | `-p` flags, output formats, exit codes, max-turns, budget, no-session-persistence, continue/resume; `--json-schema` structured_output (C2) | R | 5.9 L847 (`--json-schema` not stated: MINOR) |
| W2-28 | Default Manual permission mode in `-p`; `--permission-mode` values; `--permission-prompts none` removes AskUserQuestion; approval via `PermissionRequest` hook or `--permission-prompt-tool` (C2) | R | 5.9 L847 (the two approval mechanisms not named: MINOR) |
| W2-29 | `--bare` skips discovery; recommended for scripted calls and "will become the default for -p in a future release"; `/sc:issue` must not use `--bare` (C2) | R | 5.9 L848 (the "will become the default in a future release" sentence is not stated; flagged MINOR-FLAG below) |
| W2-30 | `-p` runs project hooks and `.mcp.json` without trust dialog; launch only in a checkout the poller controls (C2) | R | 5.9 L848 |
| W2-31 | `-p` differs from interactive for this repo: single-shot, no questions, denies un-allow-listed Bash; Orca skip-permissions is broader (C2) | R | 5.9 L847; 5.11 L869 |
| W2-32 | Headless route documented-possible alternative; bypasses Orca; decision stays with owner (C3) | R | 6.1 L1114 |
| W2-33 | claude-code-action: runs on GitHub runners, minutes plus tokens, interactive vs automation modes, prompt accepts skill invocation (D1) | R | 5.9 L849 |
| W2-34 | Action auth: API key, `CLAUDE_CODE_OAUTH_TOKEN` (tied to the subscription of the person who ran `claude setup-token`), workload identity federation via OIDC with named inputs; Bedrock/Vertex/Foundry via OIDC (D1) | R | 5.9 L849 (OAuth token provenance, federation input names and cloud-provider list not stated: MINOR) |
| W2-35 | Action GitHub App permissions (Contents, Issues, PRs); official shared app broader and "no subset"; custom App needed for three permissions (D1) | O | Absent. MINOR (Action alternative only) |
| W2-36 | Scheduled workflows default branch only, public 60-day disable; fork public (D1) | R | 5.1 L763 |
| W2-37 | Action runs outside workspace, assigns runner identity, so only selector/notifier half of B/C (D1) | R | 5.9 L849 |
| W2-38 | Who can trigger: write access; `allowed_non_write_users`; job-scoped GITHUB_TOKEN not PAT; `allowed_bots` explicit list (D2) | R | 5.9 L850 |
| W2-39 | Dispatch and schedule events get no separate actor check; `workflow_run` checks both actors (D2) | O | Absent. MINOR |
| W2-40 | Injection defenses: sanitization list; "can miss new techniques"; secret scrubbing/PID isolation partial (D2) | R | 5.9 L850 |
| W2-41 | Untrusted checkouts / base-config restoration only for Claude paths; unsigned commits unless configured; base-action lacks actor checks; short-lived scoped App credentials (D2) | O | Absent. MINOR (Action alternative only) |
| W2-42 | Cost guards: max-turns, timeouts, concurrency (D2) | R | 5.9 L850 |
| W2-43 | Lessons for the watcher: write-access analogue, integer-only plus no secrets, explicit allow-list not wildcard (D2) | R | 5.9 L850; 5.11 L873 |
| W2-44 | E1 `coder/create-task-action` inputs, Coder 2.28, OAuth lookup, no actor check, privileged token (E1) | R | 5.10 L856 |
| W2-45 | E2 Coder Agents Chats API, scoped API keys, `agents-access`, restricted egress templates; older experimental task endpoint UNVERIFIED (E2) | R | 5.10 L857 (provider-secrets-on-control-plane and human-review-before-merge points not stated: MINOR) |
| W2-46 | E3 Copilot coding agent: write access, hidden character stripping, Approve-and-run, single branch, firewall, stated risk; snippet-only points UNVERIFIED (E3) | R | 5.10 L858 (Actions runs stop after 59 minutes not stated: MINOR) |
| W2-47 | E4 OpenHands: label/@mention trigger, repo authorization, 8-hour tokens with broad rights (E4) | R | 5.10 L859 |
| W2-48 | E5 Codex integration not established; E6 Sweep not researched (E5, E6) | R | 5.10 L860-861 |
| W2-49 | E7 summary table and option A has no equivalent (E7) | R | 5.10 L863 |
| W2-50 | F1 Claude Code security page: permission system, network commands, trust, sandboxed bash, working-directory boundary, avoid piping untrusted content, VMs, no system immune; implication for Orca skip-permissions (F1) | R | 5.11 L869 (WebFetch separate model call and fail-closed command-injection detection not stated: MINOR) |
| W2-51 | F2 OWASP LLM01 definition and mitigation list (F2) | R | 5.11 L870 |
| W2-52 | F3 lethal trifecta and application to claim-only session (F3) | R | 5.11 L871 |
| W2-53 | F4 GitHub secure-use guidance and strict integer pattern for poller (F4) | R | 5.11 L872 (default read-only token permissions and reviewer approval before releasing environment credentials not stated: MINOR) |
| W2-54 | F5 seven mitigations (integer argv, allow-listed approver, least privilege, human gate, allow-listed tools if headless, hidden-content hygiene, post-approval edit risk) (F5) | R | 5.11 L873 |
| W2-55 | G1 assignment additive, no CAS, 10 assignees, silently disregarded without push access; post-write read-after-write pattern reduces not closes race (G1) | R | 5.12 L879 |
| W2-56 | G2 issue events `labeled`/`unlabeled`/`assigned` fields; poller can verify labeler on allow-list; `gh` coverage UNVERIFIED (G2) | R | 5.6 L815; 5.12 |
| W2-57 | G2 comments `author_association` values, `since`, PATCH (G2) | R | 5.12 L880; 5.6 L816 |
| W2-58 | G2 post-approval body edit not detectable; proposed body-hash mitigation and its limit (needs body at approval time) (G2) | R | 5.6 L818; 7.9 item 15 L1437 (the "only if polled before dispatch, else accept the risk" caveat: flagged as part of Q row check in Part 3) |
| W2-59 | G3 Idempotency-Key draft semantics (422, 409, retention, UUIDs) and (repo, issue, approval event) key (G3) | R | 5.12 L881 (draft date 22 Oct 2026 and expiry 25 April 2027 not stated: MINOR) |
| W2-60 | G4 leases and fencing; proportional best-effort lock; lease only as retry throttle (G4) | R | 5.12 L882 |
| W2-61 | G5 Actions concurrency semantics; does not apply to option A (G5) | R | 5.12 L883 (case-insensitive names, `queue: max` 100, newer arrival cancels waiting: MINOR) |
| W2-62 | G6 claim marker comment as durable record; eligibility predicate (unassigned or own login AND no own marker AND no live local dispatch) (G6) | R | 4.1 G8 L690; 6.1 L1069; 5.12 L885 |
| W2-63 | G7 pattern table and conclusion: no atomic exclusion across logins (G7) | R | 5.12 L885; 5.16 L983 |
| W2-64 | H1 GitHub HMAC scheme and no replay protection; Stripe timestamp scheme, tolerance 5 min, v1 only, 24 h rotation; both sides hold secret; per-workspace secrets (H1) | R | 5.13 L893-894 |
| W2-65 | H2 GitHub OIDC issuer, RS256, JWKS, audience, `id-token: write`, claims list, receiver must enforce trust conditions, no shared secret, limit: not who approved; fits Action sender (H2) | R | 5.13 L895 (token request URL/`getIDToken`, example allow-list claims `repository`/`ref`/`job_workflow_ref` values: MINOR) |
| W2-66 | H3 mTLS RFC 8705 and not supported by any Coder source (H3) | R | 5.13 L896 (`tls_client_auth`/`self_signed_tls_client_auth` modes: MINOR) |
| W2-67 | H4 Coder tokens as bearer; Coder verifies; rotation; status codes UNVERIFIED (H4) | R | 5.13 L897 |
| W2-68 | H5 comparison table of four mechanisms (H5) | R | 5.13 L902-907 |
| W2-69 | I1 `coder_app.share` owner/authenticated/public; enterprise restriction; `subdomain`, wildcard; other args (I1) | R | 5.14 L917 |
| W2-70 | I1 forwarded-port levels incl. `organization`; Premium cap; `coder_app.share` not affected by cap; CORS note (I1) | R | 5.14 L918 |
| W2-71 | I1 `CODER_DANGEROUS_ALLOW_PATH_APP_SHARING` snippet; prefer subdomain apps (I1) | R | 5.14 L919 |
| W2-72 | I2 Go package docs: cookies, `Coder-Session-Token` fallback, not documented in user guides (I2) | R | 5.14 L920 |
| W2-73 | I2 consequence: keep share owner (authenticated at most, never public); sender token must belong to owner; verify sender if authenticated; Coder#477 build paths (I2) | R | 5.14 L921 |
| W2-74 | I3 Workspace Agents API not a way to run a command; verified reach methods (I3) | R | 5.14 L922 |
| W2-75 | I4 chain GitHub login to Coder user to workspace to `coder_app`; collapses under A (I4) | R | 5.14 L923; 6.2 L1164 |
| W2-76 | J1 request transport, body fields, headers, tolerance, idempotency to at-most-once mapping (J1) | R | 5.15 L929-936 |
| W2-77 | J2 response codes 202/200/409/422/401/403/400/unreachable/429 and audit fields (J2) | R | 5.15 L938-952 |
| W2-78 | J3 six revisit conditions (J3) | R | 5.15 L954-968; 6 table L1309-1327 (merged to nine) |
| W2-79 | K polling budget: 5,000/h, secondary limits, 60 s wait/backoff, 120 req/h at 10 calls per poll, 5 workspaces 12%; page silent on ETag (K) | R | 5.4 L800 |
| W2-80 | K `gh project item-list` exists; no scope/schema on page; label-only selection as documented-safe baseline (K) | R | 5.3 L781; 5.5 L809 |
| W2-81 | Key External Findings 1-12 | R | 5.16 L972-984 |
| W2-82 | Recommendations 1-9 (cron script, stopped = no polling, small re-derivable record, read own login, selection rule, launch route and alternative, per-cycle caps and post-assignment re-read, no reliance on prompts, B/C contract) | R | 6.1, 7.3, 7.6 L1409, 7.7; post-assignment re-read limited to candidate 4 (L879, L1381) |
| W2-83 | Gaps 1-16 (UNVERIFIED items) carried as open questions | R | Verified in Part 3 against 9.2 and Appendix A.2 |

web-02 tally: 83 enumerated, R 76, D 1 (W2-08), O 6 (W2-03, W2-11, W2-17, W2-35, W2-39, W2-41). W2-82 and W2-83 were confirmed: recommendations 1-9 sit in 6.1 L1065-1071, 7.3, 7.6 L1409, 7.7 L1413 (rec 7's post-assignment re-read is deliberately limited to routing candidate 4, L879/L1381); web-02 gaps 1-16 map to Q15 (gaps 2-5), Q26 (6-9), Q16 (10), Q29 (11), Q11 (12), Q7/Q8 (13), Q23 (14), Q20 (15), C8 (16) and the provenance note at L754.

## Part 3: synthesis files (enumerated by item; each group names its members)

Note for Part 3: the report is built from these synthesis files and reproduces most tables unchanged. Where the report changed a synthesis statement (SC-5, SC-7, SC-9, SC-10, SC-13, Q3 of synth-04, the 7.6 "checks to pass" row, Phase 1-7 steps) it did so by correcting or extending it with later evidence; those are classed R (the finding is present in its newer, stronger form), not O.

### 3a. synth-02-target-gaps-external.md (467 lines)

| Group | Members | Class | Report location |
|---|---|---|---|
| S2-01 | 3.1 Desired behavior and the poll-flow diagram (2 items) | R | 3.1 L588-613 |
| S2-02 | SC-1 to SC-17 (17 items: selection, approval, owner, integer prompt, no issue text, argv no shell, repo pin, at-most-once, lost reply, caps, claim-only, plain process, nothing live, label setup, design record, repo gates, unverified flagged) | R | 3.2 L615-637 (SC-5, SC-7, SC-9, SC-10, SC-13, SC-16 strengthened) |
| S2-03 | 3.3 Constraints (9 items: no live deploy, claim identity, claim-only, integer-only, repo target, ordinary session, existing worktree, environment, Python 3.10 and house style) | R | 3.3 L639-651 |
| S2-04 | 3.4 Consequences of A (4 items: no listener/port/registry, Coder#477 unnecessary, own `gh` login identity, routing rule open) | R | 3.4 L653-662 |
| S2-05 | 3.5 Out of scope (4 items: `--pipeline`, next steps, listener/registration/transport, live deployment/labels/scope changes) | R | 3.5 L664-671 |
| S2-06 | G1 to G30 (30 gap rows: watcher, `gh` runner, `orca` wrapper and mock, account binding, approval signal, owner routing, at-most-once, same-login race, Backlog re-selectable, Project read token, label setup, integer guard, untrusted reads, containment, never-as-worker, `--pipeline` design-only, issue text expectation, Coder#477, poller host, slash-command-as-prompt, per-host prerequisites, no machine-readable result, no decision record, scaffolding, linking hazard, STALE private fork, STALE launch-level doc, hook not installed, STALE test descriptions, STALE inventories) | R | 4.1 L679-712 (G15 and G29 extended) |
| S2-07 | 4.2 unwired-capability rows (4) | R | 4.2 L714-721 |
| S2-08 | 4.3 routing candidates 1-4 (4) | R | 4.3 L723-732 |
| S2-09 | 4.4 contradictions (6: assignee pre-filter, rate limits, `coder ssh` auto-start, webhook replay, `claude -p`, permission mode) | R | 4.4 L734-744 (plus option-letters row) |
| S2-10 | 4.5 carried to Section 6 and 7 (1) | R | 4.5 L746-748 |
| S2-11 | 5.1 (5 items: schedule floor, branch/60 days, issues types, issue_comment/label, billing) | R | 5.1 L758-766 |
| S2-12 | 5.2 (4 items) | R | 5.2 L768-775 |
| S2-13 | 5.3 (10 items: item-list flags, Projects API auth, auth refresh, fine-grained PAT, App, GITHUB_TOKEN, REST projectsV2, filter syntax, GraphQL cost, projectItems status) | R | 5.3 L777-790 |
| S2-14 | 5.4 (5 items: user limit, secondary limits, GraphQL, conditional requests, cost of A) | R | 5.4 L792-800 |
| S2-15 | 5.5 (4 items: search qualifiers, search endpoint, `gh issue list`, cheapest sequence) | R | 5.5 L802-809 |
| S2-16 | 5.6 (4 items: events actor, timeline, roles, edit detection) | R | 5.6 L811-818 |
| S2-17 | 5.7 (7 items: coder_script cron, extending-templates overview, persistence, stop inference, autostop, state tiers, systemd) | R | 5.7 L820-830 |
| S2-18 | 5.8 (5 items: outbound agents, coder ssh/port-forward, external-auth access-token, external auth owner identity, REST API tokens) | R | 5.8 L832-840 |
| S2-19 | 5.9 (5 items: headless `/name`, `-p` flags/permissions, `--bare`, claude-code-action, Action security) | R | 5.9 L842-850 |
| S2-20 | 5.10 (5 dispatcher rows, Sweep note, pattern summary = 7 items) | R | 5.10 L852-863 |
| S2-21 | 5.11 (5 items: Claude security page, OWASP, lethal trifecta, GitHub secure-use, supported mitigations) | R | 5.11 L865-873 |
| S2-22 | 5.12 (5 items: assignees API, comments, Idempotency-Key, leases, concurrency; plus G7 summary = 6) | R | 5.12 L875-885 |
| S2-23 | 5.13 (6 items: GitHub HMAC, Stripe HMAC, OIDC, mTLS, Coder tokens, webhook delivery facts; plus H5 comparison table = 7) | R | 5.13 L887-909 |
| S2-24 | 5.14 (8 items: `coder_app.share`, forwarded-port levels, path-app env var, Go package docs, consequence, agent API, GitHub-to-workspace chain, scope note) | R | 5.14 L911-923 |
| S2-25 | 5.15 (request table 4, responses table 1, audit fields 1, nine revisit conditions 9, facts cutting against revisiting 1 = 16) | R | 5.15 L925-968 |
| S2-26 | 5.16 summary (11 topic rows, closing statement = 12) | R | 5.16 L970-986 |
| S2-27 | Carried to Open Questions Q1 to Q19 (19) | R | A.2 L2038-2062 |
| S2-28 | Coverage-check rows (20) and the "excluded with rationale" paragraph (1) | R | A.2 L2066-2091 |

synth-02 tally: 231 enumerated (S2-01: 2, S2-02: 17, S2-03: 9, S2-04: 4, S2-05: 4, S2-06: 30, S2-07: 4, S2-08: 4, S2-09: 6, S2-10: 1, S2-11: 5, S2-12: 4, S2-13: 10, S2-14: 5, S2-15: 4, S2-16: 4, S2-17: 7, S2-18: 5, S2-19: 5, S2-20: 7, S2-21: 5, S2-22: 6, S2-23: 7, S2-24: 8, S2-25: 16, S2-26: 12, S2-27: 19, S2-28: 21). R 231, D 0, O 0. (The web items inside S2-11 to S2-26 are the same substance as web-01 and web-02 findings enumerated in Parts 1 and 2; they are counted again here because they are separate rows of this input file.)

### 3b. synth-03-options-recommendation.md (540 lines)

| Group | Members | Class | Report location |
|---|---|---|---|
| S3-01 | 6.0 requirements R1 to R10 (10) | R | 6.0 L1014-1025 |
| S3-02 | The three questions Q-a, Q-b, Q-c every option answers (1) | R | 6.0 L1027 |
| S3-03 | Facts all four options share (11: claim-only, issue text contradicted, never-as-worker, claim never reads labels/Projects, stays in Backlog, no mutual exclusion, claim reads text live, repo public, 9 default labels, no allow-list and 3 accounts, token lacks read:project, claim environment needs) | R | 6.0 L1029-1044 |
| S3-04 | Contradictions 1-6 (option letters, assignee pre-filter, rate-limit remark, `claude -p`, private fork, launch-level guard) | R | 6.0 L1046-1055 |
| S3-05 | 6.1 Option A: description 1, steps 1-8 (8), diagram (in description group), assessment rows (effort, risk, reuse, files, pros, cons = 6), answers Q-a/Q-b/Q-c (3), launch-route variant (1) = 19 | R | 6.1 L1057-1114 |
| S3-06 | 6.2 Option B: description 1, steps 1-7 (7), assessment 6, answers 3 = 17 | R | 6.2 L1116-1166 |
| S3-07 | 6.3 Option C: description 1, steps 1-4 (4), assessment 6, answers 3 = 14 | R | 6.3 L1168-1210 |
| S3-08 | 6.4 Option D: description 1, steps 1-3 (3), assessment 6, answers 3, further hybrids (2) = 15 | R | 6.4 L1212-1254 |
| S3-09 | Requirement Scoring: scoring rule (1), 40 cells (R1-R10 x A,B,C,D), tally (1), "reading the scores honestly" (5) = 47 | R | L1256-1290 (R4 cell for A strengthened with the `gh project item-list` manual examples) |
| S3-10 | Options Comparison rows (13: effort, risk, maintainability, integration complexity, reuse, binding, untrusted input, inbound exposure, at-most-once, never-as-worker fit, latency, stopped workspace) | R | L1292-1307 |
| S3-11 | Revisit conditions 1-9 (9) and the closing line (1) | R | L1309-1327 (also 5.15 L956-968) |
| S3-12 | 7.1 recommendation and deliverable (2); 7.2 rationale rows (6); 7.3 claim-only (1), security-model controls (5), residual risk (1); 7.4 candidates (4), shared predicate (1), which one is supported and choice open (1); 7.5 routes (4) and needed-to-proceed (1); 7.6 repo-fit rows (8) and poller rules (1); 7.7 Coder#477 (1); 7.8 revisit pointer (1); 7.9 open details 1-15 (15) = 52 | R | 7.1 L1333, 7.2 L1339, 7.3 L1352, 7.4 L1368, 7.5 L1383, 7.6 L1394, 7.7 L1411, 7.8 L1415, 7.9 L1419-1437 (7.6 "checks to pass" row superseded by the corrected sync-dev/verify-sync instruction, L1407) |
| S3-13 | Coverage-of-key-findings rows (R01 13, R02 8, R03 8, W01 9, W02 10, GAPS 1 = 49) | R | A.3 L2095-2149 |
| S3-14 | Carried to Open Questions 1-20 (20) | R | A.3 L2151-2176 |

synth-03 tally: 284 enumerated (10+1+11+6+19+17+14+15+47+13+10+52+49+20). R 284, D 0, O 0.

### 3c. synth-04-plan-questions-evidence.md (553 lines)

| Group | Members | Class | Report location |
|---|---|---|---|
| S4-01 | 8.0 conventions (4); 8.1 builds and does-not-build (8); poll-cycle diagram (1); 8.3 NEW paths (3) and verb `issue-watch once` (1); 8.4 decisions D1-D3 (3) = 20 | R | 8.0-8.4 L1463-1524 |
| S4-02 | Phase 1 steps 1.1-1.10 (10), house-format facts (1), integer-only rule recorded in doc (1) = 12 | R | Phase 1 L1526-1546 (steps 1.6, 1.9, 1.10 extended) |
| S4-03 | Phase 2 steps 2.1-2.6 (6), runner/precedent note (1), "not needed" note (1) = 8 | R | Phase 2 L1548-1564 (2.2 gains `cwd`) |
| S4-04 | Phase 3 contract rows (14: invocation, agent id, worktree, existing worktree, surface, prompt, argv vs paste, slash command, agent command, success output, exit status, lost reply, other refusals), steps 3.1-3.6 (6), mocking-style note (1) = 21 | R | Phase 3 L1566-1598 (3.4 gains `resolve_orca`, timeout-as-unknown; Lost-reply row gains the documented retry text) |
| S4-05 | Phase 4: five filters (5), seven `gh` calls (7), events-jq and marker-jq (2), raw-page-length rule (1), comment-text-never-leaves rule (1), steps 4.1-4.5 (5) = 21 | R | Phase 4 L1600-1641 (adds mandatory `--jq` projection of `project item-list`) |
| S4-06 | Phase 5: at-most-once intro (1), steps 5.1-5.4 (4), `run_cycle` algorithm steps 1-13 (13), no-sleep/Q23 note (1), `once` options (8), exit codes (4), test scenarios (16) = 47 | R | Phase 5 L1643-1720 (adds `claimed` state, `considered` rotation, lease windows, three more scenarios) |
| S4-07 | Phase 6 style intro (1), steps 6.1-6.5 (5) = 6 | R | Phase 6 L1722-1735 |
| S4-08 | Phase 7 steps 7.1-7.6 (6) | R | Phase 7 L1737-1749 (7.6 grows to eleven checks) |
| S4-09 | Test plan summary rows (11) and commands pointer (1) = 12 | R | L1751-1767 |
| S4-10 | Rollback and disable rows (7) | R | L1769-1779 |
| S4-11 | Follow-up rows (10), revisit table (9), closing (1) = 20 | R | L1781-1812 |
| S4-12 | Integration checklist (14) | R | L1814-1829 |
| S4-13 | 9.1 owner decisions D1-D6 (6) | R | L1835-1846 |
| S4-14 | 9.2 open questions Q1-Q33 (33) | R | L1848-1886 (Q3 rewritten with the documented retry rule; Q34-Q36 added) |
| S4-15 | 9.3 corrected carry-overs C1-C11 (11) | R | L1891-1905 |
| S4-16 | Evidence trail: codebase rows (3), web rows (2), binding inputs (1), synthesis rows (4), gaps log (1), coverage rows (46) = 57 | R | 10 L1909-1992 |

synth-04 tally: 301 enumerated (20+12+8+21+21+47+6+6+12+7+20+14+6+33+11+57). R 301, D 0, O 0.

## Part 4: Addendum conformance (research-notes.md "ADDENDUM 2026-11-07T07:03Z" and "ADDENDUM 2 2026-11-07T07:12Z")

Checked against the final report by reading the cited passages. An OMITTED row here would be CRITICAL; there are none.

| # | Conformance item | Status | Evidence in the report |
|---|---|---|---|
| CF-1 | Sender-authentication findings for a push listener (mTLS, signed requests/HMAC, GitHub OIDC tokens from Actions, Coder session tokens), as context for alternatives B and C | REPRESENTED | 5.13 L887-909 (heading and scope note label it "CONTEXT FOR THE DOCUMENTED ALTERNATIVES B AND C AND FOR THE REVISIT CONDITIONS OF OPTION A"; GitHub HMAC L893, Stripe timestamp HMAC L894, GitHub OIDC L895, RFC 8705 mTLS L896, Coder tokens L897, comparison table L902-907) |
| CF-2 | Coder app and port exposure findings (authenticated app proxy, `coder_app` sharing levels, agent API) as context for B and C | REPRESENTED | 5.14 L911-923 (`coder_app.share` owner/authenticated/public L917; forwarded-port levels L918; app-proxy token acceptance and session cookies L920; consequence for `share = "owner"` L921; Workspace Agents API L922; account-binding chain L923) |
| CF-3 | Minimal watcher-to-listener contract (request schema, idempotency key, response codes) as context for B and C | REPRESENTED | 5.15 L925-952 (request body fields L934, headers and derived `Idempotency-Key` L935, at-most-once mapping L936, response codes 202/200/409/422/401/403/400/429 L938-950, audit fields L952) |
| CF-4 | Requirement Scoring of options A, B, C and the hybrid against the issue's stated requirements | REPRESENTED | "Requirement Scoring" L1256-1290 (R1 to R10 x A, B, C, D; tally L1273-1280; reading the scores L1284-1290) |
| CF-5 | Recommendation is option A labelled "decided by the owner", never "pending owner decision" | REPRESENTED | 7.1 L1335 ("Option A ... decided by the owner (ADDENDUM 2)"); also 6.1 heading L1057 and 1.1 L135. A search of the whole report for the phrase "pending owner decision" returns no hit |
| CF-6 | IronbellyOrg/Coder#477 stated as a sibling dependency with its repo boundary and the statement that option A makes it unnecessary unless B or C is revisited | REPRESENTED | 1.2 L143-149 (repo boundary L148, "Option A makes #477 unnecessary unless B or C is revisited" L149); 3.4 L660; 4.1 G18 L700; 7.7 L1411-1413; 9.1 D5 L1845 |
| CF-7 | Section 8 plan targets option A, with B and C only as follow-up | REPRESENTED | 8.1 L1472-1479 (does-not-build column), 8.4 L1518-1524, "Follow-up, not in this plan" L1781-1797 (options B, C, D, Coder#477 recorded, not planned), revisit table L1798-1810 |
| CF-8 | Only a validated integer issue number reaches a session prompt, never issue title or body text | REPRESENTED | 1.1 D3 L137; 3.2 SC-4 to SC-6 L624-626; 3.3 L646; 4.1 G12 L694; 7.3 Prompt row L1361; Phase 3 step 3.2 L1592; "Integer-only prompt rule recorded in the doc" L1546 |
| CF-9 | Scope is claim-only, decided by the owner (the pipeline after the claim stays manual) | REPRESENTED | 1.1 D2 L136; 2.1 L183-184; 3.5 L668-669; 7.3 L1354; 9.1 D2 L1842 |
| CF-10 | Correction that `src/superclaude/pr_submit/ci.py` is not a `gh` subprocess wrapper (imports only `re`, `.classifier`, `.models`; a poller needs its own injectable runner), together with the statement that `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected | REPRESENTED | 2.3 L340 (imports only `re`, `.classifier`, `.models`, `ci.py:10-15`; codebase-context.md corrected at line 21, research-notes.md lines 30 and 37), L341 (needs its own injectable runner); 4.1 G2 L684 and G29 L711; Phase 2 L1553; 9.3 C4 L1898; 7.6 L1402 |

Conformance result: 10 of 10 REPRESENTED, 0 OMITTED.

## Anti-Omission Report (final form)

Report reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (2,176 lines, read in chunks)
Input files checked: `research/web-01-github-events-projects-and-limits.md`, `research/web-02-coder-claude-dispatch-and-security.md`, `synthesis/synth-02-target-gaps-external.md`, `synthesis/synth-03-options-recommendation.md`, `synthesis/synth-04-plan-questions-evidence.md`; 972 findings enumerated (web-01 73, web-02 83, synth-02 231, synth-03 284, synth-04 301); plus 10 addendum-conformance items from `research/research-notes.md`
Date: 2026-11-07

### Omissions Found

Coverage was judged by meaning. The report carries the synthesis files almost verbatim (Sections 3 to 5 from synth-02, 6 to 7 from synth-03, 8 to 10 from synth-04, with Appendix A holding the synthesis carry-forward lists) and extends them with fix-cycle corrections, so the synthesis files produced no omission. Every omission found is in the two web research files, and every one is a low-relevance detail on a side topic (the Actions or Claude Action alternative, Enterprise Cloud limits, command-flag minutiae). None touches option A, the owner decisions, the plan or the open-question list.

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| 1 | Enterprise Cloud user limit of 15,000 requests/hour, and the rule that higher-limit app traffic still consumes the user's lower allowance (W1-16) | web-01 s4 | OMITTED | report 5.4 L796 names Enterprise Cloud only as a cap qualifier | MINOR |
| 2 | GraphQL secondary CPU budget (90 s per 60 s, at most 60 s for GraphQL) and "additional compute-related or unpublished restrictions may apply" (W1-27) | web-01 s6 | OMITTED | concurrency and point limits are in 5.4 L797 | MINOR |
| 3 | Example Projects GraphQL query (items/fieldValues/content) and the note that the Projects page shows no cursor pagination (`pageInfo`) (W1-33) | web-01 s7 | OMITTED | cost arithmetic is in 5.3 L789; REST cursors L787; Phase 4 reads explicit `-L 100` and page loops L1615-1624 | MINOR |
| 4 | Classic PAT also needs `repo` for items from private repositories (gh-aw secondary page) (W1-39) | web-01 s9 | OMITTED | scope names are in 5.3 L782; the fork is public and the observed token already carries `repo` | MINOR |
| 5 | Poll-interval comparison: 1 minute = 60 requests/h (1.2%), 15 minutes = 4 requests/h (0.08%) (W1-64) | web-01 s14.2 | OMITTED | only the 5-minute figures are in 5.4 L800 | MINOR |
| 6 | `coder_script` argument `start_blocks_login` (W2-03) | web-02 A1 | OMITTED | other arguments listed in 5.7 L824 | MINOR |
| 7 | With Premium dormancy a long-unused workspace is not auto-started, so the poller is silent until a human reactivates it (W2-11) | web-02 A3 | OMITTED | dormancy is listed but without the consequence for the poller (5.7 L828) | MINOR |
| 8 | Coder proxies must support WebSocket for agent connections (W2-17) | web-02 B1 | OMITTED | 5.8 L836 covers the rest of the networking row | MINOR |
| 9 | Claude GitHub App permission set (Contents, Issues, Pull requests), the shared official App's broader permissions with "no subset", and the need for a custom App to get only three (W2-35) | web-02 D1 | OMITTED | 5.9 L849 covers authentication and modes of the Action | MINOR |
| 10 | claude-code-action: dispatch and schedule events get no separate actor check; `workflow_run` checks both actors (W2-39) | web-02 D2 | OMITTED | 5.9 L850 covers the write-access gate, bots, sanitization | MINOR |
| 11 | claude-code-action: untrusted checkouts and base-config restoration limited to Claude paths; commits unsigned unless signing configured; the lower-level base-action lacks the actor checks and restoration; short-lived repository-scoped App credentials (W2-41) | web-02 D2 | OMITTED | 5.9 L850 covers "defenses can miss new techniques" and cost guards | MINOR |
| 12 | Redundant duplicate of W1-47 (`gh issue list --search` cost unknown) | web-01 s10 | COVERED-BY-DEDUP | cost model 5.4 L800 and 5.5 L809 | n/a (not an omission) |
| 13 | Agent and child processes are killed on stop only for some template types (W2-08) | web-02 A2 | COVERED-BY-DEDUP | 5.7 L826-827 (ephemeral resources; inference marked PROPOSAL) | n/a (not an omission) |

Sub-detail gaps inside rows classed REPRESENTED (flagged, not counted as separate omissions, all MINOR): W1-17 (+50/h per repo and per org user beyond 20), W1-24 (Enterprise Cloud org GraphQL 10,000), W1-45 (code and semantic search limited to 10/min), W1-48 (repo-wide events list may have a null actor), W1-50 (timeline `exclude` parameter and HTTP status codes), W1-57 ("design for out-of-order and duplicate delivery"), W1-59 (Actions credit amounts $12/$18/$300), W2-20 (`coder ssh` `--no-wait`, `--`, `-t`), W2-27 (`--json-schema`/`structured_output`), W2-28 (`PermissionRequest` hook and `--permission-prompt-tool` as the approval mechanisms), W2-29 (`--bare` "will become the default for `-p` in a future release", which could silently break a headless `/sc:issue` route later; the only sub-detail with a forward-looking effect, still limited to the follow-up headless variant), W2-34 (OAuth token tied to the person who ran `claude setup-token`, federation input names, Bedrock/Vertex/Foundry), W2-45 (provider secrets stay on the control plane, human review before merge), W2-46 (Copilot Actions runs stop after 59 minutes), W2-50 (WebFetch runs a separate model call; fail-closed command-injection detection), W2-53 (default read-only workflow token, reviewer approval before releasing environment credentials), W2-58 (the body-hash mitigation only works if the poller saw the body before dispatch, else accept the risk), W2-59 (Idempotency-Key draft dated 22 Oct 2026, expiry 25 April 2027), W2-61 (concurrency group names case-insensitive, `queue: max` 100, newer arrival cancels the waiting one), W2-65 (`ACTIONS_ID_TOKEN_REQUEST_URL`/`getIDToken`, example allow-list values `repository`, `ref`, `job_workflow_ref`), W2-66 (`tls_client_auth` and `self_signed_tls_client_auth` modes).

Why the 11 omissions are not blocking: each is a low-relevance detail of an alternative the owner already declined (B, C, the Action) or of an external limit that the report states in its decision-relevant form; none is foundational or load-bearing for the recommendation, the plan or the open questions; each can be added as a single clause in Section 5 if the owner wants byte-level completeness. The adversarial expectation of five or more dropped findings is met (11 found), but none of them is a distinct foundational or decision-relevant finding.

### Summary

- Findings enumerated: 972 (web-01 73, web-02 83, synth-02 231, synth-03 284, synth-04 301)
- Represented: 959
- Covered-by-dedup: 2 (W1-47, W2-08)
- Omitted: 11 (all MINOR: W1-16, W1-27, W1-33, W1-39, W1-64, W2-03, W2-11, W2-17, W2-35, W2-39, W2-41)
- Check: 959 + 2 + 11 = 972
- Omissions by severity: CRITICAL 0, IMPORTANT 0, MINOR 11
- Addendum conformance: 10 of 10 REPRESENTED, 0 OMITTED (no CRITICAL conformance omission)
- Method limits: the five input files were read in full. The report was read in full for Section 1, Sections 3 to 9 (L575-1908, except that L1945-1995 was checked by search) and Appendix A (L1996-2176), and for Section 2 only L153-342 (2.1 to 2.3 start). Section 2.3 L343-383, 2.4 and 2.5 (L384-574) were not read line by line, because none of the five assigned inputs is a Section 1 or 2 source (those come from synth-01 and research files 01 to 03, which belong to the other anti-omission partition). Part 3 enumerates the synthesis files by item groups with named members instead of one row per item, which is an exhaustive list but not a row per item.
- Optional follow-up for the report owner (not required for PASS): add one clause each for W2-29 (`--bare` future default), W2-35 (Claude App permission set), W1-39 (`repo` scope for private-repo items) and W1-33 (GraphQL pagination not shown on the Projects page).

Verdict: PASS (0 CRITICAL or IMPORTANT omissions; 11 MINOR omissions flagged, non-blocking)

