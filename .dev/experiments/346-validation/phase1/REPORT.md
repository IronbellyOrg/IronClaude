# Phase 1 report: past non-convergence incidents (source: agent session logs)

Status: STUB, filled section by section. Worker started 2026-11-08T01:52:29Z.

## Summary table

| Id | Incident | Rounds | Verdicts | Clearness | Recreatable | Review tool | Minutes | Tool calls |
|---|---|---|---|---|---|---|---|---|
| I1 | Orca worker-contract spec (issue 346 origin) | 3 (+4 constrained) | FAIL, FAIL, FAIL, then FAIL, FAIL, FAIL, PASS | 5 | yes (document and briefs), environment partial | `/sc:spec-panel` | 3 | 26 |
| I2 | Review-severity-rule plan, 3 pre-reviews | 3 | FAIL, FAIL (partial), FAIL; 11 -> 7 -> 10 blocking | 4 | partial | `/sc:reflect` pre mode | 6 | 11 |
| I3 | Launch-level hook plan (issue 394), 3 plan reviews | 3 | FAIL x3; 8 -> 8 -> 10 blocking | 5 | yes | adversarial reviewer agents | 6 | 12 |
| I4 | BMAD first-use research report, 3 gates | 3 per gate | FAIL-HALT x3 (Gates 1-3) | 4 | partial | tech-research QA gates (rf-qa agents) | 4 | 8 |
| I5 | P0 live-check plan package, 4 final reviews | 4 | issues, issues, issues, pass | 3 | partial | `/sc:implement` final review | 4 | 5 |

Only I1 used `/sc:spec-panel`, the command PR 427 changed. I2-I5 test the same failure shape (review, fix, re-review that keeps finding new blocking items) under other review tools, so they can only check PR 427 indirectly.

## Running cost tally

Counted from my own session log (`/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-exp346-p1-logs/93df824b-a474-4f08-8423-3a25c8421dcd.jsonl`), first call 01:52:29Z; count taken at call 97, 02:10:17Z (a few more calls follow for the method section, JSON and hand-off).

| Bucket | Tool calls | Notes |
|---|---|---|
| I1 | 26 | calls 1-26 (3 are setup) |
| General search, lead ranking, heartbeat | 8 | calls 32-34, 36-37, 44, 47, 68 (phrase ranking, verdict ranking, coordinator-session reads, `Skill` search, cap-phrase search) |
| I2 | 11 | calls 45-46, 56-62, 78-79 |
| I3 | 12 | calls 48-55, 82-85 |
| I4 | 8 | calls 69-70, 72-74, 87-89 |
| I5 | 5 | calls 38, 75-77, 91 |
| False leads and rejected candidates | 12 | calls 35 (issue-331), 39-43 (P1 and P2 sessions, review-loop-cause subagent, P1 static plan), 63-67 (liveness-v1-contract, issue-339 chain), 71 (IB-CPlus nuance agents) |
| Report editing | 12 | 11 `Edit` calls and 1 `Read` (calls 27-31, 80-81, 86, 90, 92-94) |
| Pointer spot-checks and the count itself | 3 | calls 95-97 |
| Total at count time | 97 | 84 `Bash`, 11 `Edit`, 1 `Read` (sums to 97: 26+8+11+12+8+5+12+12+3) |

Tool-result text returned to me up to that count: 352,298 characters (about 88,000 tokens).

## I1 Orca worker-contract spec (the incident behind issue 346)

Path prefix used below: `PJ` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs`; `FH` = `/home/coder/.claude/file-history`. Line numbers are jsonl line numbers (1-based) in the named session file. Each session is one Orca worker, one task per session.

**1. Description.** A 17-task Orca run (2026-11-02 03:26Z to 23:03Z) wrote `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, then ran independent `/sc:spec-panel` reviews and separate reviser workers. Rounds 1-3 each returned FAIL with new findings; the spec grew 57,763 -> 82,643 -> 92,194 bytes. Only a later diff-only, blocking/minor-graded loop (Tasks 11-17) ended in PASS.

**2. Evidence pointers.**

| Step | Session file (under `PJ`) | Brief | Output written (jsonl lines) | worker_done |
|---|---|---|---|---|
| Task 4 write spec v1 | `1b14f80b-2513-4df5-9449-924b3815a1ac.jsonl` | L10 | spec Write+Edits L95-629 | L652 |
| Task 5 review R1 | `699ae853-770c-4823-954c-43a845cd6b31.jsonl` | L11 | `review/spec-panel.md` L77-270 (Skill call `sc:spec-panel` in the file) | L289 |
| Task 6 revise 1 | `3bb70411-6b34-4a6c-b0de-81ffdbae7944.jsonl` | L10 | spec edits L221-673; `review/disposition.md` L76-719 | L738 |
| Task 7 review R2 | `aff19d65-a1f0-4494-8e6a-9ece95738d29.jsonl` | L11 | `review/spec-panel-round2.md` L105-423 (verdict L423) | L445 |
| Task 8 revise 2 | `66468bab-54d0-4268-a016-46cd22c264ab.jsonl` | L10 | spec edits L182-376; `review/disposition-round2.md` L149-534 | L552 |
| Task 9 review R3 | `1c9a7ec8-a900-4884-aef3-7f3fac245073.jsonl` | L11 | `review/spec-panel-round3.md` L116-540 (findings L475/489, verdict L503) | L562 |
| Task 10 revise 3 | `458bdc00-e815-4098-a449-4dfaef7826fd.jsonl` | L10 | spec edits L165-588; `review/disposition-round3.md` L101-613 | L634 |
| Task 11 diff review | `d534b6de-556c-4187-86e0-071dee59978d.jsonl` | L10 | `review/final-diff-review.md` | L430 |
| Task 12 combined revision | `eadb62ac-2f33-4997-9dc3-0925e98f9aa5.jsonl` | L10 | spec + `disposition-round4.md` | L1064 |
| Task 13 review | `02c0d4b8-9c10-4f01-8135-041ef59bf6ac.jsonl` | L10 | `review/round4-review.md` | L543 |
| Task 14 fix 1 | `99f9f18e-4585-4a62-af43-b609dc6d7539.jsonl` | L10 | spec + disposition | L292 |
| Task 15 recheck | `4799e7cc-0875-4067-8b38-2375cd119375.jsonl` | L10 | appended to `round4-review.md` | L313 |
| Task 16 fix 2 | `0d628073-98b2-4ae1-9ef7-0eb055d785f9.jsonl` | L10 | spec + disposition | L165 |
| Task 17 final recheck | `b510a293-1c5a-4783-bccb-793ed86fc0c2.jsonl` | L10 | appended to `round4-review.md` | L191 |

