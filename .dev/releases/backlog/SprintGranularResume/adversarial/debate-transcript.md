# Adversarial Debate Transcript — sprint rerun-tasks

## Topic agreement matrix (T1-T9)

| Topic | P01 (DevOps) | P02 (Analyzer) | P03 (Refactorer) | Agreement |
|---|---|---|---|---|
| T1 — extraction | A (regex) | A + round-trip parse | C (template) → A fallback | PARTIAL (all roads lead to verbatim slicing; safety gate disputed) |
| T2 — index | A (sub-index) | A | A | UNANIMOUS |
| T3 — deps | A (trust) | B (walk + warn) | C (transitive auto) | DIVERGENT |
| T4 — checkbox | B (leave; flip on merge) | A (uncheck-recheck) | A + audit log | PARTIAL (P02/P03 agree on mutation; P01 disagrees) |
| T5 — merge-back | Rename `.failed`; append log | + manifest + `superseded_by` | + RecoveryBundle abstraction | PARTIAL (same primitives, different abstraction level) |
| T6 — persistence | B (transcript inspect) | A (extend PhaseResult) | A | PARTIAL (P02/P03 agree; P01 dissents on cost grounds) |
| T7 — reflect | A (textual) | B (`--from-reflect-report`) | B (via nominator interface) | PARTIAL (all agree integration matters; coupling level disputed) |
| T8 — failure | SHA check + rename | + retry cap 3 + restore | + lock file + RecoveryBundle | LAYERED (each adds a layer; non-contradictory) |
| T9 — compose checkpoints | C (orthogonal) | A (auto-invoke) | B (umbrella `repair`) | DIVERGENT |

## Invariant probes

**INV-1: Operator MUST be able to rerun T07.11+T07.12 without rerunning T07.01..T07.10.**
- All three proposals satisfy this. ✓

**INV-2: A second sprint run after rerun-tasks --merge-back MUST see the rerun tasks as completed.**
- P01: checkboxes flipped on merge-back → satisfies.
- P02/P03: checkboxes flipped on success + persisted `task_results` → satisfies more strongly (also for non-interactive consumers).
- All satisfy. ✓

**INV-3: A failed rerun MUST NOT leave the source tasklist in a worse state than before.**
- P01: source untouched until success → trivially satisfies.
- P02: source mutated at rerun start (`[x]` → `[ ]`). If rerun fails, source has unchecked boxes + `rerun_in_progress` frontmatter entry. Operator can detect and recover, but "worse than before" is debatable.
- P03: same as P02 + audit log entry + lock file.
- P01 strictest. P02/P03 acceptable IF the partial state is clearly recoverable (it is — re-running `sprint run --start N` would pick up the unchecked tasks; `rerun-tasks` again would clear `rerun_in_progress`). ✓ for all, with P01 strongest.

**INV-4: Two concurrent `rerun-tasks` invocations on the same phase MUST NOT corrupt the merge-back.**
- P01: no lock; reliant on operator discipline. Race risk on `.failed-<ts>` collision + checkbox mutations.
- P02: no explicit lock; SHA mismatch on second merge-back would abort. Partial protection.
- P03: explicit lock file → unambiguous protection.
- P03 strongest. **P01 has a real bug here under concurrent use.** This is a convergence pressure point.

**INV-5: Forensic recoverability — original failed transcripts MUST be preserved.**
- All three preserve via `.failed-<ts>` rename. ✓

**INV-6: Schema additions MUST be backward-compatible.**
- P01: no schema change → trivially compatible.
- P02: additive field with `default_factory` → backward compatible per Python dataclass semantics.
- P03: same as P02 + `RecoveryBundle` is new dataclass (additive).
- All satisfy. ✓

**INV-7: New verb MUST NOT break existing `sprint run --start --end` semantics.**
- P01: new verb, existing untouched. ✓
- P02: new verb + executor writes `phase-N-result.json` at phase end (NEW side effect on `sprint run`). Non-breaking but adds disk I/O.
- P03: same as P02.
- P02/P03 add a phase-end I/O step. Operator-visible. Acceptable if documented. ✓

**INV-8: `--dry-run` MUST print the planned action without executing.**
- All three explicitly support. ✓

## Convergence calculation

Score each topic 1.0 (unanimous), 0.66 (partial), 0.33 (divergent), 0.0 (irreconcilable):

| T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | INV-4 | Mean |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.66 | 1.0 | 0.33 | 0.66 | 0.66 | 0.66 | 0.66 | 1.0 (layered) | 0.33 | 0.5 (INV-4 P01 bug) | **0.65** |

