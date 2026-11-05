# Round 1 advocate statement: Variant B (variant-2-sonnet-refactorer)

Persona: refactorer (technical debt, simplification, minimal-risk transformation). Citation forms: `A:NN`, `B:NN`, `C:NN` are line numbers in the variant files; repo paths are relative to the worktree root. Repo lines were re-read in this session (SKILL.md:4, :216, :267-277; fsm.py:582-600, :716-802, :1118-1124; agents/evidence-validator.md:1-60; tests/pr_submit/test_static_grep.py:630-678).

## 1. Position Summary

B is the lowest-regret path to the success criteria. It adds a sibling for every rule that gates a push (`merge_parent_ok`, `evaluate_sync_decision`, `build_sync_triad`) and edits none of the existing ones. `push_parent_ok` (`fsm.py:582-600`), `evaluate_push_decision` and `transition()` (`fsm.py:716-802`) are untouched, and the only `fsm.py` edit is the `--sync-tier` argument (B:18, :129). A sync cycle spends no review round, re-triggers no reviewer and adds no FSM edge. That is the shape the CI phase already uses (`SKILL.md:277`: "After an L3 CI push: do not call `retrigger-review.sh`, reply, or resolve; re-poll CI on the new `headRefOid`").

B's other distinguishing assets are the ones the refactor lens cares about most:

- It ships in four phases with go/no-go gates (B:514-525).
- A runtime dial (`--sync-tier 0|1|2`, default 1) rolls the feature back without a code change (B:97, :525).
- A regression test pins the byte-identical fragments of the pinned SKILL text (B:492-500).

B is not flawless. Section 5 concedes seven real defects, and section 4 names the best parts of A and C that the merged spec should take. My proposed synthesis:

- B's no-edge, own-counter, act-late shape, its phasing and its `finish-merge.sh` guard.
- A's captured-fixture `parse_stage_records`, its `MechanicalRule` extension table and its `pr_conflicting` skip of the CI wait.
- A's removal of the create-path rebase, shipped as a separate precursor change.
- A reviewer re-trigger for Tier 2 only, added when Tier 2 becomes default-on.

## 2. Steelman of the opposing variants

### 2.1 Variant A (opus-architect), strongest form

A's argument is not "more machinery is better". It is that reusing the FSM's own accounting keeps every invariant true with no new bookkeeping (A:45, AD-3).

- A conflict cycle rides the existing `findings` edge shape. It ticks `round_counter` on the INV-001 edge, re-triggers through S5a and lets `push_count <= max_rounds` (`SKILL.md:239`) and INV-R1/R2 hold unedited.
- A parallel counter family (`sync_push_count`, `SYNC_CAP`, `sync_cycles`) is the kind of side-channel accounting that every later change must remember. A rejects it explicitly (A:45).
- A's second argument is J-66: the merge is authored code and should be reviewed like any fix. B's own K8 admits that "reviewers never see `M`" (B:538).
- Acting before the first review (`C-initial`, A:186) means reviewers see the head that will actually merge. CI cannot start on a conflicted PR anyway.
- A diagnoses the create-path contradiction correctly. The rebase cannot be published without a force-push, and `SKILL.md:268` says so itself: "a branch Wave 0 rebased needs a force-push, which this skill never does for you" (A:27, :53).
- A has the best test story for the git-facing parser. `parse_stage_records` is tested against a captured real `merge-tree -z` fixture, so the suite never runs git (A:557, U-005).
- A has the best extension mechanism. `MechanicalRule` carries `sources`, `regenerate` and `check` argv, with a generated-dependency rule and source-before-output ordering (A:391-418, U-001).
- A has one operational idea B lacks. When no merge is pushed at `C-ci`, it skips the CI wait with reason `pr_conflicting` instead of polling to `--timeout` (A:220, U-004).
- A has the most disciplined decision record: AD-1..AD-10, each with rejected alternatives, and a traceability table.

### 2.2 Variant C (haiku-qa), strongest form

C's argument is that the smallest change that works wins, and that the pinned test surface is the real constraint.

