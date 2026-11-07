# Evidence validation result (Wave 5 gate) for REPORT.md

Recorded by the orchestrator from the evidence-validator's reply. The validator has Read, Grep and Glob only and could not write this file; its row-by-row table was not returned, so only counts and narrowings are recorded here.

- citations checked by the validator: 47 (all re-read)
- supported: 45
- partial (narrowed in the report): 2
- unsupported (dropped): 0

Narrowings applied to REPORT.md:

1. `brainstorm.md:153` (M-12) -> `brainstorm.md:153-154`. Line 153 shows only that the brief passes exactly one of `--output` or `--report-dir`; the separate worker contract that lists the own contract in `artifacts` is on line 154.
2. `plan:19` (M-16) -> worded as "names two archived P1 artifacts (`lc10-result.md`, `p1-owner-decisions-20261105.md`) as read-only", with `plan:21` cited for the six-file list.

Specific claims the validator confirmed: plan:133 "no known false FAIL"; plan:128 equals brief:217 byte for byte; plan:25 vs brief:199 as quoted in M-07; plan:152 as quoted in M-08; SKILL.md:183; analyze.md:97-98; spec:62 and spec:302; plan:26; plan:21 (six files); the report's fix block equals `recommended_wording_fix.part_a_amended_live_check_sentence` in `adversarial/merged-verdict.yaml` byte for byte.

Supporting lines the validator suggested, re-read by the orchestrator and added: `SKILL.md:199` (`fallback_1` path, M-01) and `.github/workflows/test.yml:99` (`ruff format --check src/ tests/`, M-09).
