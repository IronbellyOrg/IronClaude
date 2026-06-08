# Risk Register — Mastra + Backlog.md + Beads Port

**Date:** 2026-06-03
**Source:** `FEASIBILITY-STUDY.md` Sections 4, 6, 7, 9.C (and `synth-06-risk-questions-evidence.md`). Condensed planning extract; the full study is authoritative. No risk here is invented beyond the validated report.

**Severity** = combined Impact × Likelihood (High / Medium / Low). **Likelihood** reflects current evidence strength, not a forecast. **Owner / Decision Gate** names where the risk must be resolved before it propagates into implementation.

---

## Risk Register

| # | Risk | Source Evidence | Impact | Likelihood | Severity | Mitigation | Owner / Decision Gate |
|---|---|---|---|---|---|---|---|
| R1 | **License risk** — production multi-user RBAC/SSO/FGA/audit/on-prem are Mastra Enterprise-licensed (`ee/` directories), not Apache-2.0 core. | `web-01 §6,§10`; seed-brief Known Context. | High (cost + lock-in for the strategic multi-tenant driver) | High | **High** | Separate local/OSS vs team/EE tracks; confirm EE pricing/terms (Q6); keep OSS-only features usable single-tenant. | Owner + vendor, before any hosted multi-tenant build (Q6). |
| R2 | **Language/runtime migration** — ~65K-LOC Python orchestration must replatform onto Mastra's TypeScript step/workflow model; the `ClaudeProcess` subprocess seam must be replaced. | seed-brief Problem Statement; `research/08:38-70`; `web-01 §2-3`. | High (large rewrite; gate/convergence logic is pure Python) | Medium-High | **High** | Strangler-fig phased roadmap; port Markdown/YAML harness first; rebuild gate/wave/checkpoint loops as Mastra control flow; prototype before committing. | Architecture owner; runtime-seam spike gate (Q5/SG1). |
| R3 | **Backlog.md / Beads overlap** — both can act as task store; dual task/status owners cause drift. | seed-brief Known Context; `research/07`, `research/11:100`; `web-02 §13` (integration immature, maintainer #588). | High (data integrity / single source of truth) | Medium (avoidable with clear split) | **High** | Assign canonical owners per data class (Q1: Backlog.md = prose work-of-record, Beads = graph/memory/gates); start with one narrow sync workflow; do not assume native integration. | Owner (Q1 / decision D1). |
| R4 | **Beads / Dolt version churn** — v1.0.5 carries "do not upgrade" sync warnings; migration `0043` can silently break multi-machine `bd dolt` sync; v1.0.4 had a server-mode data-clobber regression. | `web-03 §2` (issue #4259, #3870); `web-03 §15`; seed-brief (now corrected: Beads is Dolt-first, not SQLite/JSONL, `web-03 §7`). | High (data loss / corruption in multi-writer sync) | Medium (only if upgrades unpinned/ungated) | **High** | Pin and gate Beads versions; avoid gated/pre-release builds; require `bd doctor` + backup/restore + push/pull smoke tests in adoption gates. | Platform/ops owner; version-pin gate (D5). |
| R5 | **Concurrency / multi-writer** — Beads embedded mode is single-writer ("database is locked"); multi-agent needs Dolt server/shared-server mode; session attribution is actively changing. | `web-03 §8-9` (issues #3400/#3583); `web-02 §12` (Backlog.md is file/lock-based, not transactional multi-user). | High (parallel/multi-agent orchestration correctness) | Medium-High (default embedded mode insufficient) | **High** | Require Beads server/shared-server mode for any multi-agent writer; enforce atomic `bd update --claim`; one-task-per-agent/session discipline; track session-attribution fixes. | Architecture owner; concurrency-model gate (D5/G4). |
| R6 | **Subprocess / hook safety parity** — Mastra Workspace `executeCommand` does NOT replicate Claude Code hooks, freshness checks, staging restrictions, or permission prompts; SuperClaude safety rules (UV-only, git safety, `.claude/` SoT, fork-PR target) must be rebuilt. | `web-01 §3`+limitation 3, rec 5; `research/11:111,123`; `gaps RG-I5`. | High (safety regression: unsafe execution, lost guardrails) | High (parity not provided by Mastra defaults) | **High** | Safety spike before assuming CLI parity (Q5/SG1); reimplement hook policies as Mastra middleware/guards; preserve SuperClaude governance outside Mastra defaults. | Security/architecture owner; safety-spike gate (Q5). |
| R7 | **Checkpoint contract + roadmap wiring drift** — stale prompt/template/docs reference legacy `### Checkpoint:`; per-task executor branch skips `_verify_checkpoints()`; certify gate may not be wired in production; trailing gate grace=0 forces blocking. | `research/09:98-109,158-172` (RG-C2); `research/02`, `research/11:66-67`. | Medium-High (silent loss of checkpoint/gate enforcement on port) | Medium (real in docs/prompt; runtime parser already handles both shapes) | **Medium-High** | Adopt canonical numbered-checkpoint contract; emit `Checkpoint Report Path:` lines; align stale prompt/template/docs; state effective-vs-intended behavior separately (Q8, Q12). | Implementation owner; checkpoint/parity gate (Q8/Q12). |
| R8 | **Governance / tenancy / cost gaps** — Mastra+Backlog.md+Beads provide no tenant isolation, no per-invocation audit, no cost attribution, no policy/approval/catalog control plane; MCP is a protocol, not governance. | `web-04 §1-15`; `research/07`, `research/11:99`. | High (blocks safe company-wide multi-tenant deployment) | High (none of the three tools supplies this) | **High** | Add a dedicated governance/control-plane service (tenant registry, identity mapping, RBAC/ABAC, tool catalog, audit log, cost/budget metering) + MCP/AI gateway (OAuth 2.1, audience validation, scoped tools, no token passthrough). | Owner + security; governance-plane gate (Q2/D3/G4). |
| R9 | **Reliance on fast-moving external tools** — Mastra (`@mastra/core` 1.1.0+, Temporal integration experimental), Backlog.md (v1.45.2, MCP MVP + doc drift + open browser state-loss bug #578), Beads (1.x, frequent CLI/API changes) are all rapidly evolving. | `web-01 §1,§9`; `web-02 §5,9,10,11`; `web-03 §15`. | Medium-High (breaking changes, doc/schema drift mid-build) | High (all three pre-mature/fast-moving) | **Medium-High** | Pin versions; runtime-verify MCP instruction/schema surfaces; avoid experimental runners (Temporal); prefer stable contracts (`bd --json`, Backlog CLI/MCP); budget for churn; no migration without hands-on validation. | Platform owner; version-pin + validation gates per tool. |

---

## Severity Summary

- **High (6):** R1 (license), R2 (runtime migration), R3 (Backlog/Beads overlap), R4 (Beads/Dolt churn), R5 (concurrency/multi-writer), R6 (subprocess/hook safety), R8 (governance/tenancy/cost).
- **Medium-High (2):** R7 (checkpoint/wiring drift), R9 (fast-moving external tools).

Note: R1–R6 and R8 are High; R7 and R9 are Medium-High. (Seven High + two Medium-High.)

## Critical-Gap Linkage (from Section 4)

The four **Critical** gaps cluster into two areas and map to these risks:
- **Runtime seam + Claude-Code-native safety that cannot be assumed-portable** — Gap G3 (subprocess/Claude-Code parity) ↔ R2/R6; Gap G4 (hook/safety parity) ↔ R6.
- **Multi-tenant governance layer that does not exist in current code and is not supplied by the three components** — Gap G6 (tenant state) ↔ R8; Gap G7 (auth/RBAC/governance/cost) ↔ R1/R8.

## Open-Question Cross-Reference

R1↔Q6, R2↔Q5/Q11, R3↔Q1, R4↔Q10, R6↔Q5, R7↔Q8/Q12, R8↔Q2, R9↔Q10. (See `FEASIBILITY-STUDY.md` Section 9 for the full open-questions tables.)

## Seed-Brief Required Coverage

The seed brief's mandated risk classes are satisfied: **license drift** → R1; **Backlog/Beads data-model overlap** → R3; **loss of Claude-Code-native features** → R6; **multi-tenant security** → R8. Plus concurrency (R5), version churn (R4), parity/contract drift (R7), and external-tool volatility (R9).
