# Round 2: Rebuttal from the Variant A advocate (`variant-1-opus-architect.md`)

Persona: architect (maintainability, extension scaffolding). Citation forms: `A:NN` / `B:NN` / `C:NN` are variant lines, `R1-B:NN` / `R1-C:NN` are lines of `round1-advocate-B.md` / `round1-advocate-C.md`, `DA:NN` is `diff-analysis.md`. Every repo line cited below was re-read in this session against the worktree at `119622e3` on 2026-11-04.

## 0. Headline

Round 1 changed my position on one coupled question and left the rest standing. The new repo evidence (section 3) shows that **when a conflict is acted on and whether reviewers are re-triggered are one decision, not two**: a review only counts for the current head, and a push does not trigger a review. So there are exactly two coherent designs: act early and re-trigger (A), or act late and do not re-trigger (B). C's combination, act early without a re-trigger, cannot complete its first review wait.

Within that frame I now hold that **the right answer differs by tier**:

- **Tier 2 (model judgment):** A's path. Act at `C-initial`, re-review the merge, spend a round.
- **Pure Tier 1 (deterministic regenerate):** B's path. Act late at `C-ci`, mirroring the CI-push precedent: no round, no re-trigger, B's sibling push gate.
- **Tier 3:** detect and halt at `C-initial`, before any review is spent.

Each path copies an existing, tested pattern in the skill (the fix cycle and the CI push). Neither invents a third. I call this A-prime below.

## 1. Steelman before critique (updated)

**B, after its Round 1 defense.** B's strongest case is no longer "fewer lines touched". It is that B's design is the only one that follows the CI-phase precedent faithfully. That precedent (`refs/state-machine.md:154-155`: "A CI-phase push skips S5a / S6 / RESOLVING (the push itself re-runs checks)") already pushes model-authored CI fixes with no bot re-review. So the project's protocol does not, in general, demand a re-review of every pushed change. B also understood the placement coupling before anyone else did: B:205 rejects acting early *because* "completion is keyed to the expected head (G19)", so acting early drags in S5a and INV-R1. Finally, B's Round 1 concessions (R1-B:102-109) remove most of my R1 objections: create-path rebase, the CI blind spot, K8 for Tier 2, the duplicated triad builder, script testability, the line-count pin, and the cost claim.

**C, after its Round 1 defense.** C conceded nine defects outright (R1-C:73-83) and repositioned itself as the QA scaffolding around the architecture. That is honest, and the scaffolding is real: the risk register with separate likelihood and impact (C:157-174), the "deliberately no test" boundary (C:153-155), the `== 41` pin sweep (C:161), `BLOCKED` as an explicit Tier 0 row (C:55), and per-tier call-count ceilings (NFR-8, C:127). C's sharpest point against A is that a conflict silently halves the default fix budget for exactly the PRs this feature serves (R1-C:57).

## 2. Response to every criticism of Variant A

