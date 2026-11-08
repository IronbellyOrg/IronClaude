# Round 1 advocate: variant E (performance, bottlenecks, scaling, cost-to-serve)

Section references: "E §n" is variant E's own section; "A §n" etc. likewise. Point IDs are from the diff analysis.

## Position summary

Variant E is the only variant that treats cost as a first-class requirement. It prices the idle cycle (2 calls), the worst cycle (33 calls), the hourly share of the allowance (0.48 and 7.9 percent, E §5) and the expensive event (a launched session, bounded per cycle and per day, E FR-018). Its one structural choice that changes how the system scales is the per-issue `projectItems` query (E FR-008), which makes cost track candidates instead of Project size. On crash recovery, record integrity and pagination, E is weaker than C and D, and the final spec should take those parts from them.

## Steelman per opposing variant

**Variant A (stages behind typed protocols).** Strongest form: every open decision and every alternative (B, C, D) replaces one module, not the cycle (A §1, §8, NFR-011), and the record is keyed by login so a changed login inherits nothing (A §7). It has the cleanest transition table, with an explicit `attempts -= 1` on a cancelled reservation (A §7), a closed skip-reason enum (A NFR-007), `enabled` defaulting to false so a second workspace on the same login must opt in (A OD-2), and a JSON config chosen because `tomllib` needs Python 3.11 (A OD-9, U-002). Its call bound `3 + 3N` equals E's (A NFR-005). What A gets right that E does not: a mechanical guard against same-login double polling, and a precise cancel transition.

**Variant B (root cause plus Project-first discovery).** Strongest form: three root causes RC1-RC3 (B §1.1) tie each design choice to evidence; discovery is the Project query itself, so "in a Project" and "Backlog" prune the candidate list before any per-issue call (B FR-004); approval reads the complete paged event list and fails closed at the page cap (B FR-007, FR-008); the executable probe that accepts only the `orca-cli` topic handles the GNOME screen-reader name clash (B FR-014, U-004); `re-approved` never resets attempts, so label toggling cannot bypass the cap (B OD-6, U-005). B is right that approval evidence must be complete, not first-page.

**Variant C (identity by node ID, SQLite).** Strongest form: node and account IDs survive renames (C §3, §7, U-007); consuming the slot and entering `unknown` is one durable transaction before any external I/O, and expiry never releases a consumed slot (C §7); an append-only transition table is written in the same transaction; a next-permitted-request time is persisted for rate limits (C NFR-004, U-009); absent evidence is never positive (C §3). C is right that the dispatch record is the safety core and deserves transactional semantics.

**Variant D (operations).** Strongest form: a runbook with a pre-flight, an exit-code action table, a 24-hour shadow `--dry-run` rollout, a kill switch, staleness detection at 900 s and SLOs (D §8, NFR-013, U-011, U-012). Its ambiguity rules are the most conservative: `pending_orphan` is abandoned and never relaunched, and `failed` relaunches only while `launches == 0` (D §7). It states "Default interactive mode, never a bypass mode" for the launched session (D OD-7), the only firm position on the largest residual risk. D is right that a poller nobody can see failing is a liability.

## Strengths claimed (variant E)

