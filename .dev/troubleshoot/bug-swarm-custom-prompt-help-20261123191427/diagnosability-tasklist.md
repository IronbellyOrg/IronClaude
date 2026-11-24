# Diagnosability Tasklist
**Issue**: 568, unsupported custom prompt flag in help.
**Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/cli/swarm/commands.py help  **Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: n/a
**branch**: swill-ib/bug-swarm-refactor-find-recommends-unavailable-s  **repro-venue-id**: swarm-custom-prompt-help

## Emitter search

emitter-search: n/a (no missing single-expression boolean/enum predicate; observed symptom is help wording).
emitters-found: 3 (commands.py:438 docstring help, :3785 option help, :3828 adjacent echo).
already-read-files: 4 captured streams (scaffold-help.txt, validate-lenses-help.txt, run-help.txt, run-rejection.txt), all preserved; this count is the raw observation corpus, not all source reads.
usable-capture-routes: 2. Public scaffold --help and validate-lenses --help emit the disputed strings directly into their captured stdout. These are read-only public command invocations; no new worker script execution is needed. Adjacent custom-lens rejection at :3828 is not evidence of generated help and was not executed. Job event logs are excluded: help exits before jobs start. Authorization yes for help-only inspections; model dispatch forbidden.

## Discriminator rows

core-rows=5, pack-rows=0, total-rows=5. Two surviving help producers trigger bookkeeping, not competing root causes. Primitive kind: call/return (public CLI help). Each exact form and documented minimal reference form is the same --help invocation; no differing prediction is established by this pair. This does not test an environment substitution. comparator=none; no passing environment is claimed.

| ID | Role | Claim / observable | Probe | Value if true | Value if false | Outcome mapping | State / provenance |
|---|---|---|---|---|---|---|---|
| P1-exact | core | validate-lenses help contains stale flag | uv run superclaude swarm validate-lenses --help | stale flag present | stale flag absent | present consistent, absent refuted; error inconclusive | pending, no new confined experiment boundary established beyond original public help inspection |
| P1-ref | core | same minimal help call exposes the text | uv run superclaude swarm validate-lenses --help | stale flag present | stale flag absent | present consistent, absent refuted; error inconclusive | pending; identical callee/form, not independent control |
| P2-exact | core | scaffold help contains stale flag | uv run superclaude swarm scaffold --help | stale flag present | stale flag absent | present consistent, absent refuted; error inconclusive | pending, no new confined experiment boundary established |
| P2-ref | core | same minimal help call exposes the text | uv run superclaude swarm scaffold --help | stale flag present | stale flag absent | present consistent, absent refuted; error inconclusive | pending; identical callee/form, not independent control |
| control | core | a no-op completes | no-op invocation | unknown, no causal relation to help wording | unknown, no causal relation to help wording | either value inconclusive | pending; no passing environment/control-proof; no command invented |

No discriminating falsifier established for an environment-dependent mechanism; that mechanism is not claimed. The original four public captures remain observed evidence, not retroactively preregistered results.

## Hard Constraints

Invocation sites only, additive, reversible. Any proposed instrumentation must carry `# Diagnosability-tasklist instrumentation: revert after defect closed.` No production patch, model run or new option is authorized by this tasklist.

## Implementation tasks

No invocation-site instrumentation change is justified for the already captured help mismatch. The remaining core exact/reference and no-op rows are inert proposals, not instructions to change logging or run a swarm. If later execution is approved at a suitable confined boundary, record actual outputs and exit statuses beside the original captures, never overwrite them. No production edit is an instrumentation task.

## Verification

Initial parent captures directly show each stale string and parser rejection, with exits 0/0/0/2. The five preregistered rows above were not executed. They cannot be relabelled passed from the earlier unregistered captures. The report stays `partial` until P1-exact and P2-exact have complete provenance-bound output and the reference/control rows have observed results or an evidence-backed applicability decision. No comparison of two environments or repaired-state acceptance is established.

## Rollback

No source instrumentation is proposed. Keep diagnostic evidence; do not delete it.

## Patch-round counter

Authoritative .dev/troubleshoot/diagnosability-rounds.json was read, then updated under nonblocking fcntl lock with atomic replace by counter-update.py. Current branch / swarm-custom-prompt-help now records 1; the unrelated existing branch entry was preserved. Snapshot ./diagnosability-rounds.json records the same identity and round. No reset. This run performs no further increment.
