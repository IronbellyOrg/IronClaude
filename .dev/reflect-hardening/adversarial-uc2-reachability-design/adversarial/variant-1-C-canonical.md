# Variant 1 — Position: C is the canonical UC-2 reachability GATE (owns contract 1.6.0)

<!-- Source: design position extracted from EXISTING_MATRIX rows M-028..M-031, M-042; Tasklist C TASK-RF-uc2-reachability-gate-20260620-043410 -->

## Thesis

The canonical `sc-reflect-protocol` UC-2 reachability capability is **Tasklist C (FR-RH1 contracted-sink reachability gate)**. It owns `contract_version: "1.6.0"` and the Wave 1A Step 5.6 gate. Tasklist B's runtime-surface detector is preserved as a complementary, *later*, *advisory* capability — not discarded, but not co-owner of 1.6.0.

## Design summary (C)

- **Detection question:** "For a requirement that asserts a durable side-effect through an *explicitly contracted* sink (`durable_sink:` / `@sink`), did a *real boot* actually observe the sink?"
- **Proof bar (high precision):** ONLY a real boot that observes a contracted sink absent can set `unreachable` / **Regression**. Static binding absence, discarded result, unresolved sink, oracle mismatch, or real-boot-unavailable can set `unproven` *only* when a blocking annotated sink exists. `--no-reachability` and spec/tasklist-absent are telemetry-only skips (no Grounding Gap, no status effect, no `needs_human_decision`). Semantic fallback is advisory only.
- **Contract:** additive `1.6.0` with 7 stable R7 fields (`reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`, `reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, `reachability_skip_reason`); `1.5.0` preserved D13-only.
- **Completeness shipped now:** wrapper plumbing (`--reachability/--no-reachability` through commands/reflect.md + cli/reflect/{models,config,commands,runner}.py + docs guide), consumer fixtures + producer eval cases, bounded cost profile, docs parity test, PRE reflect coverage 1.0.

## Why this should be the gate

1. **Gate role demands high precision.** A verdict that can *block* (Regression) must almost never be wrong. C's real-boot-only bar guarantees precision; false Regression is structurally impossible from static ambiguity.
2. **Attacks sc-reflect's worst failure mode directly** — false PASS on a claimed-but-never-executed durable effect ("the test is green but the side-effect never happens in a real run").
3. **Most complete artifact today** — full operator surface, docs parity, bounded cost, producer+consumer evidence, and an independent PRE reflect gate at coverage 1.0.
