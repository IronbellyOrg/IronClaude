# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 82.4 percent (14 of 17 scored diff points agreed)
- Convergence threshold: 80 percent
- Convergence status: BLOCKED_BY_INVARIANTS (the diff-point score passes, but the invariant probe found 7 HIGH-severity UNADDRESSED items)
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, Variant 2 = CLAY; general-purpose agents, persona analyzer, default model)
- Fault-finder: 1 independent agent (Round 2.5), output in `invariant-probe.md`
- Round files on disk: `rounds/round-1-advocate-1.md`, `rounds/round-1-advocate-2.md`, `rounds/round-2-advocate-1.md`, `rounds/round-2-advocate-2.md`
- Shared-assumption responses: A-001 and A-002 answered by both advocates in Round 1 (QUALIFY, QUALIFY each). No omissions.

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

##### Round 1, Advocate 1 (Variant 1 = OURS), D05 launch guard for started workers

Persona: analyzer. Written 2026-11-20. Short names as in the papers: "the guard" is `launch-level-guard.sh` (L1), "L2" is `launch-level-pre-push.sh`, "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in the snapshot `/home/coder/.cache/ic-snap-20261120/master`.

#### Position summary

An orchestrator-started worker holds push rights on an unprotected `master` and is held back by prose alone (K12, D:1234), so the guard (or an equal mechanical control) should be required before the first real issue, in a staged way: bind first, prove binding live, then enable. Clay's orchestrator-side controls (`refuse`, the head-pinned merge gate, the audit) are real gains that OURS lacks and should be adopted next to the guard, not instead of it.

#### Steelman of Variant 2

The strongest CLAY case is this. The guard was built for sessions the claim script launches, and its own text says a coordinator-started worker "is not launched by the claim script, so this guard does not govern it" (LD:23). Requiring it therefore means building something new, not switching something on. The two things needed to build it are unproven: G2 facts 1 to 4 are all UNVERIFIED (`docs/designs/issue-pipeline-guard-g2.md:40-43`) and whether `worker-start` delivers a marker-bearing first prompt was never tried. The guard's own live proof is unfinished: issue 442 (the live observations) and PR 685 (its runbook and results) are both open, OB-H1 item 8 is a FAIL (a bare `claude "<prompt>"` runs a turn outside the limits, issue 678), and the protected-push row was never exercised (results lines 537, 550). The guard says it is "a same-user guardrail, not a sandbox" and leaves pinned leaks (`bash ./push.sh`, LD:32, LD:122). Making a half-proven, leaky layer a hard prerequisite would put the whole orchestrated flow behind an unfinished gate and give false assurance. Meanwhile Clay's design adds controls that exist nowhere on master: a closed "may never" list with a failing test per pattern (D:1117), a merge pinned to the head commit (`--match-head-commit`, DQ8 D:118), and an eight-check audit after each merge (D:809-818). The exposure is graded M / H, written down and sent to an owner decision (K12, OD1), not hidden. What CLAY gets right: it does not claim protection nobody has seen, it puts controls where the irreversible act happens (the merge), and it states its own risk.

#### Strengths claimed

1. **The exposure is on the record and the live value is unchanged.** K12 (D:1234) says only "the worker's written prompt (never merge, never force-push) holds it back from pushing" to `master`. `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false` today (re-run in this round). A prompt is a request, not a control.
2. **The one-issue acceptance does not stretch to a standing rule.** G2 says: "For the one first test issue the owner accepted that this worker runs without the launch-level guard (G1) ... Before any other issue runs through the flow, the worker must be bound to the guard (G2)" (`issue-pipeline-guard-g2.md:9`, read this round). DQ7 (D:117) cites that same G1 as precedent for a standing rule. The cited source says the opposite of what it is used for.
3. **Clay's own design keeps the door open.** D:970 (row 5d) leaves "the guard-less condition of DQ7" open until "settled before the first real issue"; D:975 and D:1002 keep the #442 checks and guard rule 2 "if the owner binds orchestrated workers (OD1, option B)". The code for option B survives on master: `cmd_pending` (`orca_worktree.py:1515`) writes the pending record for "a coordinator-started worker (G2)", and the deleted worker-brief builder had an optional `nonce` that adds the `[sc-launch:v1:<nonce>]` line (`git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/brief.py` lines 52-74, verified).
4. **FS is Clay's own OD1 policy, enforced mechanically.** OD1 (D:1152): the worker "pushes its own feature branch and opens its pull request ... never merges and never force pushes". The FS row allows "commit, push a feature branch, open a PR" (LD:25-30) and blocks PUSHFORM, PROTECTED and MERGE at every level (LD:91-98, LD:113-115). Nothing new to design; a mapping to write down.
5. **Clay's detective control cannot see the worst case.** The audit is per pull request (`--pr <N>`, AU1 to AU8, D:809-818). A worker that pushes to `master` with no pull request produces nothing to audit. The merge gate guards the orchestrator's merge, not the worker's push. Only a push-time control (guard, L2 or GitHub protection) covers it.
6. **Live PASS evidence exists for the exact blocks that matter.** `observation-results.md`: implement blocked (line 530), four commit blocks (B twice at 531, C at 535, D at 536), bare `approved` does not unlock (532), `git merge` refused (549), OB-CTX PASS (line 557) telling governed from ordinary and human sessions.
7. **OB-H2's FAIL is thin.** Within OB-H2 (lines 349-477) the only FAIL rows are the two preflight checks, and each says "the FAIL comes from the verbatim-detail check only; the refusal itself matched ... W-ENFORCEMENT-ABSENT" (lines 471-472). CLAY lists it as bare evidence the guard is unproven.
8. **The gate is already designed to wait for proof.** R33 (`GOVERNED_LEVELS_ALLOWED = False`, requirements.md line 59, `launch.py:48`) means no governed launch before OB-H1, OB-H2, OB-H3 pass. "Require the guard for orchestrator workers" can be sequenced behind the same gate, so CLAY's "do not wait on an unfinished gate" is answered by staging, not by dropping the rule.
9. **WC-9 is a written rule changed by a written rule.** WC-9 (`WORKER-CONTRACT.md:41`) says every outward action is off for a worker and "no brief can turn it on". ADD1 (D:135) overrides that with a contract section. Reversing a text rule with a text rule adds no layer; the guard would be the second layer.

#### Weaknesses identified in Variant 2

1. **Its scope argument describes the status quo, not a benefit.** LD:23 says the guard does not govern this worker today. That is the premise of the question, not an answer to it. Every DQ7 "evidence" cell (LD:77, `launch-level-guard.sh:1-8`, g2.md:5-8) shows the worker is unbound, not that it should be.
2. **Its "G1 accepted" support is for one issue only** (strength 2). D:117 says "the same condition". The condition was accepted once, with a stated deadline (g2.md:9).
3. **Its controls miss the push to `master`** (strength 5). `refuse(argv)` binds the orchestrator's verbs; K22 (D:1244) concedes it "binds the verbs, not a command the model types itself"; the worker types its own commands. The merge gate and the audit fire at or after a pull request. Fact 7 of the CLAY paper is true and still silent on the one path K12 names.
4. **"Unfinished gate" overstates.** The unfinished items (OB-H1 item 8, OB-H2 verbatim checks, OB-H3, protected push) are about launch-time binding and one prompt-decline; the live observations that the grid blocks commit, merge and implement are PASS (strength 6). The protected-push row stayed pending "and the cause is the prompt, not the guard" (line 550).
5. **Fact 3 (nothing real is governed today) is true and cuts against CLAY.** If both lines run an unguarded worker today, that is the exposure to close before the first real issue (D:970), not a reason to bless it. R33 exists because the owner will not call a launch governed until proven.
6. **Its guard friction is real but pre-solved in the observed run.** The `reply-resolve-thread.sh` calls (`gh api --method POST` line 131, `gh api graphql` line 141, verified) are scripts, which the guard pins as allowed (LD:122). The one observed blocked compound command was re-issued in split form and ran (line 540). A cost worth a fixture, not a blocker.
7. **It leaves K22 and U42 open and says "a hook" might fix them.** The session-scoped hook mechanism already exists in the guard (marker plus pending record), so U42's "can a hook run only on one session" has a working precedent on master. The paper lists this as a risk instead of reading the code.
8. **Scale cuts the other way.** Up to three issues in flight (D:698-718) each with a worker holding push rights multiplies the unprotected-`master` exposure, per CLAY's own paper.

#### Concessions

