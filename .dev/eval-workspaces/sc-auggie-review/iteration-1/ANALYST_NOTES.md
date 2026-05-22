# Iteration 1 — Analyst Observations

## Summary stats

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate (assertions) | 100% | 100% | 0 |
| Avg time | 395s ± 40s | 190s ± 65s | **+205s slower** |
| Avg Claude tokens | 90.7k ± 8.9k | 93.8k ± 30.3k | -3.1k (noise) |
| Citation accuracy | 94% (avg) | 98% (avg) | -4pp |
| Tool calls | 26.7 avg | 31.0 avg | -4.3 |

## What the pass-rate metric hides

All 58 assertions pass on both configurations — meaning the assertions only check **report shape**, not **report value**. The skill's real contributions are not captured by the current rubric:

### 1. Hallucination guard (with_skill exclusive)
- **eval-2 with_skill**: Wave 3 caught Auggie's F2 finding (claimed install_templates was missing a fallback) and **inverted** it — install_templates actually has *more* robust source resolution than its siblings. Without grounding, this would have been a wrong claim posted to a PR.
- **eval-3 with_skill**: Wave 3 dropped Auggie's "roadmap_run @ executor.py:2895" finding — function name doesn't exist, cited line is mid-body of `_restore_from_state`. The dropped finding is explicitly documented in the report with full reasoning.
- **eval-3 baseline**: Cited `eval/commands.py:798` but file has only 463 lines — a real hallucination that slipped through. Baseline has no grounding pass to catch it.

The citation-accuracy metric *appears* to favor baseline (98% vs 94%) but is misleading: the with_skill "invalid" citations are documented `DROPPED` entries that the skill consciously surfaces in the audit trail. The baseline's invalid citations are silent failures.

### 2. Reproducibility / audit trail
With_skill always produces:
- `audit.log` (per-wave decisions)
- `auggie-prompt.txt` (exact prompt to Auggie)
- `auggie-raw.json` / `auggie-parsed.json` (raw + parsed Auggie output)
- `auggie-findings.json` (final parsed findings array)

Baselines produce only `REVIEW.md`. There is no way to re-run, debug, or check baselines against the underlying retrieval evidence. The skill builds a reviewable evidence chain.

### 3. Token offload contract
Claude-side token usage is essentially equal (90.7k vs 93.8k mean). The skill's design intent — offload the heavy retrieval pass to Auggie so Claude does only orchestration + synthesis — appears to be working at parity rather than dramatically better. However, this benchmark **does not measure Auggie-side cost**, which is the real point of the offload. A user-facing dollar/quota comparison would require pulling Auggie API metrics.

### 4. Time tradeoff
With_skill is consistently slower (+205s mean) because:
- Multi-wave protocol with synchronous auggie shell-out (single biggest delay)
- File:line grounding pass reads every cited file
- Audit log writes between waves

This is the cost of structured rigor. Acceptable for PR reviews where correctness > latency, but worth noting in the SKILL.md cost profile.

## Discriminating signals to add in iteration-2 (if pursued)

Current assertions are non-discriminating. To capture skill value, future assertions should check:

1. **`audit.log` mentions ≥1 Wave-3 grounding decision** — drop, invert, or revise. (Tests the hallucination guard is being exercised, not just structurally present.)
2. **`auggie-raw.json` or `auggie-parsed.json` exists** — already partially covered.
3. **Cited path/line invalidity is documented in report** — i.e., any `DROPPED` block has the original Auggie claim + rejection rationale. (Tests transparency.)
4. **Severity rubric tier names match the documented set exactly** (Critical/High/Medium/Low/Nit, not "high-priority", "critical-issue", etc.) — tests rubric adoption.
5. **No `--approve` / `--request-changes` strings appear anywhere in audit.log** — defensive check on the gh interaction boundary.

These would discriminate with_skill from baseline by ~6-8 assertions.

## Surprises / failure modes observed

1. **with_skill eval-1 subagent initially used `--json` (a fabricated auggie flag)** before re-reading the skill and correcting to `--output-format json`. The skill's `refs/auggie-prompts.md` does document the right invocation, but it's buried. Iteration-2 could foreground "Exact Auggie Invocation" in the SKILL.md body, not just the ref.

2. **Auggie's natural output is markdown, not JSON** even with `--output-format json` — the subagent had to extract a fenced ```json block from a markdown response. This worked but is fragile. The skill could explicitly teach this parse step.

3. **eval-3 with_skill report excellence**: cross-cutting CC1 (executor-skeleton duplication) and CC4 (duplicate `TurnLedger` class across sprint/models.py:693 and prd/executor.py:139) are exactly the asymmetric-helper / api-contract findings the protocol targets. These are higher-signal than 90% of the baseline's per-line nits.

4. **eval-3 baseline overspent**: 265s + 129k tokens to produce 24 findings — many of which were nits or restatements. With_skill produced 13 retained findings in 426s + 98k tokens — fewer but more concentrated on cross-cutting concerns, matching the skill's design intent of higher-signal/lower-volume output.

## Recommended next steps

- **If user wants to iterate**: improve the SKILL.md with "Exact Auggie Invocation" foregrounded; tighten the `auggie-prompts.md` parse instructions; add 2-3 discriminating assertions; re-run iteration-2.
- **If user wants to finalize**: skill is production-ready; consider running the description-optimization loop (skill-creator step) to improve trigger reliability; close out iteration-1.
- **Either way**: the skill demonstrates its core value (hallucination guard, audit trail, structured offload). The current pass-rate parity is an artifact of weak assertions, not weak skill behavior.
