<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (CLAY, variant-2-original.md) -->
<!-- Merge date: 2026-11-20 -->

# D05 merged position: the launch guard and orchestrator-started workers

<!-- Source: Base (original, modified) - the short-name list of the base paper, extended with the number glosses of Variant 1 and the debate files, so every name and number is defined once here -->

Short names and numbers, each defined once.

- "OURS" is the owner's line (the guard must govern every started worker). "CLAY" is Clay's line (a started worker runs without it). "The owner" is the repository owner, the account `ironbelly`. "Clay" is the account `clayphi`.
- "The guard" is `launch-level-guard.sh` (L1), a hook that blocks a governed agent's commit, push, merge and similar calls. "L2" is `launch-level-pre-push.sh`, the git pre-push hook.
- "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both on origin/master (snapshot `/home/coder/.cache/ic-snap-20261120/master`). "G2" is the note `docs/designs/issue-pipeline-guard-g2.md` in that snapshot; "G1" is the owner's earlier acceptance of a guard-less worker for the first test issue. "G2 rule 1" and "G2 rule 2" are two rules inside the guard (see the section Guard G2 rule 1 that PR 682 removed).
- "FS" is the guard level "full with `--submit`": it allows commit, push of a feature branch and `gh pr create --repo`. "W" is the guard's lowest (worktree) level, the only one where a release file (`.ok`) is read.
- Clay's tags: K12 (D:1234) is the risk that workers run with no guard, no L2 and push rights on their own branch, graded M / H (medium likelihood, high impact). DQ7 (D:117) is the rule that a `worker-start` worker runs without the guard. DQ8 (D:118) is the merge rule. OD1 (D:1152) is the decision on the worker's policy: it pushes its own feature branch, opens its pull request, never merges, never force pushes. ADD1 (D:135) is the "Orchestrated issue flow" section added to the worker contract. K22 (D:1244) and U42 (D:1300) are open items about the orchestrator's own typed commands. AU1 to AU8 are the audit checks (D:801-828). WC-9 (`src/superclaude/core/WORKER-CONTRACT.md:41`) is the contract rule that every outward default (push, merge, PR, GitHub post) is off.
- "INV-nnn" is a finding in `invariant-probe.md`; "R2A1" and "R2A2" are `rounds/round-2-advocate-1.md` and `rounds/round-2-advocate-2.md`. OB-H1, OB-H2, OB-H3 and OB-CTX are named observations in the issue 442 results, and the LL-... codes (LL-COMMIT, LL-MERGE and so on) are the guard's refusal names.
- Numbers. Issue 394: the issue that asked for the guard. Issue 442: the live observations of the guard, still open. PR 685: the runbook and results for issue 442, still open. PR 682: Clay's PR that deleted the issue-pipeline package and kept G2 rule 2. Issue 678: a bare `claude "<prompt>"` runs a turn outside the limits, open, and parked by the owner on 2026-11-19 so that no gate depends on it. PR 654: the pull request the issue 442 run opened in session E at level FS. PR 591: the Plan B PR by `ironbelly` that brought in the G2 sentence. Issue 655: the orchestrator design issue. PR 681: the PR that merged that design. PR D: the design's own name for the step that removes the issue-pipeline package. R33: a rule in `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` line 59 (worktree `claim-handoff-planb`) that closes the ship gate with `GOVERNED_LEVELS_ALLOWED = False` (`src/superclaude/cli/issue_watch/launch.py:48`), so only `--pipeline none` launches.

## Question

<!-- Source: Base (original) - question text given verbatim in the merge brief -->

CLAY DQ7 and K12 (D:117, D:1234) start workers with `worker-start` and no launch-level guard or L2 pre-push hook, with master unprotected. OURS (issues 394, 442, PR 685, R33 GOVERNED_LEVELS_ALLOWED=False) assume the guard governs every launch. Which wins, and should the guard be required for orchestrator-started workers? Include guard G2 rule 1 that PR 682 removed.

## Merged position

<!-- Source: Base (original, modified) - the base Claim is rewritten to follow the debate result; the base's recommendation to exempt workers is not kept, per the plan row C-001 -->
<!-- Source: Debate, debate-transcript.md - Scoring Matrix and Convergence Assessment -->

### Which line wins

<!-- Source: Debate, debate-transcript.md - Scoring Matrix, Convergence Assessment -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - the quoted sentence -->