1. **Explicit call-budget model.** E §5 derives idle = 2 calls, worst = 1 + 1 + 10 x 3 + 1 = 33, and 12 cycles an hour = 24 calls (0.48 percent of 5,000) idle and 396 (7.9 percent) worst, and notes the allowance is per login so W workspaces on one login cost W times that. No other variant states the multiplier W; it turns the same-login rule (A-004) from a correctness footnote into a quantified cost argument (E O-4).
2. **Cost scales with candidates, not with Project size (U-014).** E FR-008 reads each examined candidate's own `projectItems`. A, B, D list Project items (A FR-006, B FR-004, D FR-007) and C paginates the Project (C FR-006). A Project also holds Done items and only grows, so a `-L 100` page stops covering it at some point; D concedes "Projects over 100 always fail" (D R3), and A and B fail closed at 100 (A FR-006, B §7.4). Dispatch then stops permanently whatever the Backlog holds. E has no such cliff.
3. **Cheap-first filter order.** E FR-004 drops candidates not assigned exactly to the own login before any per-candidate call, so 50 tagged issues of which 2 are mine cost 2 x 3 calls, not 50 x 3 (E FR-004 AC). No other variant specifies a prefilter ahead of the per-candidate reads.
4. **Hard per-cycle ceiling independent of bugs.** E NFR-005 caps `gh` calls at 35 and aborts remaining examinations (AC: 100 mocked candidates, at most 35 calls). A, C and D rely on `max_candidates` arithmetic alone.
5. **Rate-limit behavior that stops the damage.** E NFR-006 stops all GitHub calls on 403/429 and launches nothing (AC: limit on call 3 means exactly 3 calls). B R9 keeps reading per issue into a 403 storm (X-006).
6. **Launch spend is bounded in absolute terms.** The only paid event is a session. E FR-018 and NFR-012 cap it at 1 per cycle and 6 per day per workspace; A, B, C, D cap only per cycle, so a selection bug could cost up to 288 sessions a day per workspace. E §7 states the asymmetry: a duplicate launch costs a session, a missed one costs one `reset`.
7. **Ambiguity resolves toward not launching.** `pending` after its lease goes to `unknown`, `unknown` without an id goes to `abandoned`, `launched` with no claim goes to `abandoned` (E §7). This matches C and D on X-001 and X-002 and contrasts with B.
8. **Field minimization as a cost and security control.** E NFR-002 whitelists retained fields; E NFR-011 forbids any model-client import. Smaller payloads, no text in logs.
9. **State is bounded.** E NFR-013 prunes terminal records after 30 days and caps `considered` at 1,000. No other variant bounds ledger or `considered` growth.
10. **Per-issue record files** (E §7): a cycle reads and rewrites only the at most 10 records it touches, never a whole ledger, and a damaged file can block one issue rather than all.
11. **Honest scope of optimisations.** ETag requests are listed as follow-up and flagged UNVERIFIED (E §9) rather than baked into the contract.

## Weaknesses identified in others

1. **A, B, D: Project item-list as the sole Project source** has a permanent fail-closed cliff at 100 items (A FR-006; B §7.4; D R3). Raising D's limit to 500 (D R3) enlarges the payload on every one of 12 cycles an hour without fixing growth.
2. **C: full Project pagination every cycle** (C FR-006) makes cost linear in Project size, and C has no call ceiling; C NFR-008 only requires pagination calls to be counted in reporting, not capped.
3. **B: highest per-candidate cost.** 42 calls per cycle (B NFR-007: `2 + 4 x 10`) with two snapshots, events and comments per candidate, and no rate-limit stop (B R9).
4. **B: relaunch of a `launched` entry after lease with no marker** (B §7.3, X-001) can start a second session beside a possibly running first one, the most expensive failure, and contradicts B's own `max_launches` 1 (B §7.4).
5. **B: corrupt state loads as empty** (B NFR-010, X-003), which re-opens every pre-marker issue to a launch; a cost multiplier.
6. **A: `pending` found after lease becomes `failed` and is retryable** (A §7, X-002), and an unclassified launch failure also reaches `failed` (A FR-014, X-004); both permit a second session.
7. **A, B: label-only escape hatches** (A OD-5 `off`; B FR-022) change the meaning of "in a Project, Backlog" (X-005) to save a scope grant.
8. **C: SQLite plus explicit `init-state`** adds an operator step and a schema-migration surface to a job whose steady state is "two calls, nothing to do". Operator time is part of cost-to-serve. This is a cost, not a disqualifier (see Concessions).
9. **D: `rate_remaining` in every audit line** (D NFR-006) has no stated source; if it needs `gh api rate_limit` it adds a call to each idle cycle, contradicting "idle cycles make 2 calls" (D NFR-009).
10. **D versus A on the lock exit:** D exits 75 and feeds it into alerting (D FR-017, FU-4) while A exits 0 on `locked` (A FR-018). Neither prices a hung-cycle alarm against a benign overlap (X-007).

