# Protocol: planning a release or iteration from all open issues

Source: the planning run of IronClaude Iteration 3 and milestone rel-7.0.0 (Tuesday 24 November 4:18 PM to Wednesday 25 November, US Central), and the first day of running it (Thursday 26 November, to 11 AM Central). This document is the procedure that run followed, with every step, script, template, check, failure and rule that came out of it, written so that it can be turned into a skill. Facts about the run itself are in `PROCESS.md` (the dated record) and `SPEC-RELEASE-PLANNING-RUN.md` (the spec the run started from, with later changes). Where this protocol and the spec differ, this protocol is current.

Where the files are: this protocol and `PROCESS.md` are copied into IronClaude at `.dev/iterations/planning-protocol/`. The paths they name (`plan/`, `scripts/`, `templates/`, `cards/`, `qa/`, `logs/`) are in the planning run's folder, `.dev/research/release-planning-20261124/` in the private IronbellyOrg/IronFlow repository. The work files the run produced are in IronClaude at `.dev/iterations/iteration-3/`.

Status of this document: written from one run. Steps marked "worked" ran and passed their checks. Steps marked "changed" were corrected during the run. The write to GitHub (step 13) ran once, live, on 25 November. Steps 13a and 13b (release, hand-off and running the iteration) are written from the first day of running it. Nothing here is a claim about a second run.

## Contents
1. What the procedure produces and what it never does
2. Parameters
3. Roles, agents and skills
4. Rules that hold in every step
5. The procedure, step by step
6. The refresh procedure (when the issues change during the run)
7. Artifacts, scripts and templates
8. Mechanical checks and what each catches
9. Watchdog and failure handling
10. What went wrong and the rule each failure produced
11. Timings of the run
12. Turning this into a skill: design decisions and open questions
13. References to earlier work

## 1. What the procedure produces and what it never does
**Input:** a GitHub repository with open issues, a GitHub Project (board) with an Iteration field, an organization issue field called Priority, and optionally a milestone. **Output:** the proposal the owner approves, `plan/min50/EXPANDED-PROPOSAL.md` (built by step 6a), backed by `RECOMMENDATION.md` (decisions, dependencies, duplicates, left out, version check). Together they name:
- the issues to set to the current Iteration and milestone, grouped by theme, each theme with one person, every issue checked open on GitHub minutes before;
- the owner decisions that would unlock more issues, ranked by how many each unlocks, with a suggested answer;
- the split of work among the people;
- the dependencies, duplicates and overlaps found, the issues left out and why, the priority changes proposed, the version and branch check, and every item that could not be verified with the check that would settle it.

After the owner approves, a script writes the Iteration, the milestone and any approved Priority to GitHub, reads every value back, and logs it.

**Never:** write to GitHub before the owner approves; close, comment on, label or assign anything; decide for the owner (agents propose, with evidence, and the owner decides); trust an agent's "done" message instead of the file on disk; trust a worker's judgment without an independent check; print a key or token.

