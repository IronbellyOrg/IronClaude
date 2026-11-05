# Round 1 — Advocate for Variant A (`variant-1-opus-architect.md`)

Persona: architect (structure, dependencies, long-term impact). Focus: maintainability and extension scaffolding. Citations: `A:NN` / `B:NN` / `C:NN` = variant line; `DA:NN` = `diff-analysis.md` line; repo paths relative to the worktree root, re-read on 2026-11-04 at `119622e3`.

## Position Summary

Variant A treats a merge conflict as one more kind of remediation cycle in the machine that already exists, not as a second pipeline running beside it. That choice runs through the whole design: one new FSM edge `(S2_CLASSIFY, "conflicting")` reuses the round gate, G-edit, S7 VAL, the S4 push triad, S5a re-trigger and S5 attribution (A:45, A:224-232). One pure module, `conflicts.py`, makes every decision (A:49, A:409-425). Two refs split by tier make cost grow with complexity (A:72-73, NFR-1 A:528). Rules are data tuples (`MechanicalRule`, `HUMAN_PATH_PATTERNS`), so a new lockfile or protected path is one tuple row plus one test row (AD-10, A:59, A:391-404).

Long term, the alternative designs are more expensive. B adds a second push gate (`evaluate_sync_decision`), a second push counter (`sync_push_count`), a second cap (`SYNC_CAP`), a second resume rule for Branch A, three scripts and a parallel output contract (B:88-97, B:270-272, B:299). Each of these must then be kept in step with the INV-016 / INV-R1 / INV-R2 machinery forever. C has the same parallel counters, plus sequencing defects that keep it from running as written (DA:116-119).

A has real weaknesses and I concede them below: the operator-recovery message (X-041), the cost of one round, a Tier 1 whitespace class that is unsafe for Python, an overclaimed `evidence-validator` verdict, and Tier 2 being on by default. None of them is structural. Each is fixed with a few lines inside A's own shape. B's and C's structural choices cannot be patched that way.

## Steelman

### Variant B: strongest form

B's best argument is minimal blast radius on an already brittle surface. `SKILL.md` is 331 lines, pinned by dozens of literal-substring tests (B:27-36). B leaves `push_parent_ok`, `evaluate_push_decision`, `build_push_triad` and `transition()` byte-identical (B:18, B:129). It copies the CI-phase precedent, a SKILL-owned phase with no FSM edges, which the repo already ships and tests: `refs/state-machine.md:140-157`, "A CI-phase push skips S5a / S6 / RESOLVING". That precedent is real, and B quotes it accurately.

B gets these right, and I would adopt them:

- **U-008 phasing (B:514-525).** P0 is read-only and fixes the "CI polls forever on a conflicted PR" blind spot with zero mutation. Tier 2 ships dark behind `--sync-tier 1`. This is better rollout discipline than A's single release with `--conflict-max-tier` defaulting to 2 (A:76).
- **U-009 high-suspicion checklist (B:193-195).** It escalates to Tier 3 when one side changes a signature, schema, dependency or public API while the other side adds callers. A's Tier 2 step 2 collects that evidence with `git grep -n <symbol>` (A:158) but never makes it a halt trigger. B is right that it should be one.
- **U-010 `finish-merge.sh` (B:92, B:352).** The positive staged-set bound "staged ⊆ base-changed ∪ resolved" is a stronger check than A's negative check "no `OPERATOR_PENDING` path" (A:325). It also lives in a script that real-repo tests can run (B:460). Ref prose cannot be run that way.
- **U-011 disjointness property test (B:325).** Asserting that `push_parent_ok` and `merge_parent_ok` reject each other's accepted inputs is the right way to pin "the sibling cannot weaken the original".
- **Narrow Tier 1 (B:157, B:177).** `uv.lock` with stage set `123` only. "No tree conflict is Tier 1." Whitespace is rejected as a Tier 1 class (B:117). See Concession 3: B is right and A is wrong on whitespace.

### Variant C: strongest form

C's best argument is testability as the primary design constraint: every pinned count is re-pinned in the same commit (C:14, C:161 "grep `tests/` for `== 41`"), and every tier boundary is a pure function with fail-closed rows (C:107, C:135). C rejects a new CLI flag because it "doubles the test matrix against the parser" (C:46). That is a fair critique of A's `--conflict-max-tier`, which makes A's routing table ordinal × tier × cap × budget × terminal (A:473). C's Definitions section (C:16-24, U-020) fixes vocabulary the other two leave implicit. C's `merge_push_count <= 1` (C:112 FR-7.4) is the simplest possible bound on merge pushes. C scopes the marker scan to the conflicted-path set so repo fixtures containing marker literals cannot block a merge (C:109, R9 C:169), and A's `conflict_marker_lines(..., sides=...)` (A:421) solves the same problem.

