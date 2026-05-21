# Troubleshoot Report — Vague input

**Command**: `/sc:troubleshoot` (old, snapshot baseline) | **Mode**: diagnose-only
**Source**: subagent inline output (harness blocked direct file write)

## What I did

1. Read the command spec at the given path.
2. **Analyze**: Noted the input has zero signal — no symptom, no component, no error, no `--type` flag, no logs.
3. **Investigate**: With no target, ran a generic system survey (`git status`, `git log`, `ls`) which produced findings unrelated to any user-stated problem.
4. **Debug/Propose/Resolve**: Could not form a hypothesis, rank solutions, or apply fixes.

## Did I ask the user for more, or proceed?

**Proceeded.** The old command has **no explicit STOP rule for vague input** and no clarifying-question protocol. Its Behavioral Flow says "Analyze → Investigate → Debug → Propose → Resolve" with no off-ramp.

Following it honestly, I produced a diagnostic report that documents the failure mode (input is unscopeable) rather than inventing a problem to solve. The most useful "proposed solution" I could offer is "user supplies a concrete symptom" — which is effectively what a STOP rule would have forced up front.

## Key finding for the eval

The old skill silently degrades on vague input. It does not ask, does not stop, and a literal-minded follower will burn tool calls on a generic system survey before concluding the input was insufficient. A STOP-on-vague-input rule is missing.