- OURS wins the central question. C-001 (should a `worker-start` worker be inside the guard): OURS, 71%. C-007 (what the owner accepted): OURS, 78%. C-009 (FS equals Clay's own OD1 policy): OURS, 67%. X-002 (weight of the OB-H2 FAIL): OURS, 67%. The CLAY advocate said it in its own words: "OURS wins the central question (the guard is required for orchestrator-started workers), staged behind a live probe" (R2A2).
- CLAY wins two descriptions of today. X-001 (binding is easy or unproven): CLAY, 67%. X-003 (does the guard govern every launch): CLAY, 69%. The OURS advocate conceded both in Round 2.
- CLAY keeps real gains that OURS lacks, and the debate adopts them next to the guard, not instead of it: `refuse(argv)`, the head-pinned merge and the audit AU1 to AU8 (U-006; both advocates).
- Three points stayed unresolved by label only (C-002 lean CLAY 55%, C-005 lean OURS 63%, C-006 lean CLAY narrow 55%); the advocates agree on the facts and on the shape.
- Status: 14 of 17 scored points agreed (82.4%, threshold 80%), but the debate is BLOCKED_BY_INVARIANTS. The invariant probe found 7 HIGH findings left unaddressed (INV-003, INV-015, INV-019, INV-027, INV-034, INV-035, INV-037). This document carries them forward as stated limits (see Limits found by the invariant probe, inside the section Controls and what each one covers, and the section Open items).

### Should the guard be required for orchestrator-started workers

<!-- Source: Debate, debate-transcript.md - C-001 and C-007 -->
<!-- Source: Debate, rounds/round-2-advocate-1.md - Proposed resolution, points 2 to 5 -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - Test of the nine-point resolution -->

Yes, as the rule that should hold, staged and not exempted: bind the worker, prove the binding live, then enable. It is a statement of the rule, not a description of master today (see the section Evidence both lines agree on, block "What the guard governs today"). The owner's G2 text asks for binding "Before any other issue runs through the flow" (see the same section, block "What the owner accepted"). Where that deadline falls for the orchestrated flow is an owner decision (see the section Open items, item 1).

Required does not mean sufficient. Binding a worker at FS leaves K12 graded M / H: it covers plain pushes to `master` and `main` and nothing else a worker can do (see Limits found by the invariant probe). A push-time control outside the worker is the only thing that closes K12 (INV-037).

Staging gate. The OURS advocate proposed it in R2A1 (Proposed resolution, points 2 to 5) and the CLAY advocate tested and extended it in R2A2; the owner has not adopted it.

1. The first prompt of every `worker-start` worker carries `[sc-launch:v1:<nonce>]` (a line added to `templates/handoff-prompt.md`, D:637) and the orchestrator ran `orca_worktree.py pending --level full-submit` first.
2. A preflight before the first worker (jq present, hooks registered, the IR-4 checks) refuses to start a worker on failure; the test is a fixture with `jq` missing that gives a refusal and no worker. The CLAY advocate adds that the existing preflight sees only the claim process (`orca_worktree.py:955-960`), so the receipt in step 3 is the real check.
3. After the worker starts, the orchestrator checks that `pending/<nonce>` is gone; if it remains, it stops the worker and escalates. The CLAY advocate adds: pair it with a listing of `sessions/` and run it on a timeout (a denied first prompt starts no turn); the timeout value N is unset (INV-017). The test is a fake `worker-start` whose prompt carries no marker.
4. The first bound worker runs on a throwaway issue and records: the receipt; one `send` and one `ask` with no `--to` reaching the orchestrator (G2 facts 2 and 3); and a full `/sc:pr-submit --monitor 3` cycle at FS. The CLAY advocate adds a scripted `git push origin master` on a throwaway repo, the summary-thread step (see the section Controls and what each one covers, control 1, "Friction at FS"), and a bare `git push` plus a compound `git add && git commit`, both refused at FS (LD grid rows 13 and 15). Until the gate passes, DQ7 keeps "unbound" and K12 stays M / H.
5. Clay's controls are adopted whatever happens to the guard, with a test that fails if the design describes the audit as covering a push with no pull request.

The OURS advocate put the deadline at "before the second real orchestrated issue". The CLAY advocate showed that this is an event and not a switch, and that it clashes with G2:9 unless the first orchestrated issue is declared the one accepted test issue (see the section Open items, item 1).

### What the merge keeps from each line

<!-- Source: Base (original) - the base "What it gets right" list (Variant 2) -->
<!-- Source: Debate, base-selection.md - "Strengths to incorporate from the non-base" (Variant 1 strengths) -->

- From CLAY: it does not claim a protection nobody has observed on this worker; it puts controls at the point of use (the merge, the audit); it states the exposure in the design with a grade and a mitigation (K12); it keeps the guard's design intact and removes only what pointed at deleted verbs.
- From OURS: the one-issue scope of the owner's G1 acceptance and its "before any other issue" clause; FS equals Clay's OD1 policy and enforces its three prohibitions; the audit cannot see a push with no pull request; K22 and U42 have a precedent; the live PASS evidence; the binding helper still on master.

### How the design bounds an orchestrated worker today (Clay's mechanism)

<!-- Source: Base (original) - base Mechanism items 1, 2, 3 and 4; item 3a is inserted per Change #2 -->

1. The guard binds only a session whose first prompt carries `[sc-launch:v1:<32 hex>]` plus a pending nonce; an unbound session with no marker is allowed (LD:77, "Unbound with no marker: allow"). A `worker-start` worker has no marker, so the guard never sees it (D:117).
2. The orchestrator never launches through the claim's levels. The skill claims at `--pipeline none` and starts the worker itself (R9, D:81); a test fails if the skill launches through `orca_worktree.py launch` (K4, D:1226; DQ7, D:117).
3. What bounds the worker instead: the handoff prompt, the "Orchestrated issue flow" section of the worker contract (ADD1, D:135), and the rule that only the orchestrator merges, with `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` and never `--auto`, `--admin` or `--delete-branch` (DQ8, D:118). The orchestrator's own verbs pass through one function `refuse(argv)` that holds the "may never" patterns as data (5.9, D:767), and an audit after landing checks force pushes, dismissed reviews, threads resolved with no reply, conflict markers, loosened tests and changes to merge-safety files such as `src/superclaude/hooks/` (5.11, D:801-828).

<!-- Source: Variant 1 (OURS), Mechanism 3 - merged per Change #2 -->

3a. Level FS is word for word Clay's own policy for the worker (OD1, D:1152: it "pushes its own feature branch and opens its pull request ... never merges and never force pushes"). The guard enforces each of the three prohibitions mechanically at FS through grid rows: PUSHFORM refuses `--force` and non-plain pushes (LD:113), PROTECTED refuses a push to `master` or `main` (LD:114), MERGE refuses `git merge`, `gh pr merge` and MCP merge tools (LD:115). FS itself allows commit, push of a feature branch and `gh pr create --repo` (LD:25-30, grid LD:91-98). A written mapping of FS to OD1 does not exist yet (see the section Open items, item 8).

<!-- Source: Base (original) - base Mechanism item 4, with the probe note from Debate, invariant-probe.md INV-006 and INV-002 -->

4. The live test of the first worker records `ls ~/.claude/state/launch-level/sessions/` before and after the worker starts, and what the worker can reach (D:975, K12 mitigation D:1234). That listing cannot say whose file is new when up to three workers start in one cycle (INV-006); an inode match would (INV-002).

## Evidence both lines agree on

<!-- Source: Base (original, modified) - the base Cited facts, regrouped by topic; each block below carries its own tag -->

### What both papers and both advocates agree on

<!-- Source: Debate, diff-analysis.md - Shared Assumptions, agreement points (a) to (f) -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - Concessions and response 7 -->
<!-- Source: Base (original) - base cited fact 4 (guard limits) and fact 8 (inconsistency recorded in the design) -->

- An unbound `worker-start` worker is allowed by the guard. `master` is unprotected. K12 is graded M / H. The guard is a same-user guardrail, not a sandbox. PR 682 kept G2 rule 2. The watcher is `enabled: false`, so nothing runs today.
- The live value was re-read by both advocates: `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false`. DQ8 (D:118) records `protected: false`, and `rules/branches/master` and `rulesets` both `[]`.
- The guard is a "Same-user guardrail, not a sandbox"; it targets honest drift and one-step workarounds, "not TH3 (deliberate evasion)"; "Coverage is the explicitly checked routes, not universal prevention" (LD:32). Identity loss is a declared fail-open (LD:81). Pinned leaks stay allowed (`bash ./push.sh`, `G=gi; ${G}t push origin main`, LD:122).
- Clay's design is inconsistent about whether binding is still a live choice, and the CLAY advocate conceded it: D:117 says "This is a risk and not a question", D:1152 marks OD1 decided, D:970 (row 5d) leaves the guard-less condition to be "settled before the first real issue", D:975 keeps the issue 442 checks "if the owner chooses to bind its workers (OD1, option B)", and D:1002 keeps G2 rule 2 for the same reason.
- No CLAY control acts on a worker's `git push origin master`. The CLAY advocate conceded this in full after re-reading D:801-828 (see the section Controls and what each one covers, controls 3 to 5). The repository holds no push-time control of its own either: `.claude/settings.json` registers only two unrelated hooks (R2A2).

### What the guard governs today

<!-- Source: Base (original) - base cited facts 1 (first sentence) and 3 -->
<!-- Source: Base (original, modified) - R33 wording per the plan row C-004 (R33 gates only the claim launches) and X-003 wording per the plan row X-003 (the OURS line is stated as a rule, not as the state of master); sources Debate, rounds/round-2-advocate-1.md response 6 and rounds/round-2-advocate-2.md response 6 -->

- The guard's own scope excludes this worker, and the owner's text says so. LD:23: "A worker that a coordinator starts after a `--pipeline none` claim (the coordinator handoff, amended 2026-11-17) is not launched by the claim script, so this guard does not govern it."
- Under the owner's own plan nothing real is governed today. R33 sets `GOVERNED_LEVELS_ALLOWED = False`: only `--pipeline none` launches. A `--pipeline none` claim writes no launch record (IR-1, LD:349: "nothing for `--pipeline none`"), so the one launch that runs is ungoverned.
- R33 gates only the watcher's claim launches (`launch.py:48`; UNVERIFIED here, the invariant probe could not find that file in the snapshot, while both advocates read it in the worktree). Both advocates agree it does not forbid binding a `worker-start` worker; its reasoning supports staging by analogy and nothing more (C-004: SPLIT, 55%).
- So "the guard governs every launch" states the rule that should hold, not the state of master (X-003: CLAY, 69%; conceded by the OURS advocate). Both lines run an unguarded worker at the only level that launches today.

### What the owner accepted

<!-- Source: Variant 1 (OURS), fact 2 - merged per Change #1; the base sentence "adds no new exposure that the owner's own text did not already describe" is replaced, because base-selection.md graded it NOT MET on Correctness 1 -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - response 7, the literal escape that does not hold -->

The owner's acceptance was for one issue and not for the design. D:117 says: "The owner already accepted the same condition for the first test issue of the coordinator handoff ("G1")". G2 (`issue-pipeline-guard-g2.md:9`) says the guard-less worker was accepted "for the one first test issue" and "Before any other issue runs through the flow, the worker must be bound to the guard (G2)". DQ7 (D:117) cites that G1 as precedent for a standing rule for every issue. The sentence in the CLAY paper that DQ7 "adds no new exposure that the owner's own text did not already describe" does not stand against that source. C-007: OURS, 78%.

The CLAY advocate offered one literal escape: G2:9 says "this worker" and "the flow" of the Plan B handoff, and PR 682 removed that flow. D:117 itself calls the DQ7 condition "the same condition" as G1, so Clay tied the two, and the escape does not hold (R2A2, response 7).

### Who the owner is

<!-- Source: Debate, rounds/round-2-advocate-1.md - response 7, citing H-design681-map.md - merged per Change #8 -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - response 7 - merged per Change #8; the ambiguous word "owner" in the base Claim and fact 8 is fixed here -->

"The owner (Clay)" in D:3, and "owner" in D:1152 (where OD1 is "Decided (ruling 3, 2026-11-19 01:25 UTC)"), mean the account `clayphi` (permission `maintain`). The analyst map (`/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/H-design681-map.md`, lines 5-6, 16, 29, 33) shows every ruling, issue 655, PR 681 and the design approval came from `clayphi`; `ironbelly`, the repository owner and admin, left no comment, review or reaction on them. The G2 sentence came in PR 591, by `ironbelly`. So ruling 3 is Clay's and does not undo the repository owner's G2 condition.

- Ruling 3's row (D:1397) reads "workers push and open pull requests, never merge or force-push, only the orchestrator merges" and does not mention the guard. The guard-less clause sits in the OD1 and DQ7 cells.
- D:970 and D:975 leave binding open (see the block "What both papers and both advocates agree on", above).
- The risk is recorded and has a named decision step, not hidden: K12 (D:1234) is graded M / H with mitigations; OD1 (D:1152) is marked decided by ruling 3; D:970 sends the guard-less condition to "settled before the first real issue".
- UNVERIFIED: `RULINGS.md` was not read by the analyst or by either advocate.

### Binding a `worker-start` worker: what is known and what is not

<!-- Source: Debate, rounds/round-2-advocate-1.md - responses 1 to 3 and New evidence 1 to 3 - merged per Change #6 -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - responses 1 to 3 and New evidence 3 to 5 - merged per Change #6; this block replaces base cited fact 6 -->
<!-- Source: Base (original) - the first two sentences of base cited fact 6 (G2 facts 1 to 4 UNVERIFIED; FU-1 precondition f not tried) -->

Binding a `worker-start` worker has never been observed. The G2 facts 1 to 4 are UNVERIFIED (`issue-pipeline-guard-g2.md:40-43`): how to read the worker's session id, that `send` and `ask` reach the guard with full text, that an omitted `--to` reaches the coordinator, and that a `.ok` file changes the next call. FU-1 precondition f (does `worker-start` deliver a bound first prompt) was not tried (`docs/designs/issue-pipeline-fu1.md`, cited at g2.md:22). The OURS phrase "one marker line plus one `pending` call, not new code in the hook" is true of the hook and false of the whole job: small code, unproven effect (X-001: CLAY, 67%). What is known after Round 2:

- The helper is on master. `publish_pending` is at `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1488` and `cmd_pending` at `:1515` (the OURS paper had them swapped). `cmd_pending` writes the pending record for "a coordinator-started worker (G2)".
- The marker slot is gone. PR 682 deleted `brief.py` (its function `build` had the optional `nonce` slot) and `templates/worker-brief.txt` (section `[marker]`); `git show 01e7a9e23 --stat` lists both as deleted. The line must now be added to Clay's new `templates/handoff-prompt.md` (D:637), a new edit and not an existing switch.
- `cmd_pending` runs no preflight. The launch path runs the IR-4 preflight before `publish_pending` (comment at `orca_worktree.py:1726`); `cmd_pending` does not. The preflight sees only the claim process: its docstring says "The agent Orca starts may run with another one" (`:955-960`), and it is Linux only.
- Binding fails closed when a marker arrives. A marker prompt with no valid session id is denied LL-NOBIND (`launch-level-guard.sh:367`), and a failed binding is also a denial (`:384`). The fail-open of LD:81 applies only when no marker reached the hook. A prompt that starts `[sc-launch:` with a missing or used nonce binds as `degraded`, which reads as level W (`:268-271`, B12): loud, but not bound at FS.
- Binding leaves a receipt. On a successful bind the guard renames `pending/<nonce>` to `sessions/.take-<sid>` (`:373-375`), so "the pending record is gone" proves binding without a session id (limits of this receipt: INV-001, INV-002, INV-003, INV-014).
- The G2 collisions and the `.ok` release apply only at level W. The guard reads `.ok` only when the level is W (`:270`); the release code says "only at worktree ..., never at full or full-submit" (`:341-343`, release block about `:341-361`); the LD grid row 34 says "A, no write" at FS; G2 section 1 scopes both collisions to "the plan-writing worker". So G2 facts 1 and 4 (session id, a `.ok` written by another session) are not needed for an FS worker. G2 facts 2 and 3 remain UNVERIFIED (`issue-pipeline-guard-g2.md:41-42`) and are staging items.
- G2 rule 2 is in the guard (`:485-520`) and tested with real preamble shapes (`tests/hooks/test_launch_level_guard_worker.py:32,36,66,67`). `WORKER-CONTRACT.md:66` already says "Messages carry no `--to` ... the launch-level guard blocks any `--to` from a bound worker". The tests use synthetic envelopes, so "tests pass" is not "live".
- The marker is accepted "anywhere" in the prompt (LD binding paragraph). The claim path already delivers its marker with `orca agent launch ... --prompt` (`orca_worktree.py:1777-1778`), which produced bound sessions in the issue 442 runs. That narrows the unknown to "does `worker-start` deliver the task the same way". UNVERIFIED: whether the `worker-start` first prompt fires a `UserPromptSubmit` event.
- Shared assumptions A-001 and A-002 (both SPLIT with QUALIFY, 61% and 65%): the user-level hooks apply to the session `worker-start` creates only if that session runs under the same `HOME` and the hook gets a valid session id (A-001); the orchestrator is trusted only as a stated limit, backed by `refuse(argv)`, the head-pinned merge and the audit (A-002).

### How proven the guard is

<!-- Source: Variant 1 (OURS), fact 6 - merged per Change #5 (live PASS blocks and OB-CTX) -->
<!-- Source: Variant 1 (OURS), fact 7 - merged per Change #5 (OB-H2 FAIL rows are verbatim-detail checks; R33 honest gating) -->
<!-- Source: Base (original) - base cited fact 2, the FAIL list, kept; item 8 correction from Debate, base-selection.md (Correctness 1) and rounds/round-2-advocate-2.md response 6 -->

The two sides of the live record are both true (C-003: SPLIT, 61%).

- Passed live, in the real-session observations of issue 442 (`observation-results.md` in worktree `issue-442-runbook`): implement blocked (LL-IMPL, line 530); four commit attempts blocked (LL-COMMIT: two in session B, one each in C and D, lines 531, 535, 536); a bare `approved` did not unlock (line 532) while a typed `/sc:implement` did; `git merge` blocked (LL-MERGE, run 2, line 549); OB-CTX passed (lines 553-563): the selector told a governed `sleep 241` from an ordinary `sleep 242` and from a person's terminal in the same worktree.
- Failed or not done: OB-H1 item 8 FAIL (line 267, issue 678); OB-H2 FAIL (line 353); the protected push was never exercised because the agent declined twice (lines 537, 550); the `/sc:pr-submit --monitor 3` cycle at FS was not observed (a plain feature-branch push and `gh pr create` at FS did run in session E, PR 654, lines 508-514, so the gap is the monitor cycle and not push or PR creation).
- Weight of the FAILs. Within OB-H2 (lines 349-477) the only FAIL rows are the two preflight checks, and each says "the FAIL comes from the verbatim-detail check only; the refusal itself matched ... W-ENFORCEMENT-ABSENT" (lines 471-472); one inode sub-check is still pending (line 470). Item 8 is real but parked: the owner decided on 2026-11-19 that issue 678 is parked and no gate depends on it, so item 8 does not count against binding beyond staging (R2A2, response 6; base-selection.md, Correctness 1).
- Status. The guard's status line says "full enforcement not runtime-approved" and "no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass" (LD:6, LD:10, LD:17). Line 17 of the results says "FAIL in OB-H2: no governed claim on a real issue (runbook section 3). Report it instead." Issue 442 and PR 685 are still open. All live evidence is from claim-launched sessions; none is from a `worker-start` worker.
- The owner already treats unproven levels honestly: R33 holds `GOVERNED_LEVELS_ALLOWED = False` until a reviewed commit flips it and un-skips the observations. The rule is "no governed launch until it is proven", not "the guard is proven".

## Where the lines differ and how the debate settled each point

<!-- Source: Debate, debate-transcript.md - Scoring Matrix and Convergence Assessment. Winner and confidence are the mean of the two advocates' Round 2 positions; "agreed" means both advocates gave the same label. -->
<!-- Source: Debate, diff-analysis.md - topic names of the 17 scored points -->

| Point | Topic | Winner | Confidence | How it was settled |
|---|---|---|---|---|
| S-001 | Section order and formatting | SPLIT (tie) | 95% | Same six sections by the brief; no merit difference. This document uses its own section order. |
| S-002 | Numbered-list presentation | SPLIT (tie) | 95% | Same list counts; presentation only. |
| C-001 | What the guard governs today, and whether a `worker-start` worker belongs inside it | OURS | 71% | The CLAY advocate conceded the end state. LD:23 describes today; G2:9 and K12 (M / H) state the rule. Staged, not exempted. |
| C-002 | How hard it is to bind a `worker-start` worker | unresolved, lean CLAY | 55% | Binding is unobserved and the marker slot was deleted by PR 682. But at FS no `.ok` or session id is needed (`launch-level-guard.sh:270`). The advocates split on the label (CLAY versus SPLIT). |
| C-003 | How proven the guard is | SPLIT | 61% | Live PASS blocks and open FAILs are both real; the OB-H2 FAIL rows are verbatim-detail checks (see the section Evidence both lines agree on, "How proven the guard is"). |
| C-004 | Meaning of R33 (`GOVERNED_LEVELS_ALLOWED = False`) | SPLIT | 55% | R33 gates only the claim launches; `--pipeline none` writes no record (LD:349). One fact, two readings. |
| C-005 | What holds a worker back instead of the guard | unresolved, lean OURS | 63% | Both agree no CLAY control acts on a worker push to `master` (the audit is per `--pr`) and that CLAY's controls are adopted next to the guard. The advocates split on the label (SPLIT versus OURS). |
| C-006 | Friction between the guard and the pull-request workflow | unresolved, lean CLAY (narrow) | 55% | Reply and resolve run in scripts and work through a pinned leak; the summary-thread and fallback comments are inline `gh api` POST, GHWRITE at FS. Narrow and fixable (see the section Controls and what each one covers, control 1, "Friction at FS"). The advocates split on the label (SPLIT versus CLAY). |
| C-007 | What the owner accepted (G1) | OURS | 78% | G2:9 says "one first test issue ... before any other issue"; "owner (Clay)" is `clayphi` (see the section Evidence both lines agree on, "What the owner accepted" and "Who the owner is"). |
| C-008 | GitHub-side protection of `master` | SPLIT | 61% | Both note `protected: false`; the guard covers only `master` and `main` (`launch-level-guard.sh:720`); a ruleset is the broader fix and has no owner yet. The merge records it as an open owner action, not as its own recommendation (see the section Open items, item 4). |
| C-009 | Which guard level an orchestrated worker would take | OURS | 67% | FS equals OD1 (LD:25-30 versus D:1152); the mapping is unwritten. |
| C-010 | Clay's K22 and U42 (a verb denylist does not bind typed commands; can a hook scope to one session) | SPLIT | 60% | OB-CTX is precedent for session-scoped hooks; the guard blocks MERGE at all levels, so it cannot bind the orchestrator (see the section Controls and what each one covers, control 3). |
| X-001 | Is binding easy or unproven | CLAY | 67% | "One marker line" is true of the hook and false of the whole job; the OURS advocate conceded. |
| X-002 | Weight of the OB-H2 FAIL | OURS | 67% | The FAIL rows are verbatim-detail checks; the refusal matched (lines 471-472). |
| X-003 | Does the guard "govern every launch" | CLAY | 69% | LD:23 and LD:349: a coordinator-started worker and a `--pipeline none` claim carry no launch record by design; the OURS advocate conceded. The merged text states the OURS line as the rule that should hold, not as the state of master. |
| A-001 | Hooks apply to the session `worker-start` creates | SPLIT (QUALIFY) | 61% | Same user and `HOME` likely; delivery by `worker-start` unobserved; the preflight sees only the claim process; the receipt tests it. |
| A-002 | The orchestrator is a trusted, ordinary session | SPLIT (QUALIFY) | 65% | Both lean on a trusted orchestrator; K22 and U42 stay open for both; the limit is to be written as a graded risk. |

Tally: OURS 4 (C-001, C-007, C-009, X-002); CLAY 2 (X-001, X-003); unresolved by label 3 (C-002, C-005, C-006); SPLIT 8 (S-001, S-002, C-003, C-004, C-008, C-010, A-001, A-002). Agreed points: 14 of 17 (82.4%).

Rejected carry-overs, kept out of this document on purpose:

<!-- Source: Base (original, modified) - the plan table "Changes NOT Being Made" (X-003, C-004, C-001, C-008), recorded so the reader can see what was not adopted and why -->

- The CLAY claim that "the design must not make workers wait for the guard". The debate settled on staged binding, so staging is kept and exemption is not.
- The OURS Claim that "nothing the system starts runs ungoverned" as a statement of fact. It is false today (LD:23, LD:349).
- The OURS reading of R33 as honest gating only. R33 gates the claim launches only.
- Any proposal of a ruleset. Neither paper made one and the debate did not decide it.

## Controls and what each one covers

<!-- Source: Base (original, modified) - base Mechanism 3, cited facts 4, 5 and 7, "What it costs" and "What it risks", regrouped control by control; each control carries its own tag -->

"Seen live" below means observed in a real session in the issue 442 results, not read from code.

### Control 1. The guard (L1) at level FS

<!-- Source: Base (original) - base cited fact 4 -->
<!-- Source: Variant 1 (OURS), Mechanism 3 and facts 6 and 7 - merged per Changes #2 and #5 -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - response 5 (friction block) - merged per Change #9 -->

- Stops: at FS, commit, push of a feature branch and `gh pr create --repo` are allowed and everything else that matters is blocked (LD:25-30, LD:91-98): a force push or non-plain push (PUSHFORM, LD:113), a push to `master` or `main` (PROTECTED, LD:114), any merge (MERGE, LD:115), inline `gh api` writes (GHWRITE, LD:116). It fails open for what it does not govern: an unbound session is allowed silently and "Ordinary sessions are never blocked by a failure" (LD:81, LD:206), so requiring it for orchestrator workers cannot break the orchestrator's own session or a person's session. A bound worker fails closed: LL-BROKEN if `jq` is missing (LD:208-215).
- Does not stop: the pinned leaks (`bash ./push.sh`, `G=gi; ${G}t push origin main`, LD:122); a push to `integration`, `develop` or a repo's own default branch (only `master` and `main` are PROTECTED, `launch-level-guard.sh:720`; D:281-284); a session with no marker or a new session id (LD:81; INV-003); deliberate evasion (TH3, LD:32); tools outside the hook matcher (INV-036; UNVERIFIED whether a worker gets such tools); a hook killed by its 5 second limit (INV-011; UNVERIFIED whether such a call is let through). The guard has no level that allows a merge ("no level authorizes a merge", LD:32), so it cannot bind the orchestrator. Denials print only to the worker's stderr and leave no record (INV-028).
- Seen live: yes for claim-launched sessions (see the section Evidence both lines agree on, "How proven the guard is"). Never seen on a `worker-start` worker. Protected push never exercised. The status line says "full enforcement not runtime-approved" (LD:6, LD:17).
- Friction at FS (C-006, narrowed, lean CLAY 55%). `/sc:pr-submit` resolves threads with `gh api graphql ... resolveReviewThread` and replies with `gh api --method POST` (`src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh:131`, `:141`). The guard blocks inline calls of that class at every level (GHWRITE, LD:116), but these sit inside scripts, which pass only through the pinned gap `bash ./push.sh` (LD:122). They work through a leak. Two other steps are model-typed inline `gh api --method POST ... issues/<N>/comments`: the single summary thread (T-642, `summary_posted` in the contract, `SKILL.md:268`) and the fallback follow-up comment (`refs/thread-reply.md:87-89`, `:93-100`); no script posts them (`retrigger-review.sh:56` posts only a re-trigger body). The guard accepts only plain `gh api` tokens (`:554`); its block text names `gh pr comment` as the route instead (`:67-69`). So at FS those two steps are blocked as written and the worker must use `gh pr comment` (class SUBMIT, allowed at FS). Compound pushes are refused too (LL-PUSH-FORM, LD:283), and in the issue 442 run one blocked command was re-issued in split form (results line 540). The pr-submit merge cycle runs `git -c ... merge --no-commit --no-ff <base_sha>` inline (`refs/conflict-mechanical.md:77`), which FS blocks, but it is off by default (`--conflict-max-tier` defaults to 0, `SKILL.md:240`) and the design never passes the flag (no match in `orchestrator.md`); if the template later raises the flag, the worker stops at the merge. A bare `/sc:pr-submit --monitor 3` cycle at FS has never been observed. Small, fixable, not a veto.
- Extra cost of requiring it: one marker line and one `pending` call per started worker, plus the preflight (see the section Evidence both lines agree on, "Binding a `worker-start` worker"); a level has to be chosen for implementation workers (FS fits OD1, F fits WC-9, neither mapping is written).

### Control 2. L2, the pre-push hook (`launch-level-pre-push.sh`)

<!-- Source: Base (original) - base "What it costs" (L2 is not installed for that worker, D:117) -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - "An L2 position" -->
<!-- Source: Debate, invariant-probe.md - INV-029 -->

- Stops: it refuses a governed push to `master` or `main` at git level (`launch-level-pre-push.sh:17`, `:197-200`), and because it acts on git's own update stream it would catch the leaks the guard pins open (R2A2; INV-029).
- Does not stop: it is not installed for a `worker-start` worker. `install_l2` runs only inside the claim's launch step (`cmd_launch`, `orca_worktree.py:1754`; D:117) and no subcommand exposes it (`:1880-1893`). Its refusal path is off (`IR7_REFUSE = False`, `orca_worktree.py:822`). Whether it would classify a `worker-start` worker as governed is UNVERIFIED (its governed check reads job records that a bound Bash hook creates, `launch-job-identity.sh:386-387`).
- Seen live: not applicable to this worker, since it is not installed for it. The debate did not decide an L2 position (R2A2: "The resolution is silent on it"; see the section Open items, item 7).

### Control 3. Clay's `refuse(argv)` (the orchestrator's closed "may never" list)

<!-- Source: Base (original) - base cited fact 7 and the first bullet of "What it risks" -->
<!-- Source: Variant 1 (OURS), fact 4 - merged per Change #4, as corrected by both Round 2 files -->
<!-- Source: Variant 1 (OURS), fact 5 - merged per Change #3 (limits sentence) -->

- Stops: the orchestrator's own verbs pass through one function that holds the "may never" patterns as data (5.9, D:767), with a failing test for every pattern (D:1117).
- Does not stop: it "binds the verbs, not a command the model types itself" (K22, D:1244), and it acts on the orchestrator, not on a worker's `git push origin master` (conceded by both advocates).
- K22 and U42, with the correction. U42 (D:1300) asks "whether a hook can run `refuse` on the Bash calls of an orchestrator session only (not on every session of the host)". A session-scoped hook exists: the guard binds a session by marker plus a pending record (LD:75-77), and OB-CTX passed live (results lines 553-563). That answers the feasibility half of U42 by precedent only. The guard blocks MERGE at every level and the orchestrator is the only actor that merges (DQ8, D:118), so the guard cannot bind the orchestrator without a new level and rule set. It does not answer K22. The first OURS reading ("already built") shrank to "precedent" (U-002; both Round 2 files). C-010: SPLIT, 60%. K22 and U42 stay open and graded.
- Seen live: no. Both advocates accept that none of this control exists on master (U-006). The map rows 5.9 and 5.11 say "NEW. Nothing equivalent on master" (as cited in the CLAY paper; the CLAY advocate did not open the map, UNVERIFIED).

### Control 4. The head-pinned merge

<!-- Source: Base (original) - base Mechanism 3 and cited fact 7 -->

- Stops: the orchestrator's own merge. Only the orchestrator merges, with `--match-head-commit <sha>` and never `--auto`, `--admin` or `--delete-branch` (DQ8, D:118). The merge gate refuses `threads_open`, `changes_requested`, a moved head and an unreadable state (D:118, D:801-818).
- Does not stop: a worker's push. The gate acts on the orchestrator's merge (D:118). A typed `gh pr merge --admin` by a misbehaving orchestrator is covered neither by the guard (the orchestrator is ordinary and never blocked, LD:23) nor by `refuse(argv)` (verbs only; K22). That is the A-002 limit.
- Seen live: no; absent from master (U-006).

### Control 5. The audit AU1 to AU8

<!-- Source: Base (original) - base cited fact 7 -->
<!-- Source: Variant 1 (OURS), fact 5 - merged per Change #3 (the audit takes --pr, so a push to master with no pull request has nothing to audit); confirmed in Debate, rounds/round-2-advocate-1.md and rounds/round-2-advocate-2.md -->

- Stops: after a merge lands, `superclaude orchestrator audit --repo <R> --pr <N>` checks one landed pull request for force pushes, dismissed reviews, threads resolved with no reply, conflict markers, loosened tests and changes to merge-safety files. It grades AU1 to AU8 and escalates only the violations that can leave a merge broken or unreviewed (D:801-828, D:822-828).
- Does not stop: the audit verb takes `--pr <N>`, so a push to `master` with no pull request has nothing to audit. No CLAY control acts on a worker push; the CLAY advocate conceded this in full (C-005: lean OURS, 63%). Guard denials leave no record, so repeated blocked attempts are invisible unless the orchestrator reads the worker's screen (INV-028). Whether the guard source is on AU7's per-repo `merge_safety_files` list is not said (INV-031; default list text truncated, UNVERIFIED), so a bound worker editing `src/superclaude/hooks/scripts/launch-level-guard.sh` may go unflagged.
- Seen live: no; absent from master (U-006).

### Control 6. The prompt and WC-9

<!-- Source: Base (original) - base Mechanism 3 and "What it costs" -->
<!-- Source: Variant 1 (OURS), fact 8 - merged (WC-9 changed by ADD1 is the same layer of defence) -->

- Stops: an honest worker that follows its written contract. The handoff prompt and the ADD1 section are the only brake on the worker (K12). WC-9 says every outward default (push, merge, PR, GitHub post) is off and "no brief can turn it on"; ADD1 (D:135) turns it on by adding a contract section.
- Does not stop: a worker that ignores its prompt can push to `master`; nothing on GitHub stops it (`protected: false`, no rulesets, D:118). A written rule changed by a written rule is the same layer of defence (V1 fact 8; conceded by the CLAY advocate, Concession 2). The guard would be a second layer.
- Seen live: not applicable (text, not a mechanism). Clay's design records the exposure itself as K12.

### Control 7. A server-side rule on `master` (branch protection or a ruleset)

<!-- Source: Variant 1 (OURS), fact 1 - the live `protected: false` re-read -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - Separable CLAY benefits, item 2, and invariant-probe.md INV-037; recorded as an open owner action per the plan row C-008, not as a recommendation made by the merge -->

- Stops: per the CLAY advocate it is the only control left that also works against a deliberate worker, and unlike the guard it is not a name filter on `master` and `main` (`launch-level-guard.sh:720`). It needs no hook.
- Does not stop: nothing is set. The live value is `protected: false`, `rules/branches/master` and `rulesets` both `[]` (D:118; both advocates re-read `false`). Neither paper designed it and it has no owner, trigger or date (R2A2; INV-037). Classic protection answers 404 for `maintain` (D:118); `ironbelly` has admin per the analyst map; UNVERIFIED whether the login that runs the orchestrator can create a ruleset.
- Seen live: no. The merge makes no recommendation about it; see the section Open items, item 4.

### Limits found by the invariant probe

<!-- Source: Debate, invariant-probe.md - INV-003, INV-015, INV-019, INV-027, INV-034, INV-035, INV-037 - merged per Change #7, in plain words; the seven HIGH findings that blocked convergence are carried forward as stated limits -->

1. Binding at FS covers K12 only for plain pushes to `master` and `main` (INV-032, INV-033); it does not close K12. The probe's enumeration (INV-035) says the claim "FS closes K12" is true only for those pushes and "should read 'mitigates K12 for honest drift on master and main'".
2. A script run passes every gate (INV-034). A worker refused once that writes a file and runs it (`bash ./push.sh`, `python -c`, `uv run python x.py`, `G=gi; ${G}t push origin master`) meets no gate: the guard never reads written file contents (`launch-level-guard.sh:733-735`), L2 is not installed, and GitHub accepts the push (D:118). LD:122 pins these forms as allowed.
3. `integration` or another default branch passes (INV-019). Only `master` and `main` are refused (`launch-level-guard.sh:720`); a push to `integration`, `develop` or a repo's own default branch is a plain push and is allowed at FS (`:787`). The design stores `default_branch` and `release_head: integration` per repo (D:281-284, D:118).
4. A new session id runs unbound while the receipt still reads clean (INV-003). A valid id with no record is allowed silently (`launch-level-guard.sh:257`, `:391`). An Orca restart (L4, `WORKER-CONTRACT.md:157`), a hand-back round worker (D:619) or any new session id carries no marker. UNVERIFIED: whether Claude Code issues a new id on `/clear` or resume.
5. "Second real issue" cannot be counted (INV-015). Nothing counts issues; one orchestrator holds up to three in flight and up to six new issues a day (D:698-718, K21 at D:1242), so issues 2 and 3 can start before issue 1's probe finishes.
6. K12 is closed only by a push-time control outside the worker (INV-037). K12's root is that nothing outside the worker stops a push: `master` is unprotected and L2 is absent. K12 "should be re-graded, not closed".
7. Three gates disagree (INV-027): the guard's status line (LD:6, LD:17), the R33 constant, and the staging gate. The consensus binds real issues without saying which gate wins (see the section Open items, item 2).

## Guard G2 rule 1 that PR 682 removed

<!-- Source: Debate, docs/designs/orchestrator.md - section 7.3, D:995-1004 (snapshot /home/coder/.cache/ic-snap-20261120/master), the table and the review sentence -->
<!-- Source: Base (original) - base cited fact 9 (PR 682 kept narrow and reviewed; rule 2 stays) -->
<!-- Source: Variant 1 (OURS), fact 9 - the 7-line diff and the review result -->

The guard has two G2 rules (`issue-pipeline-guard-g2.md`). D:999-1002 sets them out:

| G2 rule | Lines | After PR D | Reason |
|---|---|---|---|
| 1. A TAMPER class for the coordinator-side `issue-pipeline` commands that write approval rows and the worker's release file | 441-444 | Removed (guard and its plugin copy, byte-identical) | The verbs it names no longer exist. The guard's own approval path for a governed worker (`sessions/<sid>.ok`, written by a person, FR-L-07, `launch-level-guard.sh:270`, `:347-351`) is a different mechanism and stays. |
| 2. A bound worker may run `orchestration send` and `ask` only as one plain call with no `--to`, so the message goes to its own coordinator Run | 489, 497-520 | Kept | It does not depend on the approval flow. It is needed by any governed worker that reports to a coordinator, and by every worker if the owner binds orchestrated workers (OD1, option B). It has its own tests, which stay. |

What rule 1 was. A comment (lines 441-443) and a `case` (line 444) that classed `*release-worker*`, `*release_worker*`, `*issue-pipeline*adopt-*`, `*issue-pipeline*record-*`, `*issue_pipeline*release*` and `*issue_pipeline*approval_record*` as TAMPER (D:991). It belonged to the plan-approval flow (WC-17, the `issue-pipeline` approval rows and `stage-status`, D:991) and concerned approval rows and the release file, not pushes, merges or binding.

Why it went. PR D removes the `src/superclaude/cli/issue_pipeline/` package whole, including the verbs `release-worker`, `adopt-create`, `record-create` and the rest (D:991). A TAMPER class for verbs that no longer exist guards nothing. The tests of rule 1 went with it (the `release-worker` and verb TAMPER cases, lines 270-287 of `tests/hooks/test_launch_level_guard_worker.py`, and `test_a_bound_worker_may_still_run_plan_hash_and_check_approval`, D:991). Two tests that depended on the deleted package were rewritten and not deleted, so the rule 2 tests still run (D:991).

What stays. Rule 2, and with it the whole of the L1 script (the CLAY paper, "What it gets right"). Rule 2 matters for the question: it already lets a bound worker send and ask with no `--to`, and `WORKER-CONTRACT.md:66` already assumes a bound worker (R2A2, response 1). So the removal of rule 1 takes nothing away from binding an orchestrated worker at FS. The `.ok` release that rule 1 sat beside applies only at level W (see the section Evidence both lines agree on, "Binding a `worker-start` worker: what is known and what is not").

How it was reviewed. The design note requires an independent review of any change to the guard (`issue-pipeline-guard-g2.md`, header). PR D carries that review as an acceptance check, and the comments that cite `issue-pipeline-guard-g2.md` (lines 441 and 500) are updated to say the rule 1 text is retired (D:1004). `git show 01e7a9e23 --stat` shows 7 lines changed in each copy of the guard (V1 fact 9), and E-pr682.md records the independent review as PASS (V1 fact 9; V2 fact 9). UNVERIFIED: the CLAY advocate did not open E-pr682.md and called that result partly self-reported.

## Open items

<!-- Source: Debate, rounds/round-2-advocate-1.md - Proposed resolution and response 7 -->
<!-- Source: Debate, rounds/round-2-advocate-2.md - Test of the nine-point resolution, "What the resolution still lacks" -->
<!-- Source: Debate, invariant-probe.md - UNADDRESSED findings and the UNVERIFIED list; the server-side rule and the fallback are listed per the plan "Base Weaknesses Addressed" table as open owner actions, not as recommendations of the merge -->

1. The deadline for binding. G2:9 says "Before any other issue runs through the flow". The OURS advocate proposed "before the second real orchestrated issue", which is an event and not a switch (R2A2) and cannot be counted (INV-015). It clashes with G2:9 unless the first orchestrated issue is declared the one accepted test issue. The CLAY advocate also asks that the owner be asked in so many words whether one more real orchestrated issue may run unbound while the gate is open; K12 stays M / H meanwhile. FU-1 step f already ran an unbound worker on 2026-11-17 (`issue-pipeline-fu1.md:113`); UNVERIFIED which issue the G1 acceptance meant (INV-016). The CLAY advocate also notes the rule becomes testable only as a code switch like R33's constant.
2. Which gate wins (INV-027): the guard's status line, R33's closed constant, or the staging gate. R33 gates only claim launches (`launch.py:48`).
3. Wording of the guard-less condition. DQ7's guard-less condition is the repository owner's open item G2 and not a decided ruling. It stays marked "open, owner decision" and is never described as decided by ruling 3 (R2A1 point 1; the CLAY advocate found it clear and testable but needing the owner's confirmation). The D:1397 row omits the guard. Clay's design also says "This is a risk and not a question" (D:117) while D:970 and D:975 leave it open; the design is inconsistent and the debate did not settle which text wins.
4. A server-side rule on `master`. An owner action, not designed here. Live value: `protected: false`, no rulesets. It has no owner, trigger or date (R2A2: a bare live value is "Not testable"). The merge makes no recommendation. UNVERIFIED whether the orchestrator's login may create a ruleset.
5. Fallback if the staging probe fails. If `worker-start` does not deliver the marker as a hook event, the staging gate says only that DQ7 keeps "unbound", so "required" binds nothing. The CLAY advocate suggested naming a fallback: no real orchestrated issue until a server-side rule protects the branch, or the worker runs in a fork PR flow. Raised, not decided.
6. What covers `integration`, `develop` and other default branches (INV-019). Neither the guard (`launch-level-guard.sh:720`) nor L2 (refusal path off) covers them.
7. L2. The question names L2 and the debate did not decide a position on it: it is installed only in the claim's launch step, its refusal path is off, and whether it would treat a `worker-start` worker as governed is UNVERIFIED.
8. A written FS mapping and a written friction map: FS fits OD1, F fits WC-9, neither mapping is written (C-009); the marker line must be added to `templates/handoff-prompt.md` (D:637); the summary-thread step needs `gh pr comment` or `retrigger-review.sh --body`; the marker's place in the first prompt (a long Task spec may be cut to sections 1, 2 and 9 plus a path, D:567, U10, INV-013). The probe's receipt needs a timeout value (INV-017), a way to tell whose file is new (INV-002, INV-006), and a plan for restarts and nonce reuse (INV-003, INV-014; D:567, D:619).
9. K22 and U42 stay open and graded; the guard is cited as precedent for session-scoped hooks, not as the orchestrator's guard (A-002).
10. D:975's live test records "unbound". It would be wrong if the guard is extended to these workers; its wording has to change with the decision.
11. Scale. The orchestrator runs up to three issues at once (D:698-718), each worker holding push rights on its own branch, so the standing exposure grows with scale.
12. MEDIUM findings carried as warnings (they do not block): INV-001 (a `pending` record has no expiry; a crash leaves a live `full-submit` record), INV-002, INV-009 (a clean receipt does not show enforcement is registered), INV-011, INV-012 (the bound-session Bash wrapper needs `uv` and Linux), INV-013, INV-014, INV-016, INV-021 (rule 2 admits only one-line calls up to 8192 bytes and 64 arguments), INV-023 (a bound session also passes the job-identity hook, which runs each Bash call in a fresh shell; live behaviour unverified), INV-029, INV-036. LOW findings are in `invariant-probe.md` (INV-006, 017, 026, 028, 030, 031); two worth noting: guard denials leave no record (INV-028), and a prompt that quotes another worker's pending nonce deletes that record, so keep nonces out of text the orchestrator forwards (INV-030).
13. UNVERIFIED, carried from the debate and the probe: that `worker-start` delivers the marker as a hook event; whether a hook timeout lets a call through; whether Claude Code issues a new session id on `/clear` or resume; the worker's `HOME`, `PATH`, MCP set and host operating system; `launch.py:48` (not in the snapshot); which issue G1 covered; the contents of `RULINGS.md`; map rows 5.9 and 5.11 and E-pr682.md (partly self-reported, not opened by the CLAY advocate); G2 facts 1 to 4 (`issue-pipeline-guard-g2.md:40-43`); FU-1 precondition f.