C's strongest substantive point is order-independent parent checking (C:93). The set of ancestors a fast-forward publishes is the same for `[pre_push_sha, base_sha]` and `[base_sha, pre_push_sha]`, so as a pure publishing-safety argument, order does not matter. I accept that as stated, and still prefer strict order for reasons given under X-006.

## Strengths Claimed (Variant A)

1. **Invariants preserved with no new counters (AD-3, A:45, A:234-241).** A conflict push is a push that spent a round. So `push_count <= max_rounds` (`SKILL.md:239`, "Landed pushes (== `max_rounds` at most …)"), INV-R1 `rereview_request_count <= max_rounds` (`SKILL.md:243`) and INV-R2 stay true with zero edits to `rebuild_state`'s push fold. B and C both have to filter merge pushes out of `push_count` (B:271, C:81) and invent a new counter and a new output field. That forks the meaning of `push_count` in every consumer and every old-log fixture.

2. **The merge is reviewed (J-66; A:247).** The merge commit is authored code: at Tier 2 it is model-written. A re-triggers reviewers through the existing `pending_retriggers` path (`SKILL.md:274`, `refs/review-retrigger.md:42`), and S5 attribution keys on the merge SHA, so a pre-merge review is never credited. B admits the alternative's residual: "Reviewers never see `M`", rated High likelihood (B:538, K8). C's rationale, that "both sides' commits are individually reviewed" (C:82), is false for exactly the case that matters: the resolution hunk exists on neither side.

3. **The edge is reachable from the state Wave 8 actually holds.** `refs/state-machine.md:146-148`: on Augment `clean` / `REPORT_ONLY` "the SKILL continues at `S2_CLASSIFY` without sending Augment `clean` to `transition()`". A's `C-ci` hook enters from `S2_CLASSIFY` (A:187), so the one new edge sits beside `(S2_CLASSIFY, "findings")` (`fsm.py:741-748`) with the same `should_halt_rounds` gate. That is one edge in a flat table, not a new state, and it follows the existing pattern exactly.

4. **Act early resolves the conflict before rounds run out.** Under B, a conflict detected at Wave 0 is only acted on at Wave 8a, and after `HALT_MAX_ROUNDS` Wave 8a is report-only (B:261, OQ-4 B:567). With `--max-rounds 2` and a review that keeps producing findings, `HALT_MAX_ROUNDS` is a common outcome. B then leaves that PR conflicted even though it knew about the conflict before the first poll: this is the exact failure issue #305 describes. A resolves at `C-initial` before any round is spent (A:186), so the review rounds run on a conflict-free head.

5. **Extension scaffolding is first-class (U-001, U-002; A:391-407).** `MechanicalRule(pattern, kind, sources, regenerate, check)` carries the source dependency (a generated output whose source is Tier 3 is Tier 3; empty sources are Tier 3, A:139) and the check argv. A test asserts that every shipped rule's program is already in `allowed-tools` (A:407, R-6; `SKILL.md:4` lists `Bash(uv *)`, `Bash(make *)`). B's `REGEN_RECIPES = {"uv.lock": "uv-lock"}` (B:178) splits a recipe between core (id) and ref (command), so one rule lives in two files and no test links them.

6. **One routing function (A:419).** `conflict_action(...)` is the single Wave C routing table, with an exhaustive table test (FR-C6, A:473). B spreads routing across `classify_conflicts` → `action`, `evaluate_sync_decision`, `sync_fail_state` and the Wave 8a gate table (B:256-262). C spreads it across `classify_conflict`, `evaluate_merge_push_decision` and prose.

7. **Create path made consistent with the skill's own rule (AD-7, A:53).** `SKILL.md:268` already says "a branch Wave 0 rebased needs a force-push, which this skill never does for you". The head branch is pushed before `gh pr create` can open the PR, so a rebase on the create path produces a divergent head. A removes the rebase. B and C keep a behaviour the skill's own message calls unpublishable (DA:215).

8. **Fewer installed primitives.** A adds 0 scripts and 2 refs. B adds 3 scripts and 1 ref, plus three install-list entries and a script test file (B:125, B:472). Every installed script is a fork-pin target (`--repo`), a force-push scan target (`test_static_grep.py:758-776`) and an install-list entry.

## Weaknesses Identified

### In Variant B

