# Round 1, Advocate 1 (Variant 1 = OURS), D05 launch guard for started workers

Persona: analyzer. Written 2026-11-20. Short names as in the papers: "the guard" is `launch-level-guard.sh` (L1), "L2" is `launch-level-pre-push.sh`, "D:nnn" is a line of `docs/designs/orchestrator.md` and "LD:nnn" a line of `docs/designs/sc-issue-launch-level-hook.md`, both in the snapshot `/home/coder/.cache/ic-snap-20261120/master`.

## Position summary

An orchestrator-started worker holds push rights on an unprotected `master` and is held back by prose alone (K12, D:1234), so the guard (or an equal mechanical control) should be required before the first real issue, in a staged way: bind first, prove binding live, then enable. Clay's orchestrator-side controls (`refuse`, the head-pinned merge gate, the audit) are real gains that OURS lacks and should be adopted next to the guard, not instead of it.

## Steelman of Variant 2

The strongest CLAY case is this. The guard was built for sessions the claim script launches, and its own text says a coordinator-started worker "is not launched by the claim script, so this guard does not govern it" (LD:23). Requiring it therefore means building something new, not switching something on. The two things needed to build it are unproven: G2 facts 1 to 4 are all UNVERIFIED (`docs/designs/issue-pipeline-guard-g2.md:40-43`) and whether `worker-start` delivers a marker-bearing first prompt was never tried. The guard's own live proof is unfinished: issue 442 (the live observations) and PR 685 (its runbook and results) are both open, OB-H1 item 8 is a FAIL (a bare `claude "<prompt>"` runs a turn outside the limits, issue 678), and the protected-push row was never exercised (results lines 537, 550). The guard says it is "a same-user guardrail, not a sandbox" and leaves pinned leaks (`bash ./push.sh`, LD:32, LD:122). Making a half-proven, leaky layer a hard prerequisite would put the whole orchestrated flow behind an unfinished gate and give false assurance. Meanwhile Clay's design adds controls that exist nowhere on master: a closed "may never" list with a failing test per pattern (D:1117), a merge pinned to the head commit (`--match-head-commit`, DQ8 D:118), and an eight-check audit after each merge (D:809-818). The exposure is graded M / H, written down and sent to an owner decision (K12, OD1), not hidden. What CLAY gets right: it does not claim protection nobody has seen, it puts controls where the irreversible act happens (the merge), and it states its own risk.

## Strengths claimed

1. **The exposure is on the record and the live value is unchanged.** K12 (D:1234) says only "the worker's written prompt (never merge, never force-push) holds it back from pushing" to `master`. `gh api repos/IronbellyOrg/IronClaude/branches/master -q .protected` printed `false` today (re-run in this round). A prompt is a request, not a control.
2. **The one-issue acceptance does not stretch to a standing rule.** G2 says: "For the one first test issue the owner accepted that this worker runs without the launch-level guard (G1) ... Before any other issue runs through the flow, the worker must be bound to the guard (G2)" (`issue-pipeline-guard-g2.md:9`, read this round). DQ7 (D:117) cites that same G1 as precedent for a standing rule. The cited source says the opposite of what it is used for.
3. **Clay's own design keeps the door open.** D:970 (row 5d) leaves "the guard-less condition of DQ7" open until "settled before the first real issue"; D:975 and D:1002 keep the #442 checks and guard rule 2 "if the owner binds orchestrated workers (OD1, option B)". The code for option B survives on master: `cmd_pending` (`orca_worktree.py:1515`) writes the pending record for "a coordinator-started worker (G2)", and the deleted worker-brief builder had an optional `nonce` that adds the `[sc-launch:v1:<nonce>]` line (`git show 01e7a9e23^:src/superclaude/cli/issue_pipeline/brief.py` lines 52-74, verified).
4. **FS is Clay's own OD1 policy, enforced mechanically.** OD1 (D:1152): the worker "pushes its own feature branch and opens its pull request ... never merges and never force pushes". The FS row allows "commit, push a feature branch, open a PR" (LD:25-30) and blocks PUSHFORM, PROTECTED and MERGE at every level (LD:91-98, LD:113-115). Nothing new to design; a mapping to write down.
5. **Clay's detective control cannot see the worst case.** The audit is per pull request (`--pr <N>`, AU1 to AU8, D:809-818). A worker that pushes to `master` with no pull request produces nothing to audit. The merge gate guards the orchestrator's merge, not the worker's push. Only a push-time control (guard, L2 or GitHub protection) covers it.
6. **Live PASS evidence exists for the exact blocks that matter.** `observation-results.md`: implement blocked (line 530), four commit blocks (B twice at 531, C at 535, D at 536), bare `approved` does not unlock (532), `git merge` refused (549), OB-CTX PASS (line 557) telling governed from ordinary and human sessions.
7. **OB-H2's FAIL is thin.** Within OB-H2 (lines 349-477) the only FAIL rows are the two preflight checks, and each says "the FAIL comes from the verbatim-detail check only; the refusal itself matched ... W-ENFORCEMENT-ABSENT" (lines 471-472). CLAY lists it as bare evidence the guard is unproven.
8. **The gate is already designed to wait for proof.** R33 (`GOVERNED_LEVELS_ALLOWED = False`, requirements.md line 59, `launch.py:48`) means no governed launch before OB-H1, OB-H2, OB-H3 pass. "Require the guard for orchestrator workers" can be sequenced behind the same gate, so CLAY's "do not wait on an unfinished gate" is answered by staging, not by dropping the rule.
9. **WC-9 is a written rule changed by a written rule.** WC-9 (`WORKER-CONTRACT.md:41`) says every outward action is off for a worker and "no brief can turn it on". ADD1 (D:135) overrides that with a contract section. Reversing a text rule with a text rule adds no layer; the guard would be the second layer.

