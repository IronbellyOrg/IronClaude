# S3 ANALYSIS (incident I3: launch-level hook refactoring plan, issue 394)

Status: complete. Produced by `/sc:analyze` (invoked as a top-level Skill call, not through a subagent) on the brief "recreate the past incident I3 as exactly as possible, original run as baseline, output a replay package". Nothing was run against the incident: no reviewer, no loop, no `/sc:spec-panel`. Analysis and packaging only. Written 2026-11-08.

How `/sc:analyze` was applied (its five steps): Discover = locate the session log, the 6 subagent logs, the surviving brainstorm folder and the git objects (section 1). Scan = replay the recorded file edits, extract the briefs, cross-check against what the agents themselves read (sections 2 and 6). Evaluate = severity-rated findings about the incident and about how well it can be recreated (section 7). Recommend = replay modes and what to record (REPLAY.md). Report = this file plus `baseline-metrics.json`, `inputs/`, `briefs/`, `REPLAY.md`.

## 0. Summary

- One worker session (Claude Code 2.1.318, branch `ironbelly/hook-launch-level-394`, base commit 8b4858f7) ran the adversarial brainstorm pipeline for the launch-level hook (issue 394). Its Step 4 drafted a 34-change refactoring plan (`refactor-plan.md`, 136,216 bytes, 1,053 lines) and put it through THREE independent reviews with TWO fix cycles in between. All three reviews returned FAIL: 8, 8, then 10 blocking findings (26 in total; 37 minor). No review passed.
- The plan grew from 136,216 to 227,399 bytes (+66.9 percent bytes, +24.7 percent lines). The loop stopped at the cap (2 fix cycles, 3 reviews). The owner then confirmed "no more review rounds" and the open findings went into the merged spec as open decisions.
- The reviewer was NOT `/sc:spec-panel`. Every review and every fix was a plain `Agent` call (`subagent_type: general-purpose`, `model: sonnet` or `opus`, background) with a free-text brief written by the orchestrator. PR 427 changed `/sc:spec-panel` and routing text only. No file it changed is read by any agent in this loop. Expected effect of PR 427 on this scenario: none (details in section 5).
- The recorded mechanism differs from the one in the issue text ("each fix causes the next findings"). Re-derived from the plan versions: only 3 to 5 of the 8 round-2 findings and 1 to 3 of the 10 round-3 findings were created, wholly or in part, by the preceding fix cycle (phase 1 said 7 of 8 for round 2; that is not supported, section 6). The larger driver is that each round's reviewer was given a wider job and a wider definition of "blocking" than the one before (section 3.3), and the design problem (classify shell text) has no finite list of attacks.
- Recreation grade B (REPLAY.md). The reviewer briefs and every input document are verbatim or line-verified. The part that cannot be replayed is the orchestrator's own steering between rounds.

## 1. Evidence key

| Short name | Path |
|---|---|
| `H4` | `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-hook-launch-level-394/42ae46e0-b8b8-4840-aafe-9b182be079c9` (main log `H4.jsonl`, 7,453 lines; subagent logs `H4/subagents/agent-<id>.jsonl` with `.meta.json` beside each) |
| `SV` | `/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.dev/brainstorms/20261105-170229-launch-level-hook` (the original worktree `hook-launch-level-394` is gone; its brainstorm folder survives here and in commit 9aa7b4f9) |
| `baseline/` | this package: `baseline/plans/refactor-plan.v0.md`, `.v1.md`, `.v2.md` (replayed versions), `baseline/reviews/plan-review.md`, `plan-review-2.md`, `plan-review-3.md` (byte copies of the SV files), `baseline/agent-costs.json` |
| `briefs/` | this package: the verbatim briefs; the file name carries the `H4.jsonl` line number, e.g. `R1-reviewer-L919.md` |
| `tools/` | scripts used here (all read-only): `replay_plan.py`, `crosscheck_reads.py`, `reads_vs_disk.py`, `agent_costs.py`, `build_baseline_metrics.py` |

Plan versions: v0 = the plan as drafted (input of review 1); v1 = after fix cycle 1 (input of review 2); v2 = after fix cycle 2 (input of review 3; equals the plan file on disk today, sha256 f72e3d3a...). They are not stored anywhere else. They were rebuilt by re-applying every recorded `Write`/`Edit` of `refactor-plan.md` in the three writer logs (`tools/replay_plan.py`). Check: the reviewers' own Read results of the plan match the replayed versions line for line (`tools/crosscheck_reads.py`: review 1 vs v0 0 of 1,053 lines differ; review 2 vs v1 0 of 1,138; review 3 vs v2 0 of 1,313; the only extra "line" in each Read is an empty row after the final newline), and the replay of v2 equals the file on disk byte for byte.

## 2. What happened, round by round