| # | Weakness | Evidence |
|---|---|---|
| B-W1 | A second push gate that must track INV-016 for ever. `evaluate_sync_decision` has 4 predicates and deliberately no `applied_edits` predicate (B:327-338). Any future hardening of `evaluate_push_decision` (`fsm.py:173-204`) must be duplicated by hand, and no test links the two. | B:108, B:338 |
| B-W2 | Push authority outside the round budget: Wave 8a acts "regardless of `round_counter`" (B:260), bounded only by `SYNC_CAP = 2`. That creates a second, independent budget the operator's `--max-rounds` does not control. | B:260, B:272 |
| B-W3 | Model-authored Tier 2 code reaches the PR with no bot review. B rates this High likelihood (K8, B:538) and leaves it as OQ-3 (B:566). | B:273, B:538 |
| B-W4 | A known conflict is left unresolved after `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE` (report-only, B:261). Detection is early, action is late, so the operator learns at Wave 0 and still ends unmergeable. | B:209, B:261, B:567 |
| B-W5 | Create-path rebase kept as "harmless" because "the branch is not yet a published PR head" (B:622). That contradicts `SKILL.md:268` (a rebased branch "needs a force-push"). Pins stay green, but the behaviour stays broken. | B:618-624; DA:215 |
| B-W6 | Tier 0 is not cheap: a fetch plus `merge-tree` plus `gh pr view` plus a capability probe at end of Wave 0, all again at Wave 8a (X-040). A's Tier 0 is one `gh pr view` when GitHub says `MERGEABLE` (A:145). | B:214-215, B:238-239; DA:122 |
| B-W7 | L1 at Wave 8a "proposes 'resolve these? y/n'" (B:250), an interactive prompt in a skill B itself says "has no override prompt" (R9, B:112). | B:112, B:250 |
| B-W8 | Its own uncertainty about L2: OQ-11 asks whether `S4'_HALT_BEFORE_PUSH` is reachable from the Wave 8 position at all, and plans to report `halt_before_push` from the SKILL without the FSM state if not (B:574). That is a status the FSM never entered. | B:574 |
| B-W9 | Parallel output contract: `sync_tier`, `sync_outcome`, `sync_push_count` (B:424), plus `sync_cycles` and `sync_push_count` folds in `rebuild_state` (B:421). Every Output Contract consumer must learn that `push_count` no longer counts every landed push. | B:421, B:424 |

### In Variant C

| # | Weakness | Evidence |
|---|---|---|
| C-W1 | Wave 0b cannot run as placed: it runs "before Wave 1", reads "the poll snapshot fields" and appends `conflict_detected`, but the output-dir, run-log and `poll-augment-review.sh` start in Wave 1 (`SKILL.md:269`). | C:74, C:83; X-034 |
| C-W2 | L1 contradicts its own classifier: classification runs "after a merge attempt stops" (C:50), yet L1 "the merge is NOT attempted" (C:80). So L1 has nothing to classify. | X-035 |
| C-W3 | Re-check point B cannot pass either parent check: once a merge lands on top of a fix commit, neither `merge_push_parent_ok` nor `push_parent_ok` holds. | C:76; X-037 |
| C-W4 | Staged-set assertion "staged-set == conflicted-path-set" (C:111) is impossible whenever the base changed any non-conflicted file, because git stages cleanly merged paths. | X-023 |
| C-W5 | L2 commits locally (C:80), breaking T-412 "commit never" (`refs/state-machine.md:102`, `SKILL.md:273`). | X-012 |
| C-W6 | Tier 1 holds judgment: `DU`/`UD` "where the edit is provably obsolete" and rename-vs-edit (C:54) need intent, not a rule. `.claude/` sync targets as Tier 1 regenerated output are gitignored and cannot be conflicted tracked paths (`.gitignore:127-128`). | X-015, X-033 |
| C-W7 | First-match order puts `AA` in both Tier 2 (rule 2) and Tier 1 (rule 3), so the Tier 1 `AA` claim is unreachable. | C:53-54; X-036 |
| C-W8 | Lockfile-only Tier 1 pushes with no VAL at L3 (C:112 FR-7.5). C's own OQ-3 calls it a hole (C:192). | C:112, C:192 |
| C-W9 | No Tier 2 size cap, and no test runs a real merge (C:155). The git mechanics that decide correctness are pinned only as prose. | C:155; X-017 |

## Concessions

