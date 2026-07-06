---
artifact: adversarial-round-3-resolution
role: backend
round: 3
topic: "PR Review Auto-Remediation Monitor (V1.0)"
created: 2026-06-11
owns: [INV-007, INV-009]
accepts: [INV-001, INV-016]
---

# Round 3 — Backend Normative Resolution (push idempotency + dedup identity)

I accept the architect's INV-001 counter definition: `round_counter` increments by exactly 1 only on `S5_AWAITING_REREVIEW --[review_observed ∧ sha_attributed_to_our_push]--> S2_CLASSIFY`, is write-ahead journaled, monotonic, and gated by `round_counter >= max_rounds` before the next fix cycle opens.

---

## INV-007 — Write-ahead push idempotency closes the git-push/log crash window

### Normative ordered event sequence

For every authorized push attempt, the JSONL run-log sequence is exactly:

1. `push_decision{run_id, cycle_id, round_counter, predicates, authorized:true, pre_push_sha, target_branch, target_remote}` is appended and fsynced before any push-side effect.
2. Compute `target_sha` locally as the commit intended to land on `target_branch`.
3. `push_initiated{run_id, cycle_id, idempotency_key, pre_push_sha, target_sha, target_branch, target_remote, remote_ref}` is appended and fsynced before `git push` starts.
4. Execute `git push <target_remote> <target_sha>:<target_branch>`.
5. After `git push` returns successfully, append and fsync `push_completed{run_id, cycle_id, idempotency_key, pre_push_sha, target_sha, target_branch, target_remote, remote_ref, pushed_at}`.
6. Enter `S5_AWAITING_REREVIEW`; later, only a re-review attributed to a recorded `push_initiated.target_sha` may complete the cycle and tick `round_counter`.

The idempotency key is `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`; it is intentionally based on the PRE-push SHA plus cycle identity, not on post-hoc `push_completed` state.

### Crash-window resume rule

On `--resume`, if the latest event for an idempotency key is `push_initiated` with no matching `push_completed`, the monitor MUST NOT create another commit or issue another push until it queries the remote branch. It resolves the window as follows:

- If `target_sha` is reachable from the remote branch tip, treat the push as landed, append `push_completed{recovered:true,...}` using the original `push_initiated` fields, and resume in `S5_AWAITING_REREVIEW`.
- If `target_sha` is not reachable from the remote branch tip and the remote ref is still at `pre_push_sha` or otherwise lacks the target commit, treat the push as not landed, append `push_aborted_or_not_landed{recovered:true,...}`, and return to the pre-push decision path for the same cycle without recomputing the fix.
- If remote state is ambiguous or the branch tip has moved to an unrelated SHA, HALT_HUMAN with the original `push_initiated` fields and observed remote SHA.

**Ordering invariant:** every externally visible push must have a durable `push_initiated{target_sha,...}` record fsynced before `git push`, and every `round_counter` increment must attribute to one of those recorded target SHAs.

---

## INV-009 — Separate fix identity from reply identity and status wording

### Fix-dedup key

The fix-dedup key is `fix_key = sha256(normalize(repo_relative_path) + "\n" + normalize(line_or_range) + "\n" + normalize_finding_body(body))`. It excludes `comment_id`, `thread_id`, review id, author timestamp, and generated reply text. This makes a fresh Augment comment id for the same `body + file:line` defect reuse the same fix record.

### Reply/resolve-dedup key

The reply/resolve-dedup key is thread-scoped: `reply_key = provider + ":" + repository + ":" + pr_number + ":" + comment_id_or_thread_id + ":" + fix_key + ":" + reply_purpose`. It intentionally includes the current comment/thread id because replies are visible per GitHub thread.

When Augment mints a fresh `comment_id` for the same underlying defect, the monitor MUST NOT re-run the fix if `fix_key` is already applied or attempted in the current run. It MAY reply on the fresh thread because that thread has not yet been answered, but the reply MUST cite status from the fix record: `applied_edits > 0` may be phrased as applied/validated; `applied_edits == 0` or ungroundable/drop MUST be phrased as no code change applied and must not say resolved. Old threads are not resolved solely because a fresh thread appeared; they are resolved only by their own resolve key and only when the status permits.

### INV-010 disposition

Rewording collisions remain MEDIUM, not closed by `body + file:line`. The spec must add a secondary near-duplicate detector or human-review fallback later; it is outside this HIGH-invariant closure.