Times are UTC on 2026-11-05. Costs are from `baseline/agent-costs.json` (derived by `tools/agent_costs.py`: unique API messages and tool calls, output tokens; cache tokens deliberately left out).

### 2.0 Before the loop (context, not part of the metrics)

- `H4.jsonl` L12 (17:02:02): the owner's only instruction: "Read /home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-prompt.md and follow it." The brief (`inputs/owner/hook-session-prompt.md`, 6,771 bytes) says: no human is watching; run `sc:brainstorm` (3 proposals, systematic), then `sc:design`, save, commit, push, comment on issue 394; "Goal: maximum effect with the fewest edge cases and unwanted behaviour" (brief line 24).
- Skill calls in order: `sc:brainstorm` L85, `sc-brainstorm-protocol` L105, `sc-adversarial-protocol` L376 (the Step 1 to 5 pipeline of `/sc:adversarial`), `sc:design` L1155. Step 1 to 3 agents: three variant specs L409/L413/L417 (opus, sonnet, haiku), diff analysis L475, round-1 advocates L516/L520/L524, round-2 advocates L579/L601/L623, invariant probe L687, scoring L739/L743.
- The installed `sc-adversarial-protocol` Step 4 says "Delegation: debate-orchestrator drafts, analytical agent reviews" and "review: default Auto-approved" (`git show 8b4858f7:src/superclaude/skills/sc-adversarial-protocol/SKILL.md` lines 275 to 306). So the three-review loop below was the orchestrator's own addition, driven by the rule in its output style (section 4), not by the protocol.

### 2.1 Draft (v0)

- Spawn: `H4.jsonl` L895 (19:06:46): `Agent`, `subagent_type: general-purpose`, `model: opus`, description "Step 4 draft refactor plan", brief `briefs/R0-writer-draft-plan-L895.md` (5,639 characters; equals the first user message of `H4/subagents/agent-a6b78088fe4e8a5aa.jsonl`).
- Result: Write of the whole file at `agent-a6b78088fe4e8a5aa.jsonl` L193, then 16 applied Edits (last L332). 33 minutes (19:06:46 to 19:40:15), 49 tool calls, 186,979 output tokens. v0: 136,216 bytes, 1,053 lines, 34 numbered changes, a disposition row for every one of the 40 probe findings (INV-001 to INV-040), 0 named attack cases.

### 2.2 Review 1 (of v0)

- Tool and flags: `H4.jsonl` L919 (19:40:27): `Agent`, `subagent_type: general-purpose`, `model: sonnet`, background, description "Step 4 review of refactor plan". No slash command and no flag. Brief `briefs/R1-reviewer-L919.md` (2,849 characters, seven numbered checks). Agent log `agent-a13bab688a9d224f8.jsonl`.
- Work: 15 minutes (to 19:55:29), 27 tool calls (12 Bash with throwaway bash/jq tests and real git in `/tmp`, 11 Read, 3 Grep, 1 Write at its L181), 116,316 output tokens. It read v0 in three Reads (1,053 lines).
- Result: `baseline/reviews/plan-review.md:5` "Verdict: FAIL"; `:7-8` 8 blocking (B-1 to B-8), 14 minor (M-1 to M-14). Checks 1, 3, 6 PASS; 2, 4, 5 FAIL (`:10-18`). The eight blocking findings (titles from `plan-review-2.md:16-25` and `plan-review.md:73`): B-1 backtick inside a push reaches `main` (confirmed on real git), B-2 backslash-newline continuation, B-3 dashed `git-push` form, B-4 `gh api` method-flag spellings, B-5 normalisation steps without an allowed tool, B-6 the plan claimed every turn-starting route is blocked, but background Agent, Bash and Monitor calls can start a turn, B-7 deleted session file reads as an ordinary session, B-8 false claim about commit messages. Parent verdict text: `H4.jsonl` L946 (`briefs/R1-orchestrator-note-after-review-1-L946.md`).

### 2.3 Fix cycle 1 (v0 to v1)

