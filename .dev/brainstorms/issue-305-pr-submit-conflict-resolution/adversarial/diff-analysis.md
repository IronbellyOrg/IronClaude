# Diff Analysis: spec Comparison

## Metadata

- Generated: 2026-11-04T13:35:39Z
- Variants compared: 3 (A = `variant-1-opus-architect.md`, B = `variant-2-sonnet-refactorer.md`, C = `variant-3-haiku-qa.md`); source `../seed-brief.md`
- Total differences found: 124 (structural 15 + content 39 + contradictions 41 + unique 24 + promoted shared assumptions 5)
- Categories: structural (15), content (39), contradictions (41), unique (24), shared assumptions (15 enumerated: UNSTATED 5 promoted, STATED 9, CONTRADICTED 1)
- Citation form: `A:NN` = line NN of variant A (likewise B, C); repo paths are relative to the worktree root.

## Structural Differences

Variant A = `variant-1-opus-architect.md` (693 lines). Variant B = `variant-2-sonnet-refactorer.md` (634 lines). Variant C = `variant-3-haiku-qa.md` (194 lines). Heading counts exclude the `## <path>` line inside a fenced block in B (B:370), which is not a real heading.

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Document size | 693 lines, about 76 KB | 634 lines, about 85 KB (densest: long tables) | 194 lines, about 46 KB (long single-paragraph bullets) | Medium |
| S-002 | Front matter / status block | Plain status paragraph under H1 (A:3) | YAML front matter with `variant`, `persona`, `status`, `sources` (B:1-10) | Three plain header lines (C:3-6), status "COMPLETE" | Low |
| S-003 | Heading count per level (max depth 3 in all) | H1 1, H2 16, H3 28 (45 total) | H1 1, H2 13, H3 39 (53 total) | H1 1, H2 12, H3 10 (23 total) | Medium |
| S-004 | H2 section order | Summary, Current gap, Architectural decisions, Mechanism, Tier, Placement, Publishing, Core API, FR, NFR, Tests, File inventory, Risks, Out of scope, Open questions, Traceability | Summary/decision record, Grounding, Mechanism, Tier, Placement, Publishing, Requirements (FR+NFR), Tests, Phasing, Risks, Out of scope, Open questions, Index | Purpose, Definitions, Mechanism, Tier, Placement, Publication, FR, NFR, Tests, Risk register, Out of scope, Open questions | Low |
| S-005 | Decision record form | Numbered AD-1..AD-10 with rejected alternatives (A:37-59) | Six-line recommendation plus a "debt hot spot" table (B:16-36) | No decision section; decisions inline as "Seed Open Question N answered" (C:80-82) | Medium |
| S-006 | Grounding / current behaviour | "Current behaviour and the gap" fact table with citations (A:20-35) | "Grounding" G1-G19 plus empirically verified git behaviours (B:46-78) | No grounding section; citations inline; a Definitions section instead (C:16-24) | Medium |
| S-007 | Requirement format | FR-C1..FR-C23 as bold paragraphs, each with an AC bullet naming a test; NFR-1..10 | FR-1..FR-25 table with priority (M/S) and AC column; NFR-1..13 table | FR-1..FR-11 bullets with sub-numbered clauses (FR-7.1..7.6) and "Pinned:" test; NFR-1..8 bullets | Medium |
| S-008 | Core API presentation | Dedicated section 7: data types, function contract table, record schema, per-file change table | API listed inside mechanism table A1 (B:88) and FRs; no dedicated section | Helper names scattered across FRs and test plan; no dedicated section | Medium |
| S-009 | Ordinal behaviour presentation | Matrix ordinal x tier x cap (A:213-218) | Table ordinal x (Wave 0 end, Wave 8a) (B:247-252) | Prose bullet (C:80) plus FR-7.1 | Low |
| S-010 | Rollout / phasing section | None | Section 9: P0-P3 with go/no-go gates (B:514-525) | None | Medium |
| S-011 | Research traceability | Section 15 table, item -> landing section (A:647-693) | Section 13.1 index table (B:581-603) | Inline research ids only | Low |
| S-012 | File inventory | Section 11 table (A:587-604) | Section 3.3 net-effect table plus 13.2 file list (B:119-132, :605-616) | None; files only named inside FRs and test plan | Low |
| S-013 | Appendices | None | Appendix A (create-path) and B (script exit contract) nested as H3 under section 13 "Index" (B:618-634) | None | Low |
| S-014 | Risk register format | R-1..R-11, combined likelihood/impact column (A:606-620) | K1..K13 with a "Residual" column (B:527-543) | R1..R14 regression-focused, separate likelihood and impact columns (C:157-174) | Low |
| S-015 | Test plan structure | New / changed / manual (A:548-585) | New files / changed tests / pins / byte-identical fragments / manual / run order (B:450-512) | New unit tests / existing-file edits / "deliberately no test" (C:129-155) | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Overall mechanism mix | 1 core module, 2 refs, 0 scripts, 0 agents, 0 templates, 1 FSM edge, 2 events, 1 flag (A:16-18) | 1 core module, 1 ref, 3 scripts, 0 agents, 0 templates, 0 FSM edges, 2 events, 1 flag (B:18) | 1 core module, 1 ref, 1 new script + 1 extended script, 0 agents, 0 templates, 0 FSM edges, 3 events, 0 flags (C:28) | Medium |
| C-002 | Core module name and API breadth | `conflicts.py`: 12 public functions incl. `mergeability`, `parse_stage_records`, `classify_run`, `conflict_action`, `merge_parent_ok`, `conflict_resume_point`, `merge_commit_message` (A:409-425) | `conflicts.py`: `classify_conflicts`, `merge_parent_ok`, `evaluate_sync_decision`, `sync_fail_state`, `build_sync_triad`, `resolution_record_ok`, `mergeability_hint` (B:88) | `conflict.py` (singular): `classify_conflict`, `merge_push_parent_ok`, `has_conflict_markers`, `resolution_record_complete`, `evaluate_merge_push_decision` (C:32, :133-140) | Medium |
| C-003 | Ref layout | Two refs split by tier: `conflict-mechanical.md` (Tier 1+), `conflict-intent.md` (Tier 2 only) (A:72-73) | One ref `conflict-sync.md`, loaded only when probe is not Tier 0 (B:89, :219) | One ref `conflict-resolution.md`, loaded by Wave 0b and re-check points (C:33) | Low |
| C-004 | Scripts | None; rejects a mergeability script and rejects extending `poll-augment-review.sh` for this release (A:86-87) | Adds `probe-merge.sh`, `collect-conflict-evidence.sh`, `finish-merge.sh`; P3 appends `merge_state` to `poll-ci-checks.sh` (B:90-92, :430) | Adds `merge-status.sh`; appends `mergeable,mergeStateStatus` to `poll-augment-review.sh` (C:34) | Medium |
| C-005 | Agent strategy | Reuse `evidence-validator`, one batch per Tier 2 cycle; reject new resolver agent and troubleshoot routing (A:77, :84-85) | Same reuse; one spawn per Tier 2 cycle with one revision pass (B:94, :349) | Same reuse; one batch for Tier 2 (C:35) | Low |
| C-006 | Templates | None; record schema in ref, render by pure function (A:88) | None; record format inline in ref (B:105) | None; templates rejected (C:41) | Low |
| C-007 | Conflict signal and its authority | GitHub `mergeable`/`mergeStateStatus` first; `MERGEABLE` ends with no fetch or probe; `CONFLICTING`/persistent `UNKNOWN` triggers local probe (A:198-203) | Local `git merge-tree` is the truth; GitHub fields advisory only, `null` on failure, disagreement reported as `github_disagrees` (B:242) | GitHub fields from the poll snapshot or one `gh pr view`; local merge stop also counts (C:18, :74) | Medium |
| C-008 | Classification input and timing | Read-only `git merge-tree --write-tree -z` probe before any merge; stage set -> tree code (A:51, :99-117) | Same read-only probe inside `probe-merge.sh` emitting JSON stage strings (B:221-243) | Classify after a merge attempt stops, from `git status --short` codes via `merge-status.sh` (C:50) | High |
| C-009 | Tier definitions | 0 none/behind; 1 lockfile/generated/whitespace; 2 text and tree conflicts by intent; 3 human (A:9-14) | 0 none/behind; 1 regenerate-only (`uv.lock`); 2 text and tree by intent; 3 everything else (B:19) | 0 none (incl. `BLOCKED`); 1 lockfile, generated, snapshot, whitespace, AND obvious tree conflicts; 2 human-authored text; 3 submodule/binary/migration/unstatable (C:52-55) | High |
| C-010 | Tier 1 membership | `LOCKFILE` (rule table, `uv.lock` only), `GENERATED` (rule with named sources), `WHITESPACE_ONLY` (A:128-130) | `regen:uv-lock` only, and only for stage set `123` (B:157) | `uv.lock`, generated output incl. `.claude/` sync targets, snapshots (R-60), whitespace/line-ending, `AA`, provably obsolete `DU`/`UD`, rename-vs-edit (C:54) | High |
| C-011 | Tier 3 triggers | unreadable, submodule, symlink, human paths (migrations, `.claude/settings.json`, `.github/workflows/*`), binary, generated with Tier 3 or empty sources, >10 Tier 2 paths, unstatable intent, `unsupported` verdict (A:123-141) | submodule, symlink, mode change, protected globs (adds `.github/actions/**`, `settings.local.json`), migrations, binary, lockfile without recipe, generated without recipe, unknown shape, >8 text paths, `semantic` kind (B:151-173, :195) | submodule, binary, migrations (adds `prisma/migrations/`), unstatable intent, Tier 2 VAL failure, unknown code/mode (C:52, :107) | Medium |
| C-012 | Tier 2 procedure and record | Three stage blobs to files, R-112 evidence, record with `ours_intent`, `theirs_intent`, `after`, `dropped`, `evidence`; `resolution_record_errors` (A:155-164, :427-441) | `collect-conflict-evidence.sh`; `resolution.md` with `kind`, `root_cause`, intents, `resolution`, `behavior_after`, `dropped`, `evidence`; high-suspicion checklist (B:193-195, :365-383) | Stage reads, evidence pass, intents, behaviour sentence, dropped behaviour, validator verdict; `resolution_record_complete` (C:61, :114) | Medium |
| C-013 | Tier 2 size cap | `MAX_INTENT_FILES = 10` (A:140) | `TIER2_MAX_FILES = 8` (B:171) | No cap | Medium |
| C-014 | Placement / hook points | Wave C at `C-initial` (inside Wave 1 after arm, before first poll) and `C-ci` (Wave 8 before CI arm) (A:184-187) | Read-only detect at end of Wave 0; act in new Wave 8a after reviews settle, before CI wait; P3 late re-sync (B:199-217) | Wave 0b before Wave 1; re-check A at Wave 8 entry; re-check B inside the pre-push head guard (C:72-76) | High |
| C-015 | L1 behaviour | `PROPOSED`; the run stops, no review poll (A:216, OQ-1) | Report at Wave 0; reviews proceed; propose at Wave 8a (B:250) | Propose the plan; merge not attempted; continuation unspecified (C:80) | Medium |
| C-016 | L2 behaviour | Resolve, stage, VAL; halt at `S4'_HALT_BEFORE_PUSH` with `MERGE_HEAD` present, no commit (A:57, :217) | Resolve, VAL; stop with merge in progress, uncommitted (B:251) | Resolve and commit the merge locally; nothing pushed; S4' not used (C:80) | High |
| C-017 | L3 behaviour after push | S6/RESOLVING with zero threads, S5a re-trigger, S5 wait (first review wait) (A:218) | Continue to CI wait on new head; no re-trigger (B:252, :356) | Continue to Wave 1 reviews or Wave 8 re-poll on new head (C:100) | High |
| C-018 | Round accounting | Conflict cycle ticks `round_counter` on INV-001 edge; `push_count` +1 (A:234-241) | No round; separate `sync_push_count`; `SYNC_CAP = 2` (B:22, :270-272) | No round; separate `merge_push_count`, capped at 1 (C:81) | High |
| C-019 | Reviewer re-trigger | Yes, existing S5a `pending_retriggers` path (A:245-247) | No (mirrors CI-phase push) (B:273) | No (C:82) | High |
| C-020 | FSM integration | One new edge `(S2_CLASSIFY, "conflicting")` reusing round gate and G-edit (A:224-232) | No new state or edge; SKILL-owned phase like CI (B:106) | No new state or edge; SKILL-owned (C:44, NFR-5) | High |
| C-021 | Push decision gate | Reuse `evaluate_push_decision` with `applied_edits = resolved path count` (A:337) | Sibling `evaluate_sync_decision` with 4 predicates; reject reusing predicate 5 (B:108, :327-338) | `evaluate_merge_push_decision`, 3 predicates (C:112) | Medium |
| C-022 | Merge-parent rule | `merge_parent_ok`: exactly `[pre_push_sha, base_sha]` in order, ids 40-hex, not equal (A:420) | `merge_parent_ok`: same strict order, plus disjointness property vs `push_parent_ok` (B:313-325) | `merge_push_parent_ok`: set equality, order-independent (C:93) | High |
| C-023 | Pre-push guard sequence | head -> base ancestry (`merge-base --is-ancestor`) -> parent -> `push_decision` (A:332-338) | head (plus local HEAD == `pre_push_sha` before merge) -> parent -> base ancestry -> decision (B:344, :353) | head -> parent -> merge sentence -> DECIDES; no base ancestry check (C:99) | Medium |
| C-024 | Merge commit and staging check | `git commit -F <msg>`; before commit, staged set shares no path with `OPERATOR_PENDING` after clean-tree preflight (A:321-328) | `finish-merge.sh`: `MERGE_HEAD == base_sha`, no unmerged, no introduced markers, staged ⊆ base-changed ∪ resolved, then `git commit -F` (B:352) | Plain `git commit` with `GIT_EDITOR=true`; staged set == conflicted-path set (C:98, :111) | Medium |
| C-025 | Marker scan | `conflict_marker_lines`: setext-aware; ignores a marker line present verbatim in any side (A:421) | Marker-line count in result must not exceed count in stage-1 blob (B:352) | Any marker line blocks, incl. inside string literals; scoped to conflicted paths (C:109) | Medium |
| C-026 | Preflight | Foreign operation, tracked tree clean (any non-`??`), untracked -> `OPERATOR_PENDING`, branch not detached/not base (A:285-290) | `foreign_op` null and `index_clean` (staged only); unstaged/untracked tolerated (B:240-241) | Rely on git refusing; `dirty_worktree` halt; foreign-op and detached-HEAD halts (C:85) | Low |
| C-027 | Unfinished merge on halt | Leave in progress with finished paths staged (J-53); Tier 3 at probe time touches nothing (A:166) | Abort (`git merge --abort`) when resolution incomplete; leave in progress only when complete (L2, hook failure) (B:389-392) | Pre-merge Tier 3: abort; mid-resolution: leave in progress (C:62) | Medium |
| C-028 | VAL integration | VAL always; VG-1 on resolved paths escalating to VG-2 if no area maps; VG-2 mandatory at Tier 2 (A:309-317) | VAL always; VG-2 forced only for `pr_submit/` or `pyproject.toml`; `uv lock --check` added to VG-1 (B:385-387) | Tier 2 always; Tier 1 lockfile-only skips VAL (C:112 FR-7.5) | Medium |
| C-029 | Run-log events | `conflict_classified`, `conflict_resolved` (41 -> 43) (A:251-256) | `sync_started`, `sync_concluded` (41 -> 43) (B:280-285) | `conflict_detected`, `conflict_resolved`, `conflict_halted` (41 -> 44) (C:36, :83) | Medium |
| C-030 | Push record fields | `push_kind` (`fix`/`merge`) and `base_sha`, added only for merge (A:258) | `kind: "sync"` and `base_sha` on sync records only (B:96) | `push_kind` on all three triad records, default `"fix"` (C:83, FR-6.3) | Low |
| C-031 | Resume | Crash window first; then `conflict_resume_point` with 5 outcomes; Branch A resumes S5a/S5 (A:262-277) | Five-row table; Branch A of a sync returns `S2_CLASSIFY` (B:289-301) | Branch A resumes Wave 8 re-arm or Wave 1, never S5a; Branch B re-drives with record `target_sha` (C:84) | Medium |
| C-032 | Repeat conflicts in one run | Each further cycle spends a round; `C-ci` handles a base move (A:352) | `SYNC_CAP = 2`; P3 late re-sync Tier 0/1 only; late Tier 2 halts `late_conflict` (B:276) | `merge_push_count <= 1`; second conflict halts `second_conflict` (C:112 FR-7.4) | Medium |
| C-033 | Create-path rebase contradiction | Remove the create-path rebase; behind is a report; rewrite pin `test_static_grep.py:654-661` (A:53, FR-C20) | Keep rebase and HALT; add one clarifying sentence; pins byte-identical (B:618-624, OQ-7) | Keep rebase; HALT only on a conflict the rebase hits or behind on `--pr`; reword three sites and update pins (C:70) | High |
| C-034 | Flags | `--conflict-max-tier {0,1,2}`, default 2 (A:76) | `--sync-tier {0,1,2}`, default 1 (B:97) | No flag (C:46) | Medium |
| C-035 | Output contract additions | `conflict: {tier, status, files, merge_sha}` (A:FR-C21) | `sync_tier`, `sync_outcome`, `sync_push_count` (B:FR-19) | `merge_push_count` (C:81) | Low |
| C-036 | Test strategy for git behaviour | Captured real `merge-tree` fixture; no git in suite (A:550, :557) | Real-repo script tests with local bare origin under `tmp_path`, capability-skip (B:460) | No test executes a real merge; git mechanics pinned as prose (C:155) | Medium |
| C-037 | Rollout | Single release; `--conflict-max-tier` as runtime ceiling | P0-P3 phases with gates; Tier 2 dark by default (B:514-525) | Single release; create-path fix lands first (C:70) | Medium |
| C-038 | Git config use | Per-invocation `-c merge.conflictStyle=zdiff3`; reject `rerere` (A:92) | Per-invocation zdiff3 and `-c rerere.enabled=false` (B:347) | Reject zdiff3 as unneeded; rerere prohibited (C:43) | Low |
| C-039 | Cost-layering claim at Tier 0 | One `gh pr view` read, no fetch when MERGEABLE (A:11, NFR-1) | "Two read-only calls" (fetch, merge-tree) inside the probe (B:439) | "One poll-field read" (C:64) | Low |

