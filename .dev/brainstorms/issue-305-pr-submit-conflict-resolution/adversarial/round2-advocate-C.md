# Round 2: Rebuttal from the Variant C advocate (`variant-3-haiku-qa.md`)

Persona: QA (test surface, edge cases, regression risk, acceptance criteria). Citation forms: `A:NN` / `B:NN` / `C:NN` are variant lines; `R1-A:NN` / `R1-B:NN` / `R2-A:NN` / `R2-B:NN` are round documents; `DA:NN` is `diff-analysis.md`. Every repo line cited below was re-read in this session against the worktree at `119622e3` on 2026-11-04. Where I rely on a reading I did not execute, I say so.

## 0. Headline

Round 2 settles the architecture, and not in C's favor — correctly. I verified A's N1 end-to-end (the strongest new evidence in the debate) and it adds a **seventh High-class defect to C's architecture** (section 2, R-C16): C pushes the merge before Wave 1 without a re-trigger, so the only review on the PR is of the pre-merge head, the classifier excludes it, the silence poke is blocked by that same review's activity, and the first review wait ends `terminal_timeout`. I also concede a defect in my own Round 1 position that nobody else flagged: my preferences "C-014/C-019 → A" (act early, re-trigger) and "X-002 → C" (no round tick) were **jointly incoherent**, because the tick lands on re-review attribution (`SKILL.md:274`), which follows any re-trigger. The coupling is three-way, not two-way: {early ⇒ re-trigger ⇒ tick} (A) or {late ⇒ no re-trigger ⇒ no tick} (B). There is no third combination.

**My verdict on the tier split as amended by B: ACCEPT, with six QA conditions** (section 3). The split gives each tier a coherent triple, each half copying an existing tested pattern, and B's M1-M6 fix every collision I can find in A-prime as originally stated — including the `applied_edits`/S5a collision (B's NE1), which I re-verified at `fsm.py:1135-1137` and `SKILL.md:242`/`:274` and which is decisive against A's "no new code" claim. What I add is the part no variant has supplied yet: the **acceptance criteria and test rows the merged design must carry** (QA-1..QA-10), plus new evidence that the `push_count` bounds everyone argues about are enforced by nothing executable today (NE-C1, NE-C2).

## 1. Steelman before critique (updated)

**A-prime as amended by B, strongest form.** The split is the first proposal that explains why the skill has two push patterns at all: the fix cycle (`S4 → S6 → RESOLVING → S5a → S5`) is the protocol's review path for authored change, and the CI push (`SKILL.md:277`: "do not call `retrigger-review.sh`, reply, or resolve; re-poll CI on the new `headRefOid`") is its path for change whose check is "re-run the checks" (`refs/state-machine.md:154-155`). Tier 2 resolution is judgment-bearing authored code → fix-cycle shape; a Tier 1 regenerate is checked by `uv lock --check` and re-run CI → CI-push shape; Tier 3 never mutates → Wave 0 halt. No third pattern is invented (R2-A:15). I verified the four pieces of evidence the split rests on: N1 (`SKILL.md:103`, `classifier.py:245-247`, `:266-267`, `SKILL.md:274`), N2 (`run_log.py:238-239`, `:198-199`), N4 (`fsm.py:194`, `refs/ci-poll.md:27`), N5 (`tests/pr_submit/test_auggie_fallback.py:353-379`). All four hold.

**B's Round 2, strongest form.** B did what a refactorer should do with a superior opposing frame: adopt it and de-risk the delivery. M1 lands the FSM edge only when it is exercisable (P2, default still 1); M5 removes A-prime's second push gate and resolves the `applied_edits` collision with one additive clause; NE2 (`ci.py:49-57` vs `:60-66`) shows B's own B:261 report-only rule was never required by the repo; NE5 names the recovery key-tuple edit that would otherwise silently miscount a recovered sync push. B also ran the one command the debate needed (`gh repo view --json` on the fork, NE8) and conceded B-W4 for Tier 1. C's contributions that B adopts verbatim (`merge_push_count <= 1` equal to P1 `SYNC_CAP`; the risk register; the pin sweep; BLOCKED; call ceilings) are the parts of C that were C's actual job.

