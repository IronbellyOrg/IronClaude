# Diagnosability Context Card

**Issue**: 568, help advertises unsupported custom prompt option.
**failing_component**: src/superclaude/cli/swarm/commands.py generated help
**Verdict**: partial
**Complexity**: trivial (score 0: one-file deterministic wording mismatch, no security/intermittence/performance claim)
**Hard-stop fired**: false
**Round**: 1 of 3
**Captured bytes (failing run)**: 13359 across four parent-captured CLI streams

## 3-W's coverage

| W | Answerable | Evidence |
|---|---|---|
| When | partial | Invocation/exit evidence, no timestamped structured help logger. |
| Where | yes | Exact source help passages match both captured outputs. |
| Why | partial | Wording and parser rejection visible; log reachability unknown on fallback. |

## Branch A — Log-call inventory

Four signal rows in wave1_6-branch-A.md: two generated help passages, one adjacent click.echo and one parser output capture. All categorized print-like, explicitly not structured logging. No exception-handler/error-reporter hit in assigned help scope. Captures are 1871/1601/9745/142 bytes; adjacent custom-lens diagnostic remains unobserved. degraded=true.

## Branch B — Log-config reachability

Three source/config hits in wave1_6-branch-B.md; SwarmConfig declares INFO but actual effective level unknown and unrelated to generated help. Four per-signal reachability rows remain unknown under degraded discovery. No runtime filtering conclusion is asserted from this absence.

## Sufficiency rubric application

S14 does not apply: disputed help strings and parser rejection are visible, not dropped/substituted. S9 print-like deterministic signals yields partial; Augment unavailable/native fallback independently caps at partial. Two surviving string help rows trigger discriminator-required=yes mechanically. Five inert core rows emitted; no environment control or new confined experimental boundary was established. No numeric threshold/bracket is asserted. Trivial complexity permits hypothesis formation; no hard-stop.

## Implication for diagnosis confidence

The public help/parser mismatch is directly captured and its two wording sites are known.
Discovery is degraded after Augment403; no passing-environment comparator or repaired-state witness exists.
Core exact/reference/control rows remain pending in the tasklist, not successful checks.
Proceed only with a bounded wording hypothesis, without claiming an executed repair or environment-dependent explanation.

## Tasklist reference

./diagnosability-tasklist.md