## Concessions (real weaknesses of variant E)

1. **Events are fetched with one unpaginated call** (E FR-006). The REST events list is oldest-first and paged; on an issue with a long history the "latest `labeled` event" may sit on a later page and E would judge on stale data. B (FR-007, FR-008) and C (§3) fail closed on incomplete history. E must adopt that rule. This is a safety gap, not a style one.
2. **A timeout is not classified.** E §7 defines `failed` as "definite error, no session started" and `unknown` only for `agent_session_operation_unknown` or a crash; a timed-out or malformed launch reply is left unmapped. C FR-011 maps it to `unknown`. E must do the same (X-004).
3. **Corrupt record handling is unstated** (E NFR-008 covers `gh` and `orca` output, not the record). A, C, D fail closed (X-003).
4. **The daily cap has no stored counter.** The record fields (E §7) hold no date or count; the cap must be derived by scanning `records/*.json`, which pruning bounds but E does not say. 6 per day is an unevidenced [PROPOSAL] and slows a legitimate drain to 6 issues a day.
5. **Label names `claim-ready` and `claim-approved` are not namespaced** (E O-1); A, B, D namespace theirs.
6. **`--agent <agent>` widens the fixed contract** (E FR-014, X-008); the seed says `claude`.
7. **The audit file has no rotation** (E FR-020); D rotates at 5 MiB (D NFR-006). A 300-byte line every 5 minutes is about 30 MB a year: small but unbounded.
8. **Module name `select.py`** (E §8) shadows a standard-library name; use `selection.py`.
9. **`reset <N>` mutates state with no stated lock or audit line** (E FR-023).
10. **Per-issue files are not atomic across files.** Only SQLite (C §7) gives one transaction for slot consumption, transition and daily count.
11. **GraphQL `projectItems` is itself unverified** (E R-5) and needs `read:project` like every other Project read; U-014 is a design hypothesis until the live test.
12. **Dropping unassigned issues before any call** (E FR-004) makes an approved-but-unassigned issue invisible (A-005); E cannot even count them without paying for a call.
## Shared-assumption responses

- **A-001 QUALIFY:** persistence of the state path must be checked by `check-config` before enabling; E's daily cap (E FR-018) bounds the loss if the record vanishes.
- **A-002 ACCEPT:** all variants gate enablement on the live test; E's 6-per-day cap bounds the cost of sessions that start but do not run the command.
- **A-003 QUALIFY:** the Project field and option and the dispatch key should use immutable IDs (C §7); label names fail closed when renamed. Resolving IDs costs calls unless cached, so cache them in `status`-visible state.
- **A-004 QUALIFY:** accept it as a scope limit and add A's `enabled=false` default (A OD-2); the cost of a violation is W times the call budget (E §5) plus duplicate sessions.
- **A-005 QUALIFY:** accept the rule but add an audit counter of dropped not-owned approved issues so the wait is visible; E FR-004 drops them before paying for a call.
- **A-006 QUALIFY:** treat a backward clock jump as "lease not expired" and test with a fake clock (C NFR-004).
- **A-007 QUALIFY:** the state path must be a local filesystem; `check-config` warns otherwise.
- **A-008 QUALIFY:** require actor type `User` plus the allow-list (D FR-006), and record the human-run-bot residual; actor type and id are free in the events payload.
- **A-009 QUALIFY:** safety does not depend on it in E, because an unclaimed `launched` becomes `abandoned`, never a relaunch; only liveness does. The live test must measure claim duration and set the lease from it.
- **A-010 QUALIFY:** `check-config` should require owner-only mode (0600) and refuse group- or world-writable allow-list files.

## Per-point positions

