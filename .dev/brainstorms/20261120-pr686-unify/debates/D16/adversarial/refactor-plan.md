# Refactoring Plan: D16 unified prevention package

## Overview
- Base variant: Variant 1 (OURS), `variant-1-original.md`. Incorporated: Variant 2 (CLAY), `variant-2-original.md`, plus the results of Round 1, Round 2 and Round 2.5.
- Output: `merged-output.md` in the same folder as this file, titled "D16 unified prevention package". It must keep the base's section skeleton (Claim, Mechanism, Cited facts, Cost, Risk, What it gets right) and add: the ranked and ordered table, the admin-only list, the test protocol, the dropped list, the lightest version, the decisions the owner must give in chat.
- Change count: 10 planned, 9 rejected alternatives. Overall risk: Medium (the central control is one admin setting that has not been tested on this repository).
- Source for every figure: the round files and `invariant-probe.md` in this folder. Where the fault-finder's recount differs from an advocate's figure, the recount is used and marked "recount".

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Reframe the Claim: a second person with a mechanical block is what was missing; text alone does not bind (PR 681's body said "the owner reviews and merges" and its author merged it; PR 683 was self-merged about 75 minutes after 681 and 682, INV-019). The package is words in the file sessions read, one admin ruleset, a decisions file, and a direct hold on the open series. | OURS R1 + INV-026 | Claim | replace | C-002, X-003 won by OURS; CLAY conceded in R2 | Low |
| 2 | Keep the three layers but change layer 1 carrier: rule text goes in root `CLAUDE.md` (section "who rules, and what needs a second person"), a two-line pointer in `HOW-WE-WORK.md` and one line in `CONTRIBUTING.md`; the PR template gets two reminder lines and is not counted as a control (reach 14 of 100, and 0 of the last 79) | CLAY R1 (A-002), OURS R2 | Mechanism layer 1 | replace | A-002 agreed; template reach measured by both and recounted in INV-014 | Low |
| 3 | Rule text content: roles by login; "a question to a named person gets a written answer; silence is never a yes"; 3 working days is a timer to ask again, never permission; the owner names in chat a deputy or "nobody" and the channel they read; reversing or deleting someone else's merged work needs their written yes and a merger other than the author; a revert (made with GitHub's Revert button or `git revert`, undoing one named PR in full, merged within 7 days) is exempt from the written yes but not from the gate, and is reported to the author the same day; publish a plan as a draft PR or issue comment within a day; optional helper commands to check recent deletions | CLAY U-007, R2 both | Mechanism layer 1 | insert | C-005, C-004; the narrow revert definition answers INV-010 | Medium (self-classified) |
| 4 | Replace the five-path CODEOWNERS list by: core `docs/designs/`, `src/superclaude/core/WORKER-CONTRACT.md`, `/.github/CODEOWNERS` (so the gate cannot be removed by an unowned self-merge, INV-006); temporary until the owner says in chat the 655 series is reconciled: `src/superclaude/cli/issue_watch/` and `src/superclaude/skills/sc-issue-protocol/` (PR 686 has 11 source files in `issue_watch/`, per both Round 2 papers; PR 690 has 4 files in `sc-issue-protocol/`, orchestrator check); optional after the 14 day review, owner decides: `src/superclaude/hooks/scripts/launch-level-*.sh` and the plugin mirror (9 of 100 PRs touched them, 5 by Clay) | OURS R1 and R2, CLAY R2, INV-006, orchestrator re-check of 690 | Mechanism layer 3 | replace | C-003 hybrid; both advocates conceded the full list was too wide and that `issue_watch/` alone misses 690 | Medium |
| 5 | Code owner = `@ironbelly` only (not `clayphi`). Reason: at 0 required approvals a listed owner who authors the PR may merge it unreviewed (INV-007, community report, unverified), and both incident PRs were Clay's; a sole non-author owner also moves the queue to where the evidence says it is small (INV-013: 17 of the 23 gated master PRs are the owner's and would otherwise wait on Clay) | INV-007, INV-013 | Mechanism layer 3 | restructure | Neither advocate proposed it; it follows from the fault-finder and from both advocates' own cost figures | Medium |
| 6 | Ruleset on `master` and `integration` (admin only): pull request required, 0 required approvals, require review from code owners, dismiss stale approvals when new commits are pushed (because `/sc:pr-submit --monitor 3` pushes fixes after review, INV-021), block force push, block deletion, bypass for the repository admin role for pull requests only (CLAY R2; PR 662, the owner's 3 minute revert of release 6.1.0, touches `WORKER-CONTRACT.md`). `integration` is included because 23 of the last 100 merged PRs went there, all self-merged, and it is `protected=false` (INV-001) | OURS R1/R2, CLAY R2, INV-001, INV-021 | Mechanism layer 3 | insert | C-002; bypass and `integration` are separable CLAY and fault-finder benefits | Medium |
| 7 | Test protocol and fallbacks before the ruleset is announced (see section "Invariant conditions"); 14 day review that also counts silent passes and has a minimum sample | INV-007, INV-027, INV-016 | new section | insert | The claim "would have prevented 681 and 682" is conditional on this test | Medium |
| 8 | Decisions: one file `docs/decisions.md`, not a folder; seeded once with the rulings that open work depends on; every later ruling is added by the session that hears it, with the owner's chat sentence quoted, in the next PR for that area; the owner approves the wording in chat first. Source files `owner-answers.md` and `RULINGS.md` have not been read by anyone in this debate (INV-004); the seed is built from FULL-REPORT section 5 and the owner's chat | OURS R2, CLAY R2 | Mechanism layer 2 | replace | C-007 won by OURS; CLAY conceded in R2 (search sees files, not comments) | Medium |
| 9 | Direct hold on the open 655 series: the owner states in chat that PRs 686 and 690 wait for the owner's ruling; Clay sets both to Draft (neither is Draft today, INV-002); Draft is a speed bump because the author can mark ready again; the lasting hold is the ruleset with the two temporary lines | CLAY R2, INV-002, INV-009 | Mechanism layer 2 | insert | PR 690 is on no core path | Medium |
| 10 | Order and cost table, admin-only list, "lightest version" and "version still refused" paragraphs | both R2 final tables | new section | insert | The topic asks for a ranked, costed package, an order, and the admin-only items | Low |

## Residual disputes: adjudication
Weighting rule applied: OURS stands unless CLAY shows a clear evidenced benefit; a separable CLAY benefit is adopted as a hybrid.

| Dispute | Decision | Reason |
|---|---|---|
| Admin bypass (CLAY: yes for pull requests only; OURS: none) | HYBRID: bypass for the admin role, pull requests only, and the owner confirms in chat that the gate then binds non-owners | Verified CLAY benefit: PR 662 (owner revert of release 6.1.0, opened 2026-11-19T01:17:35Z, merged 01:20:30Z) touches `WORKER-CONTRACT.md`, so a no-bypass gate would have held it. Limit: sessions on the shared `ironbelly` login can use the bypass; the orchestrator never passes `--admin` (INV-022, INV-023) |
| Required paste of the deletion check (OURS) vs optional helper (CLAY) | CLAY: written sentence plus optional helper, narrow revert exemption, CI check only on a tripwire | Verified defects of the paste: fires on 11 of 100 PRs, 9 of them Clay's and mostly their own earlier work, no revert exemption (PRs 662, 664), one more thing the author can skip. OURS conceded the CI check belongs behind the tripwire |
| `IB-JonathanB` on CODEOWNERS | CLAY: not named anywhere until they agree in an issue comment | No PR authored, reviewed or commented on in this repository (`gh search`, run by both advocates and the orchestrator); a person nobody asked would get review requests on every gated PR. With one owner the question does not arise |
| Two owners (both advocates) vs sole owner | Sole owner `@ironbelly` | INV-007 (author-owner passes at 0 approvals, unverified) and INV-013 (queue is mostly owner-authored PRs). Keeps the OURS line that the owner approves designs |
| Direct hold on 686 and 690 | Adopt as an owner decision in chat | Both advocates accept a hold in substance; FULL-REPORT section 12 item 1 already recommends not merging 686 before a ruling |
| `integration` in the ruleset | Include | INV-001: 23 of the last 100 merged PRs, all by Clay, all self-merged, branch unprotected; release PRs then carry 100 to 1,146 file bundles to master |

## Invariant conditions (from Round 2.5)

The four HIGH UNADDRESSED findings become binding conditions of the recommendation. Depth standard allows no Round 3, so they are resolved here and also listed in the return contract.

| ID | Condition the verdict must state |
|---|---|
| INV-001 | The ruleset targets `master` and `integration`; or the owner retires `integration` or allows it to reach `master` only through a reviewed PR. Until then a design or deletion opened against `integration` passes every other item |
| INV-007 | "Would have prevented 681 and 682" is stated as "probably, UNVERIFIED" until the test below passes. GitHub's documentation says a pull request touching owned content "must be approved by that code owner"; it is silent on an author who is himself an owner at 0 approvals, and one community report says that case is mergeable. Mitigation in the design: the only code owner is `@ironbelly`, so the incident author (`clayphi`) is not an owner |
| INV-026 | Gate by gate for the incident input: G1 ruleset exists (no today, `protection` 404 and `rulesets` `[]`); G2 PR required (yes); G3 path match (681 yes via `docs/designs/`, 682 yes via 1 of 36 files `WORKER-CONTRACT.md`, fragile); G4 non-owner author blocked at 0 approvals (to be tested); G5 author cannot use the bypass (`clayphi` is not admin, yes); G6 approver independent (only a second login, not proof the owner read it, INV-008); G7 approval current at merge (needs dismiss stale approvals); G8 base is master or `integration` (covered). The text items alone add no prevention |
| INV-027 | Test protocol: after the CODEOWNERS file is merged and the ruleset is active, `clayphi` opens a throwaway PR that edits one line under `docs/designs/` with base `master`, with no approval; expected result `mergeStateStatus` BLOCKED and review decision REVIEW_REQUIRED, and the merge button refuses without `--admin`; repeat with base `integration`; then an owner-authored throwaway PR on the same path to learn whether the bypass is needed; close all throwaway PRs unmerged. Do not run it from the owner's login. If the first test does not block: fallback 1, require 1 approval for pull requests (cost: every PR, 89 of 100 recent merges were self-merged); fallback 2, the ruleset rule "required reviewers" by path (generally available since 2026-02-17 per GitHub's changelog; whether this free-plan organisation can use it, and whether it needs a team, is UNVERIFIED); fallback 3, drop the gate and keep words, the hold and the tripwire |

