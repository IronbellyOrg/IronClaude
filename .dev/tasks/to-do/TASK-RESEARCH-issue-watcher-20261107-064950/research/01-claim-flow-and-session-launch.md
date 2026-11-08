# Research: Claim flow and session launch
Investigation type: Code Tracer
Scope: the files listed above
Status: Complete
Date: 2026-11-07
---

Binding context applied: owner decision option A (workspace-side poller, claim-only, integer-only prompt). Coder#477 was filed assuming a push design.

All paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/` unless absolute. Line numbers were read in this session (2026-11-07).

## 1. Command file `src/superclaude/commands/issue.md` (101 lines)

- L8 `argument-hint: "--claim <number|url> | --create ... "`. L15 claim summary: assigns on GitHub and on its ClickUp task when one exists, checks accuracy, writes summary and next-step prompt under `.dev/issues/<N>/`, posts two marked comments, "then stops. It never runs the next-step commands." [CODE-VERIFIED against SKILL.md:17, :88, :146 and claim.md:80, :90]
- L18 "Both modes post directly to GitHub; nothing is shown for approval first." Matches SKILL.md:74 (B1).
- L24 Triggers: "Explicit only: the user types `/sc:issue --claim ...`". So a watcher-started session must be given the literal slash command as its first message.
- L37 `--claim` accepts "issue number (`302`, `#302`) or issue URL on the origin repo".
- L43 "There is no repository option (the repo is always `origin`), no dry-run option and no preview option."
- STOP rules L45-51, run by the model before Activation (prose, not code):
  - L47 exactly one of `--claim` / `--create`; both or neither: STOP + Usage.
  - L48 `--depth/--mode/--type` with `--claim`: STOP `E-CREATE-ONLY-FLAG`.
  - L51 empty `--claim` argument: STOP + Usage.
  - NOTE: none of L45-51 checks that the claim argument is an integer. The only code-enforced check is `origin_repo.py` in Wave 0 (section 5).
- L68 claim output files in `.dev/issues/<N>/`: `scout.md`, `clickup.json`, `accuracy-check.md` (posted), `issue-summary.md`, `analysis/analyze-<scope>.md` (only when out of date), `recommend.md`, `next-steps.md`, `claim-comment.md` (posted).
- L71 "After a claim, open `.dev/issues/<N>/next-steps.md` and run its commands in your own session, in order, after the `/model` line it starts with." The hand-off to a person; nothing runs the steps.
- L79 Will: resolve repo from `origin` only; spawn tier-pinned workers; assign issue, assign ClickUp task when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; "stop after writing `next-steps.md`". L83 Will Not: "Run any next-step command (brainstorm, design, workflow, implement, troubleshoot)"; L84 will not create labels, ClickUp tasks, or touch any repo other than `origin`; L85 never stage/commit `.dev/issues/`.
- L89-93 Activation is MANDATORY: `Skill sc:issue-protocol` before any protocol step.

Key Takeaways
- The command is explicit-only; the session's first message must be the literal `/sc:issue --claim <N>` (L24, L89-93).
- The command file validates flags in prose; only `origin_repo.py` validates the claim argument in code.
- Claim never performs the pipeline; the issue text's expectation of a full pipeline is [CODE-CONTRADICTED] by L15, L79, L83.
- Claim writes `.dev/issues/<N>/` into the working checkout, so the workspace must be a checkout of the origin repo.

## 2. Skill `src/superclaude/skills/sc-issue-protocol/SKILL.md` (156 lines)

