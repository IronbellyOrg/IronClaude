# Iteration 2 Analyst Notes

## What changed since iteration 1

**Skill edits** (committed to `src/superclaude/skills/sc-auggie-review-protocol/`):

1. **Wave 2 "Common pitfalls" callout** — explicit warnings on `--output-format json` (NOT `--json`), JSON-fence stripping with `sed`/`jq`, `--instruction-file` requires real path, `--workspace-root` must be repo root, and indexer cold-start retry.
2. **`refs/auggie-prompts.md`** — preamble acknowledges Auggie wraps JSON in markdown fences and the orchestrator strips them.

**Eval edits** (in `iteration-2/`):

1. **3 new discriminating assertions** (apply to `with_skill` only, N/A on baseline):
   - `audit-log-records-grounding` — proves Wave-3 grounding decisions were logged
   - `skill-machine-summary-header` — checks `<!-- SC:AUGGIE-REVIEW:SUMMARY ... -->` footer
   - `skill-auggie-raw-artifact-present` — globs for `auggie-raw*.json` / `auggie-parsed*.json` / `auggie-findings*.json`
   - `audit-log-no-approve-flag` — defensive: refuses any `--approve` / `--request-changes` in audit.log
2. **Severity tiers regex tightened** to `\bMedium\b` / `\bLow\b` (case-sensitive) — exercises that report uses the exact contract phrasing.

## Did iteration 2 fix the issues?

**Issue 1 — exact Auggie invocation foregrounded**: ✅ FIXED.
All three with_skill subagents used `--output-format json` correctly on the first try, and all three successfully extracted JSON from a fenced markdown wrapper. No `--json` fabrication. No exit-1 retry loop.

**Issue 2 — discriminating assertions for hallucination guard + audit trail**: ✅ FIXED.
The new with_skill-only assertions all pass for all three with_skill runs (5/5 skill-specific assertions × 3 evals = 15 hits, evidence-backed). Baselines correctly return `N/A` for these, so pass-rate parity is preserved while still proving the skill artifact contract is honored.

## New surprise: another Auggie preamble

**Both eval-1 (PR #62) and eval-2 (diff) subagents** independently flagged a *new* pitfall not in iteration-2's "Common pitfalls" block:

> Auggie prints `Applying --max-turns override: <N> over agentMaxIterations=500` as the **first stdout line** before the JSON envelope, so the orchestrator must strip the first line (`tail -n +2`) before extracting `.result` and then stripping the inner ```json fence.

Eval-3 didn't hit it because it didn't pass `--max-turns`. This is a strong iteration-3 candidate — already proven across two independent runs and trivial to add. The subagent that caught it (eval-2) explicitly called it out as "could be added in iteration 3."

## Reproducibility / audit trail (qualitative)

The skill-mode runs continue to produce a richer audit trail than baseline:

| Run | Dropped findings (logged) | Severity remaps (logged) | Audit log size |
|---|---|---|---|
| eval-1 with_skill | 1 (F3 — docstring not actually stale) | 0 | 8822 bytes |
| eval-2 with_skill | 2 (F2 inversion, F5 false premise) | 0 | (smaller — partial status) |
| eval-3 with_skill | 0 | 2 (N1 low→nit, M5 low→medium) | ~similar |

**Both baseline runs that surfaced findings did NOT log dropped findings or grounding decisions.**

That's the central qualitative advantage that pass-rate-symmetry doesn't capture.

## Benchmark numbers (iter-2 vs iter-1)

| Metric | iter-1 with_skill | iter-2 with_skill | iter-1 baseline | iter-2 baseline |
|---|---|---|---|---|
| Pass rate | 100% | 100% | 100% | 100% |
| Time | 395.0s | 425.9s | 190.2s | 205.0s |
| Tokens | 90667 | 85459 | 93785 | 82961 |

**Time delta** (with_skill − baseline): **+220.9s** in iter-2 vs **+204.8s** in iter-1 — roughly stable. The pitfall guidance did not add time; it kept Auggie's slow-but-thorough deep-pass time approximately constant.

**Token offload** remains at parity: with_skill ≈ baseline (Claude orchestration cost ≈ Claude-doing-the-review cost). Auggie tokens are not billed via this counter, so the actual offload to Auggie is invisible here but real.

## Recommendation

**Skill is shippable at iteration 2.** The hallucination guard works, the audit trail is reproducible, the invocation pitfalls are foregrounded, and the assertions now objectively prove the contract. Two open follow-ups for a future iteration:

1. **Add the `Applying --max-turns override` preamble to "Common pitfalls"** — proven across 2/2 independent runs that used `--max-turns`.
2. **Description-optimization pass** — run skill-creator's description optimizer to maximize trigger reliability without overfiring.

Recommend: present results to user, accept iteration-2 as ship-ready, queue (1) as a one-line iteration-3 fix, and run (2) once the user signs off.