- C adds no FSM edge, no flag and a minimal core module (C:28, :44, :46).
- It makes `push_kind` default to `"fix"` so every existing payload stays byte-identical (C:83).
- It keeps the merge push out of `push_count` via a `rebuild_state` filter, preserving INV-R2 (C:81).
- It has the only explicit regression-risk register tied to the pins (R1..R14, C:157-174).
- It carries two small practical items: the "grep tests/ for `== 41`" PR checklist step (C:161, U-024), and treating `BLOCKED` as Tier 0 (C:55, U-023).
- It puts the marker scan on the conflicted-path set only (C:109), so this repo's fixture files containing marker literals do not block a merge (C:169, R9).
- It insists on settling the create-path text before building tiers.
- It states honestly what it does not test (C:153-155).
- Its Definitions section fixes the vocabulary (C:16-24).
- Its "let git refuse a dirty merge" preflight is the least code of the three.

## 3. Strengths claimed for B (with evidence)

| # | Strength | Evidence |
|---|---|---|
| S1 | **Zero edits to push, gate or transition code.** Four debt hot spots (`push_parent_ok`, `evaluate_push_decision`, the push triad and recovery, the 41-event enum) each get a sibling or an additive marker, never a loosening. | B:27-36 debt table; B:129 net-effect table. Repo: `push_parent_ok` fails closed on anything but one parent (`fsm.py:593-600`); its test is pinned (`test_pre_pr_checks.py:216-222`). |
| S2 | **Disjointness by construction.** `merge_parent_ok` needs exactly 2 parents and `push_parent_ok` exactly 1. B requires a property test that each rejects every input the other accepts, so a mis-routed commit cannot pass the wrong check. | B:313-325, U-011. Neither A nor C states this property. |
| S3 | **No round, no re-trigger, no FSM edge.** Mirrors the CI phase (`SKILL.md:277`). A lockfile conflict does not consume a review round, post reviewer comments or wait on S5. `transition()` stays flat and its unknown-edge `return state` (`fsm.py:801-802`) is never relied on. | B:22, :106, :270-273. Counter-evidence against A: A:243 and A:613 (R-4) concede `--max-rounds 2` leaves one fix round after a conflict. |
| S4 | **Strict, small tier ladder.** 13 first-match rules, fail-closed `halt:unknown_shape`, Tier 1 only for `uv.lock` with stage set `123`. No tree conflict is ever Tier 1 because both sides changed the path. | B:149-181. |
| S5 | **Rollout that can be undone.** P0 is read-only (a fetch only). P1 ships Tier 1 and the publish machinery. P2 ships Tier 2 dark behind `--sync-tier` (default 1). P3 is late re-sync. Each phase has a go/no-go gate and rollback is a flag or a revert. | B:514-525, U-008. Neither A nor C has any rollout gate. |
| S6 | **Empirically verified git behaviour, not memory.** `merge-tree --write-tree` exit codes and stage sets, "cannot do a partial commit during a merge", and the `numstat` binary signature were checked in a scratch repo. These drove the exact-path-staging and own-commit-step design. | B:72-76. |
| S7 | **A correct pre-commit staging guard.** `finish-merge.sh` requires staged paths ⊆ (files changed on the base side since the merge-base) ∪ (resolved paths). Git stages cleanly merged base paths, so C's "staged == conflicted set" is unsatisfiable whenever the base touched any other file. A's guard is weaker (clean-tree preflight plus disjointness from `OPERATOR_PENDING`). | B:352, U-010. Contrast C:111 (X-023). |
| S8 | **Marker rule that survives this repo.** It counts marker lines against the stage-1 blob, so only introduced markers fail. A's per-side verbatim allowance is equivalent. C's "ANY hit blocks" blocks legitimate documentation text. | B:352, :541 (K11); contrast C:109. |
| S9 | **High-suspicion checklist before resolving.** A signature, schema, dependency, constant or public-API change on one side while the other adds callers makes the file `semantic` and the cycle Tier 3. This is the cheapest guard on the riskiest step. | B:193-195, U-009. |
| S10 | **Pin-aware editing.** A byte-identical fragment list (8.4) and a pinned-count table (8.3) make the "additive edits only" claim testable. | B:476-500. |
| S11 | **Correct operator recovery text.** B's L2 and abort messages say to commit **and push** (B:351). Head binding requires local HEAD == `headRefOid` (`SKILL.md:268`), so an unpushed local merge halts `pr_head_mismatch` (A-006, X-041). | B:351 vs A:174-175, :217. |