| # | Source | Criticism | Response | Evidence |
|---|---|---|---|---|
| R-1 | B WA1 (R1-B:75); C §A-2 (R1-C:57) | A mechanical conflict pays for a review round. With the budget spent, FR-C23 sends a Tier 1 conflict to `HALT_MAX_ROUNDS` and leaves the PR unmergeable. | **Concede for Tier 1; counter for Tier 2.** New evidence N4 makes it worse than B said: reusing `evaluate_push_decision` at `C-ci` applies predicate 4 `round_counter < max_rounds` (`fsm.py:194`). A review that ends `clean` exactly at `round_counter == max_rounds` reaches Wave 8 with the budget spent (`refs/ci-poll.md:27`), so A would refuse a `uv.lock` regenerate on a clean PR. That is issue #305's own failure. Fix: pure Tier 1 moves to the CI-push shape. For Tier 2 the round is honest. The merge is model-written code that gets a bot review, and a round is what the skill charges for a reviewed remediation. C's "silently" is not accurate: A:243 documents the cost. But documenting a cost is not removing it, and for Tier 1 removing it is right. | `fsm.py:191-196`; `refs/ci-poll.md:27`; A:236-243 |
| R-2 | B WA2 (R1-B:76); C §A-5 (R1-C:60) | L1/L2 stop on a conflicted PR before any review poll. | **Concede (extends R1 concession 9 to L2).** Below L3, `C-initial` never mutates. L1 reports the plan and continues to review. L2 reports, continues to review, and resolves only at `C-ci` (reached only after a `clean` / `REPORT_ONLY` review), then stops at `S4'_HALT_BEFORE_PUSH`. The caller sets that state, as it already does for L2 fixes (`fsm.py:1118-1121`), so no new edge is needed for it. B's reason for L2 timing also holds: a worktree left mid-merge would break a later fix cycle's `git commit --only` (B:254). | `fsm.py:1118-1121`; B:250-254 |
| R-3 | B WA3 (R1-B:77) | Re-triggering at `C-initial` is noisy, and R-5 concedes a wasted review. | **Counter on the noise; concede the quota.** The re-trigger is not optional once the head moves (N1). The initial wait classifies against the current head (`SKILL.md:103`), the classifier drops any review whose commit is not that head (`classifier.py:245-247`, `:266-267`), and "a push does NOT auto-trigger a re-review by either bot" (`SKILL.md:274`). Without the re-trigger, the run never sees a review at all. B's own placement table says the same (B:205). The wasted pre-merge review (A:614, R-5) is real. It is also why pure Tier 1, which needs no re-review, moves late. | `SKILL.md:103`, `:274`; `classifier.py:245-247`, `:266-267`; B:205 |
| R-4 | B WA4 (R1-B:78) | AD-7 bundles an unrelated pin rewrite into the feature. | **Concede the delivery; keep the substance.** Ship AD-7 as a separate precursor change that touches `test_static_grep.py:654-661` on its own, as B proposes (R1-B:102). | `test_static_grep.py:654-661` |
| R-5 | C §A-3 (R1-C:58) | AD-7 changes L0 behaviour (Wave 0 runs at all ordinals) while claiming L0 is unchanged. | **Concede; scope AD-7 to L1+.** The repo pins the L0 sentence verbatim (`test_static_grep.py:649-653`) and the token "rebase if behind `origin/<base>`" (`:657`). At L0 the STOP block does not apply (it is gated on `--monitor >= 1`, `SKILL.md:220`) and head binding is skipped (`SKILL.md:268`). So L0 keeps today's rebase byte-for-byte. At L1+ the create path neither rebases nor halts on behind-base; behind is a Tier 0 report. Only `:658` and `:660`, the L1+ create-path HALT, are rewritten. | `SKILL.md:220`, `:267-268`; `test_static_grep.py:649-661` |
| R-6 | B WA5 (R1-B:79); C A-006 (R1-C:92) | The operator recovery text omits the push. | **Concede (R1 concession 1).** Adopt B's text verbatim: "run `git commit` yourself and push; or `git merge --abort`" (B:351), in every HALT and L2 message (A:174-175, :217, :327). | `SKILL.md:268` |
| R-7 | B WA6 (R1-B:80) | `WHITESPACE_ONLY` at Tier 1 is unsafe. | **Concede (R1 concession 3).** Remove class 8 (A:130, :151); those paths fall to `TEXT`, Tier 2. | A:130 |
| R-8 | B WA7 (R1-B:81); C §A-1 (R1-C:56) | Passing `applied_edits = resolved path count` (A:337) stretches INV-016 predicate 5, so the audit record misdescribes the push. | **Qualify.** On the Tier 2 early path, the decision record already carries `push_kind: "merge"` (A:258, :337), so a reader can tell the push apart. But the Output Contract field `applied_edits` is defined as "Grounded edits applied this run (INV-016 predicate 5)" (`SKILL.md:242`). Resolved paths must not be folded into it; they go in A's `conflict.files` (FR-C21). On the Tier 1 late path, **concede fully to B's sibling `evaluate_sync_decision`** (B:327-338). Predicate 4 is wrong there (R-1), and predicate 5 has no meaning there. | `SKILL.md:242`; `fsm.py:173-204`; B:327-338 |
| R-9 | B WA8 (R1-B:82) | A has a wider FSM and record footprint. | **Partly concede, and A-prime makes it larger.** The tier split carries the union of the two shapes: one FSM edge (Tier 2) plus one sibling push gate (Tier 1). I accept that cost on purpose. There are two different kinds of conflict push, and each copies an existing pattern: a reviewed fix cycle, or a CI push. Bending one pattern to cover both is what produced R-1. | — |
| R-10 | C §A-4 (R1-C:59) | The new edge reopens the largest regression surface, and a misspelled event silently stays put (`fsm.py:801-802`). | **Counter.** The repo already adds edges this way. V1.1 added six edges, each pinned by an explicit row assert in `test_transition_v11_edges` (`tests/pr_submit/test_auggie_fallback.py:353-379`). A's FR-C7 (A:475) requires the same row for `(S2_CLASSIFY, "conflicting")`, so a misspelled event fails that test instead of passing silently. **Concede scope:** in A-prime the edge exists only for the Tier 2 early cycle. Tier 1 and Tier 3 never send it (Tier 3 uses the `needs_human_decision` pre-gate, `fsm.py:730-731`). | `test_auggie_fallback.py:353-379`; `fsm.py:730-731`, `:801-802` |
| R-11 | C strength 5 (R1-C:45) | A allows a conflict cycle per round, up to `max_rounds` merge pushes. | **Concede as written.** In A, a `C-ci` Tier 2 cycle re-enters review, can reach Wave 8 again and re-run `C-ci`. In A-prime, a Tier 1 merge at `C-ci` goes straight to the CI wait and does not loop back, so there is at most one per Wave 8 entry. Tier 2 cycles each spend a round, so `max_rounds` bounds them. C's `merge_push_count <= 1` (C:112) is tighter. I would accept it for Tier 2 at `C-ci` if the panel prefers a hard bound. | A:187, :352 |
| R-12 | C strength 7 (R1-C:47) | A reaches `BLOCKED` only implicitly. | **Concede the test, not the behaviour.** `mergeability()` already maps `MERGEABLE` + `BLOCKED` to `"clean"` (A:413). Add C's U-023 as an explicit parametrized row. | A:413; C:55 |
| R-13 | C strength 8 (R1-C:48) | A does not cover the base moving between VAL and a fix push. | **Counter.** A fix push is a fast-forward of the PR branch. A base move cannot make it fail, and it publishes nothing unreviewed. The conflict it leaves is caught at the next hook (`C-ci`) before CI is armed. C's own repair, "push the fix first, then run the merge cycle" (R1-C:81), is exactly what the hook order already does. No check inside the guard is needed, and adding one is what produced X-037. | A:187, :352; DA:119 |
| R-14 | C strength 6 (R1-C:46) | A's NFR bounds time, not calls. | **Concede (minor).** Adopt C's per-tier call ceilings (C:127) as an added NFR alongside A's NFR-1. | C:127 |
| R-15 | C steelman of B (R1-C:32) | A's flag defaults to 2 with no rollout story. | **Concede (R1 concession 5).** Adopt B's P0-P3 phasing; `--conflict-max-tier` defaults to 1. | B:514-525 |
| R-16 | C strength 1 (R1-C:41) | A's risk register combines likelihood and impact in one column. | **Concede (cosmetic).** Split the columns as C does. | A:606-620 |
| R-17 | B C-020 reason (R1-B:134) | A's edge buys nothing once the round and the re-trigger are dropped. | **Agree, and that is the tier rule.** Where the round and re-trigger are dropped (Tier 1), the edge is dropped too. Where they stay (Tier 2), the edge stays. This matches R1 concession 2. | — |

