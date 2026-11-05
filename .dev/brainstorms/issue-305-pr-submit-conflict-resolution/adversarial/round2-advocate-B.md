# Round 2: Rebuttal from the Variant B advocate (`variant-2-sonnet-refactorer.md`)

Persona: refactorer (technical debt, simplification, minimal-risk transformation). Citation forms: `A:NN` / `B:NN` / `C:NN` are lines of the variant files; `R1-A:NN` / `R1-C:NN` / `R2-A:NN` are lines of the round files; `DA:NN` is `diff-analysis.md`. Repo lines were re-read in this session against the worktree at `119622e3` on 2026-11-04. Where I rely on a reading I did not execute, I say so.

## 0. Headline

Round 2 changes my position on one coupled question and leaves most of the rest standing.

A's N1 is right and I verified it: **where a conflict is acted on and whether reviewers are re-triggered are one decision, not two.** So the only coherent pairs are {act early, re-trigger} (A) and {act late, no re-trigger} (B). I also accept A's N3 (J-66 is decided per kind of change) and N4 (reusing `evaluate_push_decision` at the late hook would repeat issue #305).

My position on A's tier split is **ACCEPT AS THE END-STATE DESIGN, WITH SIX MODIFICATIONS**. The short version:

- Tier 1 (deterministic regenerate) follows B and ships first. It now also acts when the review phase ended in `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` (I concede B-W4 and OQ-4 for this tier).
- Tier 2 (model judgment) follows A's early path, but it is **built in P2, dark**, not in the first release. A has already conceded the default `--conflict-max-tier 1` (R1-A concession 5), so nothing is lost by sequencing the code to match.
- Tier 3 halts at the end of Wave 0 in the shape that `SKILL.md:268` already uses, not at `C-initial`.
- One sibling push gate serves both tiers. A's "reuse `evaluate_push_decision` for Tier 2" collides with the S5a re-trigger gate (new evidence NE1).

## 1. Steelman before critique

### 1.1 A's tier split (A-prime), strongest form

A-prime is the first proposal in this debate that explains why the skill's two existing push patterns exist. The fix cycle (S4, S6, RESOLVING, S5a, S5) is the path for model-authored change that bots must re-review. The CI push (`SKILL.md:277`: "do not call `retrigger-review.sh`, reply, or resolve; re-poll CI") is the path for change whose check is "re-run the checks". A-prime assigns each kind of conflict push to the pattern that already fits it, and invents no third pattern (R2-A:15).

Its evidence holds up when I check it:

- **N1.** `expected_head = payload.get("head_sha") if pushed_sha is None else pushed_sha` (`SKILL.md:103`). The classifier rejects the latest review when any of its commits differs from the head (`classifier.py:266`). "A push does NOT auto-trigger a re-review by either bot" (`SKILL.md:274`; `refs/review-retrigger.md:1-6`). I agree with A's reading. I did not execute the classifier on a merged head.
- **N2.** `rebuild_state` adds every `push_completed` to `push_count` (`run_log.py:238-239`), and the round counter ticks only on `round_incremented` (`run_log.py:198-199`).
- **N3.** J-66 reads "gets whatever review path the project's protocol defines for authored changes" (`.dev/research/issue-305-conflict-resolution/03-roi-scored-list.md:94`). A quoted it accurately. My R1 use of J-66 was loose, and so was A's.
- **N4.** Predicate 4 is `round_counter < max_rounds` (`fsm.py:194`). A review that ends `clean` at `round_counter == max_rounds` reaches Wave 8 with no budget (`refs/ci-poll.md:27`). A reused gate would refuse a `uv.lock` regenerate there. That is #305's own failure.
- **N5.** `test_transition_v11_edges` pins every V1.1 edge row by row (`tests/pr_submit/test_auggie_fallback.py:353-379`). So my R3 ("transition() silently ignores unknown edges", B:106) is a real risk that the repo already contains for added edges.
- **N6.** I ran `gh repo view IronbellyOrg/IronClaude --json` with the fork named explicitly. The field list contains `mergeCommitAllowed`, `rebaseMergeAllowed` and `squashMergeAllowed`. Readability without admin scope and the behaviour of a rebase-only repository remain unverified.

A also did the thing an advocate rarely does: it moved on evidence (R2-A:7-15) and conceded eleven items to B and C.

### 1.2 C, strongest form

C's defense is the most honest in the debate, and its scaffolding transfers: the likelihood and impact columns in the risk register (C:157-174), the "deliberately no test" list (C:153-155), the `== 41` sweep (C:161; pins at `tests/pr_submit/test_run_log.py:168` and `test_codex_reviews.py:441`), `BLOCKED` as an explicit Tier 0 row (C:55), and per-tier call ceilings (C:127). C's `merge_push_count <= 1` (C:112) equals the value I now propose for `SYNC_CAP` in P1.

## 2. Response to every criticism of Variant B

Verdict key: **Concede** (I change B), **Partial** (part conceded), **Counter** (evidence against).

### 2.1 From `round1-advocate-A.md`

| # | Criticism | Verdict | Response and evidence |
|---|---|---|---|
| A-B1 | The second push gate must track INV-016 forever, and no test links `evaluate_sync_decision` to `evaluate_push_decision` (R1-A:57). | **Partial** | The gap is real: B has a disjointness test for the parent checks (U-011) but none for the decision gates. Fix with no edit to `fsm.py`: a cross-gate property test asserting that wherever the sibling authorizes, the original agrees on the shared predicates (ordinal, validated, no-human) once its budget predicate and `applied_edits` are set true. A-prime also now uses the sibling for Tier 1 (R2-A:34), so the "two gates" cost is shared, not B's alone. |
| A-B2 | `SYNC_CAP` is a second budget outside `--max-rounds` (R1-A:58). | **Partial** | Counter: INV-016's design is machine-checked predicates recorded write-ahead (`fsm.py:173-204`), not hook structure. A's own R-11 now accepts `<= 1` as a hard bound (R2-A:37). Concede the value: the number 2 exists only for the P3 late re-sync (B:276). With P3 deferred, `SYNC_CAP = 1` in P1, equal to C's bound (C:112). |
| A-B3 | Model-authored Tier 2 code reaches the PR with no bot review (K8, B:538) (R1-A:59). | **Concede for Tier 2** | Accepted via N3. Tier 2 takes the re-review path (A's early path, P2). **Counter for Tier 1:** the review path the protocol defines for a CI-class push is "re-run the checks" (`SKILL.md:277`), and `uv lock --check` is added to VG-1 (B:387). |
| A-B4 | A known conflict stays unresolved after `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` because Wave 8a is report-only there (B:261, OQ-4 B:567) (R1-A:60; R2-A:94 "stands"). | **Concede for Tier 1** | `should_arm_ci_wait` arms on all four outcomes including those two (`ci.py:49-57`). `ci_wait_autofix` (`ci.py:60-66`) restricts auto-fix of CI *findings*, which are model-authored. A deterministic regenerate that consumes no round is a different class, and B:567 already said "acting is defensible". Change B:261: Tier 1 acts on all four armed outcomes, status preserved exactly as for a CI human-gate (B:264). Tier 2 stays report-only on the two wait-only outcomes (no review, no budget). Under the split Tier 2 is acted on at `C-initial` before rounds are spent, so the residual is only a base that moves late. |
| A-B5 | The create-path rebase is kept as "harmless" (B:622) (R1-A:61). | **Concede (R1)** | Already conceded. I also accept A's L1+ scoping (R2-A:31): `SKILL.md:220` gates the STOP on `--monitor >= 1`, and L0 pins stay byte-identical (`test_static_grep.py:649-657`). |
| A-B6 | Tier 0 is not cheap: fetch, `merge-tree`, `gh pr view` and a capability probe at Wave 0 end and again at Wave 8a (R1-A:62). | **Concede (R1) and adopt A's ordering** | Adopt A's rule: read GitHub `mergeable` / `mergeStateStatus` first; run the local probe only on `CONFLICTING` or persistent `UNKNOWN` (A:198-203). That makes a normal PR cost one call. This flips C-007 / X-026 to A (B:242 made local `merge-tree` the truth; the cost argument defeats it). |
| A-B7 | L1 "proposes 'resolve these? y/n'", an interactive prompt in a skill that "has no override prompt" (R9, B:112) (R1-A:63). | **Counter** | R9 rejects a *user-override channel* (R-19, R-20), not the L1 proposal. The skill already has the L1 proposal: `PROPOSE_PROMPT = "fix these? y/n"` (`fsm.py:42`, emitted at `fsm.py:1093`), `PROPOSED` (`refs/state-machine.md:45`), and `SKILL.md:272` ("At L1: PROPOSE 'fix these? y/n' and apply NO edits"). B:250 is the same shape. I concede the wording and will say "PROPOSE", not "prompt". |
| A-B8 | OQ-11: B is unsure that `S4'_HALT_BEFORE_PUSH` is reachable from Wave 8 (B:574), so it might report a status the FSM never entered (R1-A:64). | **Concede and close** | The caller sets S4' when the decision is unauthorized and `ordinal < 3` (`fsm.py:1118-1121`); `transition()` never does. `sync_fail_state` with `s1_ordinal` false should return S4' set by the caller in exactly that way, which is also what A's R-2 says (R2-A:28). No new edge. |
| A-B9 | Parallel output contract: `sync_tier`, `sync_outcome`, `sync_push_count`, plus fold branches, so `push_count` no longer counts every landed push (R1-A:65). | **Partial** | N2 shows `push_count` already counts every landed push, including CI pushes that spend no round, so my S1/S3 wording "meaning preserved" overstated. But four prose sites state a *bound*: `SKILL.md:239` ("== `max_rounds` at most"), `SKILL.md:275` and `refs/loop-guard.md:47` (`<= max_rounds + 1`), `refs/auggie-fallback.md:43`, and the boundary is pinned at `test_auggie_fallback.py:301`. A Tier 1 sync adds a push no round paid for. Counting it would make those bounds false. Resolution in section 3 (M6): Tier 1 sync is excluded by `kind`; Tier 2 merge is counted because it spends a round. Every bound stays true with no prose edit. |
| A-S1 | A conflict push is a push that spent a round, so no new counters (R1-A:35). | **Partial** | Same as A-B9. True for the Tier 2 half. |
| A-S4 | Act early resolves the conflict before rounds run out (R1-A:41). | **Concede for Tier 2/3** | Adopted in the split. For Tier 1 the late site is safe because it no longer depends on budget (A-B4). |
| A-S5 | `REGEN_RECIPES` splits one rule across core and ref; `MechanicalRule` is the better extension point (R1-A:43). | **Concede** | Adopt `MechanicalRule(pattern, kind, sources, regenerate, check)` in the core with one row (`uv.lock`) and A's test that every rule program is in `allowed-tools` (A:407; `SKILL.md:4`). |
| A-S6 | One routing function with an exhaustive table test beats B's routing spread over four places (R1-A:45). | **Concede** | Adopt A's `conflict_action(...)` as the single pure router. NE6 shows the split makes this mandatory, not optional. |
| A-S8 | Three scripts triple the install surface; A adds zero (R1-A:49). | **Partial** | See C-B4. |

### 2.2 From `round1-advocate-C.md`

| # | Criticism | Verdict | Response and evidence |
|---|---|---|---|
| C-B1 | Reviewers never see the merge, the largest safety hole (X-003) (R1-C:64). | **Concede for Tier 2** | Same as A-B3. |
| C-B2 | Act-late pays the full review cost on a head the merge will replace (K9) (R1-C:65). | **Concede for Tier 2/3; counter for Tier 1** | Tier 2 and 3 move earlier. A lockfile regenerate does not invalidate findings about source files, so no review is wasted by acting late on Tier 1. |
| C-B3 | B undercounts Tier 0 cost (X-040) (R1-C:66). | **Concede (R1)** | Fixed by adopting A's ordering (A-B6). |
| C-B4 | Three scripts triple the install-and-pin surface (R1-C:67). | **Partial** | P1 ships two scripts. `probe-merge.sh` becomes a thin emitter (fetch, `foreign_op`, `index_clean`, raw `-z` listing); stage parsing moves to the core as `parse_stage_records`, tested against a captured fixture (R1-B concession 5; U-005). `finish-merge.sh` stays: A conceded that its subset check is the stronger gate and the only one real-repo tests can run (R1-A concession 7). `collect-conflict-evidence.sh` is Tier-2-only, so it ships with P2 and may become inline calls, as A argues (A:86). |
| C-B5 | The headline case (Tier 2) ships dark (R1-C:68). | **Concede as a cost** | The seed's L3 text-conflict criterion is met only after P2 flips the default. This is the price of the gate at B:522. It is smaller now: A has also moved to default 1, and the P2 design is fixed in this spec, so P2 is implementation, not design. |
| C-B6 | The create-path settlement keeps an unsound premise (X-013) (R1-C:69). | **Concede (R1)** | Same as A-B5. |

### 2.3 From `round2-advocate-A.md`

| # | Criticism | Verdict | Response and evidence |
|---|---|---|---|
| R2-B1 | B's planned Tier 2 re-trigger follow-up "converges on A's path" (R2-A:93). | **Concede** | A re-trigger after Wave 8a re-opens S5a, S5 and INV-R1 (the `RESOLVING -> S5A_RETRIGGER_REVIEW -> S5_AWAITING_REREVIEW` edges in `transition()`). That needs A's edge or an equivalent. I stop proposing a late Tier 2 re-trigger. |
| R2-B2 | B-W4 stands (R2-A:94). | **Concede for Tier 1** | See A-B4. |
| R2-B3 | Three scripts where one earns its place; `SYNC_CAP` as a counter where hook structure bounds pushes (R2-A:95). | **Partial** | See C-B4 and A-B2. |
| R2-B4 | B's and C's separate counters are weaker than claimed; they *exclude* a kind of push from `push_count` (R2-A:67-70). | **Partial** | See A-B9. The mechanics point is conceded. The conclusion is not: excluding a no-round push keeps four documented bounds true; including it falsifies them. |
| R2-B5 | B's own placement table shows coupling (B:205), so B understood N1 first (R2-A:19). | **Accepted, thank you** | It is why the Tier 1 half of the split is B's. |
| R2-B6 | N4: any late Tier 1 path needs B's predicates (R2-A:82). | **Agreed** | It supports B's gate for Tier 1. It also shows B:261 was wrong to go report-only (A-B4). |
| R2-B7 | A's R-2: L2 resolves only at `C-ci`, then stops (R2-A:28). | **Agreed** | Matches B:254: a worktree left mid-merge would break a later fix cycle's `git commit --only`. |

## 3. Response to A's proposed tier split

**Verdict: ACCEPT as the end-state design; MODIFY in six places.** What I accept, with evidence, is the whole premise: N1, N3, N4 and N5 verified above. What I do not accept is building both halves in the first release, running Tier 2 through a different push gate, or putting Tier 3 and late Tier 2 where A-prime currently puts them.

### M1. Sequence the code: P1 is Tier 1 only; the FSM edge lands in P2

- **P0** read-only detect and report (B:520).
- **P1** Tier 1 (B's late path, sibling gate, `finish-merge.sh`), Tier 3 Wave-0 halt, and the two refs split by tier (U-003). Touches no `transition()` row, no `evaluate_push_decision`, no `push_parent_ok`, no S5a text. Touches `run_log.py` (fold) and `recovery.py` (key tuple) about 15 lines (B:96).
- **P2** Tier 2 early path: the `(S2_CLASSIFY, "conflicting")` edge with its row assertion in the `test_auggie_fallback.py:353-379` pattern, the S5a clause change (M5), and `conflict-intent.md`. Dark behind `--conflict-max-tier` default 1.

Reason: A conceded the default of 1 (R2-A:41), so the Tier 2 code would be unreachable at release anyway. Landing the part of the FSM with the largest regression surface (fsm.py:801-802 "unknown edge: stay put", the C6 row tests) only when it can be exercised by a real run is the lowest-risk order. The spec fixes the P2 design now, so no design debt is deferred.

### M2. Tier 1 acts on all four armed outcomes

Evidence: `ci.py:49-57`, `ci.py:60-66`, B:567 (see A-B4). Status is preserved exactly as for a CI human-gate. `SYNC_CAP = 1`.

### M3. Tier 3 halts at the end of Wave 0, not at `C-initial`

`SKILL.md:268` already defines a pre-Wave-1 halt: `terminal_halted` with a reason, "appended to the run-log when one exists", plus operator text. Tier 3 at L3 can use that shape (new reason `conflict_tier3`). It needs no run-log and no armed FSM. A's route for Tier 3 is the `needs_human_decision` pre-gate at the top of `transition()`, which requires arming first. This shrinks `C-initial` to one job: the L3 Tier 2 cycle. At L1 and L2 Tier 3 is reported and the run continues to review (A's R1 concession 9 and R2 R-2).

### M4. Each tier gets one acting site per ordinal

| Tier | L1 | L2 | L3 |
|---|---|---|---|
| 0 | report only | same | same |
| 1 | report; PROPOSE | resolve at Wave 8a, stop with merge uncommitted, caller sets S4' | resolve and push at Wave 8a |
| 2 | report; PROPOSE | resolve at Wave 8a, stop uncommitted (A-prime R-2) | act at `C-initial`; a conflict first seen at `C-ci` halts `late_conflict` (B:276) |
| 3 | report, continue | report, continue | Wave 0 halt (M3) |

Why Tier 2 at `C-ci` halts: that hook is reached from `S2_CLASSIFY` after a merged `clean`/`REPORT_ONLY`, or from a preserved terminal where the FSM "never transitions out of the terminal state" (`refs/state-machine.md` section 5.2c). The `(S2_CLASSIFY, "conflicting")` edge exists in the first case and not in the second. Allowing the cycle only in one of them creates two behaviours for one input. Halting uniformly is the minimal-risk rule, and it is B's existing P3 rule.

### M5. One sibling push gate for both tiers, and an explicit S5a clause

A's R-8 holds two statements that collide:

- Tier 2 reuses `evaluate_push_decision(..., applied_edits = resolved path count)` (A:337, kept in R2-A:34).
- The Output Contract field `applied_edits` is "Grounded edits applied this run (INV-016 predicate 5)" (`SKILL.md:242`), so resolved paths "must not be folded into it" (R2-A:34).

But the S5a re-trigger is gated on that same variable: `if result.applied_edits > 0` (`fsm.py:1135-1137`; "ONLY when this cycle applied edits (`applied_edits > 0`)" in `SKILL.md:274`). If the count is not folded, the merge push does not re-trigger, and the run reproduces the defect that N1 attributes to C. If it is folded, the audit record is wrong (B:108, R5; `push_fail_state` also maps p5 false to `TERMINAL_CLEAN`, `fsm.py:206-221`).

So A-prime's "no new code" for the Tier 2 re-trigger (A:247, R2-A:29) is not accurate. Resolution:

- Extend `evaluate_sync_decision` to cover both tiers. Predicates: ordinal >= 3, validated, tier allowed and no halt, under cap. For Tier 2 "under cap" also includes `round_counter < max_rounds`; for Tier 1 it does not (N4). No `applied_edits` anywhere in the merge path.
- Widen the S5a trigger by one additive clause: `applied_edits > 0 or kind == "merge"`, in `fsm.py:1137` and `SKILL.md:274`. I found no test that pins that sentence by the strings I searched; the nearby pins at `test_static_grep.py:689` and `:750` cover the parent-check sentences, which this change leaves alone.

This removes the second push gate that A-prime would otherwise carry, and it keeps INV-016's predicate 5 truthful.

### M6. Counting rule

`push_count` keeps counting the pushes that spend a round (fix pushes and Tier 2 merge pushes, tagged `kind`). Tier 1 `kind: "sync"` pushes go to `sync_push_count` (one conditional in the `run_log.py` fold, B:96). The recovered `push_completed` must carry `kind` through the key tuple at `recovery.py:98-106`, or the fold would count a recovered sync push as a fix push; B already specifies this (B:96, :301).

## 4. Updated assessment of A and C

**Variant A.** A's R2 is the strongest document in the debate: its new evidence (N1, N3, N4, N5) held up when I re-read the code, and it conceded whitespace, the operator-recovery text, AD-7 scope, the default tier and L1/L2 timing. What remains open against A:

1. The `applied_edits` / S5a collision (NE1), and the "no new code" claim.
2. A-prime's footprint is a union (one edge, one sibling gate, two resume rules, push-kind in recovery). M1 and M5 reduce it; A's R-9 admits the cost.
3. A's Tier 3 route needs an armed FSM when a Wave 0 halt exists (M3).
4. `C-initial` re-triggers every configured reviewer because no presence is known yet (A:247). Existing code limits the damage: a Codex with no activity becomes absent once Augment settles (`reviewers.py` `codex_wait_outcome`). I am not pressing R1's WA3 further. I did not execute this path.

**Variant C.** Architecture unchanged: X-034, X-035, X-037, X-023, X-012 and X-008 stand, and A's N1(b) adds a seventh High-class defect (an early merge push with no re-trigger cannot complete its first review wait; `classifier.py:266` rejects a latest review whose commit is not the head). I verified the line, not the full run. C's value is the QA scaffolding in section 1.2, which I adopt, and `merge_push_count <= 1`, which equals my P1 `SYNC_CAP`.

## 5. New evidence not presented before

| # | Evidence | Source |
|---|---|---|
| NE1 | The S5a re-trigger fires only when `applied_edits > 0`. A-prime's R-8 both feeds a resolved-path count into the push gate and forbids folding it into `applied_edits`; the two cannot both hold, so either the audit record misdescribes the push or the merge is never re-triggered. | `fsm.py:1135-1137`; `SKILL.md:242`, `:274`; `fsm.py:206-221`; R2-A:34 |
| NE2 | `should_arm_ci_wait` includes `HALT_MAX_ROUNDS` and `TERMINAL_AUGMENT_NO_RESPONSE`; `ci_wait_autofix` restricts only auto-fix of CI findings. A Tier 1 regenerate is not such a fix, so the report-only rule at B:261 is not required by the repo. | `ci.py:49-57`, `:60-66`; B:261, :567 |
| NE3 | A pre-Wave-1 `terminal_halted` shape already exists and needs neither the run-log nor the armed FSM. Tier 3 can use it. | `SKILL.md:268` |
| NE4 | The L1 "y/n" proposal exists in the core and the skill, so R1-A's B-W7 conflates it with the rejected override channel. The caller-sets-S4' convention closes OQ-11. | `fsm.py:42`, `:1093`, `:1118-1121`; `SKILL.md:272`; `refs/state-machine.md:45`; B:112 |
| NE5 | Recovery Branch A is kind-blind: it resumes at S5a or S5 for any dangling push (`recovery.py:112-147`). That is correct, unmodified, for a Tier 2 merge and wrong for a Tier 1 sync, so the split puts the single override exactly where B already planned it (B:301). The synthesized `push_completed{recovered}` copies a fixed key tuple (`recovery.py:98-106`) and would drop `kind` unless extended. | `recovery.py:98-147`; B:96, :301 |
| NE6 | The split enlarges the routing table: tier (4) x ordinal (4) x hook (2) x entering outcome (6: clean, `REPORT_ONLY`, `HALT_MAX_ROUNDS`, `TERMINAL_AUGMENT_NO_RESPONSE`, not armed, L0) x budget (2) x cap flag (3) is about 1,150 raw combinations (my arithmetic), with a few dozen reachable rows. A single pure `conflict_action` with an exhaustive reachable-row test is therefore required, which supports A's scaffolding (A:419, FR-C6) over B's four-place routing. | `ci.py:49-57`; A:473 |
| NE7 | A collision between a conflict `cycle_id` and a fix `cycle_id` would silently undercut the INV-R1 count: the fold increments only for a cycle not yet seen. No Python generator exists, so uniqueness is by convention only. | `run_log.py:200-206`; `refs/review-retrigger.md` (resume reuses the record's id) |
| NE8 | N6 partly verified: the three merge-method field names appear in the fork's `gh repo view --json` list. Not verified: readability with a non-admin token, and whether a rebase-only repository refuses a branch containing a merge commit. | command run today, explicit `IronbellyOrg/IronClaude` |
| NE9 | `evidence-validator` confirmed: four verdicts, no re-grading, input is a report draft. It cannot judge that an intent sentence is true. | `agents/evidence-validator.md:33`, `:41`, `:66` |

## 6. Point preferences

Labels: "Split" means B for Tier 1, A for Tier 2 (P2), Wave 0 halt for Tier 3 (sections 3 M1-M4).

| Point | Preferred variant | Changed since R1? | Reason |
|---|---|---|---|
| C-008 | A and B hybrid: B's thin `probe-merge.sh`, A's `parse_stage_records` plus captured fixture | Partly (was B) | Same read-only probe; parsing moves to the core so no git runs in the suite (U-005); the script remains for fetch, `foreign_op`, `index_clean`. |
| C-009 | B | No | Tier 1 is regenerate-only; whitespace is out; tree conflicts are Tier 2. |
| C-010 | B membership (`uv.lock`, stage set `123`), A's `MechanicalRule` shape | No | One shipped row in A's data form (A-S5). |
| C-014 | Split | Yes (was B) | N1 and K9 for Tier 2/3; N4 and NE2 for Tier 1. |
| C-016 | A (state set by the caller) with B's timing (Wave 8a) | No | `fsm.py:1118-1121`; `SKILL.md:273`; T-412. |
| C-017 | Split | Yes (was B) | Tier 2 re-reviewed; Tier 1 re-polls CI on the new head (`SKILL.md:277`). |
| C-018 | Split | Yes (was B) | Tier 2 spends a round; Tier 1 does not (N4, NE2). |
| C-019 | Split | Yes (was B) | N1 couples it to C-014; N3 makes J-66 per kind. |
| C-020 | Split: no edge for Tier 1; one edge for Tier 2, landing in P2 | Yes (was B) | The edge is justified only where round and re-trigger stay; N5 shows the safe way to add it. |
| C-022 | B (A equal) | No | Strict `[pre_push_sha, base_sha]` order plus the disjointness property test (U-011). |
| C-033 | A, scoped to L1+, shipped as a precursor change | No (scope refined) | `SKILL.md:268`; `test_static_grep.py:649-661`; A's R-5. |
| X-001 | Split | Yes | As C-014. |
| X-002 | Split | Yes | As C-018. |
| X-003 | Split | Yes | As C-019. |
| X-004 | Split | Yes | As C-020. |
| X-006 | B | No | Strict order. |
| X-012 | A (state) with B's timing | No | `SKILL.md:273`; `refs/state-machine.md:101-102`. |
| X-013 | A, scoped to L1+ | No | As C-033. |
| X-015 | B | No | "No tree conflict is Tier 1" (B:177). |
| X-020 | B (A equal) | No | Classify before any mutation; only C differs. |
| X-023 | B | No | Staged is a subset of (base-changed union resolved); C's equality is unsatisfiable. |
| X-034 | A and B tie | Partly (was B) | The split uses a Wave 0 read-only step (B) and `C-initial` after run-log init (A); C is the defect. |
| X-035 | B (A equal) | No | The probe gives L1 a plan with no merge. |
| X-037 | B (A equal) | No | A sync never shares a push with a fix; A's hook order also avoids it (R2-A:39). |
| U-008 | B | No | Phasing; now also the justification for M1. |
| U-009 | B | No | High-suspicion checklist escalates to Tier 3, inside A's Tier 2 step 2. |
| A-001 | B's P1 real-PR gate plus A's advisory merge-method field read | Partly (was B) | NE8; never a halt on an unreadable value. |
| C-007 / X-026 | A (GitHub field first; probe on `CONFLICTING` or persistent `UNKNOWN`) | Yes (was B's design) | One call on a normal PR; removes X-040. |
| C-021 / X-010 | B: one sibling gate for both tiers | No (extended) | NE1; rejects A-prime's two-gate union. |
| X-005 | Tier 1 B (excluded, `sync_push_count`), Tier 2 A (counted, tagged) | Partly | A-B9, M6. |
| C-004 / X-032 | P1: thin probe plus `finish-merge.sh`; evidence script deferred or inline | Yes (was B, three scripts) | C-B4. |
| C-003 / U-003 | A (two refs split by tier) | Yes | Falls out of M1. |
| C-034 / X-014 | A's flag name `--conflict-max-tier`, B's default 1 | Yes | Name says ceiling; both sides now default 1. |
| C-015 / X-031 | B (L1 continues to review) | No | A conceded (R1-A concession 9). |
| C-032 / X-028 | B's explicit predicate, value 1 in P1 | Partly | A-B2; equals C's bound. |
| C-036 | Hybrid: A's captured fixture for the parser, B's real-repo tests for `finish-merge.sh` | Partly | R1-B concession 5. |
| C-039 / X-040 | A | Yes | A-B6. |
| U-001 / U-002 | A | Yes | A-S5. |
| U-004 | A | Yes | CI-wait skip with `pr_conflicting` when no merge is pushed; closes the blind spot I overclaimed (R1-B concession 2). |
| X-016 | B | No | Whitespace is not mechanical in Python or YAML; A conceded. |

## 7. Shared assumptions

| ID | R2 response | Changed? | Reason |
|---|---|---|---|
| A-001 | **QUALIFY** | No (adds a report) | Unverified for all variants. Keep B's P1 gate (a real PR must read `MERGEABLE` after the push) and add A's advisory report of the three merge-method fields (NE8). Report `mergeStateStatus == BLOCKED` after the push; never halt on an unreadable value. |
| A-002 | **REJECT as stated** | Yes (was QUALIFY) | The assumption includes judging that an intent is supported. The agent verifies citation grounding only (NE9). The fitting part is true: records must be rendered as a cited draft. The spec claims "grounding checked", not "intent supported". Same substance as my R1 answer, now labelled consistently with A and C. |
| A-003 | **QUALIFY** | No | Absent or empty VG-2 target caps the run at Tier 1; add C's explicit "no tests found for changed area" line. A's R2 adopted this rule. |
| A-004 | **QUALIFY** | No | Inline commands match `Bash(git *)` etc. (`SKILL.md:4`); `GIT_EDITOR=true git commit` does not (X-039); scripts are new install entries. Generalize A's allowed-tools test (A:407). |
| A-005 | **QUALIFY** | Yes (was ACCEPT with guard) | NE7: a collision silently undercuts the INV-R1 count and there is no generator to enforce uniqueness. Reserve `sync-` and `conflict-` prefixes; one test that the fix-cycle id rule cannot produce either. |
| A-006 | **REJECT** | No | `SKILL.md:268` requires local HEAD to equal `headRefOid`; every HALT and L2 message says "commit and push, or abort" (B:351). A conceded. |
