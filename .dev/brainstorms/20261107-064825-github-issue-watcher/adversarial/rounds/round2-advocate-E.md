# Round 2 rebuttal: advocate E (performance lens: bottlenecks, scaling, cost-to-serve)

Read: blind/variant-A..E, diff-analysis.md, round1-advocate-A..E, round1-tally.md, round2-advocate-A..D. I go last. Blind rules held: I opened nothing outside `adversarial/`, so code facts below are marked as relayed from another advocate unless they are arithmetic on spec values.

## 1. Responses to criticisms

**Conceded (with the fix I now support)**

1. **FR-006 is one unpaginated events call, and the 33-call arithmetic ignores paging (B, C).** Conceded. Complete approval history may need several pages. Fix is B's N1 rule (the `poll-augment-review.sh` pattern): explicit `per_page=100` pages, each page counts toward the cap, a cap reached mid-issue skips that issue as `budget_exhausted`, incomplete evidence is never positive. The hard cap stays 35, so worst case is now a hard bound, not an estimate: 12 cycles x 35 = 420 calls/h = 8.4% of 5,000/h on one login. Idle stays 2 calls (24/h, 0.48%).
2. **Per-issue record files `records/<N>.json` (S-005; A, C, D).** Conceded. One versioned JSON document needs one durable write for slot plus counter. Per-issue files cannot make "slot consumed and `launches` incremented" atomic with a day-cap count across issues, and a missing directory is harder to detect than a missing file. I adopt D's S-005 text.
3. **30-day pruning of terminal records (NFR-013; C).** Conceded as unsafe: pruning an `abandoned` entry re-opens an issue that may have a live session. Compact terminal entries to tombstones (key, state, timestamps) and never delete a consumed key. Growth cost: roughly 100 bytes per launched issue, so 1,000 issues is about 100 KiB. Pruning saves nothing worth the risk. The `considered` cap of 1000 goes too.
4. **FR-012 leaves a removed issue "deleted or marked abandoned" (A, B, D).** Conceded. Adopt B/C/D order: re-read first, a failed re-read writes no entry (audit `revalidation_failed`), then durable `pending` with `launches` consumed, then Orca.
5. **`--agent <agent>` (X-008).** Withdrawn in round 1, still withdrawn.
6. **GraphQL is POST, so "every call is GET" rejects my FR-008 (B).** Conceded. Adopt A's wording: no REST write verb, no `mutation`; queries are module constants and a test scans them.
7. **`claimed` needs own assignee AND marker (A).** Conceded. The marker by the own login is the claim's evidence; assignment alone is none. Marker alone gives `claimed` (A/B C-024).
8. **Orca-worker detector rests on an ASSUMPTION (A, D).** Dropped. It is not needed once cron stays disabled until the live test.
9. **`~/.superclaude/` state path (D).** Conceded. Use a state directory under the XDG state path, local filesystem only.
10. **Corrupt record unspecified (D).** Conceded. Exit 6, no launch, never reset.
11. **`reset <N>` without a guard (C).** Conceded. D's form: `--forfeit-guarantee`, only `abandoned`, under the lock, audited.

**Defended**

12. **Daily cap of 6 is "speculative" (A R1).** Defended as a cost bound on a selection bug, now defined as a [PROPOSAL] counted from stored launch timestamps (no separate counter that can drift) and surviving tombstoning. A and D now accept it. It needs owner sign-off because it can delay legitimate work; the poller must report `day_cap_reached` so the delay is visible.
13. **Prefilter before per-candidate calls (FR-004).** No one attacked it; B and C now require it in C-006. It is the main reason idle cost is 2 calls.
14. **Per-issue `projectItems`.** Adopted by all variants; scale is candidates (at most 10 per cycle), not Project size.

**Cost-model gap I found in my own text (new, not raised by others)**

