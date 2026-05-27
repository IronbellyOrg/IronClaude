# Promotion Adapters Reference

Load-on-demand at Wave 7. Authoritative spec source: §14.5.1, §14.5.4, §14.5.5 of `merged-requirements.md`.

## Adapter table

Two registered adapters in v1.0. Adapter selection is deterministic from the resolved input path; if both apply or neither applies, promotion is suppressed (`promotion_action: skipped`, reason logged).

| Adapter | Source path glob | Destination path | Trigger signal |
|---------|------------------|------------------|----------------|
| `task` | `.dev/tasks/to-do/TASK-*` | `.dev/tasks/done/TASK-*` | `--tasklist` resolves under `.dev/tasks/to-do/<TASK-DIR>/` AND tasklist frontmatter has a `status` field |
| `sprint-release` | `.dev/releases/current/<release>/` | `.dev/releases/complete/<release>/` | `--scope` or `--tasklist` resolves under `.dev/releases/current/<release>/` |

**Disambiguation cases.**

- `task` adapter trigger requires BOTH the path-glob match AND a `status` field in the tasklist frontmatter. A `.dev/tasks/to-do/TASK-*` path with missing/unparseable frontmatter fails condition 5a of the §14.5.2 gate before adapter selection is even relevant — the gate blocks promotion regardless.
- `sprint-release` adapter trigger accepts EITHER `--scope` resolving under `.dev/releases/current/<release>/` OR `--tasklist` resolving under the same. Both forms select the same adapter.
- If a tasklist lives inside a release directory (e.g. `.dev/releases/current/R12/tasks/TASK-foo/`), the `sprint-release` adapter wins because the path-glob match is evaluated at the release-directory level first. Adapter precedence is path-specificity, not declaration order.
- When NEITHER adapter's source-glob matches the resolved input, promotion is suppressed with `promotion_action: skipped`, `skip_reason: no-adapter-match`. When BOTH match (should not occur with the v1.0 disjoint source-globs but defensive-coded), promotion is suppressed with `skip_reason: adapter-ambiguity` and both candidate adapter names are recorded in the promotion-log.

**Operator-added extensions (deferred to v1.1).** In v1.0 the adapter registry is hard-coded to the two adapters above; there is no operator-facing registration surface. The v1.1 extension point will accept adapter definitions via a `promotion-adapters.yaml` file under the operator's repo (planned shape: list of `{name, source_glob, destination_template, trigger_predicate}` entries), loaded by reflect at startup and merged into the registry after the two built-ins. Collision between operator and built-in adapter names is resolved in favor of the built-in. Until v1.1 ships, custom promotion targets MUST be handled by the operator manually after reflect emits `promotion_action: skipped`.

## Flag semantics

All five flags are documented in §14.5.4. Per-flag behavior and interaction rules:

| Flag | Default | Effect |
|------|---------|--------|
| `--no-promote` | unset | Suppress Wave 7 entirely. Emits `promotion_action: skipped`, `skip_reason: user-flag`. No gate evaluation, no mutation, no checkpoint. |
| `--promote-anyway` | unset | Override gate condition 2 (`status: partial`) ONLY. Conditions 1, 3-9 still apply unmodified (including condition 9 on `convergence_score` and the split conditions 5a/5b/6a/6b). **Has no effect on `status: failed`** — failed verdicts remain blocked. |
| `--promote-dry-run` | unset | Print the exact `mv` command + full 9-condition gate evaluation; perform no mutation. No checkpoint, no promotion-log entry. |
| `--promote-mode <auto\|task\|sprint-release\|none>` | `auto` | Force a specific adapter or disable selection. `auto` runs the path-glob match from the adapter table. `none` is equivalent to suppressing Wave 7 but still emits a structured `promotion_action: skipped` with `skip_reason: mode-none`. |
| `--promote-resume <checkpoint-path>` | unset | Resume an interrupted cross-fs promotion from `<output>/promotion-checkpoint.yaml`. **Mutually exclusive with `--no-promote`, `--promote-anyway`, `--promote-dry-run`.** Does NOT re-run the verdict pipeline or re-evaluate the 9-condition gate (the gate was satisfied when the checkpoint was written; re-evaluating could fail if Wave 6 or external mutation has since changed state). See §14.5.5 partial-state recovery. |

