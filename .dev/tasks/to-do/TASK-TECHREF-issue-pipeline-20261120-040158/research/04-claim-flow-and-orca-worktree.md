# Research: /sc:issue --claim flow and orca_worktree.py
**Investigation type:** Code Tracer + Doc Analyst
**Scope:** commands/issue.md, skills/sc-issue-protocol/**, agents/issue-worker-t*.md, two design docs, eight test files
**Status:** Complete
**Date:** 2026-11-20
---

Source root for every path below: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/` unless an absolute path is given (called `SRC/` from here). Skill root `SK/` = `SRC/skills/sc-issue-protocol/`. Line numbers were read from the live snapshot files in this run.

## 1. Command front: SRC/commands/issue.md (117 lines, version "1.1.0")

- Frontmatter: name `issue`, version "1.1.0" (issue.md:2-3), argument-hint at :9. [CODE-VERIFIED]
- Two modes, `--claim` and `--create`, on the repo `origin` points at (:14-17). Both post directly to GitHub, nothing shown for approval first (:19).
- Options table :36-44: seven flags (`--claim`, `--create`, `--depth`, `--mode`, `--type`, `--pipeline`, `--submit`). `--pipeline` values `worktree|full|none`, default "`full` or `worktree`, picked from the issue" (:43). `--submit` only with explicit `--pipeline full` (:44). "There is no repository option ... no dry-run option and no preview option" (:46).
- Watcher rule: "The issue watcher never relies on the default: it always passes `--pipeline none`" (:48). This is command prose only; whether any code passes it belongs to the watcher research files (research 01-03).
- STOP rules (checked before Activation) :50-59:
  - exactly one of --claim/--create else STOP + Usage (:52)
  - `--depth/--mode/--type` with --claim: `E-CREATE-ONLY-FLAG` (:53)
  - unknown value for depth/mode/type: STOP list allowed (:54)
  - empty --create description or empty/missing @path: STOP (:55)
  - empty --claim argument: STOP + Usage (:56)
  - `--pipeline/--submit` with --create: `E-CLAIM-ONLY-FLAG` (:57)
  - bad `--pipeline` value or no value: STOP list the three values (:58)
  - `--submit` with a value, without `--pipeline full`, or with no `--pipeline`: `E-SUBMIT-NEEDS-FULL` (:59)
- Outputs table :74-81. Claim files under `.dev/issues/<N>/`: `scout.md`, `clickup.json`, `accuracy-check.md` (posted), `issue-summary.md`, `analysis/analyze-<scope>.md` (only if out of date), `recommend.md`, `next-steps.md`, `launch-prompt.md` (not for `none`), `claim-comment.md` (posted), `worktree.json` (never copied into worktree; not written for `none`) (:80).
- Coordinator handoff paragraph for `--pipeline none` (:85): coordinator runs the `worktree` step of `orca_worktree.py`, then `worker-start --worktree path:<printed path>`; the script creates the worktree with no agent, copies `.dev/issues/<N>/` first and closes the first plain tab. The same paragraph is repeated at SK/SKILL.md:140 and SK/refs/claim.md:96 (three copies). The coordinator side (adoption row `reserved`, `worker-list`) is prose here; the coordinator contract text is covered by research file 06. [UNVERIFIED in this file: nothing in the claim scripts implements an adoption row.]
- Will / Will Not :89-102: will not run /sc:implement, /task, commit, push or /sc:pr-submit itself; will not create labels, issue types, issue fields, ClickUp tasks; no field except Complexity; never stage/commit `.dev/issues/`; no Orca link flag; never merge.
- Activation :104-110: "MANDATORY ... invoke Skill sc:issue-protocol".
- Ship-gate prose at :16: no governed claim (`worktree` or `full`) on a real issue until OB-H1 item 1, OB-H2, OB-H3 pass. Prose only (verified in section 5 that no code checks it).

Key Takeaways
- The command file is a front: flag validation (STOP rules) is prose executed by the model, not code (`orca_worktree.py` only re-checks that `--submit` needs `--level full`, see section 5).
- The default pipeline level is stated at issue.md:43 and SK/refs/claim.md:81; the watcher is told to always pass `none` (issue.md:48).

## 2. Orchestrator protocol: SK/SKILL.md (197 lines)

- Frontmatter allowed-tools: `Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion` (SKILL.md:4).
- Files table :24-50 (refs, scripts, templates). `scripts/orca_worktree.py` is "the only file that calls `orca`" (:35).
- Worker spawn rule :54-64: `subagent_type: issue-worker-t<N>`, never the `model` parameter. Picker IDs table :58-62: t3 `claude-gw-tier2b`, t2 `claude-gw-tier2`, t1 `claude-gw-tier1b`. T1 -> T2 fallback only for t1 (:64); t2 and t3 have no fallback; failed spawn = STOP `E-TIER-UNAVAILABLE`.
- Worker contract :66-68: read-only GitHub and git, write only under `.dev/issues/`, return only the paths they wrote; empty or missing file -> retry once -> STOP `E-WORKER-NO-OUTPUT`.
- GitHub call rules :70-78. The write line at :74 lists every orchestrator write: `gh issue edit <N> --repo <R> --add-assignee @me`, `gh issue comment <N> --repo <R> --body-file <file>`, `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<file>`, `gh issue create --repo <R> ...` (create adds `--type <name>`), `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`, `scripts/clickup_claim.py`. "Workers never write to either."
- One exception to the `--repo` rule at :73: the T3 worker reads `orgs/<owner of R>/issue-fields` (read-only GET).
- Claim waves :80-92 (Wave 0 to 8); create waves :94-103; return contract :105-150 (nine base fields :109-119, ten claim fields :123-134, three create fields :144-148); error table :152-177.

### Claim waves and owners (verified against SK/refs/claim.md)

| Wave | What | Actor | Evidence |
|---|---|---|---|
| 0 | `origin_repo.py --claim`, `gh auth status`, `orca_worktree.py preflight`, default branch via `gh repo view`, mkdir `<D>` | orchestrator (the model running the skill) | refs/claim.md:11-21; SKILL.md:84 |
| 1 | Lookup, writes `scout.md` | worker issue-worker-t3 (T3) | refs/claim.md:23-34; SKILL.md:85 |
| 2 | Edge cases from scout.md | orchestrator | refs/claim.md:36-44 |
| 3 | Assign on GitHub, then ClickUp script | orchestrator | refs/claim.md:46-51 |
| 4 | Accuracy check + summary (+ analysis if out of date) | worker issue-worker-t2, or t1 when scout sizes `complex` (t1 -> t2 fallback once) | refs/claim.md:53-63 |
| 5 | `Skill sc-recommend`, write `next-steps.md`, resolve level `<L>`, plan boundary, render launch prompt | orchestrator (calls script `prompt`) | refs/claim.md:75-84 |
| 6 | Post/edit accuracy-check comment and claim comment | orchestrator | refs/claim.md:86-96 |
| 7 | Worktree create/reuse | orchestrator runs `orca_worktree.py worktree` (no worker) | refs/claim.md:98-115 |
| 8 | Launch | orchestrator runs `orca_worktree.py launch` (no worker) | refs/claim.md:117-136 |

Final output: refs/claim.md:138-150. `--pipeline none` ends after Wave 6 (refs/claim.md:94; SKILL.md:90).

Key Takeaways
- Waves 1 and 4 are the only worker waves in the claim; every write to GitHub, ClickUp or Orca is the orchestrator's.
- "Orchestrator" is the Claude session that invoked the skill, not a program: no Python runs the waves in order. The only code is three helper scripts (origin_repo.py, clickup_claim.py, orca_worktree.py).

## 3. Worker agents and tier pins

| Agent file | Lines | `model:` pin (frontmatter line 6) | Other frontmatter | Jobs |
|---|---|---|---|---|
| SRC/agents/issue-worker-t1.md | 36 | `claude-gw-tier1b` | tools `Read, Grep, Glob, Write, Bash` (:5) | claim Wave 4 when scout sizes `complex`; create flag choice at standard/deep; independent flag variant (deep); deep body (:21-24) |
| SRC/agents/issue-worker-t2.md | 36 | `claude-gw-tier2` | same tools | claim Wave 4 for simple/medium; create flag choice (quick); flag validation (standard); standard body (:21-24) |
| SRC/agents/issue-worker-t3.md | 36 | `claude-gw-tier2b` (:6) | `effort: low` (:7) | claim lookup (scout.md); create lookup; quick-depth body (:22-24) |

- Tool list has no Edit, so workers cannot edit existing source (t1:5, t2:5, t3:5). Write only under `.dev/issues/` is a prose rule (`Rules`, :30 in each).
- Worker "return contract": "Return only the path of each file you wrote, one per line, and nothing else" (t1:35, t2:35, t3:35). The orchestrator reads each file from disk (SKILL.md:66).
- Read-only GitHub rule (t*:28): only read `gh` calls with `--repo <R>`; never `gh issue edit/comment/create`, `gh label create`, `gh api -X` other than GET, or ClickUp. Only git write: `git fetch origin` (:29).
- Tier map in SK/refs/tiers.md:9-15 agrees with the three pins and with SKILL.md:58-62 [CODE-VERIFIED: agent files `model:` lines read]. Pin-versus-design: see Stale Documentation (design says T3 = claude-gw-tier3).
- SK/refs/tiers.md:17 records why t3 is Tier 2b: "since the 2026-11-12 owner decision (issue 488) it is pinned to ccsession Tier 2b (GPT-6.1 Terra first)". t3:12 repeats this and says keep `effort: low`.
- SK/refs/tiers.md:23-26: the Agent call `model` parameter accepts aliases only and overrides frontmatter, so the skill passes only `subagent_type` (verification claim cites Claude Code docs; external, [UNVERIFIED] by source here).
- T1 -> T2 fallback: tiers.md:34-42. Trigger: spawn of `issue-worker-t1` fails because `claude-gw-tier1b` is not served (the proxy answers HTTP 400 `invalid_request_error`, message starts `ccsession tier1b:` [UNVERIFIED: proxy behaviour is outside the snapshot's checked code]). Retry once with `issue-worker-t2`; T2 file starts `Handled by issue-worker-t2 (tier 2): tier1b is not available to this user.` (tiers.md:39). No fallback for T2, T3 (tiers.md:42). No alias fallback (tiers.md:52).
- `E-TIER-UNAVAILABLE` text tiers.md:44-50; the heading appears twice (tiers.md:32 and :44, first one empty) [STALE DOC: formatting duplication only].
- Which job goes to which tier for Wave 4 is the scout's complexity guess (refs/claim.md:55) and the next-step tier line is separate: `/model claude-gw-tier2` simple, `/model claude-gw-tier1b` medium/complex (claim.md:80, chains.md:11-16).

Key Takeaways
- Pin lives in agent frontmatter (line 6); the skill never passes `model`. T3 is pinned to tier2b, not tier3.
- Only one fallback exists in the whole protocol: t1 -> t2, once, to a sibling agent file.

## 4. Chains, level resolution

- SK/refs/chains.md (40 lines): six default rows at :9-16 (Feature simple/medium/complex, Bug simple/medium/complex). Tier line `/model claude-gw-tier2` for simple, `/model claude-gw-tier1b` for medium/complex. The goal format passed to `Skill sc-recommend` is :27-38; `/sc:recommend` makes the final pick (:7). `/sc:issue` never runs these commands (:7).
- Level rule (SK/refs/claim.md:81, Wave 5 step 3): explicit `--pipeline` always wins. If omitted, read Type, Complexity, Effort estimate from `issue-summary.md`; if any cannot be read -> `worktree` (this check first, so an unreadable-hours bug also gets `worktree`); else `full` for every bug (including complex), `full` for a simple/medium feature of 16 hours or less, `worktree` for a complex feature or one over 16 hours. The printed line is `Level: <L> (explicit)` or `Level: <L> (default: <reason>)` with reasons `bug`, `simple or medium feature of 16 hours or less`, `complex feature`, `feature over 16 hours`, `could not read type, complexity or hours`. `--pipeline none` prints no level line.
- Plan boundary rule: claim.md:82 (`Plan boundary: after step <K>`, K = last step before the first `/sc:implement` or `/task`; `before step 1` when the first step is the implement step). Level `worktree` stops there; `full` ignores it.
- The rule is prose executed by the orchestrating model: Grep over the whole snapshot `src/` for the reason strings is done in section 5.

## 5. Writes to GitHub and ClickUp (claim path, then create path)

All writes are made by the orchestrator (the model running the skill). Workers are read-only (agents t1/t2/t3 line 28 each). No write is made before Wave 3 for GitHub and none before the Orca preflight passes (refs/claim.md:21).

### 5a. Claim path writes

| # | Write | Exact command | Actor | Wave | Evidence |
|---|---|---|---|---|---|
| C1 | Assign issue to the current user | `gh issue edit <N> --repo <R> --add-assignee @me` | orchestrator | 3 | refs/claim.md:48; SKILL.md:74,87 |
| C2 | ClickUp assignee add (only if a task matches) | `PUT https://api.clickup.com/api/v2/task/{task_id}` body `{"assignees": {"add": [<user id>]}}` via `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"` | orchestrator runs the script | 3 | clickup_claim.py:232-237; refs/claim.md:50 |
| C3 | Accuracy-check comment, new | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md` | orchestrator | 6 | refs/claim.md:91 |
| C3' | Accuracy-check comment, edit of earlier marked comment | `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | orchestrator | 6 | refs/claim.md:89 |
| C4 | Claim comment, new | `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md` | orchestrator | 6 | refs/claim.md:92 |
| C4' | Claim comment, edit | `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/claim-comment.md` | orchestrator | 6 | refs/claim.md:92 |
| C5 | Later, only at `full --submit`: commit, `git push origin <branch>`, `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` | the launched agent (not the claim) | after Wave 8 | templates/launch-prompt.md:28-34 |

- The claim writes NO labels, NO issue type, NO issue field, NO status change, NO PR itself (issue.md:93-102 "Will Not"; refs/labels.md:7 "`--claim` changes no label, type or field"). [CODE-VERIFIED by absence: the only claim-path `gh` write verbs in SKILL.md:74 are edit --add-assignee, issue comment, api PATCH comments.]
- Posts go up directly; the body is never shown for approval (SKILL.md:76; B1). A failed post -> STOP `E-POST-FAILED` (refs/claim.md:93); a re-run edits instead of duplicating because of the markers `<!-- sc:issue:claim -->` and `<!-- sc:issue:accuracy-check -->` (claim-comment.md:23; accuracy-check-comment.md:20).
- Marker discovery is a read by T3: comment authored by the current login, body contains the marker; ID = number after `#issuecomment-` in the comment url; latest used when several (refs/claim.md:30).
- ClickUp writes: only C2. No ClickUp comment, status or custom field (clickup_claim.py:232-237 is the only non-GET request; `request()` at :104). Token is in the Authorization header only (clickup_claim.py:109), never printed.

### 5b. Claim path read-only calls

| Call | Actor | Where |
|---|---|---|
| `git remote get-url origin` | origin_repo.py | origin_repo.py:159-164 |
| `gh auth status` | orchestrator | refs/claim.md:16 |
| `orca status --json` (preflight) | orca_worktree.py | see section 8 |
| `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name` | orchestrator | refs/claim.md:18 |
| `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` | T3 | refs/claim.md:27; agent t3:22 |
| `gh api user -q .login` | T3 | refs/claim.md:27 |
| `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url` | T3 | refs/claim.md:28 |
| `git fetch origin`; `git log --since=<createdAt> --name-only origin/<B>` | T3 (the fetch is the only worker git write) | refs/claim.md:29 |
| ClickUp `GET /user`; `GET /team/{ws}/task?page&subtasks=true&include_markdown_description=true[&list_ids[]]` | clickup_claim.py | clickup_claim.py:176, :185-191 |
| `/sc:analyze` pass (code reads) | T2/T1 when out of date | refs/claim.md:59 |
| `Skill sc-recommend` | orchestrator | refs/claim.md:79 |

### 5c. Create path writes (the `--create` mode; labelled as the create path, not the claim)

| # | Write | Exact command | Actor | Wave | Evidence |
|---|---|---|---|---|---|
| X1 | Create issue | `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md`, `--label "<mode label>"` only when the label exists, `--type "<name>"` only when listed in scout.md | orchestrator | 5 | refs/create.md:92; SKILL.md:103 |
| X2 | Complexity field | `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json` (body `{"issue_field_values":[{"field_id":<id>,"value":"<option name>"}]}`) | orchestrator | 5 | refs/create.md:95; refs/labels.md:43 |
| X3 | Pushback comment (standard/deep with disagreement) | `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` (marker `<!-- sc:issue:create-review -->`) | orchestrator | 5 | refs/create.md:96 |
| (local) | rename `<D>` draft to `.dev/issues/<N>/`; write `complexity-field.json` | filesystem | orchestrator | 5 | refs/create.md:93,95 |

Create-path reads: `gh label list --repo <R> --limit 200 --json name`; `gh api repos/<R>/issue-types`; `gh api orgs/<owner of R>/issue-fields` (GET, the single allowed `orgs/` path); `gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10` (T3, agent t3:23); `gh issue view <N> --repo <R> --json issueType --jq .issueType.name` and `gh api repos/<R>/issues/<N>/issue-field-values` read-backs (refs/create.md:94,95). Create makes no ClickUp call and no self-assignment (create.md:9; SKILL.md:18).

Create-path gates: `E-CREATE-FAILED` when X1 fails, draft kept (create.md:92); `E-POST-FAILED` for X3 (create.md:99); a failed type or field never stops once the issue exists (create.md:99); one user prompt only (AskUserQuestion) when `draft-notes.md` lists new material or contradiction (create.md:84).

Key Takeaways
- Claim path = 1 GitHub assignment + 2 comments (new or edited) + at most 1 ClickUp assignment; create path = 1 issue + 1 field POST + optional 1 comment.
- Every `gh` write passes `--repo <R>`, with `<R>` from `origin_repo.py` only (SKILL.md:72-73).

## 6. Helper scripts

### 6a. SK/scripts/origin_repo.py (195 lines; stdlib only)
- `read_origin()` :156-174 runs only `git remote get-url origin` (:159-164); non-zero or OSError -> `ClaimError("E-NO-ORIGIN", 1, ...)`; non-GitHub -> E-NO-ORIGIN.
- `parse_origin_url()` :86-99 accepts `https://github.com/<o>/<r>[.git][/]` and `git@github.com:<o>/<r>[.git][/]` only (patterns :66-69).
- `check_claim(arg, origin)` :102-153: number or `#number` -> N (:108-110); GitHub URL of another owner/repo (case-insensitive, whole segments) -> `E-FOREIGN-REPO` exit 3 (:135-140); `/pull/<N>` -> `E-NOT-AN-ISSUE` exit 4 (:147-152); non-GitHub URL -> E-FOREIGN-REPO (:114-119); anything else -> E-NOT-AN-ISSUE (:120-124).
- Exit codes: 0 ok, 1 E-NO-ORIGIN, 2 argparse, 3 E-FOREIGN-REPO, 4 E-NOT-AN-ISSUE (docstring :45-50; constants :61-63). `main()` :177-191 prints `{"repo": origin, "number": N}` or just `origin`.
- Repo resolution: the repo is whatever `origin` is, parsed from its URL; no hardcoded name and no gh default. It never consults `gh repo set-default`, gh's fork-parent default or other remotes (docstring :14-15). So it resolves `IronbellyOrg/IronClaude` exactly when the clone's `origin` URL is that repo; it would resolve the upstream only if `origin` pointed there. [CODE-VERIFIED: no occurrence of a fixed owner/repo string in the file; the guarantee that origin is the fork is a property of the clone (CLAUDE.md rule), not of this script.]

### 6b. SK/scripts/clickup_claim.py (270 lines; stdlib urllib)
- Env: `CLICKUP_API_TOKEN` (required), `CLICKUP_WORKSPACE_ID` (required), `CLICKUP_LIST_IDS` optional, `CLICKUP_MAX_PAGES` optional default 20 (`DEFAULT_MAX_PAGES` :74; `max_pages_from_env` :88-94).
- `claim()` :163-242. Outputs (one JSON object, exit 0): `skipped` reason `no_token` (:166) or `no_workspace` (:169); `not_found` (:211); `ambiguous` + `rule` + `candidates` (:213-220); `already_assigned` (:231); `assigned` (:238); `error` reasons `auth` (401/403, :117-118), `rate_limited` (429 retried once after `Retry-After`, :119-123), `page_cap` (:206), `http_<code>` (:124), `network` (:126), `bad_response` (:132,:179), `unexpected` (:242). Exit 2 only for bad arguments (`parse_args` :245-259: positive number, `owner/repo` shape, URL must equal `https://github.com/<repo>/issues/<N>`).
- Matching `match_rule` :148-160: rule 1 `github_link` = issue URL in markdown description or custom-field values (case-insensitive, not followed by a digit); rule 2 `title_number` = `#<N>` token in task name, only if rule 1 found nothing (:208). More than one match is `ambiguous`; nothing assigned.
- Only write: `request("PUT", f"{API}/task/{id}", token, {"assignees": {"add": [user_id]}})` (:232-237). All other requests are GET.
- ClickUp is non-fatal in the claim (refs/claim.md:51) except exit 2 (bad args), which STOPs and keeps the GitHub assignment.

Key Takeaways
- origin_repo.py is the single source of `<R>` and `<N>` (SKILL.md:72) and carries the closed vocabulary E-NO-ORIGIN / E-FOREIGN-REPO / E-NOT-AN-ISSUE with exit codes 1/3/4.
- ClickUp matching is read-then-assign with a page cap; ambiguity and page cap are safe no-ops.

## 7. Templates (SK/templates/, 15 files, not 17)

Glob of the folder returns 15 files: issue-bug-simple, issue-summary, description, recommend-record, create-review-comment, issue-bug-complex, flags-decision, launch-prompt, scout-report, draft-notes, claim-comment, next-steps, issue-feature-simple, accuracy-check-comment, issue-feature-complex. SKILL.md:36-50 lists the same 15. The task brief's "17 files" is [CODE-CONTRADICTED] (15 found). Claim-side templates (7): scout-report (claim section), accuracy-check-comment, issue-summary, recommend-record, next-steps, claim-comment, launch-prompt. Create-side (8): description, flags-decision, 4 issue-* bodies, draft-notes, create-review-comment (+ scout-report create section).

- claim-comment.md (23 lines): `## Claimed by @<login>`; ClickUp line (`assigned task ... | already assigned | skipped (<reason>) | not found | ambiguous (<count> candidates) | error (<reason>)`); Accuracy check verdict; `### Summary` with effort hours, complexity, type, first next step; `### Files` with repo-relative paths to summary, next-steps, analysis plus the note "These links are paths in the repository; they open on GitHub only after someone commits and pushes the files."; ends `<!-- sc:issue:claim -->` (:23).
- accuracy-check-comment.md (20 lines): `## Accuracy check for #<N>`; optional line `Handled by issue-worker-t2 (tier 2): tier1b is not available to this user.` (:4); `**Verdict:** <current | out_of_date>`; claim table and merged-PR table; ends `<!-- sc:issue:accuracy-check -->` (:20).
- issue-summary.md (23 lines): lines `Type:`, `Complexity:`, `Effort estimate: <hours> hours` (:7-9) are what the level rule reads (refs/claim.md:81); optional fallback line (:4).
- next-steps.md (14 lines): first line is the `/model` tier line (:1); `Plan boundary: after step <K>` (:5); numbered steps; effort estimate; optional "Default row not used" line (:14).
- launch-prompt.md (34 lines): four blocks `<!-- block:common -->` :11, `worktree` :20, `full` :25, `submit` :28; assembled by code (`orca_worktree.py prompt`, header :2-9), not by the model. `common` (:12-18): read `issue-summary.md` and `next-steps.md`, run each step through the Skill tool in the session, never by hand and never in a subagent, never merge, never push to master or main. `worktree` (:21-23): stop at the plan boundary, print the plan path and `Waiting for approval`; a human approves only by running a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`; no `/sc:implement`, `/task`, commit, push, `/sc:pr-submit` before approval. `full` (:26): run every step; no commit, push, PR; stage nothing; print `git status --short`. `submit` (:29-34): check no PR is open or merged for the branch (`gh pr list --repo <R> --head <branch> --state all`), conventional commit staging `.dev/tasks` and changed files but never `.claude/` and never `.dev/issues/`, `git push origin <branch>`, `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`, never merge.
- scout-report.md and recommend-record.md exist (listed in SKILL.md:36,39); their bodies were not needed for any claim in this file. [Not read.]

Key Takeaways
- The posted comments are the only template-driven GitHub text on the claim path; both end with a hidden marker used for idempotent re-claim.
- The level behaviour of the launched agent is fixed text in launch-prompt.md assembled by code, but only the L1 guard and L2 hook (research 05) enforce it mechanically; the prompt itself is advisory.

## 8. SK/scripts/orca_worktree.py (1906 lines), all ranges read (1-1906)

Entry: `orca_worktree.py <preflight|worktree|prompt|launch|pending>`; stdlib only; no shell; every runtime outcome prints ONE JSON object and exits 0; exit 2 only for argparse errors (docstring :11-12). Timeouts `DEFAULT_TIMEOUT=120`, `PREFLIGHT_TIMEOUT=30`, `TERMINAL_READ_TIMEOUT=15`, env override `SC_ORCA_TIMEOUT` (:88-91, `_timeout` :120). `run()` :132-166 never raises (a timeout or missing binary returns a failed `Result`).

### 8.1 preflight (`cmd_preflight` :210-223)
argv `orca status --json` (30 s). Prints `{"ok": true}` only when exit 0, JSON object, `ok is True` and `result.runtime.reachable is True`; otherwise `{"ok": false, "detail": ...}` with details "orca status did not print a JSON object", "orca status reported ok is not true", "the Orca runtime is not reachable", or the first stderr line / "command not found" / "timed out". The skill turns `ok:false` into STOP `E-ORCA-REQUIRED` (refs/claim.md:17). Runs for every claim including `--pipeline none`.

### 8.2 worktree create / reuse (`cmd_worktree` :625-738; warning codes in `WARNING_ORDER` :230-239)
- Closed warning vocabulary for the worktree step, in rank order: `W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`, `W-ORIGIN-BASE-STALE`, `W-FIRST-TAB-LEFT` (:230-239). Output keys `status, path, branch, match_key, warning, detail, tracked_files, tracked_known` (`Outcome.as_dict` :265-280). Primary warning is the first by this rank; others go to `detail` as "also <code>: <text>".
- Step 1: `git rev-parse --path-format=absolute --git-common-dir` (:287-291, :629); not in a git checkout -> failed `W-WORKTREE-CREATE-FAILED` "not inside a git checkout" (:630-632). Main checkout = parent of the `.git` common dir (:294-296).
- Step 2: `orca worktree list --repo path:<main> --limit 500 --json` (`list_rows` :314-350). Unusable list (nonzero exit, not ok, no rows array, `truncated: true`, omitted hosts, zero rows, no `isMainWorktree` row) -> `(None, why)`; then `reuse_record(why)` (:635-642) reuses the path in `<D>/worktree.json` only if that dir exists and shares the main git common dir (`guarded_record_path` :361-370), tagged `W-ORCA-LIST-FAILED` note "unverified, reused from worktree.json"; no usable record -> failed `W-ORCA-LIST-FAILED` (:638).
- Step 3: `lookup()` :373-411. Candidates exclude archived and main rows (:396-398). Keys tried in order and the first key with a hit decides: `marker` (row `comment` contains `sc:issue <R>#<N>` not followed by a digit), `record` (row path equals the record path), `basename` (`^issue-<N>(-|$)`), `branch` (same pattern on the branch tail) (:399-404). More than one live hit -> failed `W-WORKTREE-AMBIGUOUS` (:655-658); none live -> failed `W-WORKTREE-STALE` "gone from disk" (:659-662); exactly one -> `finish(... "reused", key)`.
- Step 4 (no hit): `git fetch origin` (result kept), `git rev-parse --verify <base>`; failure of the verify -> failed `W-ORIGIN-BASE-MISSING` (:671-677); failed fetch with a verified base -> note `W-ORIGIN-BASE-STALE` (:678-682).
- Step 5 create argv (:684-700): `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json`. No `--agent`, no `--issue`, no `--pr`. Create failed and not timed out -> failed `W-WORKTREE-CREATE-FAILED` (:701-703). A timed-out create is still checked by relisting.
- Step 6: relist; new rows = ids not in `ids_before` whose basename matches `^issue-<N>(-|$)` (:708-713). More than one -> `W-WORKTREE-AMBIGUOUS` (:714-716); none -> `W-WORKTREE-CREATE-FAILED` "created but not listed" (:717-719); dir missing -> `W-WORKTREE-CREATE-FAILED` (:720-724); else `finish(... "created", None)` and `close_first_tab` (:736-737). A failed relist falls back to `reuse_record` (:704-707).
- `finish()` :527-563: checks `git -C <wt>` common dir equals main common dir (else failed `W-WORKTREE-STALE`, :540-546); `tracked_under` = `git -C <wt> ls-files .dev/issues/<N>` (:414-421); copies `<D>` into `<wt>/.dev/issues/<N>/` with `copy_issue_dir` :439-504 (skips `worktree.json` :466; refuses any symlink component :469-474; never overwrites a tracked file :476-478; a differing untracked file becomes `<name>.prev` :494-497; copy errors -> failed `W-WORKTREE-COPY-FAILED` :555-557; non-error skips -> note under the same code :558-559); then `write_record` (:507-524) writes `<D>/worktree.json` = `{"path", "status"}` via `atomic_write_text` (:183-201; mkstemp + os.replace, mode 0644). A previous `launch` entry survives only for a reused worktree at the same path (:516-523).
- `close_first_tab` :568-622: only for a newly created worktree after a good copy; needs an ok create reply with no `setup` and no `defaultTabs`; argv `orca terminal list --worktree path:<wt> --json`, then, only when exactly one terminal without `agentIdentity` and with a handle, `orca terminal close --terminal <handle> --tab --json`. Every reason it cannot close becomes `W-FIRST-TAB-LEFT` (never changes `status`). A reused worktree gets no `terminal` call.

### 8.3 prompt render (`cmd_prompt` :764-784, `render_prompt` :746-761)
Keeps blocks `common` + the level block (+ `submit` when `--submit`), drops every other block, replaces `<N>` and `<R>`; a missing block raises ValueError -> `{"status": "failed", "detail": ...}`. With `--source` and a `launch` entry in `worktree.json` whose worktree still exists (`guarded_record_path`) and an existing `--out` file, it prints `{"status": "kept", ...}` and writes nothing (:765-777). Otherwise writes with `atomic_write_text` and prints `{"status": "written", "path": ...}`.

### 8.4 Launch constants and the closed code vocabulary (:789-874)
- `PENDING_PARTS = (".claude", "state", "launch-level", "pending")` (:791). The directory is `$HOME/.claude/state/launch-level/pending/`. [CODE-VERIFIED path; `sessions/` is not named in this file at this range, it is described in the claim.md final-output text (refs/claim.md:125) and belongs to the guard (research 05).]
- Shim detection constants: `SHIM_MARKERS = ("[ccsession]", "Session name (Enter or Ctrl+C")` :792; `SHIM_TITLE` regex `sc-launch-v1-[0-9a-f]{1,12}-\d{4}-\d{6}-[0-9a-f]{4}\b` :797; `SHIM_TRIES = 5` :798; `SHIM_INTERVAL = 2.0` seconds, env `SC_ORCA_SHIM_INTERVAL` :799-800.
- `REMEDY` dict :802-817 has exactly four codes: `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `W-L2-ABSENT`.
- `IR7_REFUSE = False` at :822 with the comment "IR-7: turn on only after the #442 observations pass (owner decision 2026-11-08)" [CODE-VERIFIED]. `IR7_REFUSAL` text :823-826. `remedy(code)` :829-831 returns the refusal text for `W-L2-ABSENT` only when `IR7_REFUSE` is True. [Reads of IR7_REFUSE are listed in 8.8.]
- `GOVERNED_TOOLS` :841-867 = 14 names (Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, CronCreate, CronDelete, ScheduleWakeup) plus 9 `mcp__x__*` names (merge_it, push_it, commit_it, pull_request_it, create_or_update_file, delete_file, update_ref, create_ref, create_branch) = 23 [CODE-VERIFIED by count].
- `GUARD_COMMANDS = ("cat","sed","tr","mkdir","mv","ln","rm")` :871.

### 8.5 IR-4 enforcement preflight (`enforcement_preflight(wt)` :955-1045) - READ ONLY, never edits config
Returns a list of failure strings; empty = effective. Checks, in order:
1. `jq`, `uv`, and each of `GUARD_COMMANDS` on PATH (:965-967).
2. `process_interface_gaps()` :877-907: Linux only; `/proc/self/stat`, `/proc/sys/kernel/random/boot_id` exist; `pidfd_open` of own pid via libc and the query form of `prctl(PR_GET_CHILD_SUBREAPER)` (:874 constant 37) both succeed (:968-974).
3. `~/.claude/hooks/launch-level-guard.sh` exists (:975-977), is executable (:979-980) and contains the exact line `# launch-level-guard-version: 1` (:839, :987-988).
4. `CLAUDE_CONFIG_DIR` unset or resolving to `$HOME/.claude` (:989-997).
5. `$HOME/.claude/settings.json` readable as a JSON object (required); worktree `.claude/settings.json` and `settings.local.json` readable if present (:998-1006); `disableAllHooks: true` in any of the three is a failure (:1007-1012).
6. Guard registered on `UserPromptSubmit` (matcher empty, `*` or `.*`) (:1014-1024); on `PreToolUse` for every one of the 23 `GOVERNED_TOOLS` (:1025-1036); `launch-job-identity.sh` registered on `PreToolUse` and firing for `Bash` (:1037-1044).
The result is advisory on the environment of the claim process only (docstring :957-960): "The agent Orca starts may run with another one."

### 8.6 L2 pre-push hook install / status (:1048-1442)
- `l2_status(wt)` :1048-1067 (read only) returns `(state, reason)` with state `owned | absent | conflict | unsupported`. `install_l2(wt)` :1386-1442 returns `installed | owned | conflict | unsupported | unavailable`.
- Preconditions `_l2_preconditions` :1335-1383: `git -C <wt> config --get core.hooksPath` set -> `unsupported` (:1348-1350); `git rev-parse --path-format=absolute --git-path hooks` must equal `<git-common-dir>/hooks` else unsupported (:1356-1367); hooks dir must be a real directory owned by the euid, not group/other writable, else `unsupported` "hooks-dir-unsafe" (:1368-1382). The hook goes into the clone's shared hooks directory `<git-common-dir>/hooks/pre-push` (:1365, :1402), so it covers every worktree of that clone [CODE-VERIFIED; contradicts the loose wording "as the worktree's `pre-push` hook" at refs/claim.md:125, see Stale Documentation].
- Packaged hook source: `$HOME/.claude/hooks/launch-level-pre-push.sh` (`_l2_packaged` :1195-1211, must contain `# launch-level-pre-push-version: 1`, <= 64 KiB, `uv` on PATH). Data file `pre-push.launch-level` (`L2_DATA_NAME` :1079) holds `HOME` on line 1 and the `uv` directory on line 2 (`l2_data_expected` :1162-1175).
- Install steps (:1403-1442): an existing entry is never replaced (`os.path.lexists(entry)` -> report through `l2_status`); data file published with no-replace hard-link (`publish_no_replace` :1123-1158); the hook is staged in a private `.<uuid>` directory and self-tested by `_l2_selftest` :1278-1332 (empty push OK, selector output shape, push to main allowed when the session is ordinary, refusal `L2-UNKNOWN` rc 1 for main and master when the data file is removed, a non-protected ref allowed); only then linked in with `os.link` (:1428). A failed self-test = `unavailable` "the hook self-test failed at step <x>" (:1425).
- Entry verdicts `_l2_entry_verdict` :1249-1275: not a regular file (symlink) / wrong owner / group-or-other writable / foreign content / stale version / not executable / data file differs -> `conflict` with a printed `rm` command, else `owned`. The claim "never deletes them" (:1245).

### 8.7 Launch (`cmd_launch` :1696-1834), publish_pending, pending, shim detection
Order of checks (each can end the command; all print one JSON object, exit 0):
1. No usable worktree record (`guarded_record_path` None) -> `failed`, `W-LAUNCH-FAILED` "no usable worktree record" (:1700-1702).
2. A `launch` entry in `<D>/worktree.json`, or in the mirror `<wt git dir>/sc-issue-launch-<N>.json` (`launch_mirror` :1586-1597, `read_mirror` :1600-1616) -> `already_launched`, no Orca call, detail names both files (:1704-1721). The result carries no level (the level is inside the entry `{level, submit, at}` written by `record_launch` :1619-1643).
3. `stale_prompt` (:1666-1693): worktree copy of `launch-prompt.md` must be byte-identical to `<D>/launch-prompt.md` (symlink, missing or differing -> `failed` `W-LAUNCH-FAILED`, no agent, no hand command) (:1722-1724).
4. IR-4 `enforcement_preflight(wt)` (:1730): any failure -> `failed`, warning `W-ENFORCEMENT-ABSENT`, `enforcement_hook: "missing"`, detail = "the launch-level guard would not be effective: <conditions>. This check verified the claim process only ..." (:1731-1747). No `pending` record is written and no agent is started.
5. `install_l2(wt)` (result ignored) then `l2_status(wt)` (:1754-1756). Not `owned` -> a `W-L2-ABSENT` note with `L2_ABSENT_WHY + reason` (:1756). `if IR7_REFUSE and l2_notes:` -> `failed` (:1757-1758); with the constant False the branch never runs.
6. `publish_pending(word)` with word `full-submit` when `--submit`, else the level (:1759-1761). `publish_pending` (:1488-1512): walks `~/.claude/state/launch-level/pending` creating each missing part 0700 (refuses a symlink or a non-directory, :1493-1499), writes `.tmp-<nonce>` O_EXCL mode 0600 and `os.replace`s it to `pending/<nonce>`; nonce = `secrets.token_hex(16)` (32 hex). The inode of the record is read for the release text (:1764-1767). OSError -> `failed` `W-LAUNCH-FAILED` "could not write the launch record" (:1768-1775).
7. Agent launch argv (:1776-1779): `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. No `--model`, no `--effort`, no link flag. A not-ok reply removes the pending record (`pending.unlink`, :1783) and returns `failed` `W-LAUNCH-FAILED` with a `hand_command` (`shlex.join` of the argv without the marker, :1790-1793); a timed-out launch says "an agent may have started, check Orca before re-running" (:1784-1785).
8. Shim check (:1802-1811): `find_handle` (:1526-1541) walks the reply for the first `handle`; `behind_ccsession(handle)` (:1564-1583) tries up to 5 times (sleep 2.0 s between, `SC_ORCA_SHIM_INTERVAL`) `orca terminal read --terminal <h> --screen --json` and looks for `[ccsession]` or `Session name (Enter or Ctrl+C`, else `orca terminal show --terminal <h> --json` (`ccsession_title` :1551-1561) and the title regex `sc-launch-v1-<hex>-<MMDD>-<HHMMSS>-<hex4>`. No handle or no marker -> note `W-LAUNCH-NOT-CCSESSION` ("the agent's screen showed no ccsession text", or "the launch result named no terminal"). The launch still counts as `launched`.
9. `record_launch` (:1814, writes `launch` into `<D>/worktree.json` and the mirror); write failures do not fail the launch but add text "the agent is running but its launch was not fully recorded ... do not re-run the claim" (:1815-1821, :1832-1833).
10. `session_report` (:1445-1485): `release` text (a person runs `rm` on `<store>/sessions/<session id>` and `<session id>.ok`; `ls -i` inode hint) and `layers` = [`L1 guard: effective (the IR-4 preflight passed)`, `L2 pre-push: owned (...)` or `L2 pre-push: <state> (<reason>; the limits are enforced by the L1 guard only)`].
11. Result `status: launched`; `warning` = first note code (the ccsession note stays first, then `W-L2-ABSENT`) (:1823-1831; `launch_result` :1646-1663 puts the rest in `detail` as "also <code>: ...").

Closed launch vocabulary: statuses `launched | already_launched | failed`; warnings `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `W-L2-ABSENT` (`REMEDY` :802-817); `enforcement_hook` `installed | missing | null`.

`W-LAUNCH-NOT-CCSESSION` (requested): a warning, not a refusal. Emitted only at :1804-1810 when the agent was launched but neither the screen markers nor the title regex was seen. It means "this agent is NOT behind the ccsession shim, or could not be verified; close it" (REMEDY :804-807). The claim `status` stays `success`. It does not kill or close the agent.

`pending` subcommand (`cmd_pending` :1515-1523): `orca_worktree.py pending --level worktree|full|full-submit` calls `publish_pending` and prints `{"ok": true, "nonce": "<32 hex>", "level": ...}` or `{"ok": false, "detail": ...}`; exit 0. Intended for a coordinator that starts a worker itself (docstring :7-9; "(G2)" in the docstring of `cmd_pending` :1516). Choices differ from `prompt`/`launch`: `pending` accepts `full-submit` (:1891), `prompt`/`launch` accept only `worktree|full` (:1873, :1883) and take `--submit` separately.

Callers of `pending` / `cmd_pending` (Grep of the whole snapshot, patterns `orca_worktree\.py[" ]+pending`, `cmd_pending`, `publish_pending`, `pending --level`): in `src/` only the definition and argparse registration inside orca_worktree.py itself (:8, :1488, :1515, :1518, :1893). No command, skill, ref, template, hook, CLI module or agent in `src/` invokes the `pending` subcommand. The only external invocation is a test: tests/hooks/test_launch_level_guard_worker.py:287 (`[sys.executable, str(SCRIPT), "pending", "--level", "worktree"]`, SCRIPT imported from tests/skills/test_issue_orca_worktree.py:281). The only prose naming it as the coordinator's way to bind a worker is docs/designs/issue-pipeline-guard-g2.md:18 ("The coordinator creates the `pending` record through the `pending` subcommand Task 15 adds"). RESULT: no production caller found in the snapshot. [CODE-VERIFIED by grep; listed under Defect Candidates.]

### 8.8 How a chosen level becomes launch-level files (verified end to end)
1. The orchestrator resolves `<L>` in Wave 5 (prose rule, refs/claim.md:81) and passes `--level <L>` (and `--submit`) to `prompt` and `launch`. `none` never reaches the script (only `preflight` runs for `none`).
2. `launch` writes ONE file: `$HOME/.claude/state/launch-level/pending/<nonce>` containing one word: `worktree`, `full`, or `full-submit` when `--submit` (orca_worktree.py:1759-1761; `publish_pending` :1488-1512; modes 0700/0600).
3. The agent's first prompt carries `[sc-launch:v1:<nonce>]` (:1779).
4. The L1 guard `SRC/hooks/scripts/launch-level-guard.sh`, on that agent's first UserPromptSubmit, matches `\[sc-launch:v1:([0-9a-f]{32})\]` (:318), renames `pending/<nonce>` to `sessions/.take-<session id>` (:372-374), and hard-links it as `sessions/<session id>` (:299-305; `ln` at :305); a bad word is treated as `worktree` with a state note (:268). Level letters: `worktree`->W, `full`->F, `full-submit`->FS (:265-267); `sessions/<sid>.ok` present at level W gives WA = approved (:270-272). The `.ok` file is created when, at level W, the prompt's first line matches `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` (:347-359). So the `sessions/` folder files and `.ok` files are written by the GUARD, not by orca_worktree.py. [CODE-VERIFIED in the guard; the full guard is research file 05.]
5. The shim `ccsession-orca` does not carry the level. The only thing the claim does about the shim is DETECT it afterwards (`behind_ccsession`, :1564-1583) and warn. [CODE-VERIFIED: no other reference to a level in the shim detection code; the shim sources themselves are not in this file's scope.]
6. The `~/.claude/state/launch-level/{requests,jobs}` sub-stores named elsewhere are not touched by orca_worktree.py: Grep of the file for `requests` and `jobs` finds no such path (the only parts are `PENDING_PARTS` :791 and the `sessions` string in `session_report` :1454,1471). [UNVERIFIED here beyond that; owned by research 05.]

### 8.9 CLI and argument rules (:1837-1902)
- `issue_number` positive integer; `repo_name` regex `owner/repo`; `origin_ref` regex `origin/[A-Za-z0-9._/-]+` (:1837-1854). `build_parser` :1857-1894 defines `preflight`, `worktree --repo --number --base --source`, `prompt --template --level worktree|full [--submit] --number --repo [--source] --out`, `launch --number --source --level worktree|full [--submit]`, `pending --level worktree|full|full-submit`.
- `main` :1897-1902: `--submit` with `prompt` or `launch` and `--level != full` -> `parser.error("--submit needs --level full")` (exit 2).

### 8.10 Status of each piece (BUILT-ON / BUILT-OFF / NOT BUILT / REMOVED)
- preflight, worktree create/reuse, prompt render, launch, IR-4 preflight, L2 install/status, shim detection, `record_launch`: BUILT-ON (code paths unconditional in `cmd_launch`; no config flag gates them). 
- IR-7 refusal of a launch when L2 is not owned: BUILT-OFF: code at :1757-1758 and :829-831 is unreachable while `IR7_REFUSE = False` (:822).
- `pending` subcommand: BUILT-ON as a CLI verb (:1893) but with NO PRODUCTION CALLER (see 8.7).
- IR-3 `pipeline.json` (design): NOT BUILT (Grep `pipeline\.json` over `src/` returns no match).
- Default-level pick (Wave 5): BUILT as prose only (no code); see section 4 and Grep result below.
- The ship gate "OB-H1 item 1, OB-H2, OB-H3": prose only, no code check (no reference in orca_worktree.py).

Key Takeaways
- `orca_worktree.py` is the only code that calls `orca` for the claim; the only argv it builds for creation and launch are the two listed in 8.2 and 8.7.
- The launch order is "refuse early, write the record last": already-launched, stale prompt, IR-4, L2 install, pending record, agent launch.
- Worktree creation is done by Orca; this file never commits, pushes, stages or removes (docstring :32-34). It creates `issue-<N>` with no agent, copies `.dev/issues/<N>/` in, closes the plain tab.
- Closed warning vocabulary: worktree step 8 codes (:230-239); launch step 4 codes (`REMEDY` :802-817). `W-LAUNCH-NOT-CCSESSION` is emitted in `cmd_launch` (checked in 8.7).
- `IR7_REFUSE = False` at :822: a missing L2 hook never blocks a launch.

## 9. STOP and warning codes (closed vocabularies)

### 9a. STOP codes (all executed by the model reading the prose; no code raises them except the exit-code mapping of origin_repo.py)
| Code | Condition | Source |
|---|---|---|
| (no code) both/neither of --claim/--create; bad depth/mode/type/pipeline value; empty description; empty claim argument | usage STOP before Activation | issue.md:52,54-56,58 |
| `E-CREATE-ONLY-FLAG` | `--depth/--mode/--type` with `--claim` | issue.md:53 |
| `E-CLAIM-ONLY-FLAG` | `--pipeline/--submit` with `--create` | issue.md:57 |
| `E-SUBMIT-NEEDS-FULL` | `--submit` with a value, without `--pipeline full`, or with no `--pipeline` | issue.md:59 |
| `E-NO-ORIGIN` | no `origin`, git failed, or origin not GitHub; origin_repo.py exit 1 | origin_repo.py:47,167-173; claim.md:15 |
| `E-FOREIGN-REPO` | claim URL names another repo or non-GitHub host; exit 3 | origin_repo.py:49,114-119,135-140 |
| `E-NOT-AN-ISSUE` | `/pull/<N>` URL, not a number or issue URL (exit 4), or `scout.md` says `is_pull_request` | origin_repo.py:50,147-153; claim.md:40 |
| `E-GH-AUTH` | `gh auth status` fails | claim.md:16 |
| `E-ORCA-REQUIRED` | `orca_worktree.py preflight` prints `ok:false` (even for `none`); before any GitHub or ClickUp write | claim.md:17; SKILL.md:84,160 |
| `E-WORKER-NO-OUTPUT` | worker file missing/empty after one retry | SKILL.md:66,168 |
| `E-TIER-UNAVAILABLE` | t3 or t2 spawn not served, or the T2 fallback not served; no alias fallback | tiers.md:44-52; SKILL.md:167 |
| (no code) closed issue "Issue #N is closed; not claimed."; assigned to another login "Issue #N is assigned to @<login>; not claimed." | no writes | claim.md:41-42; SKILL.md:163-164 |
| `E-ASSIGN-FAILED` | `gh issue edit ... --add-assignee @me` fails; before ClickUp and any comment | claim.md:48; SKILL.md:169 |
| `E-POST-FAILED` | comment post or PATCH fails; files stay, re-run edits by marker | claim.md:93; SKILL.md:172 |
| `E-CREATE-FAILED` | (create path) `gh issue create` fails; draft kept | create.md:92; SKILL.md:173 |
Exit code 2: `clickup_claim.py` bad arguments (the claim STOPs, keeps the GitHub assignment, claim.md:51); `orca_worktree.py` argparse errors incl. `--submit needs --level full` (:1900-1901). Exit codes 1/3/4: origin_repo.py. No exit code is defined for the rest; every `orca_worktree.py` runtime outcome exits 0 (:11-12).

### 9b. Warning codes (never STOP; claim `status` stays `success`)
- Worktree (Wave 7), 8 codes: `W-ORCA-LIST-FAILED`, `W-ORIGIN-BASE-MISSING`, `W-WORKTREE-CREATE-FAILED`, `W-WORKTREE-AMBIGUOUS`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`, `W-ORIGIN-BASE-STALE`, `W-FIRST-TAB-LEFT` (orca_worktree.py:230-239; remedy lines refs/claim.md:106-115; SKILL.md:161). Trigger lines are in 8.2.
- Launch (Wave 8), 4 codes: `W-LAUNCH-FAILED`, `W-LAUNCH-NOT-CCSESSION`, `W-ENFORCEMENT-ABSENT`, `W-L2-ABSENT` (orca_worktree.py:802-817; refs/claim.md:127-132; SKILL.md:162). Triggers: `W-LAUNCH-FAILED` at :1702, :1724, :1772, :1797, `W-ENFORCEMENT-ABSENT` at :1737, `W-LAUNCH-NOT-CCSESSION` at :1806, `W-L2-ABSENT` at :1756. Ordering when both ccsession and L2 apply: ccsession first (`warning`), `also W-L2-ABSENT: ...` in `detail` (refs/claim.md:134; :1825).
- `W-LAUNCH-NOT-CCSESSION`: see 8.7. A launched agent that is not behind the shim is NOT stopped by the claim; the remedy line tells the person to close it.
- Output carries the warning as `worktree_warning` / `launch_warning` in the return contract (SKILL.md:130,132).

## 10. `--pipeline` levels in code and prose

| Level | Where defined | In code (orca_worktree.py) | What it does |
|---|---|---|---|
| `worktree` | issue.md:43; launch-prompt.md:20-23 | `--level worktree` (:1873,:1883); pending word `worktree` | Orca worktree + agent; agent runs `next-steps.md` up to `Plan boundary`, prints plan path and `Waiting for approval`; a human approves by running `/sc:implement`/`/task` first-line prompt in that session; then rest, still no commit/push/`/sc:pr-submit` |
| `full` | issue.md:43; launch-prompt.md:25-26 | `--level full`; word `full` | Worktree + agent; every step, no commit, no push, no PR, stage nothing, prints `git status --short` |
| `full --submit` | issue.md:44; launch-prompt.md:28-34 | `--submit` flag with `--level full`; word `full-submit` (:1759); `prompt` adds the `submit` block | Adds checks for an existing PR, conventional commit (stage `.dev/tasks` and changed files, never `.claude/`, never `.dev/issues/`), `git push origin <branch>`, `/sc:pr-submit --monitor 3 ...`; never merge |
| `none` | issue.md:43,83; claim.md:94 | Not a value of `--level` in the script; the script is only called for `preflight` | No worktree, no agent; the claim ends after the two comments; a person (or a coordinator with `worktree` + `worker-start`) runs `next-steps.md` |
| (omitted) | issue.md:43,48; claim.md:81 | No code | Orchestrator picks: unreadable type/complexity/hours -> `worktree`; bug -> `full`; simple/medium feature of <= 16 h -> `full`; complex feature or > 16 h -> `worktree`; explicit value always wins |

- The default-level rule is PROSE ONLY. Grep of the snapshot `src/` for the reason strings (`default: bug`, `simple or medium feature of 16 hours or less`, etc.) matches only commands/issue.md, core/HOW-WE-WORK.md and refs/claim.md; no `.py`, `.sh` or `.json` contains it. [CODE-VERIFIED] It is pinned only by text assertions: tests/skills/test_issue_protocol.py:774 (`test_default_level_is_full_and_only_worktree_waits_for_a_person`) and :791 (`test_default_level_rule_is_bug_full_complex_feature_worktree`), and tests/commands/test_issue_command.py:182.
- The level reaches the launch-level store only through the `launch` subcommand (8.8).
- Prompt vs guard mismatch: launch-prompt.md:23 tells the agent that approval at level `worktree` is a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`; the guard regex that creates the `.ok` approval file is `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` (launch-level-guard.sh:347) and Grep of the guard for `sc:task` returns no match, so a first line `/sc:task ...` would NOT release the session. [CODE-CONTRADICTED between launch-prompt.md:23 and launch-level-guard.sh:347.]

## 11. State stores (every file or directory written or read)

| Path pattern | Writer | Readers | Format / mode |
|---|---|---|---|
| `.dev/issues/<N>/scout.md` | T3 worker (Write tool) | orchestrator; T1/T2 | markdown from scout-report.md |
| `.dev/issues/<N>/clickup.json` | `clickup_claim.py` stdout, redirected by the orchestrator | orchestrator (claim comment) | one JSON object (section 6b) |
| `.dev/issues/<N>/accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md` | T2 or T1 worker | orchestrator (posted comment body; level rule reads summary) | markdown templates |
| `.dev/issues/<N>/recommend.md`, `next-steps.md`, `claim-comment.md` | orchestrator | launched agent; coordinator | markdown |
| `.dev/issues/<N>/launch-prompt.md` | `orca_worktree.py prompt` (atomic_write_text, 0644) | launched agent; `stale_prompt` compares copies | markdown assembled from 3-4 blocks |
| `.dev/issues/<N>/worktree.json` (origin checkout, never copied into worktree) | `write_record` (:507) and `record_launch` (:1619) via atomic_write_text 0644 | `cmd_worktree` reuse (record key), `cmd_launch`, `cmd_prompt` | `{"path","status","launch":{"level","submit","at"}}` |
| `<wt>/.dev/issues/<N>/*` | `copy_issue_dir` (file by file, no symlink writes, `.prev` backups) | launched agent | copy of the above except worktree.json |
| `<wt git dir>/sc-issue-launch-<N>.json` | `record_launch` (:1634-1642) | `read_mirror` (:1600) | `{"path","launch"}` mirror; untracked by construction |
| `$HOME/.claude/state/launch-level/pending/<nonce>` | `publish_pending` (via `launch` or `pending`) | launch-level-guard.sh (consumes by rename) | one word `worktree|full|full-submit`; file 0600, dirs 0700 |
| `$HOME/.claude/state/launch-level/sessions/<session id>`, `.take-<sid>`, `<sid>.ok` | the L1 guard hook (launch-level-guard.sh:289-313, :358, :372-376), NOT the claim | guard; a person removes them with `rm` per the `release` text | level word / empty approval file |
| `<git-common-dir>/hooks/pre-push` and `pre-push.launch-level` | `install_l2` (hard link, 0755) and `publish_no_replace` (0644) | git (hook); `l2_status` | packaged hook copy; data file `HOME\nuv_dir\n` |
| Reads only: `~/.claude/settings.json`, `<wt>/.claude/settings.json`, `settings.local.json`, `~/.claude/hooks/launch-level-guard.sh`, `launch-job-identity.sh`, `launch-level-pre-push.sh` | - | IR-4 preflight, `_l2_packaged` | JSON / shell |
| Orca-side state (worktree row with comment `sc:issue <R>#<N>`) | Orca (`orca worktree create`) | `list_rows`/`lookup` | owned by Orca |

Never written by the claim: `.dev/issues/<N>/pipeline.json` (no code, Grep empty); any staged/committed `.dev/issues/` (issue.md:100); labels/type/fields on a claim; source files; ClickUp comments/status; `sessions/`, `requests/` or `jobs/` entries (no such path in orca_worktree.py: Grep `requests|jobs` returns nothing); worktree.json for `--pipeline none` (issue.md:80; claim.md:94). For `--pipeline none` the claim leaves files only in the origin checkout's `.dev/issues/<N>/`.

## 12. Gates (approval, refusal, kill switch, cap, budget, guard)

| Gate | Condition | Word / exit | Evidence |
|---|---|---|---|
| Orca-down gate | `orca status --json` not ok/reachable | STOP `E-ORCA-REQUIRED`; before any write | orca_worktree.py:210-223; claim.md:17,21 |
| Fork-safety / origin gate | repo from `origin` only; foreign repo STOP | `E-FOREIGN-REPO` exit 3 | origin_repo.py:135-140 |
| Idempotence | earlier markered comments edited, not duplicated; already assigned continues | (none) | claim.md:44,88-93 |
| Assign gate | assignee failure stops before ClickUp and comments | `E-ASSIGN-FAILED` | claim.md:48 |
| Posting gate | no approval prompt (B1); failed post stops | `E-POST-FAILED` | SKILL.md:76; claim.md:93 |
| `--submit` gate | needs explicit `--pipeline full` | `E-SUBMIT-NEEDS-FULL`; script exit 2 | issue.md:59; orca_worktree.py:1900-1901 |
| Worktree reuse/ambiguity | >1 live match, stale match, list unusable, base missing | warnings (8.2) | orca_worktree.py:655-662,672-677 |
| Already-launched gate | `launch` entry in worktree.json or mirror | `already_launched`, no Orca call | :1704-1721 |
| Stale-prompt gate | worktree prompt differs from rendered prompt | `failed` `W-LAUNCH-FAILED`, no agent | :1722-1724 |
| IR-4 enforcement preflight | any of the conditions in 8.5 | `W-ENFORCEMENT-ABSENT`, no agent, no record | :1730-1747 |
| IR-7 L2 refusal | L2 not owned AND `IR7_REFUSE` True | would be `failed` with `W-L2-ABSENT`; today `IR7_REFUSE = False` so never refuses | :822, :1757-1758 |
| Plan-approval gate (level `worktree`) | human first-line `/sc:implement` or `/task` (guard regex) | `.ok` file | launch-level-guard.sh:347-359 (research 05) |
| Ship gate (OB-H1 item 1, OB-H2, OB-H3) | prose: no governed claim on a real issue until observations pass | none | issue.md:16; claim.md:136; no code reference: Grep `OB-H1|OB-H2|OB-H3` in `src/superclaude` `*.py *.sh *.json` returns 0 |
| Per-command caps | subprocess timeouts 120/30/15 s, `SC_ORCA_TIMEOUT`; shim tries 5 x 2 s; L2 selftest 30 s; packaged hook <= 64 KiB | - | :88-91, :798-800, :1078, :1178 |
| ClickUp caps | `CLICKUP_MAX_PAGES` default 20; 429 retried once | `error` `page_cap` / `rate_limited` | clickup_claim.py:74,88-94,119-123,203-206 |
| Worker caps | one retry of an empty worker; one T1->T2 fallback | `E-WORKER-NO-OUTPUT`, `E-TIER-UNAVAILABLE` | SKILL.md:64,66 |
| Budget / kill switch / `enabled` flag | none found in this area | - | no `enabled`, budget or switch in the claim scripts (Grep of the three scripts shows none beyond IR7_REFUSE) |

## 13. Triggers (what starts this piece)

- Human typing: "Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...`" (issue.md:25). Frequency: on demand. No scheduler in this area.
- Issue watcher launch prompt: `build_claim_prompt(n)` returns `/sc:issue --claim <n> --pipeline none` (SRC/cli/issue_watch/launch.py:84-92; `PROMPT_PATTERN` :33) and `ORIGIN_REPO = "ironbellyorg/ironclaude"` is the only origin its `check_origin` accepts (:50-51). The watcher is covered by research files 01-03; here only the claim-side contract matters: issue.md:48 says the watcher always passes `none`.
- Coordinator handoff after a `none` claim: prose at issue.md:85, SKILL.md:140, claim.md:96 (runs `orca_worktree.py worktree`, then `worker-start`). No code in `src/` calls `orca_worktree.py worktree` on behalf of a coordinator: Grep `orca_worktree` in `src/` finds only issue.md, require-orca-worktree-agent.sh (a comment at :60), refs/claim.md, orca_worktree.py, SKILL.md and launch-prompt.md. [CODE-VERIFIED: the coordinator handoff is prose, not code.]
- `orca_worktree.py pending`: no trigger found in snapshot `src/` (see 8.7).

## 14. Test-pin table (deliverable a)

Paths under `/home/coder/.cache/ic-snap-20261120/master/tests/`. Lines = `wc -l`; Test count = count of `def test_` lines (a parametrized function counts once). Classes counted with `^class `.

| Path | Lines | Test count | What it pins | Key test names |
|---|---|---|---|---|
| skills/test_issue_protocol.py | 1055 | 62 (0 classes) | SKILL.md frontmatter/size; two-way file inventory (every named path exists and every file is named); spawn rule text; Wave 0/5/7/8 ordering (preflight in Wave 0, worktree after the posts, prompt before Wave 7); launch-prompt has exactly four blocks and PR tokens only in the submit block; every worktree warning code listed with a remedy line; no forbidden Orca flag in script or md; plan-boundary rule; `none` creates no worktree; return contract has the ten claim fields; default-level rule text; posted templates end with their marker; create-mode template headings and required plan sections; chain flags exist in their commands; fork safety (`--repo` on every `gh issue/pr/label` mention; no brace placeholder); the single allowed `orgs/` read; Complexity field POST-only, read-back by field id; coordinator handoff paragraph identical in three files | `test_every_named_path_exists_and_every_file_is_named` :147, `test_st6_preflight_is_in_wave_0_and_worktree_is_wave_7_after_the_posts` :251, `test_every_worktree_warning_code_is_listed_with_a_remedy_line` :350, `test_st4_script_has_no_forbidden_orca_flag_and_launch_flags_only_in_launch` :387, `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` :560, `test_default_level_rule_is_bug_full_complex_feature_worktree` :791, `test_every_gh_issue_pr_label_mention_carries_repo` :833, `test_the_coordinator_handoff_is_the_same_paragraph_in_all_three_files` :1029, `test_the_claim_still_writes_no_worktree_record_for_pipeline_none` :1054 |
| skills/test_issue_orca_worktree.py | 2501 | 109 (1 class) | `orca_worktree.py` against a fake `orca` on PATH and a temp HOME (no real orca/gh/network): preflight PF1-PF2 + timeout; lookup keys marker/record/basename/branch (FO2-FO4, FO13); ambiguity, stale, archived rows; create argv exact and no forbidden flag (FO18 :837); copy rules `.prev`, tracked files, symlinks (FO14-FO16, PR425); first-tab close FT1-FT12; prompt rendering PR1-PR16; launch argv exact (LA1 :1328), record privacy and nonce freshness (LA2), failure removes record (LA3), already-launched (LA4), shim detection by screen or title with 5 tries (LA5), IR-4 refusal (LA6, `test_ir4_*`), IR-6 release and layers, IR-7 warns and launch proceeds (:1838); PR 425 review-round regressions; `pending` subcommand (:2472-2496) | `test_la1_launch_argument_list_is_exact`, `test_fo18_exact_commands_and_no_forbidden_flag`, `test_la6_launch_without_an_executable_hook_is_refused`, `test_ir7_l2_absent_warns_and_the_launch_proceeds`, `test_ir4_each_failing_condition_refuses_the_launch`, `test_la5_launch_shim_check_failure_keeps_the_launch_and_warns`, `test_pending_writes_one_private_record_and_prints_its_nonce`, `test_pending_refuses_a_level_outside_the_guard_words`, `test_ir4_pipeline_none_never_reaches_the_preflight` |
| skills/test_issue_repo_resolution.py | 291 | 18 (0) | `origin_repo.py`: origin URL forms to owner/repo; non-GitHub origin and missing origin exit 1 `E-NO-ORIGIN`; only `origin` is read when another remote exists; claim arg to number; foreign URL exit 3; `/pull/` URL exit 4; digits in owner/repo never become N; bad args exit 2; stdlib only | `test_only_origin_is_read_when_another_remote_exists`, `test_claim_url_on_another_repo_is_e_foreign_repo`, `test_pull_url_on_origin_is_rejected_not_parsed`, `test_digits_in_owner_or_repo_never_become_n`, `test_script_imports_only_standard_library` |
| skills/test_issue_worker_agents.py | 559 | 24 (0) | three agent files: `model:` = `claude-gw-tier2b` (t3), `claude-gw-tier2` (t2), `claude-gw-tier1b` (t1), no `[1m]`; t3 `effort: low`; each tier key (`tier2b`,`tier2`,`tier1b`) exists in ccsession-models.json; tools exactly `Read, Grep, Glob, Write, Bash` (no Edit); no `permissionMode`; GitHub-read-only and write-only-under-`.dev/issues/` rules; `gh_lines_missing_repo` fork-safety helper; files-are-tool-inputs rule; harness-blocked file names; required-plan-section rule | `test_worker_file_exists_with_pinned_picker_id` :77, `test_t3_effort_is_low` :85, `test_picker_tier_exists_in_ccsession_models` :96, `test_tools_exclude_edit` :102, `test_worker_states_required_plan_sections_rule` :535 |
| skills/test_issue_t1_fallback.py | 69 | 8 (0) | T1 -> T2 fallback text in SKILL/tiers/claim/templates; STOP when fallback not served; no alias fallback; no fallback for T3/T2; optional fallback line in accuracy template; next-steps line offers tier2; no `tier1a` left | `test_doc_states_the_t1_to_t2_fallback`, `test_doc_keeps_no_alias_fallback`, `test_tiers_says_no_fallback_for_t3_or_t2`, `test_no_tier1a_left_in_the_issue_workers_or_skill` |
| skills/test_issue_l2_install.py | 716 | 26 (1 class) | `install_l2` / `l2_status` on real git under temp HOME with copies of the packaged hook: fresh install under umask 077, repeat install, forgery/wrong uid/wrong mode never owned, data-file conflicts, `core.hooksPath` unsupported, unsafe hooks dir, git failure, packaged hook not installed, self-test failure links nothing, concurrent installs converge, foreign entry survives, `l2_status` never writes, IR-7 switch behaviour and shipped value | `test_ir7_l2_switch` :594, `test_ir7_shipped_switch_is_off` :639 (asserts `IR7_REFUSE is False`), `test_hookspath_is_unsupported` :312, `test_selftest_failure_links_nothing` :436, `test_l2_status_never_writes` :575 |
| commands/test_issue_command.py | 212 | 15 (0) | static pins of `commands/issue.md`: frontmatter, version `1.1.0`, exactly seven flags in the options table, allowed values and defaults, no repo/dry-run/preview flag, STOP rules before Activation, `E-SUBMIT-NEEDS-FULL`, Will Not text, outputs/examples, default level text and watcher explicit, activation names the skill, no `src/superclaude` path, rule-10 line verbatim | `test_st3_version_is_1_1_0` :80, `test_st1_options_table_lists_exactly_the_seven_flags` :84, `test_default_level_is_for_a_person_and_the_watcher_stays_explicit` :182, `test_submit_rule_stops_a_bare_submit_and_keeps_its_message` :191 |
| cli/test_issue_body_templates.py | 97 | 5 (0) | NOT a claim test: ISSUE-HANDOFF/ISSUE-BACKLOG body files shipped flat, exactly four headings, no execution key or ClickUp text; CLAUDE.md has exactly one issue rule line; `/sc:issue` command and skill are the only issue primitives | `test_body_files_shipped_and_installed_flat`, `test_claude_md_has_exactly_one_issue_rule_line`, `test_issue_command_and_skill_are_the_only_issue_primitives` |

Related test (not in the assignment, found while tracing): tests/hooks/test_launch_level_guard_worker.py:273 `test_a_prompt_with_a_pending_nonce_binds_the_worker_and_one_without_does_not` runs `orca_worktree.py pending --level worktree` (:287) and is the only caller of that subcommand in the snapshot. No test computes the default level or the OB-H gates; they are text pins (test_issue_protocol.py:774,:791).

## 15. Design documents: doc-vs-code verification (deliverable: staleness)

| Doc | Claim | Tag | Evidence |
|---|---|---|---|
| docs/designs/sc-issue-command.md:3 | "Status: Design only (nothing implemented)" | [CODE-CONTRADICTED] | command, skill, scripts, agents, templates all exist (sections 1-8) and have tests (section 14) |
| sc-issue-command.md:58,107,129,391,423,449 (D3) | T3 pinned to `claude-gw-tier3` | [CODE-CONTRADICTED] | agents/issue-worker-t3.md:6 `model: claude-gw-tier2b`; refs/tiers.md:17; tests/skills/test_issue_worker_agents.py:22-23 |
| sc-issue-command.md:154-158 | Wave 0 has no Orca check; no `--limit 200` | [CODE-CONTRADICTED] (self-amended at :150) | refs/claim.md:17 (Orca check), :28 (`--limit 200`) |
| docs/designs/sc-issue-claim-pipeline-flag.md:3 | Implemented (PR #425), amended by #394 | [CODE-VERIFIED] for the code it names (preflight, worktree, prompt, launch, IR-4, W-L2-ABSENT); PR number [UNVERIFIED] (no git history in the snapshot) | orca_worktree.py |
| pipeline-flag.md:21 | level table row "`worktree` (default)" | [CODE-CONTRADICTED] at its head; the same cell is amended twice (2026-11-18) to "picked from the issue" | refs/claim.md:81; issue.md:43. Same stale head text at :43 (P2 "default `worktree`") and :66 |
| pipeline-flag.md:58 | `pipeline.json` not built | [CODE-VERIFIED] | Grep `pipeline\.json` in `src/` no match |
| pipeline-flag.md:59 | "the claim installs the L2 `pre-push` hook in the new worktree" | [CODE-CONTRADICTED] (loose) | hook is installed in `<git-common-dir>/hooks/pre-push`, shared by every worktree of the clone: orca_worktree.py:1365,1402 |
| pipeline-flag.md:60 | `W-ENFORCEMENT-ABSENT` refuses, `W-L2-ABSENT` warns | [CODE-VERIFIED] | orca_worktree.py:1730-1758 |
| pipeline-flag.md:291 | `W-L2-ABSENT` is "A warning while `IR7_REFUSE` is `False`" | [CODE-VERIFIED] | :822,:1757 |
| refs/claim.md:125 | "installs ... as the worktree's `pre-push` hook" | [CODE-CONTRADICTED] (loose, see above) | :1365,:1402 |
| refs/claim.md:125 | "Before anything else the script runs the IR-4 preflight" | [CODE-CONTRADICTED] | record check :1700, already-launched :1704-1721 and stale-prompt :1722-1724 run first |
| refs/claim.md:125 | read-only check at `git rev-parse --git-path hooks/pre-push` | [CODE-CONTRADICTED] (minor) | code asks `--git-path hooks` (:1356-1359) so a symlinked `pre-push` reaches the entry check |
| SKILL.md:35 | script used in Waves 0, 5, 7, 8 | [CODE-VERIFIED] but incomplete: `pending` subcommand not listed | orca_worktree.py:1886-1893 |
| refs/tiers.md:32,44 | duplicate heading `E-TIER-UNAVAILABLE (default D4)`, first one empty | [STALE DOC] formatting | tiers.md:32 and :44 |
| templates/launch-prompt.md:23 | approval prompt may start `/sc:task` | [CODE-CONTRADICTED] | launch-level-guard.sh:347 regex has only `sc:implement` and `task`; no `sc:task` in the guard |
| Task brief: templates folder has 17 files | | [CODE-CONTRADICTED] | Glob returns 15 files (section 7) |
| refs/tiers.md:23-26, :36 | Claude Code resolves model in a stated order; proxy answers 400 `ccsession tier1b:` | [UNVERIFIED] | external behaviour; not in the snapshot code |
| issue.md:85 / SKILL.md:140 / claim.md:96 | coordinator adoption row `reserved`, `worker-list`, `worker-start` | [UNVERIFIED] in this area | the coordinator text is in core/WORKER-CONTRACT.md (research 06); no code in the claim scripts or in `cli/issue_watch` implements an adoption row (Grep matched `adoption|worker-start` in md files and in unrelated `cli/recommend`, `cli/swarm` modules, which were not read) |
| issue.md:16, claim.md:136 (OB-H1/2/3 ship gate passed?) | | [UNVERIFIED] | no observation record in the snapshot code; no code reads the gate |

## 16. Live-vs-off status (deliverable b), one line per piece

| Piece | Status | Evidence |
|---|---|---|
| `/sc:issue` command front (issue.md) | BUILT-ON | file exists, version 1.1.0 (issue.md:3), Activation at :104-110; trigger is a human typing it |
| Skill orchestrator protocol (SKILL.md, refs) | BUILT-ON | files exist; executed by the model; no switch |
| `origin_repo.py` | BUILT-ON | Wave 0 step 1 (claim.md:14); exit codes 1/3/4 |
| `clickup_claim.py` | BUILT-ON but conditional on env (`CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID`, else `skipped`) | clickup_claim.py:164-169 |
| Worker agents t1/t2/t3 | BUILT-ON (pins tier1b / tier2 / tier2b) | agents/*.md:6; test_issue_worker_agents.py:22-26 |
| T1 -> T2 fallback | BUILT-ON (prose rule) | tiers.md:34-42 |
| `orca_worktree.py preflight/worktree/prompt/launch` | BUILT-ON | no gating flag; `build_parser` :1857-1894 |
| IR-4 enforcement preflight (refuses launch) | BUILT-ON | `cmd_launch` :1730-1747 |
| L2 pre-push install and status | BUILT-ON (installed on every launch; result advisory) | :1754-1756 |
| IR-7 refusal when L2 not owned | BUILT-OFF (constant, not `enabled:false`): `IR7_REFUSE = False` | :822, :1757; decision text "owner decision 2026-11-08" at :822 and :819-821 "owner decision OD-3"; pinned off by test_issue_l2_install.py:639 |
| `W-LAUNCH-NOT-CCSESSION` detection | BUILT-ON (warning only) | :1803-1811 |
| `orca_worktree.py pending` subcommand | BUILT-ON as verb; NO production caller in `src/` | 8.7 Grep results; only test caller tests/hooks/test_launch_level_guard_worker.py:287 |
| Default `--pipeline` pick | BUILT as prose only (no code, executed by the model) | claim.md:81; Grep finds no code |
| IR-3 `pipeline.json` | NOT BUILT (documented as not built) | pipeline-flag.md:58; Grep empty |
| Coordinator handoff for `--pipeline none` | prose only in this area; code not found in snapshot | issue.md:85; 15 above |
| Watcher passes `--pipeline none` | BUILT-ON in `cli/issue_watch/launch.py:92` (watcher research 02 owns the rest) | launch.py:33,84-92 |
| OB-H1/OB-H2/OB-H3 ship gate | NOT BUILT as a mechanism (prose gate) | issue.md:16; Grep 0 hits in `src/superclaude` `*.py *.sh *.json` |
| `--create` mode | BUILT-ON | refs/create.md, labels.md, create templates; `gh issue create` path 5c |
| `/sc:issue` removed pieces | no REMOVED piece found in this area; the removed `issue-pipeline` package belongs to research 06 | - |

## 17. Integration and extension notes (how a developer extends this)
- Add a pipeline level: change the `--pipeline` option rows and STOP rules in issue.md (:43,:58), the level rule at claim.md:81, a new block in templates/launch-prompt.md (the block name is matched by `BLOCK_MARKER` regex `[a-z]+`, orca_worktree.py:743) and the `choices` of `prompt` and `launch` (:1873,:1883) and `pending` (:1891); then the guard's word table (launch-level-guard.sh:264-269); tests: test_issue_protocol.py (4-block assertion :295), test_issue_command.py (options-table pin :84), test_issue_orca_worktree.py PR/LA tests.
- Add a worker tier: new `agents/issue-worker-tN.md` with `model:` picker ID, add to `WORKERS` dict in tests/skills/test_issue_worker_agents.py:21-26, SKILL.md :58-62 table, tiers.md :11-15 and the tier key in ccsession-models.json.
- Add a warning code: add to `REMEDY` (:802-817) or `WARNING_ORDER` (:230-239), add its remedy line to refs/claim.md tables (:106-115, :127-132) and the error table in SKILL.md (:161-162); `test_every_worktree_warning_code_is_listed_with_a_remedy_line` (:350) enforces the docs side.
- Add a template: file under templates/, add a row to the SKILL.md files table (:36-50); `test_every_named_path_exists_and_every_file_is_named` pins the two-way inventory.

Key Takeaways (sections 9-17)
- Closed vocabularies: 13 STOP codes plus unnamed usage/closed/assigned STOPs; 12 warning codes (8 worktree, 4 launch); exit codes 1/3/4 (origin_repo.py), 2 (argparse / bad clickup args), 0 for every other `orca_worktree.py` outcome.
- The only mechanical enforcement of a level is the L1 guard fed by `pending/<nonce>`; everything the claim does before that (level pick, STOP rules, ship gate, coordinator handoff) is prose run by the model.
- The only write the claim makes to GitHub is the assignee plus two marked comments; ClickUp gets one assignee add; `--create` adds an issue, a field POST and an optional comment.
- No kill switch, budget or `enabled` flag exists in the claim scripts; the single off-switch is the constant `IR7_REFUSE = False`.

## Gaps and Questions

All [UNVERIFIED] and [CODE-CONTRADICTED] claims plus open questions:
1. [UNVERIFIED] Orca CLI flags (`--surface terminal`, `agent launch`, `terminal close --tab`, `worktree create --no-parent --comment`) are valid in the installed Orca: no real `orca` was run; tests use a fake `orca` (tests/skills/test_issue_orca_worktree.py:1-6); reply shapes are assumptions in code (`find_handle` walks any `handle` key, :1526).
2. [UNVERIFIED] Tier pins resolve to the models named in tiers.md:17 ("GPT-6.1 Terra first"): the tier keys `tier1b`, `tier2`, `tier2b`, `tier3` exist in SRC/skills/ccsession-tag/ccsession-models.json (lines 85, 93, 104, 113 by Grep) but the model order was not read.
3. [UNVERIFIED] tiers.md:23-26 and :36 statements about Claude Code's model resolution order and the proxy's HTTP 400 `ccsession tier1b:` message: external behaviour.
4. [UNVERIFIED] Whether OB-H1 item 1, OB-H2 and OB-H3 have passed (issue.md:16; claim.md:136). No code reads the gate. Open question for the owner: is a claim at `worktree` or `full` currently permitted on a real issue?
5. [UNVERIFIED] Coordinator handoff for `--pipeline none` (adoption row `reserved`, `worker-list`, `worker-start`; issue.md:85): the contract text is in core/WORKER-CONTRACT.md (research 06); no code in this area implements it. Open question: what actually runs `orca_worktree.py worktree` for a coordinator?
6. [UNVERIFIED] Who or what calls `orca_worktree.py pending`: no production caller in `src/` (8.7). docs/designs/issue-pipeline-guard-g2.md:18 says a coordinator does through a "Task 15" subcommand; no evidence in the snapshot that any coordinator does.
7. [CODE-CONTRADICTED] launch-prompt.md:23 names `/sc:task` as a releasing first line; guard regex at launch-level-guard.sh:347 accepts only `/sc:implement` and `/task`. Open question: which side is intended?
8. [CODE-CONTRADICTED] items listed in "Stale Documentation Found" below (design status line, T3 pin, level table head text, L2 location wording, IR-4 "before anything else", git-path form, 17-file template count).
9. Not read: templates/scout-report.md and recommend-record.md bodies; the create-mode flag-decision, description, issue-body, draft-notes and create-review templates (create path was traced through refs/create.md and refs/labels.md only); `/sc:recommend` and `/sc:analyze` behaviour inside Wave 4/5; launch-level-guard.sh beyond lines 240-400 (research 05 owns it); docs/designs/sc-issue-launch-level-hook.md beyond grep hits.
10. Tests were read by name and selected bodies; none was run (no execution in this task), so "pins" means what the test asserts by reading, not a pass result.
11. Test counts are `grep` counts of `def test_`; parametrization expands real collected counts.
12. PR numbers (#425, #394, #441, #442) are cited by the docs; nothing in the snapshot can verify them.
13. Whether any scheduler or person invokes `/sc:issue --claim` on a cadence: the only automatic trigger found is the watcher prompt builder (launch.py:84-92), whose scheduling is covered by research 01-03.
14. Open question: `W-LAUNCH-NOT-CCSESSION` leaves an un-shimmed agent running (remedy "close it", REMEDY :804-807); there is no automatic close. Is that intended?
15. Open question: the IR-4 preflight verifies only the claim process's HOME/PATH/env and settings files (:1740-1742); an agent started with another environment may be ungoverned. This is documented in the warning text itself.

## Stale Documentation Found

- **[STALE DOC]** docs/designs/sc-issue-command.md:3 "Design only (nothing implemented)": the command, skill, scripts, agents and tests exist.
- **[STALE DOC]** sc-issue-command.md:58,107,129,391,423,449 pin T3 to `claude-gw-tier3`; agents/issue-worker-t3.md:6 pins `claude-gw-tier2b` (issue 488, tiers.md:17; test pin test_issue_worker_agents.py:22-23).
- **[STALE DOC]** sc-issue-command.md:154-158 Wave 0 has no Orca check and no `--limit 200` (self-amended at :150; code: claim.md:17,28).
- **[STALE DOC]** docs/designs/sc-issue-claim-pipeline-flag.md:21, :43 (P2) and :66 still lead with "default `worktree`" before stacked amendments; the real default is the prose pick at refs/claim.md:81 (`full` for a person-typed bug or small feature, `worktree` otherwise; watcher passes `none`).
- **[STALE DOC]** pipeline-flag.md:59 and refs/claim.md:125: "in the new worktree" / "as the worktree's pre-push hook"; code installs into the shared `<git-common-dir>/hooks/pre-push` (orca_worktree.py:1365,1402).
- **[STALE DOC]** refs/claim.md:125 "Before anything else the script runs the IR-4 preflight": record check, already-launched and stale-prompt checks run first (:1700-1724). SKILL.md:92 says "first checks" with the same looseness.
- **[STALE DOC]** refs/claim.md:125 names `git rev-parse --git-path hooks/pre-push`; code uses `--git-path hooks` (:1357).
- **[STALE DOC]** SKILL.md:35 lists four script subcommands in use; `pending` (orca_worktree.py:1886) is not named anywhere in skill, refs, command or templates.
- **[STALE DOC]** refs/tiers.md:32 and :44 repeat the heading `E-TIER-UNAVAILABLE (default D4)` with the first empty.
- **[STALE DOC]** templates/launch-prompt.md:23 lists `/sc:task` as an approving first line; the guard does not accept it (launch-level-guard.sh:347).
- Task brief says 17 template files; folder has 15.

## Defect Candidates and Not-Built Capabilities

No remediation tasks were created and nothing was written outside the task folder; these rows are for the owner to decide.

| # | Capability | Declaring doc (path:line) | Status | Evidence it is unreachable or unbuilt | Recorded decision in snapshot? |
|---|---|---|---|---|---|
| 1 | `orca_worktree.py pending` (a coordinator writes a launch record for a worker it starts) | orca_worktree.py:7-9 and :1516; docs/designs/issue-pipeline-guard-g2.md:18 | DEFECT CANDIDATE: verb built, no production caller | Grep of `src/` for `orca_worktree\.py[" ]+pending`, `cmd_pending`, `publish_pending`, `pending --level` finds only the definition/argparse lines inside orca_worktree.py (:8,:1488,:1515,:1518,:1893) plus `publish_pending` use in `cmd_launch` (:1761); only caller is a test: tests/hooks/test_launch_level_guard_worker.py:287 | None found: no file says the coordinator use is deliberately out of scope |
| 2 | IR-7 refusal of a launch when the L2 pre-push hook is not owned | issue.md:16; SKILL.md:92; refs/claim.md:134; sc-issue-launch-level-hook.md:355 | BUILT-OFF (`IR7_REFUSE = False`) | orca_worktree.py:822; branch :1757-1758 and :829-831 unreachable while False; test_issue_l2_install.py:639 pins False | Yes: orca_worktree.py:818-822 ("owner decision OD-3", "owner decision 2026-11-08", turn on only after the #442 observations pass) and hook design :355 (FR-065). Listed for visibility, not as a defect |
| 3 | Default `--pipeline` pick from type, complexity and hours | issue.md:43; refs/claim.md:81; pipeline-flag.md:21,43 | DEFECT CANDIDATE (NOT BUILT as code): rule exists only as prose the model applies | Grep of `src/` for the reason strings finds only issue.md, core/HOW-WE-WORK.md and refs/claim.md; no function computes it; tests pin text only (test_issue_protocol.py:774,:791; test_issue_command.py:182) | None found stating prose-only is deliberate |
| 4 | OB-H1 item 1 / OB-H2 / OB-H3 ship gate before any `worktree` or `full` claim on a real issue | issue.md:16; SKILL.md:92; refs/claim.md:136; pipeline-flag.md:4 | NOT BUILT as a mechanism (prose gate) | Grep `OB-H1|OB-H2|OB-H3` over `src/superclaude` `*.py *.sh *.json` returns 0 hits; no check in orca_worktree.py | The prose is itself the decision; no record says it is enforced by code |
| 5 | Coordinator handoff for `--pipeline none` (run the `worktree` step then `worker-start`, adoption row `reserved`) | issue.md:85; SKILL.md:140; refs/claim.md:96 | NOT BUILT in this area: prose only | Grep `orca_worktree` in `src/` shows no caller of the `worktree` subcommand other than the claim prose (files: issue.md, require-orca-worktree-agent.sh comment :60, claim.md, SKILL.md, launch-prompt.md, the script itself); the adoption-row text is in core/WORKER-CONTRACT.md (research 06) | None found |
| 6 | IR-3 `pipeline.json` level file | pipeline-flag.md:58; hook design (cited there) | NOT BUILT | Grep `pipeline\.json` over `src/` no match | Yes: pipeline-flag.md:58 and :4 state it is documentation only and deliberately not built |
| 7 | Approval by a first line `/sc:task` (prompt text) | templates/launch-prompt.md:23 | DEFECT CANDIDATE: prompt names a releasing form the guard does not accept | launch-level-guard.sh:347 regex; Grep `sc:task` in the guard returns no match | None found |
| 8 | Automatic action on `W-LAUNCH-NOT-CCSESSION` (close or kill an un-shimmed agent) | refs/claim.md:130 (remedy "close it") | NOT BUILT: warning only | orca_worktree.py:1803-1811 adds a note and continues; no close call | Remedy text asks a person to close it; no decision on automation found |

## Summary

`/sc:issue --claim` is a prose protocol run by the orchestrating model, backed by three helper scripts: `origin_repo.py` (resolves the repo from `origin` only, exit 1/3/4), `clickup_claim.py` (at most one ClickUp assignee add) and `orca_worktree.py` (the only caller of `orca`: preflight, worktree create/reuse, launch-prompt render, IR-4 guard preflight, L2 pre-push install, launch, and a `pending` verb). Worker agents t3/t2/t1 (pinned tier2b/tier2/tier1b) only read GitHub and write under `.dev/issues/`; the orchestrator alone writes to GitHub (assignee, two marked comments) and to ClickUp. A launch writes `pending/<nonce>` that the L1 guard consumes; the L2 refusal is switched off by `IR7_REFUSE = False`, and the default-level pick, the OB-H ship gate and the coordinator handoff exist only as prose. Several design and ref passages are stale (design status "nothing implemented", T3 tier3 pin, default-level table head, L2 location wording, the `/sc:task` approval form), and `orca_worktree.py pending` has no production caller in the snapshot.

## Gap-fill c1 B-2 (ERRATUM, supersedes the earlier wording)

Finding B-2: the section 3 table (Worker agents and tier pins) gives the Lines column of `issue-worker-t1.md`, `issue-worker-t2.md` and `issue-worker-t3.md` as 36. That is wrong. Snapshot root `/home/coder/.cache/ic-snap-20261120/master/` (origin/master 61ac2c2e6), read with `wc -l` in this gap-fill run.

### Corrected values (supersede the three `36` cells in the section 3 table, lines 69-71 of this file)

| Agent file | Lines (was) | Lines (correct) | Evidence |
|---|---|---|---|
| src/superclaude/agents/issue-worker-t1.md | 36 | 35 | `wc -l` = 35 [CODE-VERIFIED] |
| src/superclaude/agents/issue-worker-t2.md | 36 | 35 | `wc -l` = 35 [CODE-VERIFIED] |
| src/superclaude/agents/issue-worker-t3.md | 36 | 35 | `wc -l` = 35 [CODE-VERIFIED] |

Consistency check: line 35 of each file is the `**Return value.**` rule ("Return only the path of each file you wrote, one per line, and nothing else."), so 35 is the last line. This agrees with the existing `t*:35` citations in section 3, which were already right. Only the Lines column was wrong. The other cells in those rows were re-read and still hold: `model:` is on line 6 (`claude-gw-tier1b`, `claude-gw-tier2`, `claude-gw-tier2b`), `tools: Read, Grep, Glob, Write, Bash` on line 5 in all three, `effort: low` on line 7 of t3 only, numbered job items on lines 21-24 in t1 and t2 (four items) and `:22-24` in t3 (items 1-3 on lines 22-24), and `## Rules` begins at line 26 in t1 and t3 with the "Writing only under `.dev/issues/`" rule at line 30 [CODE-VERIFIED].

### Re-check of every other count in the section 3 table and of the other line counts in this file

The section 3 table has only those three rows, so there is no other file in that table. To meet the intent of the request, every other line count stated anywhere in this file was also re-run with `wc -l` against the snapshot:

| Claim in this file (location) | Stated | `wc -l` | Verdict |
|---|---|---|---|
| commands/issue.md (section 1 heading) | 117 | 117 | [CODE-VERIFIED] |
| skills/sc-issue-protocol/SKILL.md (section 2 heading) | 197 | 197 | [CODE-VERIFIED] |
| refs/chains.md (section 4) | 40 | 40 | [CODE-VERIFIED] |
| scripts/origin_repo.py (6a) | 195 | 195 | [CODE-VERIFIED] |
| scripts/clickup_claim.py (6b) | 270 | 270 | [CODE-VERIFIED] |
| templates/claim-comment.md (section 7) | 23 | 23 | [CODE-VERIFIED] |
| templates/accuracy-check-comment.md | 20 | 20 | [CODE-VERIFIED] |
| templates/issue-summary.md | 23 | 23 | [CODE-VERIFIED] |
| templates/next-steps.md | 14 | 14 | [CODE-VERIFIED] |
| templates/launch-prompt.md | 34 | 34 | [CODE-VERIFIED] |
| scripts/orca_worktree.py (section 8 heading) | 1906 | 1906 | [CODE-VERIFIED] |
| tests/skills/test_issue_protocol.py (section 14) | 1055 | 1055 | [CODE-VERIFIED] |
| tests/skills/test_issue_orca_worktree.py | 2501 | 2501 | [CODE-VERIFIED] |
| tests/skills/test_issue_repo_resolution.py | 291 | 291 | [CODE-VERIFIED] |
| tests/skills/test_issue_worker_agents.py | 559 | 559 | [CODE-VERIFIED] |
| tests/skills/test_issue_t1_fallback.py | 69 | 69 | [CODE-VERIFIED] |
| tests/skills/test_issue_l2_install.py | 716 | 716 | [CODE-VERIFIED] |
| tests/commands/test_issue_command.py | 212 | 212 | [CODE-VERIFIED] |
| tests/cli/test_issue_body_templates.py | 97 | 97 | [CODE-VERIFIED] |
| templates folder file count (section 7) | 15 | 15 | [CODE-VERIFIED] |

Result: no other wrong line count was found. The only wrong counts in this file were the three `36` cells. The section 14 test counts (`def test_` counts) are not line counts and were not re-counted here. [UNVERIFIED in this gap-fill: test counts.] No unwired, switched-off, retired or caller-less capability is involved in B-2, so there is nothing to record under C8.

Gap-fill c1 B-2 complete

---

## Gap-fill c1 F-2 (ADDENDUM: two more test-pin rows)

Finding F-2: the section 14 test-pin table and section 6b omit two test files that pin the claim path. This addendum adds them. Nothing above was altered. Method: both test files were read in full (all lines), `clickup_claim.py` was read in full (270 lines), and the three agent files' `model:` lines and the design doc lines were read from the snapshot `/home/coder/.cache/ic-snap-20261120/master`. Counts below come from `wc -l` and `grep -c 'def test_'` run on the live files (same method as section 14: a parametrized function counts once).

### F-2.1 The two rows (same columns as section 14; paths under `/home/coder/.cache/ic-snap-20261120/master/tests/`)

| Path | Lines | Test count | What it pins | Key test names |
|---|---|---|---|---|
| skills/test_clickup_claim.py | 569 | 29 (0 test classes; the one `class FakeClickUp` :101 is a fake ClickUp server, not a test class). 41 collected cases once the five parametrized functions are expanded (2 + 5 + 2 + 2 + 6 cases, read from the `parametrize` lists, not from a pytest run) | Behaviour of `clickup_claim.py`, the only ClickUp write in the claim path (row C2, `clickup_claim.py:232-237`). `urllib.request.urlopen` is patched with a fake server (:101-157) that answers only `GET /api/v2/user`, `GET /api/v2/team/<ws>/task` and `PUT /api/v2/task/<id>`; any other request raises `AssertionError` (:145-146), so a second kind of ClickUp write would fail every test that reaches it. Pinned: (1) skip without token or workspace, no HTTP call (:189, :197); (2) match rule 1 `github_link` (markdown description or custom-field value, case-insensitive, a longer issue number does not match; :208, :228, :242) and rule 2 `title_number` (whole-token `#<N>` only; :248, :259), and the order rule-1-before-rule-2 (:208); (3) more than one match is `ambiguous`, candidates returned, no PUT (:277; also :442 under the default cap); (4) `not_found` (:289); (5) `already_assigned` makes no PUT (:298); (6) the one write is `PUT https://api.clickup.com/api/v2/task/86todo` with body `{"assignees": {"add": [4242]}}` and the token only in the `Authorization` header (:311-318); (7) `list_ids[]`, `subtasks=true`, `include_markdown_description=true` are sent (:321); (8) 401 and 403 give `auth` (:336), 429 is retried exactly once after `Retry-After` and then continues (:343), two 429s give `rate_limited` after one sleep and two calls (:352), another HTTP error gives `http_500` (:360); (9) paging: the cap is honoured and the first page is 0 (`cc.FIRST_PAGE == 0`; :372), an empty page ends the search (:382), an invalid `CLICKUP_MAX_PAGES` (`0`, `-1`, `abc`, empty, `2.5`) falls back to the default 20 with exactly 1 user call plus 20 page calls and no PUT (:389-399); (10) a search stopped by the page cap never assigns, whatever it found: a title match with a link task past the cap (:405, with and without `CLICKUP_LIST_IDS`), a second link match past the cap (:428), an already-assigned task with an unseen page left (:492), while the same data under the default cap is `ambiguous` (:442) and a lone match on the last allowed page is assigned or `page_cap` depending on cap 4 or 3 (:459); (11) a request error inside the search wins over `page_cap` (:500); (12) bad arguments exit 2 with zero HTTP calls (six cases: no args, missing `--repo`, non-numeric number, number 0, `--repo not-a-repo`, URL for another issue number; :514-545); (13) the token never reaches stdout or stderr: an autouse fixture asserts it at teardown (:160-168), `run()` asserts it per call (:179-183), and :548 loops over assigned, 401, double 429 and 500; (14) the script imports only standard-library modules, checked with `ast` and `sys.stdlib_module_names` (:561). Every test starts with the four `CLICKUP_*` variables cleared (:160-165) | `test_ambiguous_returns_candidates_and_makes_no_put` :277, `test_already_assigned_makes_no_put` :298, `test_assign_sends_assignees_add_body` :311, `test_429_is_retried_exactly_once_then_continues` :343, `test_page_cap_is_honoured_and_first_page_is_zero` :372, `test_title_match_with_link_task_past_the_cap_is_not_assigned` :406, `test_request_error_inside_the_search_wins_over_page_cap` :500, `test_bad_arguments_exit_2` :539, `test_token_never_printed_on_any_outcome` :548, `test_script_imports_only_standard_library` :561 |
| skills/test_model_alias_policy.py | 249 | 11 (0 classes). 13 collected cases: `test_issue_worker_allow_list_entries_exist` is parametrized over the three allow-list keys (:246) | Static (file text and `ast`) model-selection policy of issue 384. The part that touches this pipeline: `ISSUE_WORKER_PINS` (:29-33; entries :30-32) maps `issue-worker-t3.md` to `claude-gw-tier2b`, `issue-worker-t2.md` to `claude-gw-tier2`, `issue-worker-t1.md` to `claude-gw-tier1b`. (1) `test_frontmatter_model_is_an_alias_when_present` (:83-101) fails when an agent file in `ISSUE_WORKER_PINS` has a `model:` that differs from its pin (:95-98); every other agent, skill and command frontmatter `model:` must be `opus`, `sonnet`, `haiku` or `inherit`. A file with no `model:` line is skipped (:92-94). (2) `test_tier_ids_appear_only_in_allowed_paths` (:104-119) fails on the text `claude-gw-tier` anywhere under `src/superclaude/{agents,commands,skills,cli,hooks,core}` outside `TIER_TEXT_ALLOWED` (:38-44): the three pinned worker files, `skills/sc-issue-protocol/`, `skills/ccsession-tag/` and `cli/review/data/`. (3) `test_issue_chains_use_the_default_brainstorm_models` (:191-196) reads `skills/sc-issue-protocol/refs/chains.md`, finds every backticked `/sc:brainstorm ...` step, requires at least two, and requires that none carries `--models`. (4) `test_issue_worker_allow_list_entries_exist` (:246-249) only asserts that each allow-listed worker file exists (it does not read the pin). (5) The other eight tests are repository-wide alias policy and are not part of the claim path: Python string constants are not full model ids (:139), markdown does not pass a full id to `--model` or `--models` (:164), the reflect default is an alias (:176), the D12 manual test does not pin the old reflect model (:183), the cleanup-audit docs match the `audit-scanner` pin (:199), the retry ladder uses the exported slot names (:217), the mapping document spells the three exports and the tiers exist in `ccsession-models.json` (:231) | `test_frontmatter_model_is_an_alias_when_present` :83, `test_tier_ids_appear_only_in_allowed_paths` :104, `test_issue_chains_use_the_default_brainstorm_models` :191, `test_issue_worker_allow_list_entries_exist` :247 (the `def` line; the decorator is :246) |

### F-2.2 Ties to the claim path (re-verified against the live files)

Tie to the C2 write row (`clickup_claim.py:232-237`, section 5a row C2 and section 6b):
- Live code: `request("PUT", f"{API}/task/{quote(result['task_id'])}", token, {"assignees": {"add": [user_id]}})` at `clickup_claim.py:232-237`. The assertion at `test_clickup_claim.py:316-317` (`put["url"] == "https://api.clickup.com/api/v2/task/86todo"` and `put["body"] == {"assignees": {"add": [4242]}}`) is the one that pins it, and `:318` pins that every request carries the token in `Authorization` (code: `req.add_header("Authorization", token)`, `clickup_claim.py:109`) [CODE-VERIFIED].
- The "no PUT" outcomes map to the code paths that return before line 232: `ambiguous` (code :212-220, test :277-286), `already_assigned` (code :230-231, test :298-308), `not_found` (code :210-211, test :248-256 and :289), `page_cap` (code :203-206, tests :372-379, :405-425, :428-439, :492-497, :500-508), `skipped` (code :166, :169, tests :189-202) and bad arguments (code :245-259, test :539-545). Every `assert fake.puts() == []` is a statement that the C2 write did not happen [CODE-VERIFIED].
- All six outcome words that `refs/claim.md:51` lists as non-fatal (`assigned`, `already_assigned`, `skipped`, `not_found`, `ambiguous`, `error`) each have at least one test: :208, :298, :189, :289, :277, :337 [CODE-VERIFIED]. The `claim.md:50` command line and the claim.md "exit 2 means STOP and the GitHub assignment stays" prose are not exercised by this file (it calls `cc.main()` directly); the prose half is text in `refs/claim.md:51`, not a test pin [CODE-VERIFIED by absence in the 569 lines].
- Cross-check of the C2 write count claim in section 5a ("clickup_claim.py:232-237 is the only non-GET request"): the fake server rejects any other request type with `AssertionError` (:145-146), so the test file independently enforces it [CODE-VERIFIED].

Tie to the T3 stale-doc finding (section 15 row D3 and the Stale Documentation entry about `claude-gw-tier3`):
- Live agent files: `model:` is on line 6 of each: `issue-worker-t1.md` `claude-gw-tier1b`, `issue-worker-t2.md` `claude-gw-tier2`, `issue-worker-t3.md` `claude-gw-tier2b` [CODE-VERIFIED, `grep -n '^model:'`]. These three values equal `ISSUE_WORKER_PINS` at `test_model_alias_policy.py:30-32`, so `test_frontmatter_model_is_an_alias_when_present` passes on the snapshot, and it would fail if `issue-worker-t3.md` said `claude-gw-tier3` (:97-98) [CODE-VERIFIED by reading the test logic].
- `docs/designs/sc-issue-command.md` still says `claude-gw-tier3` for T3 at lines 58, 107, 129, 391, 423 and 449 (re-grepped on the snapshot) [CODE-CONTRADICTED by `issue-worker-t3.md:6`, by `test_model_alias_policy.py:30` and by `test_issue_worker_agents.py:22-23`, which carries the comment "Pinned to Tier 2b (Terra first) by the owner on 2026-11-12, issue 488" and the entry `"issue-worker-t3": ("claude-gw-tier2b", "tier2b")`]. Line 423 is the design's description of `test_issue_worker_agents.py` and also says `claude-gw-tier3`, so the design describes a test that the live test no longer matches.
- No test catches this stale design text: `test_tier_ids_appear_only_in_allowed_paths` scans only `src/superclaude/{agents,commands,skills,cli,hooks,core}` (:50), and `docs/designs/` is outside that list. The stale line is therefore a documentation staleness finding, not a failing test.
- `docs/reference/model-aliases.md:16` states the same three pins and calls the name `issue-worker-t3` "a label" now running on Tier 2b (issue 488) [CODE-VERIFIED against the agent files' line 6]. Its lines 12 and 18 cite test line numbers that have moved ("test lines 46-47 and 100-115", "test lines 36-40"); the live positions are `TIER_TEXT_DIRS` :50, `TIER_TEXT_ALLOWED` :38-44 and the test :104-119 [CODE-CONTRADICTED, line numbers only]. Its line 18 lists three allowed locations (the three pinned files, `sc-issue-protocol/`, `ccsession-tag/`) and omits the fourth, `src/superclaude/cli/review/data/` (live :43) [CODE-CONTRADICTED, doc omission; a grep for `review/data` in that doc found nothing].
- `docs/designs/sc-issue-command.md`, `docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md` and `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` all contain the text `claude-gw-tier3`. Only the design file was read for this addendum; the other two were not read, so whether they pin T3 to tier3 or mention tier3 as a tier is [UNVERIFIED].

### F-2.3 Doc claims inside the two test files

| Claim in the test file | Tag | Evidence |
|---|---|---|
| `test_clickup_claim.py:1` "(design section 12)" | [CODE-VERIFIED] | `docs/designs/sc-issue-command.md:306` is `## 12. ClickUp lookup and assignment`. Whether the tests match every sentence of that section was not compared here |
| `test_clickup_claim.py:3-5` "EXECUTABLE ... urlopen is patched ... Every fixture value is made up" | [CODE-VERIFIED] | patch at :176 (`monkeypatch.setattr(cc.urllib.request, "urlopen", fake)`); token is `pk_000000_FAKETOKENFORTESTSONLY` (:32); all ids are made up (:33-36, :48-78); all 569 lines were read |
| `test_clickup_claim.py:7-8` "Every test starts with all four CLICKUP_* variables cleared" | [CODE-VERIFIED] | autouse fixture `clean_env` :160-165 deletes `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES` (tuple :38-43) |
| `test_model_alias_policy.py:1` "(issue #384, owner decision: option A)" | [UNVERIFIED] | the issue was not read; `docs/reference/model-aliases.md:3` repeats "issue #384 owner decision of 2026-11-05" |
| `test_model_alias_policy.py:26-28` the pinned agents "stop with E-TIER-UNAVAILABLE outside a ccsession tier workspace (see ... tiers.md)" | [CODE-VERIFIED] | `refs/tiers.md:44-46` (STOP `E-TIER-UNAVAILABLE` when the picker id is not served, "for example, outside a ccsession tier workspace"). The heading appears twice, `tiers.md:32` and `:44`, as already recorded in section 3 |
| `test_model_alias_policy.py:35-37` "ccsession-tag is the launcher package (owned by issue #315, read-only for this policy)" | [UNVERIFIED] | issue 315 was not read; only the allow-list entry itself (:41) is verified |
| `test_model_alias_policy.py:42` "the review panel tier file maps the gateway tier aliases to model lists by design (PN1, shared contract C2)" | [UNVERIFIED] | `src/superclaude/cli/review/data/` is outside this pipeline and was not opened |
| `test_model_alias_policy.py:191-196` the chains pass no `--models` | [CODE-VERIFIED] | `refs/chains.md:12` and `:13` are the only two lines with `/sc:brainstorm` and neither has `--models` (they carry `--blind`, `--depth deep --research deep --codebase --blind`). This meets the test's "at least two steps" floor exactly, so removing one brainstorm step from `chains.md` would make `test_issue_chains_use_the_default_brainstorm_models` fail at `assert len(steps) >= 2` |

### F-2.4 Correction to the finding text and gaps in what the two files pin

Corrections where the source disagrees with the instruction wording (the numbers in the instruction were right: 569 lines and 29 tests, 249 lines and 11 tests, the five named example tests at the stated lines, and the map at lines 30-32):
- "page_cap beating other outcomes" holds for `not_found`, `ambiguous`, `assigned` and `already_assigned`, but the reverse also holds for one case: a request error inside the search wins over `page_cap` (`test_clickup_claim.py:500-508`; code: `ClickUpError` raised by `request()` is caught at `clickup_claim.py:239-240` before the `complete` check at :203). Both directions are pinned.
- `test_issue_worker_allow_list_entries_exist` (:246-249) pins only that the three worker files exist. The pin values are pinned by `test_frontmatter_model_is_an_alias_when_present` (:83-101), which reads them from `ISSUE_WORKER_PINS` (:29-33).

What the two files do not pin (coverage facts, not defects; every item checked by reading all of both files):
- `test_clickup_claim.py` has no test for the error reasons `network` (code :125-126), `bad_response` (code :127-132 and :178-179) or `unexpected` (code :241-242), for the `seen` de-duplication of task ids (code :196-199), for an `ambiguous` result under rule 2 `title_number` (test :277 and :442 use only link matches), or for `already_assigned` under rule 2 (test :298 uses a link match only).
- `test_model_alias_policy.py:92-94` skips a worker file that has no `model:` line, so deleting the pin from an issue worker does not fail this file; it is held by the separate worker-agent test file already in the section 14 table (`test_worker_file_exists_with_pinned_picker_id` :77 per that row; not re-read in this gap-fill).
- Neither file tests `effort: low` of `issue-worker-t3.md:7` (that is `test_t3_effort_is_low` in the section 14 row for `test_issue_worker_agents.py`, per that row).

C8 (unwired, switched-off, retired, dead or caller-less capabilities): none was found in these two files or in the paths they pin, so no DEFECT CANDIDATE or NOT BUILT entry is created. The only discrepancy is the stale design text about T3 and the stale line citations in `model-aliases.md`, recorded above as documentation staleness.

Gap-fill c1 F-2 complete

---

## Gap-fill c2 N-1 (ERRATUM, supersedes the earlier wording)

Finding N-1: in the F-2.1 row for `skills/test_model_alias_policy.py` (the second row of the table at line 554 of this file), "What it pins" item (5) says "The other eight tests are repository-wide alias policy and are not part of the claim path" and then lists seven tests. Nothing above was altered; this section supersedes that one word. Method: the live files `/home/coder/.cache/ic-snap-20261120/master/tests/skills/test_model_alias_policy.py` (249 lines) and `/home/coder/.cache/ic-snap-20261120/master/tests/skills/test_clickup_claim.py` (569 lines) were re-read in full, and `grep -n -E '^\s*(async )?def test_|^class '` plus `grep -n parametrize` were run on both. Line numbers below are for the 61ac2c2e6 snapshot.

### N-1.1 The erratum

Item (5) of the `test_model_alias_policy.py` row must read: "The other **seven** tests are repository-wide alias policy and are not part of the claim path". The live file disagrees with nothing in the instruction, so it needs no correction [CODE-CONTRADICTED: the word "eight" in the F-2.1 row is wrong; the row's own list and the live file both give seven].

Evidence (live file, `def` lines of all 11 test functions, in file order): `test_frontmatter_model_is_an_alias_when_present` :83, `test_tier_ids_appear_only_in_allowed_paths` :104, `test_python_selection_constants_are_not_full_model_ids` :139, `test_markdown_does_not_pass_full_model_ids_to_model_flags` :164, `test_reflect_default_model_is_an_alias` :176, `test_d12_manual_test_does_not_pin_the_old_reflect_model` :183, `test_issue_chains_use_the_default_brainstorm_models` :191, `test_cleanup_audit_docs_match_the_audit_scanner_pin` :199, `test_retry_ladder_uses_the_variable_names_the_workspace_exports` :217, `test_mapping_document_states_the_exports_and_tiers_exist` :231, `test_issue_worker_allow_list_entries_exist` :247 (decorator :246) [CODE-VERIFIED].
- Items (1) to (4) of the row cover four of the 11: :83, :104, :191, :247.
- 11 - 4 = 7. The seven are exactly the ones the row lists after the sentence: :139, :164, :176, :183, :199, :217, :231 [CODE-VERIFIED].
- The other numbers in the row still hold: 11 tests, 13 collected cases (the one parametrized function, :246, runs over the three keys of `ISSUE_WORKER_PINS`, :29-33, so 10 + 3 = 13), 0 classes, 249 lines, `ISSUE_WORKER_PINS` entries at :30-32 [CODE-VERIFIED].

### N-1.2 Re-check of every other count in the two F-2.1 rows

`test_clickup_claim.py` row (all [CODE-VERIFIED] against the live file; no number is wrong):
- 569 lines (`wc -l`); 29 test functions (`def test_` at :189, :197, :208, :228, :242, :248, :259, :277, :289, :298, :311, :321, :337, :343, :352, :360, :372, :382, :390, :406, :428, :442, :475, :485, :492, :500, :539, :548, :561); 0 test classes, one `class FakeClickUp` at :101.
- Five parametrized functions, each decorator on the line before its `def`: :336 (`[401, 403]`, 2 cases), :389 (`"0", "-1", "abc", "", "2.5"`, 5), :405 (`[None, "111"]`, 2), :459 (cap `"3"` and `"4"`, 2), :514 (six argument lists, 6). 2 + 5 + 2 + 2 + 6 = 17 cases from 5 functions, plus the other 24 functions, gives 24 + 17 = 41 collected cases. The row's "41" is right (read from the `parametrize` lists, not from a pytest run).
- Line citations in the row all point at the stated content: fake server :101-157 (class body ends :157); `AssertionError` :145-146; autouse fixture :160-168 (`clean_env`; the four-variable delete is :162-163); `run()` assertion :179-183; skip tests :189, :197; rule tests :208, :228, :242, :248, :259; ambiguous :277 and :442; not found :289; already assigned :298; the PUT assertions :311-318 (url :316, body :317, auth :318); list ids :321; auth :336/:337; 429 :343 and :352; HTTP 500 :360; paging :372, :382, :389-399; past-the-cap :405/:406, :428, :492, :442, :459/:475; request error vs cap :500; bad arguments :514-545 (six cases, in the order the row lists them); token never printed :548; stdlib-only :561. The ten "Key test names" lines (:277, :298, :311, :343, :372, :406, :500, :539, :548, :561) are all the `def` lines of those names.
- Code line citations used by the row and by F-2.2 and F-2.4 all match the live `clickup_claim.py` (270 lines): PUT :232-237, Authorization header :109, `network` :125-126, `bad_response` :127-132 and :178-179, `unexpected` :241-242, `seen` :196-199, `ClickUpError` catch :239-240, page-cap return :203-206, `ambiguous` :212-220, `already_assigned` :230-231, `not_found` :210-211, `skipped` :166 and :169, argument parsing :245-259.

`test_model_alias_policy.py` row: every line citation was re-read and matches (:83-101, :92-94, :95-98, :104-119, :38-44, :50, :139, :164, :176, :183, :191-196, :199, :217, :231, :246-249). The only wrong number in the row is "eight" (N-1.1).

Wrong numbers found: one (the word "eight", corrected to seven above). No other wrong number was found in either row.

### N-1.3 Wording that is not a number but is looser than the live test (found while re-checking)

These do not change any count; they are recorded so a reader of the F-2.1 rows is not misled.
- Row `test_clickup_claim.py` item (10) says "a lone match on the last allowed page is assigned or `page_cap` depending on cap 4 or 3 (:459)". In the live test (:459-482) the single link match is on page index 2 in both cases. With cap 3, page 2 is the last allowed page, no empty page is read, so the result is `page_cap` (pages seen `[0, 1, 2]`). With cap 4, the search also reads page 3, which is empty, so the search completes and the match is assigned (pages seen `[0, 1, 2, 3]`); there page 2 is not the last allowed page. The test name ("only match on the last allowed page") fits the cap-3 case only [CODE-VERIFIED].
- Row `test_clickup_claim.py` item (6) says the token is "only in the `Authorization` header". The test pins `auth == TOKEN` on every recorded call (:318) and pins the PUT url and body (:316-317), and the autouse fixture and `run()` pin that the token is absent from stdout and stderr. No test asserts that the token is absent from the URL of a GET request, so "only" is shown for the PUT and for the output, not for every request [CODE-VERIFIED by reading all 569 lines].
- Row `test_model_alias_policy.py` item (2) says "the text `claude-gw-tier` anywhere under" the six directories. The test reads only files whose suffix is in `TEXT_SUFFIXES` (`.md`, `.py`, `.json`, `.yaml`, `.yml`, `.sh`, `.txt`, `.toml`; :51 and :112), so a file with another suffix is not scanned [CODE-VERIFIED].
- Row `test_model_alias_policy.py` item (5), last test (:231): the test requires `tier1a`, `tier1b` and `tier2` to be keys of `models["tiers"]` in `ccsession-models.json` (:243). It does not check `tier2b`, which is the tier that `issue-worker-t3` runs on [CODE-VERIFIED].
- Row `test_model_alias_policy.py` item (1): the frontmatter scan covers `agents/*.md`, `skills/*/SKILL.md` and `commands/*.md` directly under `src/superclaude/` (:85-89; the globs are not recursive), not command files in subfolders [CODE-VERIFIED].

C8 (unwired, switched-off, retired, dead or caller-less capabilities): none found in this re-check; no DEFECT CANDIDATE or NOT BUILT entry is created. The only defect is a documentation error in this research file (the word "eight"), now superseded.

Gap-fill c2 N-1 complete

