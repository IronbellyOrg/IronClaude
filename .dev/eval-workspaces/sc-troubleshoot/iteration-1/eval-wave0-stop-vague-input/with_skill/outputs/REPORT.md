# Troubleshoot Report — Vague Input STOP

**Command**: `/sc:troubleshoot` (NEW protocol skill) | **Tier reached**: 0 | **Status**: stopped
**Source**: subagent inline output (harness blocked REPORT.md write; audit.log was written separately)

## Decision: STOPPED at Wave 0

Applied protocol honestly. Input `"Something's broken. Please troubleshoot it deeply."` triggers the explicit Wave 0 STOP rule in `SKILL.md`:

> STOP if `--depth deep` is requested but the issue description is under 10 words and no scope was given.

All three conditions are met:

- `--depth deep` (inferred from the word "deeply")
- 6 words (< 10)
- No `--scope` provided

The hallucination contract forbids fabricating hypotheses from no signal — no error, stack trace, failing command, file, symbol, or domain keyword exists to ground a single citation.

## Did NOT

- Spawn `root-cause-analyst`
- Query auggie / serena / context7 / tavily
- Invoke `sc:adversarial-protocol`
- Invent hypotheses

## Asked the user for

Any one of:

1. **Concrete symptom** — exact error / stack trace, failing command + expected-vs-actual, regression description, or failing test name.
2. **`--scope`** (file/dir/symbol).
3. **Domain hint** to set `--type` (bug/build/performance/deployment/security/test).
4. **Repro command** if available.

## Artifacts

- `audit.log` (written successfully) — contains `SC:TROUBLESHOOT:TARGET` header and `SC:TROUBLESHOOT:SUMMARY` footer with `status=stopped, tier_reached=0, escalation_reason=wave0_stop_underspecified_deep`.
