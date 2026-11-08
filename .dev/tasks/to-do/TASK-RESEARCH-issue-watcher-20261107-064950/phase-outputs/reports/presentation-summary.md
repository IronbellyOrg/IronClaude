# Presentation summary: GitHub issue watcher research (issue #331)

Date: 2026-11-07. Every statement below is taken from the final report or from the five gate verdict files; nothing is new.

## Report location

`.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md`

## Key findings (8 bullets, each traceable to the report)

1. `/sc:issue --claim` stops after writing `next-steps.md` and never runs a next step; the issue text's expectation that it starts the full pipeline is CODE-CONTRADICTED, and `--claim --pipeline` is design only (Section 2.1; gaps G16, G17).
2. Nothing watches or polls today: no Python module under `src/superclaude` builds a `gh` call or runs `orca agent launch`, and no workflow has a `schedule:` or `issues:` trigger (Section 2.3; gaps G1 to G3).
3. The claim has no mutual exclusion (check, then `--add-assignee @me`, which adds) and leaves the issue in Backlog, so the poller needs its own dispatch record written before the launch (Sections 2.1, 2.4; gaps G7 to G9).
4. `orca agent launch` needs an existing worktree, has no `--repo` flag and no permission-mode or allowed-tools flag, and submits the prompt; whether a leading `/sc:issue` runs as a slash command is UNVERIFIED and needs one owner-run live test (Section 2.2; gaps G14, G20; Q1, Q6).
5. The repository is PUBLIC and the claim reads title, body and comments live, so the integer-only prompt protects the launch prompt but not the session; nothing registered constrains a launched session (Sections 2.4, 7.3; gaps G13, G14).
6. No trigger or approval label exists (the fork has 9 default labels); approval can only be a GitHub-side act by a Triage-or-higher account (3 accounts today), and the `labeled` event actor is the available signal (Section 2.4; gap G5).
7. Reading Project and Status needs `read:project`, which the observed token lacks; whether `gh project item-list --query "status:Backlog ..."` is accepted is UNVERIFIED (Sections 5.3, 5.5; gap G10; Q7, Q8).
8. Polling is cheap (12 polls an hour is about 0.24 percent of the 5,000 an hour allowance per call type) and Coder documents `coder_script` with a five-minute cron, but a stopped workspace polls nothing (Sections 5.4, 5.7; gap G19).

## Recommendation

**Option A, the workspace-side poller. Decided by the owner (ADDENDUM 2).** Rationale: it needs no listener, no inbound port, no address registry and no privileged Coder token, has the lowest effort (M) of the options that start a session, and uses the `gh` login the claim already uses (Section 7.2).

## Answers to the three questions of issue #331

| # | Question | Answer in the report |
|---|---|---|
| 1 | Microservice versus GitHub Action | Neither push design: the owner chose option A, a poller in each workspace. B (GitHub Action plus workspace listener) and C (central microservice plus listener) stay documented alternatives with nine revisit conditions (Sections 1, 6, 7.8). |
| 2 | Binding each workspace to a GitHub account | Under A the binding is the workspace's own `gh` login, read each cycle with `gh api user -q .login`, and the claim assigns `@me` of the same login. Whether the Coder workspace owner is the same person as that login is not checkable in this repo [UNVERIFIED] (Sections 1, 6.1; Q16). |
| 3 | The Coder-side listener | There is none under A: no listener, no inbound port, no registry. The 5-minute poller (`superclaude issue-watch once`, run by a Coder `coder_script` cron entry that lives in the Coder repo) is the whole Coder-side component. Where it runs and keeps its state in the target template is [UNVERIFIED] (Sections 1, 6.1, 8; Q15). |

## Research file count (counted with Glob on the `research/` folder)

5 research files: 3 codebase (`01-claim-flow-and-session-launch.md`, `02-github-surface-and-cli-patterns.md`, `03-governance-and-security-surface.md`) and 2 web (`web-01-github-events-projects-and-limits.md`, `web-02-coder-claude-dispatch-and-security.md`). The folder also holds `research-notes.md`, which carries the two binding owner addenda and is not counted as a research file. This matches the report header "3 codebase + 2 web research".

## Gate results (read from the five verdict files)

