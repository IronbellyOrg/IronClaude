# Round 2 rebuttal: advocate B (analyzer lens: root cause, evidence)

## 1. Responses to criticisms

Criticisms of variant B from round 1 (A, C, D, E) and from round 2 so far (A):

1. **NFR-010 resets a corrupt record to empty (X-003).** Conceded in full. The root cause is that B treated the record as a cache; it is the only at-most-once guard between launch and marker (the claim has no mutual exclusion; `refs/claim.md:41-42` stops only on *another* login). An empty record re-dispatches every `launched` issue whose marker is not yet posted. Adopt A/D: an unreadable or unknown-version record exits 6, launches nothing, never resets.
2. **Section 7.3 relaunches `launched`/`failed` after the lease (X-001).** Conceded in full. Advocate A is right that this and item 1 are B's two most dangerous rules. The lease cannot be a relaunch trigger because the claim posts its marker in Wave 6 after an unmeasured multi-agent Wave 4 (A-009). Adopt D: `launched` without a marker after the lease becomes `abandoned`, reason `claim_not_observed`; only `reset` reopens it.
3. **`pending` found at cycle start is treated as `launched` (X-002).** Conceded. Treating it as `launched` fed item 2's relaunch path. Adopt D: `abandoned`, reason `pending_orphan`.
4. **`--label-only` mode (X-005).** Conceded. A missing `read:project` must not widen eligibility; option D is the documented fallback. Withdrawn.
5. **No rate-limit handling, 42-call worst case (X-006, E).** Conceded on handling: adopt C's persisted next-permitted time plus a distinct exit code. Partly contested on cost: B's 42 had two causes. The Project list (one call, but a 100-item cliff) is fixed by adopting E's per-issue `projectItems`. The complete event history is not a cost bug; it is the correctness requirement round 1 agreed (C-002 HYBRID, 4 of 5). The merge keeps completeness and budgets it: event pages count toward E's 35-call cap, and a cap reached mid-issue skips that issue, never approves it.
6. **One verb, no `status` or `check-config` (C-020, C-021).** Conceded. Adopt A/D verbs and D's `DISABLED` switch.
7. **`--method GET` rule contradicts GraphQL reads, which are POST (my own round-1 finding).** Conceded; A accepted the corrected wording. The rule becomes: REST calls are GET; GraphQL calls send only a `query` document from a fixed set, never `mutation`.
8. **No bot check on the approver.** Conceded: `actor.type == "User"` and login not ending `[bot]` (agreed C-002).
9. **Lock loser exits 0 (FR-019).** Conceded to D's exit 75 `lock_held`: a hung cycle that silently exits 0 every 5 minutes is invisible to the staleness signal.

Points I still defend, with evidence, because other variants dropped them:

- **Origin check before any `gh` call (B FR-002).** A's round-2 E2 shows `origin_repo.py:102` `check_claim` returns a bare int with no repo check, and the claim consults only `origin` for the repository. If the configured worktree's origin is not IronClaude, the launched claim targets the wrong repository. Only B and C test this; it belongs in C-010, and A's ruling now includes it.
- **Orca probe (B FR-014).** A's E1 found `_find_orca()` at `install_user_setup.py:198` already resolving `orca-ide` or `orca`. A literal `"orca"` argv[0] (A, D) fails on a host that has only `orca-ide`. Reuse the helper.
- **Approver and event ID in the audit (B FR-020).** A's C-007 ruling now carries `approver_id` and `approval_event_id`; nothing further needed.
- **Re-approval never resets counters (B OD-6).** No other variant states it. Without it, removing and re-adding the approval label is a free relaunch after `failed`/`abandoned`. Added to the C-007 ruling.
- **Unrecognised argv fails loudly in tests (B FakeRunner exit 99, `_assumed_shape` fixtures).** This is how "read-only" is proven by test rather than by review, and how UNVERIFIED JSON shapes stay marked until the live test. Carried in S-007 (traceability with UNVERIFIED tags).
- **Per-issue fail scope (B NFR-009).** Converged into A's C-015 ruling.

## 2. Changed views on other variants