**Mutual exclusion enforcement.** `--promote-resume` rejects combination with any of the other three flags at CLI-parse time (before any wave executes). The other three flags are not mutually exclusive with each other in general, but `--no-promote` short-circuits before `--promote-dry-run` or `--promote-anyway` can have any effect.

**Flag interaction reference (precedence order):**

1. `--promote-resume` — if set, all other promotion flags are rejected at parse time; reflect runs only the recovery action against the checkpoint.
2. `--no-promote` — if set, Wave 7 is suppressed entirely; `--promote-anyway`, `--promote-dry-run`, and `--promote-mode` are accepted at parse time but have no effect.
3. `--promote-mode none` — equivalent to `--no-promote` for adapter selection; still emits a structured skip entry.
4. `--promote-dry-run` — runs the full gate eval and adapter selection, prints the `mv` command, exits Wave 7 without mutation.
5. `--promote-anyway` — combined with a clean gate (conditions 1, 3-9), permits promotion when condition 2 alone would block. Has no effect when any of conditions 1, 3-9 fail or when `status: failed`.

## Mutation mechanics + collision rules

**Filesystem detection.** Reflect determines same-fs vs cross-fs by comparing `stat().st_dev` of the source path and the destination parent directory. If `st_dev` matches, the `rename(2)` path is used; otherwise the copy + verify + remove + fsync path is taken. The decision is recorded in the promotion-log as `cross_fs_promotion: bool`.

**Same-filesystem move.** Template: `mv <source> <destination>`. Implemented by POSIX `rename(2)` — atomic. The destination either appears in full or not at all, and the source disappears in the same syscall. No checkpoint required; no `cross_fs_promotion` flag emitted.

**Cross-filesystem move.** Template: copy + verify (SHA-256) + remove + fsync. **NOT atomic** — there is a window between copy completion and source removal during which both source and destination exist on disk. Emits `cross_fs_promotion: true` into the promotion-log and is gated by the checkpoint mechanism below. NOT `rsync` (non-atomic and not what `mv` invokes).

**Pre-mutation checkpoint (cross-filesystem only).** Wave 7 step 7.3.5 (inserted between 7.3 collision-check and 7.4 mv) MUST write `<output>/promotion-checkpoint.yaml` BEFORE invoking the copy. Schema verbatim from §14.5.5:

```yaml
checkpoint_version: "1.0"
adapter: task | sprint-release
source: <abs path>
destination: <abs path>
intended_action: moved
cross_fs: bool
source_sha256_before: <hex>
copy_started_at: <ISO-8601>
copy_completed_at: <ISO-8601> | null   # written after copy succeeds, before remove
state: pending | copy-complete | move-complete | aborted
```

On normal completion, the checkpoint's `state` field transitions `pending` → `copy-complete` (after fsync) → `move-complete` (after source removal).

**Checkpoint field semantics.**

- `checkpoint_version`: schema version string; v1.0 reflect rejects checkpoints with other versions and falls back to manual operator review.
- `adapter`: literal `task` or `sprint-release`; future operator-registered adapter names are valid in v1.1+.
- `source` / `destination`: absolute paths; relative paths are rejected at checkpoint-write time.
- `intended_action`: always `moved` in v1.0 (copy-only or link-only modes deferred).
- `cross_fs`: redundant with the existence of the checkpoint (same-fs moves never write one) but explicit for forensic clarity.
- `source_sha256_before`: computed over the source directory tree (recursive merkle of file SHA-256s sorted by relative path). Used in step 7.5 SHA-invariance verification.
- `copy_started_at` / `copy_completed_at`: ISO-8601 with timezone offset; `copy_completed_at` is `null` until the copy finishes successfully.
- `state`: monotonically advances through the recovery-table values; an `aborted` transition is terminal.

