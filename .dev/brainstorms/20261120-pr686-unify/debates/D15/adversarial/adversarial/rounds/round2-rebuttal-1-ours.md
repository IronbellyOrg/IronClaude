# D15 Round 2: Rebuttal for Variant 1 (OURS)

Topic: Clay strengths bundle, what to adopt and how. Variant 1 = OURS (the owner's line). "They" means Clay (account `clayphi`); the repository owner is `ironbelly`. Weighting rule: OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS; a clear separable CLAY benefit is a HYBRID.

Notation: "D:nnn" is a line of `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master`. "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in the same export. "Dnn" is `debates/Dnn/VERDICT.md` under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. "pr-a" is the PR 686 export in `/home/coder/.cache/ic-snap-20261120/pr-a`.

## Facts I read myself in this round

- Design lines D:60, D:73-140 (DQ1 to DQ13, ADD1 to ADD6), D:510-513 (the verb group), D:532-545, D:573, D:596-625, D:664-694, D:686, D:715-771, D:796-865, D:877, D:1123-1141 (tests T1 to T13), D:1177.
- `pr-a/src/superclaude/cli/issue_watch/repos.py:37-50` (tier names, defaults), `:79`, `:132-159` (tier list read), `:350` (`clone_parent`); `pr-a/.../github.py:165-175` (`argv_search_assigned`, `argv_search_info`); `pr-a/.../cycle.py:1226` (`missing` against `no_checkout`), `:918`, `:1586`, `:1616` (info reads).
- `pr-a/tests/issue_watch/test_audit.py:78-106` (the 62-reason pin, the 14 removed reasons, exit codes).
- Master: `src/superclaude/core/WORKER-CONTRACT.md` lines 41, 62-63, 66-74, 100-199, 236-248; `skills/sc-issue-protocol/refs/claim.md` Wave 2; `skills/sc-issue-protocol/refs/tiers.md`; `skills/ccsession-tag/ccsession:1001-1010` (the `--tier` option); `skills/sc-closeout-protocol/refs/result.md:18,40-47` (the `handback` and `remaining` fields); `skills/agent-work-report/scripts/collect.py:201-215` (one `gh search issues --owner <org> --involves <person>` per org); `cli/issue_watch/launch.py` (a grep finds no `ccsession` and no `--tier` text).
- Verdicts D01, D04, D06, D07, D08 (in full or the parts cited), and a grep of D01 to D13 for each G topic.
- Counts I ran (read only): the last 50 issue titles of `IronbellyOrg/IronClaude` (`gh issue list --repo IronbellyOrg/IronClaude`); the last 30 merged PR bodies (`gh pr list --repo IronbellyOrg/IronClaude`); the last 300 commit messages of the local checkout; a grep for a bare seven-equals line in `src`, `tests` and `docs` of the master export.

Not re-read by me and therefore UNVERIFIED: the coordinator spec FR-8, FR-10, FR-23, FR-24 and Q12 (it lives in IronFlow, outside this repository); the Q26 text (taken from D07); the owner's local unpushed plan rows R9, R17, R23, R25, R33; the PR 681 and PR 682 merge timings; `pr-a/tests/issue_watch/fixtures/_assumed_shape/ccsession_help_tiers.txt` (I saw its name only; the folder name says the shape is assumed, not captured).

One correction to my Round 1: I wrote that the cap of 5 notices is "not ruled on; open (AD-B4, D:1177)". The design contradicts itself: D:1177 says "not ruled on; open", while D:686 and D:877 say "settled as recommended" (ruling 39). Either way the ruling is Clay's, not the owner's, so for the owner it stays a proposal (D11). I now cite both lines.

---

# TASK A: Rebuttal

## A1. Reply to each criticism in CLAY's "Weaknesses identified in OURS"

**CLAY W1: "No neighbour list (C-001, C-007)".**
Counter and partial concession. My Round 1 table had a "Needs (neighbour)" column on every row, so the claim that OURS has no dependency column is not right. The deeper point, that the leaning is wider than my one example, is right, so here is the full list. CLAY names five interlocks (Strengths 1). I checked each against the verdicts and the design:

| Interlock named by CLAY | My finding | Why |
|---|---|---|
| Merge: `E-NO-GRANT` does not see a raw `gh pr merge`, so one verb must demand the go entry; gate run twice; new reason "no recorded merge go" (D06 item 8, D04 item 6) | Real. One build unit ("merge path") | I conceded this in Round 1. |
| `repos` verbs refuse to change `grants`, `reach_daily_max`, `merge_safety_files` without an accepted `--answer-ref` (D:758, D04 item 7) | Real. Joins the merge-path unit | It uses the same `answer-check`. |
| `refuse` release and tag patterns pass only with an `answer_ref` (D:767, D:763) | Removable | My G-9 reply below deletes the pass path, so the edge disappears. |
| `--interrupt` passes only when the caller is `escalate` (D:749, D:767) | Removable | My G-6 reply below drops the interrupt, so the edge disappears. |
| T13 pins merge-gate reasons and the `answer-check` question key together (D:1141) | Real, but inside the merge path | Same unit. |

So the interlock closure is one unit (merge gate, go entry, `answer-check`, `E-NO-GRANT`, the `repos` guard, T13), not a set of seven verbs. That is the dependency column CLAY asked for, and it is finite.

**CLAY W2: "Verbs priced as separate rows; no shared contract (C-002)".**
Concession on the build home (already in my Round 1), plus a number. D:510 lists 12 verbs: `wake-check`, `wake-ack`, `state`, `lease`, `merge-gate`, `plan-check`, `repos`, `report-entry`, `escalate`, `answer-check`, `audit`, `handback`. By my reading of D01 to D13, nine already have a verdict that adopts them in some changed form: `wake-check` and `wake-ack` (D10 items 1 to 3), `state` (D07 item 7), `merge-gate` (D06 item 2), `plan-check` (D01 item 2), `repos` (D07 item 5 and D04 item 7), `answer-check` (D04, D06 item 9), `audit` (D05), `report-entry` (D11 living report). Three have no verdict: `lease`, `escalate`, `handback`. Those are my G-1, G-6 and G-9, and G-3 below. So "one verb group with one JSON contract" is a fair build home for the nine, and the other three are decided here. I accept D:140 as the contract home. What I do not accept is that the group is one test unit: only the merge-path members must be tested together.

**CLAY W3: "No coordinator-layer live-test plan (U-004, C-008)".**
Counter and concession. I already adopted T1 to T13 and the U and K registers as the skeleton. Two corrections to their framing. (a) The owner's line is not without live evidence: D03 records 117 test functions and recorded real GitHub replies from throwaway issue 452 for the pipeline PR 682 deleted, and D07 item 1 records `tests/issue_watch/test_dispatch.py` covering the dispatcher loop on the owner's branch (I did not re-run either). (b) The plan cannot be adopted "as the single plan", because by my reading of D:1127-1141 six of the 13 rows test a rule that a verdict rejects or changes: T1 (listed repos and `repos.yaml`, D07), T3 (`setup-clone`, `repo_not_listed`, D07 and G-8), T4 (two orchestrators and the lease, D07 and G-1), T8 (autonomous merge of a clean PR, D06), T10 (the poll starts orchestrator 2, D07), T11 (poll label writes, D09 and Q03). The other seven (T2, T5, T6, T7, T9, T12, T13) need the D08 rename, and T12 needs the re-approval step I add in G-3. So the plan is a skeleton with six rows to rewrite, which is what I said.

**CLAY W4: "Capabilities absent: cap, restart, acknowledged wake, hand-back (C-005)".**
Concession. All four are capability gaps and I adopt all four: cap and restart (D07 items 3 and 4), acknowledged wake (D10), hand-back (G-3 below, adopt with change). They are right that an unmeasured constant is a reason to measure. My position is unchanged only on the labels: `HANDBACK_MAX` = 3 is "this design's value, not measured" (D:612, which I have now read), so it ships as a labelled default. For tiers I split (G-2 below): the coordinator session tier is adopted, the worker tier stays an unproven request until U28 passes, and `plan_tier` is not adopted.

**CLAY W5: "Wake defects are reasons to amend, not reject (C-004)".**
Concession. My Round 1 table already adopts the transport with M1 and M2 as conditions, but my per-point line said "OURS". That label undersold it. The transport is CLAY's (D10 picks it); the two conditions are OURS. Final: HYBRID.

**CLAY W6: "The reasons-table argument stops at 'edit one test' (C-003, U-001)".**
Concession on the label. The edit is cheap (`test_audit.py:86-98` pins 14 removed reasons and the sum `59 - 14 - 5 + 5 + 17 == 62` at line 98), and the closed table with a kind and an exit code per reason is a real pattern the owner's line lacks. D01 adds `plan_incomplete` and `held_backlog`, D07 adds `coordinator_full` and `name_collision`. We agree: keep the closed, pinned form and the changed exit codes (`ack_not_observed` and `attempts_exhausted` exit 7, lines 101-106), put the 14 approval reasons back as D01 needs them, and rewrite the pin. That is CLAY's own "OURS as is, CLAY as a pattern". Final: HYBRID, not the OURS I wrote.

**CLAY W7: "'Unbuilt counts against a piece' is asymmetric (X-001)".**
Partial concession. They are right that my R23, R25 and R33 are in an unpushed local plan, and that the guard binding for `worker-start` workers has never been observed (D05). I withdraw "unbuilt counts against". What I keep is narrower: under the weighting rule a benefit must be shown, and design text alone shows no observed benefit. CLAY supplies the benefit by capability gap (their Strengths 3), which is the right kind of evidence, and I accepted it. So X-001 is a split (see A4).

**CLAY W8: "OURS rests on the verdicts as if they were rulings (A-001)".**
Agreed. Both papers do. A-001 stays QUALIFY. Every row of the final table must carry "depends on owner decision" where the verdict says so (D01 R19, D04 R9 and R10, D06 amendments).

## A2. Reply to "What I ask the judges to take"

CLAY asks for a HYBRID with four parts. My answer to each:

1. **OURS decides every rule row.** Accepted. This is C-006.
2. **CLAY's control verbs built as one group against one contract.** Accepted for the nine verbs that have verdicts, and for the three decided in Task B below. Tested together only where they interlock (A1, W1).
3. **T1 to T13, the U-register and the K-register as the single test plan.** Accepted as the skeleton and the register of what is unproven. Not accepted "as is": six rows need a rewrite (A1, W3).
4. **A named amendment list, already finite in the verdicts.** Accepted as a method, rejected as complete. Their list names D04, D05, D06, D07, D08 and D10 amendments. It leaves out every design row that no verdict touched. Those are exactly G-1 to G-9 in Task B. By my reading each needs an amendment: DQ3 layer 4 (D:113), DQ4 (D:114), DQ9 (D:119), DQ13 and ADD3 (D:123, D:137), section 5.8 (D:720-734), wave 8 (D:603-620), section 5.12 (D:830-847), N6 and N7 (D:749, D:763-764), and the escalation rows of the audit (D:825). So "finite" holds only after these are added, and I add them here.

## A3. Points still in dispute after Round 1

1. **C-001 packaging boundary.** CLAY: all control verbs are one build and test unit. OURS: the merge path (gate, go entry, `answer-check`, `E-NO-GRANT`, `repos` guard, T13) is one unit; the other adopted verbs are independent. Small, but real: it decides whether one PR or several carries them.
2. **Single test plan.** CLAY: one plan, amended. OURS: the plan is a skeleton, six of 13 rows are rewritten, and the register of unproven items is adopted whole.
3. **Amendment list completeness.** CLAY: finite in the verdicts. OURS: finite only after Task B.
4. **X-001 weight of "unbuilt".** Residual: whether design-only verbs carry any weight beyond "needs building". I say none for or against; benefit must come from a capability gap.

Everything else is agreed by both papers: C-006 to OURS, C-007 tie to OURS, C-009 OURS on the home with CLAY key names, X-002 tie to OURS, A-001 QUALIFY, A-004 limits ("narrows", never "closes").

## A4. Final position on each point

| Point | Final | One-line reason |
|---|---|---|
| C-001 unit of adoption | HYBRID | Every rule row is decided per element by OURS; the merge path is one build and test unit and the verbs share one contract (D:140). Changed from my Round 1 "OURS". |
| C-002 status of unbuilt verbs | HYBRID | They are design text, so adoption is building; one verb group is the build home. Nine of 12 verbs already have a verdict; Task B decides the other three. |
| C-003 62-reason table | HYBRID | Adopt the closed table pattern, kinds and exit codes; the pin at `test_audit.py:94` is rewritten and the 14 approval reasons D01 needs come back. Changed from my Round 1 "OURS". |
| C-004 wake transport | HYBRID | CLAY's file plus ack wins (D10); M1 and M2 are mandatory conditions (OURS). Changed from "OURS". |
| C-005 tiers and hand-back | HYBRID | Hand-back adopted with a re-approval step (G-3); coordinator and worker tiers adopted as proposals, `plan_tier` and the effort keys not adopted until U28 and U30 pass (G-2). |
| C-006 contested rules | OURS | Both papers agree; five contested rules rejected or deferred (D01, D04, D05, D06, D07, D09). |
| C-007 who pays the rewrite | OURS (tie) | Rename (D08) and re-home (D07) are paid per row under both approaches; no figure favours the set. |
| C-008 readiness evidence | HYBRID | Merged and reviewed pieces adopted; unbuilt verbs and the presence-only plan check carry no proof. |
| C-009 settings home | OURS on the home, CLAY on key names | `issue-watch.d/<repo>.json` with a `merge` block (D07 item 5); no `repos.yaml`, no registry repo. |
| X-001 "never ran live" or "unbuilt" | SPLIT | Tie on "never ran live" (both lines, D10). Unbuilt design text proves nothing either way; the benefit rests on the capability gap, which CLAY showed. |
| X-002 piecemeal multiplies rewrite | Tie, so OURS | Same renames and re-homes per row either way; CLAY's residual "same three or four edits" is UNVERIFIED in size. |

---

# TASK B: Gaps no verdict decided

Method for each gap: I read the cited design lines, then the nearest owner-line evidence (verdict, contract line or code), then applied the weighting rule. "Needs" names the neighbours that must land with it. "Change" says what edits in code or doc. Every gap is also an input to the unified spec's amendment list.

## Summary table

| Gap | Element | Outcome | One-line reason |
|---|---|---|---|
| G-1 | Lease comment (DQ3 layer 4) | Defer to an owner decision | Real race, but it needs a second poller or a second user; the owner's line has its own cross-host lock (Q26) and the claim-marker guard (MR-2). |
| G-2 | Tier settings and efforts (5.8) | Adopt with change | Keep `coordinator_tier` and `worker_tier` as proposals; drop `plan_tier` (duplicates `refs/tiers.md`) and the effort keys until U30. |
| G-3 | Hand-back loop (wave 8) | Adopt with change | The closeout already prints the signal; the consumer is missing. But the re-plan edit voids the approval (D01 item 5), so each later round needs a recorded go. |
| G-4 | Naming rule (5.12) | Adopt with change | It forbids "generated with" lines in PR bodies, but 25 of the last 30 merged PR bodies in this repo carry one. The owner must set the scope. |
| G-5 | DQ9: type into terminals, approve prompts | Adopt with change (typing safety rules only) | Reject approving permission prompts: WC:122, WC:137 and WC:188 forbid it. Keep the FR-24 safety rules as extra conditions on typed nudges. |
| G-6 | N7 `escalate --interrupt` | Reject, defer to an owner decision | A second interrupt exception beside WC-14; no evidence it prevents harm; its receipt is unverifiable (U40). |
| G-7 | DQ13 info entries and ADD3 streams | Adopt with change (off by default) | The report already collects "involves" (`collect.py:201-215`); keep PR 686's read-only code behind a switch that is off, as D07 item 6 does for org search. |
| G-8 | DQ4 `setup-clone` | Reject | It needs `repos.yaml` (removed by D07) and a machine-changing step with no recorded owner authorization. Keep the origin check. |
| G-9 | Audit escalation rows and N6 | Adopt with change | Escalate only through a report line; fix AU5's bare `=======` rule; N6 becomes an unconditional refusal with no `answer_ref` pass path. |

## G-1. Lease comment (DQ3 layer 4; D:113 and the claim section D:544)

**Outcome: defer to an owner decision.** Record it in the unified spec as "reserved design, not built".

**What it is.** Before wave 1 the coordinator posts a comment `<!-- sc:orchestrator:lease host=<host> run=<run id> -->`, lists its own login's comments with that marker, and keeps the claim only if its lease has the lowest comment id; the loser edits its lease to `released` (D:113). D:544 runs `lease post` then `lease check` before `/sc:issue --claim`.

**Reason.** The race it closes is real: master's claim treats an issue already assigned to the current login as "continue, re-claim is allowed and idempotent" (`refs/claim.md`, Wave 2 item 4), so two coordinators on one login are not stopped by the claim. But the design itself says the lease matters only for "two hosts that each run a poll, two users' orchestrators, a hand-run `--take`, a store restored from a backup" (D:113). Under the D07 topology there is one cron entry and one dispatcher on one host, with a lock per child cycle. D07 names a second host polling as something that would change its verdict, so it is out of scope today. The owner's line already has two lines of defence: Q26's create-once claim files on a shared branch for cross-developer cases (D07 strongest point OURS 3; it acts at push time, D07 A-004), and the claim-marker guard `marker_in_window` that D01 item 4 (MR-2) requires. No observed double claim is cited anywhere. Under the weighting rule that is a tie, so OURS: do not build now.

**Cost if built.** One extra visible comment per claimed issue, carrying a host name and a Run id; one more write that needs the `issue.comment` grant (standing in D04 item 5) and `E-NO-GRANT`; a marker that names "orchestrator" and must follow D08 (`sc:coordinator:lease`); and an ordering rule: the D01 start re-check (MR-1) must run before the lease, not after.

**Needs.** D07 (topology; trigger to revisit), D01 (MR-1 and MR-2), D04 (the `issue.comment` grant), D08 (marker name).

**Change.**
- Doc: in the unified spec move DQ3 layer 4 to a "reserved, not built" list with the trigger "a second host or a second user runs a poll"; rename the marker; keep layers 1 to 3 (poll as only router, exclusive-create state file, the claim's own stops).
- Code: none now. If the owner later enables it: one verb `coordinator lease post|check`, one template, and T4 rewritten.
- Owner decision: "Do you want the lease comment built before a second host exists?" Default no.

## G-2. Tier settings `plan_tier`, `worker_tier`, `orchestrator_tier` and the effort keys (5.8; D:720-734; code `pr-a/.../repos.py:41-43`)

**Outcome: adopt with change.**

**What it is.** Three tier keys, defaults `tier1b`, `tier2`, `tier1b` (`repos.py:41-43`), plus `plan_effort` and `worker_effort`. A tier is a ccsession tier name, never a model id (D:722). The coordinator session is started with `ccsession <tag> --tier <tier>` (D:726); the worker through `worker-start --model claude-gw-<tier>`; the plan call passes `plan_tier` as the `--depth` of `/sc:issue --plan`. Validation reads the live tier list from `ccsession --help` (`repos.py:132-159`) and falls once to the next listed tier (D:730).

**Reason, key by key.**
- `orchestrator_tier` (renamed `coordinator_tier`): adopt. The `--tier` option exists in master (`ccsession:1001-1010`), and the master watcher has no tier setting at all (master `launch.py` has no `ccsession` or `--tier` text). That is a real gap with a verified mechanism for the session start. The live-list validation is better than a hard-coded list, because the available tiers depend on the user's role (`refs/tiers.md`).
- `worker_tier`: adopt the key as a request, not a fact. The path through `worker-start --model <picker id>` is UNVERIFIED (U28, D:726 and D:1286). D:726 itself says the worker's tier is "a request, not a fact" until the local test passes. Record `launch.effective`, as D:726 and D:728 say.
- `plan_tier`: do not adopt. The owner's `/sc:issue` already routes work by complexity to pinned worker tiers (`refs/tiers.md`: T3, T2, T1 agent files pinned in frontmatter), and D12 already defers a "higher tier floor at create" for lack of a cost baseline. A second knob for the same decision is an extra rule with no evidence. Revisit when D12's trigger (a cost baseline) is met.
- `plan_effort` and `worker_effort`: do not adopt until U30 shows which levels `worker-start` accepts (D:1288). PR 686 already has effort handling in `repos.py` (13 matching lines; I did not read them); keep it unused until U30.

**Needs.** D07 (the keys live in `issue-watch.d/<repo>.json`, not `repos.yaml`), D08 (rename `orchestrator_tier`; D08 action 8 already lists it), D10 (one-verb session start), D12 (plan depth), D05 (the worker route has no guard until the probe), the model-alias test `tests/skills/test_model_alias_policy.py` (D:726, U29).

**Change.**
- Code: in `repos.py` rename the key and the field `orchestrator_tier` to `coordinator_tier`; remove `plan_tier` and the effort keys from `DEFAULT_TIERS` and the parser; move the file format from `repos.yaml` to the per-repo JSON; keep the `TIER_ORDER` fallback and `parse_tiers`. Rename in the session-start code and the tests (`test_launch.py` has 20 lines mentioning tier, `test_cli.py` 15).
- Doc: rewrite D:60 (G6) and section 5.8 points 1, 4, 5 and 6; keep point 3 (recording `tiers` in the state file) and the limit that a tier name appears only on the two entry lines (D:832).
- Owner decision: none needed to start; the worker tier waits for U28.

## G-3. Hand-back loop (wave 8; D:603-620; `HANDBACK_MAX`)

**Outcome: adopt with change.** This moves C-005 to HYBRID.

**What it is.** When the closeout says a merged PR did not finish its issue (`issue.handback: remaining`), the coordinator records what remains, re-plans through `/sc:issue --plan --remaining`, makes a new branch and starts a new worker, up to `HANDBACK_MAX` = 3 hand-backs (4 rounds), stopping on `cap`, `no_progress` or `no_remaining` (D:612). The `handback` verb is a pure function over the saved closeout result and the state file and makes no GitHub call (D:613).

**Reason.** The producer is already on master: `sc-closeout-protocol/refs/result.md:40-47` prints `issue.handback: remaining` and the unmet criteria. D12 adopts `--remaining` (PR 690). Today the consumer of that signal is a person; D13 notes that closeout's `left_open` "feeds the hand-back loop of the PR 681 design". The bound is a testable pure function (the order at D:612 can be checked line by line), so this is a capability gap with a clear, separable benefit.

**The change I require, from the owner's rules.** D01 item 5 says any body edit after the approval voids it (`predicates.py:249-259`), and D01 item 1 requires an approval "unedited since" before any worker is started. The hand-back round re-plans by editing the issue body (D:618, the grant `issue.body.append_plan_sections`). So by D01's own rule the approval is void when round 2 begins, and the start rule fails by construction. Also D06 says merges need a person's go, and the owner's rule is that nothing starts work on an issue without a recorded approval. So:
- Round 1 stays as designed.
- For round 2 and later, `handback` prints `handback round=<n+1>` as a proposal, the state file goes to a new waiting step (for example `handback_awaiting_go`), and no worker starts until the person gives a go in chat that the agent records and `answer-check` accepts (Q01's chat rule). The go is bound to the issue, the round and the hash of the remaining file.
- `HANDBACK_MAX` = 3 stays as an upper bound and is labelled "this design's value, not measured" (D:612).
- The wait for the old worker to be final (D:614) stays; it matches WC:157 (restart only on a positive stall proof).

**Needs.** D01 (approval gate and the ordering rule), D06 and D04 (go entry and `answer-check`), D12 (`--remaining`, adopted with four fixes), D13 (closeout fields on master), D11 (entry lines), D07 (state file per issue), D08 (names). The `handback` verb is unbuilt: I found no `handback` verb in master (the only hits are the closeout skill's result fields and three agent or rule files); I did not grep pr-a or pr-p for it.

**Change.**
- Code (new): `handback` verb with the stop reasons; the waiting step and the go check; a test that the re-plan's body edit does not start a worker without the go.
- Doc: rewrite D:610-620 ("Not an escalation") so a hand-back is a proposal that waits for a go; rewrite T12 (e), (h), (i) to include the go; add the new step to the "State and restart" list at D:608.
- Owner decision: confirm that every round after the first needs a fresh recorded go.

## G-4. Naming rule (section 5.12; D:830-847)

**Outcome: adopt with change (the owner sets the scope).**

**What it is.** Nothing the poll, the coordinator or a worker writes where a person reads it may name the agent or the model: no model id, no agent product name, no "generated with" or co-author line (D:832). One exception: the commit trailer `Co-Authored-By: Claude Code <noreply@anthropic.com>` (ruling 39). A function `names_check(text)` with a deny list is run by the writer verbs and by tests (D:847).

**Reason for the change.** The rule collides with the repo's current practice. In this repository, 25 of the last 30 merged PR bodies contain "Generated with" (`gh pr list --repo IronbellyOrg/IronClaude --state merged --limit 30`), and the last 300 commit messages hold 300 `Co-Authored-By` lines (the trailer exception covers commits, not PR bodies). The design forbids the PR-body line outright (D:832, D:841). Master's own templates and skills have no such line (a grep of `src/superclaude` and `docs` finds the phrase only in the design file), so the lines come from the sessions' tools, not from owner files. Whether the owner wants them gone from PR bodies is the owner's call. The design calls this "owner ruling 15", but it defines the owner as Clay (D:3 and D:11, as D07 notes), so it is not shown to be the repository owner's decision.

Evidence on the false-positive risk (U54, D:1312, which asks for the last 50 issue titles): of the 50 most recent titles in this repo (any state), one contains "IronClaude" (a repository name) and six contain "Jev" (a model name in this repo's own work). Whether those trip the deny list depends on deny-list data that does not yet exist; the design skips backtick spans and quoted fences, but a title written as plain link text is not covered by those skips. This is a measurement, not a verdict.

**Needs.** D08 (names), D06 (who writes PR bodies: workers do not run `/sc:pr-submit`), D11 (report entries), the handoff prompt template (D:841).

**Change.**
- Doc: the unified spec states the scope the owner picks, one of: (A) as written (no attribution lines in PR bodies, comments or report entries; commit trailer allowed); (B) only the coordinator's own writers (`report-entry`, `escalate`) are scanned and workers' PR bodies keep the current practice. I recommend B for the first build because the design already says a worker's PR body "cannot be scanned before it is written" (D:847), and AD-X1 settled that the handoff line is the only rule there.
- Code: `names_check` under the coordinator package (not `orchestrator`); the deny list as data; run the 50-title measurement before enabling (U54).
- Owner decision: A or B, and whether "generated with" lines in PR bodies stay.

## G-5. DQ9: the coordinator types into worker terminals and approves worker permission prompts (D:119, D:573, D:752)

**Outcome: adopt with change.** Adopt the typing and its safety rules; reject answering permission prompts.

**What it is.** DQ9 puts check-ins, typed keys and approvals inside the coordinator skill, under the "FR-24 safety rules" of wave 5 (D:573): (1) the prompt is on the current screen; (2) no output in 60 seconds and an empty draft; (3) re-read the screen just before sending; (4) the single-use yes, never "always allow"; (5) re-read after sending and log the exact key; (6) a prompt for rows 1 to 7 of the escalation table is never approved; (7) an approval never relies on text from an issue or comment. D:752 lists "Answer one approval once".

**Reason.** The two halves differ.
- Typed nudges and check-ins: the owner's contract already allows them, with strict rules (WC:135 one typed copy per message id at an idle empty prompt; WC:152-153 typed nudge and ask with `--wait-submit`). Clay's rules (1), (2), (3) and (5) are extra conditions on top of that and cost nothing. Adopt them.
- Answering a permission prompt: the contract forbids it. WC:122 says state S4, "blocked on a person prompt", is a person-only state: "never answer the prompt". WC:137 says "never type into a busy, S11 or S4 session; never answer a person prompt". WC:188 lists "answers a permission or person-only prompt" under "Never on silence". D06 INV-003 shows a script cannot be told from a person at the same terminal, and WC:199 lists as UNVERIFIED "what Claude Code does with text typed while a tool call runs". No measured gain from approving is given anywhere (D06 notes that Clay's throughput gain has no figure). Under the weighting rule that is a tie, so OURS.

**Needs.** WC:122, 137, 188 stay unchanged; D10 item 3 (typed line only to an idle person-opened session); D05 (guard); the playbook ref (D:507) loses its "approval" rows.

**Change.**
- Doc: rewrite DQ9 (D:119), wave 5 (D:573) and D:752 so that S4 is reported (L5, re-reported every 15 minutes per WC:155) and the approval rules (4) to (7) are removed; keep rules (1), (2), (3), (5) as typing conditions; the typed parts of FR-10 and FR-23 stay in scope, the approval part of FR-24 does not.
- Code: the typing tests of D:1106 keep their fake `orca terminal` cases for (1), (2), (3), (5); the cases that expect an approval are dropped.
- Owner decision (optional, later): a closed list of prompt classes the coordinator may approve, recorded in chat, if stalls turn out to cost more than the owner wants.

## G-6. The single interrupt exception, N7 `escalate --interrupt` (D:749, D:764)

**Outcome: reject for the first build; defer to an owner decision.**

**What it is.** The verb writes an escalation first, then sends `orca terminal send --interrupt` to stop a worker's current turn, only for a case that fits a row of the table of 5.6 (D:749). It is exempt from the 60-second typing hold. The design says it reverses AD-C1 (ruling 25) and conflicts with the coordinator spec in five places, C25 to C29 (D:764).

**Reason.** The owner's contract already has one interrupt: the S6 context-exhausted nudge (WC-14 exception at WC:63 and WC:124), and its typing rule says "Input veto: never interrupt" (WC:137). N7 adds a second. The benefit it claims is to stop a worker that is about to do something that fits rows 1 to 7 (identity, secret, money, legal, irreversible, other people's access, breaking change). The design offers no incident for it. Orca gives no receipt that says whether text reached a live turn or waited behind it (U40, D:1298), so the interrupt cannot be confirmed to have landed. An interrupt does not undo what is already done. The real brakes for those rows are the launch guard and the person's go (D05, D06). Ruling 25 is one of Clay's rulings 23 to 35 (D:1170), not the owner's. Tie, so OURS.

**What I keep.** The ordering rule "the verb writes the escalation first and sends nothing if the escalation is refused" is a good pattern for the `escalate` verb in general; keep it as a rule of `escalate` with no interrupt attached.

**Needs.** D11 and D06 item 11 (the nine-row list is an inventory pending an owner decision); G-9 (`escalate` verb); WC:63 and WC:124 unchanged.

**Change.**
- Doc: delete the "Interrupt a worker, in one case" row (D:749); in N7 (D:764) drop the exception so it reads "no `worker-stop`, no `worker-abandon`, no Escape or Ctrl+C by `terminal send --text`, no `terminal send --interrupt`"; remove `--interrupt` from the verb list (D:140, D:510); do not apply C25 to C29.
- Code: the `limits.py` pattern for N7 has no `caller` branch (D:767); the `escalate --interrupt` tests (D:1106) are not written.
- Owner decision: "May the coordinator ever interrupt a running worker besides context exhaustion?" Default no.

## G-7. DQ13 information entries (`could_assign`, `mention`, `affects`) and the three info search streams (ADD3; D:123, D:137, D:184)

**Outcome: adopt with change (off by default).**

**What it is.** Wave 0 writes an information-only entry for each of the three kinds into `.dev/coordinator/orchestrated/info/`, under "Watching", dropped after `info_ttl_days` (14) (D:123). The poll reads three extra streams per org, one search each, about 8 calls per cycle against a budget of 35 (D:137), and the wake file carries `info.mentions[]`, `info.could_assign[]`, `info.affects[]` (D:184).

**Reason.** Two of the three kinds duplicate what the owner's line already collects. The report skill's collector gathers "open items the person is involved in (author, assignee, mention, commenter)" with one `gh search issues --owner <org> --involves <person>` per org (`collect.py:201-215`). `mention` and `affects` are subsets of "involves". Only `could_assign` (new unassigned issues) is new, and it is awareness, never a claim (D:123). D07 item 6 already says org-wide search is optional, off in the first build, fail-open and never a discovery gate. Putting three more reads in the poll widens what the poll reads beyond discovery, which sits badly with NG-2's spirit that the poll does the minimum. But the code is written: `github.py:171` `argv_search_info`, `cycle.py:918`, `:1586`, `:1616`, and `wake.py` carries the fields. Deleting it costs more than switching it off.

**Needs.** D07 item 6 (the same off switch), D11 (report layer, entry files, the "Watching" section), D10 (wake schema), D09 (poll writes nothing).

**Change.**
- Code: keep `argv_search_info` and the info reads in PR 686 behind one config switch, default off, fail-open (a failed search, 100 or more results or a missing field skips nothing); the wake file's `info.*` arrays stay empty when off; the `mention` and `affects` kinds are not written as entries (the daily run already lists them, and D:123 says they merge by URL).
- Doc: mark DQ13 and ADD3's information streams "off in the first build"; the `could_assign` entry becomes a later addition to `collect.py` plus the "Watching" section, only if the owner wants it.
- Owner decision: "Do you want a list of newly assignable issues in the report?" Default no.

## G-8. DQ4: `orca project setup-clone` for a repo with no checkout (D:114, D:544, N5 at D:762)

**Outcome: reject.** Keep the origin check.

**What it is.** For a listed, enabled repo whose checkout is missing and which has a `clone_parent`, wave 1 runs `orca project setup-clone ... --destination <clone_parent>` once, re-reads the path, runs the origin check and writes the checkout into `repos.yaml` (D:114).

**Reason.** It rests on `repos.yaml` and `clone_parent`, which D07 removes. Under D07 the dispatcher lists projects with `orca repo list` and each coordinator lives in its project; a repo with no checkout is not a project yet and has no Coordinator worktree. The clone creates a directory on the host and adds an Orca project, which D:762 itself puts in the N5 class ("machine or VM lifecycle", with `setup-clone` as the one allowed `orca project` verb). No owner authorization for it is recorded; its stated basis is "FR-8 and Q12 in the coordinator spec", "since approvals are broad" (D:114; I did not read the spec, UNVERIFIED). Under D01 approvals are per issue and not broad, so that basis does not carry over. The origin check (`check_origin`, D:114) is a control the owner's line also requires (D07 "must be kept": per-launch origin check), so it stays. Code status: PR 686 has the `clone_parent` field (`repos.py:79`, `:350`) and the `missing` state (`cycle.py:1226`), but I found no `setup-clone` call in the poll code; it is coordinator text only.

**Needs.** D07 (repos come from `orca repo list`), D01 (approval per issue), D08.

**Change.**
- Code: remove `clone_parent` from `repos.py`; make `cycle.py:1226` always give `no_checkout`, a visible skip reason (D07 keeps "seen but not allowed" reasons); drop T3's first case.
- Doc: replace DQ4 with "a repo with no checkout is skipped with a visible reason; a person adds the project to Orca"; strike the `setup-clone` exception from N5.
- Owner decision (later): if the repo count grows, a recorded authorization per repo before any clone.

## G-9. Audit escalation rows (AU4a, AU4c, AU5 raise an escalation; D:825) and N6 (D:763)

**Outcome: adopt with change.**

**Part 1: audit escalations.** After a merge the audit reads the PR and prints violations and warnings. AU4a (merged over a change request), AU4c (merged with an unresolved thread) and AU5 (conflict markers) each raise one escalation per PR, written as lines of the issue's own entry; warnings never reach a person (D:825).
- Why adopt: under D06 the merge gate refuses `changes_requested` and `threads_open` and no go overrides them (D06 item 3). So AU4a and AU4c fire only for a merge made outside the gate, a person's raw `gh pr merge` or someone else's merge. That is the exact case the audit is the only detector for (D06 "Post-merge audit"). The volume is low and the cost is one report line.
- Change 1: the escalation goes only into the report entry (the existing "Needs you" path, D:825 items 1 and 2), not a ClickUp DM or a gate, until the owner rules on the nine-row list and the notice cap (D06 item 11 and D11 both leave them as owner decisions). No new notification channel is built.
- Change 2, the AU5 rule: the design flags a "bare `=======`" (D:815). In the master export, a search of `src`, `tests` and `docs` finds exactly one line of seven equals signs, a banner in `src/superclaude/cli/swarm/tmux.py:9`. Adding or editing such a banner would be flagged as a violation and escalated. Change the rule to: flag a line starting `<<<<<<< ` or `>>>>>>> `, or a bare `=======` only when an opener or closer is also present in the same file. I found no `<<<<<<< ` line in the markdown files of `src` and `docs`; I did not search other file types for it.
- Needs: D05 (audit adopted), D06 (gate reasons), D11 (report entry), `report-entry --update` (D:622).
- Code: `check_pr` pure function with the new AU5 rule and a test on a canned diff that adds a banner; D:1141 T13 case (e) uses a real marker, so add a banner case.

**Part 2: N6, release and tag only with a recorded OK (D:751, D:763, D:767).** The design lets the coordinator tag or publish when the call carries an `--answer-ref` that `answer-check` accepted.
- Why change: that sends the most irreversible action in the table (row 5 of D:676) through a check that cannot tell a person from a script (D06 INV-003, D06 item 9), and D06 item 1 says no outward action without a person's typed go. Also D:769 admits `refuse` sees only commands that verbs run, so the real protection is a test that scans the skill text for these commands, not a runtime pass.
- Change: N6 becomes an unconditional denial. The refusal function has no `answer_ref` branch for N6; releases are run by a person or by the release flow outside the coordinator. The scan test of D:769 asserts that `git tag`, `git push origin <tag>`, `gh release create` and package uploads do not appear in the coordinator skill or refs outside "Will Not Do" and the denylist file. This also removes one of CLAY's five interlocks (A1, W1).
- Merging a release PR stays allowed only as any merge: a person's go that names `release_merge_method` (D06 item 1).
- Needs: D06, D05 (`refuse(argv)` adopted), D04 (grants).
- Code: `limits.py` N6 patterns with no pass branch; tests: each argv refused, with and without an `answer_ref`.
- Doc: D:751 row deleted; D:763 rewritten; D:767 loses "The patterns of N6 pass only with an `answer_ref`".
- Owner decision: confirm that the coordinator never tags or publishes.

---

## Effect of Task B on the Round 1 table

Add these rows to my per-element table (all keyed on file and row, not on a PR):

| Clay element | Outcome | Change on the way in | Needs | Evidence |
|---|---|---|---|---|
| Lease comment | Defer to owner decision | reserved design; marker renamed | D07, D01, D04, D08 | D:113, `refs/claim.md` Wave 2 |
| `coordinator_tier`, `worker_tier` | Adopt with change | rename, per-repo JSON, worker tier a request until U28 | D07, D08, D10 | `repos.py:41-43`, `ccsession:1001-1010` |
| `plan_tier`, effort keys | Not adopted | revisit on a cost baseline and U30 | D12 | D:724, `refs/tiers.md` |
| Hand-back loop and `handback` verb | Adopt with change | go required for rounds after the first; `HANDBACK_MAX` labelled unmeasured | D01, D04, D06, D12, D13 | D:612, `sc-closeout-protocol/refs/result.md:40-47` |
| Naming rule 5.12 | Adopt with change | owner sets scope; measure U54 | D06, D08, D11 | D:832, 25 of 30 PR bodies |
| DQ9 typing and FR-24 rules (1), (2), (3), (5) | Adopt | extra conditions on typed nudges | D10, WC | D:573, WC:135, WC:152-153 |
| DQ9 approval of permission prompts | Reject | S4 stays a report | WC:122, 137, 188 | D:119, D:752 |
| N7 `escalate --interrupt` | Reject, defer | keep escalation-first ordering | D11, G-9 | D:749, D:764, WC:63, WC:137 |
| DQ13 and ADD3 info streams | Adopt with change, off by default | one switch; no `mention` or `affects` entries | D07 item 6, D11 | `collect.py:201-215`, `github.py:171` |
| DQ4 `setup-clone` | Reject | `no_checkout` skip reason; keep origin check | D07, D01 | D:114, `cycle.py:1226` |
| Audit escalation rows AU4a, AU4c, AU5 | Adopt with change | report line only; AU5 rule narrowed | D05, D06, D11 | D:825, D:815, `tmux.py:9` |
| N6 release and tag | Adopt as unconditional refusal | no `answer_ref` pass | D05, D06 | D:763, D:767, D:769 |

## What I could not verify

- The coordinator spec rows FR-8, FR-10, FR-23, FR-24, Q12 and the C25 to C29 amendments (IronFlow copy, not in this repository).
- Whether the owner ever runs a second poller or a second host (D07 lists it as a trigger, not as a fact).
- That `worker-start --model claude-gw-<tier>` works (U28) and which effort levels exist (U30).
- The size of the "same three or four edits" CLAY says repeat across rows.
- The number of PR bodies that contain "Generated with" beyond the last 30 merged ones, and the PR-body practice of unmerged branches.
- Whether the "Jev" titles would trip a deny list; the deny-list data is not written.
- Q26's exact text and the owner's unpushed rows R9, R17, R23, R25, R33 (taken from the verdicts).
- Whether `handback` exists in pr-a or pr-p (I grepped master only).