## 2. Response to every criticism of Variant C

Verdict key: **Concede** / **Partial** / **Counter**. Round 1 criticisms are answered briefly where my R1 concession already covers them and in full where Round 2 changed the picture.

### 2.1 From `round1-advocate-A.md` (C-W1..C-W9)

| # | Criticism | Verdict | Response |
|---|---|---|---|
| R-C1 | Wave 0b cannot run as placed (C-W1, X-034) | **Concede** (R1 concession 5) | Confirmed: run-log and poll loop initialize in Wave 1 (`SKILL.md:269`). The merged design drops Wave 0b entirely: read-only detect at Wave 0 end (B), acting at `C-initial` (Tier 2) or Wave 8a (Tier 1). |
| R-C2 | L1 proposes a classification it cannot produce (C-W2, X-035) | **Concede** (R1 concession 6) | The probe is the classifier input; C's after-merge classification is gone in the merged design. |
| R-C3 | Re-check point B cannot pass either parent check (C-W3, X-037) | **Concede the sequence; drop the mechanism** | My R1 repair ("push the fix first, then run the merge cycle", R1-C:81) is superseded by A's R-13 (R2-A:39): the hook order already pushes the fix first, and the conflict is caught at the Wave 8 entry hook, which arms on all four review outcomes (`ci.py:49-57`) — including `HALT_MAX_ROUNDS` and `TERMINAL_AUGMENT_NO_RESPONSE`. The uncovered residual (terminals that never arm Wave 8: `HALT_HUMAN`, `VALIDATION_FAIL`, `TERMINAL_TIMEOUT`) is a report line, not a mechanism. My R1 tally row "keep C's window coverage via the push-fix-first reorder" is withdrawn. |
| R-C4 | Staged-set equality is unsatisfiable (C-W4, X-023) | **Concede** (R1 concession 3) | B's subset form (B:352) is the merged rule. |
| R-C5 | L2 commits locally (C-W5, X-012) | **Concede** (R1 concession 2) | Merged rule: resolve at Wave 8a, stop with `MERGE_HEAD` present and uncommitted, caller sets `S4'_HALT_BEFORE_PUSH` (`fsm.py:1118-1121`). |
| R-C6 | Tier 1 holds judgment; `.claude/` premise false (C-W6, X-015/X-033) | **Concede** (R1 concessions + self-flagged X-036) | The whole "obvious-answer tree conflict" Tier 1 class is dropped; `.gitignore:127-128` makes those paths unconflictable. |
| R-C7 | Lockfile Tier 1 pushes with no VAL at L3 (C-W8, C's own OQ-3) | **Concede, and adopt C's own OQ-3 fix** | FR-7.5's "no VAL" was a hole my own Open Question 3 already admitted. Merged rule: a Tier 1 lockfile merge runs `uv lock --check` (B's VG-1 addition, B:387) plus the VG-3/VG-4 floor (seconds of cost, closes the malformed-lockfile hole); no VG-1/VG-2. Cost layering survives; the hole does not. |
| R-C8 | No Tier 2 size cap, no real-merge test (C-W9, X-017/C-036) | **Concede** | B's 8-file cap with a boundary row (8 vs 9, FR-2 B:407) and the hybrid test strategy (A's captured fixture for the parser, B's real-repo tests for `finish-merge.sh`) are the merged rule (R1-B concession 5). |
| R-C9 | First-match puts `AA` in two tiers (C-W7, X-036) | **Concede** (self-flagged in R1) | Dropped with the Tier 1 tree-conflict class. |

### 2.2 From `round1-advocate-B.md` (WC1..WC11)