MEDIUM findings the verdict must also carry: dismiss stale approvals (INV-021); the two authorities for CODEOWNERS edits, Clay in the orchestrator design lines 288 and 593 against the owner here (INV-022); the orchestrator never uses `--admin` and the owner's chat go is not a GitHub approval, so on gated paths the merge needs both (INV-022); who converts 686 and 690 to Draft (INV-002); the undefined "revert" (INV-010); the 14 day review needs a minimum sample and a count of silent passes (INV-016, INV-027); corrected figures (INV-012, INV-013, INV-014).

## Changes NOT Being Made

| Item | Proposed by | Why rejected (evidence) |
|---|---|---|
| `/sc:overlap` command or CI overlap scan | OURS section 11 item 8 | Days of work; contradicts the owner's 2026-10-29 answer on issue 290 ("only file issues until we have an eval framework"); misses the unpublished work that was the real miss (U-005) |
| Stop-on-overlap in `/sc:issue --create` and `--claim` | section 11 item 1 | `--claim` already stops on an issue assigned to someone else (`refs/claim.md:42`); `--create` lists up to 10 possible duplicates and continues (`refs/create.md:20`); issue 655 cited 13 items so a stop would have passed (X-002) |
| 24 hour cooling period | section 11 item 7 | GitHub cannot enforce a delay; the required reviewer does the work (C-009) |
| Tracked in-flight register | section 11 item 6 | Rots; draft PRs and issue comments do the job at zero cost (C-008). Revisit when the coordinator layout `.dev/coordinators/` of Q26 exists (topic D07) |
| `docs/decisions/` folder with index and full back-fill | section 11 item 5 | One file is enough until it has about 50 entries (OURS R2) |
| Mandatory pasted deletion check | OURS R2 | See dispute table |
| Five-path CODEOWNERS list | section 11 item 3 | Matches 27 of the last 60 merged PRs; a queue on active work (OURS R1 concession) |
| Naming `IB-JonathanB` as the deputy | both R1 | Not shown active |
| Changing `/sc:pr-submit` to inject the PR template | OURS R2 | The template reached 0 of the last 79 PRs, so the template is not a carrier; text goes in root `CLAUDE.md` instead. Drop for now |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 5 and 6 (sole owner, ruleset) | The gate never blocks, or blocks the owner (INV-007) | High if silent; Medium if loud | One admin click turns the ruleset off; the test protocol finds it loud or silent before it is announced |
| 6 (bypass) | Sessions on the shared login can use it | Medium | Remove the bypass; the owner's PRs then need a second approver |
| 4 (paths) | Queue on the owner for Clay's gated PRs, about 17 in 10 days on `master` and `integration` together (recount; one third on master) | Medium | Drop a path at the 14 day review, `WORKER-CONTRACT.md` first |
| 3 (self-classified text) | Authors skip the "reversal" sentence, as 682's author did | Medium | The gate on paths is the backstop; CI check on tripwire |
| 8 (decisions file) | Rots, or seeded from second-hand summaries | Low | Move rulings to issue comments if fewer than 3 entries are added in 30 days |
| 9 (hold) | Draft is reversible by the author | Low | The ruleset with the two temporary lines |

## Review Status
Auto-approved (unattended run, no interactive checkpoint). Timestamp 2026-11-20.