Document version after each round. These are pre-edit backups that Claude Code keeps outside `projects/`; the logs name them (for example `aff19d65...jsonl` L140 and `1c9a7ec8...jsonl` L136), and I read them and checked `wc`:
- v1 (after Task 4, before revise 1): `FH/3bb70411-6b34-4a6c-b0de-81ffdbae7944/2d815cfd5e9a74d2@v1` = 57,763 bytes, 285 lines.
- v2 (after revise 1): `FH/66468bab-54d0-4268-a016-46cd22c264ab/2d815cfd5e9a74d2@v1` = 82,643 bytes, 402 lines (also an `ls` at `aff19d65...jsonl` L37).
- v3 (after revise 2): `FH/458bdc00-e815-4098-a449-4dfaef7826fd/2d815cfd5e9a74d2@v1` = 92,194 bytes, 414 lines (also named in the Task 10 brief, `458bdc00...jsonl` L10).
- v4 (after Task 10): `FH/eadb62ac-2f33-4997-9dc3-0925e98f9aa5/2d815cfd5e9a74d2@v1` = 89,089 bytes. v5 (after Task 12): `FH/99f9f18e-4585-4a62-af43-b609dc6d7539/2d815cfd5e9a74d2@v1` = 115,819. v6 (after Task 14): `FH/0d628073-98b2-4ae1-9ef7-0eb055d785f9/2d815cfd5e9a74d2@v1` = 116,538. Final 116,815 bytes, 451 lines (`0d628073...jsonl` L165).
- Cross-check only, not a source: git branch `ironbelly/OrcaCLICommandRefactor-Specs` still exists and holds `.dev/orca-command-refactor/` (first commit ce642492, approved commit 969c7709).

**3. Per-round metrics (verified against the reports and snapshots).**

| Round | Verdict | New findings | Severity split | Caused by the previous round's fix | Spec bytes at review time |
|---|---|---|---|---|---|
| R1 (`spec-panel.md`) | FAIL | 24 | 3 CRITICAL, 15 MAJOR, 6 MINOR | n/a (first review) | 57,763 |
| R2 (`spec-panel-round2.md`; section 5 intro `aff19d65...jsonl` L382) | FAIL | 13 (+2 overstated citations, which are N6 and N13) | 1 CRITICAL, 9 MAJOR, 3 MINOR | 13 of 13 ("introduced or exposed by the revision"). Verdict text (L423) says 10 of the 24 R1 fixes introduced or exposed a new defect | 82,643 |
| R3 (`spec-panel-round3.md`; each finding has an "Origin" line, `1c9a7ec8...jsonl` L489) | FAIL | 14 | 0 CRITICAL, 8 MAJOR, 6 MINOR | 10 clearly (M2, M3, M5-M10, M13, M14 each name an N-fix); 2 partly (M1, M4); M11 is a reworked step; 1 pre-existing (M12). Verdict (L503): 8 of 13 R2 fixes introduced or exposed a new defect | 92,194 |
| Task 11 diff-only review | FAIL | 7 | 3 MAJOR, 4 MINOR | all on lines Task 10 changed | 89,089 |
| Task 13 review | FAIL | 13 | 2 blocking, 11 minor | | 115,819 |
| Task 15 recheck | FAIL | 1 (N1) | blocking | caused by Task 14's fix | 116,538 |
| Task 17 recheck | PASS | 0 blocking, 2 minor notes | | | 116,815 |

Dispositions: R1 24 of 24 applied, none rejected (`3bb70411...jsonl` L738); R2 15 of 15 applied (`66468bab...jsonl` L552). The numbers in issue 346 (24, 13, 14 findings; 57,763 / 82,643 / 92,194 bytes) all match the logs.

**4. Clearness: 5/5.** Three full rounds with new findings each time, nearly all written by the previous fix, 60 percent growth, no clean pass until four more constrained rounds. Caveat: the R3 brief says "any finding of any severity is FAIL" (`1c9a7ec8...jsonl` L11), so MINOR findings counted; CRITICAL plus MAJOR alone were 18 (R1), 10 (R2), 8 (R3), so the blocking-grade claim still holds.

**5. Recreatability: partial to yes.**