## 4. Weaknesses identified in A and C (with evidence)

### 4.1 Variant A

| # | Weakness | Evidence |
|---|---|---|
| WA1 | **A mechanical conflict pays for a review round.** A lockfile-only merge ticks `round_counter`, posts two re-trigger comments (`auggie review`, `@codex review`) and waits in S5 up to `--timeout`. A itself says the goal is that a lockfile conflict must not pay the semantic-conflict cost (A:35). With the budget spent, FR-C23 sends a Tier 1 conflict to `HALT_MAX_ROUNDS` and leaves the PR unmergeable, although the fix needs no review round. | A:236-243, :523 (FR-C23), :613 (R-4). |
| WA2 | **L1/L2 runs stop on any conflicted PR before a single review poll.** Today a conflicted PR at L1/L2 still produces review findings. Under A it ends at `proposed` or `halt_before_push` with no review output. That is a behaviour regression A made by design and parked as OQ-1. | A:216-217, :639 (OQ-1). |
| WA3 | **Re-triggering at `C-initial` is noisy.** A says "every configured reviewer" is re-triggered because none is yet recorded absent, on a PR the bots were just triggered on at creation. A's own R-5 concedes a wasted pre-merge review. | A:247, :614. |
| WA4 | **Bundles an orthogonal behaviour change.** AD-7 removes the create-path rebase and rewrites the pin at `test_static_grep.py:654-661` (A:53, :567). The diagnosis is right (see Concessions) but the vehicle is wrong: it couples a pin rewrite to a feature whose only mandate is conflict resolution. |
| WA5 | **Operator recovery is a dead end.** "Finish it by hand and commit ... Then re-run with `--pr <N>`" omits the push. Head binding fails on an unpushed merge commit (`SKILL.md:268`: local HEAD must equal `headRefOid`). | A:174-175, :217; X-041/A-006. |
| WA6 | **`WHITESPACE_ONLY` as Tier 1 is not safe.** The test is `git diff --quiet --ignore-all-space <oid2> <oid3>` (A:105). `-w` ignores all whitespace, including indentation. That is semantic in Python, YAML and Makefiles, and in Python the side is picked by `uv run ruff format --check`, which cannot tell a moved block from a reformatted one (A:151). This is my reasoning about git's documented `-w` semantics, not a repo-verified fact. B rejects R-161 for this reason: whitespace-only conflicts fall to Tier 2 (B:118, X-016). |
| WA7 | **Stretches INV-016 predicate 5.** `evaluate_push_decision(applied_edits = resolved path count)` makes "grounded finding edits" mean "files merged". The audit record then says something untrue. | A:337, vs B:108 (R5). |
| WA8 | **Wider FSM and record footprint.** One new edge in `transition()`, `build_push_triad` kwargs, `SkillArgs`, `needs_rebase` docstring, `run_log.py` fold and `recovery.py` keys (A:594). Each touched function needs its gate-table or record-shape test row extended (A:575-577). |

### 4.2 Variant C

