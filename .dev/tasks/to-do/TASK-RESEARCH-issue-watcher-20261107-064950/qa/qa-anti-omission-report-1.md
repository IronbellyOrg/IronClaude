# Anti-Omission Report 1

**Status:** Complete
**Date:** 2026-11-07

VERDICT: FAIL

(14 of 301 enumerated findings omitted: 0 CRITICAL, 2 IMPORTANT [O-05, O-04], 12 MINOR. Addendum conformance 6 of 6 REPRESENTED. Details in Part C and Part D.)

## Anti-Omission Report

**QA phase:** anti-omission (source to output completeness), partition 1
**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (2,176 lines)
**Input files checked:** research/01-claim-flow-and-session-launch.md (290 lines), research/02-github-surface-and-cli-patterns.md (231), research/03-governance-and-security-surface.md (233), gaps-and-questions.md (42), synthesis/synth-01-problem-current-state.md (507). Total findings enumerated: 301 (83 + 73 + 68 + 33 + 44)

Method: coverage judged by meaning, not by ID citation. Report location references are line numbers in `RESEARCH-REPORT-issue-watcher.md` (read in chunks; plus targeted pattern searches over the whole report for every item not found in the chunks read). Findings are enumerated at the granularity of one distinct claim, rule, number, tag or recommendation. Where the synthesis file repeats a research finding, it is enumerated once under its research file and the synthesis file is checked separately for anything it added or dropped.

Report structure noted before enumeration: sections 1-2 of the report are a near-verbatim carry of synth-01 (a line diff of synth-01 lines 17-507 against report lines 102-700 leaves only 39 non-matching synth lines: the owner-decision labels Q1-Q3 renamed D1-D3, one rewritten bullet, and the "Carried to Open Questions" list, which the report moved to Appendix A.1 and Section 9). The report also holds a "Coverage of research-file key findings" table (lines 1941-1992) and a Section 9 that maps all 24 gap rows; I did not accept either as proof, I re-checked by meaning.

---

## Part A. ADDENDUM conformance (extra rows; an OMITTED row here is CRITICAL)