- L4 `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`. AskUserQuestion is allowed, but claim mode never uses it: L74 "The only user prompt is the create-mode contradiction question"; Grep of `AskUserQuestion` in the skill directory finds it only at SKILL.md:4 and `refs/create.md:59` (create mode). `claim.md` has no hit. [CODE-VERIFIED by Grep 2026-11-07]
- L52-66 Workers: `issue-worker-t3` (picker `claude-gw-tier3`), `issue-worker-t2` (`claude-gw-tier2`), `issue-worker-t1` (`claude-gw-tier1a`) (L58-60); spawn never passes `model` (L54, L62); a spawn that fails because the picker ID is not served is STOP `E-TIER-UNAVAILABLE`, "there is no alias fallback" (L62, L130; `refs/tiers.md:32-40`, which says the failure happens "outside a ccsession tier workspace"). ENVIRONMENT DEPENDENCY for the watcher: the launched session must run where the picker IDs `claude-gw-tier3/2/1a` are served. Because Wave 1 (T3 spawn) comes before Wave 3 (assign), this failure stops the claim before any GitHub write (claim.md:20, :22-24), so a misconfigured workspace would fail every issue without assigning it; the poller would then see the issue still unassigned and could re-dispatch it every cycle unless it keeps its own dispatch record.
- L70 `<R>` = the `origin` repo from `uv run --no-project python "<skill base>/scripts/origin_repo.py"`; "Nothing else is consulted: not `gh repo set-default`, not gh's fork-parent default, not a `--repo` flag (B10)."
- L71 every `gh` call passes `--repo <R>`; `gh api` path is `user` or `repos/<R>/...`.
- L72 the orchestrator (the session) is the only writer: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `scripts/clickup_claim.py`.
- L75 `.dev/issues/` never staged or committed. L76 ClickUp token never printed.
- L82-88 claim waves 0-6 (section 3).
- L101-117 Return contract is printed last in chat, both modes: `status: success | stopped | failed`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`. It is chat text, not a file. A poller that launched the session in a terminal cannot read it except by reading the terminal; the on-disk completion signals are `.dev/issues/<N>/next-steps.md` and the GitHub-side assignee and marked comments.
- L121-138 error table (STOP codes: `E-NO-ORIGIN`, `E-FOREIGN-REPO`, `E-GH-AUTH`, `E-NOT-AN-ISSUE`, `E-TIER-UNAVAILABLE`, `E-WORKER-NO-OUTPUT`, `E-ASSIGN-FAILED`, `E-POST-FAILED`).

Key Takeaways
- No machine-readable result file is written for the poller to read; completion is observable only on GitHub (assignee, marked comments) and in `.dev/issues/<N>/`.
- Stops in Waves 0-2 make no GitHub write; after Wave 3 the issue is assigned even if Waves 4-6 fail (then the claim comments are missing, and a re-run is the repair, claim.md:42-43, SKILL.md:135).
- `claude-gw-tier*` picker IDs are a hard prerequisite of the claim; a workspace not serving them fails at Wave 1.

## 3. Claim waves, traced in `refs/claim.md` (91 lines) against SKILL.md:82-88

| Wave | What happens (file:line) | Writes / posts |
|---|---|---|
| 0 prerequisites (orchestrator) | `origin_repo.py --claim "<argument>"` resolves `{"repo","number"}`; exit 1 `E-NO-ORIGIN`, 3 `E-FOREIGN-REPO`, 4 `E-NOT-AN-ISSUE` (claim.md:13-15); `gh auth status` else `E-GH-AUTH` (:16); default branch via `gh repo view <R> --json defaultBranchRef` (:17); create `.dev/issues/<N>/` (:18) | local dir only; "No GitHub or ClickUp write happens before Wave 3" (:20) |
| 1 lookup (`issue-worker-t3`, read-only) | `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author`, `gh api user -q .login` (:26); merged PRs since `createdAt`, limit 200 (:27); `git fetch origin`, then `git log --since ... origin/<B>` (:28); an earlier comment authored by this login with `<!-- sc:issue:claim -->` or `<!-- sc:issue:accuracy-check -->` (:29, latest wins); writes `scout.md` (:30) | `.dev/issues/<N>/scout.md` |
| 2 edge cases (reads `scout.md`) | in order: pull request -> STOP `E-NOT-AN-ISSUE` (:39); `CLOSED` -> STOP "Issue #N is closed; not claimed." (:40); assigned to anyone other than the current login -> STOP "Issue #N is assigned to @<login>; not claimed." (:41); already assigned to the current login -> continue, "re-claim is allowed and idempotent" (:42); earlier marked comment IDs remembered (:43) | no GitHub or ClickUp write on any STOP (:37) |
| 3 assign | `gh issue edit <N> --repo <R> --add-assignee @me`; failure -> `E-ASSIGN-FAILED`, no ClickUp, no comment (:47); then `clickup_claim.py --issue-url <url> --issue-number <N> --repo <R> > clickup.json`, all outcomes non-fatal (:48-50) | GitHub assignee; ClickUp assignee when configured; `clickup.json` |
| 4 accuracy check + summary | `issue-worker-t2`, or `t1` when `scout.md` says complex (:54); writes `accuracy-check.md`, `issue-summary.md`, and `analysis/analyze-<scope>.md` when out of date (:57-59) | files only |
| 5 next steps | `Skill sc-recommend` with the goal format of `refs/chains.md`, saved to `recommend.md`; `next-steps.md` written, starting with the `/model` tier line (simple -> `claude-gw-tier2`, medium/complex -> `claude-gw-tier1a`) (:78-79); "Do not run any of those commands (B2)" (:80) | files only |
| 6 post | accuracy-check comment edited by marker id or posted (:84-87); claim comment likewise (:88); post failure -> `E-POST-FAILED` (:89); "Print the `next-steps.md` path and STOP" (:90) | two GitHub comments |

Answer to question (1): CODE-VERIFIED (lines read in claim.md and SKILL.md). It writes the files in the last column, assigns the issue (and the ClickUp task when configured), posts exactly two marked comments, and never commits (claim.md:90).

Key Takeaways
- Stop points in order of cost: Waves 0-2 write nothing; Wave 3 is the first write (assignee), so the "claimed" state on GitHub exists before the accuracy-check and summary exist.
- The claim never gates on labels or Project status. `labels.md:7` "`--claim` changes no labels"; Wave 1 only records `labels` into `scout.md` (claim.md:26, :30). The watcher must do the "tagged, approved, in a Project, Backlog" gating itself.
- Nothing in the claim moves the issue in a GitHub Project: Grep for `gh project|projectV2|graphql` over `src/superclaude/skills/sc-issue-protocol` returned no match in any file. [CODE-VERIFIED by Grep 2026-11-07] So after a claim the issue stays in Backlog status; a poller that filters on "Backlog" will keep seeing an already-claimed issue until a person (or a new watcher step) changes its status.

## 4. `refs/labels.md` (46 lines)

- L7 "These are the only labels `/sc:issue` ever applies (B7). It never creates a label. `--claim` changes no labels."
- L9-13 label set is mode (`bug`, `enhancement`), type (`type: cicd` ... `type: other`), complexity (`complexity: simple|medium|complex`), all applied by `--create` only.
- L22-43 maintainer creation lines use `gh label create "<name>" --repo <owner/repo>`.
- No trigger label and no approval label exist in the fixed set. [CODE-VERIFIED: the table at L9-13 and the lines at L27-42 contain none.] The watcher's trigger and approval labels are new, need their own one-time `gh label create` instructions (the owner-decided deliverable), and must not be added through `/sc:issue` (labels.md:7).

Key Takeaways
- Labels are an output of `--create`, never an input of `--claim`; no per-person label exists today, so a "per-person label" routing candidate (question 2) would also be new setup.

## 5. `scripts/origin_repo.py` (196 lines): argument validation and ClaimError paths

- L65-74 regexes. `_NUMBER = ^#?(?P<n>[1-9][0-9]*)$` (L74): ASCII digits only, no leading zero, no sign, optional single `#`. `_GITHUB_URL` (L70-73) matches `https?://` or none, optional `www.`, `github.com/` or `git@github.com:`.
- L102-153 `check_claim(arg, origin)`: strips whitespace (L107); an integer or `#integer` returns `int(...)` immediately (L108-110) with no upper bound; any other string goes on to the URL branch.
- Accepted: `302`, `#302`, and `https://github.com/<origin owner>/<origin repo>/issues/302` (trailing `/`, `#fragment`, `?query` ignored, L25-27, L126, L143-146).
- Rejected (L45-50; `main` L177-191 prints `CODE: message` to stderr and returns the code):
  - `owner/repo#N` (no `github.com`, no `://`): `_GITHUB_URL` does not match (L112), no `://` and no `git@` (L114), so `E-NOT-AN-ISSUE` exit 4 (L120-124). [CODE-VERIFIED by reading; not executed]
  - Any other text, `0`, `007`, `-5`, `302 extra words`: `E-NOT-AN-ISSUE` exit 4 (L120-124).
  - A URL on another host: `E-FOREIGN-REPO` exit 3 (L114-119).
  - A GitHub URL naming another owner/repo, or no repo: `E-FOREIGN-REPO` exit 3 (L127-140; case-insensitive whole-segment compare L135).
  - A `/pull/<N>` URL: `E-NOT-AN-ISSUE` exit 4 (L147-152). Another path on origin: exit 4 (L153).
