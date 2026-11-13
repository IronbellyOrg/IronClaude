## Round 2: Rebuttals

### Variant 1 Advocate (sonnet class), sequential position 1

- Concedes F1 (stale `cycle_id`) is a spec ambiguity the plan inherits: no fold row sets `cycle_id` on any request (spec 186-206); downgrades from "bug" to "required spec clarification"; plan still pins nothing for it (Task 3 ACs).
- F5 partly conceded: needs `published` and an `ambiguous` dangling branch together (two pushes, or a stale id as in F1); row order (spec 166 before 167-168) is real.
- F6 and F7 conceded as low value (MINOR). INF-021 "covered" conceded: V1 did not check AC gaps.
- V2 F1 is half a gap: Task 8 body names "this cycle's applied-edit count" (plan 124), Task 3/4 tests `applied_edits=0` after a fixing cycle (plan 75), but Task 8's ACs never check the call-site count.
- F4 is fail-safe but a dead end: engage row 6 (spec 138) never re-checks live draft; resume row 8 does.
- Blocking: F1 no; F4 no (MAJOR); F5 yes (only finding that can bypass a hold on an ambiguous tip; MAJOR non-blocking if the owner reads the row order as intended); V2 F1 no (MAJOR).
- Shared assumptions: A-001 ACCEPT, A-002 ACCEPT, A-003 QUALIFY. S-001: layout only.

### Variant 2 Advocate (haiku class), sequential position 2

- Concedes blocking on F1 is overstated (plan 75 and 166 name the zero-edit-after-fixing case; the gap is the caller). Concedes F2 label inconsistency; narrows to "a changed tail still passes" (plan 154, spec 377); pins not read, coverage unverified. Concedes missed C-001 and C-004. C-002 real but Medium (plan 124 restates event-append and script steps).
- Plan 75 tests the function with an input count; plan 166's driver supplies its own count; no test drives the protocol caller. Three of the 8 quote flags (plan 75, spec 107, spec 366) are stripped backticks; five unchecked.
- A wrong count fails closed: zero-edit push blocked (spec 276); with the run-wide count, release row 9 (spec 157) holds and the PR stays draft.
- V1 F5 bounded: release row 8 (spec 156) still requires `head_sha == target_sha`; the spec never says where resume gets `target_sha`.
- Claims V1 F4 contradicts the spec's engage-failure trace (spec 68, 274).
- Blocking: V2 F1 drop to MAJOR non-blocking; V1 F5 drop to MAJOR non-blocking once the plan names the `target_sha` source; V2 F2 MAJOR non-blocking; keep V1 F4 blocking.
- Shared assumptions: A-001 QUALIFY, A-002 ACCEPT, A-003 QUALIFY. S-001: layout only, Low.

### Variant 3 Advocate (opus class), sequential position 3

- Concedes "assigned rows covered" has no row-by-row evidence and that the Task 10 dependency concern was noticed but not raised.
- Checks V2's claim on V1 F4: the engage-failure trace ends in `terminal_halted` with no edit (spec 274); engage row 6 (spec 138) is not reached on that trace. F4 not blocking.
- Task 10 consumes Task 8's ref; spec 363 requires a `Depends on:` line for every consumed task; Task 9's dependency on Task 8 orders them transitively but does not meet the explicit instruction.
- Blocking: F4 no; F5 no (row 4 requires `landed` or `published`; the ambiguous-tip bypass is not established by the stated conditions); F1 no (ambiguity inherited); V2 F1 no (fails closed); V2 F8 no (MINOR).
- Shared assumptions: A-001 QUALIFY, A-002 ACCEPT, A-003 ACCEPT. S-001: V3's layout cleaner, low impact.

## Round 2.5: Invariant Probe (fault-finder, sonnet class)

See `invariant-probe.md`. One HIGH-severity UNADDRESSED item (INV-001) blocks convergence under the AD-1 gate; no Round 3 runs at depth standard.
