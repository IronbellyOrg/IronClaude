# Diagnosability Tasklist
**Issue**: PR #359 round 3 hook misclassifications  **Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/hooks/scripts/block-bare-python.sh  **Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: n/a
**branch**: ironbelly/bare-python-hook-  **repro-venue-id**: bash .dev/troubleshoot/bug-pr-round-hook-findings-/trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh

## Emitter search
emitters-found: 2 (src/superclaude/hooks/scripts/block-bare-python.sh:130 `print b`; :339 block message)
already-read-files: 1
usable-capture-routes: 1 (read-only scanner copy printing every chosen command word; executed this run, trace-probe.out)

## Discriminator rows
core-rows=4, pack-rows=0, total-rows=4
| ID | role | claim | observable | probe | value-if-true | value-if-false | outcome mapping | provenance | state |
|---|---|---|---|---|---|---|---|---|---|
| P4-exact | core | P4 (:336) produced exit 0 for `{fd}>/dev/null python3 -c 1` because the scanner chose `{fd}` | cmdword= lines + hook_exit | trace-probe.sh | `cmdword={fd}`, `hook_exit=0` | a python3 cmdword or hook_exit=2 | true -> consistent; false -> refuted; empty -> unobserved | scanner :206 | observed: consistent |
| P4-ref | core | reference: `2>/dev/null python3 -c 1` (numeric fd) is blocked | hook_exit | hook run | 2 | 0 | 2 -> numeric path works (consistent) | scanner :206 | observed: hook_exit=2 (tier1-observation.md "Reference rows") |
| P5-exact | core | P5 (:340) produced exit 2 for `python3() {...}; echo ready` because endword chose `python3` before the `()` | cmdword= lines + hook_exit | trace-probe.sh | `cmdword=python3`, `hook_exit=2` | no python3 cmdword or hook_exit=0 | true -> consistent; false -> refuted; empty -> unobserved | scanner :216-219 | observed: consistent |
| P5-ref | core | reference: `f() { python3 x.py; }` stays blocked (body word) | hook_exit | test function-body | 2 | 0 | 2 -> consistent | tests/hooks/test_block_bare_python.py:101 | observed: hook_exit=2 (tier1-observation.md "Reference rows") |

## Bracket
n/a

## Fix candidate
Proposal only (applied by sc-pr-submit-protocol): skip a command-position word followed by `()` as a function name; treat an unquoted `{NAME}` word directly before `<`/`>` like a numeric fd prefix.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
None required (measurements already observed through a read-only copy).

## Verification
P4-exact and P5-exact observed in trace-probe.out.

## Rollback
Nothing to roll back.

## Patch-round counter
Identity: branch `ironbelly/bare-python-hook-`, venue above; authoritative .dev/troubleshoot/diagnosability-rounds.json = 1 (snapshot diagnosability-rounds.json).