- L156-174 `read_origin()` runs `git remote get-url origin` with no `cwd`, so it reads the repo of the current directory; non-zero -> `E-NO-ORIGIN` exit 1 (L169-170); `parse_origin_url` accepts only `https://github.com/o/r[.git][/]` and `git@github.com:o/r[.git][/]` (L66-69); anything else -> exit 1 (L172-173).
- It does NOT check that the issue exists, is open, or is an issue rather than a PR for a bare number; that is Wave 2 from `scout.md` (claim.md:39).

Answer to question (8), argument validation: the `/sc:issue --claim <N>` argument is parsed in two places. (a) By the model, using the command's STOP rules (issue.md:45-51, prose). (b) By `origin_repo.py check_claim` in Wave 0 (claim.md:13-15, code). Besides an integer it accepts `#N` and an issue URL on origin (no `owner/repo#N` form). A non-integer that is not such a URL is rejected by exit 4; a URL on a wrong repo by exit 3. [CODE-VERIFIED]

Key Takeaways
- A bare positive integer is the strictest argument: it passes `_NUMBER` with no URL parsing, and the repository is always `origin` of the session's working directory. A prompt `/sc:issue --claim <int>` cannot name a foreign repository.
- The script validates only the string the model passes to it (claim.md:14 says `--claim "<argument>"`); words after the integer in the prompt are read by the model, not by code. The watcher must build the prompt as `"/sc:issue --claim " + str(int(n))` itself and never forward issue text. The script is a second check, not the first.
- Integers of any size pass (L110); the poller should apply its own sanity bound (for example the integer must come from the `gh` JSON `number` field).

## 6. `scripts/clickup_claim.py` (271 lines)

- L8-19 env: `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` required for any action; `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES` (default 20, L74) optional. The token is the person's own personal token (L10), sent only in the header (L109).
- L163-170: missing token -> `{"status": "skipped", "reason": "no_token"}`; missing workspace -> `no_workspace`. Exit code is 0 for every outcome except bad arguments (L50, L262-266).
- L230-231 already assigned to the token owner -> `already_assigned` (idempotent). L212-220 more than one match -> `ambiguous`. L203-206 page cap -> `error/page_cap`. L239-242 any other exception -> `error/unexpected`.
- L245-259 argument checks: `--issue-number` positive int, `--repo` matches `owner/repo`, `--issue-url` must equal `https://github.com/<repo>/issues/<N>` case-insensitively. Exit 2 via argparse otherwise.
- Matching rules L42-48, L148-160: a GitHub issue link in the description or custom fields, else `#<N>` as a whole token in the task name.
- ClickUp calls use `urllib` with a 30 s timeout (L76, L114) and one 429 retry that sleeps `Retry-After` seconds (L119-122).

Key Takeaways
- ClickUp is optional and never blocks the claim (claim.md:50). A workspace without ClickUp variables still claims on GitHub; the claim comment states "skipped" (SKILL.md:133).
- The ClickUp identity is the personal token in the workspace environment, independent of the `gh` login; no code ties the two to the same person. [Inference from L10 and claim.md:47; UNVERIFIED as an enforced rule]
- The ClickUp step can be slow (up to 20 pages, 30 s timeout per request), so a poller must not assume a claim finishes quickly.

## 7. `src/superclaude/core/WORKER-CONTRACT.md` (never-as-worker list)

- L23 "Never-as-worker list: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode." [CODE-VERIFIED L23] The list changes only when the coordinator-only command set or D3 changes (L23).
- L11 "Worker run": "a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages; a session the user started, inside or outside Orca, is an ordinary session."
- Brief guard (L16-20): case 3, a `Command:` line naming a never-as-worker command makes the worker refuse with body `guard refused:`. The guard applies only in a session whose prompt carries a live Orca preamble (L16).
- `/sc:issue` has no `## Unattended mode` section: `issue.md` goes from Activation (L87-93) to Related Commands (L95-100). [CODE-VERIFIED by reading the whole file]
- WC-13 (L61): a worker's session never calls `worker-start`, `dispatch`, `task-create`, `orca-cli worktree create --agent` or `agent launch`.
- WC-9 (L40): under `--unattended`, every outward default (push, PR, GitHub post, ...) is off; the coordinator performs them. Applies to worker runs only.

Answer to question (7): the list governs coordinator-dispatched supervised workers (a Task with a preamble). A poller that starts an ordinary top-level session with `orca agent launch --prompt` does not create a "worker run" (no preamble, no Task ID, L11), so the list does not stop it. It also means the session gets no heartbeats, no `worker_done`, no `return-contract.yaml`, and no coordinator visibility. Dispatching `/sc:issue` through `worker-start` WOULD violate L23, and the guard would refuse it. No file states explicitly that a poller-launched ordinary session is outside the list; that reading is an interpretation of L11 and L23. [UNVERIFIED as owner intent; listed in Gaps]

Key Takeaways
- Do not model the watcher as a coordinator dispatching a worker Task for `/sc:issue`.
- The watcher's session is an ordinary session; the claim's GitHub writes are direct posts by design (issue.md:18), which WC-9 restricts only for worker runs.
- Any `orca agent launch` call is itself forbidden inside a worker session (WC-13, L61), so the poller must run as a plain process in the workspace (cron, systemd, a shell loop), not inside a supervised worker. [UNVERIFIED: that a Coder workspace provides cron or systemd, that such a process survives a workspace autostop or restart, and where durable state can live; nothing in the repo shows any of the three. See Gaps and Questions item 9.]

## 8. Analysis finding file `.dev/issues/331/analysis/analyze-sc-issue-protocol.md` (59 lines), cross-checked