## 3. New evidence not presented in Round 1

**N1. A review counts only for the current head, and a push triggers no review. So placement and re-trigger are one decision.**

- The initial wait sets `expected_head = payload.get("head_sha")` (`SKILL.md:103`).
- `_completion_reviews` skips any review whose commits all differ from that head (`classifier.py:245-247`) and rejects the latest one if any commit differs (`:266-267`).
- `SKILL.md:274`: "a push does NOT auto-trigger a re-review by either bot".

Consequences:

- (a) A's `C-initial` re-trigger is required, not noise (answers R-3).
- (b) **C has a new defect that the diff analysis did not list.** C pushes the merge before Wave 1 (C:74). It does not re-trigger (C:82: "a merge push does NOT re-trigger reviewers"), yet expects "Wave 1 reviews the merged head" (C:100). The only review on the PR is of the pre-merge head, so the classifier keeps returning `polling`. The run then likely ends `terminal_timeout` (`fsm.py:706-707`). The silence re-request (`fsm.py:691-704`) fires only when the snapshot shows zero Augment activity, and a completed pre-merge review is activity. That last step is my reading of the code, not an executed test. Severity: High, the same class as X-034.
- (c) X-001 and X-003 should be scored together. The coherent pairs are {early, re-trigger} (A) and {late, no re-trigger} (B). B stated this coupling itself (B:205).