## Contradictions

Cross-variant rows are X-001..X-033. Intra-variant rows (a variant against itself or against the repo it cites) are X-034..X-041. "n/a" means the variant does not take a position.

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | When conflict handling ACTS in the flow | "`C-initial` ... before the first `poll-augment-review.sh` call" and "`C-ci` ... before `should_arm_ci_wait`" (A:186-187) | "Act before Wave 1 ... Reject: highest coupling"; act in "Wave 8a ... after the review phase settles and before the CI wait" (B:205-206, :20) | "Wave 0b, after Wave 0 head binding, before Wave 1"; plus re-checks at Wave 8 entry and the pre-push guard (C:74-76) | High |
| X-002 | Does a conflict cycle consume a review round | "ticks `round_counter` on the existing INV-001 edge" (A:16, :236) | "`round_counter`, `max_rounds`, `push_count` and `rereview_request_count` do not move" (B:22) | "a merge cycle NEVER ticks `round_counter`" (C:81) | High |
| X-003 | Are reviewers re-triggered after the merge push | "re-triggers the reviewers through the existing S5a path" (A:16, :247) | "A sync push does not call `retrigger-review.sh`" (B:273) | "a merge push does NOT re-trigger reviewers" (C:82) | High |
| X-004 | FSM change | "one new FSM edge `(S2_CLASSIFY, "conflicting")`" (A:18, :224-230) | "no new FSM state or edge" (B:18, R3 B:106) | "Zero new `MonitorState` members, zero new `transition()` edges" (C:44) | High |
| X-005 | Is a merge push counted in `push_count` | "`push_count` +1 per landed merge push" (A:239) | sync push "folds into the new `sync_push_count`" (B:271) | excluded "via the `push_kind: merge` filter ... NEW output field `merge_push_count`" (C:81) | Medium |
| X-006 | Parent order in the merge-parent check | "`parents[0] == pre_push_sha`, `parents[1] == base_sha` ... a swapped order is rejected" (A:344, :420) | "target_parents[0] ... (first parent is the PR head)"; "swapped order -> false" (B:319-322) | "`{p1.lower(), p2.lower()} == {...}` (order-independent)"; "order swapped OK" (C:93, :110) | High |
| X-007 | Name of the merge-parent check | `merge_parent_ok` (A:420) | `merge_parent_ok` (B:314) | `merge_push_parent_ok` (C:93) | Low |
| X-008 | Base reachability and what the merge push publishes | Requires `git merge-base --is-ancestor <base_sha> origin/<base>`; other new ancestors "are already public" (A:335, :343) | Same check as step 10(c); "the only commits `M` adds ... are ancestors of `base_sha`" (B:309, :353) | No ancestry check; pushing `merge_sha` "publishes exactly one commit (the merge)" (C:93) | Medium |
| X-009 | Order of guard steps | head -> base ancestry -> parent -> `push_decision` (A:334-337) | head -> parent -> base ancestry -> decision (B:353) | head -> parent -> merge sentence -> DECIDES (C:99) | Low |
| X-010 | Whether the INV-016 push decision can be reused | "`evaluate_push_decision(...)` with `applied_edits = <resolved path count>`" (A:337) | "Reusing `evaluate_push_decision` with `applied_edits := files changed` ... makes the audit record lie" (B:108) | New 3-predicate `evaluate_merge_push_decision` (C:112) | Medium |
| X-011 | Run-log event count after the change (pinned 41) | 43 (`conflict_classified`, `conflict_resolved`) (A:251) | 43 (`sync_started`, `sync_concluded`) (B:280) | 44 (`conflict_detected`, `conflict_resolved`, `conflict_halted`) (C:36) | Medium |
| X-012 | L2 semantics | "`MERGE_HEAD` still present: no commit, matching T-412" (A:57) | "stop with the merge in progress and uncommitted" (B:251) | "L2: resolve + commit locally (the merge commit exists; nothing pushed)" (C:80) | High |
| X-013 | Create-path rebase vs HALT | Remove the rebase: "the head is already published ... a rebased branch 'needs a force-push'" (A:27, :53) | Keep both: "on the create path the branch is not yet a published PR head, so rewriting it locally is harmless" (B:622) | "create path rebase stays (unpublished branch, no force-push needed)"; pins "updated in the same commit" (C:70) | High |
| X-014 | New flag | `--conflict-max-tier {0,1,2}` default 2 (A:76) | `--sync-tier {0,1,2}` default 1 (B:97) | "A new CLI flag ... rejected for V1" (C:46) | Medium |
| X-015 | Tier of tree conflicts (`AA`, `DU`/`UD`, rename) | `MODIFY_DELETE`, `ADD_ADD`, `RENAME_SIDE` are Tier 2 (A:131-133) | "No tree conflict is Tier 1" (B:177) | "tree conflicts with an obvious answer: `AA` ..., `DU`/`UD` ..., rename-vs-edit" are Tier 1 (C:54) | High |
| X-016 | Whitespace-only conflicts | Tier 1 `WHITESPACE_ONLY`, side chosen by `ruff format --check` (A:130, :151) | R-161 whitespace class rejected (B:118); such a path is `text:content` Tier 2 | Tier 1 "whitespace-only or line-ending conflicts" (C:54) | Medium |
| X-017 | Tier 2 file-count cap | `MAX_INTENT_FILES = 10`; 11 -> Tier 3 (A:140) | `TIER2_MAX_FILES` default 8; 9 -> Tier 3 (B:171, FR-2) | No cap | Medium |
| X-018 | VAL for a lockfile-only Tier 1 merge | VAL runs; VG-1 escalates to VG-2 (A:313) | VAL runs; `uv lock --check` added to VG-1 (B:387) | "Tier 1 lockfile-only: no VAL" (C:112 FR-7.5) | Medium |
| X-019 | VG-2 (`make test`) at Tier 2 | "mandatory at Tier 2" (A:314) | Forced only for `pr_submit/` paths or a `pyproject.toml` conflict (B:387) | "VG-2 escalation via the unchanged `is_cross_cutting`" (C:112) | Medium |
| X-020 | Classify before or after starting the merge | Probe "never changes the working tree or index"; classify before merge (A:51, FR-C3) | Probe "performs no worktree or index mutation" (B:243) | "after a merge attempt stops, `merge-status.sh` produces the per-path inventory" (C:50) | High |
| X-021 | Unfinished merge on a mid-resolution halt | "the merge stays in progress with finished paths staged (J-53)" (A:166) | "Halt before the resolution is complete ...: `git merge --abort`" (B:391) | "leave the merge IN PROGRESS locally (J-53)" (C:62) | Medium |
| X-022 | Conflict-marker rule | A marker line inherited verbatim from a side is ignored (A:421) | Count in result must not exceed count in stage-1 blob (B:352) | "ANY hit blocks the commit", including markers in string literals (C:109) | Medium |
| X-023 | Staged-set check before the merge commit | Staged set must share no path with `OPERATOR_PENDING` (A:325) | Staged ⊆ (files changed on base since merge-base) ∪ (resolved paths) (B:352) | "staged-set == conflicted-path-set assertion before `git commit`" (C:111 FR-6.4); impossible whenever the base changed any non-conflicted file, because git stages cleanly merged paths | High |
| X-024 | Dirty-tree preflight | Any tracked change halts `merge_preflight_dirty` (A:288) | Only a staged index halts; "Unstaged or untracked operator files are tolerated" (B:241) | Rely on git refusing to merge; halt `dirty_worktree` (C:85) | Low |
| X-025 | `zdiff3` conflict style | Use per-invocation `-c merge.conflictStyle=zdiff3` (A:297) | Same (B:347) | "zdiff3 is not needed" (C:43) | Low |
| X-026 | Authority of GitHub `mergeable` | `MERGEABLE` ends Wave C "after one read ... no fetch, no probe" (A:FR-C2) | GitHub fields "advisory ... never a halt"; "Local `merge-tree` is the source of truth" (B:242) | GitHub fields drive Wave 0b; local stop also counts (C:74) | Medium |
| X-027 | `UNKNOWN` mergeability | "re-read at most 3 times, 10s apart" then probe (A:199) | Advisory; `null` on failure (B:242) | "re-read once ... then treat a second `UNKNOWN` as no-signal and continue" (C:74) | Low |
| X-028 | Conflict cycles per run | Bounded only by `max_rounds` (A:612) | `SYNC_CAP = 2` (B:272) | `merge_push_count <= 1`; second conflict halts (C:112 FR-7.4) | Medium |
| X-029 | Lockfile with no recipe (e.g. `package-lock.json`) | No rule matches; falls through to `TEXT`, Tier 2 (A:128, :134) | `halt:lockfile_no_recipe`, Tier 3 (B:158) | "lockfiles regenerable by a known package manager" are Tier 1 (C:54) | Medium |
| X-030 | Resume Branch A for a conflict push | Resolves "exactly as today" at S5a or S5 (A:266) | "Branch A of a sync returns `S2_CLASSIFY` (never S5)" (B:299) | "resume at Wave 8 re-arm or Wave 1 continuation, NOT at S5a" (C:84) | Medium |
| X-031 | L1 run continuation after a proposal | "the run stops (no review poll, no merge started)" (A:216) | Reviews continue; propose at Wave 8a (B:250) | Proposes plan; continuation not stated (C:80) | Medium |
| X-032 | Scripts | "New script ... rejected"; extending poll script "rejected for this release" (A:86-87) | Three new scripts (B:90-92) | One new script plus extended `poll-augment-review.sh` (C:34) | Medium |
| X-033 | `.claude/` paths in a conflict | `.claude/settings.json` is Tier 3 `HUMAN_PATH` (A:126) | `.claude/settings.json` and `settings.local.json` are `halt:protected` (B:154) | "`.claude/` sync targets from `src/superclaude/`" are Tier 1 generated output (C:54); `.claude/*` is gitignored except `settings.json` (`.gitignore:127-128`), so they are never conflicted tracked paths | Medium |
| X-034 | Variant C (intra): Wave 0b sequencing | n/a | n/a | Wave 0b runs "before Wave 1", reads "the poll snapshot fields" and appends `conflict_detected` (C:74, :83); the output-dir, run-log and `poll-augment-review.sh` loop start only in Wave 1 (SKILL.md:269) | High |
| X-035 | Variant C (intra): L1 without a merge | n/a | n/a | "L1: detect + classify + PROPOSE ... the merge is NOT attempted" (C:80) vs classification runs "after a merge attempt stops" (C:50) | High |
| X-036 | Variant C (intra): `AA` tier | n/a | n/a | First match wins; Tier 2 rule (listed 2nd) covers `UU`/`AA`, Tier 1 rule (listed 3rd) also claims `AA` (C:53-54) | Medium |
| X-037 | Variant C (intra): re-check point B | n/a | n/a | Merge after the fix commit exists, then "the fix push proceeds with `push_parent_ok` against the updated `pre_push_sha`" (C:76). The merge's first parent is the fix commit, not `pre_push_sha`, so `merge_push_parent_ok` fails; the fix commit's parent is the old head, so `push_parent_ok(.., merge_sha)` fails | High |
| X-038 | Variant C (intra): behind on `--pr` | n/a | n/a | HALT applies to "a behind-base state discovered on `--pr`" (C:70) vs "BEHIND-only is NOT a conflict ... `--pr` path reports" (C:55) | Medium |
| X-039 | Variant C vs allowed-tools | n/a | n/a | Merge commit with `GIT_EDITOR=true` prefix (C:98); SKILL front matter allows only `Bash(git *)`-style prefixes (SKILL.md:4), so the env-prefixed form may not match | Low |
| X-040 | Variant B (intra): Tier 0 cost | n/a | "a normal PR pays for two read-only calls" (B:219) vs probe at end of Wave 0 AND again at Wave 8a, each also doing `gh pr view` and a capability probe (B:214-215, :238-239) | n/a | Low |
| X-041 | Variant A vs head binding: operator recovery | HALT and L2 messages: "Finish it by hand and commit ... Then re-run with `--pr <N>`" (A:174-175, :217); a re-run requires local HEAD == `headRefOid` (SKILL.md:268), so an unpushed local merge commit halts `pr_head_mismatch` | Message says "run `git commit` yourself and push" (B:351) | n/a | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | `MechanicalRule` data extension point with `sources`, `regenerate`, `check` argv, plus the run-level "generated dependency" rule (output is Tier 3 if a source is Tier 3 or sources are empty) and source-before-output resolution order (A:139, :391-404) | Medium |
| U-002 | A | Every mechanical rule's program must already be in the SKILL `allowed-tools`, enforced by a test (A:407, R-6) | Medium |
| U-003 | A | Ref split by tier so a Tier 1 run never loads the Tier 2 ref, with a static test that `conflict-intent.md` is named only in the Tier 2 sentence (A:73, NFR-1) | Medium |
| U-004 | A | When Wave C does not push a merge at `C-ci`, skip the CI wait with reason `pr_conflicting` instead of polling until `--timeout` (A:220, FR-C23) | Medium |
| U-005 | A | Captured real `git merge-tree -z` output as a test fixture (`fixtures/merge_tree_conflict.z`) so the parser is tested without running git (A:557) | Medium |
| U-006 | A | `conflict_resume_point` as a pure function returning one of six named resume points (A:425) | Low |
| U-007 | A | Operator guidance that a conflict costs one round, so `--max-rounds 2` leaves one review-fix round; `--max-rounds 0` reports and never merges (A:238, :243) | Low |
| U-008 | B | Four-phase rollout P0-P3 with go/no-go gates; Tier 2 ships dark behind `--sync-tier 1` default; P0 is read-only (B:514-525) | High |
| U-009 | B | High-suspicion checklist (signature, schema, dependency, constant, public API changed on one side while the other adds callers; API removed while consumers remain) that marks a file `semantic` and the cycle Tier 3 (B:193-195) | High |
| U-010 | B | `finish-merge.sh` commit gate: `MERGE_HEAD == base_sha`, no unmerged paths, no introduced markers, staged ⊆ base-changed ∪ resolved, hooks on (B:352, FR-11) | Medium |
| U-011 | B | Disjointness property test: `push_parent_ok` rejects every input `merge_parent_ok` accepts and vice versa (B:325) | Medium |
| U-012 | B | Extra Tier 3 classes: mode change, `.github/actions/**`, `settings.local.json`, named lockfiles without a recipe, `generated/`/`dist/`/`build/` without a recipe (B:151-159) | Medium |
| U-013 | B | Real-repo script tests using a local bare `origin` under `tmp_path`, a `gh` PATH stub, skipped by capability probe (B:460) | Medium |
| U-014 | B | `SKILL.md` growth cap (at most 15 lines, line-count assertion `<= 346`) and a byte-identical fragment regression test (B:444, :492-500) | Medium |
| U-015 | B | P3 late re-sync: `merge_state` appended to `poll-ci-checks.sh` output so a base move during the CI wait triggers one more Tier 0/1 sync (B:276, FR-25) | Medium |
| U-016 | B | Per-invocation `-c rerere.enabled=false` so no recorded resolution is replayed (B:347) | Low |
| U-017 | B | Exact revert command (`git revert -m 1 M`) in reports, and the `uv.lock` dependency diff in the merge commit body (B:307, :363) | Low |
| U-018 | B | `github_disagrees` report when GitHub and local `merge-tree` disagree (B:242) | Low |
| U-019 | C | Re-check point B: re-read mergeability inside the pre-push head guard of a fix push (C:76); the sequence as written cannot pass the parent checks (X-037) | Low |
| U-020 | C | Definitions section fixing terms: conflict state, unmerged path, merge cycle, marker line, HALT (C:16-24) | Low |
| U-021 | C | Explicit "what deliberately has no test" list (C:153-155) | Low |
| U-022 | C | Snapshot and test-expectation files (R-60) as Tier 1 regenerate-from-resolved-code (C:54) | Low |
| U-023 | C | `mergeStateStatus` `BLOCKED` treated as Tier 0 alongside `CLEAN` and `BEHIND` (C:55) | Low |
| U-024 | C | PR checklist step: grep `tests/` for `== 41` so no pinned event count is missed (C:161) | Low |

