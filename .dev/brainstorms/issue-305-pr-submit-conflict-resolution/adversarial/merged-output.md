---
title: "Spec: merge-conflict resolution for sc:pr-submit (issue #305)"
variant: merged (base variant-2-sonnet-refactorer)
status: merged-spec
sources:
  - .dev/brainstorms/issue-305-pr-submit-conflict-resolution/seed-brief.md
  - .dev/brainstorms/issue-305-pr-submit-conflict-resolution/enrichment/codebase-context.md
  - .dev/research/issue-305-conflict-resolution/03-roi-scored-list.md (Items scored above 5)
  - .dev/brainstorms/issue-305-pr-submit-conflict-resolution/adversarial/refactor-plan.md (Changes 1-25)
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:refactorer), variant-2-sonnet-refactorer.md -->
<!-- Merge date: 2026-11-04 -->

# Spec: merge-conflict resolution for sc:pr-submit (issue #305)

## 1. Summary and decision record

### 1.1 The recommendation in six lines

<!-- Source: Base (original, modified): restated as the tier split per Change #1; refs and scripts per Change #2; flag per Change #15; counters per Changes #8 and #16; phasing per Change #1 (R2-B M1) -->

1. **Mechanism mix:** one new pure-Python module (`pr_submit/conflicts.py`, Core API in section 3.4), two lazily loaded refs split by tier (`refs/conflict-mechanical.md` for Tier 1 and up, `refs/conflict-intent.md` for Tier 2 only), two thin P1 scripts (`probe-merge.sh`, `finish-merge.sh`), two new run-log events, one flag (`--conflict-max-tier {0,1,2}`, default 1). No new agent, no new template, no new FSM state. `push_parent_ok` and `evaluate_push_decision` stay byte-identical and keep their pinned tests; `build_push_triad` gains two additive keyword arguments (`push_kind`, `base_sha`) whose default output is unchanged. P2 adds exactly one FSM edge, `(S2_CLASSIFY, "conflicting")`, and widens one S5a clause (section 5.6). There is no longer a promise of "no change to any push, gate or transition code": P2 makes those two edits.
2. **Tiers:** Tier 0 none, behind-only or `BLOCKED` (report, no action); Tier 1 regenerate-only (`uv.lock` through one `MechanicalRule` in v1); Tier 2 text and tree conflicts resolved by stated intent; Tier 3 anything else (halt, nothing pushed). Classification is a pure function over a probe that never touches the worktree. Tier never decreases inside a cycle.
3. **When (the tier split):** detection is read-only at the end of Wave 0 (L1+). Each tier then has one acting site:
   - Tier 0: report only.
   - Tier 1: deterministic regenerate. Acts late at Wave 8 entry (Wave 8a), with no round, no re-trigger and no FSM edge. Ships in P1.
   - Tier 2: text by stated intent. Acts early at `C-initial` through the one FSM edge `(S2_CLASSIFY, "conflicting")`, re-triggers reviewers and spends a round. Ships in P2, dark.
   - Tier 3: halts at the end of Wave 0 in the `SKILL.md:268` shape.
4. **Publish:** a single merge commit `M` made by `git merge --no-commit --no-ff <base_sha>` on the PR branch, pushed as a plain fast-forward `git push origin M:<HEAD_BRANCH>`. A new sibling check `merge_parent_ok(parents, pre_push_sha, base_sha)` accepts exactly two parents in exactly that order. `push_parent_ok` is not loosened.
5. **One commit per cycle stays true:** a cycle is a *fix* cycle (one fix commit), a *sync* cycle (Tier 1, one merge commit) or a *merge* cycle (Tier 2, one merge commit). They never share a push. Sync cycles have their own cap (`SYNC_CAP = 1`) and their own counter (`sync_push_count`); `round_counter`, `max_rounds`, `push_count` and `rereview_request_count` do not move for them. A merge cycle spends a round on the INV-001 edge and counts in `push_count` (section 5.6).
6. **Delivery:** four independently shippable phases (P0 detect and report; P1 Tier 1, the publish machinery and the Tier 3 Wave 0 halt; P2 Tier 2, dark; P3 late re-sync during the CI wait). Ship P0 first: it is read-only and already reports a conflicted PR at the end of Wave 0 instead of leaving the operator to discover it during the CI wait.

### 1.2 Decision record (refactorer lens)

<!-- Source: Base (original, modified): debt table and reject list restated as AD-style decision entries per Change #24; form from Variant A (opus:architect), Section 2 (S-005); entry content per Changes #1, #8, #9, #10, #13, #22 -->

The existing skill is already carrying debt: `SKILL.md` is 331 lines with single bullets over 5,000 characters (Wave 6 is one bullet), pinned by dozens of literal-substring assertions. Every decision below is judged first by *how little of that surface it has to touch*. Each entry states the choice, the alternatives rejected and why.

**AD-1. Publish a two-parent commit through a sibling check, never a loosened one.** `push_parent_ok` is pinned to "exactly one parent" (`fsm.py:582-600`, `tests/pr_submit/test_pre_pr_checks.py:216-222`). Choice: a sibling `merge_parent_ok` (section 6.2). The two functions are mutually exclusive by construction (1 parent vs 2 parents), so neither can accept the other's commit. Rejected: loosening `push_parent_ok` or giving it a `kind` parameter (section 3.2 R4); rebasing the PR branch (section 3.2 R12).

**AD-2. One sibling push gate for both conflict tiers.** `evaluate_push_decision` is the INV-016 five-predicate conjunction (`fsm.py:173-204`), and predicate 5 means "grounded finding edits". Choice: `evaluate_sync_decision` covers Tier 1 and Tier 2 with its own predicates and no `applied_edits` predicate (section 6.3). Rejected: reusing `evaluate_push_decision` with `applied_edits = resolved paths` for Tier 2 (section 3.2 R5): it collides with the S5a gate or misstates INV-016 predicate 5 (NE1).

**AD-3. Push kind on every push record, through the existing builder.** The push triad and recovery have no push-kind field today (`fsm.py:236-288`, `recovery.py:57-171`). Choice: `kind` in `{fix, merge, sync, ci}` on all three records, added by keyword arguments to `build_push_triad`; absence means `fix`, so old run-logs and existing record-shape tests are unchanged (section 5.7). Rejected: a separate `build_sync_triad` (duplicates the builder); a kind on sync records only (a crashed L3 CI push would still resume at S5a, INV-002).

**AD-4. Two events, two pin edits.** The event enum is closed at 41 and pinned in two tests (`models.py:22-90`, `test_run_log.py:168`, `test_codex_reviews.py:441`). Choice: add exactly two events (`sync_started`, `sync_concluded`) for Tier 1, edit the two pins and the `models.py:23` docstring once, and reuse `terminal_halted` with new `reason` values for every halt. The Tier 2 (P2) event set is OPEN (section 12, C-029). Rejected for now: a new event per halt reason.

**AD-5. Procedure lives in the refs, and `SKILL.md` stays small.** `SKILL.md` must keep exactly one python block (`test_cosmos_protocol.py:36`, `test_codex_reviews.py:688`). Choice: all new procedure lives in the two refs; `SKILL.md` grows by a bounded handful of lines (NFR-9), checked by the byte-identical fragment test (section 8.4). Rejected: a `SKILL.md <= 346` line-count assertion (brittle; removed per section 8.2).

