# Round 2 findings for issue 812 (W4: Exponential backoff with a ceiling for GitHub throttling)

Checked 2026-11-24 on master f2894fc44 (worktree Realign). Issue 812 is OPEN, sub-issue of umbrella #717 (watcher). Read-only. Round 1 file: `/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/2/812/findings.md`. Plan files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`). Owner records (REQ): `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. Design (DES): `docs/designs/issue-watcher.md`.

Defect in the issue text: the body of 812 is W4 followed by a copy of W5 to W15 (134 lines). "Done when ... the item below" is ambiguous, and W5 is now closed (#813). Trim the body to W4.

## Alignment with architectural decisions

- **R38 (REQ:64): CONFLICT in origin, partly aligned in substance.** Exponential backoff comes from Clay's design (655 section 10). R38 adopts no Clay element; PR 729 keeps uncovered features tracked in #717. So the item may be tracked, but only the owner can adopt it.
- **DES Q3 (`docs/designs/issue-watcher.md:873`) and C22 (:109): CONFLICT.** Q3 asks the owner to "accept the 3600 s clamp for per-issue rate limits"; C22 says a per-issue rate limit always clamps to 3600 s. The clamp is shipped and tested; W4 asks to replace it. I found no recorded owner answer to Q3 in the REQ, DEC, SPEC or verdicts (searched for backoff, exponential, 3600, clamp, C22: no hit in SPEC.md, DECISIONS.md, FOLLOW-UPS.md or `debates/*/VERDICT.md`). Q3 is open: UNVERIFIED whether answered in chat.
- **FR-028 (DES `:930`, code `github.py:469-524`): CONFLICT.** `RATE_LIMIT_MAX_WAIT_S = 3600`; `rate_limit_wait` returns Retry-After (1 to 3600 s), else the reset time within 3600 s, else now + 3600 s `rate_limit_clamped`. The 3600 s is the ceiling W4 would keep; the growth below it is new.
- **FR-20 (SPEC:210) and REASON_TABLE (`audit.py:26-104`): aligned.** `rate_limited` and `rate_limit_clamped` are both in the table (`audit.py:52`); a growing wait needs no new reason name, so no table change.
- **NG-2 / FR-06 / FR-82 (SPEC:196, :218): aligned.** A longer wait writes nothing to GitHub.
- **NFR-05 (SPEC:343) and SPEC:705 (cron shadow run "real replies captured to replace assumed fixtures"): aligned with the item's own caveat.** The throttle reply shapes are assumed (`tests/issue_watch/fixtures/_assumed_shape/`); no real reply has been captured. On this host: 4689 cycle lines in the audit logs, 0 lines mentioning `rate_limit`, so no throttle has happened to capture.
- **Schema rule (`record.py:31`, `:120-131`): partly aligned, a cost.** StoreDoc has an exact key set and `SCHEMA_VERSION = 1` with an empty migration table; a stored streak counter means a key and a schema bump (FR-22, SPEC:212, asks a backup before any migration), or a side file like `account-rate-wait.json` (`dispatch.py:60`, `:243-266`).
- **R16 / D02 shared account wait (`dispatch.py:478-483`): partly aligned.** The dispatcher writes the account-wide wait for plain `rate_limited` and deliberately not for the clamp.
- **WORKER-CONTRACT.md and HOW-WE-WORK.md: none apply** (grepped for rate, throttl, backoff).
- **Verdict files:** none mention W4 (searched all `debates/*/VERDICT.md` for backoff|exponential: no hit).

## Complementary issues

- **#817 (W9, conditional reads):** lowers the chance of throttling; W4 shortens the cost when one happens. Interface: both wait for the same captured throttle replies and a call-budget measure. Neither needs the other.
- **#811 (W3, interval):** the interval sets the call rate that W4 reacts to.
- **#819 (W11, retry of an unknown launch):** a throttled launch read must not be taken for `launch_unknown`; the two share `launch.py`/`cycle.py` stop handling.
- **#816 (W8, alert after three bad cycles):** W8's bad set is exits 3, 4, 5, 6 or 7, so a throttle (exit 5) would count as bad, while the dispatcher already treats 5 as not a fault (`cli.py:380`, `_CHILD_OK_EXITS = (0, 5, 75)`). The two issues must agree, and a longer W4 wait makes more exit-5 cycles.
- **#774 and #823 (docs):** the runbook states the 3600 s rule (`docs/designs/issue-watcher-setup.md:336`, `:396-397`).
- **#761:** gap check that raised the throttle question; no overlap in acceptance.

## Closest overlap

1. **#817 (W9)**, "Cheaper GitHub reads with conditional requests". Shared: the throttling/call-budget problem, the same gate (real captured GitHub replies, measured call numbers), the same two functions' neighbourhood (`github.py`, `cycle.py` call counting). It covers about 20% of W4's done-when (it reduces the chance of a throttle; it adds no wait growth, no streak, no reset test).
2. **#811 (W3)**: about 10% (call rate).
3. **#819 (W11)**: about 5% (stop handling when GitHub misbehaves during a launch).

## Standalone or merge

Test against #817:

| Test | W4 | W9 | If merged |
|---|---|---|---|
| Owner | owner decides Q3 and the ceiling | owner decides the budget trigger | one decision doc |
| Acceptance test | three throttled replies: `next_permitted_at` grows geometrically to the ceiling, resets after a good read | repeat poll with no change spends the minimum calls, `gh_calls` falls | two unrelated tests in one issue |
| Files touched | `github.py` wait rule, `cycle.py` stop step, `record.py` or side file, tests that pin 3600 | the `gh api` call layer, ETag store | partial overlap in `github.py` only |
| Build phase | after capture of real throttle replies | after a call-budget measure | a trigger met for one but not the other holds both |
| Risk if merged | a growing wait can hide a real fault for hours; W9 is a cost saver with no such risk | none | a safe item waits behind a risky one |

Verdict: **stand alone.** They are different mechanisms with different tests and risks. Merging would be right only if the owner decides to treat "GitHub throttling" as one package built after one capture session; even then keep two acceptance lines. Record one shared gate for both: build neither until a real throttle reply or a call-budget measurement exists. Numbers from this host: average 5.08 `gh` calls per cycle (max 15) over 4689 audit lines; at one cycle per minute for 4 repos that is about 1200 calls an hour, about 24% of the 5000 an hour GitHub limit, which is shared with every agent on the same login (the limit warning appeared in this session). That raises the value of W4 and W9 a little, but not to a trigger: 0 throttled cycles so far. (Derived from the audit logs and `crontab -l`; the 4-repo, 1-per-minute figure is my arithmetic, UNVERIFIED as a measured rate.)

## Closed issues and merged PRs checked

- **#450 (closed):** rollout done; says nothing on backoff; live since 2026-11-23, no throttle recorded.
- **#331 (closed):** the original watcher issue; no backoff asked (the 3600 s clamp comes from design FR-028, built in PR 447).
- **#655 (closed, not planned):** source of the backoff idea.
- **#665 (closed, not planned):** review findings on the 655 plan; no text on rate waits found by grep, so it delivers nothing here.
- **#751 and PR 759 (merged):** retry of a failed first run (config step each sweep, later steps after one hour). Not a throttle backoff; do not count it as W4.
- **PR 447 and PR 448 (merged):** poller and the approvers-file race fix; PR 447 shipped the clamp.
- **PR 485 (merged):** capture sheet lists `gh_graphql_rate_limited.json` and `gh_stderr_rate_403.json` as "capture if seen"; none was seen.
- **PR 707 (merged):** zero-setup watcher; left the wait rule unchanged.
- **PR 729 (merged):** R38.
- **#813 and #809 (closed today):** show the owner trimming 655-origin items whose premise changed.

## Updated recommendation

**Keep open with changes.** Changes: (1) trim the body to W4 only; (2) restate as "no-header case only": keep the header value as the floor, start at about 60 s (GitHub's own advice, round 1 cites its docs), double per consecutive throttle up to the 3600 s already in the code, clear the streak after one good cycle; (3) state it reopens design question Q3 and needs the owner's answer; (4) mark it blocked until a real throttle reply is captured or call-budget pressure is measured, sharing that gate with #817; (5) note that a stored streak is a schema bump or a side file. Priority P3. Complexity medium, size M. Unchanged from round 1 on action, priority and size; changed: R38 weighed, Q3 is shown as an open owner question rather than assumed, the host numbers are refreshed (4689 cycle lines, 0 throttles, 5.08 calls per cycle), and the closest overlap is named (#817, about 20%).

## Scan record

- Lists read in full: open-issues.tsv 134 of 134; closed-issues.tsv 157 of 157; merged-prs.tsv 508 of 508.
- Search terms: rate, throttle, backoff, GitHub, poll, cron, interval, call budget, retry, unknown launch, alert, watcher, issue-watch, docs refresh, runbook, SLO.
- Opened in full (open): 717, 716, 774, 761, 777, 770, 811, 814, 815, 816, 817, 819, 820, 821, 822, 823, 757, 775 (18). Closed: 450, 331, 655, 665, 751, 809, 813 (7). Merged PRs: 447, 448, 485, 707, 729, 759 (6).
- Master check: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/9/analyze`; report `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/9/analyze/analyze-report.md` (findings 1 and 6; `rate_limit_wait` has one production caller, `_login_step`, per codegraph_callers).
- UNVERIFIED: the real GitHub throttle reply shape; whether the owner answered Q3 in chat; the 4-repo hourly call figure; plan-file stage state after PR 700.
