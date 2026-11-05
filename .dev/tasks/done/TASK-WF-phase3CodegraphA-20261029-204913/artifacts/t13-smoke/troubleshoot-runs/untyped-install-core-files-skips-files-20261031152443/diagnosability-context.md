# Diagnosability Context Card
**Issue**: install_core_files skips files
**failing_component**: src/superclaude/cli/install_core.py
**Verdict**: partial
**Complexity**: trivial (score 0)
**Hard-stop fired**: false
**Round**: 1 of 3
**Captured bytes (failing run)**: n/a (no capture supplied)
## 3-W's coverage
| W | Answerable | Evidence |
|---|---|---|
| When | no | No failing-run capture |
| Where | partial | Named function localized in source only |
| Why | partial | Conditional skip visible; actual inputs unobserved |
## Branch A: Log-call inventory
Branch unavailable: invalid selected worker roster. Parent inspected returned skip message at install_core.py:83-88 and CLI echo at main.py:179. Failed copies are separately collected at install_core.py:73-74. No branch artifact fabricated.
## Branch B: Log-config reachability
Branch unavailable. Parent inspected direct message return and CLI echo; actual command and stream are unknown. No branch artifact fabricated.
## Sufficiency rubric application
Degraded parent discovery found direct output signal: partial under degradation cap. No evidence of S14 datum substitution. Missing failing-run datum triggers discriminator-required=yes. Complexity score 0: trivial, no hard stop.
## Implication for diagnosis confidence
The skip message lists names, but no run transcript was supplied.
Static behavior can be explained; the incident's cause cannot be selected.
Obtain original command and complete skipped-files output before recommending overwrite.
## Tasklist reference
diagnosability-tasklist.md