15. **A call cap is not a time cap.** 35 calls at a 20 s `gh` timeout is 700 s, more than a 300 s cadence; a 120 s Orca launch plus a 10 s probe adds more. The spec needs a wall-clock budget: reads end at 240 s with exit 3; no launch is started after 120 s elapsed; the Orca probe and re-read count inside it. The non-blocking lock means overlap exits 75 rather than double work.

## 2. Changed views

- **C.** Consume-before-spawn is the only rule that makes at-most-once true at every crash point. I take it, but in D's JSON form; SQLite buys nothing for a few hundred bytes of state.
- **D.** Best operations spec, and D's concessions made it safer. I take exit 75, `DISABLED`, `last_completed_cycle_age_seconds`, the shadow dry run, `--forfeit-guarantee`.
- **B.** Page counting settles my biggest conflict (complete history versus 35 calls). B's origin check and Orca probe are correctness, not hardening.
- **A.** Its round-2 rulings are the best merge text on 18 or more points; I AGREE with A wherever A and D agree.
- **My own variant.** E wins on C-003 and C-006 only. On state, recovery, and operability E was the weakest variant.

## 3. New evidence

No file outside `adversarial/` was opened (blind rules). Items marked "relayed" were checked by the named advocate, not by me.

- **N1 (arithmetic, mine).** Hard bounds with the 35-call cap: idle 2 calls/cycle; worst 35. One login, W workspaces: idle 24W/h, worst 420W/h. W=5 gives 120 idle (2.4%) and 2,100 worst (42%) of 5,000/h. A 12th always-busy workspace on the same login would exceed 100%; same-login multi-enablement is therefore a cost problem as well as a duplicate-launch problem, and `host` plus `login` in every audit line matters (C-005).
- **N2 (arithmetic, mine).** Cycle time as in item 15: unbounded by call count alone. Needs the 240 s deadline.
- **N3 (arithmetic, mine).** State growth: tombstones about 100 bytes each; 1,000 launched issues is about 100 KiB, read in full every cycle. That is negligible next to one `gh` call, so no pruning is justified.
- **N4 (relayed, B).** `poll-augment-review.sh:46-56` already fails closed at a page cap; no `--paginate` elsewhere in the package. The pattern is house practice.
- **N5 (relayed, A/D).** `write_prepared_bytes` (`swarm/atomic.py:14-39`) gives 0600 and file fsync but no directory fsync, so a thin wrapper must fsync the parent directory. `_find_orca` (`install_user_setup.py:198-221`) calls `subprocess.run` directly with a 10 s timeout; it must go through the injected runner, and its 10 s counts in the cycle budget (D N5).
- **N6 (relayed, D).** No code in the package reads rate-limit headers, so `rate_remaining` has no source. Keep the idle cycle at exactly 2 calls: do not add a `rate_limit` call to learn the budget.

## 4. Updated positions (all 28 UNRESOLVED points)

"AGREE with X" = accept advocate X's round-2 ruling exactly as written.