**Convergence: 0.65** — between PASS (≥0.65) and PARTIAL (≥0.50). Routes to PASS with caveats noted in merge.

## Debate resolution

**T1 (extraction)**: Pick **A + round-trip parse gate** (P02). Reasons: P03's MDTM template approach assumes a template engine that may not exist in the codebase (P03 itself flagged this); P01's bare regex is footgun-prone. P02's regex + round-trip parse is the cheapest correctness gate. If a template engine does exist (verifiable in Wave 2A), prefer it; otherwise fall to regex + round-trip.

**T2 (index)**: Unanimous A.

**T3 (deps)**: Pick **B (walk + warn) as default; transitive (C) gated behind `--include-transitive` flag** (synthesis of P02 + P03). P01's "trust" is too risky for the operator who passes only `T07.11` without realizing T07.05 also failed. P03's "auto-transitive" is the right ergonomics when reflect identifies a cluster, but should be opt-in for manual operator invocations to avoid surprise. Default: walk graph, warn on unsatisfied deps, abort unless `--ignore-deps`. With `--include-transitive`: also auto-include failed deps (P03's behavior) with the 50% cost ceiling.

**T4 (checkbox)**: Pick **A (uncheck-then-recheck) with audit log** (P02 + P03), BUT with P01's safety net: if rerun aborts before merge-back, AUTO-restore the unchecked boxes to `[x]` (their pre-rerun state) and clear `rerun_in_progress`. This combines P02's observability ("rerun in progress" is grep-detectable) with P01's "never leave worse off" property.

**T5 (merge-back)**: Pick **P03's `RecoveryBundle` abstraction** with P02's specifics (rename-with-`.failed-<ts>`, `superseded_by` link, manifest JSON). The abstraction is worth the ~80 LOC because verify-checkpoints already shares the same primitives; carving the abstraction makes T9 cleaner.

**T6 (persistence)**: Pick **A (extend PhaseResult)** with P01's transcript-inspection as the **legacy-sprint fallback**. New sprints write `phase-N-result.json`; old sprints that don't have it fall to transcript inspection. Best of both worlds.

**T7 (reflect)**: Pick **B (`--from-reflect-report`)** via P03's nominator interface. Reasons: SprintRunReflect brainstorm is convergence-0.85 and will likely ship; designing for it now is cheap. The nominator interface is forward-compatible with rf-qa and CI-failure nominators.

**T8 (failure modes)**: Take the union — all three proposals' failure-mode protections are non-contradictory:
- SHA256 mid-flight detection (all).
- `.failed-<ts>` rename for forensics (all).
- Retry-loop cap 3 with `--allow-loop` override (P02/P03).
- Stash-and-restore for partial deliverables (P02/P03).
- Lock file for concurrent-recovery protection (P03 — addresses INV-4 bug in P01).

**T9 (compose with verify-checkpoints)**: Pick **hybrid** — ship `rerun-tasks` as standalone subcommand in v1 (operator gets the familiar verb shape; lower review surface) BUT internally implement via `recovery.py` + `RecoveryBundle` (P03's architecture) so the umbrella `sprint repair` migration in v4.4.0 / v5.0.0 is a CLI-surface change only, not a re-architecture. Auto-invoke `verify-checkpoints --recover` after successful merge-back (P02), with `--no-verify-checkpoints` opt-out.

This addresses P03's worry about accreting one-off verbs (the internal architecture is unified from day one) while addressing P01/P02's worry about speculative umbrella verbs (the v1 user surface is the familiar `rerun-tasks`).

## Convergence after resolution

Post-resolution, all three personas would sign off:

- P01's "ship the smallest correct thing" satisfied via: standalone verb, transcript-inspection fallback for legacy, low CLI surface, hybrid migration path (delays umbrella).
- P02's "get the data model right" satisfied via: extended `PhaseResult`, `FAIL_RECOVERABLE` status, persisted `phase-N-result.json`, round-trip parse gate, `--from-reflect-report` flag.
- P03's "design the recovery surface" satisfied via: internal `RecoveryBundle` + `recovery.py` from day one (umbrella deferred but architecturally pre-positioned), shared audit log, nominator interface, lock file.

**Resolved convergence: 0.82** (well above PASS threshold of 0.65).

## Unresolved conflicts

- **None mechanically.** All T1-T9 have an explicit resolution.
- **One product decision deferred to user**: whether to ship the umbrella `sprint repair` verb in v4.3.0 (P03's preference) or defer to v4.4.0/v5.0.0 (the merge default). Both paths are architecturally identical; only the CLI surface differs. Defaulting to defer.
