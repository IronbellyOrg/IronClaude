# Bun vs Node.js — Backend Runtime Evaluation (Adversarial Merged Output)

This is the adversarial pipeline's merged output, prior to brainstorm-owned canonical normalization. The brainstorm normalization layer copies this content into `../merged-requirements.md` and applies the canonical contract (frontmatter, six required sections, fit-to-intent gate).

## Decision context

Compare Bun and Node.js as runtimes for backend services and produce a workload-scoped decision (adopt / pilot / defer / reject) grounded in deep external research.

## Six comparison axes

1. Runtime architecture
2. Performance (throughput, startup, memory, tails)
3. Ecosystem & library compatibility (incl. native modules, APM agents, FaaS hosting)
4. Operations & supportability (LTS, security, vendor support)
5. Tooling & developer experience
6. Risk

## Workload-scoped recommendation pattern

- **Adopt** where: workload is greenfield, latency-sensitive, dependencies are pure-JS / pure-TS, hosting environment supports Bun as first-class.
- **Pilot** where: workload is bounded in blast radius, performance / DX gains are measurable, native modules / APM agents have been validated.
- **Defer** where: workload is mission-critical, depends on niche native modules or specific APM agents lacking Bun support, or is hosted on a managed FaaS without Bun runtime.
- **Reject (for now)** where: hard regulatory or LTS / patch-cadence requirements cannot be met by the current Bun release posture.

## Pilot exit criteria (when pilot is selected)

- Performance: target workload's p50 and p99 latency at or better than current Node baseline at equivalent infrastructure.
- Compatibility: 100% of critical native / APM / observability dependencies validated.
- Operability: pager / runbook / incident-response coverage equivalent to Node baseline.
- Time-bound: explicit pilot window (e.g., one calendar quarter) with documented decision review.

## Risk register (summary)

- Ecosystem-compatibility risk — native and observability tooling parity.
- Operational maturity risk — younger runtime, no Node-equivalent LTS commitment.
- Tooling coverage risk — debugger / profiler / APM agent gaps.
- Hosting risk — managed FaaS support varies.
- Talent / hiring risk — Bun-specific operational experience rarer.
- Lock-in risk — Bun-only APIs increase switching cost.
- Mirror risk on Node — DX / cold-start / install-speed advantages forfeited if Node is retained without revisiting workflow.

## Open questions

- Which specific backend workload classes is the team evaluating Bun for?
- What is the team's adoption-risk tolerance and evaluation horizon?
- Are there specific native modules / APM agents that gate adoption?
- Are managed FaaS platforms in scope, or is container deployment acceptable?

This file is the adversarial pipeline's pre-normalization output. The canonical brainstorm spec is `../merged-requirements.md`.