- F3 (L34): claim assigns to the `gh` login and stops if someone else is assigned. [CODE-VERIFIED: claim.md:41, :47]
- F4 (L35): `/sc:issue` cannot be an Orca worker; use a new top-level session or type into a coordinator session. [CODE-VERIFIED for the first half (WORKER-CONTRACT.md:23); the second half is a design judgement, see section 12]
- F5 (L36): claim reads only `origin`, so a multi-repo watcher needs a repo-to-checkout map. [CODE-VERIFIED: origin_repo.py:156-174 reads the current directory's `origin`; SKILL.md:70]
- F7 (L38): exactly-once delivery is not designed; the claim comment (claim.md:88) can serve as a record. [CODE-VERIFIED that the claim comment exists with marker `<!-- sc:issue:claim -->`; but see section 10: that comment is posted only in Wave 6, minutes after the assignment, so it is a late record]
- The file's statement 3 (L24), that `--claim --pipeline` is design only, is checked in section 11.

## 9. Which GitHub login assigns, and how a workspace can decide an issue is meant for THIS login (question 2)

Which login: `--add-assignee @me` (SKILL.md:72, :85; claim.md:47). `gh issue edit --help` on this machine says `--add-assignee login  Add assigned users by their login. Use "@me" to assign yourself`. [CODE-VERIFIED by running `gh issue edit --help`] So the login is whichever account `gh auth` holds in the session's environment; Wave 1 also reads it with `gh api user -q .login` (claim.md:26).

Edge cases (all before any write, claim.md:37-43): pull request -> `E-NOT-AN-ISSUE` (:39); closed -> STOP "Issue #N is closed; not claimed." (:40); assigned to another login -> STOP "Issue #N is assigned to @<login>; not claimed." (:41); already assigned to this login -> continue (:42).

Candidates for "meant for this login", evaluated against what the code can read:

| Candidate | What `/sc:issue --claim` reads or does with it | What the poller needs | Fit |
|---|---|---|---|
| 1. Issue is already assigned to this workspace's login | Wave 2 item 4 continues on "already assigned to the current login" (claim.md:42); assigned to anyone else stops (:41). Claim semantics already encode this rule. [CODE-VERIFIED] | `gh issue list --repo IronbellyOrg/IronClaude --assignee "@me" --label <trigger> ...`; the flags `--assignee`, `--label`, `--search`, `--state`, `--json`, `--limit` exist (`gh issue list --help`, [CODE-VERIFIED by running help]). No new label, no claim change. The human approval step must assign the person | Best fit to claim semantics. Because assignment persists after the claim, "assigned" cannot double as the dispatch marker (needs a separate record, section 10) |
| 2. Per-person label | `--claim` never reads or changes labels (labels.md:7; claim.md:26, :30). No per-person label exists (labels.md:9-13). [CODE-VERIFIED] | New labels per person, created by a maintainer with `gh label create` (the pattern of labels.md:22-43), and a poller write to remove or swap the label | Works, and the label can serve as dispatch marker, but adds per-person setup and a poller write |
| 3. Project field | The claim has no Project code: Grep `gh project\|projectV2\|graphql` over the skill returned nothing. [CODE-VERIFIED] `gh project item-list` has `--query "assignee:octocat -status:Done"` and `--owner` (`gh project item-list --help`, [CODE-VERIFIED by running help]) | Projects query, and a token that can read the org Project; the needed token scope was not shown by the help text [UNVERIFIED] | Needed anyway for the "in a Project, Backlog status" filter; can express an owner via the `assignee:` filter of the same query. The claim does not move the item out of Backlog (section 3), so the status filter alone never excludes an already-claimed issue |
| 4. Unassigned, first workspace to take it | Wave 2 passes for an unassigned issue; Wave 3 adds the assignee (claim.md:41, :47). No lock | The at-most-once record of section 10 | Not routing, a race. See below |

Race: two workspaces with different logins starting a claim on the same unassigned issue. Reading the code, not running it: each runs Wave 1 (a T3 worker that runs `gh issue view`, `gh pr list --limit 200`, `git fetch origin`, `git log`, claim.md:26-30), then Wave 2 reads `scout.md` only (claim.md:35), then Wave 3 assigns (:47). Nothing re-reads the assignees after Wave 3 starts, and `--add-assignee` adds a user rather than replacing the list (help text above). So if both scouts finish before either assignment lands, both pass Wave 2 and both assign themselves. [Derived from code; GitHub's allowance of several assignees on one issue is not shown in this repo; UNVERIFIED here.] Expected result: two assignees, two sessions through Waves 4-6, two separate claim and accuracy-check comments (an earlier comment is matched only when authored by the current login, claim.md:29), and, where ClickUp is configured, the task assigned to both people (clickup_claim.py:230-238 adds the token owner when absent). The window is the length of Wave 1 plus the spawn, which is seconds to minutes; a 5-minute poll cycle with unsynchronised workspaces makes a collision possible but not frequent.

Design suggestion (not in any file, UNVERIFIED, untested): a poller-side reservation before the launch: `gh issue edit <N> --add-assignee @me`, re-read the assignees, proceed only when this login is the sole assignee, otherwise `--remove-assignee @me` and skip; with a deterministic tie-break (for example lowest login keeps it) so two pollers cannot both back off. Compatible with the claim because Wave 2 item 4 continues on "already assigned to the current login" (claim.md:42). Candidate 1 avoids the cross-person race by construction.

Same-login race: a person with two workspaces polling with one login is not stopped by any assignee check (both pass claim.md:42). Both run Wave 1 before either posts in Wave 6, so both find no earlier marked comment and both post new comments (marker lookup happens in Wave 1, claim.md:29, and the post in Wave 6, :84-88). The claim cannot prevent it. Whether one person has several workspaces polling is an open fact [UNVERIFIED]; the dispatch record must then be on GitHub, not local.

Key Takeaways
- Question 2 answer: `@me` is the `gh` login of the session. Already-assigned-to-me (candidate 1) is the routing rule the claim already understands and the only candidate that needs no new label and no Project read. Candidates 2 and 3 need new setup. Candidate 4 is a race, and the claim gives no mutual exclusion.
- Nothing in the claim prevents two workspaces from both claiming an unassigned issue; at-most-once has to be built in the poller.
- The claim stops without writing when the issue is closed, a PR, or assigned to someone else (claim.md:37-41); a poller that selects only issues assigned to its own login never meets the last of these.
- Reconciliation pointer (fix cycle 1, QA finding 1): the single predicate is "skip an issue assigned to a login other than the own login; an issue assigned to the own login (candidate 1) or to nobody (candidate 4) is not stopped by the claim". Candidate 1 selects assigned-to-me; candidate 4 selects unassigned, and so excludes every already-assigned issue, own login included (a post-Wave-3 failure strands such an issue under candidate 4 but re-selects it every cycle under candidate 1, section 10 line 173). The claim-stop pre-filter "skip an issue assigned to someone else" (claim.md:41-42) is the claim's own rule and is not identical to either candidate's filter. Full table and evidence: `research/02-github-surface-and-cli-patterns.md` section 2c.

## 10. Idempotence and at-most-once (question 3)

- Marked comments: `templates/accuracy-check-comment.md:17` ends with `<!-- sc:issue:accuracy-check -->` and `templates/claim-comment.md:23` with `<!-- sc:issue:claim -->`. [CODE-VERIFIED by Grep] A re-run finds an earlier comment authored by the current login with the marker, the latest one if several (claim.md:29), and edits it with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>` instead of posting (claim.md:84-88; SKILL.md:135, :145). So marked comments are edited, not duplicated, for the same login, as long as the earlier comment exists when Wave 1 runs.
- Re-claim by the same login is allowed (claim.md:42). ClickUp is idempotent: `already_assigned` (clickup_claim.py:230-231).
- Not idempotent in cost: a full re-run repeats all workers, the merged-PR lookup and the ClickUp search (up to 20 pages, clickup_claim.py:74, :184). Output files are refilled from the templates (SKILL.md:50). Whether `<D>` already existing is tolerated is not stated: claim.md:18 says "Create `<D>`" only. [UNVERIFIED]
- At-most-once across workspaces: none. The only cross-run state the claim reads is the assignee list and the same-login marked comments, and the claim comment is posted last (Wave 6), so it is a late record: the assignment (Wave 3) precedes it by the duration of Waves 4-5 (accuracy check, `/sc:recommend`).
- A claim that fails after Wave 3 (for example `E-WORKER-NO-OUTPUT` or `E-POST-FAILED`, SKILL.md:131, :135) leaves the issue assigned to this login with no claim comment. A poller using candidate 1 would select it again every cycle. It therefore needs its own durable record with a retry cap. [Derived]
- Local vs GitHub record: `.dev/issues/<N>/next-steps.md` exists only in the workspace's checkout; it proves a claim finished in that checkout, not elsewhere.

Key Takeaways
- Re-run safety limits the damage of a duplicate dispatch to cost (full re-run) and, across different logins, to duplicate comments and double assignment.
- The poller's own dispatch record must be written before the launch (the launch can succeed with a lost reply, section 12) and must survive a workspace restart.

## 11. Environment, interactivity, why the claim stops, and the design-only pipeline (questions 4 and 5)

Environment a claim needs (all from the files above):
- `origin` remote that is a GitHub URL, read from the session's current directory (origin_repo.py:156-174). So the session must start inside a checkout of `IronbellyOrg/IronClaude`.
- `uv` (Wave 0 runs `uv run --no-project python ...`, claim.md:14) and `gh auth status` succeeding (claim.md:16) with rights to read the issue, edit assignees and comment; `git fetch origin` access (claim.md:28).
- The skill and command installed (`~/.claude/skills/sc-issue-protocol/`, issue.md:93), the three issue-worker agents (SKILL.md:58-60), and the `sc-recommend` skill (claim.md:78).
- A session that serves `claude-gw-tier3`, `claude-gw-tier2` and `claude-gw-tier1a` (refs/tiers.md:11-15, :32-40), else `E-TIER-UNAVAILABLE` at Wave 1.
- ClickUp variables only if ClickUp assignment is wanted (clickup_claim.py:8-19); otherwise the claim comment reports "skipped" and the claim continues (SKILL.md:133).
- No terminal is required by the claim itself; the Claude Code session needs one only because Orca starts it as a terminal agent.

Interactivity: the claim asks the user nothing. `/sc:recommend` questions are written into `recommend.md` and the default row is used (claim.md:79; SKILL.md:134). [CODE-VERIFIED] Residual prompts outside the claim: Claude Code tool-permission prompts, which depend on the launch arguments. On this machine Orca's `agentDefaultArgs.claude` is `--dangerously-skip-permissions` (`/home/coder/.config/orca/profiles/local-default/orca-data.json`, read 2026-11-07); the Coder workspace value is [UNVERIFIED]. Reconciled with file 03 in fix cycle 1 (QA finding 3): `CCSESSION_PERMISSIONS=default` does NOT by itself make a launched session stall on prompts, because `ccsession-tag/README.md:534` says flags the caller passes, "such as Orca's default `--dangerously-skip-permissions` option", still apply; the launch profile reads `agentDefaultArgs[agent]` and, when nothing typed is set, falls back to Orca's YOLO default for `claude`, `--dangerously-skip-permissions` (`/opt/Orca/resources/app.asar.unpacked/out/shared/agent-launch-profile.js:12-14`, `.../shared/tui-agent-permissions.js:16`, read this session). Whether the `orca agent launch` CLI route builds its Claude command through that profile is [UNVERIFIED] (not traced). Full treatment in `research/03-governance-and-security-surface.md` section 2.2 (ccsession row). The ccsession name question is not asked when a prompt is carried (ccsession-tag/README.md:272; `ccsession-orca` lines 56-125 set `task_carried=1` for a positional argument).

Why the claim stops, and what running the next steps would take (question 5):
- It stops by design (B2): issue.md:15, :79, :83; SKILL.md:17, :88, :146, :150; claim.md:80, :90; `templates/next-steps.md:5` "Run these in your own session, in order. `/sc:issue` does not run them." [CODE-VERIFIED]
- A command-level test file (`tests/commands/test_issue_command.py`) has no hit for "never runs", "Will Not", "B2" or "stop after", so whether tests pin the stop text is not shown by this search. [UNVERIFIED; other test files (`tests/skills/test_issue_protocol.py`) were not read]
- Running them would need: (a) removing B2 in issue.md, SKILL.md and claim.md and the tests that pin it; (b) the proposed `--claim --pipeline <level>` interface of `docs/designs/sc-issue-launch-level-hook.md`: the claim script would write `pending/<nonce>` and launch with a prompt `[sc-launch:v1:<nonce>] ...` (design L52, IR-1/IR-2 at L349-350); (c) the launch-level guard that governs such a session.
- `--claim --pipeline` is design only: `issue.md` contains no occurrence of "pipeline" (Grep count 0; argument-hint L8 and Options L35-41 list none); the design says "current claim code does not implement this proposed pipeline interface" (design L34) and "Full enforcement is not runtime-approved ... blocking actor-selection prerequisite B-CTX" (L17); the only implemented piece is `src/superclaude/hooks/scripts/launch-job-identity.sh` (Glob of `launch-*.sh` found only it; `launch-level-guard.sh`, listed as "proposed" at design L40, does not exist). [CODE-VERIFIED]

Key Takeaways
- The workspace needs: a checkout of the repo with `origin`, `gh` auth for the owner's login, `uv`, installed skills/agents, and a model gateway that serves the tier picker IDs. Nothing needs a person at the keyboard, but nothing writes a result a poller can read.
- Claim-only (owner decision) matches what the code can do today; the pipeline route is design only with a blocked governance gate.

## 12. Ways to start a top-level Claude session with a prompt, and the `orca agent launch` contract (question 6)

Entry points:

| Entry point | Evidence | Requires | Notes for a poller |
|---|---|---|---|
| `orca agent launch --agent claude --worktree <selector> --prompt "<text>" --surface terminal [--json]` | `orca agent launch --help` run locally; `/opt/Orca/resources/app.asar.unpacked/out/cli/specs/agent-launch.js:9-33`; handler `.../handlers/agent-launch.js:11-35`; request `.../agent-launch-request.js:38-117`; repo rule `src/superclaude/core/CLAUDE.md` section "Orca session launches" (L45-53) and `ccsession-tag/README.md:228-237` | A running Orca runtime (`client.call`, handler L23-35); an existing Orca workspace (`createsWorktree: false`, handler L12-14) | The path the owner decision names |
| `ccsession-orca` as Orca's Claude command | `ccsession-tag/README.md:211-226`; `~/.local/bin/ccsession-orca` is a symlink to `~/.claude/skills/ccsession-tag/ccsession-orca` (249 lines) | Orca Settings > Agents > Claude > Command set to its absolute path, one executable with no arguments (README:216-223) | Optional for function, adds session names. On this machine `agentCmdOverrides` is `{}` (not configured). The Coder value is [UNVERIFIED] |
| Plain headless `claude --print` | `src/superclaude/cli/pipeline/process.py:134-166` (`claude --print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns N --output-format stream-json`, prompt on stdin per its docstring L137-138); `max_turns` default 100 (L91) | `claude` on PATH | A one-shot run, no session to attach to, not resumable (`--no-session-persistence`, L152); ccsession README:278 says print mode is untagged. Whether `/sc:issue` runs correctly under `--print` is [UNVERIFIED] |
| `orca orchestration send` into a live coordinator | `orca orchestration send --help` run locally: `--to <run:id|dispatch:id|legacy_handle>`, `--subject`, `--body`, `--type` ...; `.dev/orca-command-refactor/inventory/orca-capabilities.md:66` | A coordinator Run or Dispatch to address | "Enqueue is durable but does not interrupt you, so nothing arrives unless you look": [CODE-VERIFIED] in Orca's own guide text `.../cli/bundled-skill-guides.js:3158` (also :2413 "best-effort attention only and does not prove the recipient read or accepted it") |
| `orca terminal send --terminal <handle> --text <text> --enter` | `orca terminal send --help` run locally: "Send input to a live terminal" | A runtime-issued terminal handle (needs a prior `terminal list`) | Types immediately into whatever is on that terminal, competing with a person or an unfinished prompt |

Tradeoff, new top-level session per issue vs typing into a live coordinator session (analysis F4, `.dev/issues/331/analysis/analyze-sc-issue-protocol.md:35`):
- New session per issue (`orca agent launch`): isolated (a failed claim affects only its own session), clean context window, no competition with a person, auto-named from the prompt's first words (README:272), and its own `.dev/issues/<N>/` output in the targeted worktree. Costs: one more tab and Claude process per issue; nothing in the claim closes the session after it stops (SKILL.md:88), so tabs accumulate [inference, not observed]; the session is not a worker run (section 7), so there is no coordinator visibility.
- Typing into a live session: `orchestration send` is pull-only, so the claim does not start until the session looks (orca-capabilities.md:66; guide text at bundled-skill-guides.js:3158), and a message is not a prompt that the session is known to run as `/sc:issue` [UNVERIFIED]; `terminal send` is immediate but collides with a person's input and puts the claim's output and context into a session the person is using. The WORKER-CONTRACT coordinator rules (L66) describe a coordinator that plans and dispatches, not one that runs claims.
- Evidence supports F4's conclusion for the new-session route; the point about competing with a person is a judgement from the `terminal send` help text ("live terminal") and the pull-only guide text, not from a run.

`orca agent launch` argument contract, for the poller's injectable launch function and its mock:

| Part of the contract | What the files show | Tag |
|---|---|---|
| Invocation | `orca agent launch --agent <id> [--worktree <selector>] [--prompt <text>] [--model <id>] [--effort <level>] [--surface chat\|terminal] [--focus] [--retry-launch <operationId>] [--json]` (specs/agent-launch.js:9; help output) | [CODE-VERIFIED] |
| Agent id | `--agent` is required; must be a known TUI agent else `invalid_argument` "Unknown TUI agent" (request.js:32-37); `claude` is known (`shared/tui-agent-config.js:15`) | [CODE-VERIFIED] |
| Which worktree or repo | `--worktree <selector>` (`identity:`, `id:<repo-id>::<path>`, `name:`, `branch:`, `issue:<n>`, `path:<abs>`, `active`, `current`; help text). Omitted, `active` or `current` resolves from the caller's cwd (handler.js:18-22; `agent-workspace-selector.js:10-48`). A remote server requires `--worktree` (handler.js:15-17). There is no `--repo` flag: the checkout is chosen only by the worktree | [CODE-VERIFIED] |
| Needs an existing worktree | Yes: target `{kind: 'existing', worktree}` and `createsWorktree: false` (handler.js:12-14, :30-33); a new checkout needs `orca worktree create --agent` (spec note L24) | [CODE-VERIFIED] |
| Terminal vs chat | `--surface terminal` always runs the agent CLI; without it the host's Chat UI setting decides (spec note L22-23; request.js:2); `--surface` other than chat or terminal is refused (request.js:21-30) | [CODE-VERIFIED] |
| How the initial prompt is passed | `--prompt <text>` becomes `{text, delivery: 'submit'}` (request.js:63-65): submitted, not left as a draft. A prompt that is empty or only whitespace is dropped silently and the agent starts with no prompt (request.js:63 `prompt.trim()`). A valueless `--prompt` is rejected (request.js:51). A host without the prompt-carry capability is refused with `incompatible_runtime` (request.js:84-86) | [CODE-VERIFIED] |
| Mechanism by which Claude receives it (argv vs paste) | `tui-agent-config.js:15-21` gives Claude `promptInjectionMode: 'argv'` and `draftPromptFlag: '--prefill'`; `orca-capabilities.md:47` says the task is passed on the command line for Claude on the `worker-start` path. Which path `agent launch` takes lives in the host runtime, not in the unpacked CLI directory | [UNVERIFIED] |
| Whether Claude Code runs a leading `/sc:issue` given this way as a slash command | Not shown by any file. `WORKER-CONTRACT.md:93` arranges that "the Task text never starts with `/sc:`" without stating why | [UNVERIFIED]; needs one owner-run live test in the live-plan phase |
| Agent command | Orca runs the configured Claude command, `ccsession-orca` only when set in Orca Settings (README:216-223); locally `agentCmdOverrides` is `{}` | [CODE-VERIFIED] locally; Coder [UNVERIFIED] |
| Name question | Not asked when a prompt is carried (README:272; `ccsession-orca` lines 56-125, positional sets `task_carried=1`) | [CODE-VERIFIED] |
| Success output | text lines `agent: terminal` or `agent: chat session`, `handle`, `sessionId` (chat only), `worktreeId`, `operationId`, `why`, `prompt: <outcome>`, `warning` (request.js:105-117); with `--json` the result object `{outcome{kind,handle,sessionId?}, receipt{detail}, worktreeId, operationId, prompt{outcome}, warning}` via `printResult` (handler.js:34) | [CODE-VERIFIED] for fields; exact JSON key nesting printed by `printResult` not read: [UNVERIFIED] |
| Exit status | Error: `reportCliError(...)` then `process.exitCode = 1` (`cli/index.js:128-137`); success leaves the default 0 (no assignment found in the success path) | [CODE-VERIFIED] by reading; not executed |
| Lost reply | `--retry-launch <operationId>` replays the same launch; "Never retry as a fresh launch" (spec note L27). On an unconfirmed outcome the CLI throws `agent_session_operation_unknown` with `launchOutcome: 'unknown'`, `retrySafe`, `operationId`, `recoveryCommand`, `nextSteps`, message "the agent may already be running and the prompt may already be submitted" (`agent-launch-recovery.js:54-64`) | [CODE-VERIFIED] |
| Other refusals | `incompatible_runtime` when the host cannot start agents or lacks surface or focus capability (handler.js:24-29; request.js:87-92); `Setup decision required for this repository` passes through (recovery.js:21-24) | [CODE-VERIFIED] |

What the mock must do: accept exactly that argv (list form, never a shell string) and record `--agent`, `--worktree`, `--surface`, `--prompt`; succeed with exit 0 and JSON; fail with exit 1; simulate the unknown-outcome error that carries an `operationId`; and let a test assert that the recorded prompt equals `/sc:issue --claim <int>` and nothing else. It should also simulate "the cwd is not inside an Orca workspace" (selector resolution failure), because a poller started outside an Orca workspace has no `--worktree` default. [Mock shape derived from the sources above; the real JSON error body is UNVERIFIED.]

Key Takeaways
- `orca agent launch` is installed and documented locally, takes the prompt as a submitted prompt, needs an existing worktree and a running Orca, and signals failure with exit 1 and a recoverable unknown-outcome error. Both the delivery mechanism and whether a leading slash command is executed need one live check that this research must not run.
- The launch reply can be lost after the session started, so the poller's dispatch record must exist before the launch and a lost reply must be treated as "dispatched", never relaunched fresh.
- The poller needs a way to know its worktree (`--worktree path:<abs>` for the repo checkout) because there is no repo option.

## 13. Integer-only prompt (question 8, owner rule)

- Can the initial prompt be the single line `/sc:issue --claim <N>` with nothing else? The launch side accepts any text in `--prompt` (request.js:50, :63-65); `ccsession-orca` takes a positional argument as the task and starts a session without a question (lines 56-125; README:272). The command accepts `--claim <number>` with nothing else (issue.md:29, :37). Nothing in the files requires extra text. So yes on the files read; the live behaviour of a leading slash command given as an initial prompt is [UNVERIFIED] (section 12).
- What `/sc:issue --claim <N>` accepts beyond an integer: `#N` and an issue URL on origin (origin_repo.py:74, :102-153; issue.md:37). Everything else is rejected by `origin_repo.py` (exit 4 for non-numbers, exit 3 for a foreign repository, section 5), but only for the string the model passes in `--claim "<argument>"` (claim.md:14).
- What the integer-only rule does and does not protect: the initial prompt carries no issue text, but the claim itself reads the issue body and comments (`gh issue view --json ...,body,...,comments`, claim.md:26) and its accuracy-check worker checks "each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code" (claim.md:56). The workers have a Bash tool (agent list: `issue-worker-t1/t2/t3` tools include Bash). So untrusted issue text still reaches a model inside the session, just not as the prompt. The remaining trust boundary is the "human-approved" gate before dispatch: who may apply the approval label or assignment. [Analysis from claim.md:26, :56 and the agent tool lists in the session's agent catalogue; the agent files themselves were not read.]
- The poller must build the prompt as `"/sc:issue --claim " + str(int(number))` where `number` comes from the `number` field of `gh ... --json number` output, reject anything that is not a positive integer, and pass it as one element of an argument list (no shell). A prompt starting with `/` cannot be read as an option by `ccsession-orca` (its loop treats `-*` as options at `ccsession-orca:110`, and only a first positional word equal to `mcp`, `config`, `doctor`, `update`, ... is a subcommand, line 116; any other positional becomes the task, line 119). [CODE-VERIFIED by reading `/home/coder/.claude/skills/ccsession-tag/ccsession-orca`, which is a symlink target of the repo's installed copy]

Key Takeaways
- Prompt contract: exactly one line, `/sc:issue --claim <positive integer>`, built from `int()`, no issue-derived text.
- Integer-only protects the prompt, not the claim's own reading of issue text; the approval gate is the real boundary.

## Gaps and Questions

Open items:
1. Whether `/sc:issue --claim <N>` runs correctly when given as an initial prompt by `orca agent launch --prompt` (slash command executed, session submits it) is not shown by any file. One owner-run live test is needed in the live-plan phase; this research ran nothing live.
2. Whether `agent launch` passes the prompt as argv or as a typed paste (host runtime, not in the unpacked CLI), and the exact JSON error body of `reportCliError`.
3. Whether one person has several workspaces polling with one login (same-login race, section 9).
4. Whether the Coder workspace has: an Orca runtime reachable by the poller, `ccsession-orca` configured, the `claude-gw-tier*` picker IDs served, `--dangerously-skip-permissions` or another permission mode, `gh` authenticated as the person, ClickUp variables.
5. Whether the token that `gh` holds in a workspace can read the org Project (needed for the Project and Backlog filters); `gh project item-list --help` did not state the scope.
6. Whether tests pin the claim-stops-after-`next-steps.md` text (`tests/commands/test_issue_command.py` has no hit; other test files unread).
7. Whether `<D>` already existing is tolerated on re-run (claim.md:18 says only "Create `<D>`").
8. Whether `--claim` under `claude --print` works (only relevant if the headless route is chosen).
9. **[UNVERIFIED] Where the 5-minute poller runs and where it keeps its dispatch record (added in fix cycle 1, QA finding 2).** Under option A the poller is the whole "Coder-side listener", and its host is not established by any file read. Specific unknowns: (a) whether a Coder workspace has `cron`, a systemd user session or any other scheduler, or only a foreground shell loop; (b) whether the poller process survives a workspace autostop, stop/start or restart, and what restarts it; (c) where durable state can live (a path that persists across a workspace restart versus an ephemeral path) for the dispatch record that sections 10 and 12 say must be written before the launch and survive a restart; (d) whether a stopped workspace polls at all (a stopped workspace cannot dispatch, so issues approved while it is stopped wait until it starts). Evidence available in the repo: none for Coder; the repo only shows that the poller must be a plain process outside any Claude session (section 7, WORKER-CONTRACT.md:61) and that `orca agent launch` needs a running Orca runtime (section 12, handler.js:23-35). Owner of the question: web-02 (Coder autostop and scheduling, listed at `research-notes.md:85`) and the live plan phase; this file did not check any Coder documentation.

Claims tagged UNVERIFIED or CODE-CONTRADICTED:
- [CODE-CONTRADICTED] The issue text's expectation that `/sc:issue --claim` kicks off the full orchestration path: contradicted by issue.md:15, :79, :83, claim.md:80, `templates/next-steps.md:5`.
- [UNVERIFIED] That a poller-launched ordinary session is outside the never-as-worker list as an owner intent (my reading of WORKER-CONTRACT.md:11, :23).
- [UNVERIFIED] Argv vs paste delivery of `--prompt`; slash-command execution of a leading `/sc:issue`; JSON key nesting of `agent launch --json`; real JSON error body.
- [UNVERIFIED] Multi-assignee behaviour on GitHub (inferred from the additive flag text); the double-claim outcome in section 9 is derived from code, not observed.
- [UNVERIFIED] That Claude sessions started by Orca stay open after the claim stops (inference from SKILL.md:88).
- [UNVERIFIED] Same-login multiple-workspace polling; Coder workspace configuration items in item 4 above.
- [UNVERIFIED] Whether `/sc:issue` works under `claude --print`.
- [CODE-VERIFIED, noted for the spec] `--claim --pipeline` is design only (issue.md has no "pipeline"; design L17, L34; `launch-level-guard.sh` absent).

## Stale Documentation Found

- [STALE DOC] None found among the files read as contradicting current code on the claim flow: issue.md, SKILL.md, claim.md, origin_repo.py, clickup_claim.py and the analysis file agree line for line on the points checked.
- [STALE DOC risk] `.dev/orca-command-refactor/inventory/orca-capabilities.md` is a team-written inventory: the pull-only statement at its line 66 is quoted from Orca's guide text, which this research re-found in `bundled-skill-guides.js:3158` and :2413, so it is current for the installed Orca. Its `/opt/Orca` line citations were not re-checked beyond `tui-agent-config.js:15-22`, which matched.
- `.dev/issues/331/analysis/analyze-sc-issue-protocol.md` L26 says the repo has no trigger or approval label; confirmed for `labels.md` (no such label in the fixed set) but the live label list of the repo was not re-read (`gh label list` not run here).
- `docs/designs/sc-issue-launch-level-hook.md` is authoritative "for new planning" but its status table marks `launch-level-guard.sh` "proposed" (L40); the file does not exist, consistent with the design's own status.
- Analysis finding F2 recommends a "pull model"; it is consistent with the owner decision A and needs no change.

## Summary

`/sc:issue --claim <N>` is non-interactive, claims only (assign, optional ClickUp, accuracy check, summary, two marked comments) and stops by design at `next-steps.md`; running the next steps is design-only and blocked. It validates its argument in code in `origin_repo.py` (positive integer, `#N` or an origin issue URL), assigns `@me` (the session's `gh` login), stops without writing on a closed issue, a pull request or an issue assigned to someone else, and has no mutual exclusion, so two logins racing for an unassigned issue can both claim it; "already assigned to this login" is the routing rule the claim already understands. A poller can start the session with `orca agent launch --agent claude --worktree <path:...> --surface terminal --prompt "/sc:issue --claim <int>"` (installed locally; prompt delivered as a submitted prompt, existing worktree required, exit 1 on error, unknown-outcome errors carry an `operationId` and must never be relaunched fresh); `/sc:issue` is never-as-worker, so an ordinary top-level session is the only route. Three things could not be verified without a live run and are flagged: slash-command execution of the initial prompt, the prompt delivery mechanism, and the Coder workspace configuration.