**4-state recovery table.** On process crash, the checkpoint persists on disk; recovery is driven by whether source AND destination exist at the recorded paths:

| state at crash | source exists | destination exists | Recovery action |
|----------------|---------------|--------------------|-----------------|
| `pending` (crash during copy) | yes | partial/missing | Operator/reflect deletes partial destination; rerun reflect (idempotent re-promotion will re-check the gate). |
| `copy-complete` (crash between copy and remove) | yes | yes (full, SHA matches) | `--promote-resume` completes the move (verifies SHA, removes source, transitions to `move-complete`). |
| `move-complete` | no | yes | Promotion already succeeded; checkpoint can be archived. No action. |
| `aborted` | indeterminate | indeterminate | Manual operator review — checkpoint records the cause in a `abort_reason` field. |

**Promotion-log pre-write atomicity (§14.5.5).** Step 7.6 (append promotion-log) MUST be split: a `pending: true` log entry is written BEFORE step 7.4 (the mv), and is flipped to `pending: false` after step 7.5 (post-move SHA verification). This ensures that if 7.4 succeeds but the 7.6 finalization write fails (disk full, permission denied, process crash), the forensic record still exists with `pending: true` — the next reflect invocation MUST detect a `pending: true` log entry whose `destination` path now exists and `source` path does not, treat it as a `move-complete` state, and emit a one-line warning to the audit log so the operator can reconcile.

**Destination collision rules.** Seven cases, evaluated at Wave 7.3 and re-checked at 7.3 immediately before mutation:

| Condition | Behavior |
|-----------|----------|
| Destination does not exist | Proceed |
| Destination exists, empty dir | Remove empty destination, then move (audit-logged) |
| Destination exists, non-empty, differs from source | STOP: `promotion_action: rejected`, `destination_collision`; diff captured. Do NOT auto-suffix or overwrite. |
| Destination exists, non-empty, identical to source | Idempotent: `promotion_action: already-promoted`; remove source after second SHA verification |
| Source path no longer exists at Wave 7.4 | FAIL: `promotion_action: failed`, `source_disappeared` |
| Destination parent dir missing | Create parent; emit audit row |
| Both source AND destination exist with matching SHA AND a `pending: true` promotion-log entry references them | Treat as crash recovery: emit `promotion_action: resumed`; complete source removal; flip log entry to `pending: false`. Only fires under `--promote-resume`. |

## Rollback command template

**Operator-driven manual rollback.** Reflect itself never auto-rolls-back; auto-rollback is deferred to v1.1 per §19.3. Every promotion-log entry includes the inverse `mv` command in a `rollback_command` field. Template:

```bash
mv <destination> <source>
```

Where `<destination>` and `<source>` are the absolute paths recorded in the same promotion-log entry. The operator is responsible for verifying that:

1. The destination path still exists at the recorded location (no intervening moves).
2. The source path is currently empty (or did not get re-created by a subsequent reflect run).
3. No downstream tooling has consumed the promoted artifact in a way that would be broken by the rollback (e.g., git commits, release tags).

Reflect does NOT `git add` moved files. Operator stages and commits both the original promotion and any subsequent rollback.

**Rollback log discoverability.** The `rollback_command` field is emitted on EVERY promotion-log entry, including:

- Same-fs atomic moves (where `cross_fs_promotion: false`).
- Cross-fs moves that completed normally (`state: move-complete`).
- Crash-recovered moves promoted via `--promote-resume`.

For `promotion_action: rejected` and `promotion_action: failed` entries, no `rollback_command` is emitted because no mutation occurred. For `promotion_action: already-promoted` (idempotent case), the rollback command targets the most recent source-removal step only — restoring the destination is the operator's responsibility if they want to undo the original promotion that produced the existing destination.