- **D** is now my reference for the state machine and operations: `launches` separate from `attempts`, `pending_orphan`, `claim_not_observed`, `DISABLED`, exit 75, `last_cycle_age_seconds`. In round 1 I split votes between B and D; on X-001, X-002, X-003 and C-018 I now vote D outright.
- **E** fixes the one scaling defect every other variant shared: `gh project item-list -L 100` fails closed permanently once the Project passes 100 items (D's own R3 admits it). Per-issue `projectItems` makes cost scale with candidates, not Project size. E's 35-call cap is the right shape for B's pagination concern.
- **C** I underweighted. Its "absent or unreadable evidence is not positive evidence" is the cleanest statement of the fail-closed root cause, and account-ID approvers close the rename hole (A-003). I still reject SQLite (S-005): a JSON file written with the existing `write_prepared_bytes` (`swarm/atomic.py:14`) meets the integrity need with no new storage engine, and C's required properties (no silent reset, explicit init) carry over.
- **A** trimmed its seams in round 2 (protocols only for runner, store, launcher); my round-1 objection to speculative stages is resolved. A's conceded orca argv[0] and origin check now match B.

## 3. New evidence (checked read-only this round)

- **N1. The house pattern for paged GitHub reads exists and fails closed at a cap.** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:46-56`: explicit `-F per_page=100 -F page=<n>` with `--method GET`, the comment "Explicit page numbers avoid an unbounded gh --paginate on a broken API cursor", and "fail incomplete at the cap, never silently truncate". No other `--paginate` appears under `src/superclaude` (grep). So complete event and comment reads (C-002, C-024) have a precedent: explicit pages, each page counted, cap reached means incomplete, incomplete means not positive. This settles how C-002 and E's call cap compose.
- **N2. The claim reads comments itself and reuses the latest marker** (`refs/claim.md:26`, `:29`), and re-claim by the same login is "allowed and idempotent" (`:42`) with earlier marked comments edited (`:43`). Consequence: a duplicate launch for the same login does not double-post, but it starts a second full session and a second Wave 4. At-most-once remains a cost and review-load requirement; it never justifies trading a missed launch for a duplicate.
- **N3. The claim stops on a pull request** (`refs/claim.md:39`, `E-NOT-AN-ISSUE`) and on a closed issue (`:40`). The watcher's `state == OPEN` check and `gh issue list` (issues only) are defence in depth; C's explicit non-PR predicate costs nothing and can stay as a pure-function check.
- **N4. The claim proceeds on an unassigned issue** (`refs/claim.md:41-42` stops only on another login). Candidate-1 routing (exactly the own login assigned) is stricter than the claim, which is why A-005 (someone must assign first) is real and must be visible in the audit as `unassigned` skips.
- **N5.** Confirmed A's citations exist: `_find_orca` at `install_user_setup.py:198`, `check_claim` at `origin_repo.py:102`, `write_prepared_bytes` at `swarm/atomic.py:14`.

## 4. Updated positions

"AGREE" means I accept advocate A's round-2 proposed ruling as written.

| Point | Superior variant | Confidence % | Merged ruling or AGREE with A |
|---|---|---|---|
| C-001 | HYBRID | 85 | AGREE |
| C-004 | A | 85 | AGREE |
| C-005 | HYBRID | 80 | AGREE |
| C-006 | HYBRID (E+B) | 80 | Discovery: `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --json number,labels,assignees,state -L 100`; 100 results exit 4. Every `gh` call, including each event or comment page (`per_page=100`), counts toward a 35-call cap; cap reached mid-issue skips it `budget_exhausted`. |
| C-007 | D | 85 | A's fields and states, plus: removing and re-adding the trigger or approval label never resets `attempts` or `launches`; only `reset <N>` (audited) does. A fresh launch requires `launches == 0`. |
| C-008 | HYBRID | 75 | AGREE |
| C-009 | HYBRID | 70 | Immediately before launch, re-read state, labels, assignees and Project Status. A failed read or predicate skips the issue `revalidation_failed`, leaves the record unchanged and launches nothing. Only then write `pending` durably and call Orca. |
| C-010 | HYBRID (B+A) | 85 | AGREE |
| C-011 | C | 85 | AGREE |
| C-012 | HYBRID | 80 | AGREE |
| C-013 | HYBRID (C) | 80 | AGREE |
| C-014 | HYBRID | 80 | AGREE |
| C-015 | C | 85 | AGREE |
| C-018 | D | 85 | AGREE |
| C-020 | HYBRID | 85 | AGREE |
| C-023 | HYBRID | 75 | AGREE |
| C-024 | HYBRID | 80 | `claimed` requires a comment by the own login containing `<!-- sc:issue:claim -->`, read over all comment pages and returned only as a `--jq` boolean; an incomplete read is not evidence. Assignment is never evidence. A marker without a record yields `claimed`. |
| S-001 | HYBRID | 70 | AGREE |
| S-004 | A | 75 | AGREE |
| S-005 | HYBRID | 80 | AGREE |
| S-007 | B | 70 | AGREE |
| S-008 | HYBRID | 65 | AGREE |
| X-001 | D | 90 | AGREE |
| X-002 | D | 90 | AGREE |
| X-003 | D | 95 | AGREE |
| X-005 | D | 90 | AGREE |
| X-007 | HYBRID | 75 | AGREE |
| X-008 | HYBRID | 75 | AGREE |

Reasons for the four non-AGREE rows:

- **C-009.** A's text writes `pending` first and then deletes the entry when the re-read fails. Root cause: the deletion is needed only because the write came too early. Re-reading first removes the deletion path and one class of `pending_orphan` (a crash during a failed re-read would otherwise abandon an issue that never launched). The window between re-read and launch grows only by one local `fsync`. The audit line keeps the `revalidation_failed` evidence, so nothing is lost.
- **C-006.** Adds the page-counting rule from N1. Without it, "complete event history" (agreed C-002) and the 35-call cap (E) contradict on an issue with more than 100 events.
- **C-024.** Adds "all comment pages" and "incomplete read is not evidence". A marker on page 2 missed by a one-page read would leave a claimed issue `launched`, and under D's X-001 rule it would end `abandoned` instead of `claimed`: a wrong audit, not a duplicate. Low risk, cheap to state.
- **C-007.** Adds B OD-6 (no counter reset on re-labelling); otherwise A's text.

## 5. Shared-assumption changes

Only assumptions whose answer changed since my round 1:

- **A-001 (state survives restarts):** QUALIFY, tightened. The store is created only by `check-config` (explicit init); a missing store after init exits 6 and never starts empty, so loss of `$HOME` stops dispatch rather than duplicating it.
- **A-002 (slash command runs from `--prompt`):** QUALIFY, extended. The same owner-run live test must also record the launched session's permission mode (C-014) and the real success and `unknown` JSON, which replace the `_assumed_shape` fixtures.
- **A-003 (logins stable):** changed from QUALIFY to a split ACCEPT. Owner routing stays by login (the claim itself works by login, N4); approvers move to account IDs (C-013), so a rename cannot transfer approval trust.
- **A-007 (`flock` effective):** QUALIFY, plus A's two-process lock test as acceptance; a local, single-host state directory is a documented setup precondition.
- **A-009 (marker within lease):** REJECT unchanged, now reflected in the merge: with D's X-001 and X-002 rules the lease is only a reporting threshold, so no safety property depends on it.
