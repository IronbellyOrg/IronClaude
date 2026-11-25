# Completion Contract Ledger

## Contract rows

| contract_token | role | component_path | discovery_method | classification | unreachability_proof |
|---|---|---|---|---|---|
| runtime.on_completion.write_done_sentinel | producer | models.py:563-573 | source Read | classified: default-on intended policy | n/a, live |
| runtime.on_completion.write_done_sentinel | transformer | commands.py:931-937,1929 | exact references and Read | classified: fresh lens sets true, decoded to JobSpec | n/a, live |
| runtime.on_completion.write_done_sentinel | transformer | preflight.py:1888-1976 | definition search and Read | classified: resume only recovers subset; runtime defaults apply | n/a, live |
| terminal + done.json | consumer | commands.py:2145-2178 | graph callers + exact references + real CLI | classified: foreground continuation omits writer | n/a, live |
| terminal + done.json | consumer | commands.py:2578-2599 | graph callers + exact references + real resume | classified: resume continuation omits writer | n/a, live |
| terminal + done.json | transformer | commands.py:1297-1309 | Read child argv | classified: detached child re-enters normal CLI; parent does not complete job | n/a, live; runtime not exercised |
| ResultContract.status -> DoneSentinel | producer | reduce.py:383-440 | definition/caller search and Read | classified: existing validated writer; not called by run completions | n/a, live via reflect and tests |
| ResultContract.status -> DoneSentinel | consumer | reflect/ensemble.py:421 | only production caller from exact src search, Read | classified: reflect already calls existing writer | n/a, live; not changed |
| killed marker | producer | commands.py:3518-3555 | exact reference search and Read | classified: distinct operator-kill writer and empty contract path | n/a, live; not changed |
| done.json presence/status/path | evaluator | docs/swarm/monitoring-patterns.md:35-71 and run artifacts filesystem checks | doc/source sweep and executed oracle | classified: documented polling consumer; actual waiting consumer not exercised | n/a |
| writer helper outputs | evaluator | tests/swarm/test_done_sentinel.py:47-146 | test source and observed pytest result | classified: passing helper tests, not CLI-boundary acceptance | n/a |

Source paths above resolve under src/superclaude/cli/swarm unless explicitly prefixed reflect/ (then src/superclaude/cli/reflect). No component is marked dead/legacy without proof.

## Sibling sweep

Exact src search found one production emit_done_sentinel caller (reflect), plus its definition. reduce_wave3 graph callers48/48 and source Read locate foreground, resume and reflect. Detached child argv routes into normal continuation; kill is separate writer. No helper proof is promoted to a product-path pass. Early transport errors before terminal completion are a different outcome and must not gain false completion markers. Partial/failed terminal reduction follows the inspected shared continuation, but was not runtime-reproduced. Original runtime-policy persistence on resume is incomplete and outside this omission fix's acceptance claim; do not silently expand into unrelated metadata recovery.

## Verdict

HC2: PASS for bounded contract enumeration and sibling classification. This ledger does not claim the classified defective consumers are repaired, nor that detached/failure/polling behavior was exercised.
