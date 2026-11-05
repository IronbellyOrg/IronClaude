# Spec: merge-conflict resolution for sc:pr-submit (issue #305), variant 1 (architect)

Status: draft for adversarial comparison. Domain: code. Source: `seed-brief.md`, `enrichment/codebase-context.md`, `.dev/research/issue-305-conflict-resolution/03-roi-scored-list.md` (items scored above 5). Paths are relative to the repo root. Line citations were re-read on 2026-11-04 against the worktree at commit `119622e3`.

## 0. Summary

sc:pr-submit gains one reusable procedure, **Wave C (conflict gate)**, called at two hook points: after arming and before the first review poll (`C-initial`), and before Wave 8 arms the CI wait (`C-ci`). Wave C reads GitHub's mergeability, and only when the PR conflicts does it pay for more: a read-only local probe (`git merge-tree --write-tree`, which never touches the working tree), a deterministic per-path classification into four tiers, and then a tier-specific procedure.

| Tier | Meaning | Who decides | Cost paid |
|---|---|---|---|
| 0 | No conflict (behind only, or mergeable) | core | one `gh pr view` read |
| 1 | Mechanical: lockfile regenerate, generated file regenerate, whitespace-only | core rule table | fetch, probe, merge, regenerate, VAL, one ref |
| 2 | Text or tree conflict resolved by stated intent | main session, checked by `evidence-validator` | Tier 1 cost plus a second ref, per-file records, evidence check, full `make test` |
| 3 | Semantic or high-risk (submodule, binary, symlink, migration, protected config, unreadable, too many files, intent not statable) | human | a HALT message; nothing pushed |

The resolution is published as **one merge commit** of the fetched `origin/<base>` tip into the PR branch, pushed as a fast-forward with the existing push triad. A new pure check `merge_parent_ok(parents, pre_push_sha, base_sha)` (parents exactly `[pre_push_sha, base_sha]`, in that order) replaces `push_parent_ok` **for that push kind only**; `push_parent_ok` is not loosened. A conflict cycle is an ordinary remediation cycle: it enters the FSM through one new edge `(S2_CLASSIFY, "conflicting")`, consumes a round on the existing INV-001 edge, re-triggers the reviewers through the existing S5a path, and keeps every existing invariant (`push_count <= max_rounds`, one commit per cycle, no force-push, head guard before parent check before `push_decision`).

Mechanism mix: one new pure core module (`conflicts.py`), two new lazily loaded refs (`conflict-mechanical.md`, `conflict-intent.md`), two new run-log events, one optional flag (`--conflict-max-tier`), one new FSM edge, additive fields on the push records. No new agent, no new script, no new template file, no new FSM state, no new idempotency set, no new dependency.

## 1. Current behaviour and the gap

| Fact | Evidence |
|---|---|
| Nothing reads GitHub `mergeable` or `mergeStateStatus`. The only PR read in the poll script is `--json number,url,headRefName,headRefOid,baseRefName`. | `scripts/poll-augment-review.sh:38`; zero grep hits per `enrichment/codebase-context.md` section 3 |
| On `--pr <N>` the skill only reports how many commits behind; on the create path Wave 0 says "rebase if behind". | `SKILL.md:267` |
| The STOP block and the Error Handling row say the create path HALTs when behind base, contradicting Wave 0. Both sides are pinned by one test. | `SKILL.md:220-223`, `SKILL.md:315`; `tests/pr_submit/test_static_grep.py:654-661` |
| The create-path rebase cannot work as written: the head is already published when `gh pr create` runs, so a rebased checkout no longer equals the PR head and Wave 0 head binding fails; the skill's own message says a rebased branch "needs a force-push, which this skill never does for you". | `SKILL.md:268` |
| `push_parent_ok` fails any commit with a parent count other than one; a test pins the two-parent case as a failure. | `src/superclaude/pr_submit/fsm.py:582-600` (`:593`); `tests/pr_submit/test_pre_pr_checks.py:216-222` |
| The fix commit uses `git commit --only -- <paths>`, which git refuses during a merge ("cannot do a partial commit during a merge"). | `SKILL.md:274`; [external] git behaviour |
| Push records carry no push kind; recovery copies a fixed key list into its recovery events. | `fsm.py:238-288`; `src/superclaude/pr_submit/recovery.py:98-110` |
| The run-log event enum is closed at 41 members, pinned twice. | `src/superclaude/pr_submit/models.py:22-90`; `tests/pr_submit/test_run_log.py:168`; `tests/pr_submit/test_codex_reviews.py:441` |
| `transition()` is a flat table; an unknown edge stays put; `needs_human_decision` short-circuits to `HALT_HUMAN` first. | `fsm.py:716-802` (`:730-731`, `:801-802`) |
| [external] GitHub does not run `pull_request` workflows while a PR has a merge conflict, so a Wave 8 CI wait on a conflicted PR can only report `polling` until timeout. | `enrichment/codebase-context.md` section 3 |

The gap: a PR whose reviews and CI could be clean stays unmergeable, and the run ends in a report or a timeout. The fix must not make a lockfile conflict pay for semantic analysis, and must not weaken any push rule.

## 2. Architectural decisions

Each decision states the choice, the alternatives rejected and why. These are binding on the FRs in section 8.