| # | Weakness | Evidence |
|---|---|---|
| WC1 | **Wave 0b cannot run where C puts it.** It reads poll-snapshot fields and appends `conflict_detected`, but the output-dir, run-log and poll loop start in Wave 1 (`SKILL.md:269`). | C:74, :83 (X-034, High). |
| WC2 | **L1 "propose, no merge" contradicts classification "after a merge attempt stops".** With no merge there is no `git status --short` code to classify. | C:50 vs C:80 (X-035, High). |
| WC3 | **L2 commits locally.** The L2 contract is "NO commit, NO push, NO reply" (`SKILL.md:273`; `state-machine.md` T-412 "commit never"). C breaks it (C:80, X-012). |
| WC4 | **Re-check point B cannot satisfy its own parent checks.** Merging after the fix commit exists makes the merge's first parent the fix commit, not `pre_push_sha`, so `merge_push_parent_ok` fails. The fix commit's parent is the old head, so `push_parent_ok(.., merge_sha)` fails too. | C:76, :93 (X-037, High). |
| WC5 | **Order-independent parent rule.** `{p1, p2} == {pre_push_sha, base_sha}` accepts `[base, head]` (C:93, :110 "order swapped OK"). That flips `git log --first-parent` and the meaning of `git revert -m 1 M`. Both A (A:344) and B (B:319-322) require the order. |
| WC6 | **Wrong safety claim.** "Pushing `merge_sha` publishes exactly one commit" (C:93) contradicts the `push_parent_ok` docstring: a fast-forward "publishes every commit between the two" (`fsm.py:585-588`). The merge also publishes the base-side ancestors, which is safe only because of a base-ancestry check C does not have (A:335, B:353). |
| WC7 | **Tree conflicts as Tier 1.** `AA`, provably obsolete `DU`/`UD` and rename-vs-edit all need a judgment ("deletion wins only with shown evidence", C:54), which is not mechanical. The tier rules also overlap on `AA` (X-036). C pays no evidence step there. | C:53-54, X-015/X-036. |
| WC8 | **Weaker gates on the risky path.** A Tier 1 lockfile-only merge skips VAL (C:112 FR-7.5). The "3-predicate" decision accepts "validated-or-VAL-skipped", which weakens INV-016 predicate 2 for a commit pushed at L3. The staged-set assertion is impossible (X-023). |
| WC9 | **No executable test of any git step.** The partial-commit refusal, `MERGE_HEAD` detection and the abort path are "pinned only as PROSE" (C:155). The riskiest mutations are covered by the weakest tests. |
| WC10 | **Fixes a payload while widening it.** It appends fields to `poll-augment-review.sh` (C:34), which touches `test_cosmos_poll.py` (A:87 notes the same). B's only poll change is an append to the CI poll, and only in P3 (B:430). |
| WC11 | **One wrong factual premise.** `.claude/` sync targets are listed as Tier 1 regenerable output (C:54), but they are gitignored apart from `settings.json` (diff-analysis spot-check, X-033), so they can never be conflicted tracked paths. |

## 5. Concessions (genuine weaknesses of B)

1. **X-013, create-path rebase (the flagged point): B's rationale is wrong.** B's Appendix A keeps both the create-path rebase and the HALT because "the branch is not yet a published PR head, so rewriting it locally is harmless" (B:622). `SKILL.md:268` itself says "a branch Wave 0 rebased needs a force-push, which this skill never does for you", and head binding requires local HEAD == `headRefOid`. B's pin-preserving clarification is safe, but it keeps a contradiction it cannot defend. A's removal (A:53) is the better substance. The refactor-correct delivery is a separate precursor change that touches `test_static_grep.py:654-661` on its own, not bundled into the conflict feature.
2. **Overclaim about the CI blind spot.** B says P0 "already fixes the 'CI polls forever on a conflicted PR' blind spot" (B:23). Nowhere does B skip the CI wait when Wave 8a is report-only (L1, a wait-only path, or `tier_above_cap` at the default `--sync-tier 1`). A grep of B for "skip the CI" and `pr_conflicting` finds nothing. In those cases the CI wait still polls to `--timeout`. A's U-004 (A:220) is the missing piece, and I adopt it.
3. **K8: reviewers never see `M`** (B:538, OQ-3). That is acceptable for Tier 1, which is mechanical and checked by `uv lock --check`. It is a real gap for Tier 2 at L3. The mitigation is only that Tier 2 ships dark. The re-trigger for Tier 2 (reusing S5a, excluded from `rereview_request_count`) must be designed before the default flips.
4. **Duplicated triad builder.** `build_sync_triad` parallels `build_push_triad` (B:88). That is a drift risk A avoids with additive `push_kind`/`base_sha` kwargs (A:594). I would take A's additive-field mechanism and keep B's sibling decision and parent functions.
5. **Three bash scripts are the hardest-to-test part.** B's tests depend on a local bare repo and skip when `merge-tree --write-tree` is unavailable (B:460), so on some runners they silently do not run. A's parser plus captured fixture is more hermetic. The merged design should move stage parsing into the core as `parse_stage_records`, leaving `probe-merge.sh` as a thin emitter of fetch, `foreign_op`, `index_clean` and the raw `-z` listing.
6. **B creates new pin debt.** The `SKILL.md <= 346` line-count assertion (NFR-9, B:444) is a brittle test that breaks on the next unrelated edit. Replace it with the existing one-python-block pins and the byte-identical fragment test.
7. **Cost claim and default.** "Tier 0 adds at most two read-only calls" (NFR-4, B:439) is understated: the probe runs at the end of Wave 0 and again at Wave 8a, each with `gh pr view`, a capability probe, a fetch and `merge-tree` (X-040). Also, default `--sync-tier 1` means the seed's L3 text-conflict success criterion is not met by default, which is a deliberate trade-off I accept but state plainly.
8. **L2 FSM fidelity (minor).** A routes L2 through existing states to `S4'_HALT_BEFORE_PUSH` (A:209, :217). `fsm.py:1118-1124` shows S4' reached when the push decision is unauthorised at `ordinal < 3`, which a reused `evaluate_push_decision` produces naturally. B's OQ-11 (B:574) leaves open whether the L2 halt is reachable from Wave 8 without a new event.