| # | Criticism | Verdict | Response |
|---|---|---|---|
| R-C10 | WC1-WC4, WC7, WC9, WC11 | **Concede** | Same substance as R-C1..R-C9 above; no new defense exists. |
| R-C11 | Order-independent parent rule accepts a base-first merge (WC5, X-006) | **Concede** (R1: C-022 → A) | The set form also accepts a merge whose first parent is `base_sha` — a merge made from the base branch — inverting first-parent history and `git revert -m 1`. Strict order plus B's disjointness property test (U-011) is the merged rule. |
| R-C12 | "Publishes exactly one commit" is false (WC6, X-008) | **Concede** (R1 concession 1) | Adopt the base-ancestry check; the sentence is struck. |
| R-C13 | C fixes a payload while widening it — `poll-augment-review.sh` append touches `test_cosmos_poll.py` (WC10) | **Concede the placement; the cost is void in the merged design** | C put the fields in Wave 1's review poll — the wrong hook under the split: the conflict read belongs to the Wave 0 / Wave 8a `gh pr view` calls, not the review poll. The merged design does not touch `poll-augment-review.sh` at all, so the payload-widening edit (and its `test_cosmos_poll.py` ripple) disappears. B's own P3 `poll-ci-checks.sh` append (B:430) is the same class of edit and stays, correctly, scoped to the CI poll. |
| R-C14 | No executable test of any git step (WC9) | **Concede** (R1 concession 9) | C-036 resolves hybrid per R2-B:206. |

### 2.3 From `round2-advocate-A.md`

| # | Criticism | Verdict | Response |
|---|---|---|---|
| R-C15 | N1 coupling: act-early without re-trigger cannot complete its first review wait; placement and re-trigger are one decision (R2-A:47-58) | **Concede in full — and I verified every leg** | (a) `SKILL.md:103`: for the initial wait `pushed_sha is None`, so `expected_head = payload.get("head_sha")` — after C's Wave 0b push that is the merge SHA. (b) `classifier.py:245-247`: a review whose commits all differ from `expected_head` is excluded before ordering. (c) `classifier.py:266-267`: even the latest review is rejected if any commit differs. So the pre-merge review can never complete the wait. (d) `classifier.py:79-87` (`has_augment_activity`): that same pre-merge review counts as activity, so `silent` is False and the silence re-request path (`fsm.py:691-704`) never fires. (e) `fsm.py:706-707`: plain polling timeout → `TERMINAL_TIMEOUT`. A flagged leg (d) as "my reading"; I confirm it from the code. This is C's seventh High-class architecture defect (after X-008, X-012, X-023, X-034, X-035, X-037). |
| R-C16 | N1(c): X-001 and X-003 must be scored together | **Concede, and extend to X-002** | See Headline: the coupling is three-way because the round tick lands on attribution (`SKILL.md:274`: "The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA"). A re-trigger without a tick would require forking INV-001's meaning — exactly the class of special case all three variants claim to avoid. My R1 combination (A's placement + A's re-trigger + C's no-tick) was incoherent, and no one had to point it out but me. |
| R-C17 | A's section 4 on C: value is the QA scaffolding; `merge_push_count <= 1` taken "but not as a separate output field" (N2) | **Partial** | The scaffolding transfer is accepted. On the field: A's N2 ("count merge pushes in `push_count`, tagged, no new field") and B's M6 ("exclude Tier 1, `sync_push_count` field") are still contradictory between the two of them, and QA cannot accept "no field" under B's M6 — if Tier 1 pushes are excluded from `push_count`, the operator report loses the merge entirely unless a field carries it, and a tag without a count forces the operator to count run-log events by hand. Minimum QA requirement either way: `push_kind` on the triad records (all three variants have it) **plus** one count field for merge pushes. This is QA-2 below. |
| R-C18 | A's R-11: `merge_push_count <= 1` is tighter; A accepts it for Tier 2 at `C-ci` (R2-A:37) | **Accepted** | Both halves of the split now carry C's bound value (A: R-11; B: `SYNC_CAP = 1`, R2-B A-B2). C's C-018/C-032 position lost the principle for Tier 2 and won the number everywhere. |

### 2.4 From `round2-advocate-B.md`

