# Design: `/sc:closeout` command and `sc-closeout-protocol` skill

**Status:** Design only. Nothing is built: no skill, no command, no script and no test exists. The owner approves this spec before anything is built.
**Issue:** IronbellyOrg/IronClaude #668 (body and its accuracy-check comment).
**Branch and base:** `clayphi/issue-668`, from `origin/master` at 64dfc0e86.
**Produced by:** `/sc:design closeout --type architecture --format spec`, 2026-11-19. Independent readers review it after its author; the author's own checks are not a gate.
**Adopts:** `skills/closeout/SKILL.md` and `scripts/branch-landed.sh` from https://github.com/Simple-With-Us/AI-Fleet-Coordinator, Jay Wedgeworth's work, Apache-2.0, used with the owner's approval. Content pins and the lines relied on are in sections 2 and 7.
**Source of truth:** `src/superclaude/` copied to `.claude/` by `make sync-dev`; `.claude/` is never staged.
**Where this file lives:** `docs/designs/sc-closeout.md`, fixed by the assignment. The routing guide says `/sc:design` has "No declared destination option" (`src/superclaude/core/HOW-WE-WORK.md:230`) while the command file lists `--output <file>` (`src/superclaude/commands/design.md:23,26`); this design relies on neither.

Grounding: codegraph was not used for lookups. The work is a design over text files and one shell script, so every `file:line` below was read with Read, Grep or `sed`. One `codegraph_status` call showed an index of this worktree with 0 changes pending.

Evidence: each statement about our code cites a `file:line` read in this worktree (base 64dfc0e86). Statements about Jay's files cite their line numbers as read on 2026-11-19. Statements about `gh` and `orca` come from commands run read-only on that day. Anything not read is marked UNVERIFIED and listed in section 11.

Rulings that bind this design (owner and orchestrator, 2026-11-18 and 2026-11-19):

