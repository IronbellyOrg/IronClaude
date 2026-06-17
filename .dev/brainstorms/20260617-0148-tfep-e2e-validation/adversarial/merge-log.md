# Merge Log — provenance of merged-requirements.md

| Merged section | Source | Provenance note |
|----------------|--------|-----------------|
| Conventions (worktree root, 5 files, 7-field set, enums, ignore-list, determinism rule) | A §0 + B non-determinism controls | A's conventions + B's `LC_ALL=C`/`--sort path`/digest rules |
| Coverage map (E1–E4 ↔ 4 dimensions, E3∩E4 `--fix` overlap) | A §coverage | unchanged from base |
| Test 1 (Residual + Sync) probes + criteria | A E1 + C TEST-01 negative (troubleshoot present) | A's falsification AC1.5/1.6 + C's "backend IS present" sanity (same idea) |
| Test 2 (Contract round-trip) | A E2 + B E2E-B2 exact-anchor probes + A's no-leak AC2.6 | A's 7×3 matrix + exactly-5 rows + B's byte-anchored enum/field-line probes + A's leak tripwire |
| Test 3 (Chain trace) | A E3 + B E2E-B3 anchor ladder + A's `FIX_TOTAL==FIX_PROHIBITION` | A's H1–H9 chain hops + B's exact branch-ladder line anchors + the count-equality `--fix` check |
| Test 4 (Safety invariants) | A E4 + B E2E-B4 (incident rebind, report-template rules) | A's freeze byte-diff + no-token-in-freeze + baseline-self-consistency, UNION B's incident/report coverage |
| Per-run evidence schema (verdict.yaml + findings.md, sha256, digest, criterion class) | C §3 + B common schema | C's 2-file split + B's sha256/digest/class fields |
| 3× execution + aggregation (12 runs, strict, DISAGREE, suite_failure_class) | A §1 + B aggregation + C orchestration | A's strict-12/12 rationale + B's digest gate + failure-class + C's batch spawn + aggregator subagent |
| roll-up.yaml + dashboard.md (4×3 + GREEN/RED) | C §4 | adopted wholesale |
| Human audit-trail (re-derivation-free) | A §2 | adopted wholesale |
| Orchestration prompts (spawner + aggregator) | C §1 | adopted, with B's absolute-path pinning |

**Conflicts resolved:** 0 hard conflicts. The only adjudication (verbosity vs operability) resolved by
taking A's rigor as the spec body and C's orchestration as the execution wrapper.

**Convergence:** 0.88 → PASS (≥0.65). No unresolved conflicts.
