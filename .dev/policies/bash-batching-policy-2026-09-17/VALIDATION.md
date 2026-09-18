# Validation — Bash Inspection Batching Policy

**Date:** 2026-09-17
**Requested invocation:** `sc-adversarial-protocol --compare POLICY.md,RISK-REGISTER.md --focus policy-soundness,risk-coverage`

## Execution record

1. The required `sc-adversarial-protocol` skill was invoked directly in Mode A with the requested compare files and focus areas.
2. The initial standard-depth orchestrator stopped before debate because its agent constraints prohibited the required Markdown outputs and Sequential was unavailable. It wrote a failure contract; no verdict was inferred from that failure.
3. Per the protocol's F1 fallback, the comparison was retried at quick depth with two parallel advocates and an independent invariant probe.
4. The quick retry produced diff, debate, invariant, base-selection, refactor, merge-log, merged-verdict, and return-contract artifacts under `adversarial/`.
5. Surviving findings were incorporated into `POLICY.md`; residual-risk grades and two cross-risk interactions were corrected in `RISK-REGISTER.md`.

## Merged verdict

**Conditional Pass.** The policy is sound as a latency optimization with strict eligibility and judgment boundaries. It is not a security boundary and is not mechanically enforced by the current repository.

### Surviving decisions

- Keep `N = 4`; trigger on the fifth **serial** eligible call.
- Batch planned known reads prospectively, before the first call.
- Do not batch mutations, interactive commands, semantic dependencies, network/remote/recursive/streaming work, or dynamic shell.
- Use continue-and-report with isolated blocks, markers, explicit aggregate rc, and setup fail-fast.
- Use one private `mktemp -d` script per bounded chunk, created/executed/cleaned in one Bash call.
- Do not ship a hard fifth-call hook. A future counter is an advisory mechanical proxy only.

### Findings incorporated into `POLICY.md`

| Finding | Incorporated change |
|---|---|
| Mechanical transcript streaks differ from semantic waves | Evidence qualified; rollout measures both populations |
| Same-turn parallel Bash already removes RTT | Explicit exemption |
| Late singleton fifth call creates a pointless script | Singleton exception when discovery was genuinely late |
| Judgment boundary/reset definitions diverged | Any interpretation before next action resets the wave |
| No snapshot isolation | Consequential facts require individual calls or revalidation |
| One-script rule conflicted with 15-command cap | One script per chunk plus checkpoint |
| Footer could report failure but exit zero | Explicit marker accounting and `exit 0`/`exit 1` |
| Predicted caps were not enforced | Aggregate/per-command timeout and output truncation contract |
| “Secure `/tmp`” was underspecified | `umask 077`, `mktemp -d`, exact cleanup, cleanup-failure marker |
| Inline visibility was treated too strongly under bypass | Audit-only wording and simple-command subset |
| Hook could not count completed calls | Completion-event requirement and proxy labeling |
| Freshness and subagent multiplication | Required tracked `Read`; threshold applies across delegated wave |
| Prompt guidance called enforceable | Renamed normative guidance; active SoT wiring remains future work |

## Remaining risk

One High residual remains intentionally visible: without a mechanical validator, trusted structured runner, or read-only sandbox, unattended `bypassPermissions` execution cannot prove that a generated script is read-only. The revised policy responds by restricting unattended batches to a simple fixed-command subset and requiring individual calls otherwise. This is risk containment, not proof.

## Evidence and metrics

- Incident: 20 read-only calls, 112 seconds agent wall time, 0.048-second replay.
- Implied average: 5.6 seconds per agent call versus about 2.4 ms local execution per inspection.
- Transcript sample: newest 45 JSONL transcripts available during analysis, 322 Bash events, 184 mechanical streaks; 97% length 1–4; 5–6 streaks crossed four.
- Existing freshness-hook pattern benchmark: 100 runs in 3.209 seconds, about 32 ms each. Hook CPU cost is negligible relative to 5–19-second agent round trips; semantic false positives are the real concern.

## Artifact index

- `POLICY.md` — revised proposed guidance
- `RISK-REGISTER.md` — ten risks with alternative mitigations
- `adversarial/merged-verdict.md` — merged verdict
- `adversarial/adversarial/diff-analysis.md`
- `adversarial/adversarial/debate-transcript.md`
- `adversarial/adversarial/invariant-probe.md`
- `adversarial/adversarial/base-selection.md`
- `adversarial/adversarial/refactor-plan.md`
- `adversarial/adversarial/merge-log.md`
- `adversarial/return-contract.json`