1. **X-041 / A-006, operator recovery is wrong as written (A:174-175, A:217, A:327).** "Finish it by hand and commit … Then re-run with `--pr <N>`" fails head binding: `SKILL.md:268` requires local HEAD == `headRefOid`, and an unpushed local merge commit gives `pr_head_mismatch`. Fix within A: the message says "run `git commit --no-edit`, then `git push origin HEAD:<HEAD_BRANCH>` yourself (a normal fast-forward push), then re-run with `--pr <N>`; or `git merge --abort`, then re-run". B already says "commit yourself and push" (B:351).
2. **A conflict costs a round (R-4, A:614).** With the default `--max-rounds 2`, a conflicted PR keeps one review-fix round. This follows from keeping `push_count <= max_rounds` and re-reviewing the merge. I keep the design, but I accept that this cost is the main reason a reader would prefer B. If the merged design drops the re-trigger (X-003 to B or C), then the round tick (X-002) and the FSM edge (X-004) should go with it, because they are justified only together.
3. **`WHITESPACE_ONLY` at Tier 1 is unsafe (A:130, A:151).** I am raising this myself; the diff analysis does not flag it. `git diff --quiet --ignore-all-space` treats an indentation change as whitespace, and in Python or YAML indentation is meaning: it moves a line into or out of a block. `ruff format --check` can pass on both sides, so A would silently take the PR side and drop the base's semantic change. Remove class 8; such paths fall to `TEXT` (Tier 2). B's rejection (B:117) is right.
4. **A-002: the `evidence-validator` verdict A relies on does not exist.** A writes "an `unsupported` verdict" (A:164, A:484). The agent's verdicts are `verified` / `line-mismatch` / `file-missing` / `snippet-mismatch` (`src/superclaude/agents/evidence-validator.md:66`), and it "do[es] not re-grade confidence" (`:33`). It takes a `report_draft_path` (`:41`). Fix: render the records as a report draft with `file:line` plus a quoted snippet per evidence item, and escalate to Tier 3 on any citation that is not `verified`. Truth of the intent sentence stays unverified, so the honest claim is "grounding checked", not "intent supported". B and C carry the same overclaim (B:349, C:61).
5. **U-008: B's rollout is better.** Adopt B's P0-P3 gates and ship `--conflict-max-tier` with default 1, not 2. Keep A's flag name and its cap semantics (A:141).
6. **U-009: B's high-suspicion checklist belongs in A's Tier 2 step 2 (A:158)** as an escalation, not just evidence collection.
7. **X-023 / U-010: B's commit gate is stronger.** Adopt "staged ⊆ base-changed ∪ resolved" in place of A's negative `OPERATOR_PENDING` check (A:325). I also concede that this one gate earns a script (`finish-merge.sh`) with real-repo tests under a local bare origin (B:460). A's "no git in the suite" (A:550) is a choice, not a seed requirement. B's probe and evidence scripts I still reject (A:86), because they wrap inline calls without adding a decision.
8. **C's flag-matrix critique is fair.** If `--conflict-max-tier` stays, A's routing test must stay exhaustive (A:473). It already is, but the matrix cost is real.
9. **A's L1/L2 stop before any review at `C-initial` (A:216-217, OQ-1 A:639).** An L1 operator on a conflicted PR gets no review proposals. A defends this (stale findings, no CI), but B's "reviews continue at L1" (B:250) is the more useful default for a propose-only run. I would accept B's L1 behaviour (report the conflict plan, continue to review) and keep A's L2/L3.

## Shared Assumption Responses