**Auto-rollback deferral (§19.3).** v1.1 will add `--auto-rollback-on-verify-fail` (auto-revert when Wave 7.5 post-move SHA verification detects mismatch). v1.0 emits a verify-fail entry with `promotion_action: verify-failed` and surfaces the inverse `mv` command in the audit log for operator action, but does not execute the inverse automatically. Operators MUST treat verify-failed entries as urgent — both source and destination may exist in inconsistent states pending the rollback.

## Wave 7 sequence (adapter perspective)

For cross-reference with §14.5.3, the adapter layer is invoked at the following points within Wave 7:

1. **7.1 Adapter resolution** — path-glob matching from §14.5.1; selects `task`, `sprint-release`, or `none`. `--promote-mode` overrides auto-selection. Adapter identity is fixed at 7.1 and reused at every subsequent step.
2. **7.2 Gate re-verification** — adapter-agnostic; the 9-condition gate from §14.5.2 is evaluated against the same input that drove adapter selection. Wave 6 re-Read happens here if applicable.
3. **7.3 Collision check** — adapter-aware; the destination path is computed via the adapter's destination template (e.g. `task` rewrites `.dev/tasks/to-do/TASK-foo/` → `.dev/tasks/done/TASK-foo/`). The 7-row collision table is then applied to the computed destination.
4. **7.3.5 Checkpoint write** (cross-fs only) — records `adapter` field so recovery can re-bind the same adapter at resume time without re-resolving.
5. **7.3.6 Promotion-log pre-write** — records the adapter and the inverse `mv` command before any mutation.
6. **7.4 Move** — atomic on same-fs, copy + verify + remove + fsync on cross-fs.
7. **7.5 SHA re-verify** — adapter-agnostic; uses `source_sha256_before` from the checkpoint (cross-fs) or a freshly computed source-side SHA (same-fs, captured at 7.3).
8. **7.6 Finalize** — promotion-log entry flipped to `pending: false`; checkpoint state advances to `move-complete`; audit-log row appended with adapter name.
9. **7.7 Return-contract** — `promotion_adapter`, `promotion_action`, `cross_fs_promotion`, and `rollback_command` are populated in `return-contract.yaml` for downstream tooling.

## Telemetry fields summary

The following promotion-related fields appear in the return-contract and promotion-log. They are populated regardless of outcome (skip/reject/success/failure) to keep downstream tooling's parsing surface uniform:

- `promotion_adapter`: `task` | `sprint-release` | `none`.
- `promotion_action`: `moved` | `already-promoted` | `resumed` | `skipped` | `rejected` | `failed` | `verify-failed` | `dry-run`.
- `skip_reason` / `reject_reason`: free-form short string when `promotion_action` is `skipped` or `rejected`.
- `cross_fs_promotion`: `bool`; `false` for same-fs and for all non-mutation outcomes.
- `citation_revalidation_at_promotion`: `bool`; `true` if Wave 6 ran and 7.2 re-Read cited files (§14.5.2 cond 6a clarification).
- `rollback_command`: inverse `mv` string; absent on `rejected` / `failed` entries.
- `gate_evaluation`: 11-atomic-field struct (1:1 with the 9 numbered §14.5.2 conditions; cond 5 and cond 6 are each split into a/b sub-conditions per the structural split). Field order: `mode_post`, `status_success`, `tasklist_completion_pct_1_0`, `no_drift_no_regression`, `frontmatter_present`, `frontmatter_status_matches`, `no_citations_dropped`, `no_grounding_gaps`, `no_input_drift`, `no_user_decision_pending`, `adversarial_result_present`. Written even when the gate blocks promotion so operators can see which condition failed. Source-of-truth contract: SKILL.md §14.5.6 (L1213-1224).
- `gate_evaluation_failures`: list of `gate_evaluation` keys whose value is `fail` — derived convenience field consumed by eval-workspace `yaml_list_contains` assertions; emitted byte-1:1 with the `gate_evaluation` map so the two cannot drift. Empty list when `gate_passed: true`.