| # | Criticism | Verdict | Response |
|---|---|---|---|
| R-C19 | Section 4: C's architecture unchanged, seven High defects stand; C's value is the adopted scaffolding plus the cap (R2-B:145) | **Accept** | Accurate. I add nothing in C's defense; the architecture is not what C was for, and the merged design in section 3 is not C's. |
| R-C20 | B's M4: Tier 2 at `C-ci` halts `late_conflict` uniformly, because the hook is reachable both from `S2_CLASSIFY` (edge exists) and from a preserved terminal (it does not) (R2-B:114) | **Accept, on testability grounds** | Two behaviors for one input is a routing-table smell a table test cannot pin. Uniform halt keeps `conflict_action` a function. This is the right call and it is B's existing P3 rule (B:276). |

## 3. Response to the tier split as amended by B

**Verdict: ACCEPT as the end-state design, with six QA conditions.** I accept M1 (P1 Tier 1 only, edge in P2), M2 (Tier 1 acts on all four armed outcomes), M3 (Tier 3 halts at end of Wave 0 in the `SKILL.md:268` pre-Wave-1 shape — verified: `terminal_halted` with a reason, "appended to the run-log when one exists", so no run-log and no armed FSM needed), M4 (one acting site per tier per ordinal; uniform `late_conflict` halt), M5 (one sibling gate for both tiers plus the widened S5a clause `applied_edits > 0 or kind == "merge"`), and M6 (Tier 1 excluded by kind, Tier 2 counted). The split resolves the three-way coupling by never holding an incoherent triple, and each half copies a pattern the repo already ships and tests.

Two open items between A and B that the merged spec must settle, not carry as options:

1. **The counting contradiction** (A's N2 "count it, tagged" vs B's M6 "exclude Tier 1"): my evidence NE-C1/NE-C2 (section 5) says the existing `push_count` bounds are prose-only and already strained by the CI path, so *neither* side is defending a pinned invariant. Settle it on operator reconstructability (QA-2), then pin it behaviorally (QA-1).
2. **A's R-8 remainder**: A kept "Tier 2 reuses `evaluate_push_decision`" alongside "resolved paths must not be folded into `applied_edits`" (R2-A:34). B's NE1 shows these collide at `fsm.py:1135-1137` (verified: the S5a gate is `if result.applied_edits > 0`; and `push_fail_state` maps predicate-5-false to `TERMINAL_CLEAN`, `fsm.py:217-218` — so a Tier 2 merge that clears the gate without `applied_edits` would route to a *clean report* on failure). M5's single sibling gate for both tiers is the resolution; A should accept it.

### QA acceptance criteria and tests the merged design must carry

These are the conditions of my acceptance — each names an AC and its test; several are C contributions the merged spec must not drop in translation.