**N2. The CI push precedent already lands pushes that spend no round.**

- `rebuild_state` adds every `push_completed` to `push_count` (`run_log.py:238-239`).
- `round_counter` ticks only on `round_incremented` (`run_log.py:198-199`), at the S5→S2 edge (`fsm.py:776-777`).
- A CI fix push skips S5 (`refs/state-machine.md:154-155`) and is gated only by `round_counter < max_rounds` (`refs/ci-poll.md:27`).

So my R1 Strength 1, "`push_count <= max_rounds` holds because each push spent a round", describes the review cycle only. It is not an existing guarantee for every push. Two corrections follow:

- B's and C's case for a separate counter is weaker than they say. The existing meaning of `push_count` is "every landed push", including CI pushes.
- My charge that B and C "fork" that meaning stands. They are the ones who *exclude* a kind of push (B:271, C:81).

The precedent-faithful choice is: a merge push counts in `push_count`, tagged `push_kind: "merge"` (A:258), with no `sync_push_count` or `merge_push_count` field.

**N3. J-66 does not say what I claimed in Round 1.** The research item reads: "A conflict resolution is authored code and gets whatever review path the project's protocol defines for authored changes" (`.dev/research/issue-305-conflict-resolution/03-roi-scored-list.md:94`). This protocol defines two review paths:

- S5a re-review for review-cycle pushes (`SKILL.md:274`);
- none for CI pushes (`SKILL.md:277`).

So J-66 decides the question per kind of change, not globally. My R1 Strength 2 overclaimed. Read correctly, J-66 supports the tier split:

- A Tier 2 resolution is judgment-bearing, like a review fix, so it takes the re-review path.
- A Tier 1 regenerate is checked by `uv lock --check` and re-run CI, like a CI fix, so it takes the CI path.

**N4. Reusing `evaluate_push_decision` at `C-ci` reproduces issue #305.** Predicate 4 is `round_counter < max_rounds` (`fsm.py:194`). A run whose last attributed re-review is `clean` at `round_counter == max_rounds` arrives at Wave 8 with no budget. There, CI fixes are already forbidden (`refs/ci-poll.md:27`), and A's FR-C23 would block the merge too. The result is a reviewed, clean PR left unmergeable over a lockfile. This is the decisive reason the late Tier 1 path needs B's predicate set (B:333-336), not A's.

**N5. The repo has a precedent for safe edge additions.** `test_transition_v11_edges` (`tests/pr_submit/test_auggie_fallback.py:353-379`) pins every V1.1 edge row by row, plus the unchanged INV-001 edge. An edge added the same way is not a silent-failure risk (answers R-10).

**N6. A-001 has a cheap observation hook.** The installed `gh` lists `mergeCommitAllowed`, `rebaseMergeAllowed` and `squashMergeAllowed` as `gh repo view --json` fields. I checked this by running `gh repo view --json` today, which prints the field list. Two things remain **unverified**: whether a non-admin token can read them, and whether a rebase-merge-only repository refuses a PR branch that contains a merge commit.

## 4. Updated assessment of B and C

