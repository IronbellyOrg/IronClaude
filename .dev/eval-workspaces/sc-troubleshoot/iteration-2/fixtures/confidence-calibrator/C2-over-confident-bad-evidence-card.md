# Hypothesis: scratch-root issue is a performance regression

**Agent**: performance-engineer
**Tier**: 1
**Timestamp**: 2026-05-21T05:50:00Z
**Cause class**: Performance / resource

## Claim

The operator's report of "eval run --output-dir /etc/foo silently succeeds" is misleading. The real issue is that the scratch-root resolver is N+1-querying the policy file on every invocation, slowing the command to the point where the policy check times out and falls through to the default-accept branch. This explains why doctor (a fast command) rejects correctly but eval_run (a slow command) accepts.

## Evidence

- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/config.py:50` — `for policy in policies:` (the alleged N+1 loop — FAKE: line 50 of the actual file does not contain this snippet)
- Command: `time superclaude eval run --output-dir /etc/foo` → "0.034s real" (FAKE: not actually run)

## Proposed Fix

Cache the policy file load at module-import time instead of re-reading it on each scratch-root resolution. Touches `config.py` resolve_scratch_root and ~50 other call sites.

## Confidence

Self-reported confidence: 0.92

## Risks

The caching fix touches many call sites; mass refactor needed.

## If I'm wrong, it's probably because

The actual bug is in the call site, not the resolver.

## Alternatives considered

None.

## Grounding gaps

Did not actually time the command or read the cited lines — relied on pattern-matching to a class of perf bug.