**AD-6. The tier split: Tier 1 acts late, Tier 2 acts early.** Choice: Tier 1 resolves at Wave 8a with no round and no re-trigger; Tier 2 resolves at `C-initial`, re-triggers reviewers and spends a round (sections 5.1, 5.6). Rejected: every conflict push, including Tier 1, spending a round (on a spent budget this reproduces #305, N4); acting late for every tier (reviewers would never see a Tier 2 resolution); Tier 3 through the `needs_human_decision` pre-gate (it needs an armed FSM, while the Wave 0 halt in the `SKILL.md:268` shape does not).

**AD-7. The create path at L1+ neither rebases nor halts when behind base.** The create path both rebases and halts when behind (`SKILL.md:267` vs `:220-223`, `:315`). Choice: a separate precursor change (section 9). At L1+ being behind base on the create path is a Tier 0 report; L0 keeps today's rebase byte for byte (`test_static_grep.py:649-657` unchanged); only the L1+ HALT pins at `test_static_grep.py:658` and `:660` are rewritten (section 8.2). Rejected: clarifying wording only (the "unpublished branch" premise is false: the head is published when `gh pr create` runs); keeping the create-path rebase at L1+.

### 1.3 What "done" looks like (maps to the seed's success criteria)

<!-- Source: Base (original, modified): restated for the tier split per Change #1; "grounding checked" wording per weakness W20 (A-002); no-op note per Change #23 (INV-033) -->

- L3, mechanical conflicts only (a tracked `uv.lock`): one merge commit at Wave 8a, pushed fast-forward, no round spent, CI re-polled on the new head with `expect_checks` (section 6.10), PR mergeable.
- L3, text conflicts, `--conflict-max-tier 2` (P2): resolved at `C-initial` before the first review, per-file stated intent recorded, `evidence-validator` grounding checked, VAL green, one merge commit pushed, reviewers re-triggered on the merge head, one round spent; unclear intent halts with nothing pushed.
- Semantic or high-risk (Tier 3): at L3, halt at the end of Wave 0 with nothing touched and nothing pushed; at L1 and L2, reported, and the run continues.
- L1 reports the plan and proposes; L2 leaves the validated resolution as an uncommitted merge in progress; L0 is byte-identical to today.
- All existing tests pass apart from the deliberate pin edits of section 8.2; new tests pin the tiering, the routing table, the merge-parent rule and the halts.
- **Note on this repository (INV-033):** P1's Tier 1 rule is a no-op in IronClaude, because `uv.lock` is gitignored (`.gitignore:169`, `:222`). P1 still pays here through Tier 0 detection, the Tier 3 Wave 0 halt and the `pr_conflicting` CI-wait skip (section 5.5). The P1 gate is therefore met with a hermetic real-git test and a live run on a separate repository (section 8.5); `uv.lock` is not un-ignored here.

### 1.4 Definitions

<!-- Source: Variant C (haiku:qa), Section 2: merged per Change #20, adapted to the tier split; VAL and FSM expanded on first use (Clarity-4) -->

- **FSM**: the finite state machine in `src/superclaude/pr_submit/fsm.py` (`transition()`, `MonitorState`) whose reach the `--monitor` ordinal caps (`SKILL.md:36-41`).
- **VAL**: the validation gate list VG-1 to VG-5 that runs before any push (`SKILL.md:279-291`); section 6.7 gives its inputs for a conflict cycle.
- **Conflict state**: GitHub reports `mergeable: "CONFLICTING"` (after the `UNKNOWN` re-read rule of section 5.3) or `mergeStateStatus: "DIRTY"`, or the local probe reports unmerged paths.
- **Unmerged path**: a path with index entries at stages 1, 2 or 3 in the probe's raw `-z` listing.
- **Tier**: the complexity class of the whole merge attempt, the maximum tier over its conflicted paths (section 4.2). It selects the procedure, the acting site and the process cost.
- **Sync cycle**: a Tier 1 cycle. Cycle id prefix `sync-`, one merge commit, push kind `sync`, acts at Wave 8a, consumes no round, re-triggers no reviewer, capped by `SYNC_CAP = 1`.
- **Merge cycle**: a Tier 2 cycle (P2). Cycle id prefix `conflict-`, one merge commit, push kind `merge`, acts at `C-initial` through the `(S2_CLASSIFY, "conflicting")` edge, re-triggers reviewers and spends a round.
- **Fix cycle**: the existing remediation cycle (one fix commit, push kind `fix`).
- **Hook points**: `C-initial` is Wave 1 after arming and before the first review poll; Wave 8a (also called `C-ci`) is Wave 8 entry, before the CI wait arms.
- **Resolution record**: the per-file Tier 2 record of section 6.6.
- **Marker line**: a line that starts at column 0 with seven `<`, `|`, `=` or `>` characters. The finish gate rejects only *introduced* marker lines (section 6.4 step 9).
- **HALT**: `terminal_halted` with a `reason`, appended to the run-log when one exists (before Wave 1, in the `SKILL.md:268` shape); nothing is pushed.

## 2. Grounding: facts this spec relies on

<!-- Source: Base (original) -->

Repo facts (re-checked in this session; line numbers are from the current worktree):

| # | Fact | Source |
|---|---|---|
| G1 | The ordinal is a ceiling on one FSM; the core decides, `SKILL.md` sequences and does git/gh I/O | `SKILL.md:36-41` |
| G2 | Wave table; each wave lazy-loads its own ref | `SKILL.md:252-265` |
| G3 | Wave 0 rebases if behind on the create path; on `--pr` it only reports commits behind | `SKILL.md:267` |
| G4 | STOP block and Error Handling row say HALT for "behind base branch on the create path" | `SKILL.md:220-223`, `:315` |
| G5 | The suite pins BOTH the rebase wording and the HALT wording, so the "contradiction" is encoded as intentional | `tests/pr_submit/test_static_grep.py:656-661` |
| G6 | Head binding reads `--json headRefName,headRefOid,isCrossRepository` (substring pinned) | `SKILL.md:268`, `test_static_grep.py:636` |
| G7 | Wave 6: one fix commit per cycle, `git add -- <paths>`, `git commit --only -- <paths>`, `OPERATOR_PENDING` refusal, pre-push head guard (`pr_head_ok`, then `push_parent_ok`, then "The deterministic core DECIDES"), push triad, `git push origin <target_sha>:<target_branch>` | `SKILL.md:274`, pins `test_static_grep.py:664-755` |
| G8 | `push_parent_ok` fails closed on anything but exactly one parent equal to `pre_push_sha` | `fsm.py:593-600` |
| G9 | `build_push_triad` records carry run_id, cycle_id, key, pre_push_sha, target_sha, target_branch, target_remote and nothing about kind | `fsm.py:236-288` |
| G10 | `rebuild_state` adds every `push_completed` to `push_count` and `pushed_commit_shas`; `rereview_requested` is folded by distinct `cycle_id` | `run_log.py:204`, `:238-241` |
| G11 | Recovery matches a dangling `push_initiated` by idempotency key; Branch A resumes at S5a or S5; the recovered record copies a fixed key tuple | `recovery.py:57-80`, `:112-147` |
| G12 | The CI phase is SKILL-owned: no new FSM edges, a CI push skips S5a/S6/RESOLVING and re-polls CI on the new head | `refs/state-machine.md` section 5.2c, `SKILL.md:277` |
| G13 | Wave 8 arms only after Augment `clean`/`REPORT_ONLY`/`HALT_MAX_ROUNDS`/`TERMINAL_AUGMENT_NO_RESPONSE`; a human gate maps to `HALT_HUMAN` unless Augment already halted | `SKILL.md:277` |
| G14 | Nothing in src/, the skill, the command or tests reads `mergeable` or `mergeStateStatus` | enrichment section 3 |
| G15 | T-N50 bans the tokens `git` and `gh` in `fsm.py`, `ci.py`, `state-machine.md` and five more files; a new core file must join the set or stay equally clean | `test_static_grep.py:37-51`, `:132-143` |
| G16 | The force-push scan regex covers every `.md` and `.sh` in the skill folder, so even a prose mention such as "never run git push --force" fails it | `test_static_grep.py:758-776` |
| G17 | `evidence-validator` is read-only (Read, Grep, Glob) and re-reads file:line citations | `agents/evidence-validator.md:1-9` |
| G18 | The command "Will Not" sentence "push any commit besides the cycle's one fix commit" is pinned | `commands/pr-submit.md:85`, `test_static_grep.py:754-755` |
| G19 | Reviewer completion is keyed to the expected head: `_selection` passes `expected` into `_completion_reviews` (verify the equality semantics during implementation) | `classifier.py:446-461` |

Behaviours of git verified empirically in a scratch repo (git 2.47.3) while writing this spec:

- `git merge-tree --write-tree <ours> <theirs>` exits 0 on a clean merge and 1 on conflicts, never touches the index or worktree (it writes only unreachable tree objects), and its full form lists every conflicted path with `<mode> <oid> <stage>`. Stage sets seen: `123` content conflict, `13` modify/delete (deleted by the base side). A binary conflict prints "Cannot merge binary files". `--name-only` drops the stage data, so the probe must use the full form (with `-z`).
- `git commit --only -m x -- <path>` during a merge fails with "cannot do a partial commit during a merge". The merge commit therefore needs its own commit step (plain `git commit -F <file>` after exact-path staging).
- `git diff --numstat <merge-base> <side> -- <path>` prints `-  -  <path>` for a binary file.

External facts (not verifiable offline; the spec uses them as hints, never as gates): GitHub computes `mergeable` asynchronously and can return UNKNOWN; `pull_request` workflows do not start while a PR has a merge conflict; `gh pr view --json` exposes `mergeable`, `mergeStateStatus` and `baseRefName` (probe the field list with `gh pr view --help`, the same pattern as the CI-wait preflight at `SKILL.md:225-230`).

## 3. Mechanism mix: what to build, what to reject

<!-- Source: Base (original) -->

Selection rule: a piece earns its place only if (a) it carries a safety property that prose cannot enforce, or (b) it removes work that would otherwise be repeated per run, and (c) its test and maintenance cost is lower than the failure it prevents. ROI ids are from `03-roi-scored-list.md` (score above 5 only).

### 3.1 Adopt

<!-- Source: Base (original, modified): rows A1-A4 and A8-A10 replaced per Changes #2, #3, #5, #7, #10, #12, #15, #16; rows A12 (P2 FSM edge) per Change #2 and A13 (CI-wait keyword) per Change #25 -->

| Piece | What it is | Why it earns its place | Cost |
|---|---|---|---|
| **A1. `pr_submit/conflicts.py`** (pure core) | The Core API of section 3.4: `parse_stage_records`, `classify_conflicts`, `conflict_action`, `merge_parent_ok`, `merge_preflight_ok`, `evaluate_sync_decision`, `sync_fail_state`, `crash_resume_plan`, `is_conflict_cycle`, `resolution_record_ok`, `mergeability_hint`; data `MechanicalRule` and `MECHANICAL_RULES`; constants `SYNC_CAP`, `TIER2_MAX_FILES`, the protected and migration path tables | Everything that gates a push, picks a tier or routes an action is deterministic, exhaustively unit-testable and fail-closed. Mirrors `ci.py` (a standalone pure module, no git/gh tokens, in the T-N50 set). Keeps `fsm.py` edits to the parser, the triad keyword arguments and (P2) one edge. | About 250 lines, one test file. |
| **A2. Two refs split by tier** (lazy) | `refs/conflict-mechanical.md` (Tier 1 and up): Wave 0 reporting, the probe, preflight, merge start, the Tier 1 rule, the finish gate, the push, resume rules, HALT message text. `refs/conflict-intent.md` (Tier 2 only): evidence reads, intent rules, the resolution-record format, the `evidence-validator` dispatch | `SKILL.md` is already over-dense; a ref loads only when a conflict is actually in play, so Tier 0 pays nothing, and a Tier 1 run never loads the intent ref, so cost grows with tier. Host of the resolution-record format and HALT text (see rejection R2). | About 150 lines across both; static-grep tests. |
| **A3. `scripts/probe-merge.sh`** (thin) | Read-only: fetch `origin <base>`, record `base_sha`, detect a foreign git operation (`foreign_op`) and a dirty tracked tree (`tree_clean`), and emit the raw `git merge-tree --write-tree -z` listing unparsed, plus the paths `git diff --numstat` marks binary; **one JSON line** (same contract as `poll-ci-checks.sh`). Takes `--repo`. Stage parsing lives in the core (`parse_stage_records`). Runs only when GitHub reads `CONFLICTING` or a persistent `UNKNOWN` (section 5.3) | Keeps git I/O out of the core and out of `SKILL.md` prose; one deterministic call replaces 6 to 8 ad hoc calls; R-26, R-43, J-16, J-17, S-38 become data fields. It is the only way Tier 0 to Tier 3 classification can run without mutating the worktree. | About 60 lines of bash; real-repo tests. |
| **A4. `scripts/collect-conflict-evidence.sh`** (Tier 2 only, deferred to P2, or written as inline calls) | For one path: writes stage 1/2/3 blobs, `git log --left-right --merge -- <path>`, and both merge-base diffs into `<output-dir>/sync/<cycle>/<n>/`, output bounded | Implements S-12, S-13, S-14, R-112, R-181 as one bounded call. Also solves a hard constraint: `evidence-validator` can only Read/Grep/Glob files, so the stage blobs must exist as files. Tier 0 and Tier 1 never run it, so cost layers with complexity. | About 60 lines, or the same reads inline in `refs/conflict-intent.md`. |
| **A5. `scripts/finish-merge.sh`** | The commit gate: verifies the merge is ours (`MERGE_HEAD` equals the recorded `base_sha`), no unmerged paths, no conflict markers introduced, staged paths are a subset of `(files changed by base since merge-base) union (resolved paths)`, then runs `git commit -F <msg>` (hooks on) and prints `{merge_sha, parents}`. It also re-asserts the clean tracked tree right before the regenerate, and after the commit asserts both `git status --porcelain=v1 --untracked-files=no -z` empty and `git diff --quiet HEAD` (section 6.4) | Concentrates every pre-commit safety check in one place that real-repo tests can exercise; R-11, J-56, J-60, J-61, J-63 live here. | About 90 lines. |
| **A6. Inline git/gh/uv calls in the refs** | `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus`, `git merge --no-commit --no-ff`, `git add -- <path>`, `git rm -- <path>`, `uv lock`, `uv lock --check`, `git merge --abort`, `git rev-list --parents -n 1`, `git push origin <sha>:<branch>` | These steps are one-liners whose next step depends on the previous output or on judgment; wrapping them in a script adds nothing. | None beyond the ref text. |
| **A7. Reuse `evidence-validator`** | One read-only spawn per Tier 2 cycle, over `resolution.md` plus the evidence directory | Independent grounding check on the highest-risk automated step (model-authored resolution pushed at L3), at zero new primitives. Same pattern as Wave 3. | One spawn per Tier 2 cycle. |
| **A8. Two run-log events** | `sync_started` (write-ahead, before the merge) and `sync_concluded` (outcome, record path, merge sha). The Tier 2 (P2) event set is OPEN (section 12, C-029) | Resume must tell "our merge in progress" from "the operator's" (J-17, S-05); a bracket is the minimum that does so. Halts reuse `terminal_halted` with a `reason`. | Edit two pinned counts and the `models.py:23` docstring (41 to 43). |
| **A9. `kind` on every push record + kind-aware fold and recovery** | `build_push_triad` gains keyword arguments `push_kind` and `base_sha`; `kind` in `{fix, merge, sync, ci}` goes on all three push records (absent means `fix`). `run_log.py`: the `rebuild_state` fold (`run_log.py:238-239`) excludes kind `sync` only from `push_count` and counts it into `sync_push_count`; `sync_started` events fold into a `sync_cycles` list. `recovery.py`: the key tuple (`recovery.py:98-110`) gains `kind`, and the pure `crash_resume_plan` returns the resume directive for `sync` and `ci` (section 5.8) | Closes the recorded gap that recovery cannot tell a merge or CI push from a fix push (enrichment section 2; INV-001, INV-002), and keeps the counting contract stated in section 5.6. | About 25 lines plus tests. |
| **A10. Flag `--conflict-max-tier {0,1,2}`** (default 1 for the first release) | Ceiling on the tier the skill may act on; 0 = detect and report only | Gives a two-stage rollout without a code change: ship Tier 2 dark, flip the default after evidence. Needs `SkillArgs`, `parse_args` and the command table (`fsm.py:73-99` area) | About 10 lines plus 3 tests. |
| **A11. Edits to `SKILL.md`, command, `state-machine.md`, `ci-poll.md`** | Wave table rows, one Wave 8a bullet, the Wave 0 detection and operation-check sentences, the `C-initial` sentence (P2), output-contract rows, Will Not bullet, Error Handling rows, section 5.2d in `state-machine.md` (no git tokens), the wait-only sentences (section 6.9) and the `expect_checks` sentence (section 6.10) | Required for the skill to be coherent; each edit keeps the pins listed in section 8.3, and the deliberate pin edits are listed in section 8.2. | NFR-9 budget. |
| **A12. One FSM edge (P2)** | `(S2_CLASSIFY, "conflicting")` in `transition()`, with the same round gate as `findings`, plus the widened S5a clause `applied_edits > 0 or kind == "merge"` (section 5.6) | A Tier 2 merge is authored code and must reach S3, S7, S4, S6, RESOLVING, S5a and S5 through the same gates as findings, and spend a round (J-66). | One edge, one clause, row and behavioural tests. |
| **A13. CI-wait keyword (`expect_checks`)** | `ci.classify_checks(..., expect_checks=False)` and `poll-ci-checks.sh --evidence-sha <sha>` (section 6.10) | Without it the first post-push CI poll can read `clean` before any check exists on the merge head (INV-034), and CI is Tier 1's only test signal. | One keyword, one script option, tests. |

### 3.2 Reject

<!-- Source: Base (original, modified): row R3 narrowed to keep it consistent with the one P2 edge adopted per Changes #1 and #2 -->

| # | Rejected piece | Reason | Revisit trigger |
|---|---|---|---|
| R1 | **New agent** (a `conflict-resolver`) | The skill's rule is that the main session performs every side effect (`SKILL.md:82-84`); a resolver agent would need Bash and write access, contradicting that. A read-only variant duplicates `evidence-validator`. A new agent also adds an installed primitive, a dual-surface lookup test and a prompt to maintain. R-173 and J-39 (ROI 6 and 8) say the attended session does the judgment. | Tier 2 resolutions routinely exceed one session's context. |
| R2 | **New template file** for the resolution record or HALT text | No second consumer exists; HALT text already lives inline in `SKILL.md` and is pinned verbatim there (G7); `src/superclaude/templates/` has no matching family. A template is one more installed path to test and sync. | A second skill (for example a standalone `/sc:merge`) needs the same record. |
| R3 | **New FSM states** (`S_SYNC`), and any FSM edge beyond the one P2 edge `(S2_CLASSIFY, "conflicting")` | `transition()` silently ignores unknown edges (`fsm.py:801-802`) and `state-machine.md` claims to be the complete enumeration, so a new state costs `models.py`, `transition()`, the doc and the row-by-row tests. The CI phase proves a SKILL-owned phase works (G12), and Tier 1 uses that shape. The single P2 edge is the exception, adopted because a Tier 2 merge must be re-reviewed and spend a round (A12). | A conflict outcome must change a later FSM decision beyond the Tier 2 cycle. |
| R4 | **Loosening `push_parent_ok`** (accept two parents) or adding a `kind` parameter | It exists so a fast-forward push cannot publish extra local commits (`fsm.py:585-587`); a looser check weakens the fix path for the sake of the sync path and breaks the pinned `merge` test id. A sibling function cannot weaken the old one. | Never. |
| R5 | **Reusing `evaluate_push_decision`** with `applied_edits := files changed` | Predicate 5 means "grounded finding edits" (INV-016); overloading it makes the audit record lie. | Never. |
| R6 | **Dispatch to `/sc:troubleshoot`** | Troubleshoot diagnoses defects from a finding seed (`refs/troubleshoot-dispatch.md`); a merge conflict is not a defect to diagnose, and the seed shape (issue, scope, type) adds ceremony without evidence. | None. |
| R7 | **mergiraf**, `suggest-pr-split`, `meta-route`, `categorize-conflicts` as scripts, `conflict-status`, sbse recombine (R-64 to R-73, R-37 to R-39, R-23 to R-25, R-40 to R-50, R-101) | New external dependency (forbidden by the seed), or routing frameworks that duplicate a 40-line pure function; scored 1 to 6 by the research. | A measured Tier 2 failure rate above an agreed bar. |
| R8 | **`gh pr update-branch`** for behind-only | Server-side merge produces a head the local checkout does not have and skips local VAL; it cannot resolve conflicts anyway. | A maintainer wants a no-checkout path for Tier 0 only. |
| R9 | **A user-override channel** (R-19, R-20) | The skill is attended but has no override prompt; any "override" is a re-run with a different flag. Adding a mid-run override creates an unreviewed authority path. | None. |
| R10 | **Blanket side-taking and hard resets** (R-13, R-14, R-15) as options | Forbidden outright (FR-21). | Never. |
| R11 | **Global git config changes** (`merge.conflictStyle`, `rerere`) | Seed constraint. Use per-invocation `-c merge.conflictStyle=zdiff3` and `-c rerere.enabled=false` (R-128 forbids silently replaying a historical resolution). | None. |
| R12 | **Rebasing the PR branch** | Rewrites a published head and needs a force-push. | Never. |
| R13 | **Arbitrary conflict-count abort thresholds** (R-33 to R-36) | Scored 1 to 3. A single cost guard `TIER2_MAX_FILES` is kept instead, as a tunable constant. | After 10 real runs. |
| R14 | **Whitespace check `git diff --check --cached`** (R-161, ROI 6) | VG-3 and VG-4 already cover format; inherited whitespace in merged base content would trigger unrelated cleanup, which R-169 forbids. | None. |

### 3.3 Net effect on the primitive inventory

<!-- Source: Base (original, modified): counts updated per Changes #2, #10 and #25 -->

| Surface | Before | After |
|---|---|---|
| Core modules in `pr_submit/` | 11 files | +1 (`conflicts.py`); `ci.py` gains one keyword (`expect_checks`) |
| Refs | 11 | +2 (`conflict-mechanical.md`, `conflict-intent.md`) |
| Scripts | 4 | +2 in P1 (`probe-merge.sh`, `finish-merge.sh`); `collect-conflict-evidence.sh` in P2 or inline; `poll-ci-checks.sh` gains `--evidence-sha` |
| Agents | no change | 0 new |
| Templates | no change | 0 new |
| Commands | `pr-submit.md` | one flag row, one Will Not clause |
| `fsm.py` | as is | P1: argument parser (about 6 lines) and two additive `build_push_triad` keyword arguments; P2: one `transition()` edge and the widened S5a clause at `fsm.py:1137` |
| `models.py` | 41 events | 43 events (Tier 2 event set OPEN) |
| FSM states | 23 | 23 |
| FSM edges | as is | +1 in P2 |
| Python blocks in `SKILL.md` | 1 | 1 |

### 3.4 Core API (`superclaude.pr_submit.conflicts`)

<!-- Source: Variant A (opus:architect), Section 7 (A:363-451) and FR-C6 (A:473): merged per Change #5; MechanicalRule per Change #3 (A:391-407); merge_preflight_ok per Change #12; crash_resume_plan per Change #10 (inv-A); is_conflict_cycle per Change #21; classify_checks keyword per Change #25 -->

Pure module: no I/O, no `anthropic` import (T-N41), no `git` / `gh` token anywhere including docstrings (T-N50), standard library only. Every function fails closed on malformed input. Public names are re-exported from `superclaude/pr_submit/__init__.py`.

**Data.**

```python
SYNC_CAP = 1
TIER2_MAX_FILES = 8

@dataclass(frozen=True)
class MechanicalRule:                 # the extension point: adding a rule is one row plus one test row
    pattern: str                      # repo-root-anchored path (never a bare basename; closes INV-025)
    kind: str                         # "lockfile" | "generated"
    sources: tuple[str, ...]          # paths the output is derived from; empty -> Tier 3
    regenerate: tuple[str, ...]       # argv, e.g. ("uv", "lock")
    check: tuple[str, ...] = ()       # argv, e.g. ("uv", "lock", "--check")

MECHANICAL_RULES: tuple[MechanicalRule, ...] = (
    MechanicalRule("uv.lock", "lockfile", ("pyproject.toml",), ("uv", "lock"), ("uv", "lock", "--check")),
)
```

The one shipped rule matches only the repository-root `uv.lock` with stage set `123`, and applies only when that path is tracked and `uv` resolves on PATH (inv-B INV-033); the skill passes both facts in. A rule's `regenerate` and `check` argv must start with a program the skill's `allowed-tools` already permits (`SKILL.md:4`); the allowed-tools test covers every new inline command and every rule program (A-004).

**Functions.**

| Function | Contract |
|---|---|
| `parse_stage_records(text, *, nul=True) -> list` | Parses the probe's raw `<mode> <oid> <stage>\t<path>` records (NUL- or newline-separated). Raises `ValueError` on a bad mode, a non-40-hex oid, a stage outside 1..3, an empty path or a duplicate `(path, stage)`. Tested against the captured fixture `fixtures/merge_tree_conflict.z`. |
| `mergeability_hint(mergeable, merge_state)` | Normalises the GitHub fields to `conflicting`, `behind`, `clean`, `unknown` (FR-24). |
| `classify_conflicts(entries, *, conflict_max_tier, rules=MECHANICAL_RULES, tier2_max_files=TIER2_MAX_FILES)` | Section 4.2: per-path class, run tier, action hint, reasons. |
| `conflict_action(*, tier, ordinal, hook, entering_outcome, budget, conflict_max_tier, ...)` | The single router for every conflict decision (replaces routing spread over sections 5.4, 5.5 and 6.3 in earlier drafts, NE6). Inputs: tier x ordinal x hook (`wave0`, `C-initial`, `wave8a`) x entering outcome x budget x cap. Returns the action of sections 5.4 and 5.5 (`none`, `report`, `propose`, `resolve_local`, `resolve_push`, `halt`) with a reason (`conflict_tier3`, `late_conflict`, `tier_above_cap`, ...). Any unknown or out-of-range input reaches a fail-closed default row (halt). Pinned by an exhaustive reachable-row test (QA-4). |
| `merge_parent_ok(parents, pre_push_sha, base_sha) -> bool` | Section 6.2. |
| `merge_preflight_ok(porcelain) -> (bool, list[str])` | True only when `git status --porcelain=v1 --untracked-files=no -z` output is empty; otherwise false with the dirty tracked paths (section 6.4 step 2). Untracked files are tolerated. |
| `evaluate_sync_decision(...)`, `sync_fail_state(decision)` | Section 6.3, for both conflict tiers. |
| `crash_resume_plan(dangling, branch)` | The pure resume function: for kinds `sync` and `ci` returns a resume directive (enter the Wave 8 CI wait with `source=ci`, `wait_sha`, the preserved terminal), never `S4_PUSHING`, S5a or S5; kinds `fix`, `merge` and absent keep today's outputs byte-equal; a missing terminal fails closed (section 5.8). |
| `is_conflict_cycle(cycle_id) -> bool` | True for the reserved prefixes `sync-` and `conflict-` (section 5.7). |
| `resolution_record_ok(record) -> list[str]` | Section 6.6; empty list means valid. |

Related change outside this module: `superclaude.pr_submit.ci.classify_checks(payload, *, wait_sha=None, expect_checks=False)` (section 6.10). `ci.py` stays in the T-N50 set; `gh` stays out of the core.

## 4. Tier model: process cost grows only with conflict complexity

### 4.1 Cost ladder

<!-- Source: Base (original, modified): Tier 0 cost per Change #6 (GitHub first); acting sites and round cost per Changes #1 and #8 -->

| Tier | Meaning | Calls | Model reasoning | Agent spawn | Pushes |
|---|---|---|---|---|---|
| 0 | No conflict (clean, behind only, or `BLOCKED`) | the Wave 0 local operation check and one `gh pr view` read (up to 3 re-reads on `UNKNOWN`); no fetch, no probe | none | none | none (report only) |
| 1 | Mechanical: every conflicted path matches a `MechanicalRule` | Tier 0 calls + `probe-merge.sh` + `merge`, `uv lock`, `uv lock --check`, `add`, `finish-merge.sh`, VAL at Wave 8a | none | none | one merge commit, no round |
| 2 | Text or tree conflicts resolved by stated intent (P2) | Tier 1 calls at `C-initial` + the evidence reads per file (`collect-conflict-evidence.sh` or inline) | one intent statement pair per file | one `evidence-validator` | one merge commit, one round, reviewers re-triggered |
| 3 | Semantic or high-risk, or anything unclassifiable | Tier 0 calls + the probe; at L3 a halt at the end of Wave 0 | none after detection | none | none, halt |

### 4.2 Classification rule (pure, `classify_conflicts`)

<!-- Source: Base (original, modified): input from parse_stage_records per Change #7; rule 7 and the recipe note per Change #3; BLOCKED row per Change #4 (Variant C, C:55); GitHub-first row per Change #6; cap note per Change #15 with INV-012 marked OPEN -->

Input is the conflict entries that `parse_stage_records` builds from the probe's raw `-z` listing, grouped per path as `{path, stages, modes{base,ours,theirs}, binary}`, where `stages` is the string of index stages present (`"123"` both sides modified, `"13"` deleted by the base side and modified here, `"12"` the reverse, `"23"` added on both sides), `ours` is the PR branch and `binary` comes from the probe's binary list. Each path gets exactly one class from the **first matching rule** below; the tier is the maximum over paths. Any shape no rule recognises is `halt:unknown_shape` (fail closed).

| Order | Rule | Class | Source |
|---|---|---|---|
| 1 | any side mode `160000` | `halt:submodule` | R-43, R-56 |
| 2 | any side mode `120000` | `halt:symlink` | fail closed |
| 3 | modes differ between ours and theirs (mode-only or mode-plus-content) | `halt:mode_change` | fail closed |
| 4 | path matches the protected globs (`.github/workflows/**`, `.github/actions/**`, `.claude/settings.json`, `.claude/settings.local.json`) | `halt:protected` | blast radius of a bad CI or permissions file |
| 5 | path matches a migration pattern (`migrations/`, `alembic/versions/`, `db/migrate/`) | `halt:migration` | R-54, S-53 |
| 6 | `binary` is true | `halt:binary` | R-57 |
| 7 | path matches a `MechanicalRule` pattern (root-anchored; shipped: `uv.lock`), `stages == "123"`, the path is tracked and the rule's program resolves on PATH | `regen:<rule>` | R-58, R-189, J-48 |
| 8 | basename is a known lockfile name without a matching rule (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `Pipfile.lock`, `flake.lock`) or ends in `.lock` | `halt:lockfile_no_recipe` | R-59, J-48 (use only the manager the lockfile names) |
| 9 | path is under `generated/`, `dist/`, `build/` or matches `*.generated.*` and has no rule | `halt:generated_no_recipe` | R-59 |
| 10 | `stages == "123"` | `text:content` | R-149 |
| 11 | `stages in {"13","12"}` | `text:modify_delete` | R-154, S-39 |
| 12 | `stages == "23"` | `text:add_add` | S-40 |
| 13 | anything else | `halt:unknown_shape` | fail closed |

Tier assignment, applied after the per-path classes:

| Condition | Tier |
|---|---|
| GitHub reads `mergeable == MERGEABLE` (the probe is not run) | 0 |
| GitHub reads `mergeStateStatus == BLOCKED` with `mergeable == MERGEABLE` (its own parametrized row) | 0 |
| probe reports `clean` (no conflicts) | 0 |
| at least one `halt:*` class | 3 |
| number of `text:*` paths is greater than `TIER2_MAX_FILES` (default 8) | 3, reason `too_many_files` |
| at least one `text:*` class (regen paths may accompany them) | 2 |
| all paths are `regen:*` | 1 |

GitHub `CONFLICTING` with an empty local conflict set has no agreed action yet (OPEN, section 12, INV-022).

Notes that make the table safe and small:

- **No tree conflict is Tier 1.** A modify/delete or add/add only surfaces when both sides changed the path, so there is no purely mechanical answer (R-154 says "determine which intent supersedes"). They are Tier 2 with a mandatory kind label and a dropped-behaviour line. This rejects the idea of an "obvious-answer tree conflict" tier; revisit only if field logs show a repeating mechanical shape.
- **Rules are data.** The core holds `MECHANICAL_RULES` (section 3.4); each rule names its pattern, sources, regenerate command and check command. Adding a rule is one row plus one parametrized test row, not a new code path. A rule whose path is untracked, or whose program is not on PATH, does not match, and the path falls through to rule 8.
- **Manifest first (R-58).** When `pyproject.toml` also conflicts it is `text:content` (Tier 2); `uv lock` runs only after it is resolved and staged.
- **Cap by flag.** If `tier > conflict_max_tier` the plan's action is `report` with reason `tier_above_cap`; the plan still prints (FR-4). The route for a tier above the cap at L3 is OPEN (section 12, INV-012).

### 4.3 Exit criteria per tier

<!-- Source: Base (original, modified): Tier 1 preflight and VAL per Changes #11 and #12; Tier 3 site per Change #6 (R2-B M3) -->

| Tier | Exit to "commit" requires all of | Exit to "halt" when |
|---|---|---|
| 0 | n/a. Report "N commits behind, no conflicts" (or the `BLOCKED` reason) and continue. | n/a |
| 1 | (a) the tracked tree was clean (`merge_preflight_ok`) and the merge started with `MERGE_HEAD == base_sha`; (b) `uv lock` exit 0 and `uv lock --check` exit 0 after the manifest is final; (c) `finish-merge.sh` passes every guard; (d) Tier 1 VAL green (section 6.7) | recipe command fails, `--check` fails, any guard fails, VAL red after the one retry |
| 2 | everything in Tier 1 minus the recipe, plus: (e) for every `text:*` file a record entry with `kind`, one-sentence `ours_intent`, one-sentence `theirs_intent`, `resolution`, `behavior_after` and `dropped` (R-18, R-156, S-29); (f) `resolution_record_ok(record)` returns no problems; (g) `evidence-validator` confirms every entry; (h) no third behaviour (S-26) | an intent cannot be stated in one sentence (R-18), the kind is `semantic` by the high-suspicion checklist (R-180, R-251), the validator marks an entry unsupported after one revision pass, a file is unreadable (R-84), any Tier 1 halt condition |
| 3 | n/a. At L3, print the HALT message at the end of Wave 0 (FR-10); nothing started, nothing pushed. At L1 and L2, report. | n/a |

**Escalation is monotone.** A cycle that starts as Tier 1 or 2 may escalate to Tier 3 at any point; it never de-escalates, and it never retries a halted cycle in the same run. The cap on retries inside a tier is one revision pass (validator disagreement) and one VAL retry, matching the existing "a validation retry does not tick the round counter" rule (`SKILL.md:291`).

### 4.4 High-suspicion checklist for Tier 2 (R-180, R-251, S-26)

<!-- Source: Base (original) -->

Before resolving a `text:*` file the model must check, using the evidence bundle: does either side change a function signature, a type or schema, a dependency, a constant or env var, or a public API, while the other side adds or changes callers (R-180)? Does one side remove an old API or column while consumers remain (R-251)? A yes on any item makes the file `kind: semantic` and the cycle Tier 3. The model may use `git grep` for the symbol (R-181) as a read-only check.

## 5. Where it runs in the sc:pr-submit flow

### 5.1 Placement decision: detect early, act by tier

<!-- Source: Base (original, modified): placement restructured as the tier split per Changes #1 and #6; option A adopted for Tier 2 from Variant A (opus:architect), Section 5.1 (C-initial) -->

Three placements were weighed. The design uses two of them, one per acting tier, and detects for every tier at the end of Wave 0.

| Option | Fit | Verdict |
|---|---|---|
| **A. Act before the first review** (`C-initial`: Wave 1, after arming, before the first review poll) | Reviewers see a conflict-free head. A push moves the head, so reviewers must be re-triggered and the first wait run with the S5 attribution parameters (`pushed_sha`, per-reviewer watermarks), because completion is keyed to the expected head (G19). For a Tier 2 merge that is exactly what is wanted: the merge is authored code and must be reviewed (J-66). Cost: one FSM edge, the widened S5a clause, one round. | **Adopt for Tier 2 (P2).** |
| **B. Act after the review phase, before the CI wait** (Wave 8a) | One call site. Reuses the CI-phase precedent: SKILL-owned, no FSM edges, no re-trigger, no thread reply, CI re-polled on the new head (G12). Sees the *latest* base, so base drift during a long review is covered by construction. CI does not start on a conflicted PR (external), so resolving just before the CI wait is exactly where the wait would otherwise stall. | **Adopt for Tier 1 (P1).** |
| **C. Act only during the CI wait** (when CI reports nothing) | Latest information, but wastes the first `--timeout` window before noticing. | Keep only as the P3 re-sync trigger. |

**Detection runs early and read-only for every tier**, at the end of Wave 0 (L1+), so the operator sees the tier and the plan before any review round is spent:

1. **Unconditional local check first** (every L1+ run, whatever GitHub says): if `MERGE_HEAD`, a rebase or a cherry-pick is in progress, HALT (INV-004). This catches an L2 merge left in progress even when GitHub reads `MERGEABLE`. The check must run even when no ref is loaded, so its sentence lives in the `SKILL.md` Wave 0 text. The reason code is OPEN (`operation_in_progress`, `foreign_op_in_progress` or `merge_in_progress`); the default is `foreign_op_in_progress`, which matches the `foreign_op` naming (section 12).
2. **GitHub first:** read `mergeable` / `mergeStateStatus`. If `UNKNOWN`, re-read up to 3 times, 10 s apart.
3. **Local probe only on `CONFLICTING` or a persistent `UNKNOWN`** (section 5.3), then classify.
4. **Tier 3 at L3 halts here** (reason `conflict_tier3`), in the `SKILL.md:268` pre-Wave-1 shape: `terminal_halted` with a reason, appended to the run-log when one exists, plus operator text. It needs no run-log and no armed FSM. At L1 and L2 a Tier 3 conflict is reported and the run continues to review.

Cost of acting on Tier 1 at Wave 8a: a Tier 1 resolution arrives after the review phase has spent its rounds. That is acceptable because Tier 1 is mechanical, spends no round and needs no review; the halt or push is reported alongside the review outcome (same shape as a CI human-gate after `HALT_MAX_ROUNDS`, `SKILL.md:277`).

### 5.2 Wave table additions

<!-- Source: Base (original, modified): rows per Changes #1, #2 and #6 -->

```text
Wave 0 (end, L1+):   local operation check; GitHub read; probe + classify only on CONFLICTING or persistent UNKNOWN;
                     report the plan; Tier 3 at L3 halts here      <- loads refs/conflict-mechanical.md ONLY if the probe reports conflicts
C-initial (L3, P2):  Tier 2 merge cycle, in Wave 1 after arming and before the first review poll
                                                                    <- loads refs/conflict-mechanical.md and refs/conflict-intent.md
Wave 8a (L1+):       re-probe, then act per tier and ordinal       <- loads refs/conflict-mechanical.md
                     runs after the review phase settles, before the CI poll loop is entered
```

Neither ref is loaded when detection is Tier 0, so a normal PR pays for the local operation check and one `gh pr view` read, and nothing else. `refs/conflict-intent.md` loads only for Tier 2.

### 5.3 Detection and probe contract

<!-- Source: Base (original, modified): thin probe with raw -z listing per Change #7 (Variant A, AD-6); tree_clean replaces index_clean per Change #12; GitHub-first order per Change #6; base Appendix B exit contract folded in per Changes #7 and #24 -->

**GitHub read (inline, before the probe).** `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus`. `UNKNOWN` is re-read up to 3 times, 10 s apart. `MERGEABLE` (including `BLOCKED`) is Tier 0 with no probe. `CONFLICTING` or a persistent `UNKNOWN` runs the probe. A read failure yields `null` hints and the probe runs.

**Probe** (`scripts/probe-merge.sh --repo "$REPO" --pr <N> --base <base> --head-branch <HEAD_BRANCH>`). One JSON line on stdout; a non-zero exit is a prerequisite failure (reported, never retried as "polling"), the same convention as `SKILL.md:56-58`:

```json
{"ok": true, "merge_tree_supported": true,
 "base_ref": "origin/main", "base_sha": "<40hex>", "head_sha": "<40hex>", "merge_base": "<40hex>",
 "behind": 3, "ahead": 2,
 "foreign_op": null, "tree_clean": true,
 "clean": false,
 "stage_records": "<raw merge-tree --write-tree -z listing, NUL bytes JSON-escaped>",
 "binary_paths": []}
```

Rules:

- The script runs `git fetch origin <base>` (origin only; never another remote) and takes `base_sha` from `git rev-parse origin/<base>` after the fetch. `base` is the PR's own `baseRefName` from the GitHub read, falling back to the resolved `--base`.
- `merge_tree_supported` is set by a capability probe (`git merge-tree --write-tree` against `HEAD HEAD`), never by parsing a version number (`SKILL.md:225-230` pattern). If false, the probe returns `ok: true, clean: null` and the skill degrades to report-only using the GitHub fields.
- `foreign_op` is non-null when any of `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `sequencer` exists under `git rev-parse --git-path` (worktree-aware, J-16, J-17, S-05).
- `tree_clean` is true only when `git status --porcelain=v1 --untracked-files=no -z` is empty. Untracked operator files are tolerated (git itself refuses a merge that would overwrite them); any staged or unstaged tracked change is not, because `uv lock` and VAL read the worktree and the commit must equal the tree that was validated (INV-008).
- `stage_records` is the raw listing, unparsed; `parse_stage_records` in the core parses it (section 3.4). The probe does no classification.
- Once the probe has run, local `merge-tree` is the source of truth for action; a disagreement with GitHub is reported as `github_disagrees`.
- The script performs no worktree or index mutation. It may leave unreachable tree objects (documented, harmless).

**Script exit contract** (for the implementer):

| Script | Success | Failure tokens (stdout, one line) | Exit |
|---|---|---|---|
| `probe-merge.sh` | the JSON above | `PROBE_FAIL <reason>` (missing `--repo`, not a git worktree, fetch failed) | 0 / 2 |
| `collect-conflict-evidence.sh` (P2, if not inline) | `{"dir": "<path>", "files": [...], "truncated": false}` | `EVIDENCE_FAIL <reason>` | 0 / 2 |
| `finish-merge.sh` | `{"merge_sha": "<sha>", "parents": ["<ours>", "<base>"]}` | `FINISH_FAIL unmerged` / `markers` / `staged_unexpected` / `foreign_merge` / `hook_rejected` / `no_merge_head` / `tree_dirty` | 0 / 2 |

None of the scripts reads stdin, prompts, or writes outside the repository's own git directory and the given output directory.

### 5.4 Behaviour by tier and ordinal

<!-- Source: Base (original, modified): replaced by the one-acting-site-per-tier table per Change #6 (R2-B M4); L2 status rule per Change #6 (INV-003); Tier 2 edge from Variant A (opus:architect), Sections 5.3-5.4 per Changes #1 and #8; open items INV-010, INV-011, INV-012 carried -->

| Tier | L1 | L2 | L3 |
|---|---|---|---|
| 0 | report only | report only | report only |
| 1 | report, PROPOSE | resolve at Wave 8 entry, stop uncommitted | push (Wave 8a) |
| 2 | report, PROPOSE | resolve at Wave 8 entry, stop uncommitted | `C-initial`; first seen at `C-ci` (Wave 8a) -> halt `late_conflict` |
| 3 | report | report | Wave 0 halt |

**L0:** nothing. The FSM never leaves `S0_IDLE`; the L0 sentence and AC-1 stay byte-identical (`test_static_grep.py:650-653`). No hook is reached.

Details per acting site:

- **End of Wave 0 (L1+):** probe and classify when GitHub requires it, then print the plan (R-51): tier, per-path class and reason, what would run. No merge, no edits. Tier 3 at L3 halts here.
- **L1 at Wave 8a:** re-probe; print the plan again only if the tier or paths changed. Proposes "resolve these? y/n" for Tier 1 and 2 (same shape as the `PROPOSED` state) and applies nothing.
- **L2 at Wave 8a, Tier 1 and 2:** perform the local resolution through VAL, then **stop with the merge in progress and uncommitted** (no commit, no push, no reply). The caller sets `S4'_HALT_BEFORE_PUSH` (`fsm.py:1118-1121`, status `halt_before_push`) only when Wave 8 was entered from `clean` or `REPORT_ONLY`. Entered from `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, L2 reports only and keeps the preserved terminal status (INV-003).
- **L3 at Wave 8a, Tier 1:** full cycle through commit and push (section 6.4), then continue to the CI wait on the new head with `expect_checks` (section 6.10).
- **L3 at `C-initial`, Tier 2 (P2):** send `transition(S2_CLASSIFY, "conflicting")`. The edge has the same round gate as `(S2_CLASSIFY, "findings")`: a spent budget gives `HALT_MAX_ROUNDS`; otherwise `S3_FIXING`. The cycle then runs the tier procedure in `S3_FIXING`, VAL in `S7_VALIDATING`, the publish path in `S4_PUSHING`, `S6_REPLYING` and `RESOLVING` with zero threads, the S5a re-trigger and the S5 wait (section 5.6). That S5 wait is the run's first review wait.
- **L3, Tier 2 first seen at Wave 8a:** halt `late_conflict`. The `(S2_CLASSIFY, "conflicting")` edge exists only from `S2_CLASSIFY`, not from a preserved terminal, so a uniform halt avoids two behaviours for one input.

Open items on this table (section 12): at L2 a Tier 2 conflict first seen at Wave 8a is resolved locally while L3 halts (INV-010, three options); a tier that rises between Wave 0 and a later hook has no specified route (INV-011); the route for a tier above the cap at L3 (INV-012).

Why L2 ends the run instead of continuing: a worktree mid-merge breaks the later fix cycle (the fix commit uses `git commit --only`, which git refuses during a merge, and `OPERATOR_PENDING` would flag every merged file). Wave 8a is the last mutating phase, so ending there loses nothing. The merge in progress is *ours*, recorded by `sync_started`, so a re-run recognises it (FR-17); the unconditional Wave 0 check (section 5.1) halts before anything else runs.

### 5.5 Wave 8a gate on the Wave 8 arming outcomes

<!-- Source: Base (original, modified): Tier 1 acts on all four armed outcomes per Change #6 (R2-B M2, INV-003); status preservation from R2-C QA-5; CI-wait skip inserted per Change #14 (Variant A, A:220, FR-C23) -->

| Review outcome entering Wave 8 | Wave 8a action |
|---|---|
| Augment `clean` / `REPORT_ONLY` (merged clean or findings reported) | Acts per section 5.4. Tier 1 acts **regardless of `round_counter`** (it consumes no round). A Tier 2 conflict first seen here halts `late_conflict` at L3. |
| `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE` (wait-only paths, `ci_wait_autofix` false) | Tier 1 acts at L3 (the single sync push is the one exception to the wait-only rule, section 6.9). The report shows the preserved Augment status with the sync outcome alongside, exactly as for a CI human-gate (`SKILL.md:250`); the status enum gains no member. L2 reports only and keeps the preserved terminal (section 5.4). L1 proposes. |
| `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` / L0 | Wave 8 is not armed, so Wave 8a does not run. The early Wave 0 report already informed the operator. |

On a Tier 3 halt found by the Wave 8a re-probe after an ordinary review outcome, the FSM takes the existing human-gate route to `HALT_HUMAN`; after `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` the retained terminal status is preserved and the halt is reported alongside it, exactly as for a CI human-gate (`SKILL.md:277`). No new FSM edge is needed for Tier 1 or Tier 3. The general rule for a tier that rises between hooks is OPEN (section 12, INV-011).

**`pr_conflicting` CI-wait skip (INV-024).** When Wave 8 is entered on a still-conflicting PR and no merge is pushed (L1, L2, a tier above the cap, or a preflight halt), skip the CI wait with reason `pr_conflicting` instead of polling until `--timeout`. GitHub runs no `pull_request` workflows on a conflicting PR, so the wait could otherwise read empty check lists.

### 5.6 Interaction with rounds, caps and reviewers

<!-- Source: Base (original, modified): rounds, caps and re-trigger per tier per Change #8 (Variant A, Sections 5.4-5.5; R2-B M5; R2-C QA-3); counting per Change #16 (R2-B M6, R2-C QA-1/QA-2, INV-018) -->

| Item | Behaviour |
|---|---|
| `round_counter` / `max_rounds` | **Tier 1 (`kind: "sync"`):** untouched. The counter ticks only on `S5 -> S2` (`state-machine.md` section 5.1 and INV-001); Wave 8a never enters S5. **Tier 2 (`kind: "merge"`, P2):** ticks `round_counter` once, on the INV-001 edge, when the re-review of the merge push is attributed. The `(S2_CLASSIFY, "conflicting")` edge applies the round gate first. |
| `push_count` (contract: `SKILL.md:239` "== `max_rounds` at most" and INV-R2 `push_count <= max_rounds + 1` at `SKILL.md:275`) | Excludes kind `sync` only. Fix pushes and Tier 2 merge pushes count. The `rebuild_state` fold at `run_log.py:238-239` becomes kind-aware, and `SKILL.md:239` is reconciled with `:275` (INV-018). |
| `sync_push_count` | New field; counts landed `kind: "sync"` pushes; at most `SYNC_CAP`. Pushes-by-kind are reconstructible from the report through this field plus `push_kind` on the records (QA-2). |
| `SYNC_CAP` | 1 sync cycle per run. Counted from `sync_started` events via `rebuild_state()["sync_cycles"]`. The cap is evaluated by `evaluate_sync_decision`. Which per-run bound applies across both tiers (Tier 2 `<= 1` plus Tier 1 `SYNC_CAP = 1`) is OPEN (section 12, INV-019). |
| Reviewer re-trigger | **Tier 1:** none. A sync push does not call `retrigger-review.sh` and writes no `rereview_requested`, mirroring the CI-phase push (`SKILL.md:277`: "do not call `retrigger-review.sh`, reply, or resolve"). Reviewers never see a Tier 1 `M`; the commit body is the human-visible audit (FR-11). **Tier 2 (P2):** the S5a step re-triggers. Widen the S5a trigger in `fsm.py:1137` and `SKILL.md:274` to `applied_edits > 0 or kind == "merge"`, placed between the pins at `test_static_grep.py:689` and `:750`, which stay unchanged (NE-C3). Add a new static pin for the widened sentence and the zero-edit-pair behavioural test: a zero-edit merge cycle re-triggers, a zero-edit fix cycle still does not (QA-3). At `C-initial` no reviewer has been observed yet, so the re-trigger targets the *configured* reviewers; pin that substitution (INV-030, in part). |
| `rereview_request_count` | Tier 1: unchanged. Tier 2: +1 per merge cycle (folded by `cycle_id`). |
| Thread reply / resolve | Tier 1: none (there are no threads in a sync cycle). Tier 2: `S6_REPLYING` and `RESOLVING` run with zero threads. |
| Impact warning (`sc:impact-protocol`) | Not invoked; the advisory VG-1 test suggestion in VAL already covers changed areas. |
| Late conflict while polling CI (P3) | If the CI poll payload carries `merge_state` CONFLICTING, or the CI wait is stuck at `polling` with no checks and GitHub reports CONFLICTING, run Wave 8a once more (subject to `SYNC_CAP = 1`, so only when no sync push landed earlier in the run; Tier 0 and 1 only: a late Tier 2 halts with reason `late_conflict`). |

### 5.7 Run-log events, push kinds and write-ahead order

<!-- Source: Base (original, modified): push kinds per Change #10 (INV-001, INV-002); cycle-id prefixes per Change #21 (A-005, QA-8); Tier 2 event set marked OPEN per the unresolved diff point C-029/X-011; halt reasons per Changes #6, #12, #18 -->

Exactly two new `EventType` members (41 to 43) for Tier 1:

| Event | Written | Payload |
|---|---|---|
| `sync_started` | before the merge command (write-ahead) | `run_id, cycle_id, base_ref, base_sha, pre_push_sha, tier, conflict_max_tier, paths` |
| `sync_concluded` | when the cycle ends | `cycle_id, outcome` in `{pushed, left_in_progress, aborted, halted, report_only}`, `merge_sha` or null, `record_path`, `dropped` (list of strings) |

**Tier 2 (P2) events: OPEN** (C-029 / X-011). Competing positions: A adds `conflict_classified` / `conflict_resolved`; C adds three events (44); inv-B adds no new event type in P1. Whatever the final count, apply QA-6's pin sweep: both `len(EventType)` pins, the `models.py:23` docstring and a `grep` of `tests/` for `== 41`.

**Push kinds.** `kind` in `{fix, merge, sync, ci}` goes on all three push records (`push_decision`, `push_initiated`, `push_completed`) through `build_push_triad(..., push_kind=..., base_sha=...)`. It defaults to `fix` when absent, so legacy logs read as today. `push_initiated` for `sync` and `ci` also records the preserved review terminal (inv-B). The recovery key tuple (`recovery.py:98-110`) gains `kind`.

**Cycle ids.** The prefixes `sync-` (Tier 1) and `conflict-` (Tier 2) are reserved; the pure `is_conflict_cycle` recognises them, and one test proves the fix-cycle id rule can produce neither prefix (the INV-R1 fold at `run_log.py:200-206` counts each `cycle_id` once).

Order for an L3 Tier 1 cycle: `sync_started` -> (merge, resolve, VAL, commit) -> `push_decision{kind: sync}` -> `push_initiated{kind: sync}` (fsynced before the push) -> push -> `push_completed{kind: sync}` -> `sync_concluded{pushed}`. Halts append `sync_concluded{halted}` (when a cycle started) then `terminal_halted{reason}` with these new reasons: `conflict_tier3`, `foreign_op_in_progress` (name OPEN, section 5.1), `merge_preflight_dirty`, `sync_foreign_operation`, `sync_merge_failed`, `sync_marker_left`, `sync_unmerged_left`, `sync_staged_unexpected`, `sync_commit_failed`, `sync_head_mismatch`, `sync_range_mismatch`, `sync_base_moved`, `sync_cap`, `late_conflict`, `push_rejected`, `resume_unrepresentable`. No other event type is added (reasons are free-text fields of an existing event, like `pr_head_mismatch`).

### 5.8 `--resume` crash recovery

<!-- Source: Base (original, modified): dangling-push row replaced by the kind-aware resume rule per Change #10 (inv-A, inv-B, inv-C INV-001; C:83 C-030); base B:299 withdrawn; rejected-record rule per Change #18 (INV-035); INV-005 carried as OPEN -->

Recovery has these mid-cycle states, each decidable from the run-log plus read-only git state.

| Observed on resume | Meaning | Action |
|---|---|---|
| `sync_started` with no `sync_concluded`, no `push_initiated` for the cycle, `MERGE_HEAD` exists and equals the recorded `base_sha` | Our merge was interrupted before commit | Continue the cycle: re-read the probe, resume Tier 2 at the first path still unmerged (J-40 one file at a time), then finish. |
| `MERGE_HEAD` exists but no matching `sync_started` (or a different sha) | Someone else's operation | HALT `sync_foreign_operation`. Never touch it (J-17). |
| `sync_started`, no `MERGE_HEAD`, local `HEAD == pre_push_sha` | The merge never started or was aborted | Restart the cycle; nothing to undo. |
| `sync_started`, local `HEAD` is a 2-parent commit `[pre_push_sha, base_sha]`, no `push_initiated` | Crash between commit and push | Re-run the pre-push guard, then the triad and push. Whether to re-run `finish-merge.sh` and VAL first is OPEN (section 12, INV-005). |
| Dangling `push_initiated` with `kind` `sync` or `ci` | The existing three-way crash window, CI phase | `crash_resume_plan` returns a resume directive. **Branch A** (landed): append `push_completed{recovered, kind}` and enter the Wave 8 CI wait with `source=ci`, `wait_sha = target_sha` and the preserved terminal. **Branch B** (not landed): re-run the Wave 6 pre-push guard, plus `merge_parent_ok` with the record's `base_sha` for `sync`, push the recorded `target_sha`, then take the same directive. Never `S4_PUSHING`, S5a or S5. A missing terminal fails closed with `resume_unrepresentable`. **Branch C** halts as today. |
| Dangling `push_initiated` with `kind` `fix`, `merge` or absent | The existing crash window, review phase | Today's outputs, byte-equal. |
| A `push_aborted_or_not_landed` record marked `rejected: true` | A rejected live push (section 6.4 step 12) | Branch B never re-drives it; the run stays halted `push_rejected`. |

The earlier rule "Branch A of a sync returns `S2_CLASSIFY`" is withdrawn: it would wait for a review that is never requested. The recovered `push_completed` copies `kind` and `base_sha` (a two-key extension of the fixed tuple at `recovery.py:98-110`), so the `rebuild_state` fold counts it under the right kind. The `expect_checks` value recorded for the push is reused on resume (section 6.10).

## 6. Publishing the resolution without a force-push

### 6.1 Why a merge commit, and why it is safe

<!-- Source: Base (original) -->

Integrating the base into an already-published PR head without rewriting history means exactly one thing: a merge commit on the PR branch. Its parents are `[pr_head, base_tip]`, so `pr_head` is an ancestor of `M` and `git push origin M:<HEAD_BRANCH>` is a plain fast-forward. Nothing is rewritten; rollback is a normal revert commit (`git revert -m 1 M`, recorded in the ref for the operator).

The reason `push_parent_ok` forbids extra commits is that a fast-forward publishes every commit between the PR head and the target (`fsm.py:585-587`). For `M` that risk is bounded by construction: the only commits `M` adds to the PR branch besides itself are ancestors of `base_sha`, which is a commit that was just fetched from `origin/<base>` and therefore already exists on the remote. The exact parent rule below pins that.

### 6.2 Exact parent rule: `merge_parent_ok`

<!-- Source: Base (original, modified): the recorded base_sha source generalized from sync_started to the cycle's write-ahead record, for consistency with the Tier 2 cycle of Change #1 -->

```text
merge_parent_ok(target_parents, pre_push_sha, base_sha) -> bool
  true iff ALL hold:
    target_parents is a list with exactly 2 entries
    pre_push_sha and base_sha are str and each matches [0-9a-fA-F]{40} in full
    both parents are str and each matches [0-9a-fA-F]{40} in full   (no whitespace, no short ids)
    target_parents[0].lower() == pre_push_sha.lower()               (first parent is the PR head)
    target_parents[1].lower() == base_sha.lower()                   (second parent is the recorded base tip)
    pre_push_sha.lower() != base_sha.lower()
  anything else (None, wrong type, 0/1/3 parents, swapped order, bad id) -> false
```

Properties the tests must assert: `push_parent_ok` returns false for every input `merge_parent_ok` accepts, and `merge_parent_ok` returns false for every input `push_parent_ok` accepts (disjoint by parent count), so a mis-routed commit can never pass the other check. `base_sha` is the value recorded in the cycle's write-ahead record (`sync_started` for Tier 1), never re-read from a ref.

### 6.3 The sync decision: `evaluate_sync_decision`

<!-- Source: Base (original, modified): one sibling gate for both tiers per Change #9 (R2-B M5); cross-gate property test per R2-B A-B1; flag name per Change #15 -->

A sibling of `evaluate_push_decision` (which stays untouched), covering both conflict tiers and returning a `SyncDecision` dataclass with one flag per predicate, evaluated immediately before the push:

| Predicate | Holds when |
|---|---|
| `s1_ordinal` | `monitor_ordinal >= 3` |
| `s2_validated` | `validation_status == "validated"` |
| `s3_tier_allowed` | `tier in (1, 2)` and `tier <= conflict_max_tier` and no halt reason is set |
| `s4_under_cap` | Tier 1: `prior_sync_cycles < SYNC_CAP` (count of earlier `sync_started`, excluding this cycle). Tier 2: under the per-run merge bound (section 12, INV-019) **and** `round_counter < max_rounds` |

`authorized` is the conjunction. `sync_fail_state(decision)` maps a block: `s3` false -> `HALT_HUMAN`; `s4` false -> report-only (`sync_cap`); `s1` or `s2` false -> report-only. There is deliberately no `applied_edits` predicate anywhere in the merge path; the audit record names the four predicates (`p1_ordinal`, `p2_validated`, `p3_tier_allowed`, `p4_under_cap`) and carries `kind` (`sync` or `merge`). A cross-gate property test checks that `evaluate_sync_decision` and `evaluate_push_decision` agree on their shared predicates (ordinal, validated).

### 6.4 Procedure, step by step

<!-- Source: Base (original, modified): tree-clean preflight and post-commit assertions per Change #12 (Variant A, A:288; INV-008); triad keyword arguments per Change #10; rejected-push handling and merge-method advisory per Change #18 (A-001, INV-035); "grounding checked" per weakness W20; guard order kept and marked OPEN (X-009); post-push CI per Change #25; exit tokens per Change #7 -->

Applies to Tier 1 at Wave 8a and Tier 2 at `C-initial` (P2). L2 stops after step 8; L1 never starts.

| Step | Action (exact) | Fail behaviour |
|---|---|---|
| 1 | Re-read the PR head (`gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository`) and require `pr_head_ok(<local branch>, <local HEAD sha>, headRefName, headRefOid, isCrossRepository)` (local `HEAD` is the live PR head), `headRefName == HEAD_BRANCH`, and local `HEAD == pre_push_sha` (the stored value), so an unpublished local commit can never become the first parent of `M`. Also require `HEAD_BRANCH != <base>` (J-26) and that the checkout is the current worktree (J-91). | `terminal_halted` reason `sync_head_mismatch`; nothing started. |
| 2 | Run `probe-merge.sh` again (fresh `base_sha`, fresh classification). Require `foreign_op == null` (J-17) and `merge_preflight_ok` on the tracked tree: `git status --porcelain=v1 --untracked-files=no -z` empty, untracked files tolerated (J-18, INV-008). Plan = `classify_conflicts(...)`. | `sync_foreign_operation`; or HALT `merge_preflight_dirty` naming the dirty files, in the shape of the `fix_commit_failed` message: commit or discard your own changes, never stash (J-20). Nothing merged. |
| 3 | Append `sync_started{...}` (write-ahead). The Tier 2 write-ahead event is OPEN (section 5.7). | n/a |
| 4 | `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>` (by SHA, so the target cannot move; per-invocation `-c`, no stored config; `rerere` off so no historical resolution is replayed, R-128; no `--no-verify`). Exit 0 with `MERGE_HEAD` present means a clean merge (possible if the base changed again); exit 1 with unmerged paths is the expected conflict; exit 1 with no `MERGE_HEAD` means git refused (local changes would be overwritten). | Refusal: `sync_merge_failed`, nothing started, message lists git's own file list and says to commit or discard those files yourself. |
| 5 | Resolve per tier. Tier 1: re-assert the clean tracked tree right before the regenerate (`finish-merge.sh` performs this re-check), then the rule of section 6.5 (seed the one named lock file from the PR side, `uv lock`, `uv lock --check`, `git add -- uv.lock`). Tier 2: one file at a time, `git add -- <path>` (or `git rm -- <path>` for a deletion) as each is finished (J-40, J-56). Never `git add -A`, `git add .`, `--ours .`, `--theirs .`, `-X ours`, `-X theirs`, `-s ours` (FR-21). | Any halt condition: if the resolution is not complete, `git merge --abort` (allowed only because `MERGE_HEAD == base_sha` is verified) and `sync_concluded{aborted}`; the worktree is restored (section 6.8). A dirty tracked tree at the re-check: `merge_preflight_dirty`. |
| 6 | Tier 2 only: write `resolution.md` (format in 6.6), run `resolution_record_ok`, then spawn `evidence-validator` once over `resolution.md` and the evidence directory; its grounding check covers every entry. One revision pass allowed. | Unsupported after the revision pass: abort, Tier 3 `sync_tier3`. |
| 7 | VAL (section 6.7). | Red after the single retry: abort or leave per 6.8, `terminal_halted` via the existing `VALIDATION_FAIL` route. |
| 8 | **L2 stops here:** `sync_concluded{left_in_progress}`, the caller sets `S4'_HALT_BEFORE_PUSH` and reports `halt_before_push` (only when Wave 8 was entered from `clean` or `REPORT_ONLY`; section 5.4), and tells the operator: "The merge of `origin/<base>`@<base_sha> is resolved and validated but not committed. Review it, then run `git commit` yourself and push; or `git merge --abort`." | n/a |
| 9 | `scripts/finish-merge.sh` with the recorded `base_sha`, the resolved-paths list and the commit-message file (6.6). It verifies: `MERGE_HEAD == base_sha`; `git diff --name-only --diff-filter=U` empty; no conflict markers **introduced** in resolved paths (count of marker lines in the result must not exceed the count in the stage-1 blob, so legitimate documentation examples pass; R-11); staged paths are a subset of (files changed on the base side since the merge-base) union (resolved paths); then `git commit -F <msg>` with hooks on. After the commit it asserts both `git status --porcelain=v1 --untracked-files=no -z` empty and `git diff --quiet HEAD`, so VAL ran on exactly the committed tree. It prints `{merge_sha, parents}` (exit contract in section 5.3). | Hook rejection (`FINISH_FAIL hook_rejected`): output reported verbatim (J-61), no amend (J-63: the merge commit does not exist yet), `sync_commit_failed`, merge left in progress with resolution intact. Any other guard failure: `sync_marker_left`, `sync_unmerged_left` or `sync_staged_unexpected`; a post-commit tree check failure (`FINISH_FAIL tree_dirty`): `merge_preflight_dirty` naming the files, nothing pushed. |
| 10 | Set `target_sha := merge_sha`. **Pre-push head guard, in this order** (base order kept; OPEN, section 12, X-009): (a) re-read the PR head and require `pr_head_ok(<local branch>, pre_push_sha, ...)` and `headRefName == HEAD_BRANCH` (compare the stored `pre_push_sha`, never local HEAD); (b) read `git rev-list --parents -n 1 <target_sha>`, drop the first id, require `merge_parent_ok(<parents>, pre_push_sha, base_sha)`; (c) require `git merge-base --is-ancestor <base_sha> origin/<base>` after a fresh `git fetch origin <base>` (the second parent is still on the real base). Before the first merge push of the run, also read `mergeCommitAllowed`, `rebaseMergeAllowed` and `squashMergeAllowed` as an advisory report line; never halt on an unreadable value. | (a) `sync_head_mismatch`; (b) `sync_range_mismatch`; (c) `sync_base_moved`. All: nothing pushed, no push record, the local merge commit named in the message so the operator can drop or push it. |
| 11 | Core DECIDES: `evaluate_sync_decision`, then `build_push_triad(..., push_kind=<"sync" or "merge">, base_sha=<base_sha>)` writes `push_decision` -> `push_initiated` (fsynced before the push; for `sync` it also records the preserved review terminal) -> `push_completed`, keyed on the existing pre-push key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` (`cycle_id` is a fresh `sync-<n>` or `conflict-<n>` id; the key format is reused as is). | Blocked decision: `sync_fail_state`, nothing pushed. |
| 12 | `git push origin <target_sha>:<HEAD_BRANCH>` (never an upstream or parent remote, never the default or protected branch, never forced). Then `pre_push_sha := target_sha`. After the push, report `mergeStateStatus == BLOCKED` with a reason line when GitHub shows it. | git rejecting a non-fast-forward is the backstop if the PR head moved after the guard, exactly as for fix pushes (`SKILL.md:305`). A rejected live push appends `push_aborted_or_not_landed{rejected: true, stderr_tail}` and halts `push_rejected`; recovery never re-drives it (section 5.8). |
| 13 | **Tier 1:** append `sync_concluded{pushed, merge_sha}`. Re-enter Wave 8 with `wait_sha = target_sha` and `expect_checks` set for this push (section 6.10): switch to `poll-ci-checks.sh`, re-poll CI on the new head. No re-trigger, no reply, no resolve. **Tier 2:** `S6_REPLYING` and `RESOLVING` with zero threads, then the S5a re-trigger and the S5 wait (section 5.6). | n/a |

### 6.5 Tier 1 recipe detail (`uv.lock` rule)

<!-- Source: Base (original, modified): recipe expressed as the uv.lock MechanicalRule with its applicability conditions per Change #3 (inv-B INV-033) and the clean-tree re-check per Change #12 -->

The rule applies only when the root `uv.lock` is tracked and `uv` resolves on PATH (section 4.2 rule 7).

1. Resolve all non-lock conflicts first (none in Tier 1; a `pyproject.toml` conflict makes the cycle Tier 2).
2. Re-assert the clean tracked tree (step 5 of section 6.4). Seed the one named file from the PR side with `git checkout --ours -- uv.lock`. This is a single explicit path, not the forbidden blanket form (R-13, R-14); it is needed because a lock file full of conflict markers is unparseable and a from-scratch resolve could upgrade unrelated dependencies. Then run the rule's `regenerate` (`uv lock`; network may be needed; failure is a halt, not a retry loop) and its `check` (`uv lock --check`). See OQ-6 for the "ours" seed versus the base-side seed.
3. `git add -- uv.lock`.
4. Report in the commit body: "uv.lock regenerated from the merged pyproject.toml; dependency versions that changed: <diff of the lock summary>".

### 6.6 Resolution record and commit message (inline in the ref, no template file)

<!-- Source: Base (original, modified): host ref named as refs/conflict-intent.md per Change #2 -->

Tier 2 only; the format lives in `refs/conflict-intent.md`. `<output-dir>/sync/<cycle_id>/resolution.md`, one section per `text:*` file, fields in this order:

```text
## <path>
kind: trivial | additive | competing | structural | modify-delete | add-add | semantic   (R-149; semantic => Tier 3)
root_cause: <one phrase: what made git unable to merge>                                (R-146)
ours_intent: <one sentence, what this PR's side does>                                   (R-18)
theirs_intent: <one sentence, what the base side does>                                  (R-18)
resolution: keep_both(<order>) | take_ours | take_theirs | synthesized
behavior_after: <one sentence describing behaviour after the merge>                     (R-156)
dropped: none | <behaviour dropped and why>                                             (S-29)
evidence: <stage files / commits consulted>                                             (R-112, S-12..14)
```

The merge commit message is generated from this file: subject `Merge origin/<base> into <HEAD_BRANCH> (sc:pr-submit sync, tier <t>)`, a body with one line per resolved file (`kind`, `resolution`, `dropped`), and the repository's required attribution lines appended at commit time. It contains intents, never file content, so no secret can enter it (the run-log redaction patterns still apply to the run-log).

`resolution_record_ok(record)` is pure and returns a list of problems: every `text:*` path has an entry; no field empty; `ours_intent` and `theirs_intent` each one sentence (no newline, one terminal stop); `kind != "semantic"`; `dropped` present; `resolution` in the enum; `behavior_after` present. Any problem means no commit.

### 6.7 Validation (VAL reuse, no new gates)

<!-- Source: Base (original, modified): Tier 1 VAL and the no-tests cap per Change #11 (R2-C R-C7, A-003); VG-2 at Tier 2 kept from base and marked OPEN (C-028/X-019); baseline recorded as an open question (INV-014) -->

The VAL gate list is unchanged (`SKILL.md:279-291`). Inputs for a conflict cycle: `changed-area` = the resolved paths.

- **Tier 1 VAL** = `uv lock --check` + VG-3 (`make lint`) + VG-4 (`ruff format --check`).
- If the VG-2 target is absent or runs no tests, cap the run at Tier 1 and add the report line "no tests found for changed area".
- **VG-2 at Tier 2: OPEN** (C-028 / X-019). Base text kept as the default: `is_cross_cutting(resolved_paths)` decides VG-2 as today, and **any resolved path under `src/superclaude/pr_submit/` or any `pyproject.toml` conflict forces VG-2**. Competing positions are listed in section 12.
- VG-5 (`make verify-sync`) runs when a resolved path is under a synced component.
- A failing gate triggers the existing single retry; a retry must not introduce changes unrelated to the failure (R-169).
- Whether VAL needs a baseline run on the base to separate base-caused from resolution-caused failures is an open question (section 12, INV-014).

### 6.8 Where an unfinished merge is left

<!-- Source: Base (original, modified): OPEN marker added per the Changes NOT Being Made entry C-027/X-021 (base abort kept) -->

**OPEN (C-027 / X-021):** an inferred majority (60%) would leave a mid-resolution merge in progress instead of aborting; the choice interacts with the Wave 0 operation-check halt (INV-004) and with INV-010. The base rule below is kept until it is decided (section 12).

- Halt before the resolution is complete (Tier 3 discovered mid-way, validator disagreement, VAL red after retry): **`git merge --abort`** (ours verified), worktree and index restored, `sync_concluded{aborted}`. An abandoned half-resolution is worse for the operator than a clean tree plus the preserved `resolution.md` and evidence files.
- Resolution complete and validated but the run must stop (L2, or a commit hook rejecting): **leave the merge in progress** (J-53) so nothing the model produced is lost.

### 6.9 Staging, stash, hook and wait-only rules (summary of what the static tests pin)

<!-- Source: Base (original, modified): wait-only carve-out inserted per Change #17 (inv-A, inv-B, inv-C INV-009) -->

Exact-path staging only; the merge's own auto-merged paths are already staged by git, and `finish-merge.sh` proves the staged set is within the expected set. Never stash (J-20, shared stash stack). Never `reset --hard`. Never check out the base branch (J-06) or touch another worktree or branch (J-05, J-91). Never `--no-verify`, never amend. No `.claude/` staging except `.claude/settings.json`, and that file is itself `halt:protected` if it conflicts.

**Wait-only sentences (INV-009).** Three normative sentences say a spent round budget or a silence terminal permits waiting only: `refs/state-machine.md:144-146`, `refs/ci-poll.md:28-29` and `SKILL.md:277`. Rewrite them so that "never an additional push" covers model-authored fixes, with the single Tier 1 sync push (`SYNC_CAP = 1`) named as the only exception. Add a `test_static_grep.py` pin; none exists today. The exact wording is OPEN between the three proposals (section 12); the meaning is agreed.

### 6.10 Post-push CI wait: `expect_checks` (INV-034)

<!-- Source: INV-034 focused round (round-inv034-advocate-A/B/C.md): merged per Change #25; rule R-034' from Variant A's advocate, the timeout correction from Variant B's advocate, the tests from Variant C's advocate -->

Right after a merge push the new head has no check runs yet, and on a previously conflicting PR `pull_request` workflows wait for GitHub to rebuild the merge ref, so the first poll could read two empty check lists as `clean` (INV-034). CI is Tier 1's only test signal, so the wait must expect checks when the repository has them.

- **Core keyword.** `superclaude.pr_submit.ci.classify_checks(payload, *, wait_sha=None, expect_checks=False)`: when `expect_checks` is true and the chosen check list is empty at `head_sha == wait_sha`, return `polling`. The default (off) keeps every existing pin green (`test_ci_classify.py:36-38`).
- **Setting it.** The skill sets `expect_checks` once per push and records it in the run-log, so `--resume` reuses it. It is true if any holds: (a) checks were seen earlier in this run on any head; (b) `pre_push_sha` has at least one check run or status context; (c) `base_sha` has at least one.
- **Evidence for (b) and (c).** `poll-ci-checks.sh --evidence-sha <sha>` reads `gh api repos/$REPO/commits/<sha>/check-runs` and `/status` (commit-scoped, so it survives a PR turning conflicting) and emits `evidence_checks:<n>`, or `-1` on a failed or unparsable read; `-1` counts as "had checks" (fail closed). `gh` stays out of the core.
- **No Actions.** Only when (a), (b) and (c) all read zero is an empty list `clean`, as today.
- **Expiry.** Expiry with no registered check is the existing Wave 8 CI `timed_out` result with reason `ci_not_started` (not the review-phase `TERMINAL_TIMEOUT`); never `clean`, and the report never says "tests passed".
- **Protocol text.** Amend `refs/ci-poll.md:21` and `SKILL.md:277` ("only parsed empty ... prove there are no Actions") to add "and `expect_checks` is false".
- **Tests** (`tests/pr_submit/test_ci_classify.py` plus an evidence-setter test): empty + expect + matching head = `polling`; nonempty all-pass + expect = `clean`; empty + no expect = `clean`; existing tests unmodified; head mismatch = `polling`. Setter: `pre_push_sha` nonempty = true; all empty = false; read fails = true; `pre_push_sha` empty but `base_sha` nonempty = true.

## 7. Requirements

<!-- Source: Base (original) -->

Priority key: **M** must, **S** should. Every FR lists a verifiable acceptance criterion (AC). Research ids in brackets show where an adopted item lands.

### 7.1 Functional requirements

<!-- Source: Base (original, modified): FR-1, FR-2, FR-5 to FR-7, FR-9 to FR-11, FR-13 to FR-20, FR-22 to FR-24 aligned with Changes #2, #3, #4, #6, #7, #9, #10, #12, #15, #16, #21, #25; FR-26 to FR-33 restate Changes #5, #6, #8, #13, #14, #17, #18, #25 as requirements -->

| ID | P | Requirement | Acceptance criteria |
|---|---|---|---|
| **FR-1** | M | **Probe.** `scripts/probe-merge.sh` emits the single-line JSON of section 5.3 and performs no worktree or index mutation. It fetches only `origin <base>`, uses the PR's `baseRefName`, detects `foreign_op` and `tree_clean`, sets `merge_tree_supported` by capability probe, and emits the raw `-z` stage listing unparsed. It runs only when GitHub reads `CONFLICTING` or a persistent `UNKNOWN`. [R-26, R-43, J-16, J-17, S-05, S-38] | (a) On a repo with a clean base, output has `clean: true` and an empty listing; (b) with a content conflict, the parsed stages are `"123"`; (c) with a base-side delete, `"13"`; (d) a binary conflict appears in `binary_paths`; (e) a staged or unstaged tracked change gives `tree_clean: false`, an untracked file does not; (f) a half-finished rebase gives a non-null `foreign_op`; (g) before and after `git status --porcelain=v1 -z` are identical; (h) non-zero exit on missing `--repo`. |
| **FR-2** | M | **Pure classification.** `conflicts.parse_stage_records` parses the raw listing; `conflicts.classify_conflicts(entries, *, conflict_max_tier, rules=MECHANICAL_RULES, tier2_max_files=8)` implements the 13-rule table and the tier table of 4.2 (including the GitHub `MERGEABLE` and `BLOCKED` rows), and returns a plan: `tier`, `action` in `{none, report, resolve, halt}`, per-path `class` and `reason`, `reasons` list. Core-pure (no `git`/`gh` tokens, no network). | `parse_stage_records` accepts the captured fixture `fixtures/merge_tree_conflict.z` and rejects each malformed shape. Parametrized tests cover every rule and every boundary: submodule beats binary; protected beats text; `uv.lock` with stages `"13"` is `halt:lockfile_no_recipe`; a nested `pkg/uv.lock` does not match the root-anchored rule; the rule does not match when the path is untracked or `uv` is absent; 8 text files is Tier 2, 9 is Tier 3 `too_many_files`; `BLOCKED` with `MERGEABLE` is Tier 0 (own row); unknown stage string is `halt:unknown_shape`; `tier > cap` gives `report`/`tier_above_cap`; empty input gives Tier 0; malformed entries (missing key, non-str path) fail closed to Tier 3. |
| **FR-3** | M | **Flag.** `--conflict-max-tier {0,1,2}` (default 1 in the first release) in `SkillArgs`, `parse_args`, `build_arg_parser` and the command Options table. 0 means detect and report only. | `parse_args([])` yields 1; `--conflict-max-tier 3` is rejected by argparse; the command table row exists; `fsm.py` still has no `git`/`gh` token. |
| **FR-4** | M | **Report before acting.** At the end of Wave 0 (L1+) and at each acting hook (`C-initial`, Wave 8a), print the plan before any edit: tier, each path with class and reason, and the action the current ordinal would take. [R-51] | Static test: the refs contain the report step ahead of the merge step; L0 emits nothing. |
| **FR-5** | M | **Placement.** `SKILL.md` gets the Wave 0 detection and operation-check sentences, one Wave 8a bullet, the `C-initial` sentence (P2) and the wave-table rows of section 5.2. `refs/conflict-mechanical.md` loads lazily and only when the probe reports conflicts; `refs/conflict-intent.md` loads only for Tier 2. Wave 8a entry only after the review phase settles with an outcome allowed by section 5.5. | Static test: wave table rows present; `SKILL.md` has exactly one python block; `refs/conflict-intent.md` is named only in the Tier 2 sentence; Tier 0 path loads no ref. |
| **FR-6** | M | **Behaviour by tier and ordinal** exactly as the tables in 5.4 and 5.5 (L0 nothing; L1 report and propose; L2 local resolution at Wave 8a and stop with the merge in progress; L3 Tier 1 at Wave 8a, Tier 2 at `C-initial`, Tier 3 Wave 0 halt). | Scripted tests per ordinal assert the commands issued (via the refs' static text) and the run-log events; L2 appends no `push_*` event and no commit; L2 entered from a preserved terminal keeps that status; L0 byte-identity sentence still present. |
| **FR-7** | M | **Start preconditions.** Before `sync_started`: pr_head check (6.4 step 1), `foreign_op == null`, `merge_preflight_ok` on the tracked tree (untracked files tolerated), `HEAD_BRANCH != base`, current worktree only. A dirty tracked tree halts `merge_preflight_dirty` naming the files. `sync_started` is appended before the merge command (write-ahead). [J-05, J-16, J-17, J-18, J-26, J-91] | Static test pins the order: precondition text, then `sync_started`, then the merge command in the ref. Real-git test: a dirty `pyproject.toml` halts with nothing merged. |
| **FR-8** | M | **Merge command.** `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>`; no `--no-verify`, no global config write, no stash. [J-60, J-20, R-128, S-17] | Static test: exact command string present; absent: `git config`, `git stash`, `--no-verify`, `rerere.enabled=true`. |
| **FR-9** | M | **Tier 1 rule.** The one `MechanicalRule` (root `uv.lock`, stage set `123`, tracked, `uv` on PATH): seed the one named lock file with `git checkout --ours -- uv.lock`, then `uv lock`, `uv lock --check`, `git add -- uv.lock`. A failure of either `uv` command is a halt with `sync_merge_failed` and an abort. [R-58, R-189, S-46, J-48] | Static test: recipe order; `MECHANICAL_RULES` has exactly one row, for `uv.lock`; no other lockfile has a rule; every rule program is in the `allowed-tools` front matter. |
| **FR-10** | M | **Tier 3 halt message and abort.** At L3 a Tier 3 conflict found at Wave 0 halts there with reason `conflict_tier3` in the `SKILL.md:268` shape; nothing is started. The message names the file, the operation (merge of `origin/<base>`@sha into `<HEAD_BRANCH>`), the step `k/n`, the branch, and one sentence per side describing what it appears to do (both skipped when classification stopped before reading). It ends with explicit recovery steps and the statement that nothing was pushed. A mid-way halt runs `git merge --abort` only after verifying `MERGE_HEAD == base_sha`. [R-210, R-212, R-54, R-56, R-57, J-13] | Static test pins the message fragments; script test: abort restores a clean worktree and the original `HEAD`. |
| **FR-11** | M | **Finish guard script.** `finish-merge.sh` performs the checks of 6.4 step 9 (including the clean-tree re-check before the regenerate and the two post-commit assertions) and commits with `git commit -F <msg>` with hooks on. It prints `{merge_sha, parents}` JSON on success and a precise failure token otherwise. [R-11, J-56, J-61, J-63] | Real-repo tests: unmerged path refused; introduced marker refused; marker line already present in the stage-1 blob accepted; unexpected staged path refused; `MERGE_HEAD` mismatch refused; a dirty tracked tree refused; failing pre-commit hook refused with the hook output verbatim and no commit created; success yields exactly two parents `[HEAD, base_sha]`. |
| **FR-12** | M | **Merge parent rule.** `conflicts.merge_parent_ok` exactly as 6.2. | Matrix per 6.2 including case-insensitivity, trailing newline, swapped order, equal shas, 1 and 3 parents, bad ids; disjointness property against `push_parent_ok`. |
| **FR-13** | M | **Sync decision.** `evaluate_sync_decision` and `sync_fail_state` as 6.3, for both conflict tiers. `fsm.evaluate_push_decision` is not modified. | Full truth table (16 rows) for the four predicates, per tier; `sync_fail_state` mapping; cross-gate property test on the shared predicates; byte-for-byte unchanged `evaluate_push_decision` (existing tests pass untouched). |
| **FR-14** | M | **Push path.** Guard order head -> parent -> base-ancestor -> decision -> triad -> push, as 6.4 steps 10 to 12 (order OPEN, X-009); push command `git push origin <target_sha>:<HEAD_BRANCH>`; `pre_push_sha := target_sha` after. `build_push_triad(..., push_kind, base_sha)` emits the three records in order with `kind` and `base_sha`, and the unchanged idempotency key format. There is no separate sync triad builder. | Static test pins the order in the ref and the push command; `build_push_triad` default call output equals a recorded pre-change fixture; a conflict call adds `kind` and `base_sha` to all three records; the force-push scan passes over the new refs and scripts. |
| **FR-15** | M | **One commit per cycle.** A sync or merge cycle commits exactly the merge commit and never a fix commit; a fix cycle never merges. The cycle id prefixes `sync-` and `conflict-` are reserved and never used for a fix push; `is_conflict_cycle` recognises them. | Ref states the rule; unit test: `merge_parent_ok` rejects a one-parent fix commit and `push_parent_ok` rejects `M`; one test proves the fix-cycle id rule can produce neither prefix. |
| **FR-16** | M | **Run-log.** Add `sync_started` and `sync_concluded` to `EventType` (Tier 2 events OPEN, section 5.7); `rebuild_state` gains `sync_cycles` (list of cycle ids from `sync_started`) and `sync_push_count`; the fold at `run_log.py:238-239` is kind-aware: a `push_completed` with `kind: "sync"` does not increment `push_count`, kinds `fix` and `merge` do; `pushed_commit_shas` still records `target_sha`. | `len(EventType) == 43` (both pins and the `models.py:23` docstring updated); a behavioural `rebuild_state` test with a conflict push in the fixture (QA-1); fold tests including old logs without `kind`; `append` rejects unknown events as today. |
| **FR-17** | M | **Resume.** Recovery rules of 5.8; `resolve_crash_window` copies `kind` and `base_sha`; `crash_resume_plan` returns the Wave 8 CI-wait directive for kinds `sync` and `ci` and never `S4_PUSHING`, S5a or S5; kinds `fix`, `merge` and absent behave exactly as before; a record marked `rejected` is never re-driven. | Parametrized kind {fix, merge, sync, ci, absent} x branch {A, B, C} -> exact resume directive; `sync`/A yields the Wave 8 directive with `wait_sha == target_sha`; `fix` and absent keep today's outputs byte-equal; recovered `push_completed` carries `kind`; a missing terminal gives `resume_unrepresentable`; a foreign `MERGE_HEAD` is documented as `sync_foreign_operation`. |
| **FR-18** | M | **Post-sync CI.** After a pushed Tier 1 sync, Wave 8 polls CI with `wait_sha = target_sha` and `expect_checks` per section 6.10; no `retrigger-review.sh`, no reply, no resolve; `round_counter` and `rereview_request_count` unchanged. | Static test on the ref text; run-log fold test shows no `round_incremented` from a sync cycle; the section 6.10 tests. |
| **FR-19** | M | **Output contract and status.** Add `sync_tier` (int, 0 to 3), `sync_outcome` (enum `none`, `report_only`, `left_in_progress`, `pushed`, `aborted`, `halted`), `sync_push_count` (int, at most `SYNC_CAP`). `push_count` excludes kind `sync` only, and `push_kind` is on the records. Reconcile `SKILL.md:239` with `:275`. The `status` enum is unchanged; Tier 3 halts use `terminal_halted`, L2 uses `halt_before_push`. | Static test: three new rows in the Output Contract table; enum line unchanged; a report-contract test shows pushes-by-kind can be reconstructed from the report (QA-2). |
| **FR-20** | M | **Docs.** Update `SKILL.md` (wave table rows, Wave 8a bullet, Wave 0 sentences, `C-initial` sentence, contract rows, Will Do and Will Not bullets, Error Handling rows, the wait-only and `expect_checks` sentences at `:277`), `commands/pr-submit.md` (flag row, Will Not clause), `refs/state-machine.md` (new section 5.2d: the Tier 1 sync phase is SKILL-owned with no FSM edges, and the P2 merge cycle uses the one `(S2_CLASSIFY, "conflicting")` edge; the wait-only sentence at `:144-146`; no `git`/`gh` tokens), `refs/ci-poll.md` (`:21`, `:28-29`). The pinned fragments listed in section 8.4 are left byte-identical. | Pins in 8.4 pass; `make verify-sync` clean. |
| **FR-21** | M | **Prohibited operations** (static-greppable in the refs and scripts): blanket side-taking (`--ours`/`--theirs` with `.` or no path), `-X ours`, `-X theirs`, `-s ours`, hard reset during a conflict, stash in any form, `--no-verify`, `--amend`, `add -A`, `add .`, `commit --only` during a merge, force or `+` refspec pushes, checkout of the base branch, writes to global git config, edits to any path outside the current worktree. Prohibitions in prose use words, not the literal command (G16). [R-13, R-14, R-15, J-20, J-60, J-63, J-05, J-06, J-91] | A single static test with one regex per prohibition; the refs' prohibition paragraphs pass their own scan. |
| **FR-22** | S | **Tier 2 evidence step (P2).** `collect-conflict-evidence.sh --path <p> --out <dir>`, or the same reads written as inline calls in `refs/conflict-intent.md`, writes stage 1/2/3 blobs, the left-right log and both merge-base diffs under the output dir, bounded to 200 KiB per file and 60 seconds, and writes nowhere else. [S-12 to S-14, R-112, R-181] | Real-repo test lists exactly the expected files; truncation marker present when the cap is hit. |
| **FR-23** | S | **Tier 2 resolution record and validator.** `resolution_record_ok` as 6.6; one `evidence-validator` spawn per Tier 2 cycle for the grounding check; one revision pass; failures escalate to Tier 3. [R-18, R-156, S-26, S-29, R-146, R-149] | Core tests for each problem class; ref static test for the spawn instruction and the single-revision rule. |
| **FR-24** | S | **Mergeability hint.** `conflicts.mergeability_hint(mergeable, merge_state)` normalises the GitHub fields to `conflicting`, `behind`, `clean`, `unknown`. Used for reporting, for the GitHub-first decision whether to probe (section 5.3) and for the P3 late trigger; never to override a local probe that has run. | Table-driven tests incl. `UNKNOWN`, `None`, lowercase, junk strings. |
| **FR-25** | S | **P3 late re-sync.** `poll-ci-checks.sh` adds a `merge_state` field to its JSON line (appended after the existing keys); Wave 8 triggers Wave 8a once more under `SYNC_CAP`, Tier 0 and 1 only. | Existing `classify_checks` tests pass untouched; new payload-shape test; script test with a stubbed `gh`. |
| **FR-26** | M | **Single router.** `conflicts.conflict_action` is the only routing decision for conflicts, over tier x ordinal x hook x entering outcome x budget x cap (section 3.4), with a fail-closed default row. | Exhaustive reachable-row table test (QA-4), including the entering-outcome axis and the default row. |
| **FR-27** | M | **Wave 0 operation check.** At every L1+ run, before the GitHub read, a local check for `MERGE_HEAD`, a rebase or a cherry-pick in progress halts the run (section 5.1; reason code OPEN, default `foreign_op_in_progress`). | Static test pins the sentence in the Wave 0 text; a test with a merge left in progress and GitHub reading `MERGEABLE` halts before any fix cycle. |
| **FR-28** | M | **Tier 2 early path (P2).** The `(S2_CLASSIFY, "conflicting")` edge with the `findings` round gate; the widened S5a clause `applied_edits > 0 or kind == "merge"`; the configured-reviewer substitution at `C-initial` (section 5.6). | Edge row assertions in the `test_auggie_fallback.py:353-379` pattern; new static pin of the widened sentence; zero-edit-pair behavioural test (QA-3); `test_static_grep.py:689` and `:750` substrings unchanged; a pin for the configured-reviewer substitution. |
| **FR-29** | M | **`pr_conflicting` CI-wait skip.** Section 5.5. | Static test pins the skip wording in the Wave 8 text. |
| **FR-30** | M | **Rejected push and merge-method advisory.** Section 6.4 steps 10 and 12: advisory read of the merge-method fields, never a halt; a rejected live push appends `push_aborted_or_not_landed{rejected: true, stderr_tail}` and halts `push_rejected`; recovery never re-drives it; a post-push `BLOCKED` is reported with a reason line. | Unit test on the recovery rule; static test pins `push_rejected` and the advisory wording. |
| **FR-31** | M | **Create path at L1+** (precursor change, AD-7). At L1+ the create path neither rebases nor halts when behind base; behind is a Tier 0 report. L0 keeps today's rebase byte for byte. | `test_static_grep.py:649-657` unchanged; only the L1+ HALT pins at `:658` and `:660` are rewritten. |
| **FR-32** | M | **Expected checks after a conflict push.** Section 6.10. | The section 6.10 tests. |
| **FR-33** | M | **Wait-only carve-out.** Section 6.9: the three wait-only sentences name the single Tier 1 sync push as the only exception. | New `test_static_grep.py` pin over the three sites. |

### 7.2 Non-functional requirements

<!-- Source: Base (original, modified): NFR-4 per Changes #2 and #6; NFR-9 line-count assertion removed per Change #22 (R1-B concession 6); NFR-14 per Change #22 (R2-C QA-9) -->

| ID | Requirement | Acceptance criteria |
|---|---|---|
| **NFR-1** | **No force-push, ever.** | The pinned scan (`test_static_grep.py:758-776`) passes over the new files; push command text is exactly `git push origin <sha>:<branch>`. |
| **NFR-2** | **Core purity.** `conflicts.py` has no `git`/`gh` token (docstrings included), imports no `anthropic`, performs no I/O. It joins `CORE_PURE_FILES`. | T-N50 and T-N41 pass with the file added. |
| **NFR-3** | **L0 byte-identical.** No new output, no new call at `--monitor 0`. | The AC-1 sentence assertion is unchanged and passes. |
| **NFR-4** | **Cost layering.** Tier 0 adds the local operation check and one `gh pr view` read (up to 3 re-reads on `UNKNOWN`): no fetch, no probe, no ref load, no model reasoning, no agent. Tier 1 adds the probe and loads only `refs/conflict-mechanical.md`; no model reasoning, no agent. Only Tier 2 loads `refs/conflict-intent.md` and spawns an agent. | Static test: only the Tier 2 sections mention the evidence step and `evidence-validator`; `refs/conflict-intent.md` is named only in the Tier 2 sentence. |
| **NFR-5** | **Fail closed.** Any unparsable probe output, unknown stage shape, missing field, bad sha or unrecognised mode yields Tier 3 (or `unknown` for GitHub hints) and never an action. | Parametrized fail-closed tests for every core function. |
| **NFR-6** | **Repo pin and origin-only.** Every `gh` line in the new refs and scripts carries `--repo`; fetch and push target `origin` only; nothing contacts the upstream. | The existing fork-pin tests (T-1101 family) pass with the new files included. |
| **NFR-7** | **Secrets.** Run-log redaction applies to the new events; the commit message and `resolution.md` contain intents, never file content. | Redaction test on a `sync_concluded` payload containing a token-shaped string. |
| **NFR-8** | **Installed-path hygiene.** No `src/superclaude/` path in the new refs, scripts, command text or SKILL text. | `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit (CLAUDE.md check). |
| **NFR-9** | **Bounded growth of `SKILL.md`.** Net growth is at most 15 lines and no new python block; all procedure lives in the refs; no duplicated guard text (the refs refer to "the Wave 6 pre-push head guard" by name and state only the delta). | The byte-identical fragment test of section 8.4 passes; there is no line-count assertion. |
| **NFR-10** | **Bounded scripts.** Each new script has a per-call timeout (60 s) and truncates output at 100 KiB with a visible marker; none reads stdin or prompts. | Script tests with an oversized fixture. |
| **NFR-11** | **Capability gate, not version parse.** Missing `git merge-tree --write-tree` degrades to report-only. | Script test with a stubbed `git` that fails the capability probe. |
| **NFR-12** | **Backward compatibility of artifacts.** Old run-logs (no `kind`, no sync events) rebuild identically; the fix-push record shape is unchanged. | Fold test on a recorded fixture; `build_push_triad` default-call fixture test. |
| **NFR-13** | **Post-change gates.** `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, and the full `make test` are green. | CI. |
| **NFR-14** | **Per-tier call ceilings (counts, not time).** A mechanical conflict at L3 completes with at most 1 probe, N `git add`, 1 commit, 1 push and the tier's event count; a normal PR costs one `gh pr view`. | Ceiling constants asserted in the routing and flow tests (QA-9). |

## 8. Test plan

<!-- Source: Base (original, modified): hermetic real-git note per Changes #22 and #23 -->

Conventions kept: pure helpers by direct calls with parametrized fail-closed shapes (as `test_pre_pr_checks.py:201-230`); run-log tests with a real `RunLog` under `tmp_path`; skill text pinned by literal-substring static tests; scripts by their own test file. Real git runs only in hermetic repositories inside a pytest temporary directory, with `gh` mocked; no test touches the network or a live remote.

### 8.1 New test files

<!-- Source: Base (original, modified): additions per Change #22 (Variant A, A:557 fixture; R2-C QA-1 to QA-10), Change #12 (dirty-tree test), Change #23 (hermetic Tier 1 test), Change #25 (CI classify tests); build_sync_triad removed per Change #10 -->

| File | Covers | Notes |
|---|---|---|
| `tests/pr_submit/test_conflicts_core.py` | FR-2, FR-12, FR-13, FR-15, FR-17, FR-23, FR-24, FR-26, NFR-5, NFR-14 | Table-driven. Includes the `parse_stage_records` test against the captured fixture; the `conflict_action` exhaustive reachable-row table test (QA-4); the disjointness property between `push_parent_ok` and `merge_parent_ok`; the 16-row `SyncDecision` truth table per tier and the cross-gate property test; `merge_preflight_ok` porcelain rows (staged-dirty, unstaged-dirty, untracked-only, clean); every classification rule and boundary (8 vs 9 files, root-anchored rule, `BLOCKED` row); `crash_resume_plan` kind x branch rows; `is_conflict_cycle` and the prefix-disjointness test (QA-8); unknown shapes, malformed entries, `resolution_record_ok` problem classes; per-tier call ceilings (QA-9). |
| `tests/pr_submit/fixtures/merge_tree_conflict.z` (new fixture) | FR-2 | NUL-separated probe output captured once from a scratch repo; the capture recipe is a comment in the test. |
| `tests/pr_submit/test_conflict_sync_protocol.py` | FR-4 to FR-10, FR-14, FR-18 to FR-21, FR-27 to FR-31, FR-33, NFR-4, NFR-6, NFR-8, NFR-9 | Static-grep over `SKILL.md`, both refs, the scripts and the command. Includes the prohibited-operations scan (FR-21), ordering pins (preconditions < `sync_started` < merge command; head check < `merge_parent_ok` < base-ancestor < DECIDES < push), tier headings, `--repo` on every `gh` line, Tier-2-only mentions of the evidence step and `evidence-validator`, absence of `src/superclaude`, the widened S5a sentence (QA-3a), the wait-only sentences, the `pr_conflicting` skip and the configured-reviewer substitution. |
| `tests/pr_submit/test_conflict_scripts.py` | FR-1, FR-7, FR-11, FR-22, NFR-10, NFR-11 | Builds throwaway repos with `git init` plus a local bare repo as `origin` under `tmp_path` (no network, no gh: `gh` is a PATH stub). Skipped when `git merge-tree --write-tree` is unsupported (capability probe, not a version parse). Cases listed in FR-1 and FR-11, plus the dirty `pyproject.toml` case (halts, nothing merged) and the P1 gate (a) hermetic Tier 1 test of section 8.5. |
| `tests/pr_submit/test_ci_classify.py` (additions) and an evidence-setter test | FR-32 | The section 6.10 rows; the existing rows (`:36-38`) unmodified. |

### 8.2 Changed existing tests (exact edits)

<!-- Source: Base (original, modified): rows per Changes #8, #10, #13, #15, #16, #17, #22 (QA-1, QA-3, QA-6), #25 -->

| File | Edit | Why |
|---|---|---|
| `tests/pr_submit/test_run_log.py:168` | `len(EventType) == 41` becomes `43`; add fold tests for `sync_started`, `sync_push_count`, no `push_count` increment for `kind: "sync"`, increments for `fix` and `merge`, old-log compatibility, and one behavioural `rebuild_state` test with a conflict push in the fixture (QA-1) | FR-16, NFR-12 |
| `tests/pr_submit/test_codex_reviews.py:441` | same pinned count `41` to `43` | pinned count |
| `src/superclaude/pr_submit/models.py:23` docstring | "EXACTLY 41 members" updated to 43 (docstring, not a test, but it states the count); `grep` of `tests/` for `== 41` as a PR checklist step (QA-6) | accuracy |
| `tests/pr_submit/test_crash_recovery.py` | kind {fix, merge, sync, ci, absent} x Branch {A, B, C} rows with the exact resume directive; recovered record carries `kind` and `base_sha`; kind-less regression; a `rejected` record is never re-driven | FR-17, FR-30 |
| `tests/pr_submit/test_skill_parse.py` | `--conflict-max-tier` default 1, bounds, argparse rejection of 3 | FR-3 |
| `tests/pr_submit/test_static_grep.py:37-51` | add `PR_SUBMIT_PKG / "conflicts.py"` to `CORE_PURE_FILES`; the new refs are NOT added (they necessarily contain git commands, like `thread-reply.md`, which is also outside the set) | NFR-2 |
| `tests/pr_submit/test_static_grep.py:658`, `:660` | rewritten for the create path at L1+ (precursor change); `:649-657` unchanged | FR-31 |
| `tests/pr_submit/test_static_grep.py` (new pins) | the widened S5a sentence (P2); the three wait-only sentences; the `:689` and `:750` substrings asserted unchanged | FR-28, FR-33 |
| `tests/pr_submit/test_autonomy_gates.py` (P2) | `(S2_CLASSIFY, "conflicting")` edge rows in the `test_auggie_fallback.py:353-379` pattern | FR-28 |
| `tests/pr_submit/test_loop_guard.py`, `test_validation_gate.py` | existing zero-edit rows stay green; add the zero-edit merge row (re-triggers) beside them (QA-3b) | FR-28 |
| `tests/unit/test_cli_install.py:248-262` | add the two refs and the two P1 scripts to the expected installed list (presence check only, `:496-500`); the evidence script in P2 if it ships | install surface |
| `tests/pr_submit/test_pre_pr_checks.py` | no change to `merge` parametrize id (`:216-222`); add one assertion that `push_parent_ok` still rejects a perfectly valid `merge_parent_ok` input | pins the refusal to loosen |
| `tests/pr_submit/test_idempotency.py:89` | `len(IDEMPOTENCY_SETS) == 7` unchanged (asserts the design did not add a set) | QA-6 |
| `tests/pr_submit/test_ci_classify.py` | the section 6.10 rows; existing rows untouched; for FR-25 (P3): payload shape with `merge_state` | FR-25, FR-32 |
| `SKILL.md <= 346` line-count assertion | removed (not added); the byte-identical fragment test of section 8.4 stays | NFR-9 |

### 8.3 Pinned counts and static greps this design must not break

<!-- Source: Base (original, modified): head-binding row restated for the create-path precursor (Change #13) and the operation-check sentence (Change #6); S5a, classify_checks and idempotency rows added per Changes #8, #25, #22 -->

| Pin | Where | How the design stays safe |
|---|---|---|
| Exactly one python block in `SKILL.md` | `test_cosmos_protocol.py:36`, `test_codex_reviews.py:688` | New procedure is in the refs; code shown in the refs uses `text`/`bash` fences only, and `SKILL.md` gets prose only. |
| `len(EventType) == 41` | `test_run_log.py:168`, `test_codex_reviews.py:441` | Deliberately updated once to 43 (FR-16); no other event is added in P1. |
| T-N50 (no `git`/`gh` token in the eight core-pure files) | `test_static_grep.py:37-51`, `:132-143` | `conflicts.py` is written clean and added to the set; the `state-machine.md` section 5.2d is written clean; the `ci.py` keyword adds no token. The new refs are NOT in the set. |
| T-N41 (no `anthropic` import) | `test_static_grep.py:146-155` | `conflicts.py` imports only `re`, `dataclasses`, `typing` and `fsm.push_idempotency_key`. |
| Head-binding and push pins | `test_static_grep.py:627-755` | The Wave 6 bullet's pinned sentences and the Wave 0 head-binding bullet are not edited. The Wave 0 edits are the operation-check and detection sentences (additive) and the create-path precursor, which rewrites only the L1+ HALT pins at `:658` and `:660` (section 8.2). |
| S5a-adjacent pins | `test_static_grep.py:689`, `:750` | The widened S5a clause (P2) sits between them; both substrings stay unchanged and are asserted so. |
| Force-push scan over every `.md` and `.sh` | `test_static_grep.py:758-776` | No force form, and no prose of the form "git push" followed by a force flag, in the two refs and the scripts. |
| Command Will Not sentence | `test_static_grep.py:754-755` | The pinned clause stays; a new clause is appended after it. |
| AC-1 L0 sentence | `test_static_grep.py:650-653` | Untouched. |
| `--json headRefName,headRefOid,isCrossRepository` substring | `test_static_grep.py:636` | The head-binding read is not changed; the GitHub detection read is a separate `gh pr view ... --json baseRefName,mergeable,mergeStateStatus` call. |
| `classify_checks` rows | `test_ci_classify.py:36-38` | The `expect_checks` keyword defaults off. |
| `IDEMPOTENCY_SETS == 7` | `test_idempotency.py:89` | No set is added. |
| `test_edge_cases.py:263-267` (matches "Wrong origin" / "behind" / "wrong-owner") | edge cases | The Error Handling row keeps its first cell ("Wrong origin"). New rows are added below it. |
| `tests/commands/test_impact_command.py:327-345` | impact caller strings | Untouched. |

### 8.4 Fragments that must stay byte-identical (copy into a regression test)

<!-- Source: Base (original, modified): fragments 3 and 4 moved out of the byte-identical list because the create-path precursor rewrites the pins at test_static_grep.py:658 and :660 (Change #13) -->

1. `with \`--pr <N>\`, at any level, do not rebase`
2. `rebase if behind \`origin/<base>\`` (L0 keeps the rebase, so this stays)
3. The whole Wave 6 push-guard wording (`pr_head_ok(<local branch>, pre_push_sha,`, `push_parent_ok(<parents>, pre_push_sha)`, `The deterministic core DECIDES`, `then set \`pre_push_sha := target_sha\``)
4. `push any commit besides the cycle's one fix commit`
5. `the commit to push must have exactly one parent, that same SHA` and `The parent check applies only when the cycle applied edits` in `state-machine.md`

Not in this list any more: `branch (\`origin/<default-branch>\`) on the create path` and `| Wrong origin / behind base branch (create path) / wrong-owner URL |` (pins at `test_static_grep.py:658`, `:660`), which the create-path precursor rewrites for L1+ (FR-31).

### 8.5 P1 gate and manual verification

<!-- Source: Base (original, modified): P1 gate text replaced per Change #23 (inv-A, inv-B, inv-C INV-033); remaining manual items kept -->

**P1 gate.**

- **(a) Mandatory hermetic real-git test.** In a pytest temporary directory: a tracked `uv.lock` and a zero-dependency `pyproject.toml` on two diverging branches. It runs probe -> classify -> `uv lock` (offline, real `uv`, with a `skipif(no uv)` case) -> `finish-merge.sh` -> `merge_parent_ok`, with `gh` mocked. This is an allowed internal temporary checkout under CLAUDE.md.
- **(b) One manual live L3 run** on a separate repository that tracks `uv.lock`. Creating that repository is the user's decision; it must be under `IronbellyOrg`, never upstream. The run also exercises INV-034 (section 6.10). Manual verification is reported as manual, never as a test pass.
- Do not un-ignore `uv.lock` in this repository.

**Other manual verification** (not automated; goes into the P1 and P2 hand-test notes):

- A real text conflict at `--conflict-max-tier 2` (P2): the commit body shows the record; the validator disagreement path; a deliberate semantic conflict halts with nothing pushed; reviewers are re-triggered on the merge head.
- GitHub's own `mergeable` after the push is `MERGEABLE`.
- `--resume` after killing the session at each point of 5.8.
- Probe on a repo where `git merge-tree` is unavailable degrades to report-only.

### 8.6 Run order for the implementer

<!-- Source: Base (original) -->

`uv run pytest tests/pr_submit tests/unit/test_cli_install.py tests/commands -q`, then `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, then `make test` (VG-2 is forced by `fsm.py`/`run_log` edits).

### 8.7 What deliberately has no automated test

<!-- Source: Variant C (haiku:qa), Section 9.3 (U-021): merged per Change #22, rewritten to cover only live surfaces -->

No automated test covers only these live surfaces: the live push to GitHub, the live reviewer re-trigger POST, and real-GitHub reads (`mergeable`, the merge-method fields, check registration). Each is covered by the manual items of section 8.5. Git mechanics themselves (merge start, partial-commit refusal during a merge, `MERGE_HEAD` detection, the finish gate) are covered by the hermetic real-git tests of section 8.1.

## 9. Minimal-risk transformation path (phasing)

<!-- Source: Base (original, modified): phase contents per Change #1 (R2-B M1); create-path precursor per Change #13; P1 gate per Change #23; flag per Change #15 -->

Each phase is shippable alone, adds no behaviour that the next phase must undo, and has a go/no-go gate. This is the refactorer's core contribution: the riskiest element (publishing a model-resolved merge) arrives last and dark.

| Phase | Ships | Mutates repo or remote? | Go/no-go before the next phase |
|---|---|---|---|
| **Precursor: create path at L1+** | The separate create-path change of AD-7 (FR-31): at L1+ the create path neither rebases nor halts when behind base; L0 unchanged; the pins at `test_static_grep.py:658` and `:660` rewritten | No | The `:649-657` pins pass unchanged. |
| **P0 Detect and report** | `probe-merge.sh`, `conflicts.parse_stage_records`, `classify_conflicts`, `mergeability_hint`, `conflict_action` (report rows), the GitHub-first Wave 0 detection and report and the Wave 8a report-only path at every ordinal, wave-table rows, `refs/conflict-mechanical.md` (report sections only), `--conflict-max-tier` flag parsed but only 0 acted on | No (a fetch of `origin <base>` only) | The report matched GitHub's own `mergeable` on at least 5 real PRs, or the disagreements are explained. |
| **P1 Tier 1, the publish machinery and the Tier 3 Wave 0 halt** | `merge_parent_ok`, `merge_preflight_ok`, `evaluate_sync_decision`, the `build_push_triad` keyword arguments and `kind` on every push record, the two events, the kind-aware run-log fold and recovery (`crash_resume_plan`), the cycle-id prefixes, `finish-merge.sh`, the `uv.lock` `MechanicalRule`, the Wave 0 operation check, the Tier 3 Wave 0 halt, L2 stop, L3 push, post-sync CI re-poll with `expect_checks`, the `pr_conflicting` skip, the wait-only carve-out, rejected-push handling. `refs/conflict-mechanical.md` in full; the split into two refs is fixed here. No `transition()` row, no `evaluate_push_decision`, no `push_parent_ok`, no S5a text is touched | Yes (merge commit, fast-forward push) | The P1 gate of section 8.5: (a) the hermetic real-git test passes; (b) one manual live L3 run on a separate repository that tracks `uv.lock`. Also `--resume` exercised at each crash point, and no change to any pre-existing test except the edits listed in section 8.2. |
| **P2 Tier 2** | The `(S2_CLASSIFY, "conflicting")` edge with its row assertion, the widened S5a clause, `refs/conflict-intent.md`, the evidence step (`collect-conflict-evidence.sh` or inline), the resolution record and `resolution_record_ok`, the validator step, the high-suspicion checklist; default stays `--conflict-max-tier 1` | Yes, only when the operator passes `--conflict-max-tier 2` | At least 10 real text-conflict runs with zero silent behaviour loss found in review; then decide to flip the default to 2 (OQ-1). |
| **P3 Late re-sync** | `merge_state` in the CI poll payload, the second Wave 8a trigger (Tier 0 and 1 only) | Yes | Observed need: at least one real run where the base moved during the CI wait. |

Rollback per phase is a code revert; at runtime `--conflict-max-tier 0` restores today's behaviour (plus the report) with no other change. A pushed merge is reversed by a revert commit, never by rewriting history.

## 10. Risks

<!-- Source: Base (original, modified): Likelihood and Impact split into two columns per Change #19 (Variant C, Section 10; R2-C QA-10); K1 reworded per W20; K2, K8, K9 aligned with Changes #1 and #6; K14 from Variant C R14; K15 per QA-10; K16 to K25 from invariant-probe.md MEDIUM rows -->

| # | Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| K1 | A model-resolved Tier 2 merge silently drops behaviour and is pushed at L3 | Medium | High | Default `--conflict-max-tier 1`; mandatory one-sentence intents; `dropped` field in the commit body; independent `evidence-validator` grounding check; VAL; reviewers re-triggered on the merge head; Tier 3 on any doubt; revert path | Validator and author share model biases; the dark-launch gate in P2 is the real control. |
| K2 | Local `merge-tree` and GitHub disagree about conflicts | Medium | Low | GitHub is read first and decides whether to probe; once the probe ran, local is the truth for action; `github_disagrees` reported | GitHub `CONFLICTING` with an empty local set has no agreed action yet (K22). |
| K3 | `uv lock` needs network or changes unrelated pins | Medium | Medium | PR-side seed keeps pins; `uv lock --check`; report the lock diff in the commit body; failure is a halt | A forced re-resolve if the seed fails (halts, never auto-retried). |
| K4 | Hooks (`pre-commit`, `commit-msg`) reject the merge commit | Medium | Low | Hooks stay on; output reported verbatim; merge left in progress; no amend | Operator must finish by hand. |
| K5 | The pinned-substring tests make `SKILL.md` brittle | High | Medium | Additive edits only; section 8.4 regression test of the untouchable fragments; `SKILL.md` growth capped (NFR-9) | None specific to this feature. |
| K6 | An L2 merge in progress confuses a later run | Low | Medium | `sync_started` marks it as ours; the unconditional Wave 0 operation check halts; foreign operations halt; the L2 message tells the operator to commit or abort | A user who ignores both. |
| K7 | The base moves between probe and push | Medium | Low | Merge by recorded `base_sha`; fast-forward push unaffected; PR is "behind" again but mergeable | One more sync cycle on the next run. |
| K8 | Reviewers never see a Tier 1 `M` | High | Low | Tier 1 is mechanical; the commit body carries the record. Tier 2 merges are re-reviewed (section 5.6) | A human reviewer is the only reader of a Tier 1 regenerate. |
| K9 | A Tier 3 conflict first seen by the Wave 8a re-probe arrives after the review phase | Medium | Low | Wave 0 detection halts a Tier 3 at L3 before any review round; review results retained in the final report | Wasted review time when the tier rises between hooks (K18). |
| K10 | `gh pr view --json mergeable,mergeStateStatus,baseRefName` field set varies by gh version | Low | Low | Failure yields `null` hints and the probe runs; capability text in the ref | None. |
| K11 | A conflict marker legitimately present in a file (docs, tests that discuss conflicts, this very repo) trips the guard | Medium | Low | Guard compares marker-line counts with the stage-1 blob, so only *introduced* markers fail | A file where a side added a legitimate marker example halts with `sync_marker_left`; human finishes. The repo's `check-merge-conflict` hook disagrees with this allowance (section 12, INV-032). |
| K12 | Large Tier 2 cycles extend wall-clock early in the run | Medium | Low | `TIER2_MAX_FILES` cap; `--timeout` unaffected (it bounds waits, not resolution) | Cap value is a guess (OQ-9). |
| K13 | Reverting a merge commit is non-obvious (`-m 1`) | Low | Low | The refs and the L2 and L3 reports include the exact revert command | None. |
| K14 | A Tier 2 resolution validates but is semantically wrong (clean tests, broken behaviour), the core residual risk | Certain, partially | A merged PR that is worse than a halted one | The resolution record, the `evidence-validator` grounding check and the R-156 behaviour sentence reduce it, they do not eliminate it; Tier 3 escalation on unclear intent (R-18) is the designed backstop; the merge commit is re-reviewed like any authored change (J-66) | Accepted and stated in the report. |
| K15 | A future edit re-narrows the S5a clause and silently kills every Tier 2 re-trigger | Not rated | High | The QA-3 behavioural test (a zero-edit merge cycle re-triggers) and the new static pin | None while the test exists. |
| K16 | INV-005: resume after "crash between merge commit and push" trusts local HEAD by its parents only, so an operator-made or amended merge commit could be pushed without the finish gate or VAL | Not rated | Medium | Open question (section 12): re-run `finish-merge.sh` and VAL on resume | Open. |
| K17 | INV-010: at L2 a Tier 2 conflict first seen at Wave 8a is resolved locally while L3 halts `late_conflict`, so a higher ordinal does less | Not rated | Medium | Open question with three options (section 12) | Open. |
| K18 | INV-011: a tier that rises between Wave 0 and a later hook has no specified route | Not rated | Medium | Open question: route a re-probe tier increase between hooks | Open. |
| K19 | INV-012: a tier above `--conflict-max-tier` has no defined route at L3 | Not rated | Medium | Open question: route tiers above the cap at L3 | Open. |
| K20 | INV-013: the finish gate accepts arbitrary edits to a base-changed path that was not conflicted | Not rated | Medium | Open question: require staged blob == `merge-tree` result for non-resolved paths | Open. |
| K21 | INV-014: a base that is itself lint-red or test-red blocks every merge, with no baseline to tell base-caused from resolution-caused failures | Not rated | Medium | Open question: VAL baseline on base | Open. |
| K22 | INV-022: GitHub `CONFLICTING` with an empty local conflict set has no defined action | Not rated | Medium | Open question | Open. |
| K23 | INV-027: the final status can read `terminal_clean` while the post-push `mergeable` is `CONFLICTING` | Not rated | Medium | Open question: truthful status on post-push `CONFLICTING` | Open. |
| K24 | INV-030: the `C-initial` re-trigger may not produce a review attributed to the merge head (configured-reviewer substitution; a race with the open-time review on the create path) | Not rated | Medium | The substitution is pinned (section 5.6); the race is an open question | Open, in part. |
| K25 | INV-031: re-review findings after a Tier 2 merge may cover base-authored lines | Not rated | Medium | Open question: scope findings to the PR diff after a merge | Open. |

## 11. Out of scope

<!-- Source: Base (original, modified): create-path bullet replaced per Change #13; re-trigger bullet narrowed to Tier 1 for consistency with Change #1; CI-classification bullet aligned with Change #25 -->

- Rebasing, force-push recovery, history rewriting of any kind (R-02, R-16 to R-38).
- PR decomposition or splitting (R-09, R-10, R-37 to R-39).
- Resolution by external tools (mergiraf and similar), snapshot or notebook special-casing, rerere (R-60, R-62, R-64 to R-69).
- Conflict resolution on the create path before a PR exists. At L1+ the create path neither rebases nor halts when behind base (AD-7); L0 keeps today's rebase.
- PRs whose head lives on a fork (cross-repo head): the skill never pushes there (existing rule), so it reports only.
- Cherry-pick, revert and rebase operations in progress: detected, then halted (J-17), never resumed or finished.
- Resolving conflicts in any worktree other than the current one, or merging the base into any branch other than the PR head (J-05, J-91).
- A user-override channel (R-19, R-20) and a separate conflict-only command.
- Server-side `gh pr update-branch`.
- Re-triggering reviewers after a Tier 1 sync, replying to threads for it, and giving a sync cycle a share of `max_rounds` (a Tier 2 merge cycle does all three, section 5.6).
- Migration, submodule, binary, protected-file and unknown-lockfile resolution: these halt by design.
- Changes to reviewer detection, severity routing, loop guard semantics or CI classification, other than the additive `merge_state` field in P3 and the `expect_checks` keyword (section 6.10).

## 12. Open questions

<!-- Source: Base (original, modified): OQ-3, OQ-4, OQ-5, OQ-7 and OQ-11 closed by Changes #1, #6, #8, #13, #23; OQ-1 flag renamed per Change #15; OQ-15 to OQ-21 from the unresolved diff points and OPEN items of Changes #6, #11, #17; OQ-22 onward from the MEDIUM and LOW items carried by the plan -->

| # | Question | Recommendation | Impact if wrong |
|---|---|---|---|
| OQ-1 | Default for `--conflict-max-tier`: 1 or 2? | 1 for the first release; flip after the P2 gate. | Default 2 pushes model-resolved text merges for every L3 user on day one. |
| OQ-2 | Tier 0 behind-only with a branch rule "require up to date" (`mergeStateStatus` BEHIND): act or report? | Report only in v1; a clean `merge --no-commit` is the same machinery and can be enabled by a one-line policy flip. | A protected repo needs a manual update-branch click. |
| OQ-3 | Should a Tier 2 merge re-trigger reviewers so a bot sees the resolution? | **Closed:** yes, through the P2 edge and the widened S5a clause (section 5.6); Tier 1 does not. | n/a |
| OQ-4 | Should Wave 8a act on the wait-only paths (`HALT_MAX_ROUNDS`, `TERMINAL_AUGMENT_NO_RESPONSE`)? | **Closed:** Tier 1 acts on all four armed outcomes at L3 and keeps the preserved status; L2 reports only (section 5.5); the wait-only sentences carry the one exception (section 6.9). | n/a |
| OQ-5 | Are real-repo script tests acceptable under "no live git network tests"? | **Closed:** yes; hermetic real-git tests in a pytest temporary directory are mandatory for the P1 gate (section 8.5). | n/a |
| OQ-6 | Tier 1 lock seed: PR side (`--ours`) or base side? | PR side, because the manifest from the PR is merged in and `uv lock` then adds the base's new dependencies; verify on a real conflict that base-added pins are not downgraded. | Dependency drift in the lock file. |
| OQ-7 | Replace the create-path rebase with a sync merge? | **Closed:** at L1+ the create path neither rebases nor halts when behind base (AD-7); L0 keeps the rebase. | n/a |
| OQ-8 | Which `gh pr view --json` fields are guaranteed (`mergeable`, `mergeStateStatus`, `baseRefName`)? | Probe at run time like the CI preflight; hints are optional. | Probe returns nulls; behaviour is still correct. |
| OQ-9 | `TIER2_MAX_FILES = 8`: right value, and do regenerated files count toward it (INV-020, LOW; A proposed 10)? | Ship 8 as a named constant; revisit after 10 runs. | Too low halts easy conflicts; too high spends a long cycle. |
| OQ-10 | Is a `pyproject.toml` conflict Tier 2 or Tier 3 (dependency changes are high-suspicion, R-180)? | Tier 2 with forced VG-2 and `uv lock --check`. | A bad dependency merge reaches CI. |
| OQ-11 | Can the FSM reach `S4'_HALT_BEFORE_PUSH` from the Wave 8 position? | **Closed:** the caller sets S4' (`fsm.py:1118-1121`), only when Wave 8 was entered from `clean` or `REPORT_ONLY` (section 5.4). | n/a |
| OQ-12 | Is the `evidence-validator` pass mandatory for Tier 2? | Yes in v1; measure its disagreement rate in P2 and relax if it never disagrees. | Extra spawn cost for no signal. |
| OQ-13 | Commit attribution lines on the merge commit | Follow the session's commit rules at commit time (the finish script takes the message from a file written by the skill). | Missing attribution. |
| OQ-14 | Should `needs_rebase` (T-107) be renamed or its docstring updated now that merging is the supported way to catch up? | Leave as is; it is pinned by T-107. | None. |
| OQ-15 | Reason code for the Wave 0 operation-in-progress halt: `operation_in_progress`, `foreign_op_in_progress` or `merge_in_progress`? | Default `foreign_op_in_progress` (matches `foreign_op`). | Naming churn only. |
| OQ-16 | VG-2 at Tier 2 (C-028 / X-019): base rule (forced only for `pr_submit/` or a `pyproject.toml` conflict, plus `is_cross_cutting`), A's mandatory VG-2 at Tier 2, or C's `is_cross_cutting` only? | Base rule kept as the default (section 6.7). | A semantically broken Tier 2 merge passes VAL. |
| OQ-17 | Tier 2 run-log events (C-029 / X-011): A's `conflict_classified` / `conflict_resolved`, C's three events (44), or none in P1 (inv-B)? | Tier 1 keeps `sync_started` / `sync_concluded`; decide before P2; apply QA-6's pin sweep whatever the count. | Pin churn. |
| OQ-18 | Pre-push guard order (X-009): base head -> parent -> base ancestry -> decision, or A's head -> ancestry -> parent -> decision? | Base order kept (section 6.4 step 10). | Different halt reason on a double failure. |
| OQ-19 | Mid-resolution stop (C-027 / X-021): abort (base) or leave the merge in progress (inferred majority, 60%)? Interacts with INV-004 and INV-010. | Base abort kept (section 6.8). | Lost partial work, or a stale merge that the Wave 0 check halts on. |
| OQ-20 | Exact wording of the wait-only carve-out (three proposals; meaning agreed). | Decide with the pin (section 6.9). | None beyond wording. |
| OQ-21 | INV-010: Tier 2 first seen at Wave 8a. A: same action at L2 and L3, plus a monotonicity property test. B: drop Tier 2 resolution at L2. C: accept as a risk row (K17). | Undecided. | A higher ordinal does less than a lower one. |
| OQ-22 | INV-005: re-run `finish-merge.sh` and VAL on resume before pushing a found merge commit? | Suggested handling from the probe; undecided. | K16. |
| OQ-23 | INV-011: route a re-probe tier increase between hooks. | Undecided. | K18. |
| OQ-24 | INV-012: route tiers above the cap at L3. | Undecided; today `report` / `tier_above_cap`. | K19. |
| OQ-25 | INV-013: require staged blob == `merge-tree` result for non-resolved paths? | Undecided. | K20. |
| OQ-26 | INV-014: VAL baseline on the base? | Undecided. | K21. |
| OQ-27 | INV-022: action for GitHub `CONFLICTING` with an empty local set. | Undecided. | K22. |
| OQ-28 | INV-027: truthful status when the post-push `mergeable` is `CONFLICTING`. | Undecided. | K23. |
| OQ-29 | INV-030 (remaining part): the create-path race between the open-time review and the `C-initial` re-trigger. | Undecided. | K24. |
| OQ-30 | INV-031: scope findings to the PR diff after a merge. | Undecided. | K25. |
| OQ-31 | INV-008 hardening (A alone): also refuse untracked rule-input paths? | Not adopted; B and C tolerate untracked files. | `uv lock` reads an untracked input. |
| OQ-32 | INV-035 hardening (A alone): refuse the push before it happens on a rebase-only repository? | Not adopted; the merge-method fields stay advisory. | A rejected push (handled by `push_rejected`). |

LOW items, one line each:

- INV-016: use `--no-renames` on both diffs that feed the finish gate's subset check.
- INV-019: which per-run merge bound is intended (Tier 2 `<= 1` plus Tier 1 `SYNC_CAP = 1`).
- INV-020: cap 8 versus 10, and whether regenerated files count (OQ-9).
- INV-021: `--max-rounds 0` and `1` with Tier 2 (a merge at `max_rounds = 1` spends the only round).
- INV-025: root-anchored rule pattern; handled (section 3.4).
- INV-032: the repo's `check-merge-conflict` hook versus the finish gate's marker allowance.

## 13. Index

### 13.1 Research items adopted (ids with ROI above 5) and where they land

<!-- Source: Base (original, modified): J-66 landing extended to section 5.6 for the Tier 2 re-review of Change #8; otherwise original -->

| Items | Lands in |
|---|---|
| R-05, R-18, R-156, S-26, S-29 (halt when intent is not statable; no third behaviour; say what was dropped) | FR-10, FR-23, section 4.3, 6.6 |
| R-11 (no markers) | FR-11 (introduced-marker check) |
| R-13, R-14, R-15, J-20, J-60, J-63, J-05, J-06, J-91 (prohibited operations, no stash, no `--no-verify`, no amend, current worktree only) | FR-21, 6.9 |
| R-43, R-54, R-56, R-57, R-84 (submodule, migration, binary, unreadable halt) | FR-2 rules 1, 3, 5, 6; 4.3 |
| R-58, R-59, R-189, S-46, J-48 (generated and lock files regenerate from resolved sources; halt without a rule; only the lockfile's manager) | FR-2 rules 7 to 9, FR-9, 6.5 |
| R-51, R-210, R-212 (report before editing; HALT message content) | FR-4, FR-10 |
| R-112, S-12, S-13, S-14, S-17, R-181 (stage reads, left-right log, both merge-base diffs, three-way comparison) | FR-22, 4.4 |
| R-146, R-149, R-150 to R-154 (root cause and kind labels; additive, structural, delete-versus-edit) | FR-23 record, 6.6 |
| R-180, R-251 (high-suspicion checklist; no API drop before consumers move) | 4.4 |
| S-05, S-09, J-13, J-15, J-16, J-17, J-18, J-26 (operation ownership, ours/theirs meaning, abort lines, detached head, dirty tree, default branch) | FR-1, FR-7, FR-27 |
| S-38, S-39, S-40 (tree conflicts via status codes; delete-versus-edit; add/add) | FR-2 rules 11, 12 |
| J-39, J-40, J-53, J-56, J-61, J-66, R-173 (agent does the judgment, one file at a time, leave merge in progress when complete, exact staging, hook output verbatim, resolution is authored code, no extra LLM client) | 3.2 R1, 5.6, 6.4, 6.8 |
| R-128 (never auto-apply a historical result) | FR-8 (`rerere.enabled=false`) |
| R-169 (no unrelated changes on retry) | 6.7 |
| R-02 (bounded scope) | section 11 |

Adopted in spirit, deliberately simplified: R-26 and R-40 (a probe JSON instead of a status script and categoriser), R-33 (one tunable file cap instead of rebase-step thresholds), R-17 (bulk operation only for the single regenerate category).

Considered and rejected from the above-5 set: R-19, R-20 (no override channel), R-60 (snapshots: fold into "generated without rule"), R-101 (read-only recombination subsystem), R-161 (whitespace check duplicates VG-3 and VG-4), J-15 (already covered by `pr_branch_ok` rejecting `HEAD`), S-18 and S-39 overlaps (covered by the kind labels).

### 13.2 Files this design creates or edits

<!-- Source: Base (original, modified): file list per Changes #2, #7, #8, #10, #17, #25; base Appendix A retired per Change #13 and Appendix B folded into sections 5.3 and 6.4 per Changes #7 and #24, so no appendix remains under this Index -->

| Kind | Path |
|---|---|
| New | `src/superclaude/pr_submit/conflicts.py` |
| New | `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`, `refs/conflict-intent.md` |
| New | `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `finish-merge.sh` (P1); `collect-conflict-evidence.sh` (P2, unless written inline) |
| New tests | `tests/pr_submit/test_conflicts_core.py`, `test_conflict_sync_protocol.py`, `test_conflict_scripts.py`, `fixtures/merge_tree_conflict.z` |
| Edit | `src/superclaude/pr_submit/models.py` (+2 events, docstring), `run_log.py` (kind-aware fold, `sync_cycles`, `sync_push_count`), `recovery.py` (key tuple + the `crash_resume_plan` call), `fsm.py` (argument parser and `build_push_triad` keyword arguments in P1; one edge and the S5a clause in P2), `ci.py` (`expect_checks`), `__init__.py` (exports) |
| Edit | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `refs/state-machine.md` (section 5.2d, `:144-146`), `refs/ci-poll.md` (`:21`, `:28-29`), `scripts/poll-ci-checks.sh` (`--evidence-sha`), `src/superclaude/commands/pr-submit.md` |
| Edit tests | see 8.2 |
| After editing | `make sync-dev`, `make verify-sync`; stage only the `src/` and `tests/` side, never `.claude/` mirrors |