| # | Conformance item (from research-notes.md ADDENDUM 2026-11-07T07:03Z and ADDENDUM 2 2026-11-07T07:12Z) | Status | Report location and evidence |
|---|---|---|---|
| AC-1 | Recommendation is option A labelled "decided by the owner"; the words "pending owner decision" appear nowhere | REPRESENTED | Section 7.1 (line 1335) "Option A, the workspace-side poller, decided by the owner (ADDENDUM 2)"; also lines 135, 141, 668. A case-insensitive search for "pending owner", "owner decision pending" and "pending.{0,20}decision" over the whole report returns no match. |
| AC-2 | Options B and C are scored and documented as alternatives with revisit conditions | REPRESENTED | Section 6.2 and 6.3 headings "Documented alternative"; Requirement Scoring table with B and C columns for R1-R10 (lines 1256-1271), Tally (1273-1280), Options Comparison (1292-1307), "Revisit conditions for options B and C" with nine conditions (1309-1327), Section 7.8 (1415-1417). |
| AC-3 | IronbellyOrg/Coder#477 cited as sibling dependency with repo boundary (listener, registration and transport live in the Coder repo, not IronClaude) and the statement that it was filed assuming a push design and option A makes it unnecessary unless B or C is revisited | REPRESENTED | Section 1.2 (lines 143-149), Section 7.7 (1411-1413), Section 9.1 row D5 (1845), revisit footer (1325). All three elements (sibling dependency, boundary, "filed assuming a push design ... unnecessary unless B or C is revisited") appear in 1.2 and 7.7. |
| AC-4 | Only a validated integer issue number reaches a session prompt, never issue title or body text | REPRESENTED | Section 1.1 D3 (line 137), 7.3 security model "Prompt (D3)" (1361) and "Fields read" (1362), Section 9.1 (1843), Integration Checklist (1821). |
| AC-5 | Scope is claim-only, decided by the owner; the pipeline after the claim stays manual | REPRESENTED | Section 1.1 D2 (line 136: "the pipeline after the claim stays manual"), 7.3 "Claim-only (D2)" (1354), 9.1 D2 (1842). |
| AC-6 | Correction that `src/superclaude/pr_submit/ci.py` is not a `gh` subprocess wrapper (imports only `re`, `.classifier`, `.models`; a poller needs its own injectable runner) is flagged, together with the statement that `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected | REPRESENTED | Section 2.3 "Where gh is actually invoked" (line 340: imports `re`, `.classifier`, `.models` at `ci.py:10-15`; "has been corrected there (line 21, CORRECTION ...)" and in research-notes.md lines 30 and 37); 7.6 "Subprocess seam" (1402); 9.3 row C4 (1898); Integration Checklist (1820); "own small injectable subprocess runner" at line 341. |

Conformance result: 6 of 6 REPRESENTED, 0 OMITTED. No CRITICAL conformance omission.

---

## Part B. Full enumeration (status legend: R = REPRESENTED, D = COVERED-BY-DEDUP, O = OMITTED)

### B.1 research/01-claim-flow-and-session-launch.md (290 lines)

| ID | Finding (source section) | Status | Report location / note |
|---|---|---|---|
| 01-01 | Command is explicit-only; first message of a watcher session must be the literal `/sc:issue --claim <N>` (s1) | R | 124, 163 |
| 01-02 | Claim summary: assigns on GitHub and ClickUp when set, checks accuracy, writes summary and next-steps under `.dev/issues/<N>/`, posts two marked comments, then stops (s1 L15) | R | 183, 515 |
| 01-03 | Both modes post directly; nothing shown for approval (issue.md:18, SKILL.md:74) (s1) | R | 165, 437 |
| 01-04 | `--claim` takes number, `#N` or origin issue URL; no repo option, no dry-run, no preview (s1) | R | 164 |
| 01-05 | Command STOP rules are prose run by the model; none checks the argument is an integer; only `origin_repo.py` checks in code (s1) | R | 166, 202 |
| 01-06 | Claim output files list (`scout.md`, `clickup.json`, `accuracy-check.md`, `issue-summary.md`, analysis, `recommend.md`, `next-steps.md`, `claim-comment.md`) (s1) | R | 187 |
| 01-07 | Hand-off to a person: "open next-steps.md and run its commands in your own session"; nothing runs the steps (s1) | R | 183 |
| 01-08 | Will Not: run any next-step command; will not create labels or ClickUp tasks or touch any repo other than `origin` (s1 L83-84) | R | 183, 186, 200 (repo resolution from origin only) |
| 01-09 | Claim never stages or commits `.dev/issues/` (issue.md:85) and never prints the ClickUp token (SKILL.md:75-76) (s1, s2) | O | Not found in the report (searched `never stage`, `never print`, `.dev/issues`); the `never staged` hits at 1407, 1735, 1829 concern the plan's `.claude/` mirror. MINOR: no plan step depends on it. Part C, O-01. |
| 01-10 | Activation mandatory: `Skill sc:issue-protocol` before any protocol step (s1) | R | 167 |
| 01-11 | Claim writes `.dev/issues/<N>/` into the working checkout, so workspace must be a checkout of the origin repo (s1 key takeaway) | R | 222, 1950 |
| 01-12 | Claim never uses AskUserQuestion even though allowed (SKILL.md:4, :74; create.md:59) (s2) | R | 188 |
| 01-13 | Worker tier pickers `claude-gw-tier3/2/1a`; spawn never passes model; picker not served = STOP `E-TIER-UNAVAILABLE`, no alias fallback; environment dependency (s2) | R | 225, 1858 (Q5), 1953 |
| 01-14 | Because Wave 1 precedes Wave 3, a misconfigured workspace fails every issue without assigning, so the poller re-sees the issue each cycle unless it keeps its own record (s2) | R | 225 ("would fail every issue without assigning it"), 1858 ("attempt cap then abandons each one"), 1953 |
| 01-15 | `<R>` is origin only: not `gh repo set-default`, not fork-parent default, not `--repo`; every gh call passes `--repo <R>`, `gh api` path is `user` or `repos/<R>/` (s2) | R | 344 (Convention A), 1362 |
| 01-16 | Orchestrator (the session) is the only writer; list of write commands (s2 L72) | R | 176, 437 |
| 01-17 | Return contract is chat text printed last, not a file; poller cannot read it; on-disk signals are `next-steps.md` and GitHub assignee/comments (s2) | R | 187, 521 |
| 01-18 | Return-contract field list (`status: success/stopped/failed`, `mode`, `issue_number`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`, `next_steps_path`) (s2 L101-117) | R (partial) | 704 names three of the nine fields (`status`, `issue_number`, `next_steps_path`, "...") and the chat-text-not-file conclusion; the full field list is not reproduced. Withdrawn as an omission: redundant detail. |
| 01-19 | STOP code table: `E-NO-ORIGIN`, `E-FOREIGN-REPO`, `E-GH-AUTH`, `E-NOT-AN-ISSUE`, `E-TIER-UNAVAILABLE`, `E-WORKER-NO-OUTPUT`, `E-ASSIGN-FAILED`, `E-POST-FAILED` (s2) | R (7 of 8) | `E-WORKER-NO-OUTPUT` is never named in the report (no hit); the other seven appear (173-179, 225). Post-Wave-3 failure shape is covered at 214. MINOR sub-detail, recorded as P-2 in Part C. |
| 01-20 | Stops in Waves 0-2 make no GitHub write; after Wave 3 the issue is assigned even if Waves 4-6 fail; re-run repairs (s2 key takeaway) | R | 214, 239 |
| 01-21 | Claim wave table (waves 0-6 with writes) and answer to question 1 (s3) | R | 171-179 |
| 01-22 | Claim never gates on labels or Project status; `labels.md:7`; watcher must do the gating itself (s3) | R | 186, 239 |
| 01-23 | No Project handling in the claim (grep for `gh project|projectV2|graphql` empty), so an issue stays in Backlog after a claim and a Backlog filter keeps seeing it (s3) | R | 186, 1265 |
| 01-24 | `labels.md` fixed set (mode, type, complexity) applied only by `--create`; no trigger or approval label exists; new labels need own `gh label create` lines and cannot go through `/sc:issue` (s4) | R | 334-335, 1406, 1961 |
| 01-25 | No per-person label exists, so a per-person-label routing candidate is also new setup (s4) | R | 1375, 466 |
| 01-26 | `_NUMBER` regex, ASCII digits, no leading zero, no sign, optional `#`, no upper bound; `check_claim` returns int immediately (s5) | R | 195, 202 |
| 01-27 | Accepted/rejected argument forms table (`owner/repo#N`, `0`, `007`, `-5`, `302 extra words`, other host, other repo, `/pull/N`, other path) (s5) | R | 193-199 |
| 01-28 | `read_origin()` uses no `cwd`; non-zero = `E-NO-ORIGIN`; accepted origin URL shapes `https://github.com/o/r[.git][/]` and `git@github.com:o/r[.git][/]` only (s5) | R | 200 covers no-cwd and exit 1; the two accepted origin URL shapes (`https://github.com/o/r[.git][/]`, `git@github.com:o/r[.git][/]`) appear in plan step 3.3 (line 1593). Initially flagged, withdrawn after reading line 1593. |
| 01-29 | Script does not check issue exists/open/is-issue for a bare number; that is Wave 2 (s5) | R | 202 |
| 01-30 | Script validates only the string the model passes; words after the integer in a prompt are read by the model; the watcher must build the prompt itself and never forward issue text; script is a second check (s5) | R | 202, 294, 1361 |
| 01-31 | Integers of any size pass; poller applies own sanity bound from gh JSON `number` (s5) | R | 195, 294, 1361 (`^[1-9][0-9]{0,8}$`), 1842 |
| 01-32 | ClickUp env: token and workspace id required, `CLICKUP_LIST_IDS` and `CLICKUP_MAX_PAGES` (default 20) optional; token personal, header only (s6) | R (partial) | 226, 213 (20 pages); `CLICKUP_LIST_IDS` and `CLICKUP_MAX_PAGES` names not present (0 hits). See P-3 in Part C. |
| 01-33 | ClickUp outcomes: `skipped/no_token`, `no_workspace`, exit 0 for every outcome except bad args, `already_assigned`, `ambiguous`, `error/page_cap`, `error/unexpected`; argument checks; matching rules (issue link in description/custom fields, else `#<N>` whole token in task name) (s6) | R (partial) | `already_assigned` and "skipped" are in the report (213, 226); the other outcomes, exit-0 rule, argument checks and matching rules are absent (0 hits for `ambiguous`, `page_cap`). See P-3 in Part C. |
| 01-34 | ClickUp calls: urllib, 30 s timeout, one 429 retry sleeping `Retry-After` (s6) | R (partial) | 30 s / 20 pages at 521, 1866; the 429 retry is absent (0 hits for `Retry-After`). See P-3 in Part C. |
| 01-35 | ClickUp optional, never blocks the claim; claim comment says "skipped" (s6) | R | 226, 1956 |
| 01-36 | ClickUp identity is the personal token, independent of the `gh` login; no code ties them [UNVERIFIED] (s6) | R | 226, 1887 (Q34) |
| 01-37 | ClickUp step can be slow, so a poller must not assume a claim finishes quickly (s6) | R | 521, 1866 |
| 01-38 | Never-as-worker list text and decision-D3 caveat (s7) | R | 230 |
| 01-39 | "Worker run" definition (Orca preamble with Task ID and Dispatch ID); ordinary sessions not covered; brief guard only in a live-preamble session (s7) | R | 231 |
| 01-40 | `/sc:issue` has no `## Unattended mode` section (s7) | R | 230 |
| 01-41 | WC-13 and WC-9 consequences; the poller must be a plain process outside any Claude session (s7) | R | 232-233, 1364 |
| 01-42 | A poller-launched ordinary session gets no heartbeats, `worker_done`, `return-contract.yaml` or coordinator visibility; dispatching via `worker-start` would violate L23 (s7) | R | 233 |
| 01-43 | "Outside the list" is the researcher's interpretation, not an owner statement [UNVERIFIED] (s7) | R | 233, 1874 (Q21) |
| 01-44 | Where a poller runs (cron/systemd/loop, survives autostop, durable state) is not shown by any repo file (s7 + Gaps 9) | R | 233, 1868 (Q15) |
| 01-45 | Analysis finding F3 (assigns to gh login, stops on other assignee) (s8) | R | 175, 206-207 |
| 01-46 | Analysis finding F4 (cannot be an Orca worker; new top-level session vs typing into coordinator) (s8) | R | 254-265 |
| 01-47 | Analysis finding F5 (claim reads only origin, so multi-repo needs a repo-to-checkout map) (s8) | R | 522 |
| 01-48 | Analysis finding F7 (exactly-once not designed; claim comment is a late record) (s8) | R | 215, 1648 |
| 01-49 | Analysis finding F2 recommends a pull model, consistent with decision A; analysis statement 3 (`--claim --pipeline` design only) checked (s8 and Stale section) | D | Pull model = option A (Section 6.1, 1335); pipeline-design-only at 185. No standalone F2 sentence, which is a labelling detail only. |
| 01-50 | Which login assigns: `--add-assignee @me`, help text, `gh api user -q .login` (s9) | R | 206 |
| 01-51 | Wave 2 edge cases before any write (PR, closed, other assignee, own login) (s9) | R | 175 |
| 01-52 | Four routing candidates table with fit assessment (s9) | R | 1372-1377, 465-470 |
| 01-53 | `gh issue list` has `--assignee`, `--label`, `--search`, `--state`, `--json`, `--limit`; `gh project item-list` has `--query "assignee:octocat -status:Done"` and `--owner` (s9) | R | 781-788, 1265 (item-list), 1374 |
| 01-54 | Cross-login race derived from code: check-then-act, additive `--add-assignee`, both scouts finish before either assignment, both assign (s9) | R | 208 |
| 01-55 | Expected result of the double claim: two assignees, two sessions through Waves 4-6, two separate claim/accuracy-check comments (marker matched only for current login), ClickUp task assigned to both people (s9) | R (partial) | Two assignees at 208, "duplicate sessions and comments" at 1867 and 689-690; "ClickUp task assigned to both people" and the marker-matched-only-for-current-login reason are absent (0 hits "assigned to both"). Sub-detail only, listed in Part C as a partial drop. |
| 01-56 | Race window length = Wave 1 plus spawn, "seconds to minutes"; a 5-minute poll with unsynchronised workspaces makes a collision possible but not frequent (s9) | O | Report says the window "was not measured" (498, 1428, 1866) but never carries the seconds-to-minutes estimate or the possible-not-frequent likelihood (0 hits for `seconds to minutes`, `frequent`). IMPORTANT (borderline): a derived estimate that bears on revisit condition 4. Part C, O-04. |
| 01-57 | Poller-side reservation suggestion (add `@me`, re-read assignees, back off if not sole, deterministic lowest-login tie-break), UNVERIFIED and untested (s9) | R | 1381 (names add `@me`, re-read, back off, deterministic tie-break; "lowest login" example not stated, trivial) |
| 01-58 | Same-login race: both pass `claim.md:42`, both post new comments because marker lookup (Wave 1) precedes post (Wave 6); dispatch record must then be on GitHub, not local (s9) | R | 208, 1867 (Q14), 1409 |
| 01-59 | Question-2 key takeaways (candidate 1 is the routing the claim understands; 2 and 3 need setup; 4 is a race; poller selecting only own-login issues never meets the other-assignee stop) (s9) | R | 1381, 1379, 207 |
| 01-60 | Reconciliation pointer: single predicate (skip other-login assigned) vs candidate selectors; candidate 1 re-selects after post-Wave-3 failure, candidate 4 strands it (s9) | R | 207, 1379, 1377, 1374 |
| 01-61 | Marked comments end with `<!-- sc:issue:accuracy-check -->` / `<!-- sc:issue:claim -->`; re-run edits latest earlier comment by PATCH, same login only (s10) | R | 212 |
| 01-62 | Re-claim allowed; ClickUp idempotent; full re-run not idempotent in cost; `<D>` already existing tolerated? [UNVERIFIED]; output files refilled from templates (SKILL.md:50) (s10) | R (partial) | 213, 1871 (Q18). The "refilled from templates" clause is absent; trivial, P-5 in Part C. |
| 01-63 | At-most-once across workspaces: none; claim comment is a late record (s10) | R | 216, 215 |
| 01-64 | Post-Wave-3 failure leaves issue assigned with no claim comment; candidate 1 re-selects every cycle; needs durable record with retry cap (s10) | R | 214, 1374, 1866 (Q13 `max_attempts`) |
| 01-65 | `next-steps.md` is local to the checkout: proves a claim finished in that checkout, not elsewhere (s10) | R | 704 (gap row G22: "`next-steps.md` proves a claim finished only in that checkout (file 01 section 10)"). Initially flagged as omitted after a phrase search; withdrawn after reading Section 4. |
| 01-66 | Duplicate-dispatch damage limited to cost and, across logins, to duplicate comments and double assignment; dispatch record written before launch and survives restart (s10 key takeaways) | R | 1409, 1824, 306 |
| 01-67 | Environment a claim needs list (origin remote, uv, gh auth, fetch, installed skills/agents, picker IDs, ClickUp) (s11) | R | 218-226 |
| 01-68 | No terminal is required by the claim itself; Claude Code session needs one only because Orca starts it as a terminal agent; nothing needs a person at the keyboard (s11) | O | Not found (0 hits for `keyboard`). MINOR, O-06. The non-interactive property itself is covered (188, 238). |
| 01-69 | Interactivity: `/sc:recommend` questions go to `recommend.md`; residual prompts are tool-permission prompts; Orca default args; reconciled ccsession permission wording; name question not asked with a prompt (s11) | R | 188, 263, 300, 425 |
| 01-70 | Why the claim stops: B2 locations; test file has no hit; removing B2 plus `--claim --pipeline` interface plus launch-level guard needed to run next steps (s11) | R | 183, 185, 189 |
| 01-71 | `--claim --pipeline` is design only; only implemented piece is `launch-job-identity.sh`; `launch-level-guard.sh` absent (s11) | R | 185, 391-393, 397 |
| 01-72 | Entry-point table (agent launch, ccsession-orca, `claude --print`, orchestration send, terminal send) (s12) | R | 246-252 |
| 01-73 | New session vs typing into live coordinator tradeoff, F4 (s12) | R | 254-265, 1385-1390 |
| 01-74 | `orca agent launch` contract table (14 rows) (s12) | R | 267-287 |
| 01-75 | What the mock must do (s12) | R | 289, 1404 |
| 01-76 | Lost reply: dispatch record before launch, treat as dispatched, never relaunch fresh; poller needs `--worktree path:<abs>` (s12 key takeaways) | R | 305-307 |
| 01-77 | Prompt contract: single line `/sc:issue --claim <positive int>`, built via `int()`, argv list, not read as option by `ccsession-orca` (lines 110, 116, 119) (s13) | R | 291-296 |
| 01-78 | Integer-only protects the prompt, not the claim's own reading of issue text (workers have Bash); the approval gate is the real boundary (s13) | R | 296, 443, 504, 1366 |
| 01-79 | Gaps 1-8 (live slash command test, argv vs paste, same-login workspaces, Coder facts, org Project token, tests pin stop text, `<D>` tolerated, `claude --print`) (Gaps) | R | Q1, Q2, Q14, Q5, Q7, Q19, Q18, Q20 (1854-1873); Appendix A.1 items 1-8 |
| 01-80 | Gap 9: where the 5-minute poller runs and keeps its dispatch record, with sub-items (a)-(d) (Gaps) | R | 1868 (Q15), 1429, 233 |
| 01-81 | Tagged claims list: CODE-CONTRADICTED full-orchestration expectation; UNVERIFIED items (outside-list reading, argv vs paste, multi-assignee, sessions stay open, same-login, `--print`); `--claim --pipeline` design only (Gaps) | R | C1 (1895), Q21 (1874), Q2, Q14, Q20 |
| 01-82 | Stale-doc notes: no stale among files read; `orca-capabilities.md` team-written inventory risk; analysis L26 label claim not re-read live; design doc "authoritative for new planning" but guard "proposed" and absent; F2 consistent (Stale section) | R / D | 712, 1901 (C7) ; live label list was re-read by 02 and appears at 334; design-doc status at 390-391 |
| 01-83 | Summary paragraph (claim non-interactive, claim-only, validation, no mutual exclusion, launch route, three unverified items) | D | Carried by 2.1, 2.2, 2.5 and Section 7 |

File 01 tally: 83 findings enumerated (01-01 to 01-83). Omitted (status O): 01-09, 01-56, 01-68 (3). Covered-by-dedup: 01-49, 01-83 (2). Represented: 78, of which partial (sub-detail dropped, listed in Part C): 01-18, 01-19, 01-32, 01-33, 01-34, 01-55, 01-62. Row-level counts are rolled up in Part D.

### B.2 research/02-github-surface-and-cli-patterns.md (231 lines)

| ID | Finding (source section) | Status | Report location / note |
|---|---|---|---|
| 02-01 | `.github/workflows/` holds exactly four files (README, boundary-guard, contract3, test) (s1) | R | 319 |
| 02-02 | Trigger table for the three workflows with line numbers (s1) | R | 313-317 |
| 02-03 | No `schedule:`, `cron:`, `issues:`, `workflow_run:`, `pull_request_target:` anywhere; `workflow_dispatch` only at `test.yml:8` (s1) | R | 319 |
| 02-04 | Job skeleton to copy (runs-on, checkout@v4, setup-uv@v10.3.2, Python 3.10, `uv pip install -e ".[dev]"`, `make sync-dev`) and least-privilege precedent (`permissions: contents: read`, `persist-credentials: false`) (s1) | R | 320 |
| 02-05 | `contract3-generator-constraint-lint.yml:35` sets `timeout-minutes: 5` (s1) | O | Not found. MINOR (option B/D workflow detail). O-09. |
| 02-06 | `test-summary` needs list; new job must be added to `needs` (s1) | R | 321 |
| 02-07 | `.github/workflows/README.md` documents three workflows; "Adding a New Workflow" (l.120-125) asks for documentation; README matches directory (s1) | R | 321 |
| 02-08 | README best practices (l.137-143): pin action versions, add `workflow_dispatch` for debugging (s1) | O | Not found (0 hits "Pin action versions"). MINOR; the report does carry "pin by tag" implicitly in 320 only as a skeleton. O-09. |
| 02-09 | Under option A no workflow is required; option B would be the first schedule/issue workflow and must follow README (s1) | R | 322, 379 |
| 02-10 | Issue form table (bug_report, feature_request, other, config) with `type:` and `labels:` (s2) | R | 326-331 |
| 02-11 | Blank issues disabled, so every issue arrives through a form or `gh issue create` (s2) | R | 331 (`blank_issues_enabled: false`), 333, and 712 (gap row G30: "`config.yml` disables blank issues, so every issue arrives through one of three forms or `gh issue create`"). |
| 02-12 | Native issue `type:` field (Bug/Feature) is a second discriminator; `gh issue list --json issueType` (s2) | R | 336 (field verified there; upgraded from UNVERIFIED) |
| 02-13 | Forms inherited from Orca; no field or label for approval or readiness (s2) | R | 333, 712 |
| 02-14 | Live label list: exactly 9 GitHub defaults; origin URL is the fork (s2) | R | 334 |
| 02-15 | Implication: new labels via documented `gh label create`, or Project v2 Status (needs `project` scope [UNVERIFIED]); label approval needs a check of who applied the label (events API `labeled` actor, not exercised) (s2) | R | 336, 459, 1262-1263, 1363 |
| 02-16 | Hard line: select by label/Project state, then pass only the integer `number` onward (s2) | R | 346, 1362 |
| 02-17 | `labels.md:9-13` fixed label set; `:7` never creates, `--claim` changes none; `:22-42` one-time maintainer lines; fork lacks `type:*` and `complexity:*` so `--create` reports `not applied: label missing in repo` (`labels.md:20`) (s2b) | R | 334-335 |
| 02-18 | Claim semantics the poller depends on (Wave 0 origin_repo, `gh auth status`, Wave 2 edge cases, Wave 3 `@me`); free ownership signal; skip assigned-to-other (s2b) | R | 175, 207 |
| 02-19 | Session must run in a checkout whose `origin` is the fork else `E-NO-ORIGIN` exit 1 (s2b) | R | 200, 222 |
| 02-20 | `_NUMBER` + `check_claim` already implement integer-only validation; poller may reuse the regex shape but must validate the integer itself (s2b) | R | 294, 1361 |
| 02-21 | Key takeaways 2b: ship `gh label create` lines in house format; pre-filter only on assigned-to-someone-else (s2b) | R | 1406, 207 |
| 02-22 | 2c reconciliation of "skip issues that already have an assignee" with files 01/03: single predicate, role per candidate, per-candidate failure shapes (candidate 1 re-selects each cycle after post-Wave-3 failure; candidate 4 strands) (s2c) | R | 207, 1374, 1377, 1379, 1905 (C11) |
| 02-23 | Owner's ADDENDUM 2 names no routing candidate; whether later decision does is UNVERIFIED (s2c) | R | 1381, 1423 |
| 02-24 | `ci.py` imports (l.10-15), docstring "Pure ... NFR-6", function list (s3.1) | R (partial) | 340 carries imports and purity; function list omitted, trivial. |
| 02-25 | No other `pr_submit` module imports `subprocess`; list of the 21 files (s3.1) | R (partial) | 341 carries the claim; file list omitted, trivial. |
| 02-26 | Only gh seam: `detection._fetch_payload` stub; tests patch it; `mock_gh` used in 3 test files (s3.1) | R | 342, 359 |
| 02-27 | STALE DOC: `conftest.py:3-4` mock_gh description (s3.1) | R | 342, 1899 (C5) |
| 02-28 | Whole-`src/superclaude` search: 21 files import subprocess (names listed) (s3.2) | O | Report states the conclusion (no Python module builds `gh`) but not the list or the count of subprocess importers (0 hits "21 files"). MINOR. O-10. |
| 02-29 | Only `.py` hit for literal `gh` is a docstring at `origin_repo.py:14`; `shutil.which("gh")` nowhere in `src`/`tests` (s3.2) | R | 341 |
| 02-30 | Expected answer none found; poller needs its own injectable runner (s3.2) | R | 341, 380, 1402 |
| 02-31 | Nearest Python subprocess pattern `origin_repo.py` details and its test (s3.2) | R | 345 |
| 02-32 | Other styles: `cli/swarm/tmux.py`, `cli/sprint/notify.py`, injectable `Callable` aliases (s3.2) | R | 345 |
| 02-33 | Several CLI modules guard on `shutil.which("<tool>")` (`reflect/runner.py:387`, `reflect/commands.py:494`, `install_codegraph.py:104,156`, `install_retired_mcp.py:407`) (s3.2) | O | Not found (0 hits for `reflect/runner`). The report cites a stronger precedent (`install_user_setup._find_orca`, 341), so impact is low. MINOR. O-10. |
| 02-34 | No Python code calls `orca`; `doctor.py:61-77` is a filesystem check; `orca agent launch` appears only in docs/specs; flag list not read live (s3.2) | R | 341, 513 (live help was read by file 01, so the gap is closed in 267-287) |
| 02-35 | 136 `gh` occurrences in 23 non-`.py` files with top-file counts (s3.3) | O | Not found. MINOR. O-10. |
| 02-36 | Shell scripts list with example `gh` lines; "All gh I/O is isolated here (NFR-6)" (s3.3) | R (partial) | 343 names the scripts and the NFR-6 quote; per-line examples omitted, trivial. |
| 02-37 | Convention A (skills, `--repo <R>`, `repos/<R>/`) and Convention B (`gh repo view` fallback unsafe for fork) (s3.3) | R | 344 |
| 02-38 | Write-capable `gh` calls are made by the claim session, not the poller; poller needs reads only with minimal fields `number,labels,assignees,state`, no title/body (s3.3) | R | 346, 1362 |
| 02-39 | Test stubs table (five files) (s3.4) | R | 350-356 |
| 02-40 | `ALLOWED_PROGRAMS`; repo-scoping regex tests in `test_static_grep.py` (s3.4) | R | 358 |
| 02-41 | PATH-stub is the repo's actual mocking technique; stubs fail loudly; `assert_no_retrigger_call` tokens (s3.4) | R | 357-358 |
| 02-42 | In-process seam patches payload only; no Python-level injectable-runner test for `gh`; conftest says in-process preferred but PATH-shim is used (s3.4) | R | 359 |
| 02-43 | For a Python poller both techniques work; pattern (2) proves the argv reaching `orca` has only an integer (s3.4) | R | 1403, 1561 |
| 02-44 | Key takeaways s3 (ci.py not a wrapper; gh I/O in bash/protocol prose; nearest pattern; PATH stubs) (s3) | R | 380 |
| 02-45 | Registration pattern in `main.py`, 11 registrations in order, noqa marker, ruff `select` (s4.1) | R | 363 |
| 02-46 | New block after l.561; top-level verb; per-group test convention (`tests/swarm/test_cli_registration.py:74`) (s4.1) | R | 382, 365, 1516 |
| 02-47 | Other `from .x import` lines in `main.py` are function-local, not registrations (s4.1) | O | Not found. MINOR (negative detail). O-10. |
| 02-48 | Chosen example `cli/recommend/` (12 files, 1,784 lines, per-file sizes) and single-file alternative `init_lite.py` (s4.2) | R | 364, 1400 |
| 02-49 | Rejected examples with reasons: `swarm/` 11,799 lines, `eval/` 11,367, `cleanup_audit/` 1,820 and a Claude-pipeline executor (s4.2) | O | Not found (0 hits "11,799", "1,820"). MINOR; the choice of `recommend/` is carried, the rationale for not picking others is not. O-10. |
| 02-50 | Lazy `__getattr__` export (`recommend`, `tasklist`) vs eager import (`cleanup_audit`): both styles in use (s4.2) | R (partial) | 364 mentions the lazy export for `recommend`; "both styles in use" omitted. MINOR. O-10. |
| 02-51 | Group definition and option style, nested groups, `--dry-run` precedent that returns before any side effect (s4.2) | R | 364 |
| 02-52 | Minimal layout derived from `tasklist/` (5 files, 771 lines) and `recommend/`; docstring first-line convention (s4.2) | R (partial) | 1400, 1513, 1557 (docstring convention); `tasklist/` as second model omitted, trivial. |
| 02-53 | Packaging: hatch `packages = ["src/superclaude"]`, no `pyproject.toml` change, runtime deps, stdlib-only poller leaves `verify-deps` baseline unchanged (s4.2) | R | 364, 1819, 1551 (`scripts/dependency_baseline.txt` not named; trivial) |
| 02-54 | Registration tests: frozen set contents, `--help` test only, CODE-CONTRADICTED comment, per-group tests (s4.3) | R | 365, 1899 |
| 02-55 | Tests layout: package dirs + `tests/cli/`; directory listing (s5) | R | 369 |
| 02-56 | pytest config (`testpaths`, `--strict-markers`), `_pollution_snapshot` (s5) | R | 369, 1735 |
| 02-57 | `tests/pr_submit/` layout: 43 files, conftest fixtures (`load_fixture`, `mock_gh`, `mock_monitor`, `fixture_findings`, `tmp_skill_dir`, gate-helper registry "pr_submit-specific, not reusable"); `test_ci_classify.py` pure-function model (s5) | R (partial) | `test_ci_classify` and `load_fixture` covered (369, 1561); `mock_monitor`, `fixture_findings`, `tmp_skill_dir` and the not-reusable gate registry omitted (0 hits "mock_monitor"). MINOR. O-10. |
| 02-58 | `gh` mocked by PATH stubs; no reusable Python-level mock (s5) | R | 357-359 |
| 02-59 | Recommended test shape (a) pure unit, (b) injectable runner with no write-shaped call, (c) CliRunner e2e with fake `gh`/`orca` (s5) | R | 1403 |
| 02-60 | Makefile/CI table: `test`, `lint`, `format`, `sync-dev`, `verify-sync`, `lint-architecture`, `verify-deps` with CI counterparts (s6) | R | 370, 1735 (CI pytest flags) |
| 02-61 | `lint-architecture` Checks 3/4 (command size warn 200/error 500), 6, 8 (frontmatter `name`, `description`, `allowed-tools`), 9 (name ends `-protocol`) (s6) | O | Only Checks 1/2 are carried (371; 0 hits "frontmatter"). MINOR; relevant only if a command or skill is added, which the plan avoids. O-10. |
| 02-62 | `.claude/` mirror rule implications (a)-(d); pure CLI package avoids (b)-(d); tests `test_routing_refresh.py` and `test_how_we_work_routing_table.py` (s6) | R | 371, 1407, 1593 |
| 02-63 | Ruff scope (`line-length 88`, py310, `exclude docs/`, `extend-exclude .dev/`), `E501` ignored, Python 3.10 compatibility rules (no 3.11-only features, no `tomllib`, `X | None` only with `from __future__ import annotations`) (s6) | R (partial) | 370, 1407, 1469. `E501` ignored (pyproject l.186) not stated (0 hits). Trivial. |
| 02-64 | All Python through `uv run`; PRs only via `/sc:pr-submit --monitor 3` (s6) | R | 1826, 1829 |
| 02-65 | Key takeaways s6 (gates list; pure `cli/` code outside mirror) (s6) | R | 371, 1407 |
| 02-66 | Three design docs, three headers; `sc-issue-command.md` 20-section structure with bold-label header block; launch-level doc YAML front matter (better for open items); `prd-spec-flag.md` lightest (s7) | R | 375 |
| 02-67 | Recommendation: follow `sc-issue-command.md` skeleton + status block, Coder#477 and B/C as follow-up section, UNVERIFIED section style (s7) | R | 1405 |
| 02-68 | Design doc header "Next: /sc:workflow ... then /sc:implement" (design -> workflow -> implement, level 3) (s7) | R | 375 |
| 02-69 | CODE-VERIFIED design's claims about repo files still hold; UNVERIFIED picker-ID table vs `ccsession-models.json` (s7) | O | Not found (0 hits "ccsession-models"). MINOR. O-11. |
| 02-70 | Key takeaways s7: place design at `docs/designs/<name>.md`, precedent D1 of `sc-issue-command.md:418` (s7) | R (partial) | 1512 places the file; the D1 precedent citation is omitted. Trivial. |
| 02-71 | Gaps 1-10 (orca flags, GitHub fields/scope, `labeled` events, three CODE-CONTRADICTED items, missing `type:*` labels decision, label-name/Status mapping, org Project read, same-developer race) (Gaps) | R | Q8, Q7, Q11, C4, C5, Q9, Q14, Appendix A; gap 7 "whether the owner wants the `type:*`/`complexity:*` labels created alongside" is carried as a fact in Q9 (1862) and in 334, decision implicit under "Owner supplies the names" |
| 02-72 | Stale-doc list (conftest, ci.py note, test_cli_registration comment, workflow README minor, forms Orca text) (Stale) | R | 342, 1898-1899, 1901, 1967 |
| 02-73 | Summary paragraph (s Summary) | D | Carried by 2.3 and 7.6 |

File 02 tally: 73 findings enumerated (02-01 to 02-73). Omitted (status O): 02-05, 02-08, 02-28, 02-33, 02-35, 02-47, 02-49, 02-61, 02-69 (9). Covered-by-dedup: 02-73 (1). Represented: 63, of which partial: 02-24, 02-25, 02-36, 02-50, 02-52, 02-57, 02-63, 02-70.

### B.3 research/03-governance-and-security-surface.md (233 lines)

| ID | Finding (source section) | Status | Report location / note |
|---|---|---|---|
| 03-01 | Launch-level design self-description: "design draft; scoped job identity foundation implemented; full enforcement pending", `adversarial_status: partial`, `planning_status` conditional on B-CTX, "not runtime-approved" banner (s1.1) | R | 390 |
| 03-02 | Levels W/WA/F/FS; no level authorizes merge or push to master/main; threat model TH1/TH2, TH3 out of scope; "same-user guardrail, not a sandbox" (s1.1) | R | 399 |
| 03-03 | `launch-level-guard.sh` does not exist (Glob empty) though L23 states it in present tense (s1.2) | R | 391 |
| 03-04 | `hooks.json` has no `launch-level-guard` entries; only launch-job-identity at 96-105 (s1.2) | R | 392 |
| 03-05 | `/sc:issue --claim --pipeline` does not exist (issue.md:35-41; design admits at :34) (s1.2) | R | 393 |
| 03-06 | `[sc-launch:v1:<nonce>]` marker and `pending/<nonce>` store: no producer or consumer (s1.2) | R | 394 |
| 03-07 | `UserPromptSubmit` binding and `.ok` approval file not in code (s1.2) | R | 395 |
| 03-08 | L2 shared `hooks/pre-push` not in code (14 scripts, none) (s1.2) | R | 396 |
| 03-09 | Job identity foundation CODE-VERIFIED: 566 lines, function line ranges, registered at hooks.json:96-105 (s1.2) | R | 397 |
| 03-10 | Adapter returns `updatedInput` without `permissionDecision` (s1.2) | R | 397 |
| 03-11 | Ordinary or unbound sessions untouched (fast exit, non-Bash, invalid sid, missing sessions/<sid>) (s1.2) | R | 397 |
| 03-12 | Fresh Bash per governed call; cwd not persisted (`os.execv('/bin/bash', ['bash','-c', ...])`) (s1.2) | O | Not found (0 hits for `fresh Bash`, `execv`, `setsid`). MINOR: irrelevant to a claim-only watcher. O-12. |
| 03-13 | "Same-user, not a sandbox" at script line 2; deliberate `setsid`/daemonization escapes selection (s1.2) | R (partial) | 397 carries line 2 wording; the `setsid` escape is omitted. Trivial, O-12. |
| 03-14 | B-CTX gate: pre-push hook has no Claude session id; invariant "ordinary human push never restricted"; environment values never sufficient authority (s1.3) | R | 400 |
| 03-15 | B-CTX completion evidence is a log-only probe over process trees (main/subagent/nested/background Bash, Monitor-to-Git, human terminal, detached jobs, PID reuse, resume, /clear/fork, release while a job is alive); "no single PID-label lookup is accepted" (s1.3) | R (partial) | 400 states "completion evidence is a log-only probe (:504)"; the scenario list is omitted. MINOR, O-12. |
| 03-16 | B-CTX verdict "OPEN/BLOCKING"; scoped 19.7 integration is not a retroactive PASS; order-of-work step 0 (s1.3) | R | 400 |
| 03-17 | B-CTX gates only pipeline levels; a claim without `--pipeline` is unaffected (design :349, :355) (s1.3) | R | 400, 502, 1354 |
| 03-18 | Key takeaways s1: only job-identity adapter implemented; adapter never denies on policy, acts only when `sessions/<sid>` exists, nothing creates it, so no launch level constrains any session; design excludes hostile agent (TH3, R12 :450) (s1) | R | 401, 421, 484, 502 |
| 03-19 | Registration surfaces table (project settings, packaged hooks.json, installer list, workspace global settings) (s2.1) | R | 408-411 |
| 03-20 | CODE-CONTRADICTED by installed state: adapter script not installed or registered on this workspace; cause unestablished (s2.1) | R | 413, 1897 (C3), 1886 (Q33) |
| 03-21 | Per-control table: block-bare-python (ceilings at 48-61), freshness-pre-edit, reject-workspace-writes, sc-recommend-phase0, launch-job-identity, absent guard/pre-push, ccsession launch flags (s2.2) | R | 417-423 (ceilings referenced by line range; the individual ceilings are not listed, trivial) |
| 03-22 | Permission mode decided by three inputs (ccsession variables, Orca `agentDefaultArgs`, whether Orca runs `ccsession-orca`); `CCSESSION_PERMISSIONS=default` alone does not stall; `CC_CLAUDE_FLAGS` replaces wrapper flags; CLI-route application of `agentDefaultArgs` untraced (s2.2 amendment) | R | 300, 423, 425, 1859 (Q6) |
| 03-23 | No permission allow/deny list at any level read; default mode stalls vs ccsession default unrestricted; no middle option (s2.3) | R | 425 |
| 03-24 | No hook restricts `gh`, `git`, file reads or network; master unprotected (404, rulesets `[]`, rules/branches `[]`) (s2.3) | R | 426 |
| 03-25 | `gh` OAuth token in `hosts.yml` mode 600, scopes `gist, read:org, repo, workflow`, readable by any Bash/Read in the session (s2.3) | R | 427 |
| 03-26 | `ccsession.env` can hold proxy URL and auth tokens (s2.3) | R | 427 |
| 03-27 | Key takeaways s2: nothing stops reading secrets, using full-scope token, pushing to master; unattended permission posture undefined; "registered in hooks.json" not equal "active on the host" (s2) | R | 503, 425, 413 |
| 03-28 | Prompt boundary: command STOP rules do not constrain digits; `origin_repo.py` check is inside the session after the prompt arrived; poller must validate first; no upper bound (s3.1) | R | 433, 202, 496 |
| 03-29 | `orca agent launch` prompt is one free-text argument; there is no flag for a permission mode or an allowed-tool list (s3.1) | O | The flag set is listed (271) but the negative finding (no permission-mode or allowed-tools flag, so the launch cannot constrain the session) is not stated (0 hits "no flag for a permission"; the only `allowedTools` hits are about the headless route, 300, 423, 873, 1114). Distinct secondary security fact, directly feeding Q6. O-05. |
| 03-30 | `ccsession-orca` first-non-flag/`--prefill`/`--` handling; a prompt beginning with `/` is read as the task; prefill vs submit unverified; a prefilled prompt would not run unattended (s3.1) | R | 295, 1855, 702 |
| 03-31 | Six paths for untrusted text (launch prompt, Wave 1, Wave 4, Wave 5, Wave 6, ClickUp) (s3.2) | R | 431-438 |
| 03-32 | Worker tool sets; "read-only on GitHub", "write only under `.dev/issues/`" and "fetch origin only" limits are prompt text, not enforcement; t2/t1 files unread (s3.2) | R | 440 |
| 03-33 | Claim asks the user nothing, so a claim session runs to completion without a human, the property an automated trigger inherits (s3.2) | D | 188, 238, 1366 |
| 03-34 | Repository is PUBLIC (`gh repo view`), so issue text is authored by the public (s3.3) | R | 125, 441 |
| 03-35 | Approval controls only whether the watcher fires; claim reads live, including post-approval comments and edited body; detectability of edits UNVERIFIED (s3.3) | R | 442 |
| 03-36 | `author_association` observed (`MEMBER`) on the issue; poller can refuse non-OWNER/MEMBER/COLLABORATOR authors; comment association unchecked (s3.3) | R | 442, 1865 |
| 03-37 | Wave 6 is itself an outbound channel: unreviewed worker text posted to a public issue (s3.3) | R | 437, 1366 |
| 03-38 | Key takeaways s3: integer-only protects the prompt not the session; second part needed (claim-side change or accepted-risk statement); in-session validation only; approval not tied to text version (s3) | R | 443, 504, 1366, 1865 |
| 03-39 | No approval or routing mechanism in code; only "approved" is the typed prompt of the unimplemented design (:186-195); grep for `add-label`/`remove-label` empty; existing 9 labels (s4.1) | R | 447, 334, 186 |
| 03-40 | Authority table: open/comment = Read; apply/dismiss labels = Triage; create/edit/delete labels = Write; close/reopen/assign = Triage; be assigned = Read or higher; Project move/Status and edit-another's-body not stated (s4.2) | R (partial) | 449-456 carry all rows except "be assigned: Read or higher"; its substance is carried by 465 ("A Read-role user can be assigned but cannot self-assign"). Trivial. |
| 03-41 | Collaborators: 1 admin, 2 maintain, 8 read, 0 triage, so at least 3 accounts can label or assign; read-role accounts can open and comment but not label; org owners not enumerated (s4.2) | R | 458 |
| 03-42 | #331 events listing with actor and time for labeled/assigned/Project changes; status value text unverified (s4.2) | R | 459 |
| 03-43 | `gh project list --owner IronbellyOrg` failed: token lacks `read:project` (`gh auth refresh -s read:project` needed) (s4.2) | R | 460, 692, 1860 |
| 03-44 | Routing inputs table (assignee / per-person label / Project field) with who can set each and weakness (s4.3) | R | 463-467 |
| 03-45 | Mis-routed launch cannot take another person's issue (Wave 2 stops) but can claim an unassigned issue for the wrong login (s4.3) | R | 469 |
| 03-46 | Reconciliation pointer to R02 2c; "assigned to own login" in s7 is the routing-by-assignee row not first-come (s4.3) | R | 207, 470 |
| 03-47 | Key takeaways s4: human-approved = GitHub act by Triage-or-higher (3 accounts), no allow-list/label/code reading the label actor, events API supplies actor; assignee is the one routing input the claim respects; Project/Backlog unreadable with this token (s4) | R | 505, 491-492, 465 |
| 03-48 | Never-as-worker list, worker-run definition, brief guard only inside a live preamble (s5) | R | 230-231 |
| 03-49 | WC-8 and WC-13: `agent launch` must not be called from inside a worker session or a command; poller must be a plain process outside any Claude session (s5) | R | 232-233, 1364 |
| 03-50 | WC-9 (`:40`): outward actions off under `--unattended`, "no brief can turn it on (decision D4)"; claim assigns and posts two comments, which is why it cannot be a worker; watcher makes those writes in a session no coordinator planned (s5) | R (partial) | 232 carries WC-9 and "applies to worker runs only". The "decision D4 / no brief can turn it on" phrase and the explicit "why it cannot be a worker" rationale are absent (the only `D4` hit, 1844, is the report's own D4). MINOR, O-12. |
| 03-51 | Coordinator rule `WORKER-CONTRACT.md:112` has no category for a standing authorization by an approver's label; policy gap; design must state its own basis (claim's writes are the full extent) (s5) | R | 234, 1889 (Q36), 1973 |
| 03-52 | Worker model need not be extended for claim-only A; `agent launch` of a top-level session is the documented route (s5) | D | 1364, 1390 (dispatch through `worker-start` forbidden; route table) |
| 03-53 | Orca hazard: link flags `--issue`/`--pr`; `issue:<number>` selector may link; use `path:` or `name:` (s5) | R | 301, 1409, 1436, 1870 (Q17) |
| 03-54 | Key takeaways s5: poller outside Claude; Worker Contract does not govern that session so limits come from poller/launch flags/GitHub authority; "live conversation" basis does not describe an automated trigger (s5) | R | 506, 233, 234 |
| 03-55 | Capability inventory of a prompt-injected session (7 rows) (s6) | R | 474-482 |
| 03-56 | Mitigating facts (fixed prompt, claim stops after next-steps, refusals, threat model excludes TH3) (s6) | R | 484, 1366 |
| 03-57 | Key takeaways s6: injection in a bypass-mode session has owner's full access; most contained shape = approver-only trigger, integer-only prompt, issue/comment authors restricted by `author_association`, explicit permission-mode decision (s6) | D | Each element is carried (1359-1363 security model, 442, Q6 1859, Q12 1865, 1366); the one-sentence "most contained shape" synthesis is not stated as such. Covered by the Section 7.3 security model. |
| 03-58 | Security properties table: authentication, authorization to approve, authorization to route, at-most-once, auditability, containment, input validation (s7) | R | 488-496 |
| 03-59 | Key takeaways s7: identity tie is the `gh` token (simple, but also what an injected session can read); at-most-once built into poller, safe by claim idempotence not locking; approval authorization needs label-event actors (s7) | R | 490, 493, 1409, 1363 |
| 03-60 | Additional checks: plugin mirror byte-identical (`cmp`); `tests/hooks/test_launch_job_identity.py` exists; installer coverage unverified (s7 tail) | R | 402 |
| 03-61 | Gaps 1-3 (guard absent / `--pipeline` absent / hook not installed on host) (Gaps) | R | 391-393, 413, 1896-1897 (C2, C3), 1886 (Q33) |
| 03-62 | Gaps 4-5 (prefill vs submit; per-host Claude command, permission variables, `agentDefaultArgs`) (Gaps) | R | 1855 (Q2), 1858-1859 (Q5, Q6) |
| 03-63 | Gaps 6-9 (policy for claim's own reads; body-edit and comment association; Project permissions and status events; org owners and body-edit permission) (Gaps) | R | 1865 (Q12), 1864 (Q11), 1860-1861 (Q7, Q8), 1878 (Q25) |
| 03-64 | Gaps 10-12 (approver allow-list; at-most-once local state vs marker; `issue:<number>` linking) (Gaps) | R | 1863 (Q10), 1866 (Q13), 1857 (Q4), 1870 (Q17) |
| 03-65 | Gaps 13-15 (files not read; Coder-side tie; where the poller runs and keeps state, sub-items a-d) (Gaps) | R | 1875 (Q22), 1869 (Q16), 1868 (Q15) |
| 03-66 | WEB SEARCH PROVENANCE header: WebSearch/WebFetch used because Tavily was unavailable; only for repository-role documentation (header) | R | 1911, 754, 1007 |
| 03-67 | Stale docs: project CLAUDE.md "private fork" vs PUBLIC; design L23 present-tense overstatement; `hooks/README.md:3-19`; consistent-with-code notes (Stale) | R | 441, 391, 709, 1900-1901 (C6, C7). The "consistent with code" negative note is not carried; trivial. |
| 03-68 | Summary paragraph (s Summary) | D | Carried by 2.4 key findings (500-506) and Section 7 |

File 03 tally: 68 findings enumerated (03-01 to 03-68). Omitted (status O): 03-12, 03-29 (2). Covered-by-dedup: 03-33, 03-52, 03-57, 03-68 (4). Represented: 62, of which partial: 03-13, 03-15, 03-40, 03-50.

### B.4 gaps-and-questions.md (42 lines: 24 gap rows + 9 stale-documentation bullets)

Method: each gap row is mapped by meaning to the Section 9 question or correction that carries its substance. The report states this mapping itself (line 1992), which I verified row by row rather than accepting.

| ID | Finding | Status | Report location / note |
|---|---|---|---|
| GQ-01 | Does `/sc:issue --claim <N>` run as the initial prompt of `orca agent launch --prompt` (slash command executed, submitted)? one owner-run live test | R | 1854 (Q1), 2008 |
| GQ-02 | Argv vs typed-paste delivery; JSON shape and real error body of `agent launch` | R | 1855 (Q2), 2009 |
| GQ-03 | Same-login race and two workspaces racing for an unassigned issue; double-claim derived from code | R | 1867 (Q14), 1857 (Q4), 208, 2010 |
| GQ-04 | Coder workspace facts (Orca runtime, `ccsession-orca`, tier IDs, permission mode, `gh` identity, ClickUp variables) | R | 1858 (Q5), 1859 (Q6), 2011 |
| GQ-05 | Can the workspace `gh` token read the org Project (`read:project` missing); label-only selection avoids the question | R | 1860 (Q7), 1862 (Q9 `--label-only`), 2012 |
| GQ-06 | Do tests pin the claim-stops-after-`next-steps.md` text (one file searched) | R | 1872 (Q19), 189 |
| GQ-07 | Is an already existing `<D>` tolerated on re-run | R | 1871 (Q18), 213 |
| GQ-08 | Does `--claim` work under `claude --print` | R | 1873 (Q20) |
| GQ-09 | Where the 5-minute poller runs and keeps its dispatch record; whole "Coder-side listener"; assigned to web-02 | R | 1868 (Q15), 1429, 121, 233 |
| GQ-10 | `labeled` events as "who approved" signal; comment `author_association`; post-approval body edit detectable | R | 1864 (Q11), 442, 459 |
| GQ-11 | `gh issue list --json` field set incl. native issue type; Project v2 field/Status access; OAuth scope | R | 336 (field set verified), 1861 (Q8), 1860 (Q7) |
| GQ-12 | Trigger/approval label names and Project/Status mapping undefined; fork lacks `type:*`/`complexity:*` labels; setup instructions only | R | 1862 (Q9), 334, 1406 |
| GQ-13 | Policy for the claim's own reads of title/body/comments (accept, restrict by author, lock conversation, change claim) | R | 1865 (Q12), 443, 1426 |
| GQ-14 | Approver allow-list: location (file, org team, CODEOWNERS-like) and rule "latest `labeled` event by allow-listed account" | R | 1863 (Q10), 1424 |
| GQ-15 | At-most-once design: local state vs "assigned to me and no own claim marker"; race window not measured; per-cycle launch cap and retry cap | R | 1866 (Q13), 1857 (Q4), 1428 |
| GQ-16 | Does `--worktree issue:<number>` trigger Orca-to-GitHub linking; use `path:` | R | 1870 (Q17), 301 |
| GQ-17 | Org owners outside collaborator list; permission to edit another's issue body | R | 1878 (Q25), 2023 |
| GQ-18 | Governance files not read (`freshness-pre-edit.sh`, `sc-recommend-phase0.sh`, `issue-worker-t2/t1.md`, `test_install_hooks.py`) | R | 1875 (Q22), 2024 |
| GQ-19 | Coder-side tie between workspace and GitHub account (Coder#477 scope); unnecessary under A; owner vs login unverified | R | 1869 (Q16), 120, 490, 2025 |
| GQ-20 | Issue text expects the claim to start the full orchestration; code stops at `next-steps.md` | R | 1895 (C1), 184, 1354 |
| GQ-21 | Guard, `--pipeline`, marker binding, pre-push are design only; job-identity registered but not installed on host; B-CTX gates only a later extension | R | 1896-1897 (C2, C3), 391-396, 413, 400 |
| GQ-22 | `ci.py` is not a `gh` wrapper; no Python `gh` wrapper; PATH-stub mocking; need injectable runner; nearest pattern `origin_repo.py` | R | 340-341, 1898 (C4), 1402 |
| GQ-23 | `mock_gh` stale description; `test_cli_registration.py:28-30` frozen-snapshot comment false | R | 342, 365, 1899 (C5) |
| GQ-24 | Outside-never-as-worker reading is the researcher's; multi-assignee inferred; Orca-started sessions staying open is an inference | R | 1874 (Q21), 1867 (Q14), 233 |
| GQ-S1 | STALE: project CLAUDE.md calls `origin` a private fork; it is public | R | 441, 1900 (C6) |
| GQ-S2 | STALE: earlier research-notes claim that `ci.py` is a gh wrapper (notes and codebase-context.md corrected) | R | 340, 1898 |
| GQ-S3 | STALE: `tests/pr_submit/conftest.py:3-8` mock_gh description | R | 342, 1899 |
| GQ-S4 | STALE: `tests/cli/test_cli_registration.py:28-30` comment | R | 365, 1899 |
| GQ-S5 | STALE/overstatement: `sc-issue-launch-level-hook.md:23` vs :40 | R | 391, 1896 |
| GQ-S6 | STALE: `src/superclaude/hooks/README.md:3-19` | R | 709, 1901 |
| GQ-S7 | STALE risk: `orca-capabilities.md` line 66 team-written inventory | R | 712, 1901 |
| GQ-S8 | Minor: `bug_report.yml` Orca-specific text | R | 333, 1901 |
| GQ-S9 | Consistent with code (no staleness): issue.md, SKILL.md, claim.md, origin_repo.py, clickup_claim.py, analysis file; design 19.7 matches `launch-job-identity.sh` | D | The positive "no staleness" note is not stated as a sentence; the same facts are used as CODE-VERIFIED rows (397). Not an omission of a finding. |

File gaps tally: 33 findings enumerated (GQ-01 to GQ-24, GQ-S1 to GQ-S9). Omitted: 0. Covered-by-dedup: GQ-S9 (1). Represented: 32.

### B.5 synthesis/synth-01-problem-current-state.md (507 lines)

Method: synth-01 is the direct source of report sections 1-2. A line diff of synth-01 lines 17-507 against report lines 102-700 left 39 unmatched synth lines; a fixed-string whole-line search found 24 of them verbatim elsewhere in the report (mostly the "Carried to Open Questions" table, now Appendix A.1 at lines 2002-2028) and the remaining 13 are rewritten, not dropped: Q1-Q3 renamed D1-D3 (report line 139 states the relabelling), and the CODE-CONTRADICTED bullet, the "Lost reply" row, the native-issue-type bullet, the "No Python gh wrapper exists" bullet, the "launch prompt" row, the "Watcher / poller code" row, Appendix item 5, Appendix item 21 and two headings were extended or corrected in the report (for example the issue-type field was upgraded from UNVERIFIED to CODE-VERIFIED at line 336; the `orca skills list/install` precedent was added at 341). Each synth section is therefore enumerated as one finding group and checked for the rewritten rows.

| ID | Synth-01 finding group | Status | Report location / note |
|---|---|---|---|
| S01-01 | Problem statement: the three questions of issue #331 with answers after the owner decision | R | 115-121 |
| S01-02 | Why it matters (no automatic trigger today; repo is public so issue text is public-authored; no approval/ready expression) | R | 123-126 |
| S01-03 | Trigger (issue #331, feeds `/sc:brainstorm`; push-design wording of issue and Coder#477) | R | 127 |
| S01-04 | Owner decisions table (Q1-Q3 renamed D1-D3) | R | 129-139 (relabelling stated at 139; D-labels also at 1841-1846) |
| S01-05 | Repo-side deliverable decided by the owner | R | 141 |
| S01-06 | Coder#477 description (what it asks for; "not known yet" items) | R | 145-146 |
| S01-07 | Coder#477 candidate integration points and prior art #195 | R | 147 |
| S01-08 | Repo boundary (listener/registration/transport in Coder repo) | R | 148 |
| S01-09 | Status under owner decision (filed assuming push; unnecessary unless B/C) | R | 149 |
| S01-10 | Command and trigger fact table | R | 159-167 |
| S01-11 | Claim waves 0-6 table | R | 169-179 |
| S01-12 | What the claim does not do (7 bullets) | R | 181-189 |
| S01-13 | Argument validation table and the "second check" note | R | 191-202 |
| S01-14 | Which login assigns; claim's pre-filter; no mutual exclusion | R | 204-208 |
| S01-15 | Idempotence and failure shapes | R | 210-216 |
| S01-16 | Environment a claim needs | R | 218-226 |
| S01-17 | Never-as-worker and Worker Contract (4 bullets plus policy gap) | R | 228-234 |
| S01-18 | Key findings of 2.1 | R | 236-240 |
| S01-19 | Local entry points table | R | 244-252 |
| S01-20 | New session vs live coordinator tradeoff | R | 254-265 |
| S01-21 | `orca agent launch` argument contract (14 rows; "Lost reply" row extended with the verbatim help text) | R | 267-287 |
| S01-22 | What the mock must do | R | 289, 1404 |
| S01-23 | Prompt contract for the integer-only rule | R | 291-296 |
| S01-24 | Launch-session environment facts (permission mode inputs; Orca link hazard) | R | 298-301 |
| S01-25 | Key findings of 2.2 | R | 303-307 |
| S01-26 | Workflows and job skeleton | R | 311-322 |
| S01-27 | Issue forms, live labels, `/sc:issue` label contract, `gh issue list --json` fields | R | 324-336 |
| S01-28 | Where `gh` is invoked; ci.py correction; no Python wrapper; seam; conventions A/B; nearest pattern; read-only minimum | R | 338-346 |
| S01-29 | How tests build or stub `gh` | R | 348-359 |
| S01-30 | CLI registration and package layout | R | 361-365 |
| S01-31 | Tests, gates and the `.claude/` mirror | R | 367-371 |
| S01-32 | House design-doc format | R | 373-375 |
| S01-33 | Key findings of 2.3 | R | 377-382 |
| S01-34 | Launch-level hook design versus code | R | 386-402 |
| S01-35 | Hooks and permission settings registered today | R | 404-427 |
| S01-36 | Untrusted issue text paths into a claim session | R | 429-443 |
| S01-37 | Who decides human-approved and intended owner | R | 445-470 |
| S01-38 | What a prompt-injected issue could do today | R | 472-484 |
| S01-39 | Security properties provided versus missing, and open governance decisions | R | 486-498 |
| S01-40 | Key findings of 2.4 | R | 500-506 |
| S01-41 | Current State Summary table (17 rows; "Watcher / poller code" row extended) | R | 508-528 |
| S01-42 | Flow diagram of the code-verified path only | R | 530-573 |
| S01-43 | Carried to Open Questions list (21 items, with item 5 and item 21 extended) | R | Appendix A.1, 2002-2028; Section 9.2 |
| S01-44 | Findings carried versus excluded (carried / excluded with rationale / contradictions between research files) | R | Appendix A.1, 2030-2034 |

File synth-01 tally: 44 finding groups enumerated. Omitted: 0. Covered-by-dedup: 0. Represented: 44.

---

## Part C. Omissions Found

Rating scale as defined in the task: CRITICAL = distinct foundational finding dropped; IMPORTANT = distinct secondary finding dropped; MINOR = redundant or low-impact detail. Addendum conformance: 0 omissions, so no CRITICAL.

### Omissions Found (status OMITTED; 14 rows)

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| O-05 | 03-29: `orca agent launch` takes the prompt as one free-text argument and has no flag for a permission mode or an allowed-tool list, so the launch call itself cannot constrain the launched session. (The report lists the flag set at 271 and says the repo has no allow list at 425, but never states that the launch CLI has no permission or tool control.) | research/03 s3.1 | OMITTED | none | IMPORTANT |
| O-04 | 01-56: the claim race window is Wave 1 plus the spawn, "seconds to minutes", and a 5-minute poll with unsynchronised workspaces makes a collision "possible but not frequent". (The report says only that the window "was not measured": 498, 689, 1428, 1866.) | research/01 s9 | OMITTED | none | IMPORTANT (borderline; it is a derived estimate that bears on revisit condition 4 "double claims occur in practice") |
| O-01 | 01-09: the claim never stages or commits `.dev/issues/` (issue.md:85, SKILL.md:75) and never prints the ClickUp token (SKILL.md:76) | research/01 s1, s2 | OMITTED | none | MINOR |
| O-06 | 01-68: the claim itself needs no terminal and no person at the keyboard; the Claude Code session needs a terminal only because Orca starts it as a terminal agent | research/01 s11 | OMITTED | none (the non-interactive property is carried at 188, 238) | MINOR |
| O-09a | 02-05: `contract3-generator-constraint-lint.yml:35` sets `timeout-minutes: 5` | research/02 s1 | OMITTED | none | MINOR |
| O-09b | 02-08: `.github/workflows/README.md` best practices (l.137-143): pin action versions, add `workflow_dispatch` for debugging | research/02 s1 | OMITTED | none | MINOR |
| O-10a | 02-28: 21 `src/superclaude` files import `subprocess` (named list) | research/02 s3.2 | OMITTED | none (conclusion "no Python module builds gh" is carried at 341) | MINOR |
| O-10b | 02-33: `shutil.which("<tool>")` guard precedents (`cli/reflect/runner.py:387`, `reflect/commands.py:494`, `install_codegraph.py:104,156`, `install_retired_mcp.py:407`) | research/02 s3.2 | OMITTED | none (stronger `_find_orca` precedent is carried at 341) | MINOR |
| O-10c | 02-35: 136 `gh` occurrences in 23 non-`.py` files with per-file counts | research/02 s3.3 | OMITTED | none | MINOR |
| O-10d | 02-47: other `from .x import` lines in `main.py` are function-local imports, not registrations | research/02 s4.1 | OMITTED | none | MINOR |
| O-10e | 02-49: rejected package-model examples and why (`swarm/` 11,799 lines, `eval/` 11,367, `cleanup_audit/` 1,820 and a Claude-pipeline executor) | research/02 s4.2 | OMITTED | none (choice of `recommend/` carried at 364, 1400) | MINOR |
| O-10f | 02-61: `lint-architecture` Checks 3/4/6/8/9 (command size warn 200/error 500, Activation present, frontmatter `name`/`description`/`allowed-tools`, name ends `-protocol`) | research/02 s6 | OMITTED | none (Checks 1/2 carried at 371; plan adds no command or skill) | MINOR |
| O-11 | 02-69: design doc's picker-ID table (its section 6) not checked against `ccsession-models.json` [UNVERIFIED], and the CODE-VERIFIED checks of the design's file claims | research/02 s7 | OMITTED | none | MINOR |
| O-12 | 03-12: governed Bash runs fresh per call with cwd not persisted (`os.execv('/bin/bash', ['bash','-c', ...])`) | research/03 s1.2 | OMITTED | none | MINOR |

Non-claim note: O-03 (ClickUp matching rules, outcomes `ambiguous`/`error/page_cap`/`error/unexpected`, the 429 `Retry-After` retry, exit-0-for-all-outcomes rule, optional `CLICKUP_LIST_IDS`/`CLICKUP_MAX_PAGES` names, argument checks) is recorded below as a partial drop, not as a fully omitted row, because the report carries the decision-relevant ClickUp facts (optional, never blocks, personal token, 20 pages at 30 s, `already_assigned`) and explicitly excludes the rest as not changing any plan step (line 1956).

### Covered-by-dedup (legitimate merges; not omissions; 8 rows)

| # | Source finding | Source file | Status | By which report item | Severity |
|---|---|---|---|---|---|
| D-1 | 01-49: analysis finding F2 "pull model" and statement 3 re `--claim --pipeline` | research/01 s8 | COVERED-BY-DEDUP | Option A definition (1335) and gap row G16 (698) | n/a |
| D-2 | 01-83: research 01 Summary paragraph | research/01 | COVERED-BY-DEDUP | Sections 2.1, 2.2, 2.5 | n/a |
| D-3 | 02-73: research 02 Summary paragraph | research/02 | COVERED-BY-DEDUP | Sections 2.3, 7.6 | n/a |
| D-4 | 03-33: claim runs to completion without a human (property an automated trigger inherits) | research/03 s3.2 | COVERED-BY-DEDUP | 188, 238, 1366 | n/a |
| D-5 | 03-52: Worker model need not be extended for claim-only A | research/03 s5 | COVERED-BY-DEDUP | 1364, 1390 | n/a |
| D-6 | 03-57: "most contained shape" synthesis (approver-only trigger, integer-only prompt, author restriction, permission decision) | research/03 s6 | COVERED-BY-DEDUP | Security model 1359-1363, 442, Q6 1859, Q12 1865 | n/a |
| D-7 | 03-68: research 03 Summary paragraph | research/03 | COVERED-BY-DEDUP | 2.4 key findings (500-506), Section 7 | n/a |
| D-8 | GQ-S9: "consistent with code, no staleness" note | gaps file | COVERED-BY-DEDUP | same facts used as CODE-VERIFIED rows (397) | n/a |

### Partial drops (finding is represented; a sub-detail is not). Listed so the report author can restore them if wanted; not counted as omitted.

| # | Finding row | Sub-detail not in the report | Severity |
|---|---|---|---|
| P-1 | 01-18 | Full return-contract field list (`mode`, `issue_url`, `dir`, `clickup_status`, `labels_applied`, `labels_missing`); three of nine fields given at 704 | MINOR |
| P-2 | 01-19 | `E-WORKER-NO-OUTPUT` is never named (the other seven STOP codes appear) | MINOR |
| P-3 | 01-32 to 01-34 (O-03) | ClickUp optional env names `CLICKUP_LIST_IDS`, `CLICKUP_MAX_PAGES`; outcomes `ambiguous`, `error/page_cap`, `error/unexpected`; the one 429 retry sleeping `Retry-After`; exit 0 for every outcome except bad args; argument checks; matching rules | MINOR |
| P-4 | 01-55 | Double-claim consequences: ClickUp task assigned to both people; comments not shared because the earlier-comment match is by the current login | MINOR |
| P-5 | 01-62 | Output files are refilled from templates on re-run (SKILL.md:50) | MINOR |
| P-6 | 02-24, 02-25 | `ci.py` function list; the 21-file list of `pr_submit` | MINOR |
| P-7 | 02-36 | Per-line examples of `gh` calls in the pr-submit scripts | MINOR |
| P-8 | 02-50, 02-52 | Lazy vs eager `__init__` styles both in use; `tasklist/` as a second package model | MINOR |
| P-9 | 02-57 | Fixtures `mock_monitor`, `fixture_findings`, `tmp_skill_dir`; gate-helper registry "pr_submit-specific, not reusable" | MINOR |
| P-10 | 02-63, 02-70 | `E501` ignored (`pyproject.toml:186`); D1 precedent at `sc-issue-command.md:418` for the design-doc folder | MINOR |
| P-11 | 03-13, 03-15 | Deliberate `setsid` escape; B-CTX probe scenario list | MINOR |
| P-12 | 03-40 | Authority-table row "be assigned: Read or higher" (substance at 465) | MINOR |
| P-13 | 03-50 | "decision D4: no brief can turn it on" for WC-9; explicit rationale that the claim cannot be a worker because it assigns and posts | MINOR |

---

## Part D. Summary

### Summary

- Findings enumerated: **301** (research/01: 83; research/02: 73; research/03: 68; gaps-and-questions.md: 33; synth-01: 44 finding groups). Plus 6 addendum-conformance rows (listed in Part A, not included in the 301).
- Represented: **279**
- Covered-by-dedup: **8**
- Omitted: **14** (CRITICAL 0, IMPORTANT 2, MINOR 12)
- Check: 279 + 8 + 14 = 301.
- Addendum conformance: 6 of 6 REPRESENTED (0 CRITICAL).
- Partial sub-detail drops (not counted as omitted): 13 groups (Part C, P-1 to P-13), all MINOR.

Adversarial stance result: I assumed at least five distinct findings were dropped. The compression is far more faithful than that: the report carries a near-verbatim copy of synth-01, a 30-row gap table, 36 open questions and 11 corrections that together map every one of the 24 gap rows and 9 stale-doc bullets. My first pass (phrase search only) over-flagged; reading Sections 4 and 9 and plan step 3.3 withdrew or downgraded five candidates (origin URL shapes at 1593, the next-steps.md local-only limit at 704, the blank-issues note at 712, the return-contract fields at 704, and the double-claim consequences, now a partial drop). Of the 14 omissions that remain, only two are more than redundant detail: O-05 (the launch CLI has no permission or tool flag, which feeds the open permission-mode question Q6) and O-04 (the researcher's seconds-to-minutes / not-frequent estimate of the double-claim window, which bears on revisit condition 4). The report's own "Coverage of research-file key findings" table (lines 1941-1992) lists every key takeaway as used or excluded; neither O-05 nor O-04 is in its exclusion list, so neither omission is justified there.

Recommended fix (report author, not this gate): add one sentence to Section 2.2 or Q6 ("`orca agent launch` has no flag for a permission mode or an allowed-tool list; the prompt is one free-text argument", R03 s3.1) and one sentence to gap row G7 or Q13 (the R01 s9 estimate that the window is seconds to minutes and a collision is possible but not frequent, derived not observed). The 12 MINOR rows can be left out without loss.

Verdict: FAIL (14 omitted; 0 CRITICAL, 2 IMPORTANT, 12 MINOR). Blocking items: O-05 and O-04.