| Gate | Verdict as recorded | Fix cycles | Notes |
|---|---|---|---|
| Gate 1, research completeness | PASS | 2 (3 reviews; the third passed) | No open blocking findings. |
| Gate 2, synthesis quality | PASS | 2 (3 reviews; the third passed) | No open blocking findings. |
| Gate 3, report validation | FAIL as measured (halt), then CLOSED BY OWNER-APPROVED EXCEPTION | 2 (3 reviews) | After the third review 2 blocking findings stayed open: F1 (the candidate cap could still be filled by never-handled issues) and F2 (a `which=shutil.which` default argument made a later test patch ineffective). The owner approved on 2026-11-07; F1 and F2 were fixed by targeted edits after the final review and no fourth review ran. Final status: PASS WITH OWNER-APPROVED UNVERIFIED FIXES, not a clean pass. |
| Gate 4, source-document fidelity | PASS | 1 | Two fidelity agents; the one blocking finding (the Phase 4 filter row said `status:Backlog` is for UI filtering only) was fixed and both verifications passed. Both agents also checked the unverified Gate 3 edits against the code they cite and found them consistent. |
| Gate 5, anti-omission | FAIL by the monotonicity guard (open blocking findings 2 before and 2 after the fix), then CLOSED BY OWNER-APPROVED EXCEPTION | 1 | Edit B1 (the race-window estimate "seconds to minutes ... possible but not frequent" now applies only to a race between two different logins; the same-login window is longer, runs to the Wave 6 comment and has no estimate) and edit B2 (`orca agent launch` has no permission-mode or allowed-tools flag and takes the prompt as one free-text argument; carried into Section 9.2 Q6, gap G14 and the Phase 3 contract table) were applied after the final review and are unverified by a further review. No cycle 2 and no further review ran. |

Two gates (3 and 5) therefore close on owner-approved exceptions with late edits that no later review verified; the report records both in the Section 8 review status notes.

## Owner decisions already made (as the report records them, Sections 1.1 and 9.1)

- **D1:** option A. Each workspace polls GitHub every 5 minutes with its own `gh` login and starts the claim via `orca agent launch`; no listener, no inbound port, no address registry.
- **D2:** claim-only. The watcher's job ends at starting `/sc:issue --claim <N>`; the pipeline after the claim stays manual.
- **D3:** only a validated integer issue number reaches a session prompt, never issue title or body text. The prompt is exactly `/sc:issue --claim <positive integer>`.
- Section 9.1 also records D4 (repo-side deliverable: design doc, tested poller with mocked `gh` and `orca agent launch`, nothing run live, label setup instructions), D5 (the Coder#477 statement below) and D6 (options B and C and any live deployment recorded as follow-up).

## IronbellyOrg/Coder#477

The listener and registration live in the Coder repo, not in IronClaude. Issue #477 was filed assuming a push design. Option A makes it unnecessary unless option B or C is revisited. The only Coder-repo follow-up that A needs is the `coder_script` cron entry that runs the poller and, if the template does not already persist `$HOME`, a persisted path for the dispatch record (Sections 1.2, 7.7).

## Correction recorded by the report

`src/superclaude/pr_submit/ci.py` is not a `gh` subprocess wrapper. It imports only `re`, `.classifier` and `.models` and consumes an already-fetched payload, so a poller needs its own small injectable subprocess runner (plan step 2.2). The same wrong claim in `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/codebase-context.md` was corrected there (line 21, "CORRECTION (2026-11-07, research alignment check)") and in `research/research-notes.md` (lines 30 and 37). Report references: Sections 2.3, 4.1 gap G2, 9.3 row C4.

## Remaining open items

None of these is stated as fact in the report. Section 7.9 lists the details the addenda leave open; Section 9.2 holds the full open-question table (Q1 to Q36).

- The intended-owner rule: the research supports routing candidate 1 (issue assigned to the own login) but no addendum names a candidate, and the same-login multi-workspace case is open (Q4, Q14).
- The approver allow-list: where it lives and the rule "latest `labeled` event by an allow-listed account" (Q10).
- Trigger and approval label names, the Project and Status mapping, and whether a label-only selection is acceptable (Q9).
- Policy for the claim's own reads of issue title, body and comments (Q12), and the basis for a standing label-triggered outward action (Q36).
- The permission mode of the launched session, which `orca agent launch` cannot set (Q6), and the minimum `gh` scopes the claim needs (Q35).
- At-most-once parameters: lease, attempt cap, launch cap, and the real race window, which was not measured (Q13).
- Where the poller runs and keeps its dispatch record in the target Coder template (Q15).
- One owner-run live test: a leading `/sc:issue` as the initial `--prompt` executes, argv versus typed paste, real JSON shape and error body of `agent launch` (Q1, Q2, Q3).
- Per-host Coder facts: Orca runtime reachable, `ccsession-orca` configured, tier picker IDs served, `gh` authenticated as the person, ClickUp variables (Q5), and whether the ClickUp identity and the `gh` login are the same person (Q34).
- Whether the Coder workspace owner and the `gh` login are always the same person (Q16).
- Whether the poller's token can read the org Project and whether the server-side Backlog filter works (Q7, Q8), plus organization token policies and org owners outside the collaborator list (Q24, Q25).
- Detecting an issue-body edit after approval and the REST comment author field name (Q11).
- Whether a claim re-run tolerates an existing `.dev/issues/<N>/` directory (Q18); whether the `issue:<n>` worktree selector triggers Orca-to-GitHub linking and which checkout is used (Q17).
- Governance file bodies not read (Q22), rate-limit handling through `gh` (Q23), and the push-design details that matter only if B or C is revisited (Q26 to Q30).
- Late edits unverified by a further review: F1 and F2 (Gate 3) and B1 and B2 (Gate 5), described under the gate results above.
