# Diff Analysis: V2.0 Mention-Triggered Remediation Bot (3 variants)

## Metadata

- Generated: 2026-06-11
- Variants: 3 — V1 opus/architect, V2 sonnet/security, V3 haiku/devops
- Categories: structural (3), content (6), contradictions (4), unique (6), shared assumptions (3)

## Structural Differences

| # | Area | V1 architect | V2 security | V3 devops | Severity |
|---|------|--------------|-------------|-----------|----------|
| S-001 | Primary framing | Control-flow + component inventory (15 comps, SoT paths) | Threat-model first; attacker-goal organized | Ops runbook (systemd, deploy, alerting) | Medium |
| S-002 | Home for code | CLI group `src/superclaude/cli/remediate/` | Orchestrator + sandbox (host-side vs agent split) | Daemon module `superclaude.cli.bot_daemon` + `/opt/...` deploy | Medium |
| S-003 | Acceptance-criteria shape | AC-1..8 mapped to SC + OQ | SC-1,2,3,4,7 security-testable | Table mapped to V1.0 origins | Low |

## Content Differences

| # | Topic | V1 architect | V2 security | V3 devops | Severity |
|---|-------|--------------|-------------|-----------|----------|
| C-001 | **Execution host** | One-shot invoked runner (systemd timer), ledger-as-SoT, no inbound surface | **Split: minimal dispatcher (authz/idempotency, holds secrets) + one-shot sandboxed per-trigger runner** | Persistent daemon, in-memory round state + disk flush, ETag polling | **High** |
| C-002 | Autonomy levels | 2: propose(default)/fix | 5: propose/patch/fix/push/resolve; effective=MIN(...) | propose/fix + `--max-rounds` | High |
| C-003 | opComment delivery | Envelope, stdin, never shell-concatenated | **JSON data field, stdin, explicit "data not instructions", network deny-by-default** | SHA-256 + 120-char summary in ledger; raw never stored | High |
| C-004 | Round-state location | On-disk ledger (RAM "lies after restart") | Loop budget as one MIN operand | In-memory + periodic disk flush + SIGTERM drain | Medium |
| C-005 | Round commit ordering | **Commit AFTER act** (line 78) | (not explicit) | Ledger event per transition | High (→ INV-002) |
| C-006 | Re-review attribution | Counter keyed on thread_id, monotonic | Loop budget bounds | **SHA-correlation: head==push or descendant** (R1) | Medium |

## Contradictions

| # | Point of conflict | Position A | Position B | Impact |
|---|-------------------|-----------|-----------|--------|
| X-001 | Host shape | V1: one-shot for everything | V3: persistent daemon for everything | **High** — resolved by V2's split (watcher≠executor) |
| X-002 | Round commit ordering | V1: commit AFTER act (double-push risk) | Consensus draft: commit BEFORE act (counted-but-not-done) | **High** — neither safe; needs two-phase record (INV-002) |
| X-003 | Agent execution locus | V3: agent runs in-process in the daemon | V2: daemon must run NO agent in-process (high-value compromise) | High — V2 correct on security grounds |
| X-004 | Round-state durability | V3: in-memory round state | V1: RAM cursor lies after restart; disk is SoT | Medium — V1 correct |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V2 security | **Injection-as-data**: JSON-encoded opComment, never `/sc:troubleshoot "${opComment}"` shell interpolation | **High** (corrects the literal topic phrasing) |
| U-002 | V2 security | Authz bypass enumeration (sender from event not text; reject bots; TOCTOU re-check; mention-author-only) | High |
| U-003 | V2 security | Effective-level = MIN(parsed, authz, validation, needs_human, budget) monotonic composition | High |
| U-004 | V1 architect | 15-component inventory with SoT paths + build sequencing + parent-resolution via `in_reply_to_id` | High |
| U-005 | V3 devops | Concrete systemd unit (hardening), ETag/304 rate-limit, audit-ledger JSONL schema, alerting rules, deploy/rollback | High |
| U-006 | V3 devops | SHA-correlation to prevent false round advancement | Medium |

## Shared Assumptions (A-NNN — UNSTATED preconditions promoted)

| A-NNN | Assumption | Source agreement | Status |
|-------|-----------|------------------|--------|
| A-001 | A push-capable git credential is reachable somewhere in the fix-level execution path | All 3 assume push "just works" | **CONTRADICTED** by "GH_TOKEN absent from runner" (→ INV-001) |
| A-002 | The pre-push `uv`/`make` gate can run with the network it has | All 3 assume validation runs cleanly in sandbox | **CONTRADICTED** by deny-by-default + PyPI need (→ INV-017) |
| A-003 | `claude --dangerously-skip-permissions` is safe because the host omits `--fix` at propose level | V1+V3 lean on host discipline | **UNSTATED** — true only if no push credential reachable at propose (→ INV-007) |

## Summary

- Highest-severity items: C-001, C-002, C-003, C-005, X-001, X-002, X-003, A-001, A-002, A-003.
- The three variants **agree strongly on fundamentals** (reuse `ClaudeProcess` stdin; propose-only default; live authz; on-disk ledger; monotonic round counter; fork-only `--repo`; reply+resolve net-new; ephemeral checkout; lint+format+test pre-push gate; never log secrets) and **diverge primarily on host shape and autonomy granularity**. V2's split-host synthesis reconciles X-001. The invariant probe (Round 2.5) surfaced that the *agreement points themselves* (A-001..003) hide CONTRADICTED preconditions — the real risk was in the consensus, not the disagreements.