**B.** B's Round 1 defense strengthened B on Tier 1 and weakened it on Tier 2.

- **Tier 1:** B is right. N2 and N4 show that act-late plus a sibling gate is the only design that resolves a mechanical conflict without charging the review budget. It is also the only one that still works when that budget is already spent.
- **Tier 2:** B's own concession says a re-trigger "must be designed before the default flips" (R1-B:104). A re-trigger after Wave 8a re-opens the review loop: S5 attribution, `rereview_requested`, INV-R1. That needs either A's edge or an equivalent. So B's planned follow-up converges on A's Tier 2 path.
- **B-W4 stands:** a known conflict is report-only after `HALT_MAX_ROUNDS` (B:261). Under A-prime that matters less, because Tier 2 and Tier 3 are handled at `C-initial` before any round is spent.
- **Remaining B costs I still reject:** three scripts where one earns its place (`finish-merge.sh`), and `SYNC_CAP` as a counter where hook structure already bounds the pushes.

**C.** C's defense was the most candid of the three and moves C's value from architecture to verification, which I accept. N1 adds one more High defect to C's architecture: an early merge with no re-trigger. C's QA contributions all transfer cleanly to A-prime: the risk register, the no-test list, the pin sweep, the `BLOCKED` row, the call ceilings, and the base-ancestry correction C itself adopted. C's `merge_push_count <= 1` is the tightest bound. I would take it for Tier 2 at `C-ci` but not as a separate output field (N2).

## 5. Point preferences

High-severity points first, then other points where my preference changed.

