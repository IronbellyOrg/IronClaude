# Panel notes (shadow mode, run comboC-r2)

- Findings blocks: 3 of 3 valid on the first parse by the cluster command; no re-ask. Reviewer cards were saved with the heading `## Findings`; the files in `panel/cards/` use `## Findings block` as the aggregator expects, and carry `persona`, `model_class`, `model` (copied from `resolution.json`) and `model_observed` (read from the agent transcript).
- Identity: `identity_source: observed` (assistant-message model ids in the agent transcripts: claude-sonnet-5-5, claude-haiku-5-5, claude-opus-5-5). Self-reports named the gateway aliases (claude-gw-tier1b, claude-gw-tier1a) for two reviewers and claude-haiku-5-5 for the third; none contradicts the pins. Executor class unknown, so no claim of verified independence.
- Judge: the Wave 4 scoring and merge routing were done by the orchestrator session (claude-gw-tier1b, sonnet class), not by a judge named in the adversarial return contract. `judge_identity` is recorded as `unknown` per the contract rule; the real collision with reviewer 1's class is noted here.
- Calibration ids: `per_finding` ids match the findings-block ids; 27 of 27 scored on the first pass, 26 of 26 after the kept-ids pass (V2:F9 was withdrawn).
- Citation precheck: `panel/precheck.json` (plain snapshot, 90 flagged `not-in-snapshot`) and `panel/precheck-repo-paths.json` (repo-relative snapshot copy, 0 flagged).
- The Wave 5 validator agent has no Write tool; its table was copied by the orchestrator into `artifacts/evidence-validation.md`.