## Weaknesses identified in Variant 2

1. **Its scope argument describes the status quo, not a benefit.** LD:23 says the guard does not govern this worker today. That is the premise of the question, not an answer to it. Every DQ7 "evidence" cell (LD:77, `launch-level-guard.sh:1-8`, g2.md:5-8) shows the worker is unbound, not that it should be.
2. **Its "G1 accepted" support is for one issue only** (strength 2). D:117 says "the same condition". The condition was accepted once, with a stated deadline (g2.md:9).
3. **Its controls miss the push to `master`** (strength 5). `refuse(argv)` binds the orchestrator's verbs; K22 (D:1244) concedes it "binds the verbs, not a command the model types itself"; the worker types its own commands. The merge gate and the audit fire at or after a pull request. Fact 7 of the CLAY paper is true and still silent on the one path K12 names.
4. **"Unfinished gate" overstates.** The unfinished items (OB-H1 item 8, OB-H2 verbatim checks, OB-H3, protected push) are about launch-time binding and one prompt-decline; the live observations that the grid blocks commit, merge and implement are PASS (strength 6). The protected-push row stayed pending "and the cause is the prompt, not the guard" (line 550).
5. **Fact 3 (nothing real is governed today) is true and cuts against CLAY.** If both lines run an unguarded worker today, that is the exposure to close before the first real issue (D:970), not a reason to bless it. R33 exists because the owner will not call a launch governed until proven.
6. **Its guard friction is real but pre-solved in the observed run.** The `reply-resolve-thread.sh` calls (`gh api --method POST` line 131, `gh api graphql` line 141, verified) are scripts, which the guard pins as allowed (LD:122). The one observed blocked compound command was re-issued in split form and ran (line 540). A cost worth a fixture, not a blocker.
7. **It leaves K22 and U42 open and says "a hook" might fix them.** The session-scoped hook mechanism already exists in the guard (marker plus pending record), so U42's "can a hook run only on one session" has a working precedent on master. The paper lists this as a risk instead of reading the code.
8. **Scale cuts the other way.** Up to three issues in flight (D:698-718) each with a worker holding push rights multiplies the unprotected-`master` exposure, per CLAY's own paper.

## Concessions

1. **X-001, binding is unproven.** My "one marker line plus one `pending` call" (Mechanism 2) is cheap in code (verified) and unverified in effect: G2 facts 1 to 4 and FU-1 precondition f are UNVERIFIED. The honest wording is "cheap to attempt, not yet shown to bind a `worker-start` worker".
2. **The guard leaks and is not a sandbox** (LD:32, LD:122); a bare `claude "<prompt>"` runs outside it (issue 678, open). It reduces honest drift. It does nothing against deliberate evasion (TH3).
3. **The guard is not runtime-approved** (LD:6, LD:17); 442 and PR 685 are still OPEN (re-read this round with `gh`).
4. **Owner-naming ambiguity.** D:3 calls Clay "the owner (Clay)", and D:1152 says OD1 was decided by "ruling 3". I could not verify (UNVERIFIED) that ruling 3 is the repository owner's. If it is Clay's alone, it does not override the repo owner's G2 sentence; if it is the repo owner's, strength 2 weakens. This must be settled by the owner, not by me.
5. **CLAY's orchestrator controls are real gains** (U-006): `refuse(argv)` with a failing test per pattern, `--match-head-commit`, AU1 to AU8, none on master. They should be adopted whatever happens to the guard.
6. **My U42/K22 claim is half true.** The session-scoped mechanism exists, but the guard has no level that allows a merge ("no level authorizes a merge", LD:32), so it cannot be bound to the orchestrator itself without a new level and rule set. It answers the worker half only.
7. **FS-to-OD1 mapping is not written** and the `/sc:pr-submit --monitor 3` cycle at FS was not observed (a plain push and `gh pr create` at FS did run, PR 654, lines 508-514).

## Shared assumptions

- **A-001 (the user-level hooks apply to the session `worker-start` creates): QUALIFY.** True when the worker is a Claude Code session on the same host and `HOME` as the registered hooks, and the OB-H2 evidence command F3 already reads the hook's `HOME` and `CLAUDE_CONFIG_DIR` for claim-launched sessions (results lines 349-477). Nobody has run that probe for a `worker-start` session (G2 fact 1 UNVERIFIED). The test D:975 already plans (`ls ~/.claude/state/launch-level/sessions/` before and after the first worker) is the right probe; it should also record the hook's `HOME` and whether `UserPromptSubmit` fires. If hooks do not fire, a "required guard" binds nothing, so the requirement must be coupled to the IR-4 preflight (W-ENFORCEMENT-ABSENT refusal, results lines 471-472), which refuses rather than launches.
- **A-002 (the orchestrator is a trusted, ordinary session): QUALIFY.** Acceptable only because its outward verbs go through `refuse(argv)` and its merges through the head-pinned gate, and because the person opens it. It is the highest-power session (it merges). K22 admits typed commands escape `refuse`. The guard cannot cover it today (no level allows a merge). So "trusted" holds as a stated limit with the audit as backstop, not as a proven property; the guard requirement for workers does not depend on it.

## Point positions

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
