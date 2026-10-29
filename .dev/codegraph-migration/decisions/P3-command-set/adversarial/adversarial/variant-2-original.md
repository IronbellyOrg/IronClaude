# Option B: grounding skill + impact + graph (brainstorm K-1, K-2 with K-3 folded in, K-4)

Read `context.md` first.

## Commands and skills

1. `sc-graph-grounding` (delegate-only skill, no slash command): the shared probe (readiness, worktree provenance, version, telemetry), a capability map ref, a citation-contract ref, a closed `graph:*` degraded vocabulary and a `resolve-callsite.sh` script that turns a caller's definition line into Read-verified call-site lines. Every consumer runs it once per run as "Step 0".
2. `/sc:impact <symbol> | --file <path> | --diff [<base>]` `[--depth] [--limit] [--tests] [--output-dir] [--caller]`: dependents (prod/test), call sites resolved by the grounding skill, and with `--tests` the `codegraph affected` test list (test-scope folded in). Writes `impact.md` + `return-contract.yaml`.
3. `/sc:graph [status|init]`: user-facing readiness and the only `init` owner.

## Callers

- `sc-graph-grounding`: troubleshoot, reflect, implement, pr-submit, auggie-review, cleanup-audit, workflow, `/sc:impact`, `/sc:graph`, explain, load.
- `/sc:impact`: as in option A plus test selection callers (implement Q6, pr-submit VG-1, reflect UC-2) through `--tests`.

## Strengths

- One seam owns codegraph semantics (probe, vocabulary, citation contract), so consumers do not drift.
- The call-site resolver closes a measured gap (caller rows give definition lines, EVAL §5.5).
- Two user-facing commands instead of three; test selection lives with impact.

## Weaknesses

- The grounding skill is a skill invocation per consumer run (latency and token cost unmeasured, brainstorm OQ-6) and adds a script with its own parser and fixtures.
- A shell resolver that parses undocumented CLI text output is brittle across releases.
- More machinery than the shared guide doc; the guide plus Read already enforces read-before-cite.
- `--tests` overloads `/sc:impact` for callers that only want tests.