| Point | Superior variant | Confidence % | Merged ruling or AGREE with X |
|---|---|---|---|
| C-001 | HYBRID | 75 | AGREE with A (names, fail closed; D agrees). Label IDs are a follow-up, not v1. |
| C-004 | HYBRID | 80 | AGREE with A |
| C-005 | HYBRID | 85 | AGREE with A, plus: audit lines carry `host` and `login`; N1 shows W workspaces on one login multiply cost by W. |
| C-006 | HYBRID (E+B) | 90 | AGREE with B (page counting; 35-call cap includes every page; cap mid-issue skips `budget_exhausted`). Idle cycle is exactly 2 calls: login read plus discovery. |
| C-007 | D | 85 | AGREE with D (`launches` consumed in the same durable write as `pending`, before Orca; re-labelling never resets; only `reset <N> --forfeit-guarantee`). |
| C-008 | HYBRID | 70 | [PROPOSAL] lease 60 min (report threshold only), `max_attempts` 3, one launch per cycle, `max_candidates` 10, 10-min backoff after `failed`, `gh` 20 s, Orca 120 s, 240 s cycle deadline. Day cap 6 per rolling 24 h from launch timestamps; owner must approve. |
| C-009 | HYBRID | 85 | AGREE with D (re-read first, failed re-read writes no entry, then durable `pending`, then Orca; orphan `pending` becomes `abandoned`). Re-read adds one Project call per launch inside the 35 cap. |
| C-010 | HYBRID | 85 | AGREE with D (A's argv, `_find_orca` through the injected runner, probe 10 s counted in the cycle budget, origin must be IronbellyOrg/IronClaude). |
| C-011 | C | 90 | AGREE with D (anything after spawn other than confirmed success is `unknown`; `--retry-launch <id>` only with an id; otherwise `abandoned`). |
| C-012 | HYBRID | 90 | AGREE with A |
| C-013 | HYBRID | 85 | AGREE with A |
| C-014 | HYBRID | 85 | AGREE with C |
| C-015 | HYBRID | 85 | AGREE with A |
| C-018 | D | 90 | AGREE with D (lock held exits 75, `DISABLED` exits 0 before any call, `last_completed_cycle_age_seconds` above 900 is unhealthy). |
| C-020 | HYBRID | 75 | AGREE with D (`once [--dry-run]`, `status [--json]`, read-only `check-config`, `init-state`, `reset <N> --forfeit-guarantee`). I reject A's "check-config creates the store": a check verb must not write. |
| C-023 | HYBRID | 80 | AGREE with D (A's list plus 24 h shadow dry run, two-process lock test, staleness alert as activation gates). |
| C-024 | HYBRID | 85 | AGREE with B (all comment pages, `--jq` boolean only, incomplete read is not evidence, marker alone gives `claimed`). |
| S-001 | HYBRID | 70 | AGREE with A |
| S-004 | HYBRID | 75 | AGREE with A (module name `select` withdrawn). |
| S-005 | HYBRID | 90 | AGREE with D (one versioned JSON, `write_prepared_bytes` plus parent-directory fsync, only `init-state` creates it, exit 6 if missing, unparseable or unknown version). Terminal entries become tombstones, never deleted. |
| S-007 | B | 70 | AGREE with A |
| S-008 | HYBRID | 65 | AGREE with A |
| X-001 | D | 90 | AGREE with D (A's text plus a later own marker moves `abandoned` to `claimed`; the consumed slot is never released). |
| X-002 | D | 90 | AGREE with A |
| X-003 | D | 95 | AGREE with A |
| X-005 | D | 90 | AGREE with A (no label-only or Project-off mode; per-issue `projectItems`). |
| X-007 | HYBRID | 85 | AGREE with A (0 ok/disabled; 2 usage/config; 3 auth/scope/timeout/non-JSON; 4 truncated; 5 rate limited; 6 record; 7 launch failed/unknown; 75 lock). Deadline overrun is exit 3. |
| X-008 | HYBRID | 90 | AGREE with A |

## 5. Shared-assumption changes

Only assumptions whose answer changed since my round 1.

- **A-001:** QUALIFY, tightened. Only `init-state` creates the store; missing after init exits 6. Per-issue files are withdrawn because a missing directory is harder to detect than a missing file.
- **A-003:** changed to split ACCEPT. Owner routing stays by login (the claim works by login); approvers by account ID; label names fail closed.
- **A-004:** QUALIFY, now with a cost argument: W workspaces on one login cost W times the budget (N1), so one enabled workspace per login is a cost limit as well as a duplicate-launch limit.
- **A-006:** QUALIFY, narrowed. Clock jumps affect only the 24 h cap, backoff and lease report; no state is relaunched because of time.
- **A-009:** changed from QUALIFY to REJECT as a safety premise. The lease is a reporting threshold only.
- **A-011 (new, mine):** a call cap implies a time bound. It does not; the spec must add a wall-clock deadline (item 15).