## Shared Assumptions

### Agreement points (all three variants converge)

1. Publish by one merge commit of `origin/<base>` into the PR branch, pushed as a fast-forward; never rebase, never force-push.
2. Add a sibling merge-parent check; `push_parent_ok` stays unchanged with its `merge` test id.
3. No new agent; reuse `evidence-validator` for Tier 2; no new template file.
4. New pure core module joins `CORE_PURE_FILES` (T-N50); git commands live in a ref excluded from that set.
5. VAL is the safety net after a resolution; Tier 2 always validates.
6. Tier 3 halts with nothing pushed and the operator finishes and re-runs with `--pr <N>`.
7. `uv.lock` is the only shipped mechanical recipe, regenerated with `uv lock`.
8. Conflict cycles get their own `cycle_id`; the push idempotency key format is unchanged.
9. Never stash, never `reset --hard`, never blanket `--ours`/`--theirs .`, current worktree only, foreign operations halt.
10. L0 is byte-identical; cross-repo heads are never pushed.

### Enumerated preconditions

A-001..A-005 are UNSTATED and promoted. A-006 is CONTRADICTED and flagged for debate. A-007..A-015 are STATED and not promoted.

| # | Agreement Source | Assumption | Classification | Promoted | Impact |
|---|------------------|------------|----------------|----------|--------|
| A-001 | Point 1 | The repository's branch rules accept a PR that contains a merge commit (no base-branch "require linear history" with rebase-merge, no server hook rejecting merge commits on the PR branch). Otherwise the success criterion "PR mergeable" fails after a correct resolution. No variant mentions it. | UNSTATED | Yes | High |
| A-002 | Point 3 | `evidence-validator`'s input contract (file:line citations in a draft report) fits a resolution record and can judge whether an intent sentence is supported, not only whether cited lines exist. A says it "does not judge truth" itself (A:441); B notes shared model bias (B:531); none checks the agent contract. | UNSTATED | Yes | Medium |
| A-003 | Point 5 | The project the skill runs in has working `make test`, `make lint`, `make verify-sync` targets and a meaningful test suite; the skill is installed into other projects, so VAL as the semantic safety net depends on that. | UNSTATED | Yes | Medium |
| A-004 | Points 1, 7 | The new commands (`git merge`, `git merge-tree`, `git checkout --ours -- <path>`, `git rm`, `git show :n:`), new scripts (B, C) and env-prefixed commands (C) are permitted by the SKILL `allowed-tools` (`Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *)`, SKILL.md:4). A checks this only for mechanical-rule programs (A:407). | UNSTATED | Yes | Low |
| A-005 | Point 8 | The new conflict `cycle_id` values (A: "own cycle_id", B: `sync-<n>`, C: `merge-<n>`) cannot collide with how existing cycle ids are generated; none cites the existing generator. | UNSTATED | Yes | Low |
| A-006 | Point 6 | A re-run with `--pr <N>` after the operator finishes the merge passes Wave 0 head binding. Contradicted: head binding requires local HEAD == `headRefOid` (SKILL.md:268), so an unpushed local merge commit halts `pr_head_mismatch`. B tells the operator to push (B:351); A says only "commit" (A:174-175); C does not say. | CONTRADICTED | No (flagged) | Medium |
| A-007 | Point 7 | `uv lock` can run in the session (network, uv version matching the lock format). Stated by B (K3, B:533). | STATED | No | Low |
| A-008 | Points 1, 5 | GitHub does not run `pull_request` workflows while a PR conflicts. Stated as an external fact by A (A:33), B (B:78), C (C:75). | STATED | No | Low |
| A-009 | Point 1 | Base commits brought in by the merge are already public on the base branch, so publishing them on the PR branch adds no unreviewed work. Stated by A (A:343), B (B:309), C (C:82). | STATED | No | Low |
| A-010 | Point 3 | The attended session has enough context for up to 8-10 Tier 2 files with three stages and evidence each. Stated by B as a revisit trigger (B:104); A and B bound it with a file cap. | STATED | No | Medium |
| A-011 | Point 1 | The fetched `origin/<base>` is the same base tip GitHub computes mergeability against. Holds because the PR is opened on the repo resolved from origin (SKILL.md:267); B reads `baseRefName` (B:238). | STATED | No | Low |
| A-012 | Point 1 | The PR becomes `MERGEABLE` after the push unless the base moves in between. Stated by A (R-3, A:612) and B (K7, B:537). | STATED | No | Low |
| A-013 | Point 6 | Failure to state each side's intent in one sentence is a usable proxy for "needs a human". Stated via research R-18 in all three. | STATED | No | Low |
| A-014 | Point 9 | Foreign-operation detection through `git rev-parse --git-path` is worktree-aware. Stated by A (A:287) and B (B:240). | STATED | No | Low |
| A-015 | Point 10 | Cross-repo (fork-hosted) PR heads are never pushed, so conflict resolution there is report-only. Stated by A (A:631) and B (B:551); C is silent. | STATED | No | Low |

