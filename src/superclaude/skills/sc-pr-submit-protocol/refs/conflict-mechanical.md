# Conflict Mechanical (Wave 0, C-initial, Wave 8a) — detection and the merge cycle

This ref sequences merge-conflict detection and the merge cycle (issue #305). The core (`superclaude.pr_submit.conflicts`, plus `fsm`, `ci`, `run_log` and `recovery`) decides; this ref sequences; the SKILL performs every side effect; each script does bounded I/O and prints exactly one stdout line (a JSON object on success, a `<SCRIPT>_FAIL <reason>` token with exit 2 on failure, details on stderr).

> Every `gh` call below pins the RESOLVED repo (`--repo "$REPO"`, origin's `owner/repo` parsed from `git remote get-url origin`) or a `repos/<owner/repo>/` path. A bare `gh` is a defect. Nothing here ever contacts any repository but `origin`.

## 1. When this ref applies

- It loads only when Wave 0, `C-initial` or Wave 8a runs the probe (Tier 1 and up). A Tier 0 run never loads it; L0 never calls the router.
- Terms: "ours" is the PR head in this checkout (stage 2); "theirs" is the recorded base tip `base_sha` (stage 3); stage 1 is the merge base (S-09).
- The core decides the class of each path, the plan tier, the route (`conflict_action`), the gates, the cycle ids, the commit message and the resume plans. Nothing in this ref overrides a core answer.
- Tier 2 steps also need `refs/conflict-intent.md` (Tier 2 only: L3, `--conflict-max-tier 2`, loaded at `C-initial`).

## 2. Detection

One GitHub read per hook. Wave 0 uses the first form; the acting hooks (`C-initial`, Wave 8a) use the second, which also feeds step 1 of the merge cycle:

```bash
gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus
gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository
```

While `mergeable` is `UNKNOWN`, read it again up to 3 times, 10 s apart. Normalise with `mergeability_hint(mergeable, mergeStateStatus)`; a failed read means null hints (`unknown`) and the probe runs (OQ-8). Only when `needs_probe(hint)` is true (`conflicting`, or a persistent `unknown`) does the hook run the probe (at an acting hook, after step 1):

```bash
scripts/probe-merge.sh --repo "$REPO" --base <baseRefName> --program uv
```

- Success is one JSON line with `mode: "full"`, `merge_tree_supported`, `base_ref`, `base_sha`, `head_sha`, `merge_base`, `behind`, `ahead`, `foreign_op`, `merge_head`, `tree_clean`, `status_b64`, `clean`, `merge_tree_b64`, `numstat_ours_b64`, `numstat_theirs_b64`, `programs`, `truncated`. The core validates it with `parse_probe`.
- Exit 2 with `PROBE_FAIL <reason>` (`usage`, `not_a_worktree`, `origin_mismatch`, `bad_base`, `fetch_failed`, `no_merge_base`, `merge_tree_failed`) is a prerequisite failure: report it, never retry it as polling.
- Then `plan := conflict_plan(hint=<hint>, probe=<parsed JSON or None>, probe_failed=<True on exit 2>)`. `merge_tree_supported: false` gives an unclassified plan (`merge_tree_unsupported`); `truncated: true` or any invalid field gives Tier 3 `probe_malformed`.
- Once the probe ran, its result is the truth for action: a `CONFLICTING` hint with a clean probe is reported as `github_disagrees` (K2).
- Route with `conflict_action(hook=<"wave0" | "c_initial" | "wave8a">, plan_tier=plan.tier, ordinal=<monitor ordinal>, entering=<None at wave0 and c_initial; the Wave 8 entering outcome at wave8a>, conflict_max_tier=..., round_counter=..., max_rounds=..., prior_conflict_cycles=prior_conflict_cycles(<state conflict_cycles>, <current cycle_id or None>), github_conflicting=plan.github_conflicting, plan_reason=plan.reason)`. Whether the run halts is decided by the returned `status`, never by the reason string.

## 3. The plan report (FR-4, R-51)

Printed before any edit at every hook that probes:

- the tier (0 to 3, or "unclassified" with the plan reason);
- each conflicted path with its class and reason (for example `uv.lock` `regen:uv.lock`, `app.py` `text:content`, `.github/workflows/ci.yml` `halt:protected`);
- the action this ordinal would take (the `conflict_action` row: action, reason, status);
- at L1 Wave 8a, only after `clean` / `REPORT_ONLY`, the `CONFLICT_PROPOSE_PROMPT` ("resolve these conflicts? y/n"). After a preserved terminal the router reports `tier1_l1_preserved` and no prompt is printed.

At a later hook, print the plan again only when the tier or the path set changed. L0 prints nothing.

## 4. Tier 3 HALT message (FR-10, R-210, R-212, J-13)

Exact template:

> HALT (`<reason>`): merging `origin/<base>`@<base_sha> into `<HEAD_BRANCH>` needs a human decision. File <k>/<n>: `<path>` (`<class>`). [This PR's side appears to <one sentence>; the base side appears to <one sentence>.] Nothing was changed and nothing was pushed. To continue: on `<HEAD_BRANCH>`, merge `origin/<base>` yourself, resolve and commit, push, then re-run with `--pr <N>`.

The bracketed sentences are omitted when classification stopped before reading content (always at Wave 0). Any halt ends the run; nothing later runs.

## 5. The merge cycle

Runs for `resolve_push` (Tier 1 at Wave 8a with push kind `sync`; Tier 2 at `C-initial` with push kind `merge`) and `resolve_local` (Tier 1 at Wave 8a, L2, stops after step 8). L1 never starts it. "Abort" is defined in section 9. The Wave 8 entering outcome (`clean`, `report_only`, `halt_max_rounds` or `no_response`; null at `C-initial`) is the cycle's `review_terminal`: it is the `entering` argument of every `conflict_action` call, it is written into the step 3 write-ahead record and it is passed to `build_push_triad` at step 11, so a resumed cycle has a durable source for it. Escalation is monotone: a cycle can escalate to Tier 3 (halt) at any step and never de-escalates or retries in the same run.

**Step 0 (Tier 2 only).** `transition(S2_CLASSIFY, "conflicting", {monitor_ordinal, round_counter, max_rounds})`. `HALT_MAX_ROUNDS` ends the cycle before anything is touched.

**Step 1. Head check.** This head check uses the acting-hook read of section 2 and the local checkout (the current worktree, J-91):

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
```

Require `pr_head_ok(<local branch>, <local HEAD>, headRefName, headRefOid, isCrossRepository)`, `headRefName == HEAD_BRANCH`, local `HEAD == pre_push_sha` and `HEAD_BRANCH != baseRefName` (J-26). A detached HEAD fails `pr_branch_ok` (J-15). Failure: `sync_head_mismatch`; nothing started.

**Step 2. Fresh probe.** The section 2 probe of this hook (exactly one probe per cycle). Require `foreign_op` null (J-16, J-17) and `merge_preflight_ok(<decoded status_b64>)` returning `(True, [])` (tracked tree clean, untracked files tolerated; J-18). Rebuild `plan := conflict_plan(...)` and route again; only `resolve_push` and `resolve_local` continue. Failure: `sync_foreign_operation`; or `merge_preflight_dirty` naming the files (never stash, J-20); nothing merged.

**Step 3. Write-ahead.** `cycle_id := conflict_cycle_id(plan.tier, len(conflict_cycles) + 1)`, or the reused open cycle id on a resume restart. Append `sync_started{run_id, cycle_id, tier, kind, hook, base_ref, base_sha, pre_push_sha, merge_tree_oid, conflict_max_tier, review_terminal, paths, resumed}` before the merge command. Then `attempt := conflict_attempt(<run-log events>, cycle_id)` (the number of `sync_started` records for this `cycle_id`, counting the one just appended: 1 for a first run, 2 after one restart) and `cycle_dir := <output-dir>/sync/<cycle_id>/a<attempt>/`. Every file of this attempt (evidence, `resolution.md`, message, manifest) goes under `cycle_dir`, so a restart under the same `cycle_id` never meets the files of an earlier attempt; those stay where they are.

**Step 4. Merge by SHA.** Per-invocation config only (no stored config), rerere off (R-128), hooks on:

```bash
git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>
git diff --name-only --diff-filter=U
```

The unmerged set must equal the plan's conflicted path set. Failure: exit 1 without `MERGE_HEAD` (git refused, for example local changes would be overwritten) is `sync_merge_failed` with git's file list and `sync_concluded{halted}`; exit 0, or an unmerged set that differs from the probe, is abort and `sync_merge_failed` (the probe and the merge disagree on the same `base_sha`).

**Step 5. Resolve.** Tier 1, the `uv.lock` rule (R-58, R-189, S-46). First the precheck:

```bash
scripts/finish-merge.sh --base-sha <base_sha> --precheck
```

Then the lock trust gate (PR #378 review): `uv lock` runs build code that the merged `pyproject.toml` can name. Evaluate `lock_trust_findings` on `<toplevel>/pyproject.toml`, the file `uv lock` reads (after the precheck it equals the merge result), with the Python interpreter that passed the CI-wait preflight import, run with `-I` and the file path as its argument: `<python> -I -c 'import json, sys; from superclaude.pr_submit.conflicts import lock_trust_findings; print(json.dumps(lock_trust_findings(open(sys.argv[1], encoding="utf-8").read())))' <toplevel>/pyproject.toml`. `<python>` is the installed package's interpreter, or in a development checkout of this package `uv run --no-sync python`. Between step 4 and this gate's `[]` never use plain `uv run`: it locks and syncs the merged project, which runs the build code this gate keeps out. The call prints one JSON list. Any finding (`build-system.backend-path`, `project.dynamic`, a `[tool.uv.sources]` path or editable entry, or `pyproject.toml unreadable`), or a call that fails or prints anything else: abort (section 9) and halt `sync_tier3`, and `uv lock` never runs. The halt message is the section 4 template with `File 1/1: \`pyproject.toml\` (\`lock_trust\`)` and, in place of the intent sentences, "`uv lock` would run code from this tree: <findings joined by ", ">." `[]`: from the top of the work tree,

```bash
git checkout --ours -- uv.lock
uv lock
uv lock --check
git add -- uv.lock
```

- The precheck prints `{"precheck": "ok"}` (worktree changes only on unmerged paths; it takes no manifest, which is written only at step 9). `FINISH_FAIL tree_dirty`: abort, `merge_preflight_dirty`; any other token maps as in step 9.
- The lock is seeded from the PR side because a lock full of conflict markers is unparseable and a from-scratch resolve could upgrade unrelated pins (OQ-6). Only this one named lock file is ever seeded from one side.
- A `uv` command fails: abort, `sync_merge_failed` (no retry loop).
- Tier 2: follow `refs/conflict-intent.md` (Tier 2 only), one file at a time (J-40), staging each finished path with `git add -- <path>` or `git rm -- <path>` (J-56); then any `regen:*` path by its rule above, after the precheck. A Tier 2 halt condition: abort, `sync_tier3`.

**Step 6 (Tier 2 only). Record and grounding check.** Write `<cycle_dir>resolution.md` as `refs/conflict-intent.md` (Tier 2) describes; `resolution_record_ok(parse_resolution_record(text), plan.text_paths)` must return `[]`. Then the Tier 2 grounding check: spawn `evidence-validator` once (Tier 2 only) over `resolution.md` and the evidence directory; one revision pass. Still unsupported after one revision, or any record problem: abort, `sync_tier3`.

**Step 7. VAL.** Section 6. Red after the retry: abort, `sync_validation_failed`.

**Step 8. L2 stops here** (`resolve_local`): append `sync_concluded{left_in_progress}`, status `halt_before_push`, and print: "The merge of `origin/<base>`@<base_sha> is resolved and validated but not committed. Review it, then run `git commit` yourself and push; or `git merge --abort`."

**Step 9. Finish gate and commit.** Write the message file (`merge_commit_message(base_ref=..., head_branch=HEAD_BRANCH, tier=..., rule_patterns=..., record=<Tier 2 record or None>, lock_changes=...)` plus the session's attribution lines, OQ-13) and the manifest (`finish_manifest(plan.listing, resolved_paths)`: one `<stage-1 oid or ->` tab `<path>` line per resolved path), both under `<cycle_dir>` (step 3). Then:

```bash
scripts/finish-merge.sh --base-sha <base_sha> --merge-tree-oid <merge_tree_oid> --manifest <manifest_file> --message-file <message_file>
```

Success prints `{"merge_sha": "<40hex>", "parents": ["<old HEAD>", "<base-sha>"]}`; set `target_sha := merge_sha`. It commits only through one commit from the message file, with hooks on. After the commit it also checks that the commit records exactly the index tree it validated, so a commit hook that changes and stages content fails `tree_dirty` (step 8). Token to halt reason:

| `FINISH_FAIL` token | Halt reason | State left |
|---|---|---|
| `no_merge_head`, `foreign_merge` | `sync_foreign_operation` | not touched |
| `unmerged` | `sync_unmerged_left` | merge in progress, nothing committed |
| `markers` | `sync_marker_left` | merge in progress, nothing committed |
| `staged_unexpected` | `sync_staged_unexpected` | merge in progress, nothing committed |
| `hook_rejected`, `usage` | `sync_commit_failed` | hook output verbatim (J-61); merge in progress with the resolution intact; no amend (J-63) |
| `tree_dirty` (commit-mode step 3, before the commit) | `merge_preflight_dirty` | merge in progress, nothing committed |
| `tree_dirty` (commit-mode step 8, after the commit: the checkout is not clean, or the commit records a tree other than the validated index, for example a commit hook changed and staged a file) | `merge_preflight_dirty` | the local merge commit is named; nothing pushed |
| `parents_mismatch` | `sync_range_mismatch` | the local merge commit is named; nothing pushed |

Steps 10 to 12 are section 7 (Publish); step 13 is section 8 (After the push).

## 6. VAL for a conflict cycle

- **Trust limit:** conflict resolution and VAL run the project's build and test code on the merged tree (`uv lock`, `uv run pytest`, `make test`, the commit hooks); the step 5 lock trust gate covers only the `pyproject.toml` fields it names. Run sc:pr-submit only on PRs from collaborators you trust with your credentials.
- **Tier 1:** `VG-1` is the rule's check command (`uv lock --check`; the changed area is the lock file, which has no tests), plus `VG-3`, `VG-4`, and `VG-5` only when a resolved path is under a synced component. The report adds the line "no tests ran for the regenerated lock file; CI on the merge head is the test signal".
- **Tier 2:** `VG-1` is targeted tests over the resolved paths (plus the rule check when a `regen:*` path is in the cycle), `VG-2` `make test` is mandatory, plus `VG-3`, `VG-4`, `VG-5` when applicable.

```bash
uv lock --check
uv run pytest <tests covering the resolved paths>
make test
```

- `validation_status := conflict_validation_status(tier, results)` (Tier 2 without a green `VG-2` is `failed`).
- One retry, which must not introduce changes unrelated to the failure (R-169) and does not tick `round_counter`.
- Red after the retry: abort, `sync_validation_failed` (Tier 2: `transition(S7_VALIDATING, "validation_failed")` to `VALIDATION_FAIL`). The message notes that a red base can cause this and names the command that shows the checks of `origin/<base>` (OQ-26):

```bash
gh api "repos/${REPO}/commits/<base_sha>/check-runs" --jq '.check_runs[] | "\(.name) \(.conclusion)"'
```

The impact advisory of VG-1 is not invoked for conflict cycles.

## 7. Publish

Steps 10 to 12. This is the Wave 6 pre-push head guard with three deltas, in this order: head, parent, base ancestry (X-009).

**Step 10(a). Head re-read.** The head re-read compares the stored `pre_push_sha`, never the local HEAD (which is now the merge commit):

```bash
gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository
```

Require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Failure: `sync_head_mismatch`.

**Step 10(b). Parents.** Drop the first id (the commit itself) and require `merge_parent_ok(<parents>, pre_push_sha, base_sha)` in place of `push_parent_ok`. Failure: `sync_range_mismatch`.

```bash
git rev-list --parents -n 1 <target_sha>
```

**Step 10(c). Base ancestry.** The recorded base tip must still be on the base branch. Failure: `sync_base_moved`.

```bash
git fetch origin <base>
git merge-base --is-ancestor <base_sha> origin/<base>
```

Every step 10 failure: nothing pushed, no push record, and the local merge commit is named so the operator can push or drop it. Before the first conflict push of the run, read the repository's merge settings once and print one advisory line (for example: merge commits are not allowed, so a squash or rebase merge of this PR flattens the merge commit); never halt on it (OQ-32):

```bash
gh repo view "$REPO" --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed
```

**Step 11. The deterministic core DECIDES.** `decision := evaluate_sync_decision(monitor_ordinal=..., validation_status=..., tier=..., conflict_max_tier=..., halt_reason=None, prior_conflict_cycles=..., round_counter=..., max_rounds=...)`. Blocked (`decision.authorized` false) means `sync_fail_state(decision)` and nothing is pushed: `predicate_4_under_cap` false is `sync_cap` (s4); `predicate_1_ordinal` or `predicate_2_validated` false is report-only (s1, s2); `predicate_3_tier_allowed` false is `HALT_HUMAN` (s3). Commit-scoped check evidence for the replaced head and the base tip:

```bash
scripts/poll-ci-checks.sh --evidence-sha <pre_push_sha> --repo "$REPO"
scripts/poll-ci-checks.sh --evidence-sha <base_sha> --repo "$REPO"
```

Each prints `{"evidence_sha": "<sha>", "evidence_checks": <n>, "source": "ci"}` with `n = -1` on a failed or unparsable read; an exit 2 passes `None`. Both count as having checks (fail closed). Then `expect_checks := expect_checks_after_push(checks_seen_this_run=..., pre_push_evidence=<n for pre_push_sha>, base_evidence=<n for base_sha>)` and `build_push_triad(..., decision=decision, push_kind=<"sync" or "merge">, base_sha=base_sha, review_terminal=<the cycle's review_terminal, sync only>, expect_checks=expect_checks)`. Append `push_decision`, then `push_initiated` (fsynced before the push), keyed on the unchanged pre-push key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`.

**Step 12. Push.** Origin only, to the PR head branch only, never the default or a protected branch, never forced:

```bash
git push origin <target_sha>:<HEAD_BRANCH>
```

- **Exit 0:** append `push_completed`, then `pre_push_sha := target_sha`. Read the merge state once and print a reason line when it is `BLOCKED`:

```bash
gh pr view <N> --repo "$REPO" --json mergeStateStatus
```

- **Rejected** (non-zero exit whose stderr contains `[rejected]`, `non-fast-forward`, `fetch first` or `hook declined`): append `push_aborted_or_not_landed{rejected: true, stderr_tail}` carrying the triad's `idempotency_key` and the common fields (`run_id`, `cycle_id`, `pre_push_sha`, `target_sha`, `target_branch`, `target_remote`, `kind`, `base_sha`), so `detect_crash_window` treats the key as finalized; then `sync_concluded{halted, reason: push_rejected}` and halt `push_rejected`. A rejected push is never re-driven (INV-035).
- **Failed** (any other non-zero exit: network, auth, a local pre-push hook): no record; the `push_initiated` stays dangling and the cycle stays open (no `sync_concluded`); halt `push_failed` with stderr verbatim (J-77, J-83). For the cycle's first push, `--resume` settles it by the three-way remote check (section 10, row 4b) and closes the cycle. For a Branch B re-drive the key is already finalized, so `--resume` halts `resume_unrepresentable` and closes the cycle without retrying (row 4b').

## 8. After the push

Step 13.

- **Tier 1:** append `sync_concluded{pushed, merge_sha}`; re-enter the Wave 8 CI wait with `wait_sha := target_sha` and the recorded `expect_checks` (`classify_checks(payload, wait_sha=target_sha, expect_checks=expect_checks)`). No `retrigger-review.sh`, no reply, no resolve, no round: the one Tier 1 sync push is not a fix.
- **Tier 2:** append `sync_concluded{pushed, merge_sha}`; `transition(S4_PUSHING, "pushed")`, then S6 and RESOLVING with zero threads; `should_retrigger(0, "merge")` is true, so S5a re-triggers the configured reviewers (see `refs/conflict-intent.md`, Tier 2), and the S5 wait is the run's first review wait.
- **Skip rule:** a PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting` (GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty).
- With `expect_checks` true an empty check list is `polling`; expiry is the existing Wave 8 CI timeout with reason `ci_not_started`, never `clean`, and the report never says tests passed.
- **End of the CI wait:** when any hook this run read `conflicting` (or the run was resumed), read `mergeable` once more before sending `transition(clean)`. `CONFLICTING` means no `transition(clean)`: `terminal_halted`, reason `late_conflict` (late re-sync is #361).

```bash
gh pr view <N> --repo "$REPO" --json mergeable
```

## 9. Where an unfinished merge is left

"Abort" always means: confirm that `MERGE_HEAD` equals `base_sha` (ownership), then abort the merge, then append `sync_concluded{aborted}`. Never abort a merge this run did not start.

```bash
git rev-parse -q --verify MERGE_HEAD
git merge --abort
```

- **Abort** when the resolution is incomplete: Tier 3 found mid-way, validator disagreement, VAL red after the retry, a `uv` failure, a finding of the step 5 lock trust gate. `resolution.md` and the evidence files (Tier 2) are kept in the output dir.
- **Leave the merge in progress** only when the resolution is complete and validated but the run must stop: L2 step 8, and `hook_rejected` at step 9 (OQ-19, J-53). The finish-gate failures `unmerged`, `markers` and `staged_unexpected` also leave it in progress with nothing committed, so the operator can inspect it.

## 10. Resume

On `--resume`, right after the Wave 0 operation check, the core plans and the SKILL acts:

```bash
git rev-parse HEAD
git rev-list --parents -n 1 HEAD
```

`conflict_resume_plan(rebuild_state(), foreign_op=<from the operation check>, merge_head_sha=<its merge_head>, local_head_sha=<HEAD>, local_head_parents=<parents of HEAD>, dangling=detect_crash_window(run_log))`. Rows in table order, first match wins:

| Row | Condition | Directive and action |
|---|---|---|
| 1 | `push_rejected` in the state | `halt`, `push_rejected` (never re-driven); an open cycle is closed |
| 2 | no open conflict cycle, no foreign operation | `none`: the existing head binding and crash-window check follow |
| 3 | no open conflict cycle, a foreign operation (including an L2 `left_in_progress` merge) | `halt`, `foreign_op_in_progress` |
| 3b | the open cycle is superseded by another cycle's `push_initiated` | `halt`, `resume_unrepresentable` |
| 4c | the open cycle's `hook` is missing or unknown, or its `review_terminal` is invalid for that hook | `halt`, `resume_unrepresentable` |
| 4 | the open cycle has a `push_completed` | `complete_after_push`: append `sync_concluded{pushed, recovered: true}`; `sync`: the Wave 8 CI wait at `wait_sha = target_sha` with the recorded `expect_checks` (missing reads as true); `merge`: resume at `S5A_RETRIGGER_REVIEW` (`pending_retriggers` posts only the reviewers still missing) |
| 4b | a `push_initiated` without `push_completed`, and `dangling` is this cycle's record | `crash_window`: `resolve_crash_window_plan` settles it by the three-way remote check and closes the cycle |
| 4b' | the same, but `dangling` is `None` or another cycle's | `halt`, `resume_unrepresentable`; no push is retried; append `sync_concluded{halted, reason: resume_unrepresentable, recovered: true}` once; the message names `cycle_id` and `target_sha` |
| 5 | `MERGE_HEAD` in progress and equal to the open cycle's `base_sha` | `abort_and_restart`: our own interrupted merge; abort it, append `sync_concluded{aborted, recovered: true}`, restart under the same `cycle_id` (`sync_started{resumed: true}`) at the plan's `hook` with `entering := review_terminal`; the restart's step 3 gives it a new attempt directory `<output-dir>/sync/<cycle_id>/a<attempt>/` |
| 6 | any other foreign operation | `halt`, `sync_foreign_operation` |
| 7 | local HEAD equals the open cycle's `pre_push_sha` | `restart`: append `sync_concluded{aborted, recovered: true}` and restart as row 5 |
| 8 | anything else (including a local two-parent merge commit no `push_initiated` covers) | `halt`, `resume_unrepresentable`; the commit is named; it is never published without its finish gate and VAL (OQ-22) |

- A `wave8a` cycle restarts at step 1. A `c_initial` cycle restarts at step 0 with the FSM at `S2_CLASSIFY`; `round_counter` is unchanged.
- At a restart, `prior_conflict_cycles` counts the distinct ids in `conflict_cycles` other than the current `cycle_id`, so a restart never hits `sync_cap` because of its own earlier attempt.
- Every `halt` row that finds an open cycle (1, 3b, 4c, 4b', 6, 8) appends `sync_concluded{halted, reason, recovered: true}` exactly once, before `terminal_halted`, and only while `rebuild_state()["open_conflict_cycle"]` still names that `cycle_id`.

A dangling conflict push settled through row 4b goes through `resolve_crash_window_plan` (the unchanged `resolve_crash_window` first, then `crash_resume_plan(dangling, branch, fsm_state)`), by the record's `kind`:

| `kind` | Branch A (landed) | Branch B (not landed) | Branch C (ambiguous) |
|---|---|---|---|
| `fix`, absent | FSM state as today (S5a or S5) | `S4_PUSHING` (today) | `HALT_HUMAN`, `ambiguous_remote_tip` |
| `merge` | S5a or S5 (S5a re-triggers) | `S4_PUSHING`; the re-driven push runs the head guard with the record's `pre_push_sha` and `merge_parent_ok` | as `fix` |
| `sync` | the Wave 8 CI wait at `target_sha`, `review_terminal` and `expect_checks` from the record | re-drive under the full guard (with `merge_parent_ok`), then the same Wave 8 wait | as `fix` |
| `ci` | as `sync` | re-drive under the full guard (with `push_parent_ok`), then the Wave 8 wait | as `fix` |
| unknown | `halt`, `resume_unrepresentable` | same | same |

- A `sync` or `ci` push never resumes into `S4_PUSHING`, S5a or S5. A missing `review_terminal`, or for `sync` a missing `base_sha`, halts `resume_unrepresentable`.
- Each conflict branch closes the cycle exactly once: Branch A appends `sync_concluded{pushed, recovered: true}`; Branch C appends `sync_concluded{halted, reason: ambiguous_remote_tip, recovered: true}` after its `terminal_halted`; a halt directive appends `sync_concluded{halted, reason: resume_unrepresentable, recovered: true}`; Branch B closes after the re-driven push (exit 0: `pushed`; a guard failure or rejection: `halted`). A re-drive that ends `push_failed`, or a crash during it, appends nothing now; the next `--resume` reaches row 4b'. `--resume` never retries a re-drive.

## 11. Prohibited operations (in words)

Never stash (the stash stack is shared by every worktree), never skip hooks, never amend, never stage everything, never take one side for a whole tree or a whole merge (only the one named lock file is seeded from the PR side), never hard-reset, never check out the base branch or touch another worktree or branch, never write stored git configuration, never replay a recorded resolution, never push anywhere but `origin` and the PR head branch, never push a rewritten history.

## 12. Halt reasons and messages

Every halt is `terminal_halted{reason, ...}`, preceded by `sync_concluded{halted or aborted, reason}` when a cycle had started. Nothing is pushed unless the row says so. No message tells the operator to discard a file holding their own changes, and none suggests stashing.

The `merge_preflight_dirty` message: "Your checkout has uncommitted changes to tracked files: <paths>. Nothing was merged or pushed. Commit or discard those changes yourself (never stash: the stash is shared by every worktree), then re-run with `--pr <N>`."

| Reason | Raised at | Operator message and recovery |
|---|---|---|
| `foreign_op_in_progress` | Wave 0 operation check; resume row 3 | A merge, rebase, cherry-pick, revert or sequencer operation is in progress (named). Nothing was created or pushed. Finish or abort it yourself, then re-run. For a merge left by an earlier L2 run: commit and push it yourself, or abort it, then re-run. |
| `conflict_tier3` | Wave 0 (L3); `C-initial`; Wave 8a from `clean` / `REPORT_ONLY` | The Tier 3 template of section 4. |
| `late_conflict` | Wave 8a Tier 2; end of the CI wait when `mergeable` reads `CONFLICTING` again | PR #N conflicts with `origin/<base>`; a text conflict is resolved only before the first review (`--conflict-max-tier 2`, L3). Nothing was pushed for it. Late re-sync is #361. |
| `tier_above_cap` | Wave 8a | The conflict is Tier t, above `--conflict-max-tier c`. Nothing was pushed. Re-run with a higher cap or resolve it yourself. |
| `github_disagrees` | Wave 8a | GitHub reads conflicting, a local merge of `origin/<base>`@<base_sha> is clean; CI was not waited for. Re-run in a few minutes. |
| `probe_failed`, `merge_tree_unsupported` | Wave 8a (tier unclassified) | Conflict detection could not run (reason); the PR reads conflicting, so CI was not waited for. |
| `sync_cap` | Wave 8a; `sync_fail_state` (s4) | A conflict cycle already ran in this run (at most one). Nothing more was pushed. |
| `merge_preflight_dirty` | step 2; precheck `tree_dirty`; commit-mode `tree_dirty` (step 3 before the commit, step 8 after it) | The message above. Raised after the commit, the local merge commit is named; raised before it, the merge stays in progress with nothing committed. When finish-merge.sh's stderr says `not the validated index tree` (the commit's tree differs from the validated index), the message instead says: "A commit hook changed the local merge commit `<local HEAD>` after the finish gate checked it (finish-merge.sh output above). Nothing was pushed. Inspect it, then reset the branch to `<pre_push_sha>` yourself or publish it yourself." |
| `sync_foreign_operation` | step 2 `foreign_op`; `FINISH_FAIL no_merge_head` / `foreign_merge`; resume row 6 | Another operation owns the checkout. It was not touched. |
| `sync_merge_failed` | step 4 (git refused, or the probe and the merge disagree); step 5 `uv` failure | git's own file list, or the failing command's output; the merge was aborted. |
| `sync_marker_left`, `sync_unmerged_left`, `sync_staged_unexpected` | step 9 finish gate | The guard that failed and the paths; the merge stays in progress with nothing committed. |
| `sync_commit_failed` | step 9 `hook_rejected` (or `usage`) | Hook output verbatim; the merge stays in progress with the resolution intact; commit it yourself after fixing the cause, or abort it. |
| `sync_head_mismatch` | step 1; step 10(a) | The PR head moved or the checkout is not the PR head; the local merge commit is named when one exists. |
| `sync_range_mismatch` | step 10(b); `FINISH_FAIL parents_mismatch` | The commit's parents are not exactly the PR head and the recorded base tip. |
| `sync_base_moved` | step 10(c) | The recorded base tip is no longer on `origin/<base>` (the base was rewritten). |
| `sync_tier3` | steps 5 to 6 (Tier 2 escalation: semantic, intent not statable, validator disagreement, evidence failure, unreadable file); step 5 lock trust gate (Tier 1 or Tier 2: the merged `pyproject.toml` names code `uv lock` would run) | The Tier 3 template plus the reason (for the lock trust gate, each finding); the merge was aborted; `resolution.md` kept (Tier 2). |
| `sync_validation_failed` | step 7 | The red gate; a red base can cause this (the section 6 command shows the checks of `origin/<base>`); the merge was aborted. |
| `push_rejected` | step 12; resume row 1 | git's rejection verbatim; never re-driven. |
| `push_failed` | step 12 (first push or Branch B re-drive) | The push failed (stderr verbatim). After a first push, `--resume` checks whether it landed (three-way remote check, row 4b). After a failed re-drive, `--resume` does not retry: it halts `resume_unrepresentable` (row 4b'). |
| `resume_unrepresentable` (row 4b') | `--resume` with an open conflict cycle whose dangling push no crash record matches | The merge commit `<target_sha>` of cycle `<cycle_id>` may or may not be on the PR. Nothing more was pushed. If the PR head (`gh pr view <N> --repo "$REPO" --json headRefOid`) equals it, re-run with `--pr <N>`; otherwise push or drop it yourself, then re-run. |
| `resume_unrepresentable` | `crash_resume_plan`, `conflict_resume_plan` | The run-log cannot place the conflict cycle safely; a local merge commit is named so the operator can push or drop it. |
| `router_unreachable` | `conflict_action` default row | Internal routing error; nothing was changed. |

Report-only reasons (no halt by themselves): `no_conflict`, `behind_only`, `blocked`, `tier1_planned`, `tier2_planned`, `tier2_report_only`, `tier1_deferred`, `tier1_proposed`, `tier1_l2_preserved`, `tier1_local`, `tier1_sync`, `tier2_merge`, `no_round_budget`, `l0`, `tier1_l1_preserved`. CI-side report reasons: `pr_conflicting` (CI wait skipped) and `ci_not_started` (CI expiry with no registered check).

## 13. Revert

A pushed merge commit is reverted by a new commit, never by rewriting history. The L2 and L3 reports print it (K13):

```bash
git revert -m 1 <merge_sha>
```