**AD-1. Integrate by merge, never by rebase.** The PR head is published; rebasing it requires a force-push, which `SKILL.md:305` forbids. A merge commit with parents `[pr_head, base_tip]` is a fast-forward of the PR branch. Rejected: rebase plus `--force-with-lease` (violates the rule outright); squash-merge of base changes into a single-parent commit (it would publish base content as if authored on the PR and defeat the parent check's purpose).

**AD-2. Conflict first, then review.** Wave C runs before the first review poll. Reviewing a head that must change wastes reviewer quota, produces findings on pre-merge code, and CI cannot run while the PR conflicts. Consequence: at L1 and L2 a conflicted PR stops after Wave C (section 5.3); only L3 proceeds into review with a conflict-free head.

**AD-3. A conflict cycle is a remediation cycle, not a new kind of thing.** It enters the existing FSM at `S3_FIXING` through one new edge, reuses `S7_VALIDATING`, `S4_PUSHING`, `S6_REPLYING` / `RESOLVING` (with zero threads), `S5a_RETRIGGER_REVIEW` and `S5_AWAITING_REREVIEW`, and ticks `round_counter` on the existing INV-001 edge. This keeps `push_count <= max_rounds` (`SKILL.md:239`), INV-R1 `rereview_request_count <= max_rounds` and INV-R2 `push_count <= max_rounds + 1` (`SKILL.md:275`) true with no edits. Rejected: a separate `conflict_round_counter` like the fallback counter (it would need a second "+1" in INV-R2, a new fold in `rebuild_state`, and a new Output Contract field, for no safety gain); a SKILL-only path outside the FSM like CI (`state-machine.md:140-157`) (the CI pattern works because a CI push skips S5a; a conflict push must be re-reviewed, J-66, so it needs the S5a and S5 edges anyway).

**AD-4. Tier 3 reuses the one override.** A Tier 3 classification sets `needs_human_decision` in the transition context, so `transition()` returns `HALT_HUMAN` at any ordinal (`fsm.py:730-731`, `state-machine.md:81-84`). No new terminal, no new status value.

**AD-5. Decide in the core, act in the skill.** Parsing stage listings, classifying paths, picking the tier, routing by ordinal, the merge-parent rule, marker scanning, record validation, commit-message rendering and the resume decision are pure functions in a new `conflicts.py` that joins the T-N50 core-pure set (`test_static_grep.py:37-51`). Every `git` / `gh` call lives in SKILL.md and the refs. This mirrors how `ci.py` was added (`src/superclaude/pr_submit/ci.py:1-5`).

**AD-6. Classify before touching the working tree.** `git merge-tree --write-tree -z <pre_push_sha> <base_sha>` reports conflicted paths with their index stages (`<mode> <oid> <stage>\t<path>`) and exit status 1 on conflict, without changing the working tree or index (verified locally with git 2.47.3 on 2026-11-04). So L1 proposes and Tier 3 halts with nothing to undo. Only the stage set and modes are parsed; git's informational messages are not a stable format and are never parsed.

**AD-7. Settle the create-path contradiction by removing the rebase.** Wave 0 never rebases on either path. Being behind base is a Tier 0 report, not a HALT; conflicts are handled by Wave C after the PR exists. The STOP block and Error Handling row drop "behind base branch (create path)". `needs_rebase` stays as the "is behind" predicate for the report (its docstring changes; T-107 at `test_pre_pr_checks.py:64-72` keeps its assertions). Rejected: keeping HALT (it blocks the exact case this feature fixes); keeping rebase (cannot be published without force-push, see section 1).

**AD-8. One commit per cycle still holds; the merge commit is the conflict cycle's one commit.** A conflict cycle applies no review-finding edits, and a review cycle never starts while a merge is in progress. The two never share a commit.

**AD-9. L2 leaves the merge unconcluded.** At L2 the merge is resolved, every path staged, VAL run, and the run halts at `S4'_HALT_BEFORE_PUSH` with `MERGE_HEAD` still present: no commit, matching T-412 "commit never" (`state-machine.md:97-106`). The operator concludes it with one commit command printed in the HALT message. Rejected: a local-only merge commit at L2 (breaks the L2 "no commit" contract that the state-machine ref and its tests state).

**AD-10. Extension by data, not by branching.** Mechanical rules (lockfiles, generated files) and human-only path patterns are tuples of frozen dataclasses passed as default arguments (`rules=MECHANICAL_RULES`, `human_paths=HUMAN_PATH_PATTERNS`). Adding a rule is one tuple entry plus one parametrized test row; a future project-local rule file plugs in by passing a different tuple, with no change to the tier logic.

## 3. Mechanism mix: what is added, what is rejected

The test for each piece: does it carry a decision that must be deterministic and tested (core), knowledge only some runs need (ref, lazily loaded), an independent check that must not share the resolver's context (agent), or I/O (inline tool calls)? Anything that is none of these is rejected.

### 3.1 Adopted

| Piece | Kind | Why it earns its cost | Loaded or run when |
|---|---|---|---|
| `src/superclaude/pr_submit/conflicts.py` | pure core module | Every tier decision, the merge-parent rule and the resume decision are deterministic and must be unit-tested without a live repo (seed brief Q8). A separate module, not more code in `fsm.py`, because `fsm.py` already is 1183 lines and is a VG-2 shared-infra marker (`fsm.py:623`); a conflict-only change then stays out of `fsm.py`'s blast radius. | Imported by the SKILL in Wave C |
| One new edge in `transition()` | core edit | The conflict cycle must reach `S3_FIXING` / `PROPOSED` / `HALT_MAX_ROUNDS` through the same gates as findings (AD-3). One edge, no state. | `fsm.py` transition table |
| `merge_parent_ok` | pure core function in `conflicts.py` | The only safe way to publish a two-parent commit; a narrow sibling of `push_parent_ok`, which stays byte-identical. | Pre-push guard of a merge push |
| `refs/conflict-mechanical.md` | ref | Tier 1 procedure: probe, merge, per-rule regenerate, marker check, merge-commit recipe, HALT texts. Needed only when a PR conflicts. | Wave C, tier 1 or 2 |
| `refs/conflict-intent.md` | ref | Tier 2 procedure: stage reads, evidence recipe, intent rules, record format, evidence-validator dispatch. Needed only for text conflicts; a Tier 1 run never loads it. Splitting the refs is what makes cost grow with tier. | Wave C, tier 2 only |
| 2 run-log events (`conflict_classified`, `conflict_resolved`) | closed-enum edit | The write-ahead anchor for `--resume` inside a merge, and the per-file audit record. Existing events cannot carry this: `fix_applied` is keyed on a finding `fix_key` (`run_log.py:255-256`). | Wave C |
| `push_kind` and `base_sha` fields on the push triad | additive record fields | Recovery Branch B must re-drive the right check for the right commit (`recovery.py:149-159`). Fields, not new events, so the triad shape and idempotency key stay unchanged. | Every push |
| `--conflict-max-tier {0,1,2}` (default 2) | flag | Lets an operator allow mechanical resolution but forbid model-judgment resolution (cap 1), or make Wave C report-only (cap 0), independent of `--monitor`. Tier 3 is never allowed. | Parsed once |
| `evidence-validator` (existing agent, reused) | agent dispatch | A Tier 2 resolution states intent; an independent read-only checker that re-reads cited lines is the cheapest guard against an invented third behaviour (S-26) or an unannounced drop (S-29). It is read-only (`src/superclaude/agents/evidence-validator.md:1-9`), so the main session keeps every side effect (`SKILL.md:82-84`). | Tier 2 only, one batch per cycle |
| Inline `gh pr view ... --json mergeable,mergeStateStatus,headRefOid,baseRefName` and inline `git` commands | tool calls | Same pattern as the head-binding read (`SKILL.md:268`); one call, no wrapper needed. | Wave C |

### 3.2 Rejected

| Candidate | Why rejected |
|---|---|
| New `conflict-resolver` agent | Resolution needs write access and git; the skill rule is that the main session performs every side effect and never hands one to a subagent (`SKILL.md:82-84`). An agent with Bash would also be a second place to enforce the never-stash / exact-path / no-hook-bypass rules. J-39: resolution is the session's own work. |
| Routing Tier 2 through `/sc:troubleshoot` | Troubleshoot diagnoses defects and stops at a plan (`refs/troubleshoot-dispatch.md:51-60`); a conflict is not a defect with a symptom. The `--fix` route would also cost a Tier 2 escalation per file. |
| New script (`scripts/pr-mergeability.sh`) | One `gh pr view` call does not need a wrapper; the existing inline head-binding read is the precedent. A script would add an install-list entry (`tests/unit/test_cli_install.py:248-262`) and a fork-pin test target for no logic. |
| Extending `poll-augment-review.sh` with `mergeable` | Considered for mid-run detection, rejected for this release: the two hook points cover the cases that matter (before review, before CI), and changing the snapshot payload touches `test_cosmos_poll.py`. Listed as an extension in section 14. |
| New template file under `src/superclaude/templates/` | HALT messages are pinned inline by tests today (`test_static_grep.py:733-743`); a template file adds a dual-surface lookup (CLAUDE.md installed-path rule) for text the core can render. The resolution record is rendered by a pure function (`render_resolution_summary`) and its schema lives in `conflict-intent.md`. |
| New FSM states (`S1_CONFLICT`, `S1_MERGING`) | The existing working states already express "apply edits, validate, push, re-review"; new states would force `state-machine.md` and every C6 row test to grow for no new behaviour. |
| A new idempotency set | The set count is pinned at 7 (`tests/pr_submit/test_idempotency.py:89`). Per-file resolution progress is derived from `conflict_resolved` events into a plain state field instead. |
| `mergiraf` or any structural merge tool | Seed constraint: no new external dependency. |
| `git rerere` or any global git config | Seed constraint: no global config changes; R-128 says never auto-apply a historical result. Per-command `-c merge.conflictStyle=zdiff3` is allowed because it is scoped to one invocation. |
| Auto-updating a PR that is only behind (mergeStateStatus `BEHIND`) | A merge-up invalidates reviews and spends a round when nothing blocks the merge except an optional "require up to date" rule. Tier 0 reports it; section 14 OQ-3. |

## 4. Tier model

### 4.1 Inputs

For each conflicted path the SKILL hands the core a `ConflictEntry` built from the stage listing (`git merge-tree --write-tree -z` at probe time, or `git ls-files -u -z` once a merge is in progress; both print `<mode> <oid> <stage>\t<path>`), plus three facts it computes only for paths with both stage 2 and stage 3 (content conflicts):

- `is_binary`: `git diff --numstat <oid2> <oid3>` prints `-` `-`.
- `whitespace_only`: `git diff --quiet --ignore-all-space <oid2> <oid3>` exits 0.
- `readable`: every stage blob could be read (`git cat-file -e`).

A fact left `None` fails closed: unknown binary is Tier 3, unknown whitespace is Tier 2.

### 4.2 Tree code from the stage set

| Stages present | Code | Meaning (HEAD = PR head = stage 2, MERGE_HEAD = base = stage 3) |
|---|---|---|
| 1, 2, 3 | `UU` | both modified |
| 2, 3 | `AA` | both added |
| 1, 3 | `DU` | deleted by PR, modified by base |
| 1, 2 | `UD` | modified by PR, deleted by base |
| 2 | `AU` | added by PR, rename-related on base |
| 3 | `UA` | added by base, rename-related on PR |
| any other | invalid | parser raises; whole run is Tier 3 |

### 4.3 Classification rule (first match wins, per path)

| Order | Class | Rule | Tier | Research |
|---|---|---|---|---|
| 1 | `UNREADABLE` | `readable is False` | 3 | R-84 |
| 2 | `SUBMODULE` | any stage mode `160000` | 3 | R-43, R-56 |
| 3 | `SYMLINK` | any stage mode `120000` | 3 | (fail closed) |
| 4 | `HUMAN_PATH` | path matches `HUMAN_PATH_PATTERNS`: migrations (`*/migrations/*`, `*/alembic/versions/*`), `.claude/settings.json`, `.github/workflows/*` | 3 | R-54, S-53, CLAUDE.md `.claude/` rule |
| 5 | `BINARY` | `is_binary is True` or `None` on a content conflict | 3 | R-57 |
| 6 | `LOCKFILE` | path matches a `MechanicalRule` of kind `lockfile` (shipped: `uv.lock`, regenerate `uv lock`) | 1 | R-189, J-48, S-46 |
| 7 | `GENERATED` | path matches a `MechanicalRule` of kind `generated` whose sources are named | 1 | R-58 |
| 8 | `WHITESPACE_ONLY` | code `UU` or `AA` and `whitespace_only is True` | 1 | R-161 |
| 9 | `MODIFY_DELETE` | code `DU` or `UD` | 2 | R-154, S-39 |
| 10 | `ADD_ADD` | code `AA` | 2 | S-40 |
| 11 | `RENAME_SIDE` | code `AU` or `UA` | 2 | R-153 |
| 12 | `TEXT` | code `UU` | 2 | R-152, S-17 |

Run-level rules, applied after per-path classification:

- **Run tier** is the maximum path tier. One Tier 3 path makes the whole run Tier 3: no partial merge is ever published.
- **Generated dependency**: a `GENERATED` or `LOCKFILE` path whose rule names a source that is itself Tier 3 is Tier 3; a generated rule whose source list is empty is Tier 3 (R-59). A source that is Tier 2 is resolved first, then the output is regenerated (R-58).
- **Size bound**: more than `MAX_INTENT_FILES = 10` paths at Tier 2 makes the run Tier 3 (bounds attended cost; R-05 "halt when intent cannot be inferred" at scale).
- **Tier cap**: run tier greater than `--conflict-max-tier` routes to report (cap 0) or halt (cap 1 with a Tier 2 run); Tier 3 always halts.

### 4.4 Tier procedures and exit criteria

**Tier 0 (no conflict).** Entry: GitHub `mergeable == MERGEABLE`, or local probe exit 0. Action: record `conflict_classified{tier: 0}`; report `commits_behind` (from `needs_rebase` input) and `mergeStateStatus`. No fetch when GitHub already says `MERGEABLE` (one read total). Exit: continue to the first review poll (C-initial) or Wave 8 (C-ci).

**Tier 1 (mechanical).** Entry: run tier 1 and cap >= 1. Procedure (`refs/conflict-mechanical.md`): preflight, `git -c merge.conflictStyle=zdiff3 merge --no-ff --no-commit <base_sha>`, then per path, one at a time (J-40):

- `LOCKFILE`: resolve the rule's sources first (they merged cleanly or were resolved in this cycle), take the PR side of the lockfile (`git checkout --ours -- <path>`, exact path), run the rule's regenerate command (`uv lock`), require its check command (`uv lock --check`) to exit 0, stage `git add -- <path>`.
- `GENERATED`: same shape with the rule's regenerate command.
- `WHITESPACE_ONLY`: for a Python path, take the side whose file passes `uv run ruff format --check <path>` (PR side first; if neither passes, the path escalates to Tier 2); for any other path take the PR side.

Exit criteria (all required): `git diff --name-only --diff-filter=U` empty; `conflict_marker_lines` empty for every resolved path (R-11); every regenerate and check command exited 0; VAL green (section 6.4); merge commit parents pass `merge_parent_ok`; after the push, GitHub `mergeable` is not `CONFLICTING`.

**Tier 2 (intent).** Entry: run tier 2 and cap >= 2. Tier 1 paths are handled first with the Tier 1 procedure. Then, per Tier 2 path, one at a time (`refs/conflict-intent.md`):

1. Write the three sides to the run artifacts: `git show :1:<path>`, `:2:<path>`, `:3:<path>` into `<output-dir>/conflicts/<cycle_id>/<n>.base|ours|theirs` (S-12, S-13, S-14). Never trust the hunk labels.
2. Collect evidence: `git log --oneline --left-right --merge -- <path>` and both merge-base diffs (R-112); for signature, schema, constant, dependency or public-API changes also `git grep -n <symbol>` (R-180, R-181).
3. Write the resolution record (section 7.3): one sentence each for the PR side's intent, the base side's intent, and the behaviour after the merge (R-18, R-156); the list of dropped behaviour, explicitly `[]` when nothing is dropped (S-29); evidence citations into the artifact files.
4. Apply by category: trivial or additive, keep both in a stated order (R-150, R-151, S-18); competing, pick or combine by intent (R-152); modify/delete, decide which intent supersedes and restore plus re-apply when the edit is not obsolete (R-154, S-39); add/add, merge contents (S-40); rename, apply the edit at the new location (R-153). Never write behaviour neither side wrote (S-26). Never drop an API or column that a consumer still uses (R-251).
5. If any sentence cannot be written, the path escalates to Tier 3 (runtime escalation).
6. Stage `git add -- <path>` (or `git rm -- <path>` for a deletion) and append `conflict_resolved` (J-56).

After all paths: dispatch one `evidence-validator` batch over the records and the artifact files; an `unsupported` verdict on any record escalates that path to Tier 3. Exit criteria: all Tier 1 criteria, plus every record passes `resolution_record_errors(...) == []` and has a `supported` verdict, plus VG-2 (`make test`) green.

**Tier 3 (human).** Entry: run tier 3, or a runtime escalation, or cap exceeded. Action: append `terminal_halted` (reason `conflict_needs_human`), set `needs_human_decision`, `transition()` returns `HALT_HUMAN`. If detected at probe time, nothing was started (AD-6). If escalated during resolution, the merge stays in progress with finished paths staged (J-53), and the message gives both ways out. Exit: the run ends; nothing is pushed.

HALT message (pinned verbatim, R-210, R-212):

```text
PR #<N> conflicts with <base_ref> and needs your decision. Nothing was pushed.
Operation: merge of <base_ref>@<base_sha7> into <HEAD_BRANCH>; step <i>/<m>.
File: <path> (<class>). PR side appears to: <ours sentence or "unknown">. Base side appears to: <theirs sentence or "unknown">.
<when a merge is in progress> Your checkout is mid-merge with <k> files resolved and staged. Finish it by hand and commit, or discard it with `git merge --abort`.
Then re-run with `--pr <N>`.
```

## 5. Placement in the sc:pr-submit flow

### 5.1 Hook points

Wave C is one procedure with two call sites. It needs the run-log and an armed FSM, so it cannot run in Wave 0.

| Hook | Where | FSM state on entry | Why there |
|---|---|---|---|
| `C-initial` | Wave 1, after `DetectionContract.for_arming()`, output-dir, run-log, baseline and the arm transition (`S0_IDLE -> S2_CLASSIFY`), before the first `poll-augment-review.sh` call | `S2_CLASSIFY` | Reviewers then review a conflict-free head (AD-2). Head binding has already set `HEAD_BRANCH` and `pre_push_sha` (`SKILL.md:268`). |
| `C-ci` | Wave 8, before `should_arm_ci_wait` arms the CI wait | `S2_CLASSIFY` after a merged `clean` / `REPORT_ONLY`, or a preserved terminal (`HALT_MAX_ROUNDS`, `TERMINAL_AUGMENT_NO_RESPONSE`) | The base can move during the run; CI never starts on a conflicted PR, so arming a CI wait there only burns `--timeout`. |

Wave table row to add (`SKILL.md:254-265`):

```text
Wave C: Conflict gate (C-initial in Wave 1, C-ci in Wave 8) ← loads refs/conflict-mechanical.md (tier 1+) and refs/conflict-intent.md (tier 2 only)
```

### 5.2 Sequence inside Wave C

```text
1. read      gh pr view <N> --repo "$REPO" --json mergeable,mergeStateStatus,headRefOid,baseRefName
             UNKNOWN -> re-read at most 3 times, 10s apart (bounded 30s); still UNKNOWN -> treat as "conflicting?" and probe
2. decide    mergeability(...) == "clean" or "behind" -> tier 0 -> record, report, return
3. preflight operation_in_progress? dirty tracked tree? detached? HEAD_BRANCH == base?  -> HALT (FR-C4)
4. fetch     git fetch origin <base>; base_sha := git rev-parse origin/<base>
5. probe     git merge-tree --write-tree -z <pre_push_sha> <base_sha>   (exit 0 clean, 1 conflict, other -> HALT)
6. classify  conflicts.classify_run(entries, facts) -> run tier; conflicts.conflict_action(...) -> action
7. record    append conflict_classified{...}   (write-ahead, BEFORE any merge starts)
8. act       none | report | propose | halt_human | halt_rounds | resolve_local | resolve_push
```

`resolve_local` and `resolve_push` send `transition(S2_CLASSIFY, "conflicting")` and run the tier procedure (section 4.4) in `S3_FIXING`, VAL in `S7_VALIDATING`, then either `S4'_HALT_BEFORE_PUSH` (L2) or the publish path (section 6, L3).

### 5.3 Ordinal behaviour

| Ordinal | Tier 0 | Tier 1 or 2 (within cap) | Tier 3, or tier above a nonzero cap | Cap 0 (any tier) |
|---|---|---|---|---|
| L0 | Wave C never runs (AC-1 byte-identical, `SKILL.md:267`) | never runs | never runs | never runs |
| L1 | report, continue to the first poll | `transition -> PROPOSED`; report the tier, per-path classes and the planned procedure; status `proposed`; the run stops (no review poll, no merge started) | `HALT_HUMAN`, status `terminal_halted`, reason `conflict_needs_human`; nothing touched | report, continue (legacy behaviour plus one report line); Wave 8 is skipped with reason `pr_conflicting` |
| L2 | report, continue | resolve in the working tree, stage every path, VAL; `S4'_HALT_BEFORE_PUSH`, status `halt_before_push`; `MERGE_HEAD` left in place, no commit (AD-9); message prints `git commit --no-edit` and `git merge --abort` as the two ways out; the run stops | `HALT_HUMAN` as L1 | as L1 |
| L3 | report, continue | resolve, VAL, one merge commit, pre-push guard, push triad, S6 / RESOLVING with zero threads, S5a re-trigger, S5 wait; that S5 wait is the run's first review wait | `HALT_HUMAN` as L1 | as L1 |

At `C-ci` after a preserved terminal (`HALT_MAX_ROUNDS`, `TERMINAL_AUGMENT_NO_RESPONSE`), every action collapses to `report` (no transition out of a terminal, `state-machine.md:147-153`), and the CI wait is skipped with reason `pr_conflicting` instead of polling until timeout.

### 5.4 FSM edge and round accounting

One edge is added to `transition()` next to `(S2_CLASSIFY, "findings")` (`fsm.py:741-748`), with the same round gate:

```text
(S2_CLASSIFY, "conflicting"):
    should_halt_rounds(round_counter, max_rounds) -> HALT_MAX_ROUNDS
    else gate_edit(ordinal) -> S3_FIXING, otherwise PROPOSED
```

The pre-gate override already returns `HALT_HUMAN` when the caller passes `needs_human_decision` (Tier 3). Downstream edges are reused unchanged: `S3_FIXING -edits_applied-> S7_VALIDATING -validated-> S4_PUSHING -pushed-> S6_REPLYING -replied-> RESOLVING -resolved-> S5a -retriggered-> S5 -rereview_attributed-> S2_CLASSIFY` (`fsm.py:756-777`). The SKILL sends `replied` and `resolved` with zero threads for a conflict cycle.

| Counter or predicate | Effect of a conflict cycle |
|---|---|
| `round_counter` | +1 on the attributed re-review of the merge push (INV-001 edge, unchanged). A timed-out re-review does not tick it, as today. |
| `applied_edits` (INV-016 predicate 5) | number of resolved paths (Tier 1 and Tier 2); always > 0 when a merge commit exists. |
| `max_rounds` gate (predicate 4) | evaluated at the `conflicting` edge and again at `push_decision`, so `--max-rounds 0` reports and never merges. |
| `push_count` | +1 per landed merge push; the Output Contract bound `push_count <= max_rounds` (`SKILL.md:239`) still holds because each push spent a round. |
| `rereview_request_count` | +1 per conflict cycle (folded by `cycle_id`, `run_log.py:200-206`). |
| `effective_max_rounds` / fallback | unchanged; a conflict cycle under the INV-R3 clamp is still bounded by it. |

Operator guidance (command doc): a conflicted PR needs one round for the conflict, so `--max-rounds 2` (the default) leaves one review-fix round.

### 5.5 Reviewer re-trigger after a merge push

The merge is authored code and gets the same review path as a fix (J-66). After the push, the existing S5a step runs `pending_retriggers(<events>, cycle_id, <present reviewers>)` (`SKILL.md:274`); at `C-initial` no reviewer has been recorded absent yet, so every configured reviewer is re-triggered (`auggie review`, `@codex review`) and its watermark recorded with `rereview_requested{cycle_id, reviewer, timestamp}`. The S5 snapshot gate (`SKILL.md:88-200`) then waits with `pushed_sha := <merge sha>` and the per-reviewer watermarks, so a review of the pre-merge head is never attributed. A re-triggered reviewer that never responds is recorded absent by the existing rule (`SKILL.md:173-177`). No new re-trigger code.

### 5.6 Run-log events

The closed enum grows from 41 to 43 (`models.py:22-90`).

| Event | When | Required fields |
|---|---|---|
| `conflict_classified` | Every Wave C run at L1+, after the decision and BEFORE any merge starts (write-ahead) | `cycle_id`, `hook` (`initial` / `ci`), `mergeable`, `merge_state_status`, `commits_behind`, `base_ref`, `base_sha` (null at tier 0 without fetch), `pre_merge_head` (= `pre_push_sha`), `tier`, `tier_cap`, `action`, `entries` (list of `{path, code, class, tier}`) |
| `conflict_resolved` | After each path is staged | `cycle_id`, `path`, `class`, `method` (`regenerate` / `take_side` / `intent`), `record` (Tier 2 only, section 7.3), `verdict` (Tier 2 only, filled after the evidence batch by a second `conflict_resolved` with the same `path`) |

Push triad records gain two optional fields: `push_kind` (`"fix"` default, or `"merge"`) and `base_sha` (merge only). The idempotency key format `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` is unchanged (`fsm.py:227-235`); a conflict cycle has its own `cycle_id`, so keys never collide. New `terminal_halted` reasons (strings, no enum change): `conflict_needs_human`, `conflict_markers_remain`, `merge_commit_failed`, `merge_range_mismatch`, `operation_in_progress`, `merge_preflight_dirty`, `base_unreachable`.

`rebuild_state` gains one derived, non-idempotency field `conflict` = `{cycle_id, tier, resolved_paths, merge_sha}` from the latest conflict cycle. `IDEMPOTENCY_SETS` stays at 7.

### 5.7 `--resume` crash recovery

Order of checks on resume:

1. The existing crash window (`detect_crash_window`, `recovery.py:57-80`) runs first. A dangling `push_initiated` with `push_kind == "merge"` resolves exactly as today: Branch A writes `push_completed{recovered}` and resumes at S5a or S5 (`recovery.py:112-147`); Branch B re-drives the push without re-merging, and the re-driven push runs the pre-push guard with the record's `pre_push_sha` and **`merge_parent_ok` with the record's `base_sha`**; Branch C halts. `resolve_crash_window` copies `push_kind` and `base_sha` into its recovery events (extend the key tuple at `recovery.py:98-110`).
2. Otherwise, when the last conflict cycle has a `conflict_classified` but no `push_completed` and no terminal, call `conflict_resume_point(events, merge_head=<git rev-parse -q --verify MERGE_HEAD or None>, head_sha=<HEAD>, head_parents=<parents of HEAD>)`:

| Observed | Resume point | Action |
|---|---|---|
| `MERGE_HEAD` == record `base_sha`, HEAD == `pre_merge_head` | `continue_resolution` | Re-derive unmerged paths from `git ls-files -u -z`; skip paths with a `conflict_resolved` that are still staged; continue the tier procedure in the same `cycle_id`. |
| no `MERGE_HEAD`, HEAD == `pre_merge_head` | `restart` | The merge never started or the operator aborted it: rerun Wave C from step 1 in the same `cycle_id`. |
| no `MERGE_HEAD`, HEAD parents == `[pre_merge_head, base_sha]` | `push_merge_commit` | The commit exists and no push was initiated: run the pre-push guard and the push. |
| `MERGE_HEAD` present and != record `base_sha` | `foreign_operation` | HALT, reason `operation_in_progress` (J-16, J-17). |
| anything else | `head_moved` | HALT, reason `pr_head_mismatch` with the existing message. |

The head-binding repeat on `--resume` (`SKILL.md:268`) stays as is. In `continue_resolution` local HEAD still equals the PR head, so the full `pr_head_ok` passes. In `push_merge_commit` local HEAD is already the merge commit, so only the branch is checked (`pr_branch_ok`) and `pre_push_sha` is taken from the record's `pre_merge_head`, exactly like the dangling-push case.

## 6. Publishing without a force-push

### 6.1 Preflight (before `git merge`, L2 and L3 only)

All checks are read-only; any failure HALTs with nothing changed.

| Check | Command | Failure |
|---|---|---|
| No other operation in progress | `git rev-parse -q --verify MERGE_HEAD`; `git rev-parse --git-path rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `sequencer` tested for existence (worktree-aware, J-16) | `operation_in_progress`: "finish or abort your <operation> first" (J-17) |
| Tracked tree clean | `git status --porcelain=v1 -z --untracked-files=all`: any entry other than `??` | `merge_preflight_dirty`: "commit your changes or set them aside yourself; this skill never stashes" (J-18, J-20) |
| Untracked files recorded | the `??` entries become `OPERATOR_PENDING` for the cycle (same capture as `SKILL.md:272`) | (not a failure) |
| On the bound branch, not detached, not the base | `git branch --show-current` == `HEAD_BRANCH` != `<base>` | `pr_head_mismatch` (existing message) or `operation_in_progress` for a detached HEAD (J-15, J-26) |

The skill works in the current worktree only and never checks out another branch (J-05, J-06, J-91).

### 6.2 Start the merge

```text
git -c merge.conflictStyle=zdiff3 merge --no-ff --no-commit <base_sha>
```

The merge names the recorded `base_sha`, never the moving ref, so the base cannot change between classification and resolution. Exit 0 with no unmerged paths (the probe and the real merge disagree) is treated as a classification error: `git merge --abort` (safe: the tree was clean and the merge is ours), HALT `conflict_needs_human`. If git refuses to start because an untracked file would be overwritten, HALT `merge_preflight_dirty` with git's message verbatim.

### 6.3 Staging and prohibited commands

- Stage each resolved path the moment it is finished, by exact path: `git add -- <path>` or `git rm -- <path>` (J-56). Never `git add -A`, `git add .`, `git commit -a`.
- Never stage a path in `OPERATOR_PENDING`; never stage a `.claude/` path other than `.claude/settings.json`, and `.claude/settings.json` is Tier 3 anyway.
- Per-path side choice uses `git checkout --ours -- <path>` / `--theirs -- <path>`. The blanket forms on `.` are forbidden (R-13, R-14).
- Forbidden anywhere in Wave C: stashing (J-20), `git reset --hard` (R-15), `git clean`, `--amend` (J-63), skipping commit hooks (J-60), any force form of `git push`.

### 6.4 VAL for a conflict cycle

The existing VAL list runs unchanged (`SKILL.md:279-291`), with these inputs:

- VG-1 `<changed-area>` is the set of resolved paths. When no resolved path maps to a test area (for example a lockfile-only merge), VG-1 escalates to VG-2 and the VG-2 run counts as VG-1, so `run_validation_gates` still sees VG-1 present (`fsm.py:441-474`).
- VG-2 (`make test`) is **mandatory at Tier 2**: a textually clean merge can still be semantically broken (R-180), and CI cannot have run on the conflicted head.
- VG-3, VG-4 and VG-5 unchanged; VG-4 checks the whole tree, so a base commit that is itself unformatted fails the cycle. That is reported, not fixed: the resolution must not change unrelated code (R-169, R-161 caveat).
- Before VAL: `git diff --name-only --diff-filter=U` must be empty and `conflict_marker_lines` must be empty for every resolved path, else HALT `conflict_markers_remain` (R-11).
- A VAL retry does not tick `round_counter` (unchanged). A VAL retry for a conflict cycle may re-edit only resolved paths.

### 6.5 The merge commit (the cycle's one commit)

```text
git commit -F <output-dir>/conflicts/<cycle_id>/merge-msg.txt
```

- Not `git commit --only -- <paths>`: git refuses a partial commit during a merge. Exact-path safety comes from 6.1 (the tracked tree was clean, so the index holds only the merge result) plus 6.3 (only resolved paths were staged by the skill). Immediately before committing, require `git diff --cached --name-only -z` to share no path with `OPERATOR_PENDING`.
- The message is rendered by `merge_commit_message(...)` (section 7.4): subject `Merge <base_ref> (<base_sha7>) into <HEAD_BRANCH>`, one line per resolved path with its class and, for Tier 2, the kept and dropped behaviour (S-29), so reviewers read the resolution in the PR without a new comment write path.
- Never skip hooks. A failed commit or a HEAD that did not advance: append `terminal_halted` (reason `merge_commit_failed`), report the hook output verbatim (J-61), leave the merge in progress, never amend (J-63). Message: "The merge commit failed (<error>). Nothing was pushed. Your checkout is mid-merge with every conflict resolved and staged. Fix the cause and run `git commit --no-edit`, or discard with `git merge --abort`, then re-run with `--pr <N>`."
- `target_sha := git rev-parse HEAD`.

### 6.6 Pre-push guard for a merge push

The order is the existing order with one added step and one swapped check:

1. **Head check (unchanged):** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository`; require `pr_head_ok(<local branch>, pre_push_sha, ...)` and `headRefName == HEAD_BRANCH`. Failure: `pr_head_mismatch`, existing message, plus "This cycle's merge is in local commit <target_sha>: drop it, or re-run so the conflict gate merges the base into the new head."
2. **Base check (new):** `git fetch origin <base>`; `git merge-base --is-ancestor <base_sha> origin/<base>` must exit 0. Exit 1 (the base was rewritten) or any other exit: `base_unreachable`, nothing pushed.
3. **Parent check (swapped by push kind):** `git rev-list --parents -n 1 <target_sha>` minus the first id; require `merge_parent_ok(<parents>, pre_push_sha, base_sha)`. Failure: `merge_range_mismatch`, nothing pushed, no push record.
4. **`push_decision` (unchanged):** `evaluate_push_decision(...)` with `applied_edits = <resolved path count>`; the triad is written with `push_kind: "merge"`, `base_sha`.
5. **Push (unchanged command):** `git push origin <target_sha>:<HEAD_BRANCH>`, then `pre_push_sha := target_sha`.

Why `merge_parent_ok` is the exact rule. A fast-forward push of `target_sha` publishes `target_sha` and every ancestor not yet on the PR branch. With parents exactly `[pre_push_sha, base_sha]`:

- the first parent is the PR head the guard just confirmed, so no unreviewed local commit rides along on the PR side (the same property `push_parent_ok` gives);
- every other new ancestor is reachable from `base_sha`, and step 2 proved `base_sha` is on the remote base branch, so those commits are already public and reviewed on the base;
- the order matters: first parent = PR head keeps `git log --first-parent <HEAD_BRANCH>` the PR's own history, and a swapped order is rejected;
- `pre_push_sha == base_sha` is rejected (a degenerate merge), as are one parent, three or more parents, short, empty, `"null"` or non-hex ids, and stray whitespace; ids compare case-insensitively, mirroring `push_parent_ok` (`fsm.py:582-600`).

`push_parent_ok` keeps its two-parent rejection and its test (`test_pre_pr_checks.py:216-222`). The guard chooses the check by the push kind the cycle declared before committing; a fix cycle can never reach `merge_parent_ok`.

### 6.7 After the push

- S6 / RESOLVING with zero threads; S5a re-trigger (section 5.5).
- Re-read `mergeable` (UNKNOWN re-read rule as 5.2). `MERGEABLE`: exit criterion met. `CONFLICTING` again (the base moved between fetch and push): report it; no immediate second cycle; `C-ci` handles it within the remaining budget.

### 6.8 Rule text changes the pins allow

| Pinned text | Change | Pin still satisfied |
|---|---|---|
| Command Will Not: "push any commit besides the cycle's one fix commit" (`test_static_grep.py:754-755`) | append " or the conflict cycle's one merge commit of the fetched base" | yes, substring kept |
| `state-machine.md` "the commit to push must have exactly one parent, that same SHA" (`test_static_grep.py:749`) | keep; add one sentence: "A conflict cycle's merge commit instead has exactly two parents: that same SHA first, then the recorded base SHA, which must still be on the remote base branch." (no "git" token, T-N50) | yes |
| Wave 6 fix-commit, guard and parent-check wording and order (`test_static_grep.py:664-745`) | unchanged; the merge path is written in the Wave C bullet and refers to "the Wave 6 pre-push head guard, with `merge_parent_ok` in place of `push_parent_ok`" | yes |
| SKILL Will Not "Force-push (`--force`, `--force-with-lease`, or a `+` refspec)" (`test_static_grep.py:761`) | unchanged | yes |

## 7. Core API (`superclaude.pr_submit.conflicts`)

Pure module: no I/O, no `anthropic` import (T-N41), no `gh` / `git` token anywhere including docstrings (T-N50), standard library only. Every function fails closed on malformed input. Public names are re-exported from `superclaude/pr_submit/__init__.py` next to the existing groups (`__init__.py:63-108`).

### 7.1 Data

```python
TIER_NONE, TIER_MECHANICAL, TIER_INTENT, TIER_HUMAN = 0, 1, 2, 3
MAX_INTENT_FILES = 10
SUBMODULE_MODE, SYMLINK_MODE = "160000", "120000"

class ConflictClass(str, Enum):
    UNREADABLE, SUBMODULE, SYMLINK, HUMAN_PATH, BINARY = ...
    LOCKFILE, GENERATED, WHITESPACE_ONLY = ...
    MODIFY_DELETE, ADD_ADD, RENAME_SIDE, TEXT = ...

@dataclass(frozen=True)
class StageEntry:        # one "<mode> <oid> <stage>\t<path>" record
    mode: str; oid: str; stage: int; path: str

@dataclass(frozen=True)
class ConflictEntry:
    path: str
    stages: dict[int, tuple[str, str]]       # stage -> (mode, oid)
    is_binary: bool | None = None
    whitespace_only: bool | None = None
    readable: bool = True

@dataclass(frozen=True)
class MechanicalRule:    # the extension point (AD-10)
    pattern: str                      # fnmatch on the repo-relative path
    kind: str                         # "lockfile" | "generated"
    sources: tuple[str, ...]          # paths the output is derived from; empty -> tier 3
    regenerate: tuple[str, ...]       # argv, e.g. ("uv", "lock")
    check: tuple[str, ...] = ()       # argv, e.g. ("uv", "lock", "--check")

MECHANICAL_RULES: tuple[MechanicalRule, ...] = (
    MechanicalRule("uv.lock", "lockfile", ("pyproject.toml",), ("uv", "lock"), ("uv", "lock", "--check")),
)
HUMAN_PATH_PATTERNS: tuple[str, ...] = (
    "*/migrations/*", "migrations/*", "*/alembic/versions/*", ".claude/settings.json", ".github/workflows/*",
)
```

A rule's `regenerate` and `check` argv must start with a program the skill's `allowed-tools` already permits (`uv`, `make`; `SKILL.md:4`). Adding a rule for another tool needs an `allowed-tools` change in the same PR (section 12, R-6).

### 7.2 Functions

| Function | Contract |
|---|---|
| `mergeability(mergeable, merge_state_status) -> str` | `"clean"` (`MERGEABLE` and status not `BEHIND`), `"behind"` (`MERGEABLE` and `BEHIND`), `"conflicting"` (`CONFLICTING` or status `DIRTY`), else `"unknown"`. Case-sensitive on GitHub's enum values; anything unexpected is `"unknown"`. |
| `parse_stage_records(text, *, nul=True) -> list[StageEntry]` | Parses NUL- (or newline-) separated stage records. Raises `ValueError` on a bad mode (not 6 octal digits), a non-40-hex oid, a stage outside 1..3, an empty path, or a duplicate `(path, stage)`. Shared by the merge-tree probe and the in-progress index listing. |
| `group_entries(records) -> list[ConflictEntry]` | Groups by path, sorted by path. |
| `tree_code(entry) -> str` | Section 4.2 table; raises `ValueError` on an invalid stage set. |
| `classify_entry(entry, *, rules=MECHANICAL_RULES, human_paths=HUMAN_PATH_PATTERNS) -> tuple[ConflictClass, int]` | Section 4.3 table, first match wins. |
| `classify_run(entries, *, rules=..., human_paths=..., max_intent_files=MAX_INTENT_FILES) -> dict` | Returns `{"tier", "entries": [{path, code, class, tier}], "order": [paths in resolution order], "reason"}`. Applies the run-level rules (generated dependency, size bound). `order` puts mechanical sources before their outputs and Tier 1 before Tier 2. An empty entry list is tier 0. |
| `conflict_action(*, ordinal, tier, tier_cap, round_counter, max_rounds, fsm_terminal) -> str` | Evaluated in this order: ordinal 0 -> `"skip"`; tier 0 -> `"none"`; cap 0 -> `"report"`; `fsm_terminal` -> `"report"`; tier 3 or tier > cap -> `"halt_human"`; `round_counter >= max_rounds` -> `"halt_rounds"` (delegates to `loop_guard.should_halt`); ordinal 1 -> `"propose"`; 2 -> `"resolve_local"`; 3 -> `"resolve_push"`. Any out-of-range input -> `"halt_human"`. One function is the single routing table for Wave C (section 5.3). |
| `merge_parent_ok(parents, pre_push_sha, base_sha) -> bool` | True iff `parents` is a list of exactly two 40-hex strings, `parents[0] == pre_push_sha`, `parents[1] == base_sha` (case-insensitive), and `pre_push_sha != base_sha`. No stripping. |
| `conflict_marker_lines(resolved, *, sides=()) -> list[int]` | 1-based line numbers of conflict marker lines in `resolved`: a line starting with 7 of `<`, `>` or `|` followed by a space or end of line, and a line of exactly 7 `=` only when it sits between an opening and a closing marker. A marker line that also appears verbatim in any of `sides` (base, ours, theirs content) is inherited, not introduced, and is ignored, so a file that legitimately documents markers is not a false positive. |
| `resolution_record_errors(record) -> list[str]` | Section 7.3; empty list means valid. |
| `render_resolution_summary(records) -> str` | Deterministic markdown for the final report and the commit body. |
| `merge_commit_message(*, base_ref, base_sha, head_branch, resolved, trailers=()) -> str` | Subject plus one line per resolved path (`resolved` = the `conflict_resolved` payloads in staging order), then a blank line and `trailers` (for an attribution line the host requires). Deterministic for equal input. |
| `conflict_resume_point(events, *, merge_head, head_sha, head_parents) -> str` | Section 5.7 table: `"none"`, `"continue_resolution"`, `"restart"`, `"push_merge_commit"`, `"foreign_operation"`, `"head_moved"`. Reads only `conflict_classified`, `conflict_resolved`, `push_*` and `terminal_*` events. |

### 7.3 Tier 2 resolution record

```text
{
  "path": "src/pkg/mod.py",
  "class": "TEXT",
  "ours_intent":   "<one sentence: what the PR side changed and why>",
  "theirs_intent": "<one sentence: what the base side changed and why>",
  "after":         "<one sentence: the behaviour after the merge>",
  "dropped":       ["<one sentence per dropped behaviour>"]   // [] when nothing was dropped
  "evidence":      ["conflicts/<cycle_id>/<n>.ours:12-18", "conflicts/<cycle_id>/<n>.theirs:12-15", "<sha7> <subject>"]
}
```

`resolution_record_errors` rejects: a missing key; a non-string sentence; an empty sentence; a sentence containing a newline or longer than 280 characters; `dropped` not a list (an omitted list is an error, so "nothing dropped" is always explicit); fewer than one evidence citation per side; a `path` or `class` that does not match the `conflict_classified` entry. It does not judge truth; `evidence-validator` does that by re-reading the cited artifact lines.

### 7.4 Changes to existing core modules

| File | Change |
|---|---|
| `models.py` | `EventType` + `CONFLICT_CLASSIFIED`, `CONFLICT_RESOLVED` (41 -> 43); docstring count updated (`models.py:3-7`, `:23`). |
| `fsm.py` | one `transition()` edge (section 5.4); `build_push_triad(..., push_kind="fix", base_sha=None)` adds both fields to `common` only when `push_kind == "merge"`, so every existing fix-push record is byte-identical; `SkillArgs.conflict_max_tier` + `--conflict-max-tier` (choices 0, 1, 2; default 2) in `build_arg_parser` / `parse_args` (`fsm.py:73-134`); `needs_rebase` docstring says "is behind; reported, never rebased". No other change, and no `git` token is introduced (T-N50). |
| `run_log.py` | `rebuild_state` derives `conflict` (section 5.6); docstring of `append` says 43. `IDEMPOTENCY_SETS` unchanged. |
| `recovery.py` | add `"push_kind"`, `"base_sha"` to the copied keys (`recovery.py:98-110`). |
| `__init__.py` | re-export the `conflicts` public names. |

## 8. Functional requirements

Priority: MUST unless marked SHOULD. "AC" = acceptance criterion; each names the test that proves it (section 10).

**FR-C1 Mergeability read.** At L1+, Wave C reads `mergeable`, `mergeStateStatus`, `headRefOid` and `baseRefName` with one repo-pinned `gh pr view`, re-reading `UNKNOWN` at most 3 times 10 s apart.
- AC: `mergeability()` maps every GitHub value in section 7.2 and maps unexpected values to `"unknown"` (`test_conflicts.py::test_mergeability_*`). The SKILL text contains `--json mergeable,mergeStateStatus,headRefOid,baseRefName` with `--repo "$REPO"` (`test_static_grep.py::test_conflict_gate_wording`).

**FR-C2 Tier 0 fast path.** `"clean"` or `"behind"` ends Wave C after one read with `conflict_classified{tier: 0}` and a report line; no fetch, no probe.
- AC: `conflict_action(tier=0, ...) == "none"` at every ordinal 1..3 and cap; SKILL text states the fast path.

**FR-C3 Local probe.** For `"conflicting"` or persistent `"unknown"`: fetch the base, record `base_sha`, run `git merge-tree --write-tree -z <pre_push_sha> <base_sha>`; exit 0 is tier 0; exit 1 is classified; any other exit HALTs `conflict_needs_human`. The probe never changes the working tree or index.
- AC: `parse_stage_records` accepts the recorded probe fixture (`tests/pr_submit/fixtures/merge_tree_conflict.z`, captured from a real two-branch repo) and rejects each malformed shape. Static test: the probe command appears in `refs/conflict-mechanical.md` before the first `git merge` command.

**FR-C4 Preflight.** Before a merge (L2, L3): no foreign operation, clean tracked tree, untracked files captured as `OPERATOR_PENDING`, bound branch not detached and not the base (section 6.1).
- AC: static test pins the four checks and the reasons `operation_in_progress`, `merge_preflight_dirty`; the refs and SKILL contain no stash command (`test_static_grep.py::test_conflict_forbidden_commands`).

**FR-C5 Classification.** Each path is classified by section 4.3 and the run tier by section 4.3 run-level rules, entirely in the core.
- AC: one parametrized row per class and tier; run-level rows for max tier, generated dependency (source Tier 3, empty sources), size bound (10 vs 11 Tier 2 paths) and resolution order (`test_conflicts.py::test_classify_*`).

**FR-C6 Routing.** `conflict_action` is the only Wave C routing decision and implements section 5.3.
- AC: an exhaustive table test over ordinal 0..3 x tier 0..3 x cap 0..2 x budget {spent, open} x `fsm_terminal` {True, False} asserts the section 7.2 order (`test_conflicts.py::test_conflict_action_table`).

**FR-C7 FSM edge.** `(S2_CLASSIFY, "conflicting")` routes like `findings`: round gate, then G-edit; `needs_human_decision` wins.
- AC: `transition` returns `HALT_MAX_ROUNDS` with the budget spent, `PROPOSED` at L1, `S3_FIXING` at L2 and L3, `HALT_HUMAN` with `needs_human_decision` at every ordinal (`test_autonomy_gates.py::test_conflicting_edge_*`). `state-machine.md` gains a "5.2d Conflict cycle" section and still has no `git` / `gh` token.

**FR-C8 Tier 1 procedure.** Lockfile and generated paths regenerate from resolved sources with the rule's command and pass the rule's check; whitespace-only paths take a side per section 4.4.
- AC: static test pins `uv lock`, `uv lock --check`, "resolve the sources first", and the per-path `git checkout --ours -- <path>` form in `refs/conflict-mechanical.md`; `classify_run` orders `pyproject.toml` before `uv.lock`.

**FR-C9 Tier 2 procedure.** Per path: write the three stage blobs to `<output-dir>/conflicts/<cycle_id>/`, collect the R-112 evidence, write a record valid under `resolution_record_errors`, apply by category, stage, append `conflict_resolved`. A sentence that cannot be written escalates the path to Tier 3.
- AC: `resolution_record_errors` rows for every rejection in section 7.3; static test pins `git show :1:`, `:2:`, `:3:`, `--left-right --merge`, "one sentence", "never write behaviour neither side wrote", and "dropped" in `refs/conflict-intent.md`.

**FR-C10 Independent evidence check.** After all Tier 2 paths are staged, one `evidence-validator` batch re-reads each record's cited artifact lines; `unsupported` escalates that path to Tier 3.
- AC: static test pins the dispatch sentence and the escalation in `refs/conflict-intent.md`; `conflict_resolved` with `verdict` is accepted by `RunLog.append`.

**FR-C11 Tier 3 halt.** Tier 3 (classified, escalated, or above a nonzero cap) appends `terminal_halted{reason: "conflict_needs_human"}`, passes `needs_human_decision`, ends in `HALT_HUMAN`, pushes nothing, and prints the section 4.4 message.
- AC: static test pins the message lines verbatim in SKILL.md; `conflict_action` returns `"halt_human"` for every Tier 3 row.

**FR-C12 Marker gate.** Before VAL and before commit, no unmerged path remains and `conflict_marker_lines` is empty for every resolved path; else HALT `conflict_markers_remain`.
- AC: marker rows: real markers flagged; a setext `=======` outside a marker block not flagged; a marker line inherited from a side not flagged; markers built in tests by string multiplication so the test file itself is clean.

**FR-C13 VAL inputs.** Section 6.4: VG-1 on resolved paths with escalation to VG-2 when no area maps; VG-2 mandatory at Tier 2; VG-3, VG-4, VG-5 unchanged.
- AC: static test pins "VG-2 (`make test`) is mandatory at Tier 2" in the Wave C bullet; `run_validation_gates` behaviour is unchanged (existing tests).

**FR-C14 Merge commit.** One commit per conflict cycle via `git commit -F <msg file>`, never `--only`, never skipping hooks, never amending; message from `merge_commit_message`; failure HALTs `merge_commit_failed` with the merge left in progress.
- AC: `merge_commit_message` golden test; static test pins the commit command, the halt reason and message, and the absence of the hook-skip flag and `--amend` in the refs.

**FR-C15 Merge-parent rule.** `merge_parent_ok` exactly as section 6.6; `push_parent_ok` unchanged.
- AC: parametrized rows: correct pair; upper-case ids; swapped order; one parent; three parents; empty; `None`; string; null entry; short id; 41-char id; non-hex; trailing newline; leading space; `pre_push_sha == base_sha`. The existing `merge` row of `test_push_parent_ok_fails_closed_on_parent_shape` (`test_pre_pr_checks.py:216-222`) still passes unchanged.

**FR-C16 Merge pre-push guard.** Head check, base reachability, `merge_parent_ok`, then `push_decision`, in that order (section 6.6); a guard failure writes no push record.
- AC: static test asserts the index order of `pr_head_ok(`, `merge-base --is-ancestor`, `merge_parent_ok(` and "The deterministic core DECIDES" inside the Wave C bullet; reasons `merge_range_mismatch`, `base_unreachable` present.

**FR-C17 Push records.** Merge pushes carry `push_kind: "merge"` and `base_sha`; fix pushes are byte-identical to today.
- AC: `build_push_triad` default call output equals a recorded pre-change fixture; merge call adds exactly the two fields to all three records; idempotency key unchanged.

**FR-C18 Re-review.** After a merge push, S5a re-triggers per `pending_retriggers`; the S5 wait attributes only reviews of the merge SHA newer than each watermark; the attributed re-review ticks `round_counter` once.
- AC: `run_skill` drive with an injected `conflicting` outcome at L3 ends with `round_counter == 1`, `push_count == 1`, `rereview_request_count == 1` before the first findings cycle (`test_autonomy_gates.py::test_conflict_cycle_consumes_one_round`).

**FR-C19 Resume.** Section 5.7, with the crash window first and `conflict_resume_point` second.
- AC: one row per resume point; a `recovery.py` Branch B test on a `push_kind: "merge"` record keeps `push_kind` and `base_sha` in the `push_aborted_or_not_landed` event (`test_crash_recovery.py::test_merge_push_branch_b_keeps_kind`).

**FR-C20 Create-path contradiction removed.** Wave 0 never rebases; behind-base is reported; the STOP block and Error Handling row drop the create-path behind-base HALT; the head-binding message drops the "a branch Wave 0 rebased" clause.
- AC: `test_static_grep.py:654-661` is rewritten to assert "Wave 0 never rebases" and the absence of "rebase if behind"; `test_edge_cases.py:262-267` still passes (its "Wrong origin" alternative remains).

**FR-C21 Output contract.** The result gains `conflict: {tier, status, files, merge_sha}` with `status` in `none | reported | proposed | resolved_local | pushed | halted`; the `status` enum is unchanged.
- AC: static test pins the row in the Output Contract table.

**FR-C22 (SHOULD) Tier cap flag.** `--conflict-max-tier {0,1,2}`, default 2, parsed into `SkillArgs.conflict_max_tier`, documented in the command options table and `argument-hint`.
- AC: `test_skill_parse.py` rows: default 2; 0, 1, 2 accepted; 3 and -1 rejected by argparse choices.

**FR-C23 Wave 8 integration.** `C-ci` runs before `should_arm_ci_wait`; on a conflicted PR with an open budget at L3 from `S2_CLASSIFY`, it runs a conflict cycle and re-enters Wave 8 after the attributed re-review. With the budget spent from `S2_CLASSIFY`, `conflict_action` returns `"halt_rounds"` and the edge ends in `HALT_MAX_ROUNDS` (work remains, so `terminal_clean` would be false). From a preserved terminal it reports; at L1 it proposes and at L2 it resolves locally and halts before push, as in section 5.3. In every case that does not push a merge the CI wait is skipped with reason `pr_conflicting`.
- AC: static test pins the `C-ci` sentence in the Wave 8 bullet and "skip the CI wait" wording.

## 9. Non-functional requirements

**NFR-1 Cost grows with tier.** Tier 0 costs one API read and loads no ref. Tier 1 loads only `conflict-mechanical.md`. Only Tier 2 loads `conflict-intent.md`, dispatches an agent, and forces `make test`. Tier 3 costs at most the probe. AC: the Wave table row and the Wave C bullet state the load conditions; a static test checks that `conflict-intent.md` is named only in the Tier 2 sentence.

**NFR-2 Core purity.** `conflicts.py` joins `CORE_PURE_FILES` (`test_static_grep.py:37-51`); the new `state-machine.md` section adds no `git` / `gh` token. The two new refs carry git commands and are excluded from that set, like `thread-reply.md`.

**NFR-3 No new dependency, no global config.** Standard library only in the core; only `-c` per-invocation config in commands; no `mergiraf`, no `rerere`.

**NFR-4 Repo pin.** Every `gh` command in the new refs, inside fenced blocks, carries `--repo` (the existing `_repo_scoped` fork-pin checks, `test_static_grep.py:103-129`).

**NFR-5 Installed-path rule.** The new refs and SKILL text refer to other primitives only by installed path (`~/.claude/agents/evidence-validator.md` with the project `.claude/agents/` copy first, per CLAUDE.md dual-surface rule); `grep -rn 'src/superclaude' src/superclaude/skills/sc-pr-submit-protocol` returns no new hit.

**NFR-6 Pins preserved.** SKILL.md keeps exactly one python fenced block (`test_cosmos_protocol.py:35`, `test_codex_reviews.py:687`); new SKILL procedure text uses `text` fences. L0 AC-1 sentence unchanged (`test_static_grep.py:650-653`).

**NFR-7 Determinism.** Every core function is a pure function of its arguments; `classify_run`, `render_resolution_summary` and `merge_commit_message` are stable under input order (sorted by path).

**NFR-8 Bounded attended time.** Wave C adds at most: 30 s of UNKNOWN re-reads, one fetch, one probe, `MAX_INTENT_FILES` Tier 2 paths, one evidence batch, one VAL run plus the existing one retry.

**NFR-9 Redaction.** Records and artifacts pass through the existing run-log redaction (`run_log.py:39-71`); stage blob artifacts are written only under `--output-dir`, never staged.

**NFR-10 Lint, format, sync.** `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync` green; `make sync-dev` run after editing the skill.

## 10. Test plan

No test touches the network or a live remote (seed brief Q8). Git behaviour that the core depends on is pinned by a captured fixture, not by running git in the suite.

### 10.1 New tests

| File | Covers |
|---|---|
| `tests/pr_submit/test_conflicts.py` (new) | `mergeability` (all values, unexpected -> unknown); `parse_stage_records` (NUL and newline forms, each malformed shape, duplicate stage); `tree_code` (6 valid sets, invalid sets raise); `classify_entry` (one row per class, first-match order, `None` facts fail closed); `classify_run` (max tier, generated dependency, empty sources, size bound 10/11, resolution order); `conflict_action` (exhaustive table, FR-C6); `merge_parent_ok` (FR-C15 rows); `conflict_marker_lines` (FR-C12 rows); `resolution_record_errors` (section 7.3 rows); `merge_commit_message` and `render_resolution_summary` (golden strings, input-order stability); `conflict_resume_point` (section 5.7 rows); every `MECHANICAL_RULES` program appears in the SKILL.md `allowed-tools` front matter (risk R-6). |
| `tests/pr_submit/fixtures/merge_tree_conflict.z` (new fixture) | NUL-separated probe output with a `UU`, a `DU` and an `AA` path, captured once from a scratch repo; the capture recipe is a comment in `test_conflicts.py`. |

### 10.2 Changed tests (pinned counts and static greps)

| File and line | Today | Change |
|---|---|---|
| `tests/pr_submit/test_run_log.py:168` | `len(EventType) == 41` | `== 43` |
| `tests/pr_submit/test_codex_reviews.py:441` | `len(EventType) == 41` | `== 43` |
| `tests/pr_submit/test_idempotency.py:89` | `len(IDEMPOTENCY_SETS) == 7` | unchanged (asserts the design did not add a set) |
| `tests/pr_submit/test_static_grep.py:37-51` | `CORE_PURE_FILES` | add `PR_SUBMIT_PKG / "conflicts.py"` |
| `tests/pr_submit/test_static_grep.py:654-661` | pins "rebase if behind `origin/<base>`", "branch (`origin/<default-branch>`) on the create path", and the create-path Error Handling row | rewrite (FR-C20): assert "Wave 0 never rebases", assert "rebase if behind" is absent, assert the Error Handling row "Wrong origin / wrong-owner URL"; keep the `--pr` "do not rebase" assertion |
| `tests/pr_submit/test_static_grep.py:627-755` (rest) | Wave 6 wording, order, staging recipe, OPERATOR_PENDING, state-machine sentence, command Will Not | unchanged; must still pass (section 6.8) |
| `tests/pr_submit/test_static_grep.py:758-776` | no force form of `git push` in any skill `.md` / `.sh` | unchanged; now also scans the two new refs automatically (`rglob`) |
| `tests/pr_submit/test_static_grep.py` (new tests) | none | `test_conflict_gate_wording` (FR-C1, C11, C16, C21, C23 pins and the guard order); `test_conflict_forbidden_commands` (no `git stash`, no `reset --hard`, no `checkout --ours .` / `--theirs .`, no hook-skip flag, no `--amend`, no `commit -a` anywhere in the skill folder; prose says "never stash" and "never skip commit hooks" without the command tokens); `test_conflict_refs_lazy` (NFR-1) |
| `tests/pr_submit/test_cosmos_protocol.py:33-45`, `tests/pr_submit/test_codex_reviews.py:685-697` | exactly one python block in SKILL.md, executed | unchanged; must still pass (NFR-6) |
| `tests/pr_submit/test_cosmos_protocol.py:209-258` | ref fragment pins for 5 refs | unchanged; optionally add fragments for the two new refs |
| `tests/pr_submit/test_pre_pr_checks.py:64-72` | T-107 `needs_rebase` | assertions unchanged; docstring says "reports behind" |
| `tests/pr_submit/test_pre_pr_checks.py:216-222` | `push_parent_ok` rejects the `merge` shape | unchanged (the narrow-sibling guarantee) |
| `tests/pr_submit/test_autonomy_gates.py` | gate table rows | add the `conflicting` edge rows and `test_conflict_cycle_consumes_one_round` (FR-C7, C18) |
| `tests/pr_submit/test_crash_recovery.py` | Branch A/B/C | add the merge-kind Branch A and Branch B rows (FR-C19) |
| `tests/pr_submit/test_idempotency.py` or `test_run_log.py` | push triad shape | add the byte-identical fix-push fixture and the merge-push field rows (FR-C17) |
| `tests/pr_submit/test_skill_parse.py` | flag parsing | add `--conflict-max-tier` rows (FR-C22) |
| `tests/pr_submit/test_edge_cases.py:262-267` | "Wrong origin" or "behind" or "wrong-owner" | unchanged; passes on "Wrong origin" |
| `tests/unit/test_cli_install.py:248-262` | installed skill file list (presence only, `:496-500`) | add `sc-pr-submit-protocol/refs/conflict-mechanical.md` and `refs/conflict-intent.md` so a later rename is caught |
| `tests/commands/test_impact_command.py:327-345` | `Skill sc:impact-protocol` and `--caller sc-pr-submit-protocol` in SKILL.md and `troubleshoot-dispatch.md` | unchanged |

### 10.3 Manual verification (documented, not automated)

One scratch-repo walkthrough per tier at L3 against a throwaway PR on the fork, recorded in the PR description: a `uv.lock`-only conflict (Tier 1, one merge commit, PR mergeable), a two-sided edit in one function (Tier 2, record and verdict in the run-log), a submodule pointer conflict (Tier 3, nothing pushed, nothing touched). Manual verification is reported as manual, not as a test pass.

## 11. File change inventory

| Path | Change |
|---|---|
| `src/superclaude/pr_submit/conflicts.py` | new (section 7) |
| `src/superclaude/pr_submit/__init__.py` | re-exports |
| `src/superclaude/pr_submit/models.py` | 2 enum members, docstring counts |
| `src/superclaude/pr_submit/fsm.py` | 1 edge, `build_push_triad` kwargs, flag, `needs_rebase` docstring |
| `src/superclaude/pr_submit/run_log.py` | derived `conflict` field, docstring count |
| `src/superclaude/pr_submit/recovery.py` | 2 copied keys |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | Wave table row; Wave 0 rebase removed (AD-7); `C-initial` sentence in Wave 1; Wave C bullet (sequence, ordinal table, guard order, HALT messages); `C-ci` sentence in Wave 8; STOP block and Error Handling rows; Output Contract `conflict` row; Will Not lines (never stash, never skip commit hooks, never blanket side choice) |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` | new: preflight, probe, merge start, Tier 1 rules, marker gate, commit recipe, merge pre-push guard |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md` | new: stage reads, evidence recipe, categories, record schema, evidence-validator batch, escalation |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` | section 5.2d (conflict cycle, abstract wording), one sentence in 5.3 |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md` | one line: a conflict cycle consumes a round on the same edge |
| `src/superclaude/commands/pr-submit.md` | `--conflict-max-tier` row and `argument-hint`; Will Not append (section 6.8); one usage line; round-budget note |
| `tests/...` | section 10 |
| `.claude/...` | regenerated by `make sync-dev`; never staged (CLAUDE.md rule) |

## 12. Risks

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R-1 | A Tier 2 resolution is textually clean but semantically wrong (clean-but-broken integration, R-180). | Medium / High | Mandatory VG-2 at Tier 2; one-sentence intent and explicit `dropped`; independent `evidence-validator`; reviewers re-triggered on the merge SHA; resolution summary in the commit body. Residual risk accepted and stated in the report. |
| R-2 | `git merge-tree --write-tree` is missing (git older than 2.38). | Low / Medium | Probe failure with a usage error is detected; fallback: at L1 report GitHub's state only (tier unknown -> report); at L2/L3 start the merge, classify from `git ls-files -u -z`, and `git merge --abort` on Tier 3 (safe: clean tree, our merge). Pin the fallback in `conflict-mechanical.md`. |
| R-3 | The base moves between fetch and push, so the PR conflicts again after the push. | Medium / Low | The merge names `base_sha`, the guard re-fetches and checks ancestry, post-push re-read reports it, `C-ci` handles it within the round budget. Never a loop: each attempt spends a round. |
| R-4 | A conflict cycle spends a round, so `--max-rounds 2` leaves one review-fix round. | High / Low | Documented in the command; `--max-rounds` up to 5 is available; the alternative (a free extra push) would break `push_count <= max_rounds`. |
| R-5 | On the create path the reviewers may auto-review the pre-merge head before the merge push lands, costing one wasted review. | Medium / Low | S5 attribution ignores reviews of the old head; cost is reviewer quota only. Moving the probe before `gh pr create` is OQ-2. |
| R-6 | A future mechanical rule uses a program not in `allowed-tools` (for example `npm`). | Medium / Medium | Section 7.1 rule: a rule's argv must be permitted by `allowed-tools`; a test asserts every shipped rule's program is in the SKILL front-matter list. |
| R-7 | `HUMAN_PATH_PATTERNS` misses a high-risk path (a migration under a non-standard folder), so it is treated as Tier 2. | Medium / High | Tier 2 still requires intent, VG-2 and review; the pattern tuple is the extension point; add patterns as repos are found. |
| R-8 | Leaving a merge in progress at L2 or on a Tier 3 escalation surprises the operator. | Medium / Low | The HALT message names the state and gives exactly two commands (`git commit --no-edit`, `git merge --abort`); Tier 3 found at probe time touches nothing. |
| R-9 | Test-pin churn: the AD-7 rewrite of `test_static_grep.py:654-661` could hide a regression in the `--pr` no-rebase rule. | Low / Medium | Keep the `--pr` "do not rebase" assertion verbatim; add the "Wave 0 never rebases" positive assertion. |
| R-10 | Pre-commit hooks modify files during the merge commit (formatters), so HEAD does not advance. | Medium / Low | Treated like the fix commit today: `merge_commit_failed`, verbatim output, merge left in progress, never amend, never skip hooks. |
| R-11 | Operator's own pre-PR rebase habit (CLAUDE.md pre-PR check 2) conflicts with "never rebase". | Low / Low | That check applies to an unpublished branch before the first push and is the operator's step, not the skill's; the skill only stops rebasing a published head. |

## 13. Out of scope

- Rebasing, squashing or otherwise rewriting the PR branch; any force-push form.
- Auto-updating a PR that is only behind base (`BEHIND`) with no conflict (OQ-3).
- Semantic conflicts with no textual conflict detection beyond VAL and review (no static analysis of call sites across the merge).
- Submodule, binary, symlink, migration and protected-config resolution (always Tier 3).
- Cherry-pick, revert or rebase operations already in progress (halt only).
- A project-local rule file for `MechanicalRule` / `HUMAN_PATH_PATTERNS` (the parameters exist; the loader does not).
- Mid-run mergeability polling inside the review poll snapshot (OQ-4).
- Cross-repo (fork-hosted) PR heads at L3 (already never pushed, `SKILL.md:268`).
- Any change to L0 behaviour.
- A PR comment summarizing the resolution (the commit body carries it).

## 14. Open questions

| ID | Question | Recommendation |
|---|---|---|
| OQ-1 | Should L1 and L2 continue into the review poll after reporting or resolving a conflict, instead of stopping (AD-2)? | Stop. Findings on a head that must change are stale, and CI cannot run. Revisit if operators ask for L1 review proposals on conflicted PRs. |
| OQ-2 | On the create path, run the read-only probe before `gh pr create` and refuse to open a conflicted PR at L1/L2? | Not in this release: the merge push needs the head binding that only exists after create; a pre-create probe would be report-only and duplicate Wave C. |
| OQ-3 | Should `mergeStateStatus == BEHIND` (branch protection requires an up-to-date branch) trigger a Tier 0 merge-up at L3? | Defer. Same publishing path with zero resolved paths would need `applied_edits` redefined (predicate 5 would block it). Track as a follow-up with its own flag. |
| OQ-4 | Add `mergeable,mergeStateStatus` to the poll snapshot (`poll-augment-review.sh:38`) so a base move is seen during S5 waits? | Defer; two hook points cover the outcomes that matter. |
| OQ-5 | Should `MAX_INTENT_FILES` be operator-tunable? | No flag now; a constant with one test row. Revisit with data from the run-log `conflict_classified` events. |
| OQ-6 | Should the evidence-validator verdict be required for Tier 1 regenerations too? | No: Tier 1 correctness is proven by the rule's check command and VAL, not by stated intent. |
| OQ-7 | Does the host's attribution trailer belong on the merge commit message? | `merge_commit_message(trailers=...)` supports it; the SKILL passes whatever the session's commit convention requires, as for the fix commit. Confirm with the operator. |

## 15. Research traceability

Adopted items (all from the "Items scored above 5" list) and where they land:

| Item | Landed in |
|---|---|
| R-02 | 3.2 (no blanket sweeps, no force-push recovery), 6.3 |
| R-05 | AD-4, 4.3 size bound, 4.4 Tier 3 |
| R-11 | FR-C12, 6.4 |
| R-13, R-14, R-15 | 6.3, `test_conflict_forbidden_commands` |
| R-18, R-156 | 4.4 Tier 2 step 3 and 5, 7.3 |
| R-19, R-20 | `--conflict-max-tier` is the only override and applies per run; recorded in `conflict_classified.tier_cap` |
| R-26 | 4.4 exit criteria (`--diff-filter=U` empty) |
| R-43, R-56 | 4.3 rows 2 |
| R-51 | `conflict_classified` written and reported before any merge (5.2 step 7) |
| R-54, S-53 | 4.3 row 4 |
| R-57 | 4.3 row 5 |
| R-58, R-59 | 4.3 rows 6-7, run-level generated dependency |
| R-84 | 4.3 row 1 |
| R-112 | 4.4 Tier 2 step 2 |
| R-128 | 3.2 (`rerere` rejected) |
| R-146, R-149 | class and tree code in every record and in the HALT message |
| R-150, R-151, R-152, R-153, R-154 | 4.4 Tier 2 step 4 |
| R-161 | 4.3 row 8; 6.4 caveat |
| R-169 | 6.4 (VAL retry re-edits only resolved paths) |
| R-173 | no LLM or network in the core (NFR-2, NFR-3) |
| R-180, R-181 | 4.4 Tier 2 step 2, VG-2 mandatory, R-1 |
| R-189, J-48, S-46 | 4.3 row 6, 7.1 `MECHANICAL_RULES` |
| R-210, R-212 | 4.4 HALT message |
| R-251 | 4.4 Tier 2 step 4 |
| S-05, J-16, J-17 | 6.1 operation check |
| S-09, S-12, S-13, S-14, S-17 | 4.2 stage meaning, 4.4 Tier 2 step 1, zdiff3 in 6.2 |
| S-18 | 4.4 Tier 2 step 4 (additive) |
| S-26, S-29 | 4.4 Tier 2 step 4, 7.3 `dropped`, 6.5 commit body |
| S-38, S-39, S-40 | 4.2 tree codes, 4.3 rows 9-11 |
| J-05, J-06, J-91 | 6.1 current worktree only |
| J-13 | every Wave C HALT ends the run |
| J-15, J-18, J-26 | 6.1 |
| J-20 | 6.1, 6.3 |
| J-39 | 3.2 (no resolver agent) |
| J-40, J-56 | 4.4 one path at a time, 6.3 |
| J-53 | 4.4 Tier 3 escalation, AD-9 |
| J-60, J-61, J-63 | 6.5 |
| J-66 | AD-3, 5.5 |
| J-77, J-83 | fetch or push failure is reported verbatim and HALTs; never retried as a different command |

Not adopted although scored above 5: R-60 (snapshot regeneration needs a per-repo command; covered by the `generated` rule kind when a project adds one), R-101 (read-only candidate recombination: no subsystem for it), J-40's parallel evidence reads are allowed but not required.