### Promoted [SHARED-ASSUMPTION] diff points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | [SHARED-ASSUMPTION] Branch rules accept a PR containing a merge commit | Point 1 | High | Open for debate |
| A-002 | [SHARED-ASSUMPTION] `evidence-validator` contract fits a resolution record and can test an intent claim | Point 3 | Medium | Open for debate |
| A-003 | [SHARED-ASSUMPTION] Target project has the VAL make targets and a real test suite | Point 5 | Medium | Open for debate |
| A-004 | [SHARED-ASSUMPTION] `allowed-tools` permits the new commands and scripts | Points 1, 7 | Low | Open for debate |
| A-005 | [SHARED-ASSUMPTION] Conflict `cycle_id` values cannot collide with existing ids | Point 8 | Low | Open for debate |

## Repo Spot-Checks

Claims about existing code were checked against the worktree at `119622e3` on 2026-11-04. This section adds no new diff points; each row points to the diff point it supports.

### Claims found false or inaccurate

| Variant | Claim | Repo evidence | Related ID | Severity |
|---------|-------|---------------|------------|----------|
| C | `.claude/` sync targets are tracked generated output that can be regenerated as Tier 1 (C:54) | `.gitignore:127-128` ignores `.claude/*` except `settings.json`; those paths cannot be conflicted tracked files | X-033 | Medium |
| C | Wave 0b (before Wave 1) reads poll-snapshot fields and appends run-log events (C:74, :83) | Output-dir, run-log and `poll-augment-review.sh` start in Wave 1 (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:269`) | X-034 | High |
| C | L2 may commit the merge locally (C:80) | L2 contract is "NO commit" (`SKILL.md:273`; `refs/state-machine.md` §5.2a, T-412 "commit never") | X-012 | High |
| C | Pushing the merge "publishes exactly one commit" (C:93) | `push_parent_ok` docstring: a fast-forward "publishes every commit between the two" (`src/superclaude/pr_submit/fsm.py:585-587`); the merge also publishes base-side commits | X-008 | Medium |
| C | New ref and script "appear in the installed-files list automatically; NO edit needed" (C:150) | `tests/unit/test_cli_install.py:248-262` is a literal baseline checked by `_assert_present` (`:496-500`); new files are not added to it, though the test still passes | none | Low |
| C | Merge commit via `GIT_EDITOR=true git commit` (C:98) | `allowed-tools` lists `Bash(git *)` prefixes only (`SKILL.md:4`) | X-039 | Low |
| B, C | Create-path rebase is safe because the branch is unpublished (B:622, C:70) | The skill's own head-binding message says "a branch Wave 0 rebased needs a force-push, which this skill never does for you" (`SKILL.md:268`); the head branch is normally on the remote before `gh pr create` | X-013 | Medium |
| A | Operator recovery "commit ... then re-run with `--pr <N>`" (A:174-175, :217) | Re-run head binding requires local HEAD == `headRefOid` (`SKILL.md:268`); an unpushed local merge commit fails it | X-041, A-006 | Medium |

### Claims confirmed

- `push_parent_ok` rejects any parent count other than one (`fsm.py:582-600`); the `merge` test id is at `tests/pr_submit/test_pre_pr_checks.py:216-222`. (A, B, C)
- Event enum pinned at 41 (`tests/pr_submit/test_run_log.py:168`, `tests/pr_submit/test_codex_reviews.py:441`); `IDEMPOTENCY_SETS` pinned at 7 (`tests/pr_submit/test_idempotency.py:89`). (A, B, C)
- `CORE_PURE_FILES` includes `fsm.py` and `state-machine.md` (`tests/pr_submit/test_static_grep.py:37-51`). (A, B, C)
- The test at `test_static_grep.py:656-661` pins both the create-path rebase wording and the create-path HALT row. (A, B)
- `transition()` applies `needs_human_decision` first and leaves unknown edges in place (`fsm.py:716-802`); `S4_HALT_BEFORE_PUSH` is set by the caller, not by `transition()` (`fsm.py:1121`). (A, B)
- Recovery copies a fixed key tuple with no push kind (`src/superclaude/pr_submit/recovery.py:98-110`); Branch A resumes at S5a or S5. (A, B, C)
- `rebuild_state` adds every `push_completed` to `push_count` (`src/superclaude/pr_submit/run_log.py:238-241`). (B, C)
- `poll-augment-review.sh:38` reads `--json number,url,headRefName,headRefOid,baseRefName`. (A, C)
- The force-push regex scans every `.md` and `.sh` in the skill folder (`test_static_grep.py:758-776`). (A, B)
- `SKILL.md` is 331 lines; `fsm.py` is 1183 lines; 11 refs, 4 scripts, 23 `MonitorState` members. (A, B)
- S5a re-trigger runs only when the cycle applied edits (`SKILL.md:274`). (C)

## Summary

- Total structural differences: 15
- Total content differences: 39
- Total contradictions: 41 (33 cross-variant, 8 intra-variant or variant-vs-repo)
- Total unique contributions: 24 (A: 7, B: 11, C: 6)
- Total shared assumptions surfaced: 15 (UNSTATED: 5, STATED: 9, CONTRADICTED: 1)
- Highest-severity items: C-008, C-009, C-010, C-014, C-016, C-017, C-018, C-019, C-020, C-022, C-033, X-001, X-002, X-003, X-004, X-006, X-012, X-013, X-015, X-020, X-023, X-034, X-035, X-037, U-008, U-009, A-001
- Similarity check: 124 differences; the variants are not substantially identical, so the debate proceeds.
- Debate focus: the three-way splits on placement (X-001), round and re-trigger accounting (X-002, X-003, X-005), FSM edge (X-004), parent order (X-006), L2 (X-012) and the create path (X-013) decide the merged design. Variant C carries three High internal sequencing defects (X-034, X-035, X-037) and an impossible staging assertion (X-023).