| # | Acceptance criterion | Test |
|---|---|---|
| QA-1 | Whichever counting rule wins (N2 or M6), it is enforced **behaviorally with a conflict push in the fixture**. Today nothing executable pins it: no test pins the Output Contract row (`grep "Landed pushes" tests/` → 0 hits) and the behavioral `push_count` pins (`tests/pr_submit/test_loop_guard.py:56`, `test_crash_recovery.py:213`, `:232`, `:270`) all run conflicts-free. | A `rebuild_state` test over a run-log containing one `push_completed{kind:"fix"}` and one `push_completed{kind:"merge"|"sync"}` asserting the exact counts per the chosen rule (this is C's FR-7.4 AC, carried over). |
| QA-2 | The operator can reconstruct pushes-by-kind from the report alone: `push_kind` on all three triad records **and** one merge-push count field (C's FR-7.4 output field). A tag with no count field fails this. | Report-contract test asserting both surfaces. |
| QA-3 | The M5 widened clause (`applied_edits > 0 or kind == "merge"`, `fsm.py:1137` + `SKILL.md:274`) is pinned and byte-safe: no test pins the S5a clause today (verified: `grep "ONLY when this cycle"` and `applied_edits > 0` in `tests/` → 0 hits), but `test_static_grep.py:689` pins the *adjacent* sentence ("Next, when the cycle applied edits (a zero-edit cycle has no fix commit") and `:750` pins the parent-check sentence. | (a) New static pin of the widened sentence; (b) behavioral test: a zero-**edit merge** cycle re-triggers, a zero-**edit fix** cycle still does not (existing zero-edit rows in `test_loop_guard.py`/`test_validation_gate.py` must stay green); (c) assert `:689`/`:750` substrings unchanged. |
| QA-4 | Routing is one pure function with an exhaustive reachable-row test over the split's enlarged axes — tier (4) × ordinal (4) × hook (2) × entering outcome (6) × budget (2) × cap (3), B's NE6 arithmetic — plus a fail-closed default row (unknown shape → halt; C's FR-2 discipline). | The `conflict_action` table test in A's FR-C6 form (A:473), extended with the entering-outcome axis M2 adds. |
| QA-5 | M2's "Tier 1 acts after `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`" pins **which status the report shows** (preserved Augment status + sync outcome alongside, exactly as the CI human-gate rule does, `SKILL.md:250`, `ci-poll.md:28-29`). The Output Contract status enum (`SKILL.md:236`) gains no new member. | Parametrized rows: entering outcome × tier → action + reported status. |
| QA-6 | Enum and set pins are enumerated **exhaustively**, including the non-test claim site: the `EventType` docstring hard-codes "EXACTLY 41 members" (`src/superclaude/pr_submit/models.py:23`) — a spec that edits the enum without rewriting that narrative leaves a stale claim in source. `IDEMPOTENCY_SETS == 7` (`tests/pr_submit/test_idempotency.py:89`) stays untouched (no variant adds a set — state it). | Pin edits listed file-by-file (C's test-plan items 7-14 shape) + the `grep tests/ for "== 41"` PR-checklist step (C's U-024) + a docstring assertion. |
| QA-7 | Recovery is kind-aware end-to-end: the synthesized `push_completed{recovered}` carries `kind` through the key tuple (`recovery.py:98-106`, B's NE5 — verified: the tuple is fixed and kind-blind today); Branch A of a merge push resumes at Wave 8 re-arm / S5a per kind, never the wrong one; Branch B re-drives with the record's `target_sha`. | Crash-window fixtures for a dangling **merge** `push_initiated` on Branches A/B/C (C's FR-11 / test-plan item 10 rows, carried over). |
| QA-8 | Cycle-id prefixes are reserved and proven disjoint: `sync-`/`conflict-` prefixes plus one test that the fix-cycle id minting rule can never produce either (B's NE7: a collision silently undercuts the INV-R1 fold at `run_log.py:200-206`; no Python generator exists). | The prefix-disjointness test (all three variants converged on this in R1; keep it as one test, not prose). |
| QA-9 | Cost ceilings are per-tier **call counts**, not time: a mechanical conflict at L3 completes with at most 1 probe, N `git add`, 1 commit, 1 push, and the tier's event count; GitHub-field-first ordering (A's rule, adopted by B at A-B6) makes a normal PR cost one `gh pr view`. | CEILING constants asserted in the routing/flow tests (C's NFR-8, conceded by A at R-14). |
| QA-10 | The risk register keeps separate Likelihood and Impact columns (A conceded, R-16), keeps R14's "Certain, partially" rating for the Tier 2 semantic residual, and adds a row for QA-3's failure mode: *a future edit re-narrows the S5a clause and silently kills every Tier 2 re-trigger* — mitigated by the QA-3 behavioral test. | The register itself, as a reviewed deliverable. |

Also carried, uncontested: B's 13-rule tier table with the 8-vs-9 boundary row; `BLOCKED` as an explicit Tier 0 row (C's U-023, conceded by A at R-12); the marker scan scoped to conflicted paths (C's R9 fix; A's `sides=` form equivalent); B's `finish-merge.sh` subset gate with real-repo tests; A's captured fixture for `parse_stage_records`; A's `MechanicalRule` shape with the allowed-tools test (A:407) generalized to every new inline command; the rewritten "no test" boundary (see section 5, NE-C4 note): with B's script tests and A's fixture shipped, the deliberately-untested surface shrinks to the live push, the live re-trigger POST, and the probes against real GitHub.

## 4. Updated assessment of A and B

**Variant A.** A's Round 2 is the debate's best document: it moved on evidence (N1-N6), conceded eleven items, and produced the tier split that both other advocates now accept. What remains open against A:

1. The `applied_edits` collision (R-C17/R-C18 above): A's R-8 keeps both halves of a contradiction; M5 resolves it. A should adopt M5 wholesale.
2. N2 overstates the precedent (NE-C2): `push_count` is not round-bounded for CI pushes today, so "the precedent-faithful choice is: count it" defends a bound the CI path already strains. The counting rule should be settled by QA-1/QA-2, not by precedent.
3. Tier 3 via the `needs_human_decision` pre-gate requires an armed FSM; B's M3 Wave 0 halt (`SKILL.md:268` shape) is cheaper and testable with no run-log. Accept M3.

**Variant B.** B's Round 2 verification discipline (running `gh`, re-reading every line A cited, labeling what it did not execute) is exactly what the merged spec's reviewer should do, and M1-M6 fix every collision I found in A-prime. Remaining B costs, all acceptable: two scripts ship in P1 (thin probe + `finish-merge.sh`) — justified by U-005/U-010; `SYNC_CAP = 1` must be pinned by test, not prose (QA-1); M2's status-preservation rule must be pinned (QA-5); the P2 go/no-go gate ("at least 10 real text-conflict runs", B:522) is a manual gate and must be listed as manual in the test plan, not implied to be automated.

**Variant C.** For the record: C's architecture is not the merged design and should not be. C's surviving contributions are all verification-side (QA-1's AC, QA-2, QA-6's sweep + docstring catch, QA-7's recovery rows, QA-8, QA-9, QA-10, U-023, U-021 rewritten) plus one number — `<= 1` — that both halves of the split now carry. That is the outcome C's persona was supposed to produce.

## 5. New evidence not presented before

| # | Evidence | Source |
|---|---|---|
| NE-C1 | The `push_count` bounds the counting debate leans on are prose-only at the contract row and behaviorally pinned only in conflicts-free runs. No test pins "Landed pushes" / "`== max_rounds` at most" (grep over `tests/`: zero hits); the two prose bounds also disagree (`SKILL.md:239` "== `max_rounds` at most" vs `SKILL.md:275` and `refs/loop-guard.md` "<= `max_rounds + 1`"). Neither A's N2 nor B's M6 is defending an executable invariant; whichever wins must add the missing behavioral test with a conflict push in the fixture. | `SKILL.md:239`, `:275`; `tests/pr_submit/test_loop_guard.py:56`; `tests/pr_submit/test_crash_recovery.py:213`, `:232`, `:270`; grep verified this session |
| NE-C2 | A's N2 has a stronger form nobody stated: repeated L3 CI pushes inside one Wave 8 wait are each gated only by `round_counter < max_rounds` (`refs/ci-poll.md:27`), and each lands a `push_completed` → `push_count += 1` (`run_log.py:238-239`) with no round ticking, while the loop just "re-poll[s] CI on the new `headRefOid`" (`SKILL.md:277`) until completion or `--timeout`. So the existing design can already push `push_count` past `round_counter` by more than one within a single wait. My reading of `SKILL.md:277` + `ci-poll.md:27-32`; not executed. Consequence: per-kind push bounds must be stated and pinned explicitly — C's `<= 1` discipline generalized — not inherited from `push_count` prose. | `refs/ci-poll.md:27`, `:32`; `SKILL.md:277`; `run_log.py:238-239` |
| NE-C3 | B's M5 precondition holds with a caveat B understated: I verified no test pins the S5a clause itself ("ONLY when this cycle", "applied_edits > 0": zero hits in `tests/`), but `test_static_grep.py:689` pins the sentence immediately before the edit region and `:750` pins the parent-check sentence after it. The M5 edit is safe only if it is byte-anchored between those two pins, and it must add its own pin plus the zero-edit-pair behavioral test (QA-3), because the widened clause's failure mode — silently never re-triggering a Tier 2 merge — is invisible to every existing test. | `tests/pr_submit/test_static_grep.py:689`, `:750`; `src/superclaude/pr_submit/fsm.py:1133-1144` |
| NE-C4 | The event-enum pin surface is three sites, not two: besides `tests/pr_submit/test_run_log.py:168` and `tests/pr_submit/test_codex_reviews.py:441`, the `EventType` docstring itself hard-codes "EXACTLY 41 members" and narrates the member arithmetic (`src/superclaude/pr_submit/models.py:23-36`). No variant lists the docstring as an edit site; editing the enum without it leaves a stale count claim inside the source. `IDEMPOTENCY_SETS` is separately pinned at 7 (`tests/pr_submit/test_idempotency.py:89`) and no variant adds a set — the spec should say so rather than stay silent. | `src/superclaude/pr_submit/models.py:22-90`; `run_log.py:27-35`; `test_idempotency.py:89` |
| NE-C5 | Confirmation of A's N1(b) third leg, which A flagged as its own reading: the silence re-request requires `silent = poll_succeeded(payload) and not has_augment_activity(payload, contract)` (`SKILL.md:63`), and `has_augment_activity` returns True on **any** Augment review or comment (`classifier.py:79-87`). The pre-merge review that blocks completion also blocks the poke, so C's early-push design ends at plain `TERMINAL_TIMEOUT` (`fsm.py:706-707`), not even at a silence retry. Verified across all three sites this session. | `SKILL.md:63`; `classifier.py:79-87`; `fsm.py:691-708` |

## 6. Point preferences

"Split" = B's amended tier split (M1-M6): Tier 1 late (B shape), Tier 2 early (A shape, P2), Tier 3 Wave 0 halt.

| Point | Preferred variant | Changed since R1? | Reason |
|---|---|---|---|
| C-008 | A (hybrid with B's thin emitter) | No | Probe before any merge; A's `parse_stage_records` + captured fixture; B converged here (R2-B:167). |
| C-009 | B | No | Narrowest tiers; fail-closed rows; boundary-tested cap. |
| C-010 | B membership, A `MechanicalRule` shape | No | `uv.lock` stage `123` only; one row in A's data form. |
| C-014 | Split (with B's M3 Wave 0 halt for Tier 3) | **Yes** (was A) | N1 three-way coupling (R-C15/R-C16); N4 for Tier 1; both verified. |
| C-016 | A state (caller-set S4') + B timing (Wave 8a) | **Yes** (timing) | `fsm.py:1118-1121`; T-412; no mutation below L3 before the review settles. |
| C-017 | Split | **Yes** (was A) | Tier 2 re-reviewed via the M5-widened S5a; Tier 1 re-polls CI (`SKILL.md:277`). |
| C-018 | Split, with C's cap value `<= 1` on both halves | **Yes** (was C) | The no-tick principle survives only on the Tier 1 half; the number was adopted by A (R-11) and B (A-B2). |
| C-019 | Split | **Yes** (was A) | N1 makes re-trigger mandatory exactly where acting is early; N3 makes J-66 per-kind. |
| C-020 | Split: no edge Tier 1; one edge Tier 2 in P2 | **Yes** (was B) | Edge pinned the `test_auggie_fallback.py:353-379` way; lands only when exercisable (M1). |
| C-022 | B (A equal) | **Yes** (was A) | Same strict order; B's disjointness property test (U-011) is the stronger pin. |
| C-033 | A, scoped to L1+, precursor change | **Yes** (scope) | `test_static_grep.py:649-657` byte-identical at L0; R2-A R-4/R-5. |
| X-001 | Split | **Yes** | As C-014. |
| X-002 | Split | **Yes** (was C) | R-C16: my R1 pairing with A's placement was incoherent. |
| X-003 | Split | **Yes** | As C-019. |
| X-004 | Split | **Yes** | As C-020. |
| X-006 | B (A equal) | **Yes** (was A) | Strict order + disjointness property. |
| X-012 | A state + B timing | **Yes** (timing) | As C-016. |
| X-013 | A, scoped to L1+ | **Yes** (scope) | As C-033. |
| X-015 | B | No | "No tree conflict is Tier 1" (B:177). |
| X-020 | A and B tie | **Yes** (cosmetic; was A) | Both classify before mutation; only C differed. |
| X-023 | B | No | Subset check is the only satisfiable form. |
| X-034 | A and B tie | **Yes** (was A) | Wave 0 read-only detect (B) + `C-initial` after run-log init (A); C was the defect. |
| X-035 | B (A equal) | **Yes** (cosmetic; was A) | The probe gives L1 a plan with no merge in both. |
| X-037 | A (B equal) | No | Wave 8 entry hook covers the window (`ci.py:49-57`); my reorder withdrawn (R-C3). |
| U-008 | B | No | P0-P3 gates; now also the justification for M1's sequencing. |
| U-009 | B | No | The only semantic-conflict detector; escalates inside Tier 2 step 2. |
| A-001 | B's P1 real-PR gate + A's advisory merge-method read | **Yes** (was "none") | NE8: field names verified in the fork's `gh`; readability and rebase-only behavior unverified; never halt on an unreadable value. |
| C-021 / X-010 | B: one sibling gate for both tiers (M5) | **Yes** (unscored in R1) | NE1 verified at `fsm.py:1135-1137`; `push_fail_state` would route a p5-false merge to `TERMINAL_CLEAN` (`fsm.py:217-218`). |
| X-005 | B's M6, subject to QA-1/QA-2 | **Yes** | NE-C1/NE-C2: no executable bound exists today; pin whichever rule wins with a conflict-push fixture. |
| C-032 / X-028 | B's explicit predicate at value 1 | **Yes** | Equals C's bound; now on both tiers (R-C18). |
| C-036 | Hybrid: A fixture (parser) + B real-repo (gate) | **Yes** | R1-B concession 5. |
| C-007 / X-026 / X-040 | A (GitHub field first) | **Yes** | One call on a normal PR; removes X-040 (B conceded at A-B6). |
| C-034 / X-014 | A's flag name, default 1, per M1 phasing | **Yes** | C's no-flag position is dropped: the split needs the dial, and both sides defaulted to 1. |
| U-004 | A | **Yes** | `pr_conflicting` CI-wait skip; closes the blind spot B admitted overclaiming (R1-B concession 2). |
| X-016 | B | **Yes** (from implicit C) | Whitespace is not mechanical in Python/YAML; A conceded (R-7). |
| C-015 / X-031 | B (L1 reports and continues to review) | **Yes** (unscored in R1) | A conceded (R1-A concession 9, R-2). |

## 7. Shared assumptions

| ID | R2 response | Changed? | Reason |
|---|---|---|---|
| A-001 | **QUALIFY** | Yes (was ACCEPT-and-promote) | Converged with A and B: advisory report of `mergeCommitAllowed` / `rebaseMergeAllowed` / `squashMergeAllowed` (NE8 — names verified, non-admin readability and rebase-only behavior unverified), B's P1 gate reads `MERGEABLE` on a real PR after the push, `BLOCKED` reported with a reason line; never a halt on an unreadable value. |
| A-002 | **REJECT as stated** | Yes (was QUALIFY) | NE9 and my own re-read agree: four verdicts, no re-grading, report-draft input (`agents/evidence-validator.md:33`, `:41`, `:66`). The merged spec claims "grounding checked" and renders records as a cited draft; it never claims intent truth. All three advocates now hold the same position. |
| A-003 | **QUALIFY** | Yes (was ACCEPT) | Absent or empty VG-2 target caps the cycle at Tier 1 (B's rule, adopted by A R2); plus C's explicit "no tests found for changed area" report line instead of a silent green. |
| A-004 | **QUALIFY** | No | C's `GIT_EDITOR=true` form is dropped (use `git commit -F`, A/B form); inline commands match the `SKILL.md:4` prefixes; scripts are new install entries; A's allowed-tools test (A:407) generalized to every new inline command. |
| A-005 | **QUALIFY** | Yes (was ACCEPT with a pin) | NE7 raises the stakes: a collision silently undercuts the INV-R1 fold (`run_log.py:200-206`) and no generator enforces uniqueness. Reserve `sync-`/`conflict-` prefixes; one test that the fix-cycle id rule can produce neither (QA-8). |
| A-006 | **REJECT** | No | Head binding requires local HEAD == `headRefOid` (`SKILL.md:268`). Every HALT and L2 message says "commit **and push**, or abort" (B:351) — including C's own HALT templates, which share the defect A's had; the merged spec applies the fix uniformly. |