| Needed | Retrievable? | Pointer |
|---|---|---|
| Starting document (v1) | YES, byte-exact | `FH/3bb70411-.../2d815cfd5e9a74d2@v1` (57,763 bytes). Also replayable from the Write plus 26 Edits in `1b14f80b...jsonl` L95-629. The file-history copy sits outside `projects/*.jsonl` and may be removed by Claude Code cleanup, so copy it into the experiment folder before phase 2. |
| Exact R1 review brief | YES, verbatim | `699ae853...jsonl` L11 (runs `/sc:spec-panel @<spec> --mode critique --focus requirements,architecture`) |
| Exact revise briefs | YES | `3bb70411...` L10, `66468bab...` L10, `458bdc00...` L10 |
| Shared inputs the briefs name (README.md, inventories `commands-a.md`, `commands-b.md`, `orca-capabilities.md`) | PARTIAL | Written by Write/Edit calls in `9f0fb721...` (Task 1), `a1c4ed4e...` (Task 2), `f7191a1f...` (Task 3); README existed before all sessions (`9f0fb721...jsonl` L36). Final versions are in the git branch; round-1-time versions need replay. |
| Repo commit | PARTIAL | No SHA in the logs. Branch `ironbelly/OrcaCLICommandRefactor-Specs` (field `gitBranch`, e.g. in `699ae853...`). Master at 2026-11-02 03:25Z was about d6b02a4b (#340), an ancestor of the branch (UNVERIFIED as the exact start). `src/superclaude/commands/spec-panel.md` is unchanged between 782621f4 (2026-10-01) and PR 427 (95f2c6e4), so any commit before 95f2c6e4 gives the pre-fix command (skill folder history not checked). |
| Tools/skills | YES | `Skill` call `sc:spec-panel` with those args (`699ae853...`); Orca build `1.4.237-aidev02.0e4491a95e92` (`1c9a7ec8...jsonl` L503). Live Orca `--help` output the reviewers cited cannot be re-created exactly. |

The starting document is recoverable; the exact environment around it is only approximately recoverable.

**6. Cost to find.** About 3 minutes (01:52:29 to 01:55:29Z) and 26 tool calls (calls 1-26 of my own session log, 3 of them setup). This was the anchor incident, so the leads were given; the 3,000-line round reports were read through `jq` extractions, not whole.

## I2 Review-severity-rule plan: three pre-reviews, 11 -> 7 -> 10 blocking findings, cap reached

Prefix: `RS` = `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude--dev-worktrees-review-severity-rule`. Main session `RS/d6112a25-4a8a-4e17-927c-5d7b39e2f6af.jsonl` (8,329 lines, 2026-11-01T22:47Z to 2026-11-02T13:55Z); its 202 subagent logs are in `RS/d6112a25-4a8a-4e17-927c-5d7b39e2f6af/subagents/`. The worktree directory (`/home/coder/workspaces/IronClaude/.dev/worktrees/review-severity-rule`) no longer exists.

**1. Description.** A worker wrote a 20-task plan (via `/sc:workflow`) to remove the rule "any issue of any severity fails" and cap review loops at 2 fix cycles. The plan was pre-reviewed with `/sc:reflect` Tier 2 (3 reviewers plus adversarial merge) three times; every review returned FAIL with a different set of missed sites, and the worker had to escalate to the coordinator because the cap was reached.

**2. Evidence pointers (jsonl lines in the main session).**

| Step | Lines | What is there |
|---|---|---|
| Brief | L10 | Orca worker brief; plan input is in the `/sc:workflow` prompt at L313 ("Remove the 'any issue of any severity fails' review rule and cap review loops at 2 fix cycles (5.0.0 release blocker)...") |
| Restart after API error | L626 | "Your last turn died ... during the pre-review of package ...225635" |
| Plan v1 (package `TASK-WF-removeTheAnyIssu-20261101-225635`) | regenerated at L802 | task count of v1 not extracted (UNVERIFIED) |
| Review 1 | reviewer spawns L894/L898/L902; merge L1482; evidence check L1577; report Write L1572 (`.dev/reflect/pre-removeTheAnyIssu20261101225845/REPORT.md`); worker summary L1730 | FAIL, 11 blocking, 17 minor |
| Fix cycle 1 -> plan v3 (`...20261102-042031`, 19 tasks) | classifier L1709, plan gated L1909; "19 tasks" stated at L2015 | |
| Review 2 | coverage L1920, reviewers L2093/L2097/L2101; report Write L2235 (`.dev/reflect/pre-removeTheAnyIssu20261102042426/REPORT.md`); worker summary L2273 | status `partial` (stopped on input drift), 7 blocking (P2-B1..P2-B7) |
| Fix cycle 2 -> plan v4 (`...20261102-053741`, 20 tasks) | L2254, gated L2505 | |
| Review 3 | coverage L2515, reviewers L2628/L2632/L2636, calibrators L2777-2785, advocates L2903-2911, probe L3011; report Write L3149 (`.dev/reflect/pre-removeTheAnyIssu20261102054021/REPORT.md`); escalation L3399 | FAIL, 10 blocking (B3-01..), 12 minor |
| Coordinator decision | L4565 | add the 10 findings to the plan and implement, no fourth review |
| Final plan | L6760 ("all 21 tasks complete") | 21 tasks |

Document versions: the three plan packages are named above under `.dev/tasks/to-do/` of the vanished worktree; the plan text itself was written by subagents (not extracted). The three review reports are fully present as Write calls (L1572, L2235, L3149).

**3. Per-round metrics.**

| Round | Verdict | Blocking | Minor | Plan size | Caused by the previous fix |
|---|---|---|---|---|---|
| Review 1 (plan v1) | FAIL | 11 (B-01..B-11) | 17 | v1 tasks UNVERIFIED | n/a |
| Review 2 (plan v3) | FAIL (partial run) | 7 (P2-B1..P2-B7) | not counted (run stopped before the merge) | 19 tasks | Not attributed by the report. The worker's escalation (L3399) says each review "found new sites missing from the plan (11, then 7, then 10)", i.e. newly found misses, not fix-induced defects. P2-B3 ("CAP_PATTERN cannot detect 11 IN lines") is a defect in the fix-cycle-1 pattern. |
| Review 3 (plan v4) | FAIL | 10 | 12 | 20 tasks | Report L3149 says all 11+7 earlier blocking findings "landed" (earlier fixes worked); the 10 are new missed sites (for example `rf-qa.md:391`, `cli/prd/prompts.py:1279`). |

Totals: three FAIL verdicts, 28 blocking findings in total, never a clean pass; the plan grew 19 -> 20 -> 21 tasks. Review 2's input-drift stop is a process fault, not a finding.

**4. Clearness: 4/5.** Three rounds, new blocking findings each time, never clean, cap hit, plan grew. It loses a point because the findings are mainly newly discovered missed sites in a "list every site" plan, not defects written by the previous fix, and growth is small (tasks, not bytes).

**5. Recreatability: partial.**

| Needed | Retrievable? | Pointer |
|---|---|---|
| Starting document (plan v1) | PARTIAL | The plan package no longer exists on disk. It can be regenerated from the `/sc:workflow` input (L313), but the two source specs it names (`/tmp/t11-severity-rule-spec.md`, `/tmp/t11b-severity-rule-restart-spec.md`) are gone (`ls` fails). Their text may sit in Write calls of the earlier session that created them (not searched). The v1 plan text itself is likely in subagent logs (not extracted). |
| Review brief | YES | The three reviewer prompts are in the Agent calls at L894-902, L2093-2101, L2628-2636; the reflect protocol is `/sc:reflect` pre mode (UC-1). |
| Revise briefs | YES (in the Agent calls around L1709, L2254) | |
| Repo commit | PARTIAL | Branch `fix/review-severity-rule` (field `gitBranch`); no SHA in the logs. The fix was merged as 80f934de (#343); the base was master around a70150e2 (2026-10-31 23:53Z, UNVERIFIED as exact base). |
| Tools | YES | `Skill` `sc:workflow-protocol`, `sc:reflect-protocol`, `sc:adversarial-protocol` |

Note for phase 2: this incident reviews with `/sc:reflect`, not `/sc:spec-panel`, so PR 427 (a spec-panel change) does not touch the review tool used here.

**6. Cost to find.** About 6 minutes elapsed (02:00:37 to 02:06:12Z, interleaved with I3) and 11 tool calls (calls 45-46, 56-62, 78-79 of my session log). Lead: the `review-severity-rule` project folder name seen in the phrase ranking (call 33), then its message index.

## I3 Launch-level hook plan (issue 394): three adversarial plan reviews, 8 -> 8 -> 10 blocking findings

Prefix: `H4` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-hook-launch-level-394/42ae46e0-b8b8-4840-aafe-9b182be079c9` (main log `H4.jsonl`, 7,453 lines, 2026-11-05T17:02Z to 2026-11-07T05:14Z; subagent logs `H4/subagents/agent-<id>.jsonl`). The worktree `hook-launch-level-394` is gone, but its files survive in `/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/` (`SV` below) and in commit 3b344dd4.

**1. Description.** A worker merged three competing spec variants for a "launch-level guard" hook through an adversarial pipeline, drafted a 34-change refactor plan, and had it reviewed three times. Each review attacked the plan's shell-text parsing rules with real git and found new ways to push to `main`; each fix opened the next route. The owner stopped the loop after review 3 (no fourth review allowed).

**2. Evidence pointers.**

| Step | Pointer |
|---|---|
| Brief | `H4.jsonl` L12 points at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-prompt.md` (exists, 6,771 bytes) |
| Plan v0 draft | spawn `H4.jsonl` L895 -> `H4/subagents/agent-a6b78088fe4e8a5aa.jsonl` (Write L193 plus Edits) |
| Review 1 | spawn L919 -> `agent-a13bab688a9d224f8.jsonl`; report Write at its L181 (`plan-review.md`); parent summary L946 ("FAIL with 8 blocking findings") |
| Fix cycle 1 | spawn L947 -> `agent-a3c8e5c718996e77c.jsonl` (721 lines, about 100 Edits of `refactor-plan.md`, ends L720) |
| Review 2 | spawn L975 -> `agent-a07f24eaf42c5449e.jsonl`; report Write at its L276 (`plan-review-2.md`); parent summary L999 ("8 new blocking holes") |
| Fix cycle 2 | spawn L1000 -> `agent-a20512cfaf86249a3.jsonl` (1,195 lines; prototype scripts `llproto.*/classify.sh`, `corpus.sh`, `realgit.sh`) |
| Review 3 | spawn L1032 -> `agent-a793527cfdd94457c.jsonl`; report Write at its L331 (`plan-review-3.md`); parent summary L1059 ("fails with 10 blocking findings") |
| Owner stop | `H4.jsonl` L1082 ("Owner decision: no more review rounds ...") |
| Files on disk | `SV/.dev/brainstorms/20261105-170229-launch-level-hook/adversarial/adversarial/`: `plan-review.md` (194 lines, 33,649 bytes), `plan-review-2.md` (262 lines, 33,537), `plan-review-3.md` (300 lines, 39,519), `refactor-plan.md` (1,313 lines, 227,399 bytes, the final form only), plus variants 1-3, diff-analysis, debate rounds, invariant-probe |

Document version at each review (measured from the reviewers' own Read results of `refactor-plan.md`, last line number returned): review 1 read 1,054 lines (`agent-a13bab688a9d224f8.jsonl`, three reads); review 2 read 1,139 lines (`agent-a07f24eaf42c5449e.jsonl`); review 3 read 1,314 lines (`agent-a793527cfdd94457c.jsonl`, last read offset 990 limit 330). Byte sizes of v0 and v1 were not measured; only the final 227,399 bytes is known.

**3. Per-round metrics.**

| Round | Verdict | Blocking | Minor | Plan lines | Caused by the previous fix |
|---|---|---|---|---|---|
| Review 1 | FAIL | 8 (B-1..B-8) | 14 | 1,054 | n/a. Three routes to `main` (backtick, backslash-newline, dashed `git-push`) confirmed with real git |
| Review 2 | FAIL | 8 new (F-1..F-8) | 12 | 1,139 (+8%) | B-1, B-2, B-3, B-5 closed; B-4 closed only for listed spellings (F-3), B-7 closed with a false justification (F-4), B-8 partly (F-8). F-1, F-2, F-6, F-7 are holes in mechanisms added by fix cycle 1 (new canonical push form, word scan, line join, NM4). So 7 of 8 trace to fix cycle 1 by the review's own table and verdict; F-5 I did not classify. Four were reproduced on real git. |
| Review 3 | FAIL | 10 (B-1..B-10) | 11 | 1,314 (+25% over review 1) | Plan "buildable from the text", its own corpus reproduces except one inconsistency (B-6); 37 of 38 new attacks pass the rules. The review says the position-free rules rest on false premises; it does not classify each finding as fix-induced, so I do not claim a count. |

Totals: 26 blocking findings over three FAIL verdicts, none closed by a PASS; the plan grew 25 percent in lines. The parent's own words at review 2 (L999): "Each patch exposes another route".

**4. Clearness: 5/5.** Textbook: three rounds, new blocking findings every round (8, 8, 10), most of round 2 written by the round-1 fix, growing document, never clean, ended by an owner stop.

**5. Recreatability: yes (best of the set apart from I1).**

| Needed | Retrievable? | Pointer |
|---|---|---|
| Starting document (plan v0) | YES, by replay | Write plus Edits in `agent-a6b78088fe4e8a5aa.jsonl` (L193 onward), or the three Read results of the plan in `agent-a13bab688a9d224f8.jsonl` (1,054 lines with line-number prefixes). Inputs to the draft (three variant specs, diff analysis, debate, probe) are on disk in `SV/.../adversarial/adversarial/` |
| Review briefs | YES | Parent Agent calls at `H4.jsonl` L919 (2,849 chars), L975 (3,286), L1032 (4,152); also the first user line of each reviewer log |
| Revise briefs | YES, with a caveat | L947 (6,270 chars) and L1000 (6,656); they contain the parent's own steering ("one canonical-form allowlist", "two simplifications"), so a rerun must either reuse or drop that steering |
| Repo commit | PARTIAL | Branch `ironbelly/hook-launch-level-394` (field `gitBranch`, 2,061 lines; later `job-identity-394`); no SHA in the logs. The reviewers read repo files (`sc-pr-submit-protocol/SKILL.md` and refs) that exist in master at that time; the final feature merged as 3b344dd4 (#432) |
| Tools | YES | `general-purpose` Agent calls, `merge-executor`; reviewers needed bash 5.2, GNU sed/tr, jq 1.7, git 2.47.3 and throwaway bare repos under `/tmp` |

Note: the review tool here is a plain adversarial reviewer agent, not `/sc:spec-panel`; a `Panel review and refine spec` agent ran later (`H4.jsonl` L1677, `agent-ab0fb9d77d9cd7536.jsonl` L19 calls `sc:spec-panel`) on the finished spec, once.

**6. Cost to find.** About 6 minutes elapsed (02:01:08 to 02:07:10Z, interleaved with I2) and 12 tool calls (calls 48-55 and 82-85 of my session log). Lead: the session's prompts read in call 47 (owner message "no more review rounds" at `H4.jsonl` L1082).

## I4 BMAD first-use research report (Coder repo): three quality gates, each stopped at the 3-review cap

Prefix: `BM` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global/189f8649-3921-4435-bc6b-a15182a20399.jsonl` (5,392 lines, 2026-11-07T13:24Z to 22:00Z; subagent logs in the sibling folder `189f8649-.../subagents/`, 142 files). Repo is `IronbellyOrg/Coder` (not IronClaude), branch `ironbelly/bmad-ponytail-global`. The worktree still exists at `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global`.

**1. Description.** A `tech-research` run (task file `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md`) produced research files, four synthesis files and a final report (`RESEARCH-REPORT-bmad-first-use.md`). Each quality gate runs 2-3 independent reviewers, one fix agent, then 2 verification agents, with at most 2 fix cycles (3 reviews). Gate 1 (research completeness), Gate 2 (synthesis quality) and Gate 3 (report lenses) each ended in `FAIL - HALT` and an escalation to the coordinator; the user then granted a one-time exception for Gate 3.

**2. Evidence pointers (`BM` line numbers).**

| Gate | Review 1 | Fix 1 | Review 2 | Fix 2 | Review 3 / halt |
|---|---|---|---|---|---|
| Gate 1 research | L702-864 (analyst Important 2, qualitative Important 5, plus evidence agent; 9 blocking) | L864-946 | L964-1093 (both verification agents FAIL) | L1093-1142 | L1142-1261 (`GATE1_FINAL: FAIL - HALT`, L1261) |
| Gate 2 synthesis | L1925-2036 (qualitative 5 Important L1942, structure 4 Important L1959, analyst PASS L1992; 8 blocking) | L2036-2083 | L2083-2220 (content FAIL L2100, structural PASS) | L2220-2266 (3 findings) | L2266-2390 (`GATE2_FINAL: FAIL - HALT`) |
| Gate 3 report | L2861-3098 (seven lens agents, all FAIL, L2972; 95 findings in 69 rows; 18 blocking) | L3098-3144 | L3161-3307 (structural FAIL, qualitative FAIL) | L3307-3354 (5 findings) | L3354-3475 (`GATE3_FINAL: FAIL - HALT`) |
| Coordinator exception | L3744 (one exception, Gate 3 only); Gate 4 then passed in cycle 1 (L4012) | | | | |

Brief: `BM` L13 (a resume brief for an earlier dispatch that stopped while waiting for an exception answer). On disk in the Coder worktree, folder `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/`: the task file, `RESEARCH-REPORT-bmad-first-use.md` (1,807 lines, 407,656 bytes, final), and `qa/` with 80 files, including for every gate and cycle the consolidated findings (`qa-consolidated-findings-phase3.md`, `...-phase3-cycle2.md`, `...-phase5*.md`, `...-phase6*.md`), the fix logs (`qa-fix-log-phase3-cycle1.md` and so on) and the verification reports.

Document versions: pre-edit backups in `/home/coder/.claude/file-history/189f8649-3921-4435-bc6b-a15182a20399/` (one state per file, not one per round): `ca7857aee503d1e6@v1` = report with 1,795 lines, 387,624 bytes (the state after Gate 3 fix 1, identified by its title line and the line count in `BM` L3144); `b1f12dba87654e26@v1` = synthesis 04 (473 lines); `3e4a4f8f424a5b4d@v1` = synthesis 02 (465); `4bee01eff428f97f@v1` = synthesis 03 (399); `ae5475a180c7c83a@v1` = research file 05 (417); `7c3e47725f1b55c6@v1` = a consolidated-findings file (108 lines, `BLOCKING_COUNT: 17`). The task file has v1 (618,892 bytes) and v2 (620,012). Other states (the first assembled report at 1,785 lines, `BM` L2844) exist only as numbers.

**3. Per-round metrics (counts as stated by the worker from the gate files; I did not re-count the QA files).**

| Gate | Review 1 blocking | Review 2 blocking | Review 3 blocking | Verdict after 3 reviews | Caused by the previous fix |
|---|---|---|---|---|---|
| Gate 1 | 9 | 6 new | 1 (New-1) | FAIL, HALT | Round 2: "6 new blocking issues, all in text the fix agent wrote" (`BM` L1093): 6 of 6 |
| Gate 2 | 8 | 3 (finding 6 only partly fixed, plus new ones) | 2 (V-1, V-2) | FAIL, HALT | Round 2 findings include a fix log that omitted `synth-02` (N-1); V-1 is "my own inference stated as fact" in text written in earlier cycles; not counted precisely |
| Gate 3 | 18 | 5 | 2 (N-1, N-2) | FAIL, HALT | Verification of cycle 1: 17 of 18 fixed, 1 Important + 5 minor (structural) and 4 Important + 3 minor (qualitative) remain; the later N-1/N-2 are table cells inconsistent with the fixed text |

Report size: 1,785 lines (`BM` L2844) -> 1,795 after Gate 3 fix 1 (`BM` L3144) -> 1,807 final (on disk). So growth is small (about 1 percent), but every gate hit the cap without a PASS. Counts fall each round (9, 6, 1; 8, 3, 2; 18, 5, 2), so the loop was converging, only too slowly for a 3-review cap.

**4. Clearness: 4/5.** Three gates, each with three FAIL reviews and new findings every round; Gate 1's second round was entirely fix-written text; never clean within the cap. Lower than 5 because counts shrank every round and the document barely grew.

**5. Recreatability: partial.**

| Needed | Retrievable? | Pointer |
|---|---|---|
| Starting document | PARTIAL | The task file (on disk and as v1/v2 backups) defines the whole run; the research and synthesis files at the time of each review are not stored per round. Only the post-cycle-1 states of six files are in file-history. To restart a gate you would rerun the research phase (many web and repo reads) or start from the final files and accept a different baseline |
| Review briefs | YES | Gate agent prompts are in the Agent calls inside `BM` (and in the task file, which prescribes each gate's agents and the 2-cycle rule) |
| Revise briefs | YES | Same, plus fix logs on disk |
| Repo commit | PARTIAL | Branch `ironbelly/bmad-ponytail-global`; HEAD now 86c827af ("record the BMAD first-use decision", refs #478), which is after the run; the base at 2026-11-07T13:24Z is not logged |
| Tools/skills | YES | `tech-research` skill, `rf-analyst`, `rf-qa`, `rf-qa-qualitative` agents; web search was unavailable for part of the run (Tavily absent, WebSearch/WebFetch used), so a rerun will not match the research text |

This incident is a research-report gate, not a spec-panel review.

**6. Cost to find.** About 4 minutes elapsed (02:04:23 to 02:08:20Z) and 8 tool calls (calls 69-70, 72-74 and 87-89 of my session log). Found through the "last allowed fix cycle / review 3 of 3" phrase search over real messages (call 68, counted under general search).

## I5 P0 live-check plan package: four independent final reviews (issues, issues, issues, pass)

Prefix: `AA` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-OrcaCLICommandRefactor-Specs/aaee1ebf-4ec9-494f-85e0-52f3697170b5.jsonl` (5,569 lines, 2026-11-04T05:59Z to 2026-11-05T13:27Z; reviewer logs in `.../aaee1ebf-4ec9-494f-85e0-52f3697170b5/subagents/agent-<id>.jsonl`, 34 files). Same project folder as I1 but a different incident, different week, different document.

**1. Description.** A `/sc:implement` run executed the package `TASK-WF-writeTheP0LivePl-20261103-215902` (write the P0 live plan: three live Orca checks and a phase report). After the five tasks passed, the protocol's final independent review of the whole package returned `issues` three times in a row, each time on the evidence text written or fixed after the previous review; the fourth review passed after the owner approved three narrow fixes and rulings.

**2. Evidence pointers (`AA` line numbers).**

| Step | Pointer |
|---|---|
| Brief | `AA` L19-20 (`/sc:implement .dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/...md`) |
| Final review 1 | spawn L2001 -> `agent-a0d4eb0d0b16b7e1f.jsonl` (442 lines, 09:09-09:19Z), result `FINAL: issues` at its L441; parent report L2051 |
| Owner approval + fix 1 | L2058 ("go ahead and fix the counts"); edits L2099-2111 (`lc2-result.md`, `lc2-step5.md` x2, `lc1-step5.md`) |
| Final review 2 | spawn L2157 -> `agent-ad1d95b612f2d9bd6.jsonl` (445 lines, 12:11-12:21Z), `FINAL: issues` at its L444; parent report L2193 |
| Owner approval + fix 2 | L2204 ("approve"); edits L2242-2316 (`lc3-session-analysis.txt`, `lc3-step5.md`, `p0-phase-report.md`) |
| Final review 3 | spawn L2342 -> `agent-a88ad232bf783d3a3.jsonl` (607 lines, 12:29-12:44Z), `FINAL: issues` at its L606; parent report L2378 |
| Owner approval + fix 3 | L2390 ("approve widening"), L2427 ("include it"); edit L2464 (`p0-phase-report.md`) |
| Final review 4 | spawn L2499 -> `agent-a40f02e69785bb0f5.jsonl` (685 lines, 12:56-13:21Z), `FINAL: pass` at its L684; parent report L2559 (archived to `.dev/tasks/done/`) |

Document versions: the ledger `progress.md` has backups v2, v3, v4 and several evidence files have v2/v3 backups in `/home/coder/.claude/file-history/aaee1ebf-4ec9-494f-85e0-52f3697170b5/` (mapped by the `file-history-snapshot` entries in `AA`, for example `progress.md` -> `2217edb430755e4e@v2/@v3/@v4` = 7,219 / 7,430 / 8,156 bytes). The whole package (121 files) is also in git branch `ironbelly/OrcaCLICommandRefactor-Specs` under `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/` (cross-check only).

**3. Per-round metrics.**

| Review | Verdict | Blocking | What it found | Caused by the previous fix |
|---|---|---|---|---|
| Final review 1 | issues | 1 | "six" heartbeat gaps should be "seven" in 3 places (`lc2-result.md:27`, `lc2-step5.md:22,25`); non-blocking: "68 commands" should be 52 Bash calls | n/a |
| Final review 2 | issues | 2 | F1: `lc3-step5.md:18` and `lc3-session-analysis.txt:96` say only `check`/`send` were run (subagents also ran read-only `orca-ide`); F2: one empty bare `python3` call at 08:27Z breaks the "uv for every Python command" plan rule | 0 of 2: both were already in the delivered text; the round-1 count fix did not cause them |
| Final review 3 | issues | 1 | The first final reviewer itself ran 22 read-only bare `python3` commands (09:10-09:16Z), so the ruling and `p0-phase-report.md:71` ("every other Python call used uv run") overstate | 1 of 1: the sentence was written during fix 2 |
| Final review 4 | pass | 0 | Before it ran, the parent found one more bare `python3 -c 1` by the third reviewer (12:35:19Z, L2415); the owner's second ruling covers all 24 calls and review 4 confirmed exactly those 24 and no other | prevented: the parent told reviewer 4 to use only `uv run` (L2506) |

Document growth: not measured (UNVERIFIED); the phase report only gained a note and narrowed sentences. The task-criteria count is quoted inconsistently (23 at L2193, 22 at L2378, 18 in the review-3 text), so I do not use it.

**4. Clearness: 3/5.** Three consecutive FAIL reviews with a new blocking item each time, never clean until the fourth review, but only one or two defects per round, little growth, and only one of four rounds was caused by the previous fix (the others were newly found or process side effects of the reviewers).

**5. Recreatability: partial.**

| Needed | Retrievable? | Pointer |
|---|---|---|
| Starting document | YES (state before review 1) | The package in git (final form), plus `file-history` backups of `progress.md` and evidence files before each edit; the state before round 1 is the v2 backups |
| Review brief | YES | Agent prompts at `AA` L2001 (167 chars), L2157 (169), L2342 (169), L2499 (327); the protocol text is `sc-implement-protocol` (`refs/qa.md`, final review section) |
| Revise briefs | YES | Owner messages L2058, L2204, L2390, L2427 give the exact fixes |
| Repo commit | PARTIAL | HEAD `8db29f11` is quoted by the worker (L2193 and L2378: "HEAD is unchanged at 8db29f11"); branch `ironbelly/OrcaCLICommandRefactor-Specs` (`gitBranch` field) |
| Tools | PARTIAL | `sc:implement`; the live Orca checks the package records (three real worker runs, 32-87 minutes each) cannot be rerun cheaply. A rerun would only repeat the final review step on the stored package |

Note: the unit under review is a task package plus its evidence, not a spec; the review mechanism is `/sc:implement`'s final independent review, not `/sc:spec-panel`.

**6. Cost to find.** About 4 minutes of attention (lead at 01:57:41, detail at 02:05:32 to 02:05:45 and 02:09:07Z) and 5 tool calls (calls 38, 75-77, 91 of my session log). Lead: the owner messages "run the third and final review" in the coordinator session for I1's project folder.

## Method assessment

**Candidates examined: 17 to find 5.** I looked at least at the first prompt of each.

| Outcome | Count | Which | Why |
|---|---|---|---|
| Selected | 5 | I1-I5 | see sections above |
| False lead from inflated raw hits | 4 | issue-331 (`c619f49d`, 345 raw "verdict" hits), liveness-v1-contract (`84af4196`, 199 raw "spec-panel" hits, 0 in real messages), IB-CPlus-01 nuance-spec-panel agent (248 raw hits; a command-research task, not a review loop), qa-loop-investigation (`8917d256`; an investigation brief, not opened further) | The phrase sits in skill text, command files and request blobs copied into the log, so counts say nothing about a review loop |
| Real review loop, but it converged or was still running | 4 | P1 static plan (reflect 8 blocking -> 4 -> pass, `7fd4f558` L1621-3081); P1 live plan (1 blocking -> 0, L7430-9178); brainstorm-fix-brief plan reviews (no P1 in the last round, L13287-16347); issue-339 research gates (49 -> 5 -> 0 blocking; session still live at 2026-11-08T01:07Z) | Clearness 2-3 or unfinished; kept as spare candidates |
| Not opened beyond title and prompt | 4 | Specs coordinator `90f24ee7` (38 MB, 156 subagents), `5a587253` (/sc:implement of the earlier worker-contract plan), P2 session `ec52a47a`, the `review-loop-cause` subagent (analysis of I1, not a new incident) | Cost versus need: five were already found |

**Time and calls.** 18 minutes wall-clock from the first call (01:52:29Z) to the count at 02:10:17Z, 97 tool calls at that point (84 `Bash`, 11 `Edit`, 1 `Read`), taken from my own session log. By 02:12:54Z (after the method section, the JSON and the checks) the log showed 120 tool calls, so the whole job took about 21 minutes and about 120 calls; the hand-off adds two or three more.

**Source material read.** About 352,000 characters of tool output reached my context by call 97 (about 88,000 tokens). The filters (`rg`, `jq`) scanned far more but returned only matches: `rg` passes over the 9.3 GB `projects/` folder (about 7 seconds each) and `jq` passes over about 12 session logs, 3-40 MB each, plus 10 subagent logs. I never printed a whole log.

**Accuracy: high for numbers that sit in a report, medium for causal claims.**
- Verified against evidence: all of issue 346's figures (24, 13, 14 findings; 57,763, 82,643, 92,194 bytes) match the logs and byte-exact snapshots; severity splits in I1 and review counts in I2, I3, I5 come from the review reports and `FINAL:` lines; every jsonl line pointer in this report was spot-checked by script (all matched), and every cited disk path exists.
- Weaker: "caused by the previous fix" counts are the reviewing agents' own labels (I1 R2 and R3 "Origin" lines, I3 review 2); I did not re-derive them. I2 and I4 numbers come from the worker's messages and report headers, not from re-counting the `qa/` files. Task-criteria counts in I5 disagree within the logs (23, 22, 18), so I left them out. Per-round document sizes exist only for I1 (all rounds) and I3 (lines), not for I2, I4, I5.

**Efficiency: moderate.** Five incidents with evidence in about 20 minutes and about 100 tool calls is cheap, and the cost per incident fell from 26 calls (I1, no filter yet) to 5 to 12 once the real-message filter worked. But the first ranking pass was useless (see the obstacle) and 20 of 97 calls went to leads that did not pay off (12) or to general searching (8).

**Biggest obstacle: signal dilution and missing document states.** (1) Request blobs and pasted skill text repeat every phrase hundreds of times, so naive `rg -c` ranks sessions that never ran a review (liveness had 199 raw hits, none real). The fix that worked: count only lines starting `{"parentUuid"` and pair a phrase with a verdict word. (2) The logs hold edits and agent replies, not the documents; the per-round text of each document exists only as pre-edit backups in `~/.claude/file-history/` (outside `projects/`, one version per file per session) or in worktrees that were deleted. Copy those snapshots (for example I1's six `2d815cfd5e9a74d2@v1` files, one per session folder, and I5's `progress.md` backups) into the experiment folder before phase 2, because cleanup of `~/.claude` can remove them.

**Recommendation for phase 2.** Use I1 first (the only `/sc:spec-panel` incident, byte-exact starting spec and verbatim briefs) and I3 second (all review files and the v0 plan replayable, 3 clear rounds). I2 is a good third. I4 and I5 use other review tools and cannot be recreated from a single starting file.

Supporting material (not part of the deliverable): helper scripts and extraction files in `.dev/experiments/346-validation/phase1/scratch/` (untracked). No secret-like strings were found in them or in this report (pattern scan run at the end).