| ID | Response | Reason |
|---|---|---|
| A-001 (branch rules accept a merge commit in the PR) | **QUALIFY** | Unstated in all three; A is no better here. Squash-merge accepts any PR history. A base that allows only rebase-merge, or a "require linear history" rule, may not accept a PR containing a merge commit (I could not verify GitHub's exact behaviour offline, so this is unverified). Cheapest mitigation inside A: after the push, A already re-reads `mergeable` (A:352). Add `mergeStateStatus == BLOCKED` with a reason line to the report and document the limitation, rather than reading branch-protection settings (needs admin scope). |
| A-002 (`evidence-validator` fits a resolution record and judges intent) | **REJECT as stated** | It verifies citation grounding only: four verdicts (`evidence-validator.md:66`), no re-grading (`:33`), input is a report draft (`:41`). The records must be rendered as a cited draft, and the spec must claim grounding, not intent truth (Concession 4). |
| A-003 (target project has VAL make targets and a real suite) | **QUALIFY** | The dependency already exists for fix cycles (`SKILL.md:279-291`); the conflict feature adds no new one. But A makes VG-2 mandatory at Tier 2 (A:314), so an absent or empty `make test` must fail closed: Tier 2 then routes to Tier 3, never to a green VAL. Add that row. |
| A-004 (`allowed-tools` permits the new commands) | **ACCEPT for A, QUALIFY for B and C** | A's commands are all `git`, `gh`, `uv`, `make` inline (`SKILL.md:4`), and A tests rule programs against that list (A:407). B's three scripts follow the existing script pattern, but each is a new install and permission surface. C's `GIT_EDITOR=true git commit` env prefix does not match `Bash(git *)` (X-039). |
| A-005 (conflict `cycle_id` cannot collide) | **QUALIFY** | No generator exists in the core: `fsm.py:235` only formats the key, and the SKILL mints ids (`refs/review-retrigger.md:67` reuses the dangling record's id on resume). Fix: a reserved prefix (`conflict-<n>`), a pure `is_conflict_cycle(cycle_id)` helper, and one test that the fix-cycle minting rule can never produce that prefix. |
| A-006 (re-run after operator finishes the merge passes head binding) | **ACCEPT the contradiction; concede** | Correctly flagged against A (Concession 1). The fix is text only: tell the operator to push the commit (fast-forward), or abort, before the re-run. |

## Point Preferences

| Point | Preferred variant | One-line reason |
|---|---|---|
| C-008 | A (B equal) | Read-only `merge-tree -z` probe before any merge lets L1 propose and Tier 3 halt with nothing to undo; C's classify-after-merge forces an abort path and breaks L1 (X-035). |
| C-009 | B | Narrowest tier definitions; A's whitespace class is unsafe (Concession 3) and C's Tier 1 holds judgment calls. |
| C-010 | B (membership) with A's `MechanicalRule` scaffolding | `uv.lock` stage `123` only is the safe v1 set; A's data shape with sources and check argv is the better extension point. |
| C-014 | A | Acting at `C-initial` resolves before rounds are spent and before review; B's act-late leaves a known conflict unresolved after `HALT_MAX_ROUNDS` (B:261). C's Wave 0b cannot run before the run-log exists. |
| C-016 | A | L2 ends at the real `S4'_HALT_BEFORE_PUSH` state with no commit (T-412, `state-machine.md:102`); B is unsure the state is reachable (OQ-11); C commits. |
| C-017 | A | After the push, reviewers re-review the merge SHA through S5a/S5; B and C publish unreviewed resolution code. |
| C-018 | A (coupled to C-019) | Spending a round keeps `push_count <= max_rounds` and INV-R1/R2 with no new counter; if C-019 goes to B/C, B's separate counter is then better. |
| C-019 | A | J-66: the resolution is authored code and must be reviewed; B rates the alternative's risk High (K8). |
| C-020 | A (coupled to C-019) | One edge in a flat table beside `findings` is cheaper than a second SKILL-owned push pipeline with its own gate and counters. |
| C-022 | A and B (tie) | Strict `[pre_push_sha, base_sha]` order: same ancestor-set safety as C, but it fails closed on a commit git did not produce and keeps `revert -m 1` and first-parent log meaningful. |
| C-033 | A | `SKILL.md:268` itself says a rebased branch needs a force-push; removing the rebase is the only consistent fix. |
| X-001 | A | Same as C-014. |
| X-002 | A (coupled) | No forked `push_count` meaning; the cost (one round) is stated and documented (A:243). |
| X-003 | A | Re-trigger through existing `pending_retriggers` with S5 attribution on the merge SHA; no new code (A:247). |
| X-004 | A (coupled) | A single edge reachable from the actual Wave 8 entry state (`state-machine.md:146-148`); needed only if X-003 stays A. |
| X-006 | B | Same strict rule as A, plus the disjointness property test (U-011) as the stronger pin. |
| X-012 | A | Matches T-412 through the existing FSM state; B equal in intent but unsure of reachability; C violates the contract. |
| X-013 | A | Same as C-033. |
| X-015 | B (A equal) | Tree conflicts need intent; B states the rule explicitly ("No tree conflict is Tier 1", B:177). |
| X-020 | A and B (tie) | Classify before touching the tree; B's script makes it executable in tests, A's inline form adds no install surface. |
| X-023 | B | Positive bound "staged ⊆ base-changed ∪ resolved" beats A's negative check; C's equality is impossible. |
| X-034 | A | A's Wave C runs after the Wave 1 arm, with run-log and output-dir present (A:182, A:186). |
| X-035 | A | Probe-before-merge gives L1 a real plan with a clean tree. |
| X-037 | A (B equal) | Neither A nor B re-checks inside the fix-push guard; conflicts are handled only at the two hook points, so the parent rules never collide. |
| U-008 | B | Phased dark launch with go/no-go gates; adopt it with A's flag at default 1. |
| U-009 | B | Escalate semantic shapes to Tier 3; fold into A's Tier 2 step 2. |
| A-001 | None (all equal; A's post-push re-read is the cheapest hook) | Unstated by all; document the limitation and report `BLOCKED` after push rather than reading branch protection. |