## 6. Responses to the shared assumptions

| ID | Response | Reason |
|---|---|---|
| A-001 branch rules accept a PR with a merge commit | **QUALIFY** | Holds for this fork's flow, but it is an unverified precondition of the success criterion "PR mergeable". Make it a run-time observation, not a design belief. Repo-level merge settings or required-linear-history rules decide whether the PR can land; the exact API field names must be verified before implementation (not verified here). B's P1 gate already requires a real PR to read `MERGEABLE` after the push (B:506, :521); add "and a merge commit is accepted by the base-branch rules" to that gate. A PR that is still `CONFLICTING` after a correct push is reported, not retried (B:532, K2). |
| A-002 `evidence-validator` fits a resolution record | **QUALIFY** | Its contract is a draft report with an evidence section; it re-reads file:line citations and returns survived or dropped items. It explicitly does "not improve the report's prose, propose new evidence, re-grade" (`agents/evidence-validator.md:11-35`). That makes it a citation-existence and quote-match gate, not a judge of whether "ours_intent" is a correct reading. B's K1 residual (shared model bias, B:531) is the honest framing. The merged spec should say so, and A and B should write `resolution.md` with an Evidence section so the contract fits. C's claim that it checks "the stated intents must ground in the actual sides" (C:35) overclaims. |
| A-003 target project has `make test`, `make lint`, `make verify-sync` | **QUALIFY** | VAL already assumes these for every fix cycle (`SKILL.md:279-291`), so this adds no new exposure. But a conflict resolution leans on VAL as its only semantic net. Add a fail-closed rule: if the VG-2 target is absent, cap the cycle at Tier 1. Default `--sync-tier 1` makes this the default anyway. |
| A-004 `allowed-tools` permits the new commands and scripts | **QUALIFY** | `SKILL.md:4` allows `Bash(gh *)`, `Bash(git *)`, `Bash(uv *)`, `Bash(make *)`, `Bash(jq *)`. Inline `git merge`, `git merge-tree`, `git rm`, `git show :n:`, `uv lock` match. Env-prefixed commands such as C's `GIT_EDITOR=true git commit` (C:98) may not match the prefix (X-039). New scripts are in the same position as the existing four (precedent); the git calls inside a script are not subject to prefix matching. B should keep every command in the ref prefix-clean, and A's allowed-tools test for rule programs (A:407) is worth adopting. |
| A-005 conflict `cycle_id` cannot collide with existing ids | **ACCEPT, with a cheap guard** | A grep of `src/superclaude/pr_submit` finds `cycle_id` only read in `run_log.py:202` and `recovery.py:136`; no Python generator exists, so ids are SKILL-chosen. A distinct `sync-<n>` prefix plus B's FR-15 ("a cycle id prefixed `sync-` is never reused for a fix push", B:420) removes the risk. |
| A-006 a re-run with `--pr <N>` after the operator merges passes head binding | **REJECT** | `SKILL.md:268` requires `pr_head_ok(local_branch, local_sha, headRefName, headRefOid, ...)`, i.e. local HEAD == `headRefOid`. An unpushed local merge commit fails with `pr_head_mismatch`. Every HALT or L2 message must say "commit **and push**, or abort" (B:351 does; A:174-175 and :217 do not). |

## 7. Point preferences (High-severity diff points)

