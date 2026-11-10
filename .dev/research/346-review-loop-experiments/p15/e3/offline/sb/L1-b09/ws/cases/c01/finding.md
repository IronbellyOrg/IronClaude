### F-9. MAJOR label, graded Medium. The task confidence gate does not say whether an explicit `--compliance` override clears it.
- Expert: Wiegers.
- Locations: `SPEC:121`; `INV-B:199` (the gate text offers "Override with `--compliance [tier]`").
- Grading check: undefined edge case (Boundary Table G5, last row). A brief that already passes the flag would still block.
- Recommendation: state that an explicit tier flag clears the gate.
- Priority: Low.

=== ARCHITECTURE ANALYSIS ===

- Fowler (interfaces): the core decision (Orca on top, commands unchanged units, one shared contract file, `SPEC:16`, `SPEC:52`) is sound and supported by `CAPS:97-103` (depth 1 forbids the alternative) and `CAPS:145-149` (standalone use). `--unattended` bundles five behaviors (gate defaults, outward-off, report write, wait splitting, mode flag) behind one switch. That is acceptable, and it is why F-4 and F-7 matter: the bundle only works if all five arrive together.
- Newman (versioning): the shared contract has no version field (N-5), while the workflow contract is already versioned 1.1 (`INV-B:272`). The contract file will evolve across four phases.
- Hohpe (message flow): the `ask`, `reply`, `check` and `worker_done` flow in WC-3, WC-5 and WC-12 matches `CAPS:58-67` and `CAPS:73-77`. One gap: a blocked command maps to `--outcome failed` (`SPEC:63`), which keeps the Task's dependents blocked (`CAPS:90`) and needs a `--retry-of` start; the spec does not say that is the path (see F-2).
- Nygard (failure modes): the readiness, nesting and silent-stall analysis in 1.4 is accurate against `CAPS:52`, `CAPS:129` and `CAPS:97-103`. Open: stale contract after a crash (F-2), heartbeat during unsplittable calls (F-5). A worker's own `failed` report does not trip the circuit breaker (`CAPS:80`), so a blocked-then-retry loop has no automatic stop; this is a note, not a finding, since the loop is the coordinator's.
- Hightower: no cloud-native concern beyond the above. The remote-worker choice is excluded (`SPEC:221`).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`SPEC:62`)** fails when **`--unattended` is passed with no output directory**. Concrete attack: before, `/sc:analyze x --unattended`; the command must write `blocked` or `failed` to `<output-dir>/return-contract.yaml`, but there is no directory; after, no file exists, the worker reports `failed` by WC-5 with no reason for the coordinator to read. Severity: MAJOR label, Medium (F-1).
2. I can break this specification by **Divergence Attack**. The invariant at **WC-4 versus `SPEC:83` and `SPEC:92`** fails when **the coordinator passes `--output D` to adversarial**. Concrete attack: WC-4 says `D/return-contract.yaml`; the adversarial row says `D/adversarial/return-contract.yaml`; the coordinator reads the first, the command writes the second; step 4 (`test -s`) fails on a correct run. Severity: MAJOR label, Medium (F-1).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **`status` holds `partial`**. Concrete attack: a sprint-style command finishes 1 of 5 pieces and writes `partial`; WC-5 sends `--outcome succeeded`; Orca marks the Task completed (`CAPS:77`) and its dependents become ready (`CAPS:90`). Severity: MAJOR label, Medium (F-6).
4. I can break this specification by **Sequence Attack**. The invariant at **P1 (`SPEC:159`) before P2 (`SPEC:160`)** fails when **a coordinator dispatches a command in between**. Concrete attack: after P1, `/sc:auggie-review <PR> --unattended` is accepted; the post-to-GitHub default is still on until P2; a review is posted although WC-9 says it is off. Severity: MAJOR label, Medium (F-4). Second attack: retry into the same directory (F-2).
5. I can break this specification by **Accumulation Attack**. The invariant at **AC-1.1 (`SPEC:195`)** fails when **the section count is accumulated across 37 commands**. Concrete attack: 37 sections expected, `load` contributes none, 36 exist, P1 never passes. Severity: CRITICAL (B-1).
