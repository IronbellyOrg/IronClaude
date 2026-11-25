# OA triage: which of the 34 owner actions need a debate

Written 2026-11-20. Inputs read in full: `brainstorm/run/merged-requirements.md` section 7 (OA-1 to OA-34) and its decision rows K1 to K24, `DECISIONS.md` (32 entries, coordinator decisions, owner actions, verdict disagreements) and `debates/TOPICS.md`.

Classes:
- SETTLED: a verdict (D, Q, QG), a D15 OD answer, a built-in default row (K) or an owner standing rule already decides it. The spec is written to that answer. Any owner go that the action itself needs (a post, a PR, a push) stays an owner action under DECISIONS.md section D and does not block the spec.
- OWNER-ONLY: only the owner can act (admin setting, consent, per-repo switch, credential, a fact only the owner knows). The spec records it as an owner action with the safe default named in the row, and never asks again.
- DEBATE: a design or policy choice with no verdict yet that a quick adversarial debate can settle.

## Table

| OA id | Question (verbatim, short) | Class | Reason and source |
|---|---|---|---|
| OA-1 | Do both gates stay (start approval, and plan approval after the claim)? | SETTLED | D01 keeps approval (not assignment) as the start gate; D03 item 1 makes the revert of PR 682 the default until D01 rules; D14 revert row. Answer: both stay, PR 682 is reverted. The go to open the revert PR is a separate owner go (DECISIONS D) and is not a spec blocker. |
| OA-2 | Who adapts PR 686 and PR 690? | SETTLED | D14: REBASE-AND-ADAPT in place as drafts, keeping review history; Clay edits each PR, the owner reviews each push. Q03 notes the rework lands on Clay's PR. If Clay does not act, an owner session adapts a new draft (spec records this as the fallback). |
| OA-3 | Which poll command does cron run? | SETTLED | D07 (one dispatcher over `orca repo list`, no registry) and D02 item 2; merged design K4. Answer: `issue-watch run-all`, per-repo JSON config. X-8 (verdict disagreements) already follows D07. |
| OA-4 | Order of planb and the revert. | SETTLED | D14 action table and D15 O2; merged design K20. Answer: revert first, then contract and guard amendment, then planb landed, then design amendment, then adapted PR 686. "First" means first before PR 686. |
| OA-5 | Server-side ruleset on `master` and `integration`. | OWNER-ONLY | Only the repository admin `ironbelly` can set it (DECISIONS A; D14, D16). Spec must record it as an owner action and assume NO ruleset: every control is written as "narrows", INV-025 stays open, a person's go is a procedure. D16 supplies the recommended settings (admin bypass for PRs only, `integration` in, sole code owner `@ironbelly`) as a ready-to-say text, not as a spec build. |
| OA-6 | Who counts as "the owner" for typed answers on the shared login `ironbelly`. | OWNER-ONLY | Names a session kind or a separate agent login: a fact and a credential only the owner can supply (D06 item 9; DECISIONS C). Safe default: leave it unnamed, so `answer-check` cannot pass and every merge is typed by hand (S14 ships, merges stay manual). |
| OA-7 | Wording of WORKER-CONTRACT lines 57, 70 and 245 (master numbering). | OWNER-ONLY | A change to the owner's own contract needs the owner's ONE chat confirmation; Q01 item 2 says the line 57 sentence came from a fix agent's reading of "narrow d2", not from the owner's words; D06 item 7: "owner chat approval first; none in force". Safe default: line 57 fix prepared as its own commit, shipped only after confirmation; lines 70 and 245 drafted but not in force; `coordinator_autostart` can never be true. |
| OA-8 | Keep the trigger label? | SETTLED | D01 item 7: keep `issue-watch:trigger` for now; dropping it is a later owner decision. No change today. |
| OA-24 | Where the interim ledger lives and who commits it. | SETTLED | Owner standing rules: `.dev/tasks/` is always staged (CLAUDE.md), commit only when asked, approvals are recorded by the agent (memory `approvals-through-chat-never-files`); merged design K21 puts the ledger in the unification task package under `.dev/tasks/`, committed by the recording agent when the owner says. |
| OA-28 | Planb's default-on first run and its label write (K24, K18). | DEBATE | D09 rule 2 lets per-repo init create the two labels once (the poll never writes), but D09 item 3 and K18 leave how NG-2 is read, and K24 leaves the `auto_enable` default (owner's R18 default-on after the throwaway run against the merged design's false), open. No verdict decides these. Group OAG3. |
| OA-9 | Where the sweep JSON lives. | DEBATE | D11 item 1 says "owner decides: saved beside the report, or each reader runs its own sweep"; K19 picked beside the report as a default only. A design and policy trade (WC-16 one sweep per five minutes against the observer's 15-second refresh). Group OAG2. |
| OA-10 | Branch names: `Coordinator` working branch and `coordinators` records branch as two things. | SETTLED | D08 item 7: two things, stated in one sentence; the owner may overrule (70 percent). The layout of sections 2.2 and 4 stands. |
| OA-11 | Which of the three standing grants. | OWNER-ONLY | A permission only the owner can grant (consent). Verdicts fix the shape: QG3/OD-11 and D15 R-4 default `grants` empty and fail closed; at most three entries (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`); K6. Safe default: empty; the refusal text names the missing entry and the one sentence the owner can say in chat; the agent records the owner's words. |
| OA-12 | Close authority after merge. | SETTLED | QG3/OD-10 (D15 C-INV-4): one per-PR go, bound to the head sha, covers the merge and that PR's issue close; no standing `issue.close`. K12. |
| OA-13 | Go expiry and reviewer hold. | DEBATE | D06 item 1 says the expiry number is an owner decision and gives no source for 24 hours or 60 minutes (UNVERIFIED, RK-30); D06 item 3 already settles that `changes_requested` stays a hard refusal (not part of the debate). The two numbers and the no-expiry option are a policy choice. Group OAG1. |
| OA-14 | Hand-back and capacity. | SETTLED | QG1/OD-2 (re-plan, then the person re-applies approval) and QG1/OD-13 (a waiting hand-back does not count toward `max_in_flight`); cap 1 first is merged design K9 and D07 item 8 (claim agents share one worktree; raise only after the isolation, closing-writer and concurrency tests pass). |
| OA-15 | Local `git branch -d` in cleanup. | SETTLED | Q02: yes, `git branch -d` only, with the added refusals, report-only first week. The third bullet ("approve the issue 687 cleanup design") is a consent (D13, Q01 item 8): spec records it as an owner action; default S15d is not built until the owner says yes in chat; each `--apply` still needs its own go. |
| OA-16 | Notice cap. | SETTLED | D11 item 4 and QG2/OD-5; K23: the cap of 5 is a PROPOSAL; default absent or 0 means no cap; malformed values are a config error. Ruling 39 is Clay's, not the owner's. The owner may record a number any time; nothing depends on it. |
| OA-17 | Observer entry text and the questions panel. | DEBATE | D11 item 3 and caveats leave two choices to the owner (show entry text word for word through `observe/sanitize.py` or titles only; keep or end the questions-panel exception to "one data source"). No verdict decides them. Group OAG2. |
| OA-25 | Reminder cadence and the meaning of owner silence on a waiting go. | DEBATE | INV-023 and K9 fix that silence is never a yes and a waiting go counts toward the cap; the reminder channel is open because the notice step is reserved by QG2/OD-5 (entry lines only in the first build) and OA-16 defaults to no cap. Group OAG1. |
| OA-26 | Does each push of the `coordinators` records branch need a go? | SETTLED | Merged design K5 and INV-024 (pushing is an outward action) plus WORKER-CONTRACT.md:241 (an outward action only when the person's instruction names it). Answer: a go per push. |
| OA-18 | Per repo: `coordinator_autostart` true or false, and is a typed wake line acceptable? | OWNER-ONLY | A per-repo consent to script-started sessions and to typing into a session (D06 item 6; D10 item 3; DECISIONS C "say whether a typed wake line is acceptable at all"). Safe default: `coordinator_autostart` false (`coordinator_absent` reported); typed wake line refused, file pull and mailbox only; both paths built behind the flag and tested; a typed line also needs U25 live proof. |
| OA-27 | Which `plan_depth` the planner uses. | SETTLED | QG1/OD-1 (and D15): `quick` default; one plain key `plan_depth` passed to `/sc:issue --plan --depth`; a repo may set `standard` or `deep`. |
| OA-19 | Per repo: switch on. | OWNER-ONLY | A per-repo switch-on consent; Coder issues 515 and 516 are owner-run and come first (DECISIONS B). Safe default: every repo off (`enabled: false`, `auto_enable` false); at most one throwaway repo after the `--dry-run` shadow run, cap 1, `claim_by: poll`. |
| OA-20 | Flip `WORKER_BINDING_PROVEN` after the probe; later, open level FS for workers. | OWNER-ONLY | D05 item 3 and K16 fix the conditions (a reviewed commit flips the switch only after the live binding probe passes); the live probe has not run and the flip is the owner's reviewed go. Opening FS later needs the ruleset and issue 442's observations (D04 item 3). Safe default: not flipped, no worker starts on a real issue; probe issues only. |
| OA-23 | The claim route after the X-001 live check. | OWNER-ONLY | Depends on a live observation that does not exist yet (does the claim agent linger in the shared `Coordinator` worktree) and, for a separate claim worktree, a change to Coder issue 516 in the owner's other repo (D07 item 8; K1, RK-7). Safe default: poll-launched claims only on a throwaway issue, cap 1, real rollout off; both `claim_by` values are specified (`poll` default, `coordinator` reserved). |
| OA-21 | Confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656). | OWNER-ONLY | D14 says KEEP (not reverted) but whether the owner accepts that Clay removed those skills is a fact only the owner knows (DECISIONS B). Safe default: not confirmed; per-host diff of installed guard, contract and skills before every `superclaude install`, never a blanket `--force`. |
| OA-22 | Answer Clay on issue 450; ask Clay to drop "replaces #450" from issue 655; split issue 689. | SETTLED | D14: issue 655 KEEP and RESCOPE, issue 450 KEEP open and answer Clay's 2026-11-18 comment, issue 689 SPLIT and DEFER; D12 rule 6 (the `--mode other` and form fields split). The posts themselves are owner or assignee actions (agents write nothing; DECISIONS D) and block no stage. |
| OA-29 | Scope of the naming rule (OD-3). | SETTLED | QG2/OD-3: scope B (scan only the coordinator's own two writers, `report-entry` and `escalate`), after the U54 measurement. The owner is asked once whether it applies to workers; B stands if no answer comes. |
| OA-30 | A refused mandatory escalation by the name check (OD-4). | SETTLED | QG2/OD-4: fail open on delivery (write with a visible marker, log the refusal); fail closed only for a structurally bad call. |
| OA-31 | Channel for audit escalations (OD-5). | SETTLED | QG2/OD-5 (X-5 follows QG2): entry lines only in the first build; the push notice reserved for AU4a, AU4c and AU5 behind three triggers. |
| OA-32 | Tags, publication and interrupts (OD-6, OD-7). | SETTLED | QG3/OD-6 (never tag or publish, rule N6 unconditional, 89 percent) and QG4/OD-7 (no interrupt, N7 stays removed, 85 percent). |
| OA-33 | Build the lease comment now (OD-8). | SETTLED | QG4/OD-8: no; reserved design with the recorded trigger "a second host or user runs a poll". |
| OA-34 | List newly assignable issues, `could_assign` (OD-9). | SETTLED | QG4/OD-9: no; info streams off; add an explicit off switch and make a failed info search a warning (a fifth action on the adapted PR 686). |

## Counts

| Class | Count | OA ids |
|---|---|---|
| SETTLED | 20 | OA-1, 2, 3, 4, 8, 10, 12, 14, 15, 16, 22, 24, 26, 27, 29, 30, 31, 32, 33, 34 |
| OWNER-ONLY | 9 | OA-5, 6, 7, 11, 18, 19, 20, 21, 23 |
| DEBATE | 5 | OA-9, 13, 17, 25, 28 |
| Total | 34 | |

Notes on edge cases: OA-1, OA-2, OA-15 and OA-22 are classed SETTLED because a verdict gives the answer the spec is written to; the owner go each one still needs for an outward action is already listed in DECISIONS.md section D and does not block the spec. OA-11 and OA-18 are classed OWNER-ONLY even though QG3/OD-11 and D10 give defaults, because the act (a grant, a consent to script-started sessions) is the owner's alone.

## Debate topics (the five DEBATE rows in three topics)

| Topic | OA ids | Theme |
|---|---|---|
| OAG1 | OA-13, OA-25 | How long a merge go lives, how long a silent reviewer is waited for, and how a waiting go reaches the person |
| OAG2 | OA-9, OA-17 | What the sweep saves to disk and what the observer screen may show |
| OAG3 | OA-28 | What planb's first run may switch on and write to GitHub |

The three blocks are appended to `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/TOPICS.md` under "## OA debates OAG1..OAG3 (depth: quick each)".