| Point | Preferred variant | One-line reason |
|---|---|---|
| C-008 classification input/timing | B | Read-only `merge-tree` probe like A, bundled with `foreign_op` and `index_clean` and empirically verified (B:72-76, :221-243); C classifies only after a merge starts (C:50). |
| C-009 tier definitions | B | Tier 1 = regenerate-only, tree conflicts always Tier 2; C puts judgment-bearing tree conflicts in Tier 1 (C:54) and A adds whitespace (A:130). |
| C-010 Tier 1 membership | B | `uv.lock` with stage set `123` only (B:157); borrow A's `MechanicalRule` table as the extension shape, ship one row. |
| C-014 placement / hook points | B | Detect read-only early, act at one late call site with no run-log or armed-FSM dependency (B:199-217); A's `C-initial` costs a round and a re-trigger, and C's Wave 0b is unrunnable (X-034). |
| C-016 L2 behaviour | A | Same no-commit semantics as B, routed through the existing `S4'_HALT_BEFORE_PUSH` (A:209, :217; `fsm.py:1118-1124`), which closes B's OQ-11. |
| C-017 L3 after push | B | Re-poll CI on the new head, no re-trigger (`SKILL.md:277` precedent). Add a Tier 2 reviewer re-trigger as a follow-up before the Tier 2 default flips. |
| C-018 round accounting | B | A mechanical conflict must not consume a review round (A:243, :613 concede the cost); a separate fold keeps `push_count` meaning (B:96, :271). |
| C-019 reviewer re-trigger | B | Matches the CI-phase push and avoids WA3 noise; concede K8 for Tier 2. |
| C-020 FSM integration | B | No state, no edge; `transition()` and its tests stay untouched (B:106). A's edge buys nothing once the round and re-trigger are dropped. |
| C-022 merge-parent rule | B | Strict `[pre_push_sha, base_sha]` order like A, plus the disjointness property test against `push_parent_ok` (B:313-325); C's order-independent set (C:93) fails. |
| C-033 create-path rebase vs HALT | A | Removing the rebase is correct (`SKILL.md:268`); ship it as a separate precursor change, not inside this feature (concession 1). |
| X-001 when handling acts | B | One late call site (Wave 8a), detection earlier but read-only; A acts before reviews, C acts in an unrunnable wave. |
| X-002 conflict cycle consumes a round | B | No round; see C-018. |
| X-003 reviewers re-triggered after merge | B | No for Tier 1 (mechanical); qualified for Tier 2 (K8). |
| X-004 FSM change | B | No new edge. |
| X-006 parent order | B | Order enforced, with a stated disjointness property; A equally correct, C wrong. |
| X-012 L2 semantics | A | Uncommitted merge in progress via the existing S4' state; B agrees on semantics; C violates `SKILL.md:273`. |
| X-013 create-path rebase vs HALT | A | See C-033; B's "unpublished branch" rationale is contradicted by `SKILL.md:268`. |
| X-015 tier of tree conflicts | B | "No tree conflict is Tier 1" (B:177) with Tier 2 kind labels; A agrees on the tier, C is wrong. |
| X-020 classify before or after the merge | B | Probe before any mutation (B:243); C classifies after the merge attempt. |
| X-023 staged-set check before the merge commit | B | Staged ⊆ base-changed ∪ resolved (B:352) is satisfiable; C's equality is impossible, A's is weaker. |
| X-034 C: Wave 0b sequencing | B | B's early step is read-only and event-free, so it needs no run-log (the run-log starts in Wave 1, `SKILL.md:269`); A's `C-initial` also works but costs a round. |
| X-035 C: L1 without a merge | B | Classification comes from the probe, so L1 can report without any merge (B:250). |
| X-037 C: re-check point B | B | A sync cycle never shares a push with a fix cycle (B:22), so the parent-check composition problem cannot arise. |
| U-008 phased rollout with gates | B | Only B has gates and a flag-level rollback; adopt it for the merged spec. |
| U-009 high-suspicion checklist | B | Marks a semantic change `kind: semantic` and the cycle Tier 3 before any resolution is written (B:193-195). |
| A-001 merge commit acceptable to branch rules | B | B's P1 gate requires a real PR to read `MERGEABLE` after the push; extend it to check that a merge commit is accepted. |