- Spawn: `H4.jsonl` L947 (19:56:30): `Agent`, general-purpose, `model: opus`, description "Fix cycle 1 revise refactor plan"; brief `briefs/R1-reviser-fix-cycle-1-L947.md` (6,270 characters). Lines 5 to 13 of the brief are the orchestrator's STEERING: 8 numbered points, among them "do NOT patch each route", replace the push denylist by a CANONICAL-FORM ALLOWLIST, replace the `gh` evasion list by a GET-ONLY allowlist, name exact `sed`/`tr` commands for normalisation, do not block background agents but correct the claim, keep B-7 as a residual with an owner decision.
- Result: `agent-a3c8e5c718996e77c.jsonl`: 19 minutes (to 20:15:48), 114 tool calls (100 Edits of `refactor-plan.md`, L89 to L711), 130,891 output tokens. v1: 174,471 bytes, 1,138 lines (+38,255 bytes, +28.1 percent; +85 lines, +8.1 percent). New in v1 (absent from v0 by `rg` over the replayed versions): the canonical push form, the GET-only `gh api` form, the named normalisation steps NM1 to NM7, owner decision O-16 (the others of O-16 to O-19 are named by review 2's brief and findings).

### 2.4 Review 2 (of v1)

- Tool and flags: `H4.jsonl` L975 (20:16:01): `Agent`, general-purpose, `model: sonnet`, background, description "Plan re-review round 2"; brief `briefs/R2-reviewer-L975.md` (3,286 characters). Log `agent-a07f24eaf42c5449e.jsonl`.
- Work: 15 minutes (to 20:31:11), 39 tool calls (26 Bash including real-git attacks against two local bare repos and a stub `gh`, Write of the report at its L276), 113,287 output tokens. Its brief asked for a re-run of the first review's attacks, a regression hunt and a read of `/sc:pr-submit` (`briefs/R2-reviewer-L975.md:6-10`).
- Result: `plan-review-2.md:5` FAIL; `:7-8` 8 blocking (F-1 to F-8), 12 minor (m-1 to m-12). All eight first-round findings were closed for the exact attacks the first reviewer ran (`:16-25`). New blocking findings: F-1 alias hidden by the "later git word" exemption (`git rebase -x 'git -c alias.p=push p origin HEAD:main'` moved `main` on real git, `:46`), F-2 the push regex accepts a lone option (`git push origin --all`, `:70`), F-3 shell-built `gh` method flag (`:87`), F-4 false justification that `rm -rf ~/.claude/state` is caught (`:101`), F-5 `$GIT push origin main` pinned as allowed with no residual note (`:121`), F-6 the redirection step deletes the word after a quoted `>` (`A=">" git push origin HEAD:main`, `:131`), F-7 deleting quotes lets a quoted option value shift the subcommand (`:144`), F-8 false claim that one-line PR titles mentioning git are not blocked (`:155`). Four of them were reproduced on real git (parent text `H4.jsonl` L999).

### 2.5 Fix cycle 2 (v1 to v2)

- Spawn: `H4.jsonl` L1000 (20:31:59): `Agent`, general-purpose, `model: opus`, description "Fix cycle 2 revise refactor plan"; brief `briefs/R2-reviser-fix-cycle-2-L1000.md` (6,656 characters). Brief lines 5 to 13 are the STEERING: "STOP PATCHING POSITIONS. Make the classifier simpler and blunter"; a new GLOBAL OVER-APPROXIMATION RULE (any git word plus any gated word anywhere in the command is classified by the strongest class); canonical-form allowlists for push and `gh api`; add `.claude/state` as a tamper token; delete the continuation join and the redirection-removal step; and (item 7) "PROTOTYPE AND REGRESSION CORPUS (mandatory)": write a bash prototype in `/tmp`, run all earlier attacks and 15 benign commands, add the corpus to the plan's test plan.
- Result: `agent-a20512cfaf86249a3.jsonl`: 46 minutes (to 21:18:13), 177 tool calls (106 Edit, 34 Bash, 28 Read, 3 Write calls, all prototype files in `/tmp/llproto.*`: `classify.sh` L118, `corpus.sh` L126, `realgit.sh` L171), 194,173 output tokens. v2: 227,399 bytes, 1,313 lines (+52,928 bytes, +30.3 percent; +175 lines, +15.4 percent). New in v2 (absent from v1 by `rg` over the replayed versions): the global over-approximation rule, the second quote-stripped scan form, "command position", the rule that the segment split runs only when the command contains `git`, `gh`, `orca`, `superclaude` or `repos/` (`baseline/plans/refactor-plan.v2.md:209`), and 61 named attack cases T-ATK-1 to T-ATK-61. Parent text on return: `H4.jsonl` L1031: "Its prototype blocks 58 of 61 attacks, and the 3 leaks are listed as residual R1."

### 2.6 Review 3 (of v2), the last one allowed

- Tool and flags: `H4.jsonl` L1032 (21:18:33): `Agent`, general-purpose, `model: opus` (the first two reviews used sonnet), background, description "Plan final review round 3"; brief `briefs/R3-reviewer-L1032.md` (4,152 characters). Log `agent-a793527cfdd94457c.jsonl`.
- Work: 29 minutes (to 21:47:24), 47 tool calls (32 Bash, 13 Read, 1 Edit, 1 Write of the report at its L331), 142,080 output tokens. Its brief (`:6-12`) required: build the classifier from the plan text alone as a throwaway prototype; run the plan's own corpus; write and run at least 25 NEW attacks and 15 NEW benign commands; list ten realistic commands the plan would block; judge whether `/sc:pr-submit` is usable at `full --submit`; give MET / MET WITH CAVEAT / NOT MET per acceptance criterion.
- Result: `plan-review-3.md:5` FAIL; `:7-8` 10 blocking (B-1 to B-10), 11 minor (m-1 to m-11). It says the plan is buildable from the text and its own corpus reproduces except for 3 rows (`:12-33`); but of 38 new attacks 37 pass at every level and every remote-reaching git attack moved remote `main` on real git (`:10`). Blocking: B-1 a line continuation inside a word hides `git` (`:186`), B-2 `$''` splicing (`:202`), B-3 command position misses shell keywords and wrapper values (`:214`), B-4 a git config file outside the tamper list redirects a canonical push to `main` (`:230`), B-5 glob and brace spellings (`:236`), B-6 the segment split is skipped for the words the escape and tamper rules need (`:246`), B-7 a REST write to `main` through `curl` (`:252`), B-8 a versioned `npx` spelling of Claude Code (`:258`), B-9 reinstalling hooks via the module name (`:264`), B-10 `/sc:implement`'s retry revert block is UNKNOWN at every level (`:270`). Acceptance criteria: AC-1, 2, 3, 5, 6 NOT MET; AC-4, 8 MET WITH CAVEAT; AC-7 MET (`:167-178`). `/sc:pr-submit` at `full --submit`: "Usable, with friction the plan states honestly" (`:131-133`). Parent text: `H4.jsonl` L1059.

### 2.7 How the loop ended, and why

- Reason: the cap. The orchestrator's output style says "A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings" (`inputs/owner/output-style-pragmatic-L15.md`, also `H4.jsonl` L15). The reviser and reviewer briefs restate it ("fix cycle 1 of 2", "the last allowed", "no further fix cycle is allowed": `briefs/R1-reviser-fix-cycle-1-L947.md:1`, `briefs/R2-reviser-fix-cycle-2-L1000.md:1`, `briefs/R3-reviewer-L1032.md:1`).
- Sequence: `H4.jsonl` L1059 (21:47:59): "The rules allow no fourth review and no pass with open blocking findings. So I'm not marking these resolved." It spawned the merge executor at L1060 (21:48:19, "Step 5 merge execution") with the ten findings carried as unreviewed amendments. At L1082 (21:55:22) the owner wrote: "Owner decision: no more review rounds. Put every unresolved blocking finding from plan-review.md, plan-review-2.md and plan-review-3.md into the spec as an Open decisions list, mark the spec as not reviewed after its last amendments, then go straight to the merge, /sc:design, commit, push of the feature branch and the comment on issue 394 ..." (`briefs/R3-owner-stop-L1082.md`). The orchestrator forwarded it to the running merge executor at L1089. First commit of the result: 9aa7b4f9 at 22:28:14Z (parent 8b4858f7), then the owner decision commit 7065667a (2026-11-06T01:11:31Z).
- Final state: three FAILs, 26 blocking findings, no PASS, and the orchestrator's own summary says "the text-scanning approach keeps leaking" (`H4.jsonl` L1059). It proposed a structural alternative (a git-level `pre-push` hook) as owner decision O-22.

## 3. Reviewer tool, flags and scope in each round

### 3.1 Tool and exact call parameters

Every step used the `Agent` tool; none used a slash command or a CLI flag. The "flags" of each call are the four `Agent` inputs below (from the `tool_use` blocks at the stated `H4.jsonl` lines; sidecar copies are `briefs/*.meta.json`). All six agents were `requestShape: background`, `requestNonInteractive: true` (`H4/subagents/agent-<id>.meta.json`).

| Step | `H4.jsonl` line | `subagent_type` | `model` | `description` | Tools the agent had | Output file |
|---|---|---|---|---|---|---|
| Draft | L895 | general-purpose | opus | Step 4 draft refactor plan | all | `refactor-plan.md` |
| Review 1 | L919 | general-purpose | sonnet | Step 4 review of refactor plan | all | `plan-review.md` |
| Fix 1 | L947 | general-purpose | opus | Fix cycle 1 revise refactor plan | all | edits `refactor-plan.md` |
| Review 2 | L975 | general-purpose | sonnet | Plan re-review round 2 | all | `plan-review-2.md` |
| Fix 2 | L1000 | general-purpose | opus | Fix cycle 2 revise refactor plan | all | edits `refactor-plan.md` |
| Review 3 | L1032 | general-purpose | opus | Plan final review round 3 | all | `plan-review-3.md` |

The model aliases `sonnet` and `opus` resolved to `claude-sonnet-5-5` and `claude-opus-5-5` in the agent logs. The orchestrator itself ran on `claude-sonnet-5-5` for `H4.jsonl` lines 880 to 1060.

### 3.2 What each review was asked to do (brief line numbers)

| Review | Task list in the brief | New in this round |
|---|---|---|
| 1 (`briefs/R1-reviewer-L919.md:5-12`) | 7 checks: coverage of the 36 diff points, probe coverage INV-001 to INV-040, shared assumptions, internal consistency (test at least 5 regexes in `/tmp`), acceptance criteria AC-1 to AC-8, facts, size discipline | baseline review |
| 2 (`briefs/R2-reviewer-L975.md:5-10`) | verify B-1 to B-8 are closed by re-running the original attacks; re-test at least 8 regexes; regression hunt, including every `git push` and `gh` command `/sc:pr-submit` issues; AC sufficiency; size | re-attack with real git; reads the pr-submit protocol |
| 3 (`briefs/R3-reviewer-L1032.md:5-12`) | build the classifier from the plan text alone; run the plan's corpus; **write and run at least 25 NEW attacks and 15 NEW benign commands**; list ten realistic commands the plan would block; decide whether `/sc:pr-submit` is unusable at `full --submit`; MET / MET WITH CAVEAT / NOT MET per AC | the reviewer is told to generate fresh attacks; prototype from text; usability judgement |

### 3.3 The definition of "blocking" widened each round

Quoted from the briefs (same sentence, three versions):

- Review 1 (`briefs/R1-reviewer-L919.md:14`): BLOCKING = "wrong behaviour, missing required item, false claim, security or acceptance-criterion hole"; MINOR = "wording, format".
- Review 2 (`briefs/R2-reviewer-L975.md:12`): BLOCKING = "wrong behaviour, a leak to main/master, a missing required item, a false claim, an AC hole". Added: "a leak to main/master".
- Review 3 (`briefs/R3-reviewer-L1032.md:14`): BLOCKING = "a leak to main/master or past a level boundary that the plan claims to stop, wrong behaviour, missing required item, false claim, unusable /sc:pr-submit at full --submit, an AC hole without an honest caveat". Added: "past a level boundary", "unusable /sc:pr-submit", "AC hole without an honest caveat".

Reading: the blocking bar and the review job both grew from round to round, while the plan was never allowed to reach "no blocking finding" except by the reviewer failing to find one. In round 3 the reviewer was told to invent new attacks; it found 38 and 37 passed (`plan-review-3.md:10`). A scenario in which the reviewer is instructed to red-team a text classifier with fresh attacks cannot converge to PASS inside 3 reviews; this is a property of the brief, not only of the fixes.

## 4. Severity rule in force each round, and where the cap comes from

| Item | Rule | Source |
|---|---|---|
| Grades | two grades only, blocking and minor. "Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, ..." | orchestrator output style, `inputs/owner/output-style-pragmatic-L15.md` (section "Completion, testing, and quality gates"); `H4.jsonl` L15 |
| Verdict | binary: "Every review agent MUST produce a binary verdict: PASS or FAIL ... Only blocking findings produce FAIL"; minor findings are notes and never trigger a fix pass | same file |
| Cap | "A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings" | same file; restated in the briefs of both revisers (`:1`) and review 3 (`:1`) |
| Review 1 as told to the reviewer | GRADE BLOCKING / MINOR as in 3.3; "binary verdict PASS (no blocking findings) or FAIL" | `briefs/R1-reviewer-L919.md:14` |
| Review 2 | same wording plus "a leak to main/master" | `briefs/R2-reviewer-L975.md:12` |
| Review 3 | widened wording, 3.3 | `briefs/R3-reviewer-L1032.md:14` |
| Fix cycles | reviser must resolve "the blocking findings"; minor findings: "apply the cheap ones", skip any that adds a mechanism (fix 1 point 7); "m-1..m-12: apply the cheap ones" (fix 2 point 6) | `briefs/R1-reviser-fix-cycle-1-L947.md:12`, `briefs/R2-reviser-fix-cycle-2-L1000.md:11` |

So one rule family (binary, blocking/minor, 2 fix cycles) was in force in every round. Differences between rounds are only in the wording of what counts as blocking (3.3). The `/sc:spec-panel` command's own severity model (CRITICAL / MAJOR / MINOR, `--iterations`) was not involved. The sub-agents' own system prompts are not in their logs, so whether the output-style text also reached them is UNVERIFIED; the briefs restate the rule they act on, which is what the sections above quote.

## 5. Can PR 427 affect this scenario?

Short answer: no, not through anything the original reviewers used. Evidence:

1. The reviewer is a general-purpose `Agent` with a free-text brief, not `/sc:spec-panel` (table 3.1; the six agent logs contain no Skill call: `jq` over `H4/subagents/agent-*.jsonl` for the six ids finds no `Skill` tool use). The one `/sc:spec-panel` run in this session is later and outside the loop: `H4.jsonl` L1677 (2026-11-06T20:45:34Z, "Panel review and refine spec", one panel iteration on the finished spec).
2. PR 427 (`95f2c6e4`) changed these non-`.dev` files only: `src/superclaude/commands/spec-panel.md` (+12 lines: a `## Review Loop` section and the `--re-review <file> --baseline <copy>` option), `plugins/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md` and its plugin mirror (one sentence), `docs/guides/prd-skill-release-guide.md`, `docs/guides/tdd-skill-release-guide.md` (one line each), `docs/designs/spec-panel-review-loop.md`, `tests/skills/test_spec_panel_review_loop.py` (`git show --stat 95f2c6e4`).
3. No agent of the loop read any of those files. `tools/reads_vs_disk.py` lists every file each agent read with the Read tool; none is on the list. The Bash and Grep targets of the six agents (checked with `jq` over their commands) are the brainstorm folder, `issue-body.md`, the pr-submit and implement protocols, `WORKER-CONTRACT.md`, `install_hooks.py`, `hooks.json`, `settings.json`, `Makefile` and `/tmp` scratch paths; none is a 427 file.
4. `git grep -i spec-panel` over `sc-adversarial-protocol`, `sc-brainstorm-protocol` and the `brainstorm` and `design` commands finds nothing at 8b4858f7 and nothing at HEAD. So the pipeline cannot route into spec-panel.
5. The host's installed `~/.claude/commands/sc/spec-panel.md` is the pre-427 text (sha256 prefix e7b1a2c66f96be1f equals `git show 8b4858f7:src/superclaude/commands/spec-panel.md` and `ec1babd9:...`; the 427 text is c8d80346a96cb528). 427's own commit message says new command text reaches an installed host only after `superclaude install --force` or `superclaude update`.

Consequence for the experiment (DECISIONS.md D4, "known limit"): S3 re-run with the verbatim briefs will measure noise, not 427. It is a useful NEGATIVE CONTROL: its round-to-round spread with unchanged tooling is the yardstick for "larger than the spread between replicates" in D6(c). An optional, clearly labelled treatment arm that does put 427 in the path (replace the reviewer by `/sc:spec-panel --mode critique ... --re-review ... --baseline ...` on the plan) is described in REPLAY.md; it changes the tool, so it is not comparable to the baseline round by round.

## 6. Metrics: what was read and what was derived (full table in `baseline-metrics.json`)

| Metric | Value | Read from evidence or derived |
|---|---|---|
| M1 rounds to clean pass | none; 3 reviews, 2 fix cycles, last verdict FAIL | read: verdict lines `baseline/reviews/plan-review.md:5`, `plan-review-2.md:5`, `plan-review-3.md:5`; parent text `H4.jsonl` L946, L999, L1059 |
| M2 blocking per round | 8, 8, 10 (minor 14, 12, 11) | read: header lines `:7-8` of each review. Derived check: ids B-1..B-8 / M-1..M-14, F-1..F-8 / m-1..m-12, B-1..B-10 / m-1..m-11 re-counted by `rg`, all agree |
| M3 findings caused by the previous round's fix | round 1: n/a. Round 2: 3 to 5 of 8 (37.5 to 62.5 percent; 3 clear: F-2, F-3, F-4; 2 partial: F-1, F-8). Round 3: 1 to 3 of 10 (10 to 30 percent; 1 clear: B-6; 2 partial: B-3, B-4) | DERIVED by me (the reviews carry no origin tags and do not classify their findings by cause). Method: for each finding, does the mechanism or sentence it attacks occur in the earlier plan version (`rg` over `baseline/plans/*`)? Reading of rule text only; nothing executed. Detail and per-finding evidence in `baseline-metrics.json` under `rounds[*].M3.analyst_rederivation` |
| M4 document size | v0 136,216 B / 1,053 lines; v1 174,471 B / 1,138; v2 227,399 B / 1,313. Growth +28.1 / +30.3 percent bytes per fix cycle, +66.9 percent bytes and +24.7 percent lines over the loop | derived: replay of recorded edits; line counts confirmed against the reviewers' own Read results; v2 bytes equal the file on disk; v0 and v1 bytes are replay results (not independently observed) |
| M5 cost per round | review 1: 27 tool calls, 116,316 output tokens, 15 min; fix 1: 114, 130,891, 19 min; review 2: 39, 113,287, 15 min; fix 2: 177, 194,173, 46 min; review 3: 47, 142,080, 29 min. Loop total (excluding the draft) 404 tool calls, 696,747 output tokens, 127 min from review 1 start to review 3 end | derived from the subagent logs (`tools/agent_costs.py`; unique API messages and tool-use ids; output tokens from the last usage record per message id). Wall time includes the fix cycles. Cache tokens are not comparable and are left out |

### 6.1 Where my numbers differ from the phase-1 report (logs team, I3 section)

| Phase-1 statement | Check | Result |
|---|---|---|
| Plan lines 1,054 / 1,139 / 1,314 ("+8 percent", "+25 percent") | `tools/crosscheck_reads.py` | Those are the last line numbers the Read tool printed. The real counts are 1,053 / 1,138 / 1,313 (the Read prints one extra empty row after the final newline). Percentages: +8.1 percent and +15.4 percent per cycle in lines, +24.7 percent over the loop; in bytes +28.1, +30.3 and +66.9 percent. Use bytes for D6(b); lines under-state growth |
| "7 of 8 trace to fix cycle 1" (round 2) and "NM4 added by fix cycle 1" | `rg` over v0, v1: v0 already has N2 (delete every quote) and N4 (remove a redirection and its next word), v0 lines 192 and 194; v0 already has the "later git word is exempt" rule G4 (line 218). The sentence about "PR titles" first appears in v1 (line 234); v0 has only the commit-message form of the claim (line 218) | Only F-2, F-3, F-4 are clearly new in v1; F-1 (the NM2 join) and F-8 (the PR-title sentence) are partly new; F-5, F-6, F-7 were already in v0. So 3 to 5 of 8, not 7 |
| "I did not classify F-5" | row 33 of the v0 decision table already pins `$GIT push origin main` (v0 line 421) | F-5 was latent from v0 |
| Round 3: "I do not claim a count" | same method as round 2 | 1 to 3 of 10; B-6 is clearly new in v2 (v2 line 209); B-3 and B-4 are partly new (B-4: the hole is old, the R11/R17 contradiction is new in v2 line 994); B-1, B-2, B-5, B-7, B-8, B-9 trace to v0 or v1 text; B-10 probably latent (same "No S, UNKNOWN" rule in v0 line 210), not executed |
| Brief L919 is 2,849 characters, L975 3,286, L1032 4,152, L947 6,270, L1000 6,656 | `jq` on the log lines | All five confirmed, and each equals the first user message of its agent log |
| Starting document "YES, by replay" | done here | v0 rebuilt; line-for-line equal to review 1's Reads; v2 equals the file on disk |
| Repo commit "PARTIAL, no SHA in the logs" | Orca reflog of branch `ironbelly/hook-launch-level-394`: "Created from refs/remotes/origin/master" at 2026-11-05 17:01:24Z; the first commit 9aa7b4f9 (22:28:14Z) has parent 8b4858f7 | The base commit is **8b4858f7** (master commit 2026-11-05T10:24:11-06:00, "docs(onboarding): add the onboarding deck ..."), 95f2c6e4 is its descendant (`git merge-base --is-ancestor 8b4858f7 95f2c6e4` yes). The installed skills equal this tree, so the loop ran on it |

### 6.2 Cross-check with the tasklists team report

`/home/coder/workspaces/worktrees/IronClaude/exp346-p1-tasklists/.dev/experiments/346-validation/phase1/REPORT.md` has no entry for this incident: its "I3" is a different incident (the Orca P0 live plan, 4 reviews, 3 FAIL then PASS, `REPORT.md:101-134`) and its summary table (`:6-12`) lists no launch-level hook plan. The two reports share the label "I3" for different incidents. Its remark that plans are "edited in place" (`:247`) is confirmed here for the hook plan too: only the final form survives on disk, which is why v0 and v1 had to be rebuilt from the logs. Nothing in the tasklists report contradicts a number in this file.

### 6.3 A labelling conflict the coordinator should resolve

`DECISIONS.md` D2 lists "S2 issue-394 launch-level hook plan" and "S3 review-severity-rule plan" and says "(from the logs report, S = I)". In the logs report the numbering is the other way round: I2 = review-severity-rule plan (reviewed with `/sc:reflect`), I3 = the launch-level hook plan (`phase1/REPORT.md:10-11`). The assignment text for this task says "S3 = incident I3" and "Review the past incident I3", so this package covers the **launch-level hook plan**. If another analyst was given "S2" under the D2 labels, two packages may cover the same incident and the review-severity-rule plan may be uncovered. This is not resolvable from the evidence; it is flagged for the coordinator.

## 7. Findings (severity-rated, as `/sc:analyze` reports them)

Severity: HIGH = changes whether the replay measures what the experiment wants; MEDIUM = lowers fidelity or can mislead a comparison; LOW = housekeeping.

| # | Severity | Finding | Evidence | Recommendation |
|---|---|---|---|---|
| A1 | HIGH | PR 427 cannot affect this scenario as the original ran it: no agent in the loop uses `/sc:spec-panel` or reads a file 427 changed. | section 5 | Treat S3 as a negative control; do not count it toward "427 proven" without the labelled spec-panel arm. |
| A2 | HIGH | The reviser briefs contain the orchestrator's STEERING, which names finding ids and design pivots of the original reviews ("canonical-form allowlist", "STOP PATCHING POSITIONS"). They cannot be replayed verbatim in a chained re-run, because the re-run's reviews will find different things. The steering is also itself a likely driver of growth: both fix cycles added a new mechanism and grew the plan by about 30 percent. | `briefs/R1-reviser-fix-cycle-1-L947.md:5-13`, `briefs/R2-reviser-fix-cycle-2-L1000.md:5-13`, section 2.3 and 2.5 | Offer two modes in REPLAY.md: round-by-round (all briefs verbatim, inputs are the original documents of each round) and chained (reconstructed neutral steering, labelled). |
| A3 | HIGH | The reviewer briefs for rounds 2 and 3 are conditioned on the previous round's output (they name B-1..B-8, the canonical push form, O-21, T-ATK cases). Verbatim reuse is exact only when the plan they review is the original v1 or v2. | `briefs/R2-reviewer-L975.md:1,6,8`, `briefs/R3-reviewer-L1032.md:6,9` | Round-by-round mode reviews the original v1 and v2; chained mode uses `briefs/RECONSTRUCTED-R2-reviewer-generic.md` and `RECONSTRUCTED-R3-reviewer-generic.md` (only ids and counts generalised, plus a skip-what-is-absent line). |
| A4 | MEDIUM | The "blocking" definition and the reviewer's job widen each round (3.3); round 3 orders fresh attack generation. The loop's non-convergence is built into the briefs. | section 3.2 and 3.3 | Record which brief wording a re-run uses; a re-run with the same wording will probably also fail round 3, which is the fair baseline. |
| A5 | MEDIUM | The fix-induced share is lower than phase 1 reported (3 to 5 of 8, not 7; 1 to 3 of 10). I3 therefore tests "reviewers surface latent holes one round at a time" more than "fixes cause the next findings". | section 6.1, `baseline-metrics.json` | Report M3 as a range; state the mechanism when comparing with S1. |
| A6 | MEDIUM | The answer is on disk in many places in the current repository (the finished plan and reviews, the merged spec `docs/designs/sc-issue-launch-level-hook.md`, the hook script and tests, follow-on task packages). A re-run worktree that contains them lets the agents read the answer. | `git ls-tree 95f2c6e4`: 27 files in the brainstorm folder, plus `docs/designs/sc-issue-launch-level-hook.md`, `tests/hooks/fixtures/launch_level/`, and two `.dev/tasks/done` packages (50 files that mention the design) | `tools/prepare_replay_worktree.sh` removes them (dry run by default). |
| A7 | MEDIUM | Repo drift between 8b4858f7 and 95f2c6e4 touches files the reviewers fact-check: `hooks.json`, `install_hooks.py`, `sc-pr-submit-protocol`, `sc-implement-protocol`, `WORKER-CONTRACT.md` (PR #411, #414 and others, not 427). Installed `~/.claude` copies still equal 8b4858f7. | `git diff --stat 8b4858f7 95f2c6e4 -- <paths>`; `diff -r` of installed vs base trees | The prepare script restores these paths to 8b4858f7 in the replay worktree only; 427's files are untouched. |
| A8 | MEDIUM | The orchestrator was a different model from the one in the experiment's likely re-run, and the session later used a second model; the reviewers used two model sizes (sonnet for reviews 1 and 2, opus for review 3). | section 3.1 | Keep the same `model` parameter per step; record the orchestrator model. |
| A9 | LOW | v0 and v1 bytes are replay results; only the line text is confirmed by independent evidence. | section 1 | Acceptable; v2 equals disk, the method is the same. |
| A10 | LOW | The reviewers wrote throwaway files and ran real git under `/tmp`; the host tool versions equal the original (bash 5.2.37, sed 4.9, tr 9.7, jq 1.7, git 2.47.3). | review headers `plan-review-2.md:3`, `plan-review-3.md:3`; versions re-checked 2026-11-08 | None. Keep `/tmp` writable and clean up after the run. |

## 8. Evidence-pointer check

Every `H4.jsonl` line number in this file was read back from the log (jsonl type, time and the first words of the content): L12, L15, L85, L105, L376, L895, L919, L946, L947, L975, L999, L1000, L1031, L1032, L1059, L1060, L1082, L1089, L1155, L1677. The `baseline/...:N` and `briefs/...:N` pointers were taken from `rg -n` / `Read` output of those files while writing; `tools/check_pointers.sh` re-checks the quoted headings and phrases (REPLAY.md, last section).