| Point | Level | Superior | Conf % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | A | 45 | Given/Then bullets map directly to tests (A §4) |
| S-002 | L1 | NONE | 60 | Count is not quality |
| S-003 | L2 | HYBRID | 60 | Take A's stages, B's root causes, D's runbook, E's budget |
| S-004 | L2 | E | 55 | Seven modules suffice; but rename `select.py` (concession 8) |
| S-005 | L3 | C | 50 | Only SQLite gives one transaction for slot, transition and count (C §7) |
| S-006 | L1 | NONE | 70 | ID scheme is cosmetic |
| S-007 | L1 | NONE | 60 | Traceability codes equivalent |
| S-008 | L1 | A | 40 | Table form is the easiest to review |
| C-001 | L3 | HYBRID | 45 | Namespaced names (A, D) resolved to IDs (C §7) |
| C-002 | L3 | HYBRID | 60 | C account IDs, D `User` type, B complete paging |
| C-003 | L3 | E | 65 | Per-issue `projectItems` avoids the 100-item cliff (E FR-008; D R3) |
| C-004 | L3 | NONE | 60 | All reduce to sole-assignee; C's ID match is the only difference |
| C-005 | L3 | A | 55 | `enabled=false` default is a mechanical guard (A OD-2) |
| C-006 | L3 | E | 55 | Prefilter then 35-call cap (E FR-004, NFR-005); add B's paging rule |
| C-007 | L3 | HYBRID | 50 | D's separate `attempts`/`launches` plus E's ambiguity rule |
| C-008 | L3 | E | 65 | Only E adds an absolute daily bound (E FR-018); value unevidenced |
| C-009 | L3 | A | 55 | `attempts -= 1` on cancel is exact (A §7); C is stronger but heavier |
| C-010 | L2 | B | 55 | `orca-cli` probe handles screen-reader clash (B FR-014); E's `--agent` widens |
| C-011 | L3 | C | 60 | Timeout maps to `unknown` (C FR-011); E leaves it unmapped |
| C-012 | L3 | NONE | 70 | All reach integer-only; property test (D) is cheap to add |
| C-013 | L3 | C | 50 | Account IDs plus Triage check (C §3); needs extra calls |
| C-014 | L2 | D | 55 | Only firm "never a bypass mode" (D OD-7) |
| C-015 | L3 | C | 55 | "Absent evidence is never positive" (C §3) |
| C-016 | L3 | HYBRID | 55 | E's stop plus hard cap with C's persisted next-request time |
| C-017 | L2 | D | 55 | Shadow dry-run and staleness check (D §8) |
| C-018 | L3 | D | 50 | Kill switch plus alertable lock exit (D FR-017); price the alarm |
| C-019 | L2 | HYBRID | 55 | D's rotation, E's `gh_calls` and `duration_ms` |
| C-020 | L2 | E | 50 | `check-config` and `status` help; `reset` needs lock and audit |
| C-021 | L2 | A | 55 | JSON avoids the 3.11 `tomllib` need (A OD-9) |
| C-022 | L2 | HYBRID | 50 | C crash injection, D reruns, E 50-cycle at-most-once |
| C-023 | L2 | E | 45 | ETag follow-up kept UNVERIFIED (E §9) |
| C-024 | L3 | A | 45 | Marker count with expired-pending handling (A FR-008/009) |
| C-025 | L2 | E | 50 | Whitelist plus `test_no_text` (E NFR-002) |
| X-001 | L3 | HYBRID | 70 | Only B relaunches; A, C, D, E abandon or never relaunch |
| X-002 | L3 | D | 50 | `pending_orphan` abandoned, never relaunched (D §7) |
| X-003 | L3 | HYBRID | 55 | Fail closed per A, C, D; B empty-reload re-opens every issue |
| X-004 | L3 | C | 65 | Timeout or malformed output gives `unknown` (C FR-011) |
| X-005 | L3 | D | 60 | No label-only flag (D OD-4; C FR-006) |
| X-006 | L3 | HYBRID | 55 | E's stop and cap with C's persisted wait; B's R9 is worst |
| X-007 | L2 | NONE | 55 | No variant prices alarm against benign overlap |
| X-008 | L2 | A | 70 | Seed fixes `--agent claude`; A keeps it |