**Why it exists:** a backlog of 100 or more issues cannot be read by one reader (the run's issue bodies were 1.3 million characters). The procedure splits the reading across agents, makes every number come from a script, and puts an independent reviewer with live GitHub access between the plan and the owner.

## 2. Parameters
Ask for the repository, Project, iteration, milestone, people, minimum number of issues and owned areas at the start. Do not guess them. In the run, capacity was guessed and turned into "issues per person"; the owner rejected that twice (agents build, many in parallel).

**Model.** The skill runs on the tier 1a model (`claude-gw-tier1a`), set by the owner on 25 November. The orchestrating session must be on it; every agent the skill starts inherits the session model (no model override on any Agent call). If the session is on another model, the skill stops at step 0 and says so. This run was on tier 1b until 10:32 AM Central on 25 November and on tier 1a after; the owner then asked for a full re-review on tier 1a (`PROCESS.md` S14).

| Parameter | This run | Notes |
|---|---|---|
| Repository | IronbellyOrg/IronClaude | every `gh` call carries `--repo` |
| Project number and owner | 2, IronbellyOrg | board Status, Size, Iteration, Pipeline fields |
| Iteration | the current one (Iteration 3, 23 November to 6 December) | read the dates from the Project, never from memory |
| Milestone | rel-7.0.0 (number 1) | the owner named it; check it against the version rule (section 5, step 11) |
| People and shares | Ryan 3/8, Clay 3/8, Leandro 1/4 | asked, never guessed; people not named keep the issues they already hold |
| Minimum number of issues and capacity | at least 50 issues; "agents build, many in parallel"; window through 6 December | ask in the owner's units. Never estimate days or issues per person: the first plan did ("9 issues per person in two weeks") and the owner called it wrong. Size only orders the work |
| Owned areas | any ccsession work goes to Clay | areas the owner assigns to one person whatever the bucket or GitHub assignee says; applied as split rule 0 |
| Priority field | organization issue field (Urgent, High, Medium, Low) | read `gh api orgs/<org>/issue-fields`; the Project's own field list does not show it |
| Prior inputs | the owner's issue reviews, an earlier grouping by subject, the release procedure, earlier release plans | listed in step 1 |
| Time zone for every message | US Central | the owner's saved preference |
| Batch size | 14 issues per card worker | about 14 normal issues fit one worker; the three largest issues (70 to 140 KB each) need their own care |
| Worker agent and reviewer agent | `rf-analyst` and `rf-qa` | no model override: they inherit the session model, which must be tier 1a |
| Theme owners | one person per theme (bucket), in `plan/min50/theme-owner.tsv` | proposed by the orchestrator from the shares, confirmed by the owner; exceptions: owned areas, and an issue already assigned on GitHub to one of the people |

## 3. Roles, agents and skills
| Role | Who | What it does | What it may not do |
|---|---|---|---|
| Orchestrator | the main session | pulls data, runs scripts, starts workers with templated prompts, verifies every result from the file, fixes what checks find, writes the process record, presents to the owner | decide anything for the owner; write to GitHub before approval |
| Card worker (several in parallel) | `rf-analyst` | reads one batch of issues and the code, fills one card per issue: theme, kind, size, architecture change, hard dependencies, overlaps, holds, priority proposal, iteration fit, evidence | write anywhere but its card file and heartbeat; GitHub writes |
| Overlap agents (3 chunk agents and 1 scan agent) | `rf-analyst` | verify 28 listed pairs each (duplicate, overlaps, supersedes, related); the scan agent finds pairs nobody listed | close or edit anything |
| Merge agent | `rf-analyst` | groups all issues into buckets and writes the dependency map | invent facts: it uses cards and the overlap report only |
| Selection planners (2, blind to each other) | `rf-analyst` | each proposes a selection | read each other's file. Low value in this run: see section 12 |
| Debate orchestrator | the `/sc:adversarial` skill (agent `debate-orchestrator`) | compares the two selection plans and merges them | n/a |
| Decisions agent | `rf-analyst` | groups the issues that wait on an owner decision into the decisions that unlock them, with a suggested answer | decide; it only proposes |
| Re-check worker | `rf-analyst` | after a snapshot refresh, re-reads existing issues that changed and updates their cards | edit anything but those card fields and the change log |
| Independent reviewers (2) | `rf-qa` | re-check the recommendation and the decision list from the files and from live GitHub reads, with a verdict of PASS or FAIL | edit the work under review |

SC skills used: `/sc:adversarial` (compare two plans). Considered and not needed: `/sc:reflect` (it needs a driving spec and a tasklist), `/sc:impact` (no card needed a code dependents report), `/sc:release-split`, `/sc:roadmap`. No new agent was created; issue 731's signed consensus lists "a release-planner agent" as not needed, and this procedure is a skill with scripts and templates, not an agent.

## 4. Rules that hold in every step
1. **Files on disk are the only handover.** Every worker writes to a file and returns the path. The orchestrator reads the file; a message that says "done" is a signal to check, never proof.
2. **Stub first, then fill in place.** Every output starts as a stub made by a script from a template, with `{{RF_PLACEHOLDER:name}}` markers, and is filled section by section with Edit. Nothing large is written in one go. A worker never deletes or edits a heading line (two agents did, see section 10).
3. **Prompts are templated.** Every worker gets a prompt built from a template by a script. Parts, in order: role and boundary, read first, what you cover, definitions (a pointer, not a copy), steps, output, rules, heartbeat, return. The prompt says "fill the first item before reading further".
4. **Numbers come from scripts.** Tiers, counts, the split, the tables of the recommendation are generated from the cards by script. Hand-written text is limited to judgment (version check, open items, what happens after approval).
5. **A checker for every generated file.** A script validates enums, counts, cross-references and structure. A worker's file is not accepted until its checker passes (or the failure is logged).
6. **An independent reviewer with live reads.** The reviewer did not produce the work, re-computes everything, and reads GitHub live (issues, pull requests, branches). Blocking and minor findings are graded by consequence. At most 2 fix cycles, then escalate to the owner.
7. **Read-only until the owner approves.** The only GitHub writes are in the last step, by script, after approval.
8. **Evidence for every claim.** A file and line, an issue or pull request number, or a comment with author and time. Anything unproven is written UNVERIFIED with the one check that would settle it.
9. **Plain English, no em or en dashes, times in the owner's time zone.** Every named thing is explained in a few words with its number or link.
10. **The world moves while you work.** Take snapshots with a time stamp, re-pull before the final step, and read the state of every pull request a card names (section 6).
11. **Log as you go.** Every step, failure and fix goes into the process record at the time, with the rule it produced. This is how the protocol is kept honest.
12. **No time or capacity estimates.** Agents build, many in parallel, so people and days do not limit an iteration. Never write "N issues per person in N weeks" or a days total. What limits the list is an unanswered owner decision or an unfinished dependency. Size (XS to XL) only orders the work, easy first, and flags a large architecture change that needs the owner's explicit yes. If the owner sets a minimum number of issues, reach it by adding issues that wait only on a decision with a suggested answer (step 6a), not by lowering the bar for "ready".
13. **No closed issue ever reaches the owner.** Every list shown to the owner, and every list written to GitHub, is checked against GitHub minutes before by `scripts/live-check.sh` (state of every listed issue, issues edited since the snapshot, issues opened since). The proposal build refuses to finish if any listed issue is closed. A snapshot is never proof that an issue is still open.
15. **Open questions never gate work.** An open question on an issue is answered as part of doing that issue: by the recommended answer, or by the issue's owner at the start of the work when there is no recommendation. Never exclude, delay, stage or order an issue because a question is open, and never write "waits on the owner" or "after the owner answers". Order and staging come only from priority, hard dependencies, conflicts (shared scope, opposite aims, shared files) and complexity. A recommendation not to build an issue now, or a dependency on an issue that is left out, still keeps it out.
14. **Leave out what is too complicated; group by theme.** An issue with a large architecture change (for example the eval framework, #487), and every issue that waits on one, is left out of the iteration. It is never offered as an option to reach a number. Issues are grouped by theme (the buckets) and a whole theme goes to one person; balancing counts across people never splits a theme.

## 5. The procedure, step by step
Each step lists who does it, the command or script, the output, the check, and what to log. Every path is relative to the run folder (`.dev/research/release-planning-<date>/`). "Worked" means it ran in the run and its check passed.

**Step 0. Intake and the state of the repository (orchestrator; worked, changed).**
- Ask the owner for the parameters in section 2. Read the state yourself, never from memory: `gh api orgs/<org>/issue-fields` (Priority, Effort, Complexity, with option ids), the Project's iterations (GraphQL `projectV2.fields ... ProjectV2IterationField`), milestones (`gh api repos/<R>/milestones`), the default branch (`gh repo view --json defaultBranchRef`), the version (`pyproject.toml` on the default branch) and the latest tag.
- Log in `PROCESS.md`: the facts and what was corrected. The run said the Priority field had no options; it did (an organization issue field, invisible in the Project's own field list). The run also missed that the default branch had changed the night before; it was found only at the refresh.

**Step 1. Snapshot and prior inputs (orchestrator; worked).**
- `gh issue list --state open --limit 1000 --json number,title,body,labels,issueType,assignees,milestone,createdAt,updatedAt,comments,author,url` into `open-issues-raw.json`; `gh project item-list <N> --owner <O> --limit 600 --format json` into `board-items-raw.json`; organization issue field values per issue by paged GraphQL (`issueFieldValues`) into `field-values-raw.json`; parent and sub-issue links (`parent{number}`) into `parents.tsv`; the time into `PULL-TIME.txt`. Keep every snapshot (`snapshots/`).
- Collect prior work and list it in the process record: existing review comments on the issues (82 of 140 had a "Backlog review" comment with state, size, priority, dependencies), an earlier grouping by subject, the release procedure, earlier release plans and any draft of this skill (issue 731). Use them as inputs to check, never as facts.

**Step 2. Prepare inputs (script `prepare.sh`; worked).**
- Writes one input file per issue (`inputs/<N>.md`: body, the latest review comment in full, other comments cut at 2000 characters), `manifest.tsv` (issue, batch, starting group, title), batches of at most 14 issues grouped by subject (`batches/batch-NN.md`), a card stub per batch (`cards/batch-NN-cards.md`: machine data filled from the raw files, judgment fields left as placeholders) and a filled worker prompt per batch (`prompts/card-batch-NN.md`) from `templates/WORKER-PROMPT-TEMPLATE.md` and `templates/CARD-FILE-TEMPLATE.md`.
- Check: input files equal manifest rows; placeholders equal issues times judgment fields (18); no unresolved `@@` token.

**Step 3. Cards (10 `rf-analyst` agents in parallel; worked).**
- One agent per batch, one message to start all, one watchdog (section 9). Each fills 18 fields per issue: review check, theme, kind, still relevant, size, architecture change, hard depends on, blocks, soft related, overlap candidates, hold or blocker, priority proposal, priority change, priority evidence, iteration fit, fit reason, evidence read, UNVERIFIED.
- Check: `check-cards.sh` (every enum valid, one card per issue, every number named is an issue or pull request of the repository, evidence present for stale, hold and close-candidate). 134 of 134 cards passed in 17 minutes; the checker needed two fixes (section 10).

**Step 4. Duplicates and overlap (script, then 4 agents; worked, changed).**
- `check-overlap.sh pairs` builds `overlap/pairs.tsv` from three sources: overlaps the cards declared, issues that share three or more title words in a group, issues that link each other. 84 pairs. Three chunk agents verify 28 pairs each; a fourth scan agent looks only for pairs nobody listed, with a deliberate cross-check of issues filed on the same day by different people. `repair-overlap-headings.sh` restores headings that agents deleted. `check-overlap.sh merge` joins the four reports and `report` validates them.
- Output: 105 pairs, of which 70 overlap and 32 are only related. Real duplicates were rare (1 proposed close); most pairs are halves of one contract that need a link or a merged scope.

**Step 5. Buckets and dependencies (one agent, then scripts; worked).**
- `prepare-plan.sh merge`, one merge agent reads all cards and the overlap report, writes `plan/BUCKETS.md` (17 buckets, every issue once, ordered by priority, kind, size) and `plan/DEPENDENCIES.md` (every hard dependency as `- #A needs #B`). `check-buckets.sh` checks that every issue is placed once, the rows equal the cards, the order follows the rule, every card dependency is present (a path through other lines counts), and there is no cycle. `bucket-rows.sh` rewrites the rows from the cards after any card change.
- The agent was silent for 10 minutes while it read about 90,000 words; allow 15 minutes before any nudge.

**Step 6. Tiers (script `tiers.sh`; worked, changed).**
- Tier 1: fit `ready`. Tier 2: fit `needs-dependency` and every open dependency is in tier 1 or 2. Tier 3: fit `needs-decision`, or waiting behind such an issue. Tier 4: hold, too large, close candidate, already done, or depends on an issue that is itself left out. A link from an issue to its own parent is not a dependency, unless `plan/dependency-overrides.tsv` says the card names a real content dependency.
- Result of the run: ready 25, after a decision 68, left out 40, of 133.

**Step 6a. Expand to the owner's minimum (scripts `expand.sh`, `expand-report.sh`; worked, added after the owner said 25 was far too few).**
- Current form (`expand.sh S`, after the owner refused large changes): tier 1; tier 3 issues on a decision whose suggested answer is a go (A); tier 3 issues behind them (F); tier 3 issues whose decision has no suggested answer but that are small (XS, S, M) with no architecture change, each with one plain question (Q). Out: every large architecture change and what waits on it; every suggested answer that is "not now", or that leaves another owner ruling open, or whose chosen option needs a left-out issue (`not-now.tsv`, written by reading each answer against the card); an umbrella whose real sub-issue is out; every unmet dependency. Issues opened during the run are carded and added (`late-additions.tsv`). Result of the run: 51 issues (48 from the snapshot, 3 opened during the run), live-checked open.
- Earlier form, kept for the record: candidates were tier 1; tier 3 issues that wait on a decision with a suggested answer (wave A, no large architecture change; wave B, large architecture change, in only with the owner's explicit yes); tier 3 issues that wait behind other issues (wave F). A candidate stays in only if every issue it hard-depends on is also in (greatest fixpoint), so no chain has a missing link. Issues whose decision has no suggested answer, issues whose suggested answer is "not now" or does not settle them (`plan/min50/not-now.tsv`, written by reading each suggested answer, never by a keyword), and tier 4, are never candidates. An issue with a large architecture change is wave B whatever its fit; an issue that waits behind a B issue is B2.
- Output: `plan/min50/EXPANDED-A.tsv` and `EXPANDED-AB.tsv` (in or out, wave, decision, reason when out) and `plan/min50/EXPANDED-PROPOSAL.md` (counts, the decisions to say yes to with the suggested answer, the issues by person, the large changes to name, what is not proposed and why). Result of the run: without large changes 46, with them 62 (25 ready today); the first version said 49 and 70 and failed review (section 10, row 23).
- The proposal to approve is this file when the owner sets a minimum; the 25-issue list stays as its first group.

**Step 7. Owner decisions (decisions agent; worked, changed).**
- `prepare-decisions.sh` builds the stub and prompt. One agent groups every needs-decision issue under the single owner decision that unlocks it (46 decisions after review; the biggest unlocks 6 issues and frees 8 more). Each block: the question, who decides, where it is asked, issues unlocked, issues also freed, suggested answer, the effect of the other answer, evidence. `check-decisions.sh` checks that each needs-decision issue is on exactly one "unlocks" line.
- A decision is only a proposal. The independent review found one decision that the owner had already answered on GitHub (the plugin pin): see section 10.

**Step 8. Split among people (script `split.sh`; worked).**
- Theme mode (the current form, `THEME=plan/min50/theme-owner.tsv`): each theme (bucket) has one owner; every issue goes to its theme's owner, except ccsession work (Clay), an issue held by someone outside the three, and an issue already assigned on GitHub to one of the three (it stays with that person; the work may already be claimed). No balancing across themes. The shares follow from which themes each person owns (in the run: Ryan 17, Clay 20, Leandro 12, swill-ib 2, with the issues opened during the run).
- Earlier form, by issue: rules in order: rule 0, work in an area the owner assigned to one person (here any ccsession work, found by the title) goes to that person even if GitHub shows another of the three, unless someone outside the three holds it; an issue already assigned to one of the people keeps that person (an issue held by someone else is listed and not counted); an issue written by the owner or a named person goes to its author (one person wrote 78 percent of the issues, so that person's authorship says nothing); otherwise by area (bucket); then balance the shares by moving area-assigned issues, smallest first, separately for the set-now list and the decision list. Output `plan/SPLIT.tsv`.

**Step 9. Build the recommendation (scripts; worked, changed).**
- `rec-fragments.sh` (set-now table, split, dependencies, buckets, duplicates, left out, already set, priority changes), `rec-decisions.sh` (the decision table, no cell cut), hand-written fragments for the version and branch check, the open items and what happens after approval, `rec-build.sh` puts them into the stub (`prepare-recommendation.sh`, `rec-fill.sh`). The template is `templates/RECOMMENDATION-TEMPLATE.md` (13 sections).

**Step 10. Independent review and the fix loop (2 `rf-qa` agents, live reads; worked, changed).**
- `prepare-qa.sh selection` and `prepare-qa.sh decisions` build a report stub and a prompt from `templates/QA-PROMPT-TEMPLATE.md`, `QA-REPORT-TEMPLATE.md` and the check lists `QA-CHECKS-SELECTION.txt` (12 checks) and `QA-CHECKS-DECISIONS.txt` (7 checks). The reviewers re-compute counts, test every card against the list, read GitHub live, and grade findings blocking or minor. Corrections are made with `card-set.sh` (one field of one card, old and new value logged in `cards/corrections.md`), the recommendation is rebuilt with `rec-build.sh`, and a fresh reviewer runs round 2. At most 2 fix cycles.
- Round 1 failed both reports, each with a real blocking finding (section 10).

**Step 11. Version and branch check (orchestrator; worked).**
- Report the default branch, the versions on each branch, the latest tag, the commits each side is ahead, and the owner's release rule. Apply the repository's version rule to the chosen milestone name: here a MAJOR version means breaking changes, none of the selected issues was breaking by the cards, so the next release by the rule is a MINOR version; the milestone name stays the owner's choice.

**Step 12. Present to the owner (orchestrator; worked in part).**
- First run `scripts/live-check.sh` on the exact list (the proposal build does this and refuses on a closed issue). Card every issue opened since the snapshot (`cards/late-additions.md`, same 18 fields) and either add it (`plan/min50/late-additions.tsv`) or list it as not proposed with the reason. Then one message: the counts; the issues by person and theme; the decisions to accept; what is left out and why; the link to the file; one question with one line per answer. Never present a list the independent review has not passed, unless the message says the review is still running. The owner answers, changes or rejects. Record every change in `PROCESS.md` and in this protocol (section 10) before acting. Recompute by script after the owner's decisions.
- Every question to the owner says what the thing is (each issue named with what it does), why the owner's input is needed, and what I recommend, with one line per answer. A bare pair of issue numbers is not a question (failure row 31).

**Step 12a. Work map for the agent teams (script `work-map.sh`; worked, reviewed).**
- Lays the approved list out as epic (one per person, with a goal), feature (a subject) and story (an issue), in work order, in `plan/work-map/WORK-MAP.md` for people and `work-map.json` for agents. No GitHub issue is made for an epic or a feature. Per story: priority, size, complexity, start condition, lane (what runs in sequence and what in parallel), what it needs first, what it unblocks, overlaps and the scope to settle, open question or note. Between people: shared dependencies, shared work and shared files.
- Hand-written inputs, each with a reason: `epics.tsv` (goals, the owner confirms), `feature-order.tsv` (features that serve the goal first), `order-hints.tsv`, `story-overrides.tsv` (start conditions and notes the data files do not carry, for example "needs the owner's go per repo" or "fix already merged: confirm and close"), `cross-notes.tsv`, `questions.tsv` (every open question of every story with its recommended answer, or the named issue owner who settles it at the start of the work).
- Open questions (rule 15): every open ruling on a story's card or decision appears in `questions.tsv`, never only some of them. A recommended answer must be safe to act on as written: it never deletes, closes or overwrites live state without first reading what is there (round 2 found a recommendation that would have closed live Orca Runs with unread inbox messages). Where a story's two owners differ (a shared dependency or a shared scope), the map names both and says they settle it together; it never says "same owner" without comparing the two owners.
- Lanes: two stories share a lane when one needs the other or they must agree one scope; lanes run in parallel. Same-file collisions are not computed; known ones go in `cross-notes.tsv`, and the agent instruction says to compare changed files before running any two lanes at once.
- Before building it, re-read live state (merges since the snapshot): the first build showed two stories as work whose fix had merged minutes before (failure row 32). Independent review with check list `templates/QA-CHECKS-WORKMAP.txt` (8 checks). When the issue set or a rule changes, update the check list before the next review round: the round 3 checks still said 51 issues and the old order rule after the set had grown to 58.
- Review record in this run: round 1 FAIL (#837 shown ready, #540 and #555 already fixed), round 2 FAIL (#409 and #706 cross owners but shown as same owner, #755's unsafe recommendation, five open rulings missing), round 3 FAIL (agent instruction 3 still made five stories wait on the owner for an overlap with an issue outside the iteration; #755 could still close a Run with a running worker); both fixed and checked by script, no fourth review (two-fix-cycle limit), the owner decides on the fixes.
- Work files (step 12b) review record: round 1 FAIL (folder not in IronClaude; #442 gate text), round 2 FAIL (open pull requests on #834 and #702; #517 and #326 assigned to another login), round 3 FAIL (the continue-on-a-pull-request path missing from the agent's own steps); each fixed and checked by script, no fourth review, the owner decides. Lesson: every check the work files rely on must be read live (open pull requests, assignees, existing worktrees), and every instruction an agent needs must be in its own story file, never only in the lead's file.

**Step 12b. One work file per owner and one file per story (script `epic-files.sh`; worked, changed; three review rounds, then reviewer findings on pull request 853 fixed in the generator).**
- Why: an agent must never assemble its work from several documents or from issue comments. Comments are read by the claim only to check accuracy, and no skill reads GitHub "blocked by" links (owner, 25 Nov). The owner starts the epic by pasting the kickoff prompt of the owner's file into one lead session; the lead gives each story's agent its story file. The instruction is the prompt itself, so nothing can be missed.
- Per owner (`iteration-3/epics/<epic>-<owner>.md`): kickoff prompt; what the owner approves by starting it (claims, worktrees, commit and push of feature branches, pull requests through `/sc:pr-submit --monitor 3`; never a merge); epic goal; how the lead runs it; the lanes table (what starts now, what runs in sequence, lanes that cross owners); between people; the story workflow; every story in order.
- Per story (`iteration-3/stories/<issue>.md`, self-contained): facts, start check (`gh issue view <n> --json state` prints `CLOSED` for each prerequisite and for the story before it in its lane), shared-file check, plan approval (complex stories), decided answers word for word (and when the issue owner must answer at the start), scope note, settle lines with owners, expected route by type and complexity (the claim's chains), the agent's steps, and the result file.
- The story workflow is taken from the team's routing guide and the claim skill on the base branch, never written from memory: claim, decisions appended to `issue-summary.md`, the claim's next steps (brainstorm, design, plan, implement by complexity), read the plan and its check, implement with its final review, confirm, commit and push the feature branch, pull request, a person merges, closeout, next in the lane. While the claim's ship gate is in force (#442), claims run with `--pipeline none` in a worktree the lead made.
- Stories with no code change (confirm and close, file leftovers, live tests, measure only) get a route paragraph (`route-overrides.tsv`) that replaces the build steps.
- Checked by `scripts/check-epic-files.sh` against the map, with a negative test of ten deliberate breaks (all caught); then an independent review with `templates/QA-CHECKS-EPICFILES.txt` (8 checks). The GitHub "blocked by" links (`blocked-by.tsv`) are written in step 13 with the other approved writes.

**Step 13. Last re-pull and apply (script `apply-approved.sh`; worked: ran live 25 Nov, 116 writes, 0 read-back mismatches, plus 16 GitHub "blocked by" links from `blocked-by.tsv`, 0 missing on read-back).**
- Re-pull the open issues and compare with the snapshot: closed, opened, a decision gained or lost, a pull request merged or closed. Save the approved set as `APPROVED-LIST.tsv` (issue, iteration, milestone, optional priority). Run the script without arguments for a dry run (it prints every write it would make and skips an issue that is no longer open), then with `--apply`: for each issue it reads the current values, writes only what differs (Project Iteration by GraphQL, milestone by `gh issue edit`, Priority by `issue-field-values`), reads the value back, logs it in `apply-log.md`, retries a failed write once, and never stops the others.

**Step 13a. Release and hand-off (orchestrator; worked, changed).**
- Anything people must install (the claim change, the work files) counts as delivered only when it is on `master`: workspaces install IronClaude from `master`. Release `integration` into `master` with a release pull request (merge commit), then start the workspace image update (the Coder repo's IronClaude update check).
- The message to each owner (`plan/work-map/messages/<owner>.md`) says: pull `master`; update IronClaude first (`pipx install --force git+https://github.com/IronbellyOrg/IronClaude@master`, `superclaude install --force`, restart sessions); paste section 1 of your work file into one new lead session; what needs you along the way.
- A running lead reads its work file once. A change to the template after the start reaches it only when the owner tells the lead to pull `master` and re-read the section that changed.

**Step 13b. Running the iteration (one lead per epic, plus a helper session; worked on the first day).**
- One lead session per epic starts one agent per lane, each in its own Orca worktree with its story file as its prompt. One or two sessions cannot carry a whole epic: a second session (here the planning session) merges pull requests the lead marks "ready to merge" (every check green, every review comment handled, zero open threads) with a re-armed loop (`/tmp/e2-merge-loop.sh`), and answers agents that have stopped.
- No story stops for the owner, including for plan approval, unless something is ambiguous or two sources conflict. Questions that can be answered, or that have an obvious recommendation, are answered by the lead or the helper and recorded in the story's decisions (owner, 26 Nov). A report gives facts (what was found, what is left), never a bare state label such as "measure done".
- Review notes: an obvious small finding is fixed; a false alarm is answered with its evidence and resolved. Nothing is left open "on purpose", because an open thread blocks the merge.
- After typing into an agent's terminal, read the terminal back: answers were found left in input boxes unsent. Re-read a pull request's state just before acting on it.
- Before any outward action (filing an issue, stopping a task, opening a pull request), read what the owner already has running on it: the repo's recent issues and open pull requests, and the Orca terminals in its worktrees.
- After a merge: `/sc:closeout <pull request>` from an IronClaude checkout (the lead), then step 13 of the story workflow, the `/sc:worktrees retire issue-<N>` dry run, and `--apply` only when it says safe. Until IronClaude issue 881 lands, every finished worktree is kept, because each holds `.superclaude/` notes the cleanup script does not save.
- A pre-existing failing check on another repo (here Coder's 30 s test cap against a 75 s requirement) is merged past only with the owner's explicit word naming the failure, and gets an issue and a fix of its own.

**Step 14. Close the record (orchestrator).**
- Finish `PROCESS.md`: the final step list, timings, failures and fixes, and what to change in the skill.

## 6. The refresh procedure (when the issues change during the run)
The planning run takes hours and the issues change while it runs. In this run 6 issues were closed and 5 opened between two snapshots 16 hours apart, one issue was closed two minutes after the second snapshot, and three pull requests merged during the review. Treat the refresh as a normal part of the procedure.

1. **Drift check.** Re-pull the three raw files. Compare: closed since, opened since, existing issues with a later `updatedAt`, changed Priority or Complexity, changed board Status, Iteration or milestone. Also read the default branch again.
2. **Archive the closed.** `refresh-cards.sh` moves the cards of closed issues to `cards/archive-closed.md` (never deleted) and removes their rows from the buckets, their lines from the dependency file and their blocks from the overlap reports. Originals are kept in `snapshots/before-refresh/`.
3. **Cards for new issues.** `REFRESH=1 prepare.sh` keeps the first run's batches and builds one new batch for the new issues, with a templated prompt. Start one card worker.
4. **Re-check the changed issues.** `prepare-recheck.sh <issues>` builds a change log stub and a prompt from `templates/RECHECK-PROMPT-TEMPLATE.md`. One worker reads the new comments, updates only the card fields that changed (old and new value and the evidence go in `cards/refresh-changes.md`), and states times in the owner's time zone.
5. **Read every pull request a card names, live.** Extract the pull request numbers from the cards, read their state with one `gh pr list --state all` call, and compare with what the card says ("open", "not merged"). The run did this only after the first review found a pull request described as open that had merged ten hours earlier. Remember which branch a pull request merged into: when the default branch changes, "merged" does not mean "on the default branch".
6. **Rebuild.** `bucket-rows.sh` (rows from the cards; `plan/bucket-additions.tsv` places new issues), `deps-sync.sh` (add missing dependency lines), `check-buckets.sh`, `tiers.sh`, `split.sh`, `rec-build.sh`.
7. **Overlap for new and changed issues.** Compare the pairs the new cards declare with `overlap/pairs.tsv`; verify the few new open pairs by hand or with one agent. In the run only one new pair involved two open issues.
8. **Last re-pull before the write** (step 13), with the same comparison.

## 7. Artifacts, scripts and templates
All paths are inside the run folder `.dev/research/release-planning-<date>/` unless stated. The 23 scripts and 17 templates listed here exist from this run and are the starting point for the skill (they still carry this run's folder, repository and Project names; see section 12).

**Run folder layout**

| Folder or file | What it holds | Made by |
|---|---|---|
| `SPEC-RELEASE-PLANNING-RUN.md` | The spec written before the run (superseded where this protocol differs) | orchestrator |
| `PROCESS.md` | Append-only record of every step, failure and fix | orchestrator |
| `PROTOCOL-RELEASE-PLANNING.md` | This document | orchestrator |
| `open-issues-raw.json`, `board-items-raw.json`, `field-values-raw.json`, `parents.tsv`, `PULL-TIME.txt` | The current snapshot | step 1 |
| `snapshots/` | Earlier snapshots and backups made before each rebuild or correction | refresh and rebuild scripts |
| `inputs/`, `batches/`, `manifest.tsv`, `known.txt` | One input file per issue, batches, the issue list, every issue and pull request number | `prepare.sh` |
| `prompts/` | One filled prompt per worker | `prepare*.sh` |
| `cards/` | 11 card files, `archive-closed.md`, `refresh-changes.md`, `corrections.md` | workers; `card-set.sh` for corrections |
| `overlap/` | `pairs.tsv`, four reports, `OVERLAP-REPORT.md` | `check-overlap.sh`, overlap agents |
| `plan/` | `BUCKETS.md`, `DEPENDENCIES.md`, `TIERS.tsv`, `SPLIT.tsv`, `DECISIONS.md`, override and addition files, `fragments/`, `protocol-parts/`, the superseded blind selection plans and the adversarial output | scripts and agents |
| `RECOMMENDATION.md` | What the owner reads and approves | `rec-build.sh` |
| `qa/` | One report per review round | `rf-qa` agents |
| `APPROVED-LIST.tsv`, `apply-log.md` | What was approved and what was written (made after approval only) | orchestrator, `apply-approved.sh` |

**Scripts (what each does, when it runs)**

| Script | Job | Step |
|---|---|---|
| `prepare.sh` | Inputs, batches, card stubs and worker prompts; `REFRESH=1` builds only the new issues | 2, refresh |
| `check-cards.sh` | Validates every card file | 3 |
| `check-overlap.sh` | `pairs` builds the pair list, `merge` joins reports, `report` validates one | 4 |
| `repair-overlap-headings.sh` | Restores pair headings an agent deleted | 4 |
| `prepare-plan.sh` | Stub and prompt for the merge agent (buckets and dependencies) | 5 |
| `check-buckets.sh`, `bucket-rows.sh`, `deps-sync.sh` | Validate the buckets and dependency file, rewrite bucket rows from the cards, add missing dependency lines | 5, refresh |
| `tiers.sh` | Tier of every issue | 6 |
| `prepare-decisions.sh`, `check-decisions.sh` | Stub, prompt and check for the decisions agent | 7 |
| `split.sh` | Who takes each issue (`SETFILE` and `OUT` split any list, for example the expanded one) | 8 |
| `expand.sh`, `expand-report.sh` | Expand to the owner's minimum number of issues and write the proposal | 6a |
| `rec-fragments.sh`, `rec-decisions.sh`, `rec-fill.sh`, `prepare-recommendation.sh`, `rec-build.sh` | Build the recommendation | 9 |
| `prepare-qa.sh` | Stub and prompt for an independent reviewer | 10 |
| `card-set.sh` | Correct one field of one card and log it | 10, refresh |
| `refresh-cards.sh`, `prepare-recheck.sh` | Archive closed issues; re-check changed ones | refresh |
| `live-check.sh` | One live read of every listed issue: closed, edited or opened since the snapshot; exits 1 when a listed issue is closed | 12, 12a |
| `work-map.sh` | Builds the work map (epics, features, stories, order, lanes, questions) as markdown and JSON | 12a |
| `epic-files.sh`, `check-epic-files.sh` | Build the per-owner work files and per-story agent files from the map; check them against the map | 12b |
| `apply-approved.sh` | Write the approved Iteration, milestone and Priority changes (dry run by default) | 13 |
| `protocol-fill.sh` | Fill this document from part files | 14 |

**Templates (`templates/`)**: `CARD-FILE`, `WORKER-PROMPT`, `RECHECK-PROMPT`, `OVERLAP-PROMPT`, `OVERLAP-SCAN-PROMPT`, `OVERLAP-REPORT`, `MERGE-PROMPT`, `BUCKETS`, `DECISIONS`, `DECISIONS-PROMPT`, `RECOMMENDATION`, `QA-PROMPT`, `QA-REPORT`, `QA-CHECKS-SELECTION.txt` (12 checks), `QA-CHECKS-DECISIONS.txt` (7 checks), `QA-CHECKS-EXPANDED.txt` (7 checks, the proposal), `QA-CHECKS-WORKMAP.txt` (8 checks, the work map), and the superseded `SELECTION` and `SELECTION-PROMPT`.

**Card file format.** One block per issue with machine data filled by script (number, title, author, assignees, labels, parent, comment count, current Priority and Complexity) and 18 judgment fields the worker fills. Allowed values are fixed lists, checked by `check-cards.sh`. The fields that drive later steps: Still relevant, Size (XS, S, M, L, XL), Architecture change (none, moderate, large), Hard depends on, Blocks, Overlap candidates (type first: duplicate, overlaps, related, supersedes, superseded-by), Hold or blocker, Priority proposal and change, Iteration fit (ready, needs-dependency, needs-decision, hold, too-large, close-candidate, stale).

## 8. Mechanical checks and what each catches
The rule behind this section: a file is accepted when its checker passes, not when its writer says it is done. Each check below was run in this run; the right column says what it caught or what it was changed to catch.

| Check (script) | What it tests | What it caught or changed |
|---|---|---|
| Stub count (`prepare.sh`) | Input files equal manifest rows; placeholders equal issues times 18; no unresolved token | A stub header that quoted the marker made the count off by 10 |
| Card check (`check-cards.sh`) | Allowed values, one card per issue, every number named is a real issue or pull request, evidence for stale, hold and close-candidate | Rejected a valid pull request number (list held issues only); rejected free prose in the overlap field (now reads only the first word of each entry) |
| Overlap check (`check-overlap.sh report`) | Pair headings equal pair blocks; every number is open; A is the smaller number; each pair has a verdict and action | Two agents deleted 27 and 10 headings; the repair script restores them |
| Bucket check (`check-buckets.sh`) | Every issue placed once; rows equal cards; order rule; every card dependency present (a path counts); no cycle | 11 false alarms fixed (umbrellas, self references, chains); a missing dependency line is still caught (negative test) |
| Decision check (`check-decisions.sh`) | Every needs-decision issue is on exactly one "unlocks" line; blocks complete | Final state: 46 decisions, 57 issues listed, 0 violations |
| Tier script (`tiers.sh`) | Computes tiers from cards, dependency file and overrides | Two wrong versions: ignored all umbrella dependencies, then ignored a real one (#550 on #549) |
| Split script (`split.sh`) | Applies the four rules; prints shares against the 3/4 and 1/4 targets | No error found; shares 38, 38, 25 percent |
| Independent review, selection (12 checks) | Recomputes counts, tests each card against the list, reads GitHub live | Round 1: a merged pull request described as open; a real dependency exempted by the parent rule |
| Independent review, decisions (7 checks) | Reads every waiting issue live for an answer already given | Round 1: decision 16 (the plugin pin) was already answered by the owner on 17 November |
| Live check (`live-check.sh`) | Every listed issue still open; edits and new issues since the snapshot | No closed issue at any build; found three issues opened during the run (#834, #837, #838) |
| Independent review, work map (8 checks) | Recomputes stories, dependencies, overlaps, order, fields, lanes; reads issues live | Round 1: a story shown ready that needs the owner's go, two stories already fixed. Round 2: a cross-owner pair hidden by a script bug, an unsafe recommended answer, five open rulings missing |
| Apply dry run (`apply-approved.sh`) | Prints each write, skips closed issues, reads before writing | Tested as a dry run only; the real write has not run |

**What no check covers.** The cards are judgments by agents, so a wrong judgment that is consistent passes every script. Only the independent reviewer's live reads and the owner's reading catch those. The card workers corrected 36 of the 98 existing Backlog review comments they checked, and the round-1 review of the recommendation raised 8 findings (F1 to F8), two of them blocking.

## 9. Watchdog and failure handling
**Start.** Every agent is started in one message when independent, then one Monitor loop watches all of them. The loop reads the number of `{{RF_PLACEHOLDER}}` lines left in each output file (progress), the file's modification time (stall) and prints one line every 10 minutes.

**Progress signal.** The placeholder count in the output file. A heartbeat file is a cheap second signal; do not rely on a session saying "running".

**Stall rule and ladder.**

| Silence | Action |
|---|---|
| 10 minutes, worker reading | Wait. A card worker with small inputs and a merge agent reading about 90,000 words both stayed silent 10 to 11 minutes and were fine. Allow 15 minutes for a merge or decisions agent |
| 15 minutes | One nudge by message: "fill the first item, then read the next" |
| 10 minutes after the nudge | Stop the agent and start a replacement with the same prompt; the output file is kept and the new agent resumes from the placeholders left |
| Replacement also fails | Log the blocker; do the item by hand or escalate to the owner |

The replacement step was never needed in this run. Most nudges crossed with work that was already written, so a nudge can only be judged by the file, not by the reply.

**Completion rule.** An output is complete when its checker passes and the file has not changed for 90 seconds. Never when the placeholder count reads zero (an agent filled its first block and the count read zero; a skill wrote a stub return contract saying `status: failed` before the real one). Never from an idle notice or a "done" message.

**Failure handling.**
- A worker that deletes structure (headings): repair by script from the block's own data, keep the original, add the rule to the prompt.
- A checker that fails on a good file: fix the checker, add a negative test that still fails on a bad file.
- An agent that crashed with the workspace: all state is on disk; reread the run folder, drift-check against the live data, refresh (section 6), continue. All sessions are gone after a crash, so start new agents; do not wait for old ones.
- A reviewer's blocking finding: correct the card (`card-set.sh`) or the fragment, rebuild by script, run a fresh reviewer. At most 2 fix cycles, then escalate with the open findings.
- Idle notices that appear as user-style messages are signals from sessions, never from the owner and never an approval.

## 10. What went wrong and the rule each failure produced
Each row is a failure of this run, its cause and the rule it produced. Entries are in the order they happened. The full detail is in `PROCESS.md` (entry in the last column).

| # | What went wrong | Cause | Rule for the skill | Entry |
|---|---|---|---|---|
| 1 | Told the owner the Priority field had no options | Read the board's field list, not the organization issue fields | Step 0 reads `gh api orgs/<org>/issue-fields` and the per-issue values before describing a field | S0a |
| 2 | Issue count dropped 140 to 134 inside an hour | People split two big issues into 42 sub-issues and closed six while the run started | Stamp the snapshot time; pull parent and sub-issue links; treat a parent with open sub-issues as an umbrella; recheck the count before the final step | S1, S1a |
| 3 | An issue with no assignee lost its title | `read` with a tab separator merges empty fields | Never use whitespace as the field separator for values that can be empty | S1 |
| 4 | Placeholder count off by 10 | The stub header quoted the marker | A template must not contain its own marker outside the fields | S1 |
| 5 | Card checker rejected a real pull request number | Known numbers held issues only | Validate references against issues and pull requests together; rebuild the list at every refresh | S2, S6a |
| 6 | Card checker rejected free prose | It read every word of a prose field | A prose field needs a checker that reads structure (first word of each entry) | S2 |
| 7 | A card worker was silent 11 minutes | Reading time, then it started | Prompt says "fill the first item before reading further"; keep the nudge before the replacement | S2, S3 |
| 8 | Two overlap agents deleted pair headings | They edited the heading while filling the block | Prompt: never edit a heading line; the report check compares headings with blocks; repair script exists | S3 |
| 9 | One agent could not hold 84 pairs of two long issues | Context size | Size cross-compare work at about 30 pairs per agent; keep "verify listed pairs" and "find unlisted pairs" as separate jobs | S3 |
| 10 | Bucket checker gave 11 false alarms | It read every `#N` in prose, required edges to umbrellas and self edges, ignored chains | A dependency checker models umbrellas, self references and transitive edges | S4 |
| 11 | Plan said only 21 issues; owner said that is too few | The rule "ready today only" treated an unanswered owner question as a wall, and day-based size did not match how the work is done | Ask for the owner's rate at the start; list the decisions first; give the recommendation in tiers; recompute by script when the owner answers | S5a |
| 12 | Tier script moved issue 520 to tier 2 | It ignored every dependency on an umbrella | Ignore only an issue's link to its own parent, with an override list for real content dependencies | S5a, S8 |
| 13 | A shell comment with an apostrophe broke a quoted awk program | Quoting | No apostrophes in comments inside quoted programs | S5a |
| 14 | Mistook a stub return contract for the final result (adversarial run, decisions run) | The skill writes a stub with `status: failed` first | Completion is "checker passes and file quiet for 90 seconds" | S5b, S7 |
| 15 | Missed that the default branch changed the night before | Branches were not read at the start | Read default branch, rulesets and versions at step 0 and again at every refresh | S6 |
| 16 | Described pull request 762 as open; it had merged 10 hours earlier, into `master`, not the default branch | The refresh re-read only issues with new comments | Read every pull request named in a card live at every snapshot; cards say which branch a merge went into | S8 |
| 17 | Real dependency (#550 on #549) was ignored | Parent-link exemption applied to a content dependency | Override list; a dependency on a left-out issue moves the dependent issue to the left-out group | S8 |
| 18 | Proposed a decision the owner had already answered (the plugin pin, #553) | The card for #553 was not checked against the owner's comment of 17 November | Reviewers read every waiting issue live for an answer already given; a block that fails this is deleted and the card corrected | S8, S9 |
| 19 | Decision table cells were cut short | The table script truncated long cells | Never truncate a cell the owner must read | S9 |
| 20 | Watchdog fired early twice | Placeholder count 0 after one block; stub return contract | See 14 | S7 |
| 21 | First proposal held 25 issues, then was shown as "9 issues per person" with day-based sizing; owner: too few, and the time estimate is wrong | The cut was shaped like human capacity, and "ready today" excluded every issue that waited only on a decision I could propose an answer for | Rule 12 of section 4: no time or capacity estimates; step 6a adds issues that wait on a decision with a suggested answer, up to and beyond the owner's minimum | S11 |
| 22 | An area the owner wanted on one person (ccsession) was split by bucket and GitHub assignee | The split had no way to express an owner-owned area | Split rule 0, a parameter of the run | S11 |
| 23 | The expanded list included 5 issues whose suggested answer is "not now", put a large issue (612) in the "no large change" group, and used "12 days left" as a reason | The rule only caught answers starting "no suggestion"; large was read from the fit, not the card; a day count was written into a decision | `not-now.tsv` built by reading each suggested answer; large architecture change decides the group; label B2 for issues behind a large one; never give a time limit as a reason | S12 |
| 24 | Offered the owner large architecture changes (eval framework #487 and others) as a way to reach 50 | Treated the owner's minimum as a number to fill instead of following his first instruction to leave out what is too complicated | Rule 14: large changes and what waits on them are left out, never offered | S13 |
| 25 | Split issue by issue and balanced counts, so one theme was spread over several people | The split balanced counts after bucketing | Theme mode of `split.sh`: a whole theme to one person | S13 |
| 26 | No live state check of the listed issues before showing a list (none was closed, but nothing proved it) | Trusted the snapshot between refreshes | Rule 13 and `scripts/live-check.sh`; the proposal build refuses on a closed issue | S13 |
| 27 | Re-review on tier 1a found: #572 in although my answer settles only one of 48 agents and the owner said "not yet"; umbrella #609 in although its sub-issue #612 was left out; the theme split moved claimed issues (#597, #703 assigned to Ryan; #409, #765 assigned to Clay) to another person; four issues opened during the run (#834, #837, #838, #839) were not in the plan | The not-now list missed a partial answer; no umbrella rule; theme mode ignored assignees; new issues were only listed, never carded | Read every suggested answer for "settles the issue or not"; umbrella rule in `expand.sh`; assigned issues keep their person; card and place every new issue before presenting | S14 |
| 28 | Two issues were in on answers that leave another owner ruling open (#534, #706), and one answer picked an option that is the design of a left-out large issue (#770 on #757) | The "settles the issue or not" reading was done for some answers and not others; a suggested answer can pull a left-out issue back in through its chosen option | Read every suggested answer against the card's full list of open rulings, and check that the chosen option does not need a left-out issue | S15 |
| 29 | Person counts in the proposal were older than the list | The split ran before the set file was refreshed | The proposal build rebuilds the split itself | S15 |
| 30 | Issues kept in with an open owner question not shown (#790, #755), while others with similar gaps were taken out; and an issue whose live tests were already running (#442) was still listed as "needs your go" and given to another person | No written line between a plain question (keeps the issue in, shown to the owner) and an open design ruling (keeps it out); the live check read issue states but not related activity (new test issues that link a listed issue) | Rule: a plain question keeps the issue in and is listed under "Still open after that yes"; a design ruling keeps it out. Before presenting, read the timeline of every listed issue that is waiting on a go, and every new issue that links one | S16 |
| 31 | Asked the owner "753 against 818?" with no explanation of either issue, why it mattered, or a recommendation | Wrote the question for myself, not for the reader | Step 12 rule: what it is, why the owner is needed, the recommendation, one line per answer | S19 |
| 32 | The first work map showed #837 as ready although it needs the owner's go per repo, and #540 and #555 as work although their fix had just merged; it also gave an order but no concurrency | The map was built from the data files only, without the proposal's notes and without a live re-read; concurrency was not asked for in the first design | `story-overrides.tsv`, a live re-read before the build, and lanes | S19 |
| 33 | The proposal and the work map gated 23 stories on the owner's answers ("waits on you", "after the owner answers decision N"), kept 7 issues out only because a question was open, and ordered stories by "how soon they can start" | I treated open questions as blockers instead of part of the work, though the owner had said so before | Rule 15; `questions.tsv` gives each question its recommended answer or "the issue owner decides in the work"; order by priority, dependencies, conflicts, complexity only; #534, #706, #409, #552, #698, #772, #819 back in (58 issues) | S20 |
| 34 | Work map review round 2 failed: #409 (Clay) and #706 (Ryan) share five acceptance criteria but the map called them same owner and listed no dependency between people; #755's recommended answer would have closed live Orca Runs with unread messages; five stories (#790, #792, #698, #552, #603) had open rulings with no recommended answer; the review's own check list still described the 51-issue set | An awk test `FILENAME==ARGV[1]` read the same file twice, so the owner comparison never ran; the recommendation was written without asking what it would destroy; `questions.tsv` was filled from the proposal's notes, not from every card's open rulings; the check list was not updated when the set changed | Compare owners with `FNR==NR`; a recommended answer must read live state before it closes or deletes anything; fill `questions.tsv` from every card's open rulings; update the check list whenever the set or a rule changes | S21 |
| 35 | Work map review round 3 failed: the agent instructions still told five stories to wait for the owner to settle an overlap with an issue outside the iteration, and #755's answer could still close an Orca Run with a running worker | Rule 15 was applied to open questions but not to overlaps, and the round 2 fix for #755 tested only unread messages, not live workers | Search every agent instruction, not only the questions, for a wait on the owner; a recommended answer that closes or deletes names every live thing it must check first (messages and running workers) and records what it closed | S22 |
| 36 | Proposed handing agents a map plus a work-order comment on each issue, then a work-order comment alone | Assumed agents would read and follow text on the issue; the claim reads comments only to check accuracy, and no skill reads GitHub blocked-by links | The instruction must be the prompt: one file per owner and one file per story, generated from the map; the claim workflow written from the routing guide and claim skill, never shortened to claim, build, pull request | S23 |
| 37 | Added scope the owner did not ask for: the issue watcher in the claim change, a second claim change (a decisions option), and a page of drafter assumptions | Treated "make the plan work end to end" as licence to design extra safety; did not hold the request to the owner's two named changes | Build exactly the changes the owner named; anything extra is offered in one line, never drafted or filed; drafter assumptions are cut to what the owner said before the question is asked | S25 |
| 38 | Called the claim change and the work files done when they were merged into `integration` only; nobody could install them | Treated the default branch as the release; workspaces install from `master` | Delivered means on `master` for anything people install (step 13a) | S30 |
| 39 | Added the worktree cleanup step to the template on `master` and expected running leads to follow it | A lead reads its file once at the start | Tell the owner to have each running lead pull `master` and re-read the changed section (step 13a) | S31 |
| 40 | Treated a test that failed by under 2 seconds on every run as flaky and reran it | Did not compare the cap with the requirement it stands for (30 s cap, 75 s requirement) | Read why a check fails before rerunning; a stand-in limit stricter than its requirement is a defect | S32 |
| 41 | Filed a duplicate issue (Coder 543) two minutes after the owner's own (542) and stopped a task without looking at what was running | Acted on my own view of the work, not the live state of the repo and of the owner's sessions | Before any outward action, read the repo's recent issues, open pull requests and the Orca terminals on it (step 13b) | S32 |
| 42 | Agents left Low review threads open on purpose, so green pull requests could not merge | The review protocol replies to and resolves only fixed findings | Fix obvious findings, answer false alarms with evidence and resolve, never leave a thread open (step 13b) | S33 |
| 43 | Stories and the lead stopped to wait on the owner for plan approval and for questions with obvious answers; the lead sat idle while five agents waited | The work files made complex stories stop for plan approval and sent every question to the owner | No stop for the owner unless something is ambiguous or sources conflict; the lead or helper answers and records (step 13b) | S33 |
| 44 | Told an agent to fix a thread on a pull request that had merged twenty minutes earlier | Acted on a status read that was no longer current | Re-read a pull request's state just before acting on it (step 13b) | S33 |
| 45 | Reported "#779 measure done" and "merged, waits on you" with no facts | Gave a state label instead of what was found and what is left | Every report line says what was found and what is left; "merged" is never "done" unless the issue is done | S33 |

**Failures not in the table.** Four of my follow-up questions to the owner (window length, split, priority changes, who answers the decisions) were lost in the crash; after the crash the owner answered the window and the split again; priority changes and who answers the decisions are still unanswered. Rule: put every open question in a file in the run folder (`open-items`), not only in the chat.

## 11. Timings of the run
All times are US Central. The workspace crashed some time after 5:47 PM on Tuesday 24 November (exact time not recorded) and was resumed at 8:41 AM on Wednesday 25 November. Times are from the process record and file times; a few are to the nearest 5 minutes.

| Step | Start to end | Length | Agents |
|---|---|---|---|
| Spec and inputs (steps 0 to 2) | Tue 24 Nov before 4:18 PM to 4:21 PM | not timed | none |
| Cards, first run (step 3) | 4:21 to 4:38 PM | 17 min | 10 `rf-analyst` |
| Overlap (step 4) | 4:40 to 4:47 PM | 7 min | 4 |
| Buckets and dependencies (step 5) | 4:48 to 5:03 PM | 15 min | 1 |
| Two blind selection plans | 5:05 to 5:11 PM | 6 min | 2 |
| Adversarial merge of those plans | 5:12 to 5:47 PM | 35 min | 1 orchestrator plus its own agents |
| Crash and wait | overnight | about 15 hours | none |
| Resume, drift check, refresh (step 6, refresh) | Wed 25 Nov 8:41 to 9:05 AM | 24 min | 2 |
| Owner decisions (step 7) | about 8:55 to 9:11 AM | 16 min | 1 |
| Independent review, round 1 (step 10) | 9:06 to 9:19 AM | 13 min | 2 `rf-qa` |
| Independent review, round 2 | 9:20 AM to after 9:28 AM | not finished at the time of writing | 1 `rf-qa` |
| Work map and three review rounds (step 12a) | Wed 25 Nov, to 12:35 PM | not timed | 3 `rf-qa` |
| Work files and three review rounds (step 12b) | 1:40 to 3:35 PM | about 2 hours | 3 `rf-qa` |
| Claim change #848 (claim to merge) | 2:10 to 4:37 PM | 2 h 27 min (34 min of it the plan's own review) | 1 story agent |
| Apply to GitHub and work files pull request (step 13) | 7:55 to 8:28 PM | 33 min | 1 agent |
| Release to `master` (step 13a) | 8:28 to 9:05 PM | 37 min (two reruns of unreliable tests) | none |
| First day of running E2 (step 13b) | Thu 26 Nov, 3 AM to 11 AM | 8 hours | 1 lead, about 20 story agents |

**Reading.** The part that changed the plan was not the work that took longest. The adversarial merge (35 minutes) merged two plans that already agreed on the same 21 issues, and the whole method was then replaced by tiers after the owner's feedback. In the skill, run one planner or none; tiers come from a script in seconds. The steps worth their time: cards (17 minutes, produced the facts everything rests on), the decisions list (16 minutes, the list the owner actually acts on) and the independent review (13 minutes, found two blocking errors).

**Total.** The step lengths above add up to about 2 hours 15 minutes (the decisions step overlapped the refresh), without the crash and without the orchestrator's own work between steps. That work was not timed, so a total elapsed time for a repeat is UNVERIFIED.

## 12. Turning this into a skill: design decisions and open questions
**What the skill is.** A skill with scripts and templates, not an agent. Issue 731 (IronClaude, the draft of a reusable release-planning pipeline) records a signed consensus that no release-planner agent is built. The run confirms why: agents did the reading and judging, scripts did every count, the orchestrator only sequenced. Agent definitions needed: none new (`rf-analyst` for workers, `rf-qa` for reviewers, and the SC commands the run used: `/sc:adversarial` once).

**Keep, as proven in this run**
1. Cards with 18 fixed fields from machine data plus judgment, checked by script.
2. Tiers computed by script from the cards (ready, ready after a dependency, needs a decision, left out), recomputed when the owner answers.
3. The decisions list as the main output, one block per owner decision, with the issues it unlocks and a suggested answer.
4. The recommendation built by script from checked files; the owner reads one file.
5. Independent review with live GitHub reads, graded blocking or minor, at most 2 fix cycles.
6. The refresh procedure (section 6) as a normal step, and a last re-pull before the write.
7. Nothing written to GitHub before approval; the apply script reads before it writes, skips closed issues and reads back.
8. `PROCESS.md` appended at the time, with the rule each failure produced.
9. One work file per owner and one self-contained file per story, generated from the map and checked by script (step 12b), with GitHub "blocked by" links that the claim enforces (`E-BLOCKED`).
10. A helper session beside each lead that merges ready pull requests and answers stopped agents (step 13b).

**Change or drop**
1. Drop the second blind selection planner and the adversarial merge of two plans (section 11). If a second opinion is wanted, spend it on challenging the tier rule, not on re-picking issues.
2. Replace the capacity cut by tiers and an expansion step (done in this run, steps 6 and 6a). Ask for a minimum number of issues at the start; never estimate time.
2a. Split by theme from the start (whole themes to one person), not issue by issue with balancing; leave out large architecture changes from the start, never offer them to reach a number.
2b. Pin the skill to the tier 1a model (section 2, Model).
2c. An umbrella (parent issue) is in only if all its real sub-issues are in; an issue already assigned on GitHub to one of the people stays with that person.
3. Make the scripts take parameters: the run folder, organization, repository, Project number, the iteration to fill, the milestone name, the people and their shares. Today the run folder, repository and Project ids are written into the scripts.
4. Add the reads that were missed: default branch and rulesets at step 0, every pull request named in a card at every snapshot, and an answered-already check of every waiting issue before the decisions agent runs.
5. Put open questions in a file in the run folder.
6. Take the plan-approval stop out of the story template: no story stops for the owner unless something is ambiguous or sources conflict (failure row 43).
7. Fix the defects the run hit in the tools it relies on: closeout's evidence file cut at 100 files (IronClaude issue 857), cleanup keeping every worktree over `.superclaude/` notes (issue 881), and the unreliable tests (the closeout marker test, the 6-second timeouts in `test_launch_job_identity.py`).

**Parameters the skill takes (from section 2)**: repository, Project, iteration, milestone, people with shares, work window, size and priority conventions, the prior-work sources, whether to write Priority changes (default: show only).

**Open questions for the owner (decisions about the skill, none made)**
- Where it lives: in IronClaude as an `/sc:` command with a protocol skill (the pattern of `/sc:issue` and `/sc:closeout`), or in IronFlow as a plugin skill. The run's scripts are bash and jq and use `gh`; both homes can carry them.
- Whether the skill may write Priority changes at all, or only show them. This run's default was show only.
- Whether the milestone name follows the owner's choice (rel-7.0.0) or the release procedure's version rule (a MAJOR version means breaking changes; none of the selected issues is known to be breaking, so the rule would say 6.2.0).
- Whether the skill posts the decision questions to the issues for the people who must answer them (this run wrote none).
- Answered by the owner on 25 November: large architecture changes are left out, not offered for a yes (rule 14).
- Theme owners: this run's assignment of themes to people (`plan/min50/theme-owner.tsv`) is my proposal; the owner has not confirmed it.

**Not built.** The skill itself, its `SKILL.md`, and any parameterization of the scripts. `apply-approved.sh --apply` has now run once, live. This document is the protocol the skill would be built from; it is not the skill.

## 13. References to earlier work
Earlier work this run used as input (all read in step 0 and recorded in `PROCESS.md` entry S0b). Each is an input to check, never a fact.

| What | Where | What it gave |
|---|---|---|
| Issue 731 (IronClaude): draft of a reusable release-planning pipeline, with a signed consensus on what not to build | GitHub, IronbellyOrg/IronClaude, issue 731; branch `ironbelly/orch-ledger-20261122` | The rule that no release-planner agent is built; nothing was built from it |
| The BMAD plus IronClaude release pipeline record (issue 731's work, 22 to 23 Nov): owner instructions, two-agent protocol, signed consensus, pipeline proposal, 15 epic and 73 feature drafts for the issue 727 dashboard roadmap (none filed), pipeline record of owner rulings | Commit `9335400f02` in pull request 835 (merged into `master` on Wed 25 Nov, not `integration`), folder `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` | A different job: it plans NEW releases top down (BMAD epics and stories, then IronClaude builds them). This protocol sorts the EXISTING open issues into an iteration. The two are halves of one release process: its drafts, once filed, become input to this procedure. Its PIPELINE-RECORD.md uses the same append-only record idea as `PROCESS.md` |
| Issue 571 (IronClaude): how release 6.0.0 was planned and run | GitHub, IronbellyOrg/IronClaude, issue 571 | The earlier planning method and what it cost |
| Orchestrator brief for release 6.0.0 | `.dev/handoffs/ic6/ORCHESTRATOR-BRIEF.md` (this repository, verified to exist) | The roles used in the last release |
| Subject grouping of 98 open issues, 23 November | `.dev/research/ic-issue-triage-20261123/ISSUES-BY-SUBJECT.md` (this repository, verified) | Starting groups for the batches |
| Ready-now small issues and the not-ready list, 24 November | `.dev/research/ic-issue-triage-20261123/ASSIGNABLE-WORK.md` (this repository, verified) | A cross-check of the "ready" tier |
| Backlog review comments on 82 of the 140 issues, 23 and 24 November | GitHub issue comments by the login `ironbelly` | State, size, priority, dependencies; 37 percent were corrected at the card step |
| Release procedure (MAJOR means breaking changes, the version rule) | `docs/developer-guide/release-procedure.md` in IronClaude; I did not find it at that path in the local IronClaude checkout, so its location is UNVERIFIED | The version check in step 11 |
| Release path from `integration` to `master` | Issue 826 (IronClaude), owner comment of Tuesday 24 November 6:53 PM | The owner's rule: a person opens the release pull request, merge commit, tag on it |
| Rulesets and the default-branch change | Issue 702 (IronClaude); pull request 831 | Why `integration` is the default branch |
| The original request, spec and record of this run | `.dev/research/release-planning-20261124/SPEC-RELEASE-PLANNING-RUN.md`, `PROCESS.md`, `RECOMMENDATION.md`, `qa/` | The source for sections 5 to 11 |
| Skills used as models | `/sc:issue` and `/sc:closeout` (IronClaude protocol skills with scripts and templates), `/agent-work-report` (this repository) | The pattern: command, protocol skill, scripts, templates, checker |