- Closeout is its own small skill, `sc-closeout-protocol`, with the command `/sc:closeout <PR>`. Wave 8 of the orchestrator design calls it and a person uses it by hand for any pull request. It is its own pull request, not part of the orchestrator's (rulings 19 and 21).
- It adopts and adapts Jay's two files; it does not redo the design (ruling 22).
- People are credited by name; the agent is never named in anything a person reads (ruling 15).
- Plain English, no em or en dashes, no secret written anywhere (ruling 17). The repo is public, so no path of any machine appears in a skill file or in this spec.
- The orchestrator merges, and a person may merge first. This skill starts after a merge and never merges (ruling 13 and the issue's Out of Scope).
- Pickup of a dead agent's work is not needed (ruling 14). This skill does not pick up, start, stop or abandon a worker.

---

## 1. Purpose and scope

### 1.1 What it does

After a pull request is merged, `/sc:closeout <PR>` does five things, in this order:

1. **Truth check.** A script reads the pull request state first. Only a merged pull request goes on. For a merged one it also compares what the pull request held with what the merge changed, using a three-dot diff. It never decides from commit ancestry.
2. **Issue.** It closes the pull request's issue with one note that says what merged and who merged it, or leaves an already-closed issue alone. It checks, and does not assume, that the pull request body links the issue.
3. **Work report entry.** It settles the issue's entry in the work report.
4. **Worker's Orca task.** It settles the Orca task of the worker that built the pull request.
5. **Result.** It prints one short, fixed-shape result. The orchestrator records it; a person reads it printed.

Each of the three items (issue, entry, task) ends with one stated final status or with an escalation that says why not. An item with neither fails the skill's own check (section 3).

"Completed" means merged. "Deployed" means verified in the place it runs. This version never writes "deployed" (section 5.5).

### 1.2 Out of scope

From the issue: making the merge; the wave 8 text of the orchestrator design (issue #655 owns it); the draft additions A to E to that design; anything else in Jay's repository, such as its pull request sweep.

Dropped from Jay's skill because our setup has no such surface (section 2): Linear, Zulip, Apple Notes, Mac process rows, retiring a lane, default-off feature rows, fleet recall, and the "parked, not done" path (this skill acts only after a merge).

### 1.3 Decisions

Each decision has a one-line reason. "Draft part D" means the unmerged draft addition D to the orchestrator design (`ADDITIONS-A-E-DRAFT.md`), which the 655 side owns; where this spec differs from it, the difference is stated so the 655 side can reconcile it.

| # | Decision | Reason |
|---|---|---|
| D1 | The two scripts are shell with `jq`, not Python. | Jay's `branch-landed.sh` is shell and our model script `finish-merge.sh` is shell that requires `jq` (`src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:106`); the repo forbids calling bare Python, and the embedded `python3` heredoc (`branch-landed.sh:51-78`) is the one part that breaks that. |
| D2 | The skill headings are `## Will Do` and `## Will Not Do`. | Five protocol skills use them (`sc-pr-submit-protocol/SKILL.md:330,339`, and the auggie-review, cli-eval, swarm-wizard and troubleshoot skills); only `sc-issue-protocol` uses `## Will` and `## Will Not` (`SKILL.md:179,187`); the issue's acceptance text names `Will Do` and `Will Not Do`; no test pins either form. |
| D3 | The skill writes only after a verdict of `MERGED`. | The issue says it acts only on a merged pull request; every other verdict stops with no write. |
| D4 | The repo is always `origin`. There is no `--repo` flag. | The issue says so, `/sc:issue` works the same way (`commands/issue.md:46`, `sc-issue-protocol/SKILL.md:72`), and the fork rule in CLAUDE.md forbids guessing the target. A URL for another repo is refused. |
| D5 | The final status words are fixed: `settled`, `already_final`, `none_found`, `escalated`. | One small closed set that the orchestrator and a person read the same way (section 5.1). |
| D6 | A table in the scripts decides each status; judgment writes only the closing note's one sentence and the escalation sentence. | Ruling 19 says the contract must work when the orchestrator calls the scripts directly, so the status cannot depend on a model's reading. This uses judgment less than the issue allows, on purpose. |
| D7 | The note is posted by the same call that closes the issue; an issue that is already closed gets no note. | One write, no half-done state, and a second run finds the issue closed and does nothing. The issue asks for the note on the close only (acceptance row 3). |
| D8 | The person who merged is named by the name on their public GitHub profile, else by their login. The pull request title is never quoted. | Ruling 15 (people by name). Quoting a title would copy text a person or an agent wrote into a note without a check. |
| D9 | "Deployed" is never written in this version. | There is no input that carries a recorded check, so nothing can back the word; section 5.5 says what a recorded check will have to be. |
| D10 | The work report entry is settled only through `superclaude orchestrator report-entry --key <key> --closed`. Where that command is absent the entry item is `escalated`. | The report surface is outside IronClaude today (section 5.3); the skill must not edit report files itself. |
| D11 | The worker's Orca task is found by the task id of the worker's dispatch, or else by the title `<owner>/<repo>#<N>`, and set to `completed`. With no Orca Run bound it is `escalated`. | Verified today: `worker-list` rows carry `dispatchId` and `taskId`, and `task-list` refuses with `run_required` when no Run is bound (section 5.4). |
| D12 | `/sc:closeout` goes on the never-as-worker list, in all four places that pin it. | It writes to GitHub and to the coordinator's task, which a worker may not do (section 9.3). |
| D13 | The command has no `## Unattended mode` section. | It is not dispatched as a worker, and a test fails for any command with that section that is not on its list (`tests/skills/test_worker_contract.py:817-825`). |
| D14 | Two scripts only: `branch-landed.sh` (the adopted truth check) and `settle.sh` (the three settle steps). No Python package. | "Deterministic parts are scripts" (ruling 19); the issue lists `scripts/` and no package. Draft part D proposes a `superclaude closeout` package; this spec does not. |
| D15 | Three items settled, not four. The worker's Dispatch is only reported. | The issue names the issue, the entry and the worker's task. Draft part D adds a fourth settled status, the worker's Dispatch (release of its terminal). This skill never releases, stops or messages a Dispatch: wave 9 of the orchestrator releases it, and a person does by hand. When `--dispatch` is given, the `TASK` line carries `dispatch=<state read>` (read only), so wave 8 can see whether the worker still runs. The 655 side decides whether to ask for more. |
| D16 | One line is added to `CHANGELOG.md` under `## [Unreleased]`. | The issue left it open; earlier `/sc:issue` work has entries there, and a new command is user-visible. |
| D17 | When the held-versus-merged comparison says `differs`, nothing is written: all three items are `escalated`. `same` and `unchecked` change nothing. | The issue says the skill checks that what merged is what was asked for before it settles (section 4.4). |

## 2. Adoption table: what is kept, changed or dropped

Jay's `skills/closeout/SKILL.md` (110 lines, content hash 905bfbe5b6, last changed 2026-11-05) and `scripts/branch-landed.sh` (85 lines, content hash d18608c2a5, last changed 2026-09-17) were read in full. Line numbers below are the lines of those files. `kept as is` means the text or logic carries over unchanged except for the dash and spelling rules of ruling 17. `changed` means only the part our setup needs is different. `dropped` means it names a surface we do not have or a step the issue does not ask for.

### 2.1 `SKILL.md`

| Lines | Jay's element | Verdict | What happens in our version, and why |
|---|---|---|---|
| 1-4 | Frontmatter: `name: closeout`; description; "Never silently walk away from In Progress" | changed | `name: sc:closeout-protocol` and an `allowed-tools` line, as `sc-issue-protocol` does (`SKILL.md:2,4`). The description names our three items. The last sentence becomes "Never leave an item silently in progress", because "In Progress" is a Linear status and ours has no board. |
| 6-8 | Title "Closeout (Universal)" and the opening paragraph | changed | Same idea, our surfaces: the end of work is the issue, the work report entry, the worker's task and the pull request that links the issue. |
| 10-12 | `## 1. Truth check`, first bullet: merged to `main`? no commit ancestry after a squash merge; use PR state, then a three-dot diff | kept as is | This is the rule the issue asks for. The branch name `main` becomes "the pull request's base branch". |
| 14-19 | Code block: MCP pull request listing, `git fetch origin`, `git diff origin/main...HEAD`, helper `branch-landed.sh [repo] [branch]` | changed | `gh pr view <N> --repo <R>` replaces the MCP tool; `git fetch origin` stays; the three-dot diff uses the base the pull request names and the head GitHub kept at `refs/pull/<N>/head`, because a person who runs this has no lane whose `HEAD` is the branch; the helper takes `<PR>`. |
| 21 | Two-dot `git diff origin/main HEAD` on a stale lane is "actively misleading"; ancestry is correct only for "does this exact SHA exist on live/main" | changed | The two-dot warning is kept as is and is a Will Not. The ancestry exception is dropped: this version writes no deploy claim, so nothing needs it. |
| 22 | "Production verified? (`deploy-verify`) Completed != Deployed" | changed | Kept in meaning: two words, two meanings (section 5.5). The `deploy-verify` skill is Jay's (Coolify, per-app health URLs) and is not adopted. |
| 23 | "Uncommitted files? Commit or explicitly report why not" | dropped | This skill starts after a merge from any checkout and never touches a worker's worktree. |
| 25-30 | `## 2. Linear`: `linear_status` (completed or deployed) and `linear_comment` "Landed in #<PR>. <one line>." | changed | The GitHub issue replaces the Linear issue: `gh issue close --reason completed --comment <note>` (section 5.2). Only "completed" is written. The note keeps the shape "Landed in <PR>" plus one line, and adds who merged. |
| 32 | `Fixes <ID>` moves the issue to Done on merge; `Refs <ID>` never closes it, so run the command yourself or leave it open on purpose; seat-verified writes | changed | The link is checked, not assumed: the script reads the pull request's closing references and body and prints `closing`, `refs` or `none` (section 4.4). An open issue is closed whichever it is, because the issue's acceptance row says an issue the merge did not close is closed; the note says which. The seat and bearer rules are dropped: we write as the person's own `gh` login. "Safe to repeat" is kept as is (section 6). |
| 34-35 | "Completed = merged to main. Deployed = released and verified (say how)." | kept as is | These are the two fixed meanings of the issue. |
| 36 | Correct a wrong status with a new comment or status, never by editing another seat's comment | kept as is | Becomes a Will Not: the skill never edits or deletes any comment or any other text on GitHub. |
| 38 | Every imported GitHub issue has a Linear twin; close the Linear one | dropped | We have no twin. The GitHub issue is the issue. |
| 40 | No effort log to update | dropped | No such log. |
| 42-44 | `## 3. The PR`: the body names the issue; branch name `<seat>/<id>-<slug>`; say in the closeout post which keyword you used | changed | The body link is checked and printed; the note and the result say which kind it was. The branch naming rule is dropped (ours is a person's or the orchestrator's choice). |
| 46 | PR writes only through `git-relay` and its MCP tools; a personal `gh` credential is not the route | dropped | The opposite holds for us: every write is a `gh` call that names `--repo <R>`, as the fork rule in CLAUDE.md requires. |
| 48-58 | `## 4. Zulip` | dropped | No Zulip. ClickUp notices are not part of this skill (ruling 1: the orchestrator keeps the report; the daily run adds the rest). |
| 60-62 | `## 5. Apple Notes` | dropped | The work report entry takes its place as its own item. That item is new: the issue adds it, and neither of Jay's files has it. |
| 64-68 | `## 6. Mac local processes` | dropped | No such inventory. |
| 70-79 | `## 7. Retire the lane` | dropped | The orchestrator leaves the worktree in place and never removes one (orchestrator design wave 9, `docs/designs/orchestrator.md` on the 655 branch, line 527). Not asked for in the issue. |
| 81-83 | `## 8. Default-off features` | dropped | No enablement backlog. |
| 85-87 | `## Parked, not done` | dropped | The issue limits this skill to merged pull requests. For any other verdict the skill stops, writes nothing and says why (section 4.3). Its principle, never silently in progress, stays as acceptance row 5. |
| 89-97 | `## Fleet recall (every closeout)` | dropped | Jay's own memory service. |
| 99-103 | `## Canon` | changed | A short pointer list to our own files: the command, `refs/settle.md`, `refs/result.md`. |
| 105-110 | `## Living Handoff Morphing to Closeout` | dropped | The orchestrator keeps the report as a living document (ruling 1), and pickup of another seat's work is not needed (ruling 14). |

### 2.2 `branch-landed.sh`

| Lines | Jay's part | Verdict | What happens in our version, and why |
|---|---|---|---|
| 1-18 | Header comment: purpose, why ancestry lies after a squash with branch deletion, usage, five tokens, "Exit 0 only for MERGED", two-dot warning | changed | The purpose, the "ancestry lies" reason, the five tokens, "exit 0 only for MERGED" and the two-dot warning stay as is. The usage line becomes `branch-landed.sh <PR>`. The incident dates and the board id in lines 5-8 are Jay's own references and are dropped. The notice block of section 7 is added at the top. |
| 19 | `set -euo pipefail` | changed | `set -u -o pipefail`, as `finish-merge.sh:30` does, so a failed `gh` call cannot exit before the one stdout line is printed. |
| 21-27 | Arguments: repo path (default `.`), branch (default the current branch) | changed | One argument, the pull request number or URL; the checkout is always the current directory. A branch is not needed because the pull request number names exactly one pull request. |
| 29-32 | Detached-`HEAD` guard | dropped | No branch is read. A missing or bad argument prints `UNKNOWN reason=usage`. |
| 34-45 | Parse `origin` into `owner/repo` (strips `.git`, `git@github.com:`, `https://github.com/`, `ssh://git@github.com/`) | kept as is | Same parse. A URL argument for another repo is refused (section 4.2). A failed parse prints `UNKNOWN reason=no_origin`, one stdout line instead of a stderr line. |
| 47-48 | `gh pr list --repo "$GH_REPO" --head "$BRANCH" --state all --json number,state,mergedAt,url`, errors swallowed | changed | `gh pr view <N> --repo <R> --json ...` with the extra fields the settle steps need (section 4.2). Errors are no longer swallowed: "no such pull request" is `NONE`, any other failure is `UNKNOWN`. |
| 50-63 | Embedded `python3`: parse the JSON, treat bad JSON as no pull request, `NONE` with exit 3 | changed | `jq` replaces `python3` (D1). Bad JSON is `UNKNOWN reason=bad_json`, not `NONE`, because "I could not read it" and "there is none" are different facts. |
| 64-66 | Prefer a merged pull request when several share a head | dropped | A pull request number names one pull request. |
| 67-78 | Map state: MERGED prints `MERGED PR #n url` exit 0; OPEN exit 1; anything else `CLOSED` exit 4 | kept as is | Same tokens and the same exit codes (0, 1, 4). The line gains key=value fields (section 4.3). |
| 79-80 | Capture the heredoc's exit status | dropped | No heredoc. |
| 82-84 | Print the three-dot diffstat of `<origin/HEAD>...HEAD` as evidence for a person | changed | Still evidence only, and still never part of the verdict. It becomes the held-versus-merged comparison, printed as one `match=` field (section 4.4), because the issue asks to compare what merged with what the pull request held. |
| 85 | `exit "$status"` | kept as is | Exit code equals the verdict. |

### 2.3 What our version adds, because the issue asks

These are the only additions. Each answers a line of the issue's acceptance criteria (section 13).

- `scripts/settle.sh`: the three settle steps for the issue, the entry and the task (section 5).
- `templates/closing-note.md` and `templates/result.md`: the one note and the fixed-shape result (sections 3.3 and 5.2).
- The never-as-worker entry, the registration edits and the tests (sections 9 and 10).
- The Apache-2.0 notice in the adopted files (section 7).

## 3. Contract

### 3.1 The command line

```text
/sc:closeout <PR> [--issue <N>] [--dispatch <id>] [--entry-key <key>]
```

The command file follows the layout of `src/superclaude/commands/issue.md`: frontmatter (`name`, `version`, `description`, `category`, `complexity`, `mcp-servers`, `personas`, `argument-hint`, lines 1-10), a short summary, Triggers, Usage, Options, STOP rules, Examples, Outputs, Boundaries with Will and Will Not, Activation (lines 104-110) and Related Commands. Its Activation says `> Skill sc:closeout-protocol` and that the command file alone is not enough, as `issue.md:106-110` says for `/sc:issue`. The installer keeps a protocol skill installed when its command names it by that line (`src/superclaude/cli/install_skills.py:40-59`).

| Argument | Required | Meaning |
|---|---|---|
| `<PR>` | yes | A pull request number (`661` or `#661`) or its URL. The repo is always the `origin` repo (D4); a URL for another repo is refused. |
| `--issue <N>` | no | The issue to settle, when the pull request names none or more than one. |
| `--dispatch <id>` | no | The worker's Dispatch id. Used only to find the worker's task. |
| `--entry-key <key>` | no | The work report entry key. Default: `<owner>__<repo>__<issue number>`, the key format of the orchestrator design (`docs/designs/orchestrator.md` on the 655 branch, line 458). |

There is no `--repo`, `--dry-run`, `--close` or `--unattended` flag: the issue lists none, and `/sc:issue` has none of the first two either (`commands/issue.md:46`). The three optional flags exist only because the brief lists those inputs for the orchestrator; each one only replaces a lookup the skill makes itself. A hand run needs the pull request and nothing else.

STOP rules, checked before Activation: no `<PR>`; a `<PR>` that is neither a number nor a URL; an unknown flag; a flag with no value; a repeated flag. Each prints the usage block and stops with no write.

### 3.2 What the orchestrator passes, and what a hand run needs

| Input | From the orchestrator | A hand run |
|---|---|---|
| The pull request | the number it merged in wave 7, or found already merged by a person | typed |
| The issue | the issue it is working (`--issue`) | found from the pull request's closing references and body (section 4.4) |
| The worker's Dispatch | the Dispatch id in its state file (`--dispatch`) | none: the task is found by its title `<owner>/<repo>#<N>` (section 5.4) |
| The entry key | its `<key>` (`--entry-key`) | derived from the repo and the issue number |

The caller must run it inside a checkout of the `origin` repo (wave 1 of the orchestrator already runs from `<checkout>`), with `gh` logged in, `git` and `jq` on the path. `orca` and a bound Orca Run are needed only for the task item; without them that item is `escalated` and nothing else changes.

Where the orchestrator calls it: after the merge (wave 7) and after the orchestrator's own close of the issue, if its wave 8 still has one, and before the report refresh. The exact wave 8 text is the 655 side's. Both orders are harmless: a closed issue is left alone and an entry already moved is `already_final` (section 6). The orchestrator may call it as a skill (`Skill sc:closeout-protocol`) or call the scripts itself, in this order, with the same result:

```text
branch-landed.sh <PR>                              one line, exit 0 only for MERGED
settle.sh issue  <PR> [--issue N] [--what TEXT] [--match M]    one line
settle.sh entry  --key <key> [--match M]                       one line
settle.sh task   [--dispatch ID | --title T] [--match M]       one line
settle.sh check                                                reads the three lines on stdin
```

`--match` carries the `match=` value of the `MERGED` line. With `differs`, each step prints `escalated why=merge_differs` and writes nothing (section 4.4), so the rule lives in the script, not in a model's reading.

A skill inside a skill is itself UNVERIFIED (risk K17 of the orchestrator design, `docs/designs/orchestrator.md` line 891; U6 below), which is why the scripts carry every decision and the skill adds only the note's sentence and the printing (D6).

### 3.3 The result

The result is printed last, also after a stop, as one YAML block (the style of the return contract of `sc-issue-protocol`, `SKILL.md:105-150`). `templates/result.md` holds its fixed shape.

```yaml
closeout:
  pr: <number or null>
  status: complete | partial | stopped
  verdict: MERGED | OPEN | CLOSED | NONE | UNKNOWN
  merged_by: <name or null>
  merge_commit: <first 7 characters or null>
  match: same | differs | unchecked | null
  pr_links_issue: closing | refs | none | null
  issue: {number: <number or null>, status: <word>, detail: <token>}
  entry: {key: <key or null>, status: <word>, detail: <token>}
  task:  {id: <id or null>, status: <word>, detail: <token>, dispatch: <state read or null>}
  escalations: ["<item>: <one sentence: why not, and the one next step>"]
  stop: <STOP code or null>
```

- `<word>` is one of the four final status words (section 5.1).
- `status: complete` means no item is `escalated`. `partial` means at least one is, and each has its sentence in `escalations`. `stopped` means the verdict is not `MERGED` or a STOP code fired; no item was written, the three items print `null` and `stop` says why.
- A person sees the block printed. The orchestrator records it in the entry and in its state file. The same block is the only output; there is no second summary.
- The block never names the agent or the model (D8, section 10 row 6).
- The check: before printing, `settle.sh check` reads the three item lines. An item with no status word, or `escalated` with a `why` token that has no sentence in the table of section 5.6, makes it print `CHECK_FAIL <item>` and exit 2; the skill then sets that item to `escalated` with `why=not_reached` and prints `status: partial`. An item is never silent.

### 3.4 STOP codes and the error table

| Scenario | Behaviour |
|---|---|
| Bad or missing arguments | The command STOPs with usage before Activation. |
| No `origin`, or `origin` is not GitHub (`UNKNOWN reason=no_origin`) | STOP `E-NO-ORIGIN`. |
| A URL naming another repo (`UNKNOWN reason=foreign_repo`) | STOP `E-FOREIGN-REPO`. |
| `gh auth status` fails | STOP `E-GH-AUTH`, before any other call. |
| `jq` missing (`UNKNOWN reason=no_jq`) | STOP `E-NO-JQ`. |
| Verdict `OPEN`, `CLOSED` (closed without merge), `NONE` or `UNKNOWN` (`gh_failed`, `bad_json`) | STOP `E-NOT-MERGED` with the verdict in the message. No write. The result says `stopped`. |
| Verdict `MERGED` with `match=differs` | No STOP. All three items are `escalated` (`why=merge_differs`); nothing is written. The result says `partial`. |
| `gh issue close` fails | No STOP. The issue item is `escalated` (`why=write_failed`) and the run goes on to the other two items. |
| The entry command is absent, or the task cannot be reached | No STOP. That item is `escalated` with its reason. |

The word "STOP" here means the skill ends after printing the result block; it never asks the person a question (a stop that asks would hold the orchestrator).

## 4. The truth check script

`scripts/branch-landed.sh <PR>` is Jay's script, adapted (section 2.2). It is the only place that decides whether a pull request merged and what merged. It changes nothing: its only write is `git fetch`, which touches objects and `FETCH_HEAD`, never a branch, the index or the working tree.

### 4.1 The order, and what it never does

1. **Arguments and origin.** Check the argument and parse `origin` into `owner/repo` (Jay's lines 34-45, kept). A URL for another repo is refused.
2. **State.** One read: `gh pr view <N> --repo <R> --json number,state,mergedAt,mergedBy,mergeCommit,baseRefName,headRefOid,commits,url`. The verdict comes from this and nothing else.
3. **Held versus merged, only for `MERGED`.** A three-dot comparison against the base (section 4.4). It sets `match=` and never the verdict. If any step of it fails, `match=unchecked`.

It never uses commit ancestry (`git merge-base --is-ancestor`, `git branch --merged`, `git rev-list`, `git log` ranges) and never a two-dot diff of a branch tip against the base. Reason, from Jay's header (`branch-landed.sh:4-9`): a squash merge rewrites the commits and the branch is deleted, so ancestry calls every landed branch abandoned.

### 4.2 Arguments

`<PR>` is a number, `#<number>` or `https://github.com/<owner>/<repo>/pull/<number>`. Only the number is used. For a URL, the owner and repo in it must equal `origin`'s, else `UNKNOWN reason=foreign_repo`. Every `gh` call carries `--repo <R>` (the fork-safety scan of `tests/skills/test_issue_worker_agents.py:45` is applied to the script and the skill). The script reads no stdin and asks nothing, as `finish-merge.sh` states (line 28).

### 4.3 Results: tokens, exit codes, one stdout line

Exactly one stdout line. The first word is the token; the rest are `key=value` fields separated by one space, and no value has a space. Details go to stderr only (the style of `finish-merge.sh:20-24`, whose failure is one token and exit 2).

| Case | Stdout line | Exit |
|---|---|---|
| State `MERGED` | `MERGED pr=661 by=<login or unknown> merge=<40 hex> base=<branch> head=<40 hex> match=<same, differs or unchecked> url=<url>` | 0 |
| State `OPEN` | `OPEN pr=<N> url=<url>` | 1 |
| Not readable, bad arguments, no origin, another repo, no `jq`, a bad JSON answer | `UNKNOWN reason=<usage, no_origin, foreign_repo, no_jq, gh_failed or bad_json>` | 2 |
| `gh` says there is no such pull request | `NONE pr=<N>` | 3 |
| State `CLOSED` | `CLOSED pr=<N> url=<url>` | 4 |

The five tokens and the exit codes 0, 1, 2, 3 and 4 are Jay's (`branch-landed.sh:14-16,30,42,63,72,75,77`). Exit 0 only for `MERGED`, as in line 16. Today `gh` answers a missing pull request with `GraphQL: Could not resolve to a PullRequest with the number of 999999` and exit 1 (command run 2026-11-19); the script maps that text to `NONE` and every other failure to `UNKNOWN reason=gh_failed`. A closed pull request that was not merged has state `CLOSED` and `mergedAt` null (PR 663 on this repo is one).

### 4.4 The held-versus-merged comparison

The question: is what the merge changed the same set of files that the pull request held? The check compares file names, not contents, because a squash merge on a moved base can legitimately differ in content from the head.

1. `git fetch --quiet origin <base> refs/pull/<N>/head`. GitHub keeps `refs/pull/<N>/head` after the branch is deleted: read 2026-11-19, the branch of PR 660 is gone from `origin` and `git ls-remote origin refs/pull/660/head` still answers; the same holds for the 11 other merged pull requests checked.
2. `held` is the three-dot diff against the base as it was just before the merge: `git diff --name-only <merge>~K...<head>`, where `<head>` is `headRefOid`.
3. `merged` is the change the merge made, one commit at a time: for each of the K newest commits `c` on the base, `git diff-tree -r --name-only <c>^1 <c>` (a commit against its own first parent, which is exact and is not the stale-branch comparison Jay warns of at `branch-landed.sh:18`). The union is `merged`.
4. `K` is 1 for a squash merge or a merge commit. If the sets differ and the pull request has more than one commit (`commits` in the state read), the script tries `K` equal to that number, which is what a rebase merge leaves. Equal sets give `match=same`; otherwise `match=differs`. Any failed step gives `match=unchecked`.

Checked on this repository, read-only, 2026-11-19: the steps above (with `K` = 1) were run by hand over the 12 newest merged pull requests (PR 649 to 667): 8 squash merges (one parent) and 4 merge commits (two parents), 1 to 9 commits each, 2 to 181 files. All 12 gave equal sets (`same`). No rebase merge was among them, so the second try is untested (U2).

What `match` changes: `same` and `unchecked` change nothing. `differs` stops the writes: each `settle.sh` step, given `--match differs`, prints `escalated why=merge_differs` and writes nothing (decision D17, section 1.3; the sentence is in section 5.6). Reason: the first line of the issue is that closeout "checks that what merged is what was asked for"; closing an issue over a merge that is not what was asked would be the wrong write.

### 4.5 The cases of the issue's Test plan

Each case is run in a scratch repository with a fake `gh` (canned JSON) and a recording `git` that forwards to the real one (section 10).

| Case | State read | Expected line (shape) | Exit | Note |
|---|---|---|---|---|
| Squash merge | `MERGED`, one parent, branch deleted | `MERGED ... match=same` | 0 | The original commits are not in the base history; the verdict is still `MERGED`. |
| Merge commit | `MERGED`, two parents | `MERGED ... match=same` | 0 | `K=1`; `merged` is the diff against the first parent. |
| Rebase merge | `MERGED`, one parent per rebased commit | `MERGED ... match=same` (via the second try) | 0 | UNVERIFIED which commit GitHub reports as the merge commit for a rebase (U2). |
| Not merged | `OPEN` | `OPEN pr=<N> url=<url>` | 1 | No fetch is run. |
| Closed without merge | `CLOSED`, `mergedAt` null | `CLOSED pr=<N> url=<url>` | 4 | No fetch is run. |
| Merged by a person | `MERGED`, `mergedBy` a person's login | `MERGED ... by=<login> ...` | 0 | The script does not care who merged; the field only carries the login. |
| No such pull request | `gh` error text above | `NONE pr=<N>` | 3 | Added; it is Jay's `NONE` token. |
| Unreadable | `gh` fails, or its answer is not JSON | `UNKNOWN reason=gh_failed` or `bad_json` | 2 | Added; Jay's `UNKNOWN`. |

In every case no recorded `git` call is `merge-base`, `--is-ancestor`, `branch --merged`, `rev-list` or `log`, and the only diff that names the head is the three-dot one.

## 5. Settling the three items

`scripts/settle.sh` has three steps, `issue`, `entry` and `task`, plus `check`. Each step reads the current state first and writes only if the state is not already final. Each prints one stdout line (`ISSUE`, `ENTRY`, `TASK`), exit 0 when the status is `settled`, `already_final` or `none_found`, exit 1 when it is `escalated`, and for bad arguments `SETTLE_FAIL <reason>` with exit 2 (the failure style of `finish-merge.sh:43-48`). The line is `<ITEM> <status> <key>=<value> ... how=<token>` or `... why=<token>`; the result's `detail` is that `how` or `why` token. Statuses come from the tables below, not from a model (D6).

### 5.1 The four final status words

| Word | Meaning | Written by this run? |
|---|---|---|
| `settled` | The item is now in its final state because of this run. | yes |
| `already_final` | The item was already in its final state; nothing was written. | no |
| `none_found` | The surface was reachable and holds no record for this pull request, so there is nothing to settle. | no |
| `escalated` | The item could not be settled. A reason token and one sentence say why and give the one next step. | no |

`none_found` is a stated result, not a skip: it says the place was looked at. A surface that could not be looked at is `escalated`, never `none_found`. This is the rule that keeps a hand run on an ordinary pull request honest: with no Orca Run or no report command, those items say so.

### 5.2 The issue (`settle.sh issue <PR> [--issue N] [--what TEXT]`)

1. **Which issue.** `--issue`; else the one issue in the pull request's `closingIssuesReferences`; else the one distinct number in a `Fixes`, `Closes`, `Resolves`, `Refs` or `#N` mention of the pull request body. None: `escalated why=no_issue_named`. More than one: `escalated why=several_issues`. The number of the pull request itself: `escalated why=not_an_issue`.
2. **The link is checked.** `links=closing` when the issue is in `closingIssuesReferences` or the body has a closing keyword for it; `links=refs` when the body mentions it without one; `links=none` when it appears nowhere (possible only with `--issue`). The value is in the line and the note.
3. **Read, then write.** `gh issue view <N> --repo <R> --json state,stateReason`. `CLOSED`: `already_final how=already_closed`, with `reason=<stateReason>` read as data (`COMPLETED` for issue 651, read 2026-11-19); no write, no note, and the issue is never reopened (D7). `OPEN`: one call, `gh issue close <N> --repo <R> --reason completed --comment <note>` (both flags verified in `gh issue close --help`, 2026-11-19), then a read back. Closed now: `settled how=closed_now`. Not closed after the call: `escalated why=write_failed`.
4. **An open issue is closed whichever the link is**, because the issue's acceptance row 3 says an issue the merge did not close is closed. `links=refs` and `links=none` are stated in the note, so a person who disagrees can reopen it.
5. **The note** (`templates/closing-note.md`, stub first, slots filled by the script): "Closed after pull request `<owner>/<repo>#<PR>` merged on `<date UTC>` by `<name>`, commit `<7 characters>`. `<what>` The pull request `<closes this issue with a closing keyword | names this issue without closing it | does not name this issue, so this note is the link>`. Status: completed (merged)." Only `<what>` is written by judgment: one plain sentence from the pull request's files and the issue's goal, 25 words at most. Without `--what` the script writes "`<n>` files changed." The title of the pull request is not quoted (D8).
6. **Names.** `<name>` is the `name` of the merger's public profile (`gh api users/<login> --jq .name`, which returned `Ironbelly` for the account that merged PR 661 on 2026-11-19), else the login. A merger GitHub does not report is written "someone GitHub does not name". The agent and the model are never named; the scan of section 10 covers the note, the line and the result.

### 5.3 The work report entry (`settle.sh entry --key <key>`)

What exists today, read on 2026-11-19: no `superclaude orchestrator` command is in `src/superclaude/cli/` on this base and `report-entry` and `orchestrator_repo` appear nowhere under `src/`. The `agent-work-report` skill is in the IronFlow repo (`.claude/skills/agent-work-report/`), where `.dev/coordinator/` holds runs, priorities, settings and a report page but no `orchestrated/` folder. That skill says every open item of the previous report is listed again or closed "with a reason the source confirmed" (its `SKILL.md`, "Nothing silently dropped"). The per-issue entry files and the command that closes one are the orchestrator design's (`docs/designs/orchestrator.md` on the 655 branch, lines 484 and 520: `superclaude orchestrator report-entry --key <key> --closed` "moves the entry file to `orchestrated/closed/`"), built in the orchestrator's pull requests, and the skill's move into IronClaude is its piece C.

So the interface this skill uses is one command and nothing else, and it never edits a report file itself (D10):

| Step | Result line |
|---|---|
| `superclaude orchestrator report-entry --help` fails or the command is not found (today, and until the orchestrator's pull requests land) | `ENTRY escalated key=<key> why=surface_absent` |
| Present: run `superclaude orchestrator report-entry --key <key> --closed`; its first stdout word `moved` | `ENTRY settled key=<key> how=moved` |
| first word `already_closed` | `ENTRY already_final key=<key> how=already_closed` |
| first word `no_entry` (the surface is reachable and has no entry for this key, for example a pull request nobody orchestrated) | `ENTRY none_found key=<key>` |
| a non-zero exit or any other first word | `ENTRY escalated key=<key> why=entry_command_failed` |

The first-word contract (`moved`, `already_closed`, `no_entry`; exit 0) is what this skill needs from that command. It is not yet written anywhere: UNVERIFIED, section 11, U1, and a requirement the orchestrator's pull request B has to meet or the skill adapts to what it prints. Before the move lands, with no entry present, the entry item is therefore `escalated` and its sentence says what to do by hand. When the orchestrator calls this skill, its own wave 8 call of the same command becomes a repeat and answers `already_closed`; the 655 side may then drop it. Draft part D says closeout "never writes the report state itself" and keeps the entry write in wave 8; this spec differs because the issue asks this skill to settle the entry, and the result is the same either way.

### 5.4 The worker's Orca task (`settle.sh task [--dispatch ID | --title T]`)

1. **Preflight.** `orca` must run, and `orca orchestration run-current --json` must show a bound Run (`result.run` is `null` when none is; shape read 2026-11-19). Else `TASK escalated why=no_orca` or `why=no_orca_run`.
2. **Find the task.** With `--dispatch`, the row of `orca orchestration worker-list --json` whose `dispatchId` matches gives its `taskId` (both fields read in the output of 2026-11-19). Otherwise `orca orchestration task-list --json` (it answers `run_required` when no Run is bound, read the same day) and the task titled `<owner>/<repo>#<N>`, the title the orchestrator gives it in wave 4 (`docs/designs/orchestrator.md` line 491). No match: `none_found`. A failed lookup: `escalated why=task_lookup_failed`.
3. **Read, then write.** A task already `completed` or `failed`: `already_final how=already_<status>`. Any other: `orca orchestration task-update --id <id> --status completed --result "merged <owner>/<repo>#<PR>"`; the statuses and `--result` are verified in `task-update --help` (valid: pending, ready, dispatched, completed, failed, blocked). Then a read back: `settled how=completed`. A failed write: `escalated why=write_failed`.
4. **Not touched, only read.** The worker's Dispatch and its terminal: no `worker-release`, `worker-stop`, `worker-abandon` or message to the worker (D15). With `--dispatch`, the `dispatchStatus` of its `worker-list` row (value `dispatched` seen on 2026-11-19) is printed as `dispatch=<state>` on the `TASK` line and nothing more. The task's `result` text holds no name.

The JSON field names of the task title and status are UNVERIFIED (U3); the fixture test of section 10 pins them once read from a real Run. Whether Orca already moves a task to `completed` itself when its worker finishes is UNVERIFIED (U4); the read-then-write step is correct either way.

### 5.5 "Completed" and "deployed"

- **Completed** means merged. It is the only status word this version writes for the issue and the task.
- **Deployed** means verified in the place it runs. This version never writes the word: no output of the skill or its scripts contains it (D9). The skill's instruction files define it so that nobody writes it by habit.
- **What will count as a recorded check**, for a later change the owner decides: a record that names what was checked (a health check or an installed version), where it runs, the result and the time in UTC, written by whoever ran it, in a file or comment the caller points to. The closeout would copy it and name its source. This version has no input for it, so the word is not written.

### 5.6 The escalation sentences

Each `why` token has one fixed sentence, so the same words come out whoever calls the scripts. The sentence goes in the result's `escalations` list as `"<item>: <sentence>"`.

| Item | `why` | Sentence |
|---|---|---|
| issue | `no_issue_named` | The pull request names no issue and none was passed. Run closeout again with `--issue <N>`. |
| issue | `several_issues` | The pull request names more than one issue. Run closeout again with `--issue <N>` for each. |
| issue | `not_an_issue` | The number given is a pull request. Run closeout again with the issue's number. |
| issue | `write_failed` | Closing the issue failed. Close it by hand: `gh issue close <N> --repo <owner>/<repo> --reason completed`. |
| entry | `surface_absent` | This install has no command that updates a work report entry. Check the entry for `<key>` by hand. |
| entry | `entry_command_failed` | The report entry command failed. Run it again by hand with `--key <key> --closed`. |
| task | `no_orca` | Orca is not available here, so the worker's task was not looked at. Settle it from a session that has the Run. |
| task | `no_orca_run` | No Orca Run is bound to this session, so the worker's task was not looked at. Settle it from the coordinator's session. |
| task | `task_lookup_failed` | The task could not be looked up. Run `orca orchestration task-list` in the coordinator's session and set it by hand. |
| task | `write_failed` | Setting the task failed. Set it by hand with `orca orchestration task-update --status completed`. |
| all three | `merge_differs` | The merge changed different files than the pull request held. Check it, then run closeout again. |
| any | `not_reached` | Closeout did not reach this item. Run closeout again. |

## 6. Two actors, one pull request

A person and the orchestrator can both settle one pull request: the person merged first, the orchestrator found it merged, or both ran closeout. A second run is harmless because of these rules, each one testable:

| Rule | What it gives |
|---|---|
| The truth check only reads. | Both runs reach the same verdict. |
| The skill keeps no state of its own: no file, no lock, no marker. All state is in the three surfaces, which each run reads first. | There is nothing to get out of step, and a run that stopped half way is finished by the next one. |
| Every write is read-then-write (`settle.sh`, section 5). An issue already `CLOSED` is not closed and gets no note; an entry already closed answers `already_closed`; a task already `completed` or `failed` is left. | The second run's lines read `already_final` and write nothing. |
| The note travels with the close, in one `gh issue close ... --comment` call. | No state with the issue open and a note posted, and none with the issue closed and no note. |
| The orchestrator's own wave 8 steps (its issue close, its `report-entry --closed`) are read-then-write too. | Either order of the orchestrator's steps and this skill gives the same final state (section 3.2). |
| A person who closes the issue, or merges, while a run is going only changes what the next read shows. | The writes are one call each, so nothing is half done. |

What a second run prints: the same block, with the items that the first run settled now `already_final`. The orchestrator may record it again without harm.

The one race left: both actors read the issue as open in the same second and both call `gh issue close ... --comment`. Whether `gh` posts the second comment on an already closed issue is UNVERIFIED (U5). The worst case is two notes and one close; nothing is lost or wrongly closed. The check is in section 11.

## 7. Notice

### 7.1 What Apache-2.0 asks of an adopted, changed file

Read from Jay's `LICENSE` (Apache License 2.0, 190 lines, blob 4b14cf3c9b, the same blob GitHub reports; the copyright line in its appendix is "Copyright 2026 Jay Wedgeworth", lines 178-190). Section 4, lines 89-128:

| Clause | Requirement | How this design meets it |
|---|---|---|
| 4(a) | Give every recipient a copy of the License. | `src/superclaude/skills/sc-closeout-protocol/LICENSE`: a byte-for-byte copy of Jay's file. The installer copies a skill folder whole (`src/superclaude/cli/install_skill.py:52`, `shutil.copytree`), so the copy travels with the skill. |
| 4(b) | Modified files carry prominent notices that they were changed. | A notice block at the top of each adopted file (7.2). |
| 4(c) | Keep every copyright, patent, trademark and attribution notice of the Source form. | Neither of Jay's two files has a notice of its own (the only copyright line is in `LICENSE`). The notice block names the copyright holder, the source and the licence, so it is kept in substance. If Jay adds a notice to either file before the build starts, the build copies it. |
| 4(d) | If the Work has a `NOTICE` file, carry its attribution notices. | Jay's repository has none (`contents/NOTICE` answers 404, 2026-11-19), so there is nothing to carry. |
| last paragraph | The adopter may add its own copyright to its changes and may license them differently. | The changes stay under this repository's own licence; no extra terms are added to Jay's parts. |

### 7.2 Where the notice goes

Same pattern as the vendored `ptytest` fork, which keeps its licence verbatim in its folder, records its source and changes in `PROVENANCE.md` and is listed in the root `NOTICE` (`NOTICE:8-30`, `src/superclaude/cli/eval/pty/PROVENANCE.md`).

| File | What it carries |
|---|---|
| `scripts/branch-landed.sh` | After the shebang, a comment block of five lines: "Adapted from `scripts/branch-landed.sh` in https://github.com/Simple-With-Us/AI-Fleet-Coordinator (commit b7f695084c, 2026-09-17), Copyright 2026 Jay Wedgeworth, licensed under the Apache License, Version 2.0. Changed by IronClaude: the input is a pull request number, the output is one line, `jq` replaces `python3`, and the held-versus-merged comparison is added. The full list of changes is in `PROVENANCE.md`." |
| `SKILL.md` | A two-line quoted notice directly under the title with the same source, commit (ec86182d70, 2026-11-05), copyright and licence, and "Changed by IronClaude: see `PROVENANCE.md`." It is visible text, not a hidden comment, so it is prominent. |
| `PROVENANCE.md` (skill folder) | The two source paths, the commits and the content hashes of section 2 (so a later drift review can compare), the date adopted, and the full statement of what was changed, which is sections 2.1 and 2.2 of this design in short form. |
| `LICENSE` (skill folder) | The licence text, verbatim. |
| `NOTICE` (repository root) | A new entry 2 under "Third-party components": the component, upstream URL, licence (Apache-2.0), location of the files, and a pointer to `PROVENANCE.md` and `LICENSE`. |

Files that are new and not derived from Jay's (`settle.sh`, the templates, the refs, the command file) carry no notice; `settle.sh` and the refs may say in one line that they work with the adopted script.

The notice and the statement of changes are checked by a test (section 10, row 10): both adopted files name the source, the copyright holder and "Apache License, Version 2.0", `LICENSE` equals Jay's blob by hash, and `PROVENANCE.md` lists every row of section 2 as kept, changed or dropped.

## 8. File layout

All paths are under `src/superclaude/` unless they start with `tests/`. Nothing here is created by this design; the build creates it after the owner approves.

```text
commands/closeout.md                          thin command, about 90 lines (section 3.1)
skills/sc-closeout-protocol/
  SKILL.md                                    frontmatter, notice, file table, waves, error table, Will Do, Will Not Do
  LICENSE                                     Jay's licence, verbatim (section 7)
  PROVENANCE.md                               source, pins, changes (section 7)
  refs/settle.md                              the status tables, the escalation sentences, the note's one sentence (judgment)
  refs/result.md                              the result block and the check; how the orchestrator calls the scripts
  templates/closing-note.md                   the note, stub first
  templates/result.md                         the fixed shape of the result
  scripts/branch-landed.sh                    adopted; the truth check (section 4)
  scripts/settle.sh                           new; issue, entry, task, check (section 5)
tests/skills/test_closeout_protocol.py        structure, scripts, words, names, hygiene
tests/commands/test_closeout_command.py       the command file
```

The pattern is `sc-issue-protocol`: a thin command that names the skill, a `SKILL.md` with a file table that a test checks in both directions (`tests/skills/test_issue_protocol.py:147`), lazy `refs/`, stub-first `templates/` and `scripts/` (`SKILL.md:24-53` of that skill). The headings of `SKILL.md`, in order: title and notice, Files of this skill, Repository and GitHub call rules, the waves, Return contract, Error handling, `## Will Do`, `## Will Not Do` (D2).

### 8.1 The waves of `SKILL.md`

| Wave | What it does | Where the work is done |
|---|---|---|
| 0. Intake | Read the arguments the command already validated; resolve `origin`; `gh auth status`; `jq` present. | `branch-landed.sh` (origin parse); `gh` |
| 1. Truth check | Run `branch-landed.sh <PR>`. `MERGED` goes on; any other verdict ends the run with the result block (`stopped`). | script |
| 2. Settle | Write the note's one sentence (judgment), then `settle.sh issue`, `settle.sh entry`, `settle.sh task`, in that order, each given the `match=` value as `--match` (with `differs` each step escalates and writes nothing). A step that escalates does not stop the next. | scripts, one judgment sentence |
| 3. Check and return | `settle.sh check` on the three lines; print the result block (section 3.3). | script, then printing |

### 8.2 The judgment, and everything else

Judgment is used in one place only: the one sentence of the note (`--what`). Every escalation sentence is fixed text in the table of section 5.6. Everything else is a script or a table, so the orchestrator can call the scripts directly and get the same words (D6, section 3.2). This is narrower than the issue allows (it also lets judgment decide an item's final status), on purpose.

### 8.3 Will Do and Will Not Do

Will Do: resolve the repo from `origin` only and pass it on every `gh` call; read the pull request state first and act only on `MERGED`; close an open issue once, with a note that names who merged, crediting people by name; settle the entry and the task by read-then-write, or escalate with the reason; print the result block last, also after a stop.

Will Not Do: merge, push, commit, stage or delete a branch or a worktree; use commit ancestry or a two-dot diff; write the word "deployed"; edit or delete any comment or text on GitHub, or reopen an issue; release, stop, abandon or message a worker or its Dispatch; write a report file by hand; name the agent or the model, or quote the pull request title; ask the person a question; start a worker agent; pass an Orca link flag, or call `orca` anywhere but in `settle.sh task`; print or write a secret.

The command file's Boundaries repeat the same two lists; a test checks they match (the pattern of `tests/skills/test_issue_protocol.py:601`).

## 9. Registration and the never-as-worker question

### 9.1 Files that change to register the command

From the issue's Components Affected and the accuracy check (rows 3 to 9, 11 and 19), each re-read on this base:

| # | File | Change |
|---|---|---|
| 1 | `src/superclaude/core/HOW-WE-WORK.md` | One row `/sc:closeout` in the `other-commands` block (open marker line 287, close marker line 301), placed between `/sc:agent` and `/sc:git` to keep the block alphabetical. The row says it settles a merged pull request, starts after a merge, never merges and is for a person or a coordinator, never a worker. |
| 2 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | A byte-for-byte copy of row 1's file (`tests/commands/test_routing_plugin_parity.py:38` compares them). Then run the level-table copy of CLAUDE.md "Key Documentation Files" and confirm `src/superclaude/core/CLAUDE.md` does not change, because the new row is outside the level-table block. |
| 3 | `tests/core/test_how_we_work_routing_table.py` | Add `"sc:closeout"` to `_OTHER_COMMANDS` (lines 27-35); the test at line 286 compares it to the block's members. |
| 4 | `tests/recommend/test_routing_refresh.py` | Add `"closeout"` to `_POST_REFRESH_ADDITIONS` (line 36) and extend the comment above it (lines 32-35, which name issues 323 and 302) with issue 668. |
| 5 | `docs/user-guide/commands.md` | A table row after `/sc:issue` (rows 102-106 hold the neighbours) and a section `### /sc:closeout` (neighbours: `/sc:issue` at line 305, `/sc:pr-submit` at 443, `/sc:sweep` at 545). |
| 6 | `CHANGELOG.md` | One line under `## [Unreleased]` (D16). |
| 7 | `NOTICE` | Entry 2 under "Third-party components" (section 7). |
| 8 | the four never-as-worker places | Section 9.3. |

Not changed, and why: `src/superclaude/commands/help.md` lists no command by name (accuracy check row 10); the plugin mirror holds no command or skill of this kind beyond the routing guide copy (rows 8 and 9); `src/superclaude/cli/install_skills.py` needs nothing, because a command whose `Activation` line names the skill keeps it installed (`install_skills.py:40-59` and the regression guard its docstring names in `tests/unit/test_cli_install.py`); `pyproject.toml` includes `src/**` already (lines 79-83); `src/superclaude/cli/main.py` registers no group, because there is no CLI group (D14); `src/superclaude/core/CLAUDE.md` changes only if the level-table copy says so (row 2).

### 9.2 Sync and the gate

`make sync-dev` copies the skill folder and the command into `.claude/` (the `sync-dev` target, `Makefile:109-121`) and `make verify-sync` must report no drift. `.claude/` is never staged (CLAUDE.md). The regression gate is the one the issue lists plus `make verify-deps`, which `.github/workflows/test.yml:123` runs and the issue's list leaves out: the parallel `pytest` run with `tests/cli/test_verify_sync_hooks.py` ignored, then that test alone, `make lint`, `uv run ruff format --check src/ tests/`, `make sync-dev` then `make verify-sync`, and `make verify-deps`. The build adds no dependency, so `make verify-deps` is expected to pass unchanged.

### 9.3 Does `/sc:closeout` go on the never-as-worker list?

**Yes (D12).** The list is the set of commands that are never dispatched as workers and get no `--unattended` mode (`src/superclaude/core/WORKER-CONTRACT.md:23`). `/sc:closeout` writes to GitHub (it closes an issue) and to the coordinator's own Orca task. A worker may not take outward actions (WC-9, same file, line 41), and a worker must not settle its own task. The caller is the orchestrator or a person, as with `/sc:issue` and `/sc:sweep`.

The list is pinned in four places, and all four change together in the same pull request:

| # | Place | Change |
|---|---|---|
| 1 | `src/superclaude/core/WORKER-CONTRACT.md:23` | Add `/sc:closeout` to the list, in alphabetical position (after `/sc:agent`). |
| 2 | `tests/skills/test_worker_contract.py:86-89` | The expected text of the term line gets `/sc:closeout` in the same position. |
| 3 | `tests/skills/test_worker_contract.py:462-470` | `NEVER_AS_WORKER` gets `"/sc:closeout"`. |
| 4 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:982` | The same list in prose. |

`NOT_CONVERTED_IN_P1` (`tests/skills/test_worker_contract.py:1331`) is not changed: `/sc:sweep` is on the never-as-worker list and not on that one, and the set-equality check at lines 817-825 already fails for any command with an `## Unattended mode` section that is not in `UNATTENDED_COMMANDS`, so `closeout.md` simply has none (D13). The test at line 1096 (`test_never_as_worker_check_fails_when_command_removed`) parametrizes over `NEVER_AS_WORKER` and proves the contract's term line must name each entry, so once row 3 is done the test fails unless row 1 is done too.

## 10. Tests

Two new files, as the issue lists them, in the style of `tests/skills/test_issue_protocol.py` and `tests/commands/test_issue_command.py`: `tests/commands/test_closeout_command.py` (the command file) and `tests/skills/test_closeout_protocol.py` (the skill, its files and the two scripts). The script tests run the real scripts in a scratch git repository with a fake `gh` and a fake `orca` first on `PATH`, and a `git` wrapper that records every call and forwards it to the real `git` (the approach of `tests/pr_submit/test_conflict_scripts.py`, whose header describes a `gh` stub first on `PATH` and `GIT_CONFIG_GLOBAL=/dev/null`). The fakes return canned JSON by pull request number and record every argument list. Nothing touches GitHub or a real Orca Run.

### 10.1 One row per line of the issue's Test plan

| # | Test plan line | Tests (file, what each asserts) | Passes when |
|---|---|---|---|
| 1 | **Structure** | `test_closeout_command.py`: frontmatter fields; the Options table lists exactly `<PR>`, `--issue`, `--dispatch`, `--entry-key` and no `--repo`, `--dry-run`, `--close` or `--unattended`; STOP rules come before Activation; the command is at most 100 lines; its Activation names `sc:closeout-protocol` and says not to proceed on the command file alone; no `## Unattended mode` section; no `src/superclaude/` path (as `test_issue_command.py:206`). `test_closeout_protocol.py`: frontmatter `name: sc:closeout-protocol` and `allowed-tools`; the headings `## Will Do`, `## Will Not Do` and `## Error handling` exist; the command's Boundaries match the skill's two lists (as `test_issue_protocol.py:601`); every path the skill names exists and every file in `refs/`, `templates/` and `scripts/` is named (as `test_issue_protocol.py:147`); every STOP code and every `why` token appears in the error table or in `refs/settle.md`, and the reverse. | all asserts hold |
| 2 | **Truth check**, with a fake `gh` and `git`: squash, merge commit, rebase merge, not merged, closed without merge, merged by a person | `test_closeout_protocol.py`, one test per case of the table in section 4.5, plus the multi-commit rebase, `NONE`, `UNKNOWN` (`gh` fails; not JSON), a URL for another repo, and a `differs` case. Each asserts the stdout line (one line only), the exit code, and that the recorded `git` calls hold none of `merge-base`, `--is-ancestor`, `branch --merged`, `rev-list`, `log`, and no diff that is not three-dot or `diff-tree`. For the squash case the test first proves `git merge-base --is-ancestor <head> <base>` is false in the scratch repo, so ancestry would have said "not landed". A source scan of both scripts finds none of those strings. For `OPEN` and `CLOSED` no `git fetch` is recorded. | each verdict is right and none uses ancestry |
| 3 | **Issue handling**: an issue the merge closed is not closed twice; an open one is closed with a note naming who merged; the body link is checked | (a) issue `CLOSED`: the line is `already_final`, no `gh issue close` is recorded. (b) issue `OPEN`: exactly one `gh issue close <N> --repo <R> --reason completed --comment ...` is recorded, the comment holds the merger's profile name, the PR number and the 7-character commit, and the line is `settled`. (c) `links=closing`, `links=refs` and `links=none` for a closing keyword, a plain mention and no mention (with `--issue`). (d) no issue named, several named, and the number of the PR itself: each `escalated` with its `why`, no write. (e) a second run with the fake's issue now `CLOSED` writes nothing. (f) a close that does not take (read back still `OPEN`) is `escalated why=write_failed`. | one close at most, the note is right, the link is read |
| 4 | **Words**: fails if "deployed" is written without a recorded check | Every stdout line of every script case, the rendered note and the rendered result are scanned, case-insensitively, for `deployed`: none. The note contains `Status: completed (merged)`. The instruction files contain the two definitions ("Completed means merged", "Deployed means verified in the place it runs") and the sentence that this version never writes the word. | the word is absent from everything written or printed |
| 5 | **Never in progress**: an item with no final status or escalation fails the check | `settle.sh check`: three good lines give `CHECK ok`, exit 0; a line with no status word, a missing item, and an `escalated` line with a `why` token that has no sentence in `refs/settle.md` each give `CHECK_FAIL <item>`, exit 2. A static test checks that `SKILL.md` wave 3 runs `check` before printing and sets a failed item to `escalated` with `why=not_reached`. | a silent item cannot pass |
| 6 | **Names**: no output names the agent or the model; people are credited by name | A list of the agent and model names is kept in the test file only. The note, every script line and the result are scanned for each name (paths such as `~/.claude/` are not output and are not scanned). The fake `gh api users/<login>` returns a name: the note holds that name; returns no name: it holds the login; the merger absent: "someone GitHub does not name". The fixture's pull request title contains an agent name and must not appear in the note (the title is never quoted). | no listed name appears, the person is named |
| 7 | **Hand run**: no orchestrator, no Orca Run | Full run in the scratch repo with no `orca` on `PATH` and no orchestrator files: issue `settled`, entry `escalated why=surface_absent`, task `escalated why=no_orca`, result `partial`, `git status` of the checkout unchanged. Then a fake `orca` whose `run-current` shows `run: null`: `why=no_orca_run`. Then a fake `orca` with a Run: the task found by dispatch and by title is set with the exact `task-update --id <id> --status completed --result "merged <R>#<PR>"`; a `completed` or `failed` task gives `already_final` with no write; no match gives `none_found`. Then a fake `superclaude orchestrator report-entry` answering `moved`, `already_closed`, `no_entry` and a failure: `settled`, `already_final`, `none_found`, `escalated why=entry_command_failed`. | works with no orchestrator and no Run; the result is one block |
| 8 | **Hygiene**: no em or en dashes; no secret printed or written | Every file of the skill folder, the command file and every captured output is scanned for U+2014 and U+2013: none. The scripts run with a canary value in `GH_TOKEN` and `CLICKUP_API_TOKEN`; the canary appears in no stdout, stderr or written file. No script or file holds a path starting `/home/` or `/Users/`. | zero dashes, zero canary, zero machine paths |
| 9 | **Changed tests**: `closeout` in `_OTHER_COMMANDS` and `_POST_REFRESH_ADDITIONS` | The two edits of section 9.1 rows 3 and 4. They are tests that exist; the proof is that `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py` and `tests/commands/test_routing_plugin_parity.py` pass with the new row and the byte copy. | those three files pass |

### 10.2 Tests this design adds for other lines of the issue

| # | Source line | Test |
|---|---|---|
| 10 | Acceptance row 9 (the notice and the statement of changes) | Both adopted files name the source URL, "Jay Wedgeworth" and "Apache License, Version 2.0"; the skill's `LICENSE` has the git blob hash 4b14cf3c9bae0ab156f3979e3e5d0048be2f7e23; `PROVENANCE.md` has one row for every row of sections 2.1 and 2.2 with `kept as is`, `changed` or `dropped`; the root `NOTICE` has entry 2. |
| 11 | Risks: fork safety | The fake `gh` records every call: each carries `--repo <origin R>` and none names `SuperClaude-Org`; the shared scan `gh_lines_missing_repo` (`tests/skills/test_issue_worker_agents.py:45`) finds no `gh` line without `--repo` in the skill files. |
| 12 | Will Not Do | A source scan: `orca` appears only in `settle.sh`; no `--issue` or `--pr` Orca link flag; none of `worker-release`, `worker-stop`, `worker-abandon`, `orchestration send`, `gh pr merge`, `git push`, `git commit`, `git add`, `gh issue reopen`, `gh issue edit`, `gh issue comment` or a `gh api -X` write appears in a script. The only writes recorded in any run are one `gh issue close` and one `task-update`. |
| 13 | Section 9.3 | The four never-as-worker places name `/sc:closeout`: the contract line, the expected text and tuple in `test_worker_contract.py`, and the developer guide line. The existing tests there cover the first three; one new static assert covers the guide. |

### 10.3 The regression gate

As section 9.2: run the two new files, then the gate before and after the change. A pass is every test green, no `ruff` or `make lint` finding, `make verify-sync` with no drift, and `make verify-deps` passing.

## 11. UNVERIFIED items

Each item is something this design relies on and did not read from a file or a command. The check settles it; until then the design's fallback applies.

| ID | What is unverified | Where it matters | The check that settles it | Fallback until then |
|---|---|---|---|---|
| U1 | What `superclaude orchestrator report-entry --key <key> --closed` prints and returns: the first-word contract `moved`, `already_closed`, `no_entry` with exit 0 (section 5.3). The command is the orchestrator pull request B's and does not exist on this base. | `settle.sh entry` | When pull request B has a candidate, run the command on a closed entry, an open entry and a missing key; compare to the table of section 5.3; either B matches the table or the table is changed to match B, before the build of this skill merges. | The entry item is `escalated why=surface_absent`. |
| U2 | Which commit GitHub reports as `mergeCommit` for a rebase merge, and that the second try (`K` = number of commits) gives `same` (section 4.4). The survey covered squash and merge commits only. | `branch-landed.sh` `match=` | In a scratch repository (never this one): a three-commit pull request, rebase-merged with the branch deleted, then run the script. Also one squash merge with an edit made in the merge dialog. | A wrong `differs` holds the three items as `escalated`; a person checks and runs again. The verdict is never affected. |
| U3 | The JSON field names for a task's title and status in `orca orchestration task-list --json`. | `settle.sh task` | In a throwaway Run, create one task titled `<owner>/<repo>#<N>` and read `task-list --json`; pin the names in the test fixture. | The task item is `escalated why=task_lookup_failed`. |
| U4 | Whether Orca moves a task to `completed` itself when its worker sends `worker_done`. | `settle.sh task` | In a throwaway Run, let a worker send `worker_done` and read `task-list` before any `task-update`. | None needed: read-then-write is correct either way. |
| U5 | Whether `gh issue close --comment` on an already closed issue posts the comment again (the race of section 6). | `settle.sh issue` | In a scratch repository, close one issue twice with `--comment` and count the comments. | The worst case is two notes and one close. |
| U6 | That a protocol skill can be called from inside a wave of another skill (risk K17 and U2 of the orchestrator design). | The orchestrator's call of this skill | The orchestrator's own end-to-end test (T1, and the closeout case its draft adds). | The orchestrator calls the scripts directly (section 3.2); the contract is the same. |
| U7 | What `mergedBy` holds when GitHub's auto-merge or a merge queue merged the pull request (for example `null` or a bot). | the note's "by" | Read `gh pr view --json mergedBy` on a pull request merged by auto-merge in a scratch repository. | A merger that is absent is written "someone GitHub does not name"; a bot's login is used as is (the profile of `github-actions[bot]` has a null name, read 2026-11-19, so the login is used). |
| U8 | How `orca` fails when Orca is not running, to tell `why=no_orca` from `why=no_orca_run`. | `settle.sh task` | With Orca closed, run `orca orchestration run-current --json` and read its exit code and text. | Any failure of `orca` before a Run is read is `no_orca`. |

Read and settled in this design (no longer unverified): `gh pr view --json` accepts `mergedBy`, `mergeCommit`, `closingIssuesReferences`, `commits`, `changedFiles`, `headRefOid` and `baseRefName`; `gh issue close` has `--reason completed` and `--comment`; `gh issue view --json stateReason` answers `COMPLETED` for a completed issue; `refs/pull/<N>/head` survives a deleted branch; `orca orchestration run-current --json` answers `run: null` with no Run, and `task-list` answers `run_required`; `worker-list` rows carry `dispatchId`, `taskId` and `dispatchStatus`; the held-versus-merged check gave `same` for 12 of 12 real merged pull requests.

## 12. Risks

### 12.1 Risks

| Risk | Mitigation | Section |
|---|---|---|
| A squash merge hides the original commits, so a check by ancestry says "not landed". | The verdict comes from the pull request state; the three-dot comparison is evidence; no code path or test uses ancestry. | 4 |
| "Deployed" is written when nothing was checked. | The word is never written; a test scans every output. | 5.5, 10 row 4 |
| A person and the orchestrator settle the same pull request. | The skill keeps no state; every write is read-then-write; the note travels with the close. One race remains (U5). | 6 |
| An item is left silently in progress. | Four fixed status words, fixed escalation sentences, and a check that fails an item with neither. | 3.3, 5.1, 5.6 |
| The work report entry surface is not in IronClaude yet. | One command is the whole interface; where it is absent the item is `escalated`, never skipped. Until the orchestrator's pull requests land, every hand run ends `partial` with that item and the task item escalated: truthful, and noisy by design. | 5.3 |
| The agent or the model is named in a note a person reads. | The note is fixed text with slots; the pull request title is never quoted; a scan of every output. | 5.2, 10 row 6 |
| The repository is public: a path or a secret leaks. | Repo-relative paths only, no secret read or printed, scans for both. | 10 row 8 |
| The task is set to `completed` while the worker still runs (a person merged first). | Only the task is set; the Dispatch is read and printed, never touched; wave 9 or a person releases it. | 5.4, D15 |
| `differs` is wrong and holds an issue open. | The write is only held, the cause is stated, a re-run settles it. 12 of 12 real pull requests gave `same`; the rebase case is U2. | 4.4 |
| An open issue is closed although the pull request only referenced it (`Refs`), so half-done work looks done. | The issue's acceptance row 3 requires the close; the note says the pull request did not close it; a person can reopen it. Draft part D asks the opposite default (its question AD-D1); the owner decides. | 5.2 |
| Jay's files change upstream. | `PROVENANCE.md` pins both files by commit and hash; nothing is fetched automatically. | 7 |

### 12.2 Where this spec differs from draft part D of the orchestrator design

Draft part D is an unmerged draft of the 655 side and is being cut down (the orchestrator's note of 2026-11-19). It was used only as a list of what wave 8 needs from `/sc:closeout`, which this contract meets: the inputs (pull request, issue, dispatch, entry key), the statuses of the issue, the entry and the task, a merge made by a person, one closing note, never merging or deleting, never naming the agent. It differs on purpose, so the 655 side can reconcile:

- No `--repo`, `--state-file`, `--orchestrator-repo`, `--close`, `--dry-run` or `--deployed-evidence` flag; three optional pass-through inputs instead (D4, section 3.1).
- No `superclaude closeout` Python package, no comment marker, no worker notice; two shell scripts (D14).
- The Dispatch is reported, not settled (D15). A pull request closed without merge stops the skill with no write; it does not set a task to `failed`.
- The report entry is settled by this skill through one command (D10); draft part D leaves it to wave 8.
- A merge whose held and merged files differ holds all three items (D17).

## 13. Coverage matrix

### 13.1 Acceptance Criteria of issue 668

| # | Acceptance Criterion (short) | Answered in | Proved by |
|---|---|---|---|
| 1 | `/sc:closeout <PR>` is a thin command whose Activation names `sc-closeout-protocol`; the skill has frontmatter, Will Do, Will Not Do and an error table | 3.1, 3.4, 8, 8.3 (D2) | 10 row 1 |
| 2 | The truth check reads the state first, then a three-dot diff; no ancestry; right verdict for squash, merge commit, rebase, not merged, closed without merge, merged by a person | 4.1 to 4.5 | 10 row 2 |
| 3 | An issue the merge closed is not closed twice; an open one is closed with a note saying what merged and who merged it; the body link is checked | 5.2, 6 (D7) | 10 row 3 |
| 4 | Never "deployed" without a recorded check; "completed" is for merged | 5.5 (D9) | 10 row 4 |
| 5 | The issue, the entry and the task each end with a final status or an escalation that says why; an item with neither fails the check | 3.3, 5.1 to 5.6 | 10 row 5 |
| 6 | No output names the agent or the model; people are credited by name | 5.2 step 6, 8.3 (D8) | 10 row 6 |
| 7 | Works with no orchestrator and no Orca Run; returns a short result an orchestrator records and a person sees printed | 3.2, 3.3, 5.3, 5.4 | 10 row 7 |
| 8 | No em or en dashes in the skill files; no secret printed or written | 1 (rulings), 10 row 8 | 10 row 8 |
| 9 | The adopted files keep Jay's Apache-2.0 notice and say what changed; the skill and script stay recognizably the adopted ones | 2, 7 | 10 row 10 |
| 10 | The command is registered where the repo lists commands; the regression gate passes | 9.1, 9.2, 9.3 | 10 rows 9 and 13, 10.3 |

### 13.2 The rest of the issue

| Issue part | Answered in |
|---|---|
| Proposed Solution points 1 to 6 (truth check, issue, two words, never in progress, merge by another, short result) | 1.1, 4, 5, 3.3, 6 |
| "The spec and the build start from those two files and change only what our setup needs" | 2 (every element of both files), 12.2 |
| Fix approach step 1: flags, truth check steps, result, how the orchestrator calls it and a person runs it, scripts versus judgment, what it writes where, the notice, the tests | 3, 4, 5, 8.2, 7, 10 |
| Fix approach step 4 and Components Affected: the registration list | 9.1 |
| Test plan (nine lines) and regression gate, including `make verify-deps` | 10.1, 10.3, 9.2 |
| Documentation Needs, including whether `CHANGELOG.md` needs an entry | 9.1 rows 5 to 7 (D16) |
| Whether `/sc:closeout` goes on the never-as-worker list; the four pinned places | 9.3 (D12) |
| The report entry surface before it moves into IronClaude; no entry present | 5.3 |
| Out of Scope (the 655 wave 8 text, additions A to E, the rest of Jay's repository, the merge itself) | 1.2 |
| Wave 8 of the orchestrator design: where it is called, what it needs and returns | 3.2, 3.3 |
| The skill heading names (`Will` against `Will Do`) | 1.3 (D2) |
| Where the spec file goes (`/sc:design` output flag) | header |

### 13.3 The brief's nine settle points

| # | Point | Section |
|---|---|---|
| 1 | Adoption table | 2 |
| 2 | Contract | 3 |
| 3 | Truth check script | 4 |
| 4 | Settling the three items; "completed" and "deployed" | 5 |
| 5 | Two actors | 6 |
| 6 | Notice | 7 |
| 7 | Registration and tests | 9, 10 |
| 8 | UNVERIFIED items and this matrix | 11, 13 |
| 9 | No extra behaviour | 1.3 (every row of section 2.3 answers a line of the issue) |