| Point | Preferred variant | Changed since R1? | Reason |
|---|---|---|---|
| C-008 | A (B equal) | No | Read-only `merge-tree -z` probe before any merge; captured-fixture parser (A:557). |
| C-009 | B | No | Narrowest tiers; whitespace removed from A (R-7). |
| C-010 | B membership, A `MechanicalRule` shape | No | `uv.lock` stage `123` only; data-driven extension point. |
| C-014 | Split: A for Tier 2/3 (`C-initial`), B for pure Tier 1 (`C-ci`) | **Yes** (was A) | N1, N4: early action needs a re-trigger and a round, which a deterministic regenerate does not earn; Tier 3 still halts before reviews are spent (B's K9, B:539). |
| C-016 | A's state with B's timing | **Yes** (was A) | L2 resolves only at `C-ci`, then the caller sets `S4'_HALT_BEFORE_PUSH` (`fsm.py:1118-1121`); no mutation at `C-initial` below L3 (R-2). |
| C-017 | Split: A for Tier 2, B for Tier 1 | **Yes** (was A) | Tier 2 re-reviewed via S5a/S5; Tier 1 re-polls CI on the new head (`refs/state-machine.md:154-155`). |
| C-018 | Split: A for Tier 2 (tick), B/C for Tier 1 (no tick) | **Yes** (was A) | N2: no-round pushes already exist; N4: charging Tier 1 a round reproduces #305. |
| C-019 | Split: A for Tier 2 (required by N1 when acting early), B for Tier 1 | **Yes** (was A) | N3: J-66 defers to the protocol's two review paths. |
| C-020 | Split: A edge for Tier 2 only, B (no edge) for Tier 1 | **Yes** (was A) | The edge is justified exactly where the round and re-trigger stay (R-17); edge pinned like `test_auggie_fallback.py:353-379`. |
| C-022 | B (A equal) | No | Strict order plus B's disjointness property test (B:325). |
| C-033 | A, scoped to L1+, shipped as a precursor change | **Yes** (qualified) | L0 rebase and AC-1 stay byte-identical (`test_static_grep.py:649-657`); R-4, R-5. |
| X-001 | Same split as C-014 | **Yes** | Score X-001 together with X-003 (N1-c). |
| X-002 | Same split as C-018 | **Yes** | N2, N4. |
| X-003 | Same split as C-019 | **Yes** | N1, N3. |
| X-004 | Same split as C-020 | **Yes** | R-10, R-17. |
| X-006 | B | No | Strict `[pre_push_sha, base_sha]`; disjointness test. |
| X-012 | A state, B timing | **Yes** (timing) | No commit (T-412, `refs/state-machine.md:101-102`); L2 acts at `C-ci` only. |
| X-013 | A, scoped to L1+ | **Yes** (qualified) | Same as C-033. |
| X-015 | B (A equal) | No | No tree conflict is Tier 1 (B:177). |
| X-020 | A and B tie | No | Classify before any mutation. |
| X-023 | B | No | Staged ⊆ base-changed ∪ resolved; `finish-merge.sh` adopted (R1 concession 7). |
| X-034 | A | No | `C-initial` runs after the run-log exists (`SKILL.md:269`). |
| X-035 | A and B tie | No | The probe gives L1 a plan with no merge. |
| X-037 | A (B equal) | No | The hook order already pushes the fix first and catches the conflict at `C-ci` (R-13). |
| U-008 | B | No | P0-P3 gates; flag default 1. |
| U-009 | B | No | High-suspicion checklist escalates to Tier 3 inside A's Tier 2 step 2. |
| A-001 | C's direction with B's gate, using A's hook | **Yes** (was none) | Read the three merge-method fields once before the first merge push (N6, unverified readability) and report them; re-read `mergeStateStatus` after the push (A:352); B's P1 gate checks a real PR. |
| C-021 / X-010 | Split: B sibling gate for Tier 1, A reuse for Tier 2 with `push_kind` | **Yes** (was A) | N4; R-8. |
| X-005 | A (single tagged `push_count`) | No (reason updated) | N2: the existing `push_count` already counts no-round CI pushes; one tag beats a parallel counter. |
| C-015 / X-031 | B | **Yes** (R1 concession 9, now scored) | L1 reports and continues to review. |
| X-016 | B | **Yes** (R1 concession 3, now scored) | Whitespace is not mechanical in Python or YAML. |
| C-034 / X-014 | A's flag name, B's default 1 | **Yes** (R1 concession 5, now scored) | Phased rollout with the dial. |
| C-032 / X-028 | A-prime (C equal) | **Yes** (was implicit A) | Tier 1 at most one per Wave 8 entry; Tier 2 bounded by rounds; accept C's `<= 1` at `C-ci` if a hard cap is wanted (R-11). |

## 6. Shared assumptions

| ID | R2 response | Changed? | Reason |
|---|---|---|---|
| A-001 | **QUALIFY** | Yes (adds a check) | Still unverified for all three variants. Add a pre-push report of `mergeCommitAllowed` / `rebaseMergeAllowed` / `squashMergeAllowed` (fields confirmed in the installed `gh`; readability without admin unverified), never a halt on an unreadable value. Also report `mergeStateStatus == BLOCKED` with a reason line after the push. |
| A-002 | **REJECT as stated** | No | `evidence-validator` checks citation grounding only. The records must be rendered as a cited draft, and the spec claims "grounding checked", not "intent supported". All three advocates now agree (R1-B:116, R1-C:88). |
| A-003 | **QUALIFY** | Yes (adopts B's rule) | When the VG-2 target is absent or runs no tests, Tier 2 routes to Tier 3. B's form is "cap the cycle at Tier 1" (R1-B:117), which I adopt. Also adopt C's explicit "no tests found for changed area" report line (R1-C:89). |
| A-004 | **QUALIFY** (was ACCEPT for A) | Yes | With `finish-merge.sh` adopted, A-prime has one script. Commands inside a script are not prefix-matched (R1-B:118), but the script is a new install and permission entry. Generalize A's allowed-tools test (A:407) to every new inline command. C's `GIT_EDITOR=true` form still fails (X-039). |
| A-005 | **QUALIFY** | No | Reserved `conflict-<n>` prefix, a pure `is_conflict_cycle` helper, and one test that the fix-cycle id rule cannot produce that prefix. No Python generator exists; the SKILL mints ids (`refs/review-retrigger.md:67`). |
| A-006 | **Concede the contradiction** | No | Adopt B's push-inclusive recovery text (B:351) everywhere (R-6). |