1. **X-001, binding is unproven.** My "one marker line plus one `pending` call" (Mechanism 2) is cheap in code (verified) and unverified in effect: G2 facts 1 to 4 and FU-1 precondition f are UNVERIFIED. The honest wording is "cheap to attempt, not yet shown to bind a `worker-start` worker".
2. **The guard leaks and is not a sandbox** (LD:32, LD:122); a bare `claude "<prompt>"` runs outside it (issue 678, open). It reduces honest drift. It does nothing against deliberate evasion (TH3).
3. **The guard is not runtime-approved** (LD:6, LD:17); 442 and PR 685 are still OPEN (re-read this round with `gh`).
4. **Owner-naming ambiguity.** D:3 calls Clay "the owner (Clay)", and D:1152 says OD1 was decided by "ruling 3". I could not verify (UNVERIFIED) that ruling 3 is the repository owner's. If it is Clay's alone, it does not override the repo owner's G2 sentence; if it is the repo owner's, strength 2 weakens. This must be settled by the owner, not by me.
5. **CLAY's orchestrator controls are real gains** (U-006): `refuse(argv)` with a failing test per pattern, `--match-head-commit`, AU1 to AU8, none on master. They should be adopted whatever happens to the guard.
6. **My U42/K22 claim is half true.** The session-scoped mechanism exists, but the guard has no level that allows a merge ("no level authorizes a merge", LD:32), so it cannot be bound to the orchestrator itself without a new level and rule set. It answers the worker half only.
7. **FS-to-OD1 mapping is not written** and the `/sc:pr-submit --monitor 3` cycle at FS was not observed (a plain push and `gh pr create` at FS did run, PR 654, lines 508-514).

#### Shared assumptions

- **A-001 (the user-level hooks apply to the session `worker-start` creates): QUALIFY.** True when the worker is a Claude Code session on the same host and `HOME` as the registered hooks, and the OB-H2 evidence command F3 already reads the hook's `HOME` and `CLAUDE_CONFIG_DIR` for claim-launched sessions (results lines 349-477). Nobody has run that probe for a `worker-start` session (G2 fact 1 UNVERIFIED). The test D:975 already plans (`ls ~/.claude/state/launch-level/sessions/` before and after the first worker) is the right probe; it should also record the hook's `HOME` and whether `UserPromptSubmit` fires. If hooks do not fire, a "required guard" binds nothing, so the requirement must be coupled to the IR-4 preflight (W-ENFORCEMENT-ABSENT refusal, results lines 471-472), which refuses rather than launches.
- **A-002 (the orchestrator is a trusted, ordinary session): QUALIFY.** Acceptable only because its outward verbs go through `refuse(argv)` and its merges through the head-pinned gate, and because the person opens it. It is the highest-power session (it merges). K22 admits typed commands escape `refuse`. The guard cannot cover it today (no level allows a merge). So "trusted" holds as a stated limit with the audit as backstop, not as a proven property; the guard requirement for workers does not depend on it.

#### Point positions

| Point | Superior | Confidence % | One-line evidence |
|---|---|---|---|
| S-001 | SPLIT | 90 | Identical section order by design of the brief; no merit difference |
| S-002 | SPLIT | 90 | Same list counts (4 / 9); no merit difference |
| C-001 | OURS | 65 | CLAY's LD:23 is the status quo; g2.md:9 says bind before any other issue; K12 graded M / H |
| C-002 | CLAY | 60 | G2 facts 1-4 UNVERIFIED (g2.md:40-43); OURS "cheap" is code-level only; code exists (`cmd_pending:1515`) |
| C-003 | SPLIT | 55 | PASS blocks (lines 530-549, 557) and FAILs (267, 353) both true; OB-H2 FAILs are verbatim-detail only (471-472), item 8 is real |
| C-004 | SPLIT | 55 | R33 gates governed launches; CLAY correctly notes `--pipeline none` writes no record (LD:349); both read the same fact |
| C-005 | SPLIT | 60 | CLAY controls are new and good (D:809-818, D:1117) but none stops a worker push to `master`; adopt as HYBRID alongside the guard |
| C-006 | CLAY | 60 | `reply-resolve-thread.sh:131,141` use `gh api`; works only via the script leak (LD:122); `/sc:pr-submit` cycle at FS never observed |
| C-007 | OURS | 70 | g2.md:9 "one first test issue ... before any other issue ... must be bound"; ruling-3 owner identity UNVERIFIED |
| C-008 | SPLIT | 55 | Both note `protected: false`; CLAY is right a hook is not the real fix; neither proposes a ruleset, a separable cheap HYBRID |
| C-009 | OURS | 60 | FS equals OD1 (D:1152, LD:25-30); CLAY has no level; mapping still unwritten |
| C-010 | SPLIT | 55 | Session-scoped binding exists (LD:75-77) but no level allows a merge (LD:32), so it covers workers, not the orchestrator |
| X-001 | CLAY | 60 | OURS says "cheap" and "never observed live"; resolved by wording "cheap to attempt, unproven" |
| X-002 | OURS | 70 | Only FAIL rows in OB-H2 are verbatim-detail; the refusal matched (lines 471-472); one inode sub-check still pending (line 470) |
| X-003 | SPLIT | 55 | LD:23 and LD:349 describe today; OURS Claim is the rule that should hold; both are true at different layers |
| A-001 | SPLIT | 60 | Both papers assume it unstated; QUALIFY, test with the D:975 probe plus IR-4 preflight |
| A-002 | SPLIT | 60 | Both assume it unstated; QUALIFY, holds only with `refuse`, the head-pinned gate and the audit as backstop |

Net on the weighting rule: OURS holds the central question (C-001, C-007, C-009) because CLAY shows no capability that replaces a push-time control and concedes the exposure (K12, M / H). CLAY clearly earns a HYBRID for its orchestrator-side controls (U-006), the `reply-resolve-thread` friction check (C-006) and a server-side `master` ruleset note (C-008). Recommended shape: require binding for orchestrator workers, staged behind a live probe (A-001) and the R33-style gate; adopt CLAY's controls in addition.

### Variant 2 Advocate (CLAY)

##### Round 1, advocate for Variant 2 (CLAY), debate D05: launch guard for started workers

Persona: analyzer. Written 2026-11-20. Read-only on every source. Short names as in the papers: "the guard" is `launch-level-guard.sh` (L1), "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in the snapshot `/home/coder/.cache/ic-snap-20261120/master`.

#### Position summary

On the end state OURS is right and I say so: an orchestrated worker with push rights on an unprotected `master` should be bound to the guard before the owner's G2 condition lapses. On sequencing and on cost CLAY shows evidenced benefits OURS lacks: binding a `worker-start` worker has never been done, it is not "one marker line", and the closed gate the owner wrote forbids governed launches on real issues until the live checks pass. The clean result is a HYBRID: keep Clay's orchestrator-side controls, mark the guard-less condition as the owner's open G2 item with a named trigger, and do not make the guard a precondition of the design today.

#### Steelman of Variant 1

The strongest OURS case is this. A written prompt is a request, not a control. The guard was built to replace "prompt only" (issue 394, the issue that asked for the guard). K12 (D:1234) grades the exposure M / H and says in Clay's own words that "only the worker's written prompt ... holds it back" from pushing to a `master` whose `protected` value is `false` (I re-read it live today: `false`). The owner accepted the guard-less worker for one first test issue only, and `issue-pipeline-guard-g2.md:9` says "Before any other issue runs through the flow, the worker must be bound to the guard (G2)". Clay's DQ7 (D:117) turns that one-issue acceptance into a standing rule. Level `FS` (commit, push a feature branch, open a PR; LD:25-30) is word for word Clay's OD1 policy (D:1152), and the grid already refuses a force push (PUSHFORM, LD:113), a push to `master` or `main` (PROTECTED, LD:114) and any merge (MERGE, LD:115). Clay's audit reads one landed pull request (`--pr <N>`), so a direct push to `master` is invisible to it (D:801-828). Clay's own U42 (D:1300) asks for a hook that binds one session only, which is the shape of the guard. And D:970 and D:975 leave "option B, bind the workers" open. All of this is correct and I verified the cited lines (D:117, D:118, D:1234, D:1152, LD:113-116, G2:9). OURS also has live PASS blocks in issue 442 (the live observations of the guard): LL-COMMIT, LL-MERGE, OB-CTX.

#### Strengths claimed

