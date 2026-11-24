# Pipeline boundary assessment

## Boundary scan
| boundary_type | producer | transformers | consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|---|---|
| CLI/subprocess | lens command template | CLI substitution, reducer, YAML emitter | operator invokes suggested slash command | refactor_find.py:53; commands.py:2141-2157; captured contract:64 | A successful producer run can suggest an unavailable consumer. | applicable | Handoff names a separate command whose interface must match. |
| file-stdin-prompt | successful worker final_path list | compare_files inserts literal existing-review | adversarial existing-readable-files input contract | commands.py:2143; installed adversarial skill:54-62 | Real reports can be mixed with a nonexistent placeholder. | applicable | Source and captured artifact expose a file-delivery mismatch. |
| generated-artifact-parser | return-contract.yaml | wizard renders recommendation verbatim | operator / downstream command | wizard skill:159-164 and refs/run-monitor-summarize.md:88 | Well-formed YAML is not proof that its contained command is usable. | applicable | The full emitted artifact, not merely template name, needs validation. |
| gate-status-enum | worker status | IMM status reducer | run status | contract status success vs invalid command | Success counts are not handoff validity. | not_applicable | No status-enum implementation change is proposed. |
| duplicate-evaluator | no duplicate command-validity evaluator found | none | none | lens validator six checks :603-609 | Existing validation omits this rule. | not_applicable | No duplicated implementation of command validation is under change. |
| persisted-state | lens snapshot | rehydration | resume | resume call commands.py:2578-2586 | Old snapshots may retain defaults. | applicable | Resume is a separate consumer path; no resume fix or proof is claimed. |
| review-selector | report path list | proposed comma-list delivery | downstream comparison | actual three final_path values | Wrong-file input could be compared. | applicable | Must prove identity of the actual reports, not just nonempty count. |
| sibling-pipeline | all registered lens templates | same CLI builder/reducer; reflect own builder | wizard/operator | field search over 20 source files and caller trace | Global compare_files repair could alter sibling semantics. | applicable | Preserve sibling handoffs while repairing refactor-find. |
| prior-escape-unmask | none asserted | none | none | no historical replay executed | Cannot infer E1-E5 catch coverage. | not_applicable | No earned escape-coverage claim. |

## Mechanism
A structured result transports executable-looking instructions between independently specified interfaces. Formatting and producer success do not validate consumer availability, option syntax or the identity/existence of each referenced file. A helper-only name substitution can therefore leave the operator boundary broken.

## Decisions
pipeline_hardening_applicable: true (set once)
known_escapes_caught: []
HC5 off-path review: required, since a generated artifact selects the downstream input. Evidence-validator will receive the actual artifact and all four cards; no claim of performed review before receipt.
Scope remains diagnosis-only. The original defect is observed; repaired-state acceptance is not claimed.