1. **Binding a `worker-start` worker is unbuilt and unobserved, so "required" is a promise, not a mechanism.** `issue-pipeline-guard-g2.md:40-43` lists four facts as UNVERIFIED: how the coordinator reads the worker's session id, that `send` and `ask` reach the guard with full text, that an omitted `--to` reaches the coordinator, that a `.ok` file changes the next call. G2 section 2 names two collisions between the guard and the handoff, measured on a base commit. OURS's own Risks section concedes this (X-001).
2. **The owner's own gate says no governed work on a real issue yet.** `observation-results.md` line 17 (worktree `issue-442-runbook`): "FAIL in OB-H2: no governed claim on a real issue (runbook section 3). Report it instead." OB-H1 item 8 is FAIL (line 267; issue 678, a bare `claude "<prompt>"` runs a turn outside the limits, still open). The protected-push check was never exercised (the agent declined, lines 537 and 550). The guard's status line reads "full enforcement not runtime-approved" (LD:6, LD:17, as cited in the paper). Binding an orchestrated worker at `FS` on a real issue is a governed launch on a real issue. R33 (the owner's ship-gate rule, `requirements.md` line 59 in worktree `claim-handoff-planb`) sets `GOVERNED_LEVELS_ALLOWED = False` for the same reason.
3. **The owner's plan already runs the ungoverned launch.** IR-1 (LD:349): "nothing for `--pipeline none`", so a `--pipeline none` claim writes no launch record. R33 allows only `--pipeline none`. LD:23 says in the guard's own words that a coordinator-started worker "is not launched by the claim script, so this guard does not govern it". "The guard governs every launch" is a line of intent, not a property of the owner's present plan (X-003).
4. **Clay added controls that master lacks, and they are separable from DQ7.** `refuse(argv)` with one failing test per "may never" pattern (D:767, D:1117); merge pinned with `--match-head-commit <sha>` and never `--auto`, `--admin` or `--delete-branch` (D:118); an audit AU1 to AU8 after each merge (D:801-828). The Clay design map rows 5.9 and 5.11 say "NEW. Nothing equivalent on master" (as cited in the CLAY paper; I did not open that map, UNVERIFIED). None of these needs the guard to be absent, so a hybrid keeps them.
5. **A concrete guard versus pr-submit mismatch exists.** `reply-resolve-thread.sh:131` runs `gh api --method POST` and `:141` runs `gh api graphql ... resolveReviewThread` (both lines read today). The grid classes inline `gh api` writes as GHWRITE at every level (LD:116). The worker contract (ADD1, D:135) has the worker run `/sc:pr-submit --monitor 3`. It would work only because the call sits inside a script, which the grid lists as a pinned gap (`bash ./push.sh`, LD:122). The `--monitor 3` cycle at level `FS` was not observed in 442 (a plain feature-branch push and `gh pr create` did run at FS in session E, pull request 654, the PR the 442 run opened).
6. **The risk is recorded, graded and given an owner decision, not hidden.** K12 (D:1234), the sentence "This is a risk and not a question" (D:117), the live test that records `ls ~/.claude/state/launch-level/sessions/` before and after the first worker (D:975), and D:970 ("settled before the first real issue").
7. **Server-side protection is the only control that works against a deliberate worker.** The guard is "a same-user guardrail, not a sandbox", aimed at honest drift, "not TH3 (deliberate evasion)" (LD:32, as cited in the paper, not re-read). Pinned leaks stay allowed (LD:122: `G=gi; ${G}t push origin main`). Clay's note that the real fix for an unprotected `master` is not a hook is correct. It is not proposed as a task, though (see Concessions).

#### Weaknesses identified in Variant 1

1. **"One marker line plus one `pending` call, not new code in the hook" is overstated.** G2 section 2 collision 1: a bound session cannot use `orchestration send` or `ask` unless the allow-list at `launch-level-guard.sh:471-474` changes (PR 682, Clay's orchestrator-groundwork PR, kept rule 2, which covers this, so that part is done). Collision 2: the guard lifts a block only on a typed user prompt starting `/sc:implement` or `/task` (`:347-351`); under a handoff the approval arrives as the result of the worker's `ask`, so the guard never writes `.ok`. G2 route A needs the coordinator to write `sessions/<worker session id>.ok`, and how the coordinator learns that id is UNVERIFIED (fact 1). Whether level `FS` needs a release at all is not shown by the paper. OURS counts the marker and the `pending` helper and omits the id problem.
2. **Minor citation slip.** The paper puts `cmd_pending` at `orca_worktree.py:1488` and `publish_pending` at `:1515`. Today `:1488` is `publish_pending` and `:1515` is `cmd_pending`. The helper exists either way; this changes nothing.
3. **Fail-open on identity loss undercuts "governs every launch".** LD:81 declares that a missing or invalid session id, or an unparseable envelope, allows without claiming enforcement. A `worker-start` worker whose session id the hook cannot read is silently ungoverned, and nothing in OURS's mechanism tests for that. The guard's own text says OB-H1 and OB-H2 must show a valid top-level id on every supported governed call, "otherwise deployment stops". That is a precondition OURS skips.
4. **U42 and K22 are not answered by the guard.** U42 (D:1300) asks about a hook that checks the Bash calls of the orchestrator's own session so a denylist can bind what the model types. The guard's grid blocks MERGE at every level (LD:115), and the orchestrator is the only actor that merges (DQ8, D:118). The orchestrator cannot be bound at any existing level. The guard's session-scoped binding is reusable, but an orchestrator policy is new work, so U-002 is an analogy and not an existing answer.
5. **The remedy has not been shown to fit the OD1 worker end to end.** OURS lists the missing level mapping (FS or F) as a cost but still says "no new rule". The GHWRITE and PUSH-FORM friction (a blocked compound command was re-issued in split form, `observation-results.md` line 540) lands on a worker that runs `/sc:pr-submit --monitor 3`, whose behaviour at `FS` nobody has observed.
6. **OURS reads the 442 evidence selectively in one direction too.** It cites the OB-H2 FAIL as a verbatim-detail miss (true, lines 471-472 say "the FAIL comes from the verbatim-detail check only; the refusal itself matched"). The file still sets the gate: line 17 says no governed claim on a real issue until it is resolved. Both are true, and only the gate reading bears on whether to bind a real worker today.
7. **OD1 is already marked decided by a ruling.** D:1152 marks OD1 "Decided (ruling 3, 2026-11-19 01:25 UTC)" and D:1397 lists it as "Owner ruling 3". D:3 says the design was "approved by the owner (Clay) ... (ruling 37)". The brief names the owner as someone other than Clay. I cannot tell from the files whether ruling 3 is the owner of this debate or Clay in that role (UNVERIFIED), so I do not rely on it. If it is the owner's, DQ7 is not a stretch of a one-issue acceptance at all.

#### Concessions

1. The end-state argument is OURS's. G2:9 is the owner's explicit text and CLAY's reading of it ("the guard does not govern this worker, so no new exposure") skips the clause "before any other issue runs through the flow, the worker must be bound".
2. K12 is graded M / H and CLAY's mitigations (prompt, contract, orchestrator-merges-only, audit) do not stop a direct push to `master`. The audit works per pull request (`orchestrator audit --pr <N>`); a push with no PR is outside it. The prompt and WC-9 (`WORKER-CONTRACT.md:41`, no outward action, "no brief can turn it on") are overridden by a contract section (ADD1), which is the same layer of defence.
3. D:970 and D:975 keep option B open while D:117 says "This is a risk and not a question" and D:1152 says Decided. Clay's own design is inconsistent about whether binding is still a live choice.
4. CLAY does not propose a GitHub ruleset or branch protection task, which is the control that would fix the exposure for all workers regardless of hooks. Pointing at it is not delivering it.
5. The live 442 PASS evidence is real: four commit blocks, a merge block (LL-MERGE, run 2, line 549), OB-CTX. CLAY's paper lists the FAILs without saying what passed. OB-H2's FAIL is a verbatim-detail check, as OURS says.
6. CLAY's Cited facts 7 and 9 are partly self-reported (the map rows, the E-pr682.md review result); I did not open E-pr682.md or the map, UNVERIFIED.

#### Shared assumptions

- **A-001 QUALIFY.** User-level hooks apply to a `worker-start` worker only if (a) the worker's Claude session runs under the same `HOME` and reads the same user settings, and (b) the hook receives a valid top-level session id on that worker's calls. Neither is observed: G2 facts 1 and 2 are UNVERIFIED, LD:81 makes a missing id a silent allow, and the claim's own preflight (jq present, hooks registered, W-ENFORCEMENT-ABSENT refusal) runs in the claim script, not in `worker-start`. If a guard is required, the preflight must run before the first worker or "required" binds nothing.
- **A-002 QUALIFY.** Treating the orchestrator session as a trusted ordinary component is acceptable only as a stated limit, not as a closed question. The orchestrator is the single actor allowed to merge, and its "may never" list "binds the verbs, not a command the model types itself" (K22, D:1244; U42 open, D:1300). Both variants lean on this trust. If the orchestrator misbehaves, neither the guard (it is ordinary, never blocked, LD:23) nor `refuse(argv)` (verbs only) stops a typed `gh pr merge --admin`. Condition for ACCEPT: U42 is answered, or the limit is written into the design as a risk with a grade.

#### Point positions

| Point | Superior (OURS, CLAY or SPLIT) | Confidence percent | One-line evidence |
|---|---|---|---|
| S-001 | SPLIT | 95 | Identical six-section structure by the brief; no merit difference |
| S-002 | SPLIT | 95 | Same list counts; presentation only |
| C-001 | OURS | 60 | G2:9 and K12 make the end-state case; CLAY is right only on today's scope (LD:23) |
| C-002 | CLAY | 70 | G2 collisions 1 and 2 and facts 1 to 4 UNVERIFIED; "one marker line" omits the session-id and release problem |
| C-003 | SPLIT | 60 | Real PASS blocks (LL-COMMIT, LL-MERGE, OB-CTX) versus no evidence for the paths this worker needs (protected push, monitor cycle at FS, worker-start binding) |
| C-004 | CLAY | 55 | R33 closed gate plus IR-1 (LD:349): the owner's present plan runs the ungoverned launch; "every launch governed" is intent, not state |
| C-005 | SPLIT | 60 | CLAY has controls master lacks (D:767, D:118, D:801-828), but none stops a direct push to `master`; adopt as hybrid |
| C-006 | SPLIT | 55 | `reply-resolve-thread.sh:131,141` hit GHWRITE and pass only through a pinned leak (LD:122); it works, and is unobserved at FS |
| C-007 | OURS | 85 | G2:9: acceptance was for "the one first test issue"; bind "before any other issue" |
| C-008 | SPLIT | 55 | Both note `protected: false`; CLAY names server-side protection as the real fix but proposes no task |
| C-009 | OURS | 80 | FS equals OD1 policy (LD:25-30 versus D:1152); CLAY leaves the worker with no level |
| C-010 | CLAY | 60 | U42 asks about the orchestrator's own Bash; the guard blocks MERGE at every level (LD:115), so it cannot bind the orchestrator |
| X-001 | CLAY | 70 | OURS Mechanism 2 ("not new code in the hook") conflicts with its own Risks and with G2:40-43 |
| X-002 | OURS | 60 | Lines 471-472: the refusal matched, the FAIL is the verbatim check; CLAY listed it unqualified (the line 17 gate reading still stands) |
| X-003 | CLAY | 70 | LD:23 and IR-1: a coordinator-started worker and a `--pipeline none` claim carry no launch record by design |
| A-001 | SPLIT | 60 | Likely true for the same user and `HOME`, but session-id delivery and fail-open (LD:81) are unobserved |
| A-002 | SPLIT | 65 | Both lean on a trusted orchestrator; K22 and U42 stay open for both |

#### Separable CLAY benefits for a HYBRID

1. Keep `refuse(argv)`, the head-pinned merge and the audit AU1 to AU8 (D:767, D:118, D:801-828). They stand with or without the guard.
2. Record DQ7's guard-less condition as the owner's open G2 item with a trigger: the guard becomes required for orchestrated workers before the second real issue, and the live test (D:975) tracks "unbound" until then.
3. Before that, close the unknowns that make "required" real: G2 facts 1 to 4, the FU-1 precondition (does `worker-start` deliver a first prompt with a marker), the `/sc:pr-submit --monitor 3` cycle at `FS`, and a written `FS` level mapping (C-009).
4. Add a server-side control for `master` (ruleset or protection) as the control that needs no hook. I did not verify whether the user has the rights, UNVERIFIED.

## Round 2: Rebuttals

### Variant 1 Advocate (OURS), rebuttal

##### Round 2, Advocate 1 (Variant 1 = OURS), D05 launch guard for started workers

Written 2026-11-20, read-only. Short names as before: "the guard" is `launch-level-guard.sh`; "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in `/home/coder/.cache/ic-snap-20261120/master`. "G2" is the note `docs/designs/issue-pipeline-guard-g2.md` in the same snapshot. Numbers below match the "Weaknesses identified in Variant 1" list of Clay's advocate (round-1-advocate-2.md). I re-read the source for every point before answering.

#### Response to criticisms

1. **"One marker line plus one pending call" versus G2 collisions 1 and 2 and the session-id problem.** Partly wrong, partly right.
   - Collision 1 (a bound worker cannot run `orchestration send` or `ask`) is closed on master. Rule 2 is in the guard today (`launch-level-guard.sh:485` sends `orchestration send|ask` to a raw-command check, `:503` is the pattern that admits one plain call with no `--to`). PR #682 (Clay's PR that deleted the issue-pipeline package) kept it, and D:1002 says so in Clay's words ("needed ... by every worker if the owner binds orchestrated workers (OD1, option B)").
   - Collision 2 (release needs a typed `/sc:implement`) does not apply at level FS. Does level FS need a release at all? No. The guard reads `.ok` only when the level is `W` (`:270`: `if [ "$LL_LEVEL" = W ] && [ -f "$LL_FILE.ok" ]`). The release code says "only at worktree ..., never at full or full-submit" (`:341-343`). The grid (LD:91-98, rows IMPL and TURN) allows implement at WA, F and FS with no release. So G2 route A, fact 1 (how the coordinator learns the worker's session id) and fact 4 (a `.ok` written by another session) belong to the plan-writing worker held at `W`. They are not needed for an orchestrated implementation worker bound at FS. Clay's advocate is wrong that the session-id problem blocks this.
   - What is still right in the criticism: G2 facts 2 and 3 (send and ask reach the hook with full text; an omitted `--to` reaches the coordinator's Run) are still UNVERIFIED (`issue-pipeline-guard-g2.md:41-42`). And my "one marker line" hid two verified costs. (i) #682 deleted the place the marker lived: `brief.py` function `build` had the `nonce` slot and `worker-brief.txt` the `[marker]` section (`git show 01e7a9e23 --stat` lists both as deleted). The line now has to be added to Clay's new `templates/handoff-prompt.md` (D:637), a new edit and not an existing switch. (ii) `cmd_pending` writes the record with no IR-4 preflight (`orca_worktree.py:1726` comment: the launch path runs the preflight before `publish_pending`; `cmd_pending` does not), so a "required" rule must add a preflight or it binds nothing when `jq` or the hooks are absent. Conceded as a defect in my mechanism text.
2. **Citation slip.** Conceded. I read the file again: `publish_pending` is at `orca_worktree.py:1488` and `cmd_pending` at `:1515`. My paper had them the other way round. The helper exists either way.
3. **Fail-open on identity loss (LD:81).** Half right, and the fix is cheap.
   - Where it is wrong: a worker whose first prompt carries a marker cannot be silently unbound. With a marker and no valid session id the guard denies the prompt (`:367`, `[ -n "$LL_SID" ] || ll_deny LL-NOBIND`), and a failed binding is also a denial (`:384`). The fail-open of LD:81 covers calls with no marker and no binding. So the loud failure is the first prompt, and the orchestrator sees a worker that never started a turn.
   - Where it is right: a marker that never reaches the hook (the first prompt arrives in a way that fires no `UserPromptSubmit` event, or the marker is not in it) leaves the worker silently unbound. FU-1 precondition f was never tried. Nothing in my paper tested for this.
   - The test needs no session id. On a successful bind the guard renames `pending/<nonce>` away (`:373-375`, `mv ... "$LL_TAKE"`). The orchestrator, an ordinary session that can read the store, checks that `pending/<nonce>` is gone after the worker's first turn. If it is still there, the worker is unbound and must be stopped. This extends D:975's probe (`ls sessions/` before and after); it does not replace it. UNVERIFIED that Orca's `worker-start` first prompt fires `UserPromptSubmit`; the probe is how to find out.
4. **U42 and K22 not answered by the guard.** Conceded in scope. The guard blocks MERGE at every level (grid row 17, LD:115) and the orchestrator is the only actor that merges (DQ8, D:118), so the guard cannot bind the orchestrator without a new level. What stands: U42 asks "whether a hook can run `refuse` on the Bash calls of an orchestrator session only (not on every session of the host)". The guard plus the live PASS of OB-CTX in the 442 results (`observation-results.md` lines 553-563: a governed `sleep 241` told from an ordinary `sleep 242` and from a person's terminal in one worktree) is working precedent that a user-level hook can be scoped to chosen sessions. That answers the feasibility half of U42 by precedent. It does not answer K22, and it is not an existing answer for the orchestrator. U-002 shrinks from "already built" to "precedent".
5. **Remedy not shown to fit the OD1 worker end to end.** Right in part. I checked the fit instead of assuming it.
   - `/sc:pr-submit` keeps its `gh api` writes inside scripts (`reply-resolve-thread.sh:131,141`; inline `gh api` appears in the refs only as documentation of what a script does). Scripts pass only through the pinned gap `bash ./push.sh` (LD:122). It works, by a leak, and nobody observed it at FS.
   - The merge cycle of pr-submit runs `git -c ... merge --no-commit --no-ff <base_sha>` inline (`refs/conflict-mechanical.md:77`), which is MERGE and blocked at FS. That cycle is off by default (`--conflict-max-tier` defaults to 0, `SKILL.md:240`) and the design never passes the flag (no match for `conflict-max-tier` in `orchestrator.md`). So the default `--monitor 3` command of ADD1 does not hit it. If the template later raises the flag, the worker stops at the merge.
   - Net: the friction is real but narrower than my paper implied, and the cycle at FS is unobserved. A written FS mapping plus one live run is required before "required" is true.
6. **Selective reading of the 442 evidence.** Partly fair. Line 17 of `observation-results.md` sets a gate for governed claims on real issues, and R33 closes `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`) for the claim path. That constant gates the watcher's claim launches at `worktree` and `full`, not a `worker-start` worker. It does not forbid binding an orchestrated worker; its reasoning (no governed launch on a real issue until observed) applies by analogy, so I accept the staging it implies.
7. **OD1 is "Decided" by ruling 3; who is "the owner" in D:3 and D:1152?** This matters most for C-007.
   - D:3 says "approved by the owner (Clay)". The analyst map (`/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/H-design681-map.md` lines 5-6, 16, 29, 33) shows every ruling, issue #655 (the orchestrator design issue), PR #681 (the PR that merged the design) and the approval came from the account `clayphi` (permission `maintain`). The repository admin `ironbelly` left no comment, review or reaction on them. The G2 sentence "for the one first test issue the owner accepted ... before any other issue ... bound" (`issue-pipeline-guard-g2.md:9`) came in PR #591 (Plan B, by `ironbelly`). So "owner" in D:3 and D:1152 means Clay. Ruling 3 is Clay's and does not undo the repository owner's G2 condition. UNVERIFIED: `RULINGS.md` was not read by the analyst or by me.
   - Even by Clay's ledger, ruling 3 is "workers push and open pull requests, never merge or force-push, only the orchestrator merges" (D:1397). That row does not mention the guard. The guard-less clause sits in the OD1 and DQ7 cells, while D:970 (row 5d) says the guard-less condition is "settled before the first real issue" and D:975 keeps option B open. Clay's design is inconsistent on whether this is closed, and their advocate concedes it (their Concession 3).

#### Updated assessment of Variant 2

Clay's advocate was candid and conceded the end state: the guard (or an equal control) should bind an orchestrated worker before the owner's G2 condition lapses (their Position summary, Concessions 1 and 2). That moves the debate from "whether" to "when and how proven". On those terms CLAY has real wins, accepted below: binding has not been observed on a `worker-start` worker, the marker slot was deleted, and the owner's present plan runs only the unguarded launch. Their strengths (controls absent on master, the pr-submit friction check, server-side protection as the only control against a deliberate worker) are sound and separable. Where they stay weak: no CLAY control stops a worker's direct push to `master` (the merge gate and audit act at or after a pull request; `orchestrator audit --pr <N>`, D:801-828), their C-004 and X-003 describe today's state and not the rule, and they show no evidence that binding costs more than the exposure Clay himself grades M / H (K12, D:1234). I re-read the live value just now: `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false`.

#### New evidence

All checked this round in the snapshot or the worktrees. UNVERIFIED marks what I could not run.

1. The release step exists only at level W (`launch-level-guard.sh:270`, `:341-361`; grid row 34 in LD: at FS "A, no write"). Level FS needs no `.ok`, no session id and no coordinator write. Read, not run live.
2. Binding is fail-closed at the first prompt (`:366-384`) and leaves a receipt: `pending/<nonce>` is renamed to `sessions/.take-<sid>` (`:373-375`). A check "pending record gone" proves binding without the session id.
3. The marker line has to be written into `templates/handoff-prompt.md` (D:637) because #682 deleted `brief.py` and `worker-brief.txt`. `cmd_pending` has no preflight (`orca_worktree.py:1515`; the preflight is in the launch path, comment at `:1726`).
4. "The owner (Clay)" is the `clayphi` account; the repository admin `ironbelly` wrote the G2 condition (PR #591) and shows no comment on #655 or #681 (H-design681-map.md). Ruling 3's row at D:1397 omits the guard.
5. The OD1 worker's default `/sc:pr-submit --monitor 3` takes no inline merge (`--conflict-max-tier` default 0, `SKILL.md:240`; `refs/conflict-mechanical.md:77` is the only inline `git merge`), and its `gh api` writes live in scripts.
6. R33 gates the watcher's claim launches only (`launch.py:48`); it does not by itself forbid binding a `worker-start` worker.
7. Not verified: whether `worker-start` delivers the first prompt as a `UserPromptSubmit` event (FU-1 precondition f); whether a ruleset on `master` can be created by the owner's login (the design says classic protection answers 404 for `maintain`, D:118; `ironbelly` has admin per the analyst map).

#### Concessions

1. X-001: my "one marker line plus one pending call, not new code in the hook" is true of the hook and false of the whole job. Honest wording: small code, unproven effect. The marker slot is gone (a new edit to the handoff template), a preflight is missing, and first-prompt delivery was never observed.
2. X-003 and C-004: "the guard governs every launch" is not true today. LD:23 says a coordinator-started worker is not governed, and IR-1 (LD:349) writes nothing for `--pipeline none`. The owner's line states the rule that should hold; it is not the state of master. CLAY is right on the description.
3. C-002: CLAY wins this point, narrowly. Binding a `worker-start` worker has never been shown (G2 facts 2 and 3, FU-1 f), and my paper counted code lines where it should have counted unknowns. The two G2 collisions are smaller than CLAY said (response 1), not gone.
4. Citation slip on `cmd_pending` and `publish_pending`: conceded (response 2).
5. U42 and K22 are answered only by precedent, not by the guard (response 4). The guard cannot bind the orchestrator.
6. The guard is not runtime-approved, leaks (`bash ./push.sh`), and is no defence against deliberate evasion (LD:6, LD:32, LD:122). Issue #678 (a bare `claude "<prompt>"` runs a turn outside the limits) is open, and so is PR #685 (the runbook and results for issue #442, the guard's live observations).
7. U-006 is a clear, evidenced CLAY gain, separable from the contested rule: `refuse(argv)` with a failing test per pattern (D:767, D:1117), the head-pinned merge (D:118), audit AU1 to AU8 (D:801-828). None exists on master. Adopt it.
8. The friction check C-006 is a fair finding (script leak, unobserved at FS). It becomes a probe, not a veto.

#### Updated point positions

| Point | Superior (OURS, CLAY or SPLIT) | Confidence percent | One-line evidence |
|---|---|---|---|
| S-001 | SPLIT | 95 | Same six sections by the brief; no merit difference |
| S-002 | SPLIT | 95 | Same list counts; presentation only |
| C-001 | OURS | 70 | CLAY concedes the end state; LD:23 describes today; G2:9 and K12 (M / H) make the case |
| C-002 | CLAY | 60 | Binding unobserved (G2 facts 2 and 3, FU-1 f); marker slot deleted by #682; collision 2 and the session id do not apply at FS |
| C-003 | SPLIT | 60 | PASS blocks (lines 530-549, 557) and FAILs (267, 353) both true; OB-H2 FAILs are verbatim checks (471-472) |
| C-004 | SPLIT | 55 | R33 gates claim launches only (`launch.py:48`); `--pipeline none` writes no record (LD:349); two readings of one fact |
| C-005 | SPLIT | 65 | CLAY controls are real and absent on master (adopt as HYBRID); none stops a worker push to `master` (audit is per `--pr`) |
| C-006 | SPLIT | 55 | `gh api` writes pass only via script leak (LD:122), unobserved at FS; default `--monitor 3` has no inline merge |
| C-007 | OURS | 78 | G2:9 "before any other issue"; "owner (Clay)" is `clayphi`; D:1397 ruling 3 omits the guard; D:970 leaves it open |
| C-008 | SPLIT | 60 | Both note `protected: false` (re-read: false); a ruleset needs no hook; an owner action, not designed |
| C-009 | OURS | 65 | FS equals OD1 on paper (LD:25-30 versus D:1152); CLAY gives the worker no level; mapping unwritten, cycle unobserved |
| C-010 | SPLIT | 60 | OB-CTX is precedent for session-scoped hooks; the guard blocks MERGE at all levels so cannot bind the orchestrator |
| X-001 | CLAY | 70 | "Not new code in the hook" is true; the whole job has unknowns, a deleted marker slot and no preflight |
| X-002 | OURS | 65 | The FAIL rows are verbatim-detail; the refusal matched (lines 471-472); line 17 still gates governed claims |
| X-003 | CLAY | 70 | LD:23 and LD:349: coordinator-started worker and `--pipeline none` carry no launch record by design |
| A-001 | SPLIT | 60 | Same user and HOME likely (F3 PASS for claim sessions); worker-start delivery unobserved; the pending-file receipt tests it |
| A-002 | SPLIT | 65 | Both lean on a trusted orchestrator; K22 and U42 stay open for both; the limit must be written as a graded risk |

#### Proposed resolution

What the rule in the unified design should say (concrete and testable):

1. The guard-less condition of DQ7 is the repository owner's open item G2, not a settled ruling. It stays marked "open, owner decision" and is never described as decided by ruling 3.
2. Before the second real orchestrated issue, every `worker-start` worker is bound at level `FS`: the first prompt carries `[sc-launch:v1:<nonce>]` (a line added to `templates/handoff-prompt.md`) and the orchestrator ran `orca_worktree.py pending --level full-submit` first.
3. A preflight runs before the first worker (jq present, hooks registered, the IR-4 checks the claim already does) and refuses to start a worker on failure. Test: a fixture with `jq` missing gives a refusal and no worker.
4. After the worker's first turn the orchestrator checks that `pending/<nonce>` is gone; if it remains, it stops the worker and escalates. Test: a fake `worker-start` whose prompt carries no marker leaves the file and triggers the stop.
5. Staging gate: the first bound worker runs on a throwaway issue and records (a) the pending-file receipt, (b) one `send` and one `ask` with no `--to` reaching the orchestrator (G2 facts 2 and 3), (c) a full `/sc:pr-submit --monitor 3` cycle at FS. Until it passes, DQ7 keeps "unbound" and K12 stays M / H.
6. Adopt Clay's controls whatever happens to the guard: `refuse(argv)` with a test per pattern, the `--match-head-commit` merge, audit AU1 to AU8. A test fails if the design describes the audit as covering a push with no pull request.
7. K22 and U42 stay open and graded; the guard is cited as precedent for session-scoped hooks, not as the orchestrator's guard.
8. Separate owner action, not part of this design: a ruleset or branch protection on `master` (needs admin; `ironbelly` has it). Record it as an open item with the live value `protected: false`.

### Variant 2 Advocate (CLAY), rebuttal (saw the OURS rebuttal)

##### Round 2, Advocate 2 (Variant 2 = CLAY), D05 launch guard for started workers

Written 2026-11-20, read-only. Short names as before: "the guard" is `launch-level-guard.sh`; "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in `/home/coder/.cache/ic-snap-20261120/master`. "G2" is `docs/designs/issue-pipeline-guard-g2.md` there. "FS" is the guard level that allows commit, push of a feature branch and PR creation. Numbers below follow the seven responses of `round-2-advocate-1.md`. I re-read the source for every citation I rely on. In this file the owner means the repository owner `ironbelly`, who wrote G2; "Clay" is the account `clayphi`.

Bottom line first. OURS wins the central question (the guard is required for orchestrator-started workers), staged behind a live probe. I could not find any CLAY benefit that is both evidenced and tied to the guard-less rule. CLAY keeps real, separable wins (controls that bind the orchestrator, a friction map, a fallback control, a limit on what the guard covers).

#### Response to the OURS rebuttal

1. **Collisions 1 and 2 and the session-id problem (their response 1). Conceded; my Round 1 point was wrong for level FS.**
   - Verified in the guard: the `.ok` file is read only when the level is `W` (`launch-level-guard.sh:270`), and the release that writes it runs only at `W` (the comment in the block at about `:341-361`: "only at worktree ..., never at full or full-submit"). The grid row for a typed `approved` or `/sc:implement` says "A, no write" at FS (LD grid row 34). G2 section 1 itself scopes both collisions to "the plan-writing worker" of the Plan B handoff. So facts 1 and 4 of G2 (session id, forged `.ok`) are not needed for an FS worker.
   - Collision 1 is also closed: rule 2 is in the guard (`:485-520`) and tests use real preamble shapes (`tests/hooks/test_launch_level_guard_worker.py:32,36,66,67`: `send --from term_1d62 --type heartbeat`, `ask --from ...`, `send --type worker_done`). `WORKER-CONTRACT.md:66` already writes "Messages carry no `--to` ... the launch-level guard blocks any `--to` from a bound worker". The contract was written for a bound worker. I withdraw "G2 collisions block binding".
   - What this changes: C-002 loses its strongest leg. What stays is only the unobserved delivery (G2 facts 2 and 3 live, FU-1 precondition f), which is a probe, not a block. The hook tests use synthetic envelopes, so "tests pass" is not "live".
2. **Citation slip. Conceded**, no effect.
3. **Fail-open on identity loss; fail-closed first prompt; pending-file receipt (their response 3). Mostly conceded.**
   - Verified in `:366-384`: a prompt with a strict marker sets governed, denies with LL-NOBIND when the session id is missing (`[ -n "$LL_SID" ] || ll_deny LL-NOBIND`), and denies unless a regular `sessions/<sid>` file exists after the rename. So a marker that reaches the hook cannot silently leave the worker unbound. The fail-open of LD (identity loss) applies only when no marker reached the hook.
   - Their receipt test (`pending/<nonce>` gone after the first turn) is sound for the case I worried about, a marker that never reaches the hook, and needs no session id. Two additions. (a) Pair it with the D:975 listing of `sessions/` so the receipt proves the right session. (b) A worker whose first prompt is denied never starts a turn, so the check must run on a timeout ("no heartbeat in N minutes, then read `pending/` and the screen"), not only "after the first turn". Their text leaves N unset.
   - Evidence in their favor that they did not use: the strict marker is accepted "anywhere" in the prompt (LD binding paragraph), so Orca's preamble in front of the brief does not break binding; and the claim path already delivers its marker with `orca agent launch ... --prompt` (`orca_worktree.py:1777-1778`), which produced bound sessions in the 442 runs. That narrows the unknown to "does `worker-start` deliver the task the same way". It does not remove it.
   - One failure mode to test: a prompt that begins `[sc-launch:` with a missing or used nonce is bound as `degraded`, which reads as level `W` (`:268-271`, B12). That worker is blocked from implement and commit and never reaches FS. It is loud (a block message), but it is not "bound at FS".
4. **U42 and K22 (their response 4). Conceded.** The guard blocks MERGE at every level (LD grid), so it cannot bind the orchestrator, and OB-CTX is precedent for session-scoped hooks, not an answer to K22. C-010 stays SPLIT.
5. **pr-submit friction at FS (their response 5). Partly conceded, partly countered with a new finding.**
   - Conceded: the `gh api` writes of replies and resolves sit in scripts (`reply-resolve-thread.sh:131,141`); the refs show the inline forms as "the contract of the script" (`refs/thread-reply.md:5-6`). The merge cycle is off by default (`--conflict-max-tier` default 0, `SKILL.md:240`; the one inline `git ... merge` is `refs/conflict-mechanical.md` step 4), and the design never passes the flag. My Round 1 reading of the whole cycle was too wide.
   - Countered: two pr-submit steps are model-typed inline `gh api --method POST ... issues/<N>/comments`, not script calls. The "single summary thread" (T-642, `summary_posted` in the contract, `SKILL.md:268`) and the fallback follow-up comment are specified at `refs/thread-reply.md:87-89` and `:93-100`; no script posts them (`retrigger-review.sh:56` posts only a re-trigger body). The guard classes any `gh api` with a method, a field, quotes or variables as GHWRITE at every level (`:554` accepts only plain tokens; the block text at `:67-69` names `gh pr comment` as the route instead). So at FS those two steps are blocked as written, and the worker must improvise with `gh pr comment` (class SUBMIT, allowed at FS). Small, fixable, and not seen by either paper; it is exactly the kind of mismatch a live run would find. Not a veto.
6. **Selective reading of the 442 evidence and R33 (their response 6). Conceded.** `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48`) gates the watcher's claim launches. It does not forbid binding a `worker-start` worker. I accept their reading: the gate's reasoning applies by analogy and supports staging, nothing more. I also checked #678 (open issue: a bare nested `claude "<prompt>"` runs a turn outside the limits). Its own text says the owner decided on 2026-11-19 that the risk is parked and no gate depends on it. I should not have counted OB-H1 item 8 against binding.
7. **Who is "the owner" in D:3 and D:1152 (their response 7). Conceded; this decides C-007.**
   - The analyst map (`H-design681-map.md`) shows ruling 3, the design approval, #655 (the orchestrator design issue) and #681 (the PR that merged it) all came from `clayphi`; `ironbelly` left nothing on them. D:1152 does say, in the OD1 cell itself, "The worker runs with no launch-level guard". But D:1397 (the ruling 3 row) says only "workers push and open pull requests, never merge or force-push", and D:970 and D:975 keep it open ("settled before the first real issue"; option B still named).
   - A literal point for CLAY that I do not rely on: G2:9 says "this worker" and "the flow" of the Plan B handoff, and #682 (Clay's PR that deleted the issue-pipeline package) removed that flow. But D:117 itself calls the DQ7 condition "the same condition" as G1, so Clay tied the two. The literal escape does not hold up.
   - Their claim that nothing of Clay's stops a direct push to `master`: **conceded in full.** I re-read D:801-828: the audit is `--pr <N>`; `refuse(argv)` binds the orchestrator's verbs (K22, D:1244); the merge gate acts on the orchestrator's merge (D:118). No CLAY control acts on a worker's `git push origin master`. The repository holds no push-time control of its own either: `.claude/settings.json` registers only two unrelated hooks.

#### Test of the nine-point resolution

Their file holds eight numbered points, not nine; I test those eight.

| # | Point | Clear and testable? | Comment |
|---|---|---|---|
| 1 | The guard-less condition is the owner's open G2 item, not ruling 3 | Clear | A doc check on the OD1 and DQ7 cells and the ruling 3 row. Needs the owner to confirm; that is already the owner order. |
| 2 | Before the second real orchestrated issue every worker is bound at FS | Partly | "Second real issue" is an event, not a switch. R33 used a constant (`GOVERNED_LEVELS_ALLOWED`); this needs the same, for example a refusal in the skill. It also clashes with G2:9 ("before any other issue") unless the first orchestrated issue is declared the one accepted test issue. Say so in the rule. |
| 3 | Preflight before the first worker, fixture with `jq` missing | Clear, but incomplete | `enforcement_preflight` sees only the claim process: its docstring says "The agent Orca starts may run with another one" (`orca_worktree.py:955-960`), and it is Linux only. `cmd_pending` runs no preflight today (their concession). The receipt in point 4 is the real check. |
| 4 | Receipt: `pending/<nonce>` gone, else stop and escalate | Clear | Add the `sessions/` listing and a timeout trigger (see response 3). A fake `worker-start` fixture is easy. |
| 5 | Staging gate on a throwaway issue: receipt, `send` and `ask` with no `--to`, a full `/sc:pr-submit --monitor 3` cycle at FS | Clear, three items short | Add (d) a scripted `git push origin master` on a throwaway repo (442 left the protected push pending because the agent declined, results lines 537 and 550); (e) the summary-thread step of response 5; (f) a bare `git push` and a compound `git add && git commit` (both refused at FS, LD grid rows 13 and 15). |
| 6 | Adopt `refuse(argv)`, the head-pinned merge, audit AU1 to AU8, with a test that the audit is not described as covering a push with no PR | Clear | Fully testable. This is the CLAY win and it needs no guard. |
| 7 | K22 and U42 stay open and graded | Clear | A doc check. |
| 8 | Ruleset on `master` is a separate owner action, recorded with the live value | Not testable | A live value is not a test, and "separate" leaves the strongest control without an owner, a trigger or a date. |

What the resolution still lacks, each a CLAY-side benefit with evidence:
- **A fallback if the probe fails.** If `worker-start` does not deliver the marker as a hook event, point 5 says only "DQ7 keeps unbound". "Required" then binds nothing. The fallback must be named: no real orchestrated issue until a server-side rule protects the branch, or the worker runs in a fork PR flow.
- **The guard's real coverage.** `:720` classes only a push to `master` or `main` as PROTECTED. The orchestrator's repo list carries `default_branch` and `release_head: integration` per repo (D:281-284), and IronClaude's own flow has an `integration` branch. A worker's `git push origin <sha>:integration`, or a push to a default branch named `develop`, is plain PUSH and allowed at FS. The resolution should say what covers those branches.
- **An L2 position.** The question names L2. `launch-level-pre-push.sh` exists on master, is installed only in the claim's launch step, and its refusal path is off (`IR7_REFUSE = False`, `orca_worktree.py:822`). It would catch the leaks the guard pins open (`bash ./push.sh`, LD:122) because it acts on git's own update stream. The resolution is silent on it.
- **What happens to real issues while the gate is open.** Point 2 allows one more unbound real issue. Point 5 keeps K12 at M / H meanwhile. The owner must be asked that in so many words.

#### Updated assessment of Variant 1

Stronger than I credited in Round 1. The collisions do not apply at FS; first-prompt binding fails closed when a marker arrives; binding leaves a testable receipt; rule 2 is already in the guard and tested with Orca's own preamble shapes; the worker contract already assumes a bound worker (`WORKER-CONTRACT.md:66`); the claim path's marker delivery is live-observed. They conceded the right things (X-001, X-003, C-002 in part, U-006) and corrected a CLAY error in a way I verified.

Still weak: the guard covers only `master` and `main`, a name filter and not a protection; L1 leaks are open and L2 is not part of the resolution; the preflight cannot see the worker's `HOME`; "bound at FS" has never been observed for a `worker-start` worker; the marker slot was deleted with `brief.py` (they conceded); one pr-submit step is blocked at FS as written.

#### New evidence

All read this round in the snapshot or the live repository. UNVERIFIED marks what I could not run.
1. `launch-level-guard.sh:720`: PROTECTED is only `master` or `main`. D:281-284: repos carry their own `default_branch` and `release_head`.
2. `refs/thread-reply.md:87-89` and `:93-100`: the summary thread and the fallback follow-up are model-typed `gh api --method POST .../issues/<N>/comments`. No script posts them. Guard `:67-69` and `:554`: such a call is GHWRITE at every level and the guard's remedy is `gh pr comment`. Read, not run live.
3. `WORKER-CONTRACT.md:66` and `tests/hooks/test_launch_level_guard_worker.py:32,36,66-67`: bound-worker verbs are already specified and hook-tested. Favors OURS.
4. `orca_worktree.py:955-960`: the preflight sees only the claim process's `HOME`, `PATH` and settings. `:822`: `IR7_REFUSE = False`, so L2 is advisory.
5. `launch-level-guard.sh:268-271` with B12: a loose marker with no usable nonce binds as `degraded`, which reads as `W`.
6. `#678` (bare nested `claude` runs outside the limits) is parked by the owner's 2026-11-19 decision and is not a gate (`gh issue view 678`). Favors OURS on C-003.
7. `.claude/settings.json` in the snapshot has no push-time or merge-time control. Favors OURS on C-005.
8. UNVERIFIED: whether `worker-start` delivers the task as a hook-visible first prompt; whether the orchestrator's host is Linux (the governed path needs it); whether a ruleset can be set by the login that runs the orchestrator.

#### Concessions

1. C-002: the "G2 collisions block binding" leg is gone (response 1). CLAY keeps only "unobserved".
2. Fail-closed first prompt and the receipt test are sound (response 3).
3. R33 and #678 do not support my reading of the 442 evidence beyond staging (response 6).
4. C-007: the repository owner's G2 sentence governs; Clay's ruling 3 does not undo it (response 7).
5. C-005: no CLAY control stops a worker pushing to `master` (response 7).
6. C-006 is narrower than I wrote (script path works; default cycle has no inline merge).
7. The guard at FS is the same policy as OD1 on paper (C-009). The mapping is unwritten, but the policy is not CLAY's to deny.
8. K12 is graded M / H by Clay himself, with only a prompt holding the worker back. I cannot show that binding costs more than that exposure.

#### Updated point positions

| Point | Superior (OURS, CLAY or SPLIT) | Confidence percent | One-line evidence |
|---|---|---|---|
| S-001 | SPLIT | 95 | Same six sections by the brief; no merit difference |
| S-002 | SPLIT | 95 | Same list counts; presentation only |
| C-001 | OURS | 72 | CLAY end state conceded; LD:23 describes today, G2:9 and K12 (M / H) state the rule |
| C-002 | SPLIT | 55 | OURS right that FS needs no `.ok` or session id (`:270`); CLAY right that `worker-start` binding is unobserved and the marker slot is gone |
| C-003 | SPLIT | 62 | PASS blocks real (442 results lines 530-549, 557); item 8 (#678) parked by owner; protected push never exercised |
| C-004 | SPLIT | 55 | R33 gates claim launches only; `--pipeline none` writes no record (LD:349); one fact, two readings |
| C-005 | OURS | 62 | No CLAY control acts on a worker push to `master` (D:801-828, K22); CLAY controls are real and adopted as HYBRID (U-006) |
| C-006 | CLAY | 55 | Summary thread and fallback comment are inline `gh api` POST (`refs/thread-reply.md:87-100`), GHWRITE at FS; reply and resolve are scripts, so narrow; fixable |
| C-007 | OURS | 78 | G2:9 owner text; "owner (Clay)" is `clayphi`; D:1397 ruling 3 omits the guard; D:970 leaves it open |
| C-008 | SPLIT | 62 | Both note `protected: false`; guard covers only `master` and `main` (`:720`), so a ruleset is the broader fix; neither designs it |
| C-009 | OURS | 68 | FS equals OD1 (LD:25-30 versus D:1152); CLAY gives the worker no level; mapping unwritten |
| C-010 | SPLIT | 60 | OB-CTX shows session-scoped hooks; the guard blocks MERGE at all levels and cannot bind the orchestrator |
| X-001 | CLAY | 65 | "Not new code in the hook" true, "whole job" false; OURS conceded (marker slot deleted, no `cmd_pending` preflight) |
| X-002 | OURS | 68 | OB-H2 FAIL rows are verbatim-detail checks (442 results lines 471-472); the refusal matched |
| X-003 | CLAY | 68 | LD:23 and LD:349: coordinator-started worker and `--pipeline none` carry no record; OURS conceded |
| A-001 | SPLIT | 62 | Same user and `HOME` likely (claim sessions bound live); preflight sees only the claim process (`orca_worktree.py:955-960`); the receipt tests it |
| A-002 | SPLIT | 65 | Both lean on a trusted orchestrator; K22 and U42 open for both; write the limit as a graded risk |

#### Separable CLAY benefits

Ranked by strength, each independent of whether the guard is required.
1. **Controls that bind the orchestrator (U-006): `refuse(argv)` with a failing test per "may never" pattern (D:767, D:1117), the head-pinned merge `--match-head-commit` with no `--auto`, `--admin` or `--delete-branch` (D:118), audit AU1 to AU8 after each merge (D:801-828).** None exists on master. They cover the orchestrator's own highest-power act, the merge, which the guard cannot cover (it has no level that merges, LD:23, LD:32). This is the strongest CLAY benefit. Adopt it whether or not the guard is required. Nothing in OURS competes with it.
2. **A fallback and a coverage statement.** If the staging probe fails, a server-side rule on the default and release branches is the only control left that also works against a deliberate worker (the guard is "not a sandbox", LD:32, and covers only `master` and `main`, `:720`). The design already reads `protected` per repo (D:118). Ask for a named fallback and list which branches each control covers.
3. **A friction map for FS** with the three added probe items of point 5 and the summary-thread fix (post it with `gh pr comment`, or let `retrigger-review.sh --body` carry it). It turns "friction is a cost" into a written mapping.
4. **Staging itself.** Not making the whole orchestrated flow wait on an unobserved binding is a sound sequencing rule, and OURS adopted it (their point 5). The rule becomes testable only if it is a code switch like R33's constant.

#### Any non-separable CLAY benefit

No. I looked for one that should override OURS on the central question and found none.
- "Binding is unproven" is real but separable: it is cured by a probe and a gate before the second real issue, which OURS now proposes.
- "The guard is leaky and not runtime-approved" (LD:6, LD:122; #442 and #685, the PR holding its runbook and results, are open) lowers the value of the guard. It does not give CLAY a control that does the same job: the CLAY controls act on the orchestrator or after a PR, not on a worker's push.
- "The risk is recorded and graded" (K12) is honest, but a graded exposure with only a prompt holding it back is not a benefit under the owner's weighting rule. Clay grades it M / H himself.
- "Cost of binding" is not shown. I found no evidence that FS blocks a step the OD1 worker cannot route around: the one clear mismatch (summary thread) has an allowed workaround.
So under the owner order, where CLAY shows no clear evidenced benefit tied to the contested rule, OURS wins C-001, C-007 and C-009, and the guard (or an equal mechanical control) is required for orchestrator-started workers, staged behind the live probe. CLAY's wins are adopted as a HYBRID next to it. The one open question I cannot close, and that the owner should answer, is point 2 of their resolution: whether one more real orchestrated issue may run unbound while the gate is open.

## Round 2.5: Invariant Probe (summary; full table in `invariant-probe.md`)

One independent fault-finder agent probed the emerging consensus across six categories and returned 38 findings: 13 ADDRESSED, 25 UNADDRESSED (7 HIGH, 12 MEDIUM, 6 LOW). HIGH UNADDRESSED items: INV-003 (binding is keyed on one session id; a new id runs unbound while the one-time receipt reads clean), INV-015 ("before the second real issue" is not enforceable, three issues can be in flight), INV-019 (guard refuses only `master` and `main`; `integration` or another default branch passes at FS), INV-027 (three gates disagree: guard status line, R33 constant, staging gate), INV-034 (a worker that writes a script and runs it, `bash ./push.sh`, passes every gate), INV-035 (so "binding at FS closes K12" holds only for plain pushes to `master` and `main`), INV-037 (K12 is not closed while `master` is unprotected and L2 is absent).

## Scoring Matrix

Winner and confidence are the mean of the two advocates' Round 2 positions. "Agreed" means both advocates gave the same label (SPLIT counts as a label).

| Diff Point | Winner | Confidence | Agreed | Evidence Summary |
|---|---|---|---|---|
| S-001 | SPLIT (tie) | 95% | yes | Same six sections by the brief; no merit difference |
| S-002 | SPLIT (tie) | 95% | yes | Same list counts; presentation only |
| C-001 | OURS | 71% | yes | Clay's advocate conceded the end state; LD:23 describes today, `issue-pipeline-guard-g2.md:9` and K12 (M / H) state the rule |
| C-002 | unresolved, lean CLAY | 55% | no (CLAY vs SPLIT) | Binding a `worker-start` worker is unobserved and the marker slot was deleted by PR 682; but at level FS no `.ok` or session id is needed (`launch-level-guard.sh:270`) |
| C-003 | SPLIT | 61% | yes | Live PASS blocks (442 results lines 530-549, 557) and open FAILs; OB-H2 FAIL rows are verbatim-detail checks |
| C-004 | SPLIT | 55% | yes | R33 gates only the claim launches; `--pipeline none` writes no record (LD:349) |
| C-005 | unresolved, lean OURS | 63% | no (SPLIT vs OURS) | Both agree no CLAY control acts on a worker push to `master` (audit is per `--pr`); both agree CLAY controls are adopted as HYBRID |
| C-006 | unresolved, lean CLAY (narrow) | 55% | no (SPLIT vs CLAY) | pr-submit's summary-thread and fallback comments are inline `gh api` POST, GHWRITE at FS (`refs/thread-reply.md:87-100`); reply and resolve are scripts |
| C-007 | OURS | 78% | yes | G2:9 "one first test issue ... before any other issue"; "owner (Clay)" is the account `clayphi` |
| C-008 | SPLIT | 61% | yes | Both note `protected: false`; guard covers only `master` and `main` (`:720`); a ruleset is the broader fix, owned by nobody yet |
| C-009 | OURS | 67% | yes | FS equals OD1 (LD:25-30 versus D:1152); mapping unwritten |
| C-010 | SPLIT | 60% | yes | OB-CTX is precedent for session-scoped hooks; guard blocks MERGE at all levels so cannot bind the orchestrator |
| X-001 | CLAY | 67% | yes | "One marker line" true of the hook, false of the whole job; OURS conceded |
| X-002 | OURS | 67% | yes | OB-H2 FAIL rows are verbatim-detail checks; refusal matched (lines 471-472) |
| X-003 | CLAY | 69% | yes | LD:23 and LD:349: coordinator-started worker and `--pipeline none` carry no record; OURS conceded |
| A-001 | SPLIT (QUALIFY) | 61% | yes | Same user and HOME likely; worker-start delivery unobserved; preflight sees only the claim process |
| A-002 | SPLIT (QUALIFY) | 65% | yes | Both lean on a trusted orchestrator; K22 and U42 open |

## Convergence Assessment

- Points resolved: 14 of 17
- Alignment: 82.4 percent
- Threshold: 80 percent
- Taxonomy gate: passed (L1: S-001, S-002; L2: A-002, C-008; L3: the rest all addressed)
- Invariant gate: FAILED. 7 HIGH-severity UNADDRESSED invariants (INV-003, INV-015, INV-019, INV-027, INV-034, INV-035, INV-037) block convergence regardless of the diff-point score.
- Status: BLOCKED_BY_INVARIANTS. Depth is standard, so Round 3 (deep only) does not run. Per the unattended default the pipeline force-selects by score and records the blocked status; the 7 items are carried into the return contract and into the verdict's Unverified and Implications sections.
- Unresolved diff points: C-002, C-005, C-006 (each unresolved only by label; the advocates agree on the facts and on the HYBRID shape)
- MEDIUM UNADDRESSED invariants (12) are warnings and do not block: INV-001, 002, 009, 011, 012, 013, 014, 016, 021, 023, 029, 036.
