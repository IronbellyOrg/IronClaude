# Troubleshoot report: three shadow-run failures (Tier 1, quick)

- Issue: the exit script on shadow runs 03 to 07 failed on (1) parity, (2) the review-completeness check (EV-1), (3) findings-block compliance averaging 0.67.
- Tier reached: 1. Status: partial. Confidence: not independently calibrated.
- Grounding gaps (honest): the independent confidence-calibrator and evidence-validator passes of the protocol were NOT run; the citations below were read directly by the orchestrator from the files named. Wave 1.5 and 1.6 were skipped for this quick pass. Sample is 5 runs.
- Evidence base: `.dev/reflect/*-shadow03..07/` (card headers, `panel/resolution.json`, `panel/clusters.json`, `panel/notes.md`, `return-contract.yaml`, `adversarial/`), `scripts/reflect_shadow_exit.py`, the skill text.

## Correction to my earlier summary

Parity failed in 3 runs for two different reasons, not one: runs 04 and 05 (gateway alias in the card header) and run 07 (the legacy rotation is missing from the contract). I had grouped 07 with the alias cases.

## 1. Parity

**Root cause (alias, runs 04 and 05).** The skill says each card header `model:` is "the resolved model id, written by the orchestrator" (`SKILL.md:341`) but does not say to copy it from `panel/resolution.json`. The orchestrators of runs 04 and 05 wrote the model the harness reported (`claude-gw-tier1b[1m]`, `claude-gw-tier2[1m]`, `claude-gw-tier1a[1m]`, no suffix in run 05), while runs 03, 06 and 07 copied the pin (`claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-opus-5-5`). The exit script compares the two strings (`scripts/reflect_shadow_exit.py:148`), so the gateway alias fails parity even when the class is right.

**Root cause (run 07).** `return-contract.yaml` of run 07 has no `reviewer_personas` or `reviewer_models` telemetry, so the legacy rotation cannot be compared (exit script message: "the legacy rotation ... is not in the contract"). The contract also carries three keys outside the frozen 1.8.0 list (`memory_status`, `notes`, `zero_drop_flag`). This is an orchestrator contract-writing lapse, not an alias problem.

**Proposed solutions**
1. Skill, step 2 of the shadow steps (`SKILL.md:341`): say the `model:` header MUST be copied verbatim from `panel/resolution.json` `reviewers[N].model` (the pin), and the model the harness actually reports goes on a separate `model_observed:` header line. The aggregator reads only `persona`, `model_class` and `model`, so an extra line is safe.
2. Skill, shadow contract recording: name `reviewer_personas` and `reviewer_models` as required telemetry keys and forbid new top-level keys (they belong under `telemetry:`).
3. Optional, not recommended until 1 and 2 are tried: make the aggregator fall back to `model_class` when `model` is an unmapped alias. It would weaken the check.

## 2. EV-1 (review-completeness)

**Root cause.** The rule requires `<output>/adversarial/merged-verdict.yaml` with `merge_method: adversarial` (`SKILL.md:714`, `SKILL.md:1955`, `panel_lint.py:271`), but no step tells the orchestrator to write that file; it is presumed to exist. What the debate step actually left on disk: runs 03, 06, 07 have the yaml one folder deeper (`adversarial/adversarial/merged-verdict.yaml`); runs 04 and 05 have only `merged-verdict.md` and a `return-contract.yaml` inside `adversarial/`, no yaml at all. All five contracts nevertheless say `merge_method: adversarial` and `adversarial_unavailable: false`, so the debate really ran; the gate fails on file placement and format.

**Proposed solutions**
1. Skill, Wave 4: add an explicit step after the debate: "write `<output>/adversarial/merged-verdict.yaml` (keys: `merge_method`, `converged`, `base`, findings summary) from the debate's `merged-verdict.md` / return contract, then confirm it on disk". This is the fix the rule already implies.
2. Make the exit script count the nested path and the `.md` form only if the owner decides EV-1 should accept them; I recommend against loosening a gate that exists to catch silent fallbacks.
3. Track separately: the legacy baseline fails EV-1 in 3 of 39 runs, but 5 of 5 recent runs fail. The cause of the jump (new child skill layout versus orchestrator drift) is UNVERIFIED.

## 3. Reviewer format compliance (0.67 mean)

**Root cause (two parts).**
- **The brief names the format without giving it.** The only instruction added to the reviewer brief is one line asking for a `## Findings block` "findings-v2 block (lens: reflect-pre, citations with roles plan and spec)" (`refs/reviewer-spec.md:39`). Reviewers are never shown the schema, so they improvise: pipe tables in runs 04 and 05 (their notes say "pipe -> JSON-lines"), an escape error in run 03, and invented roles and categories in run 07 (`repo` role; categories and `INFO` severity outside the schema; allowed roles are plan, spec, source, test, diff, artifact at `findings_v2.py:35`).
- **The metric is inconsistent.** Runs 03 and 04 recorded the rate after the one re-ask (1.0), runs 05 and 07 before normalization (0.33), run 06 had 1.0. The 0.67 mean mixes both definitions. First-pass compliance in the runs where it is stated is 1 of 3 (runs 05 and 07).

**Proposed solutions**
1. Extend the brief line with a schema stub and one example line: required fields, the allowed severity, role and category values, and the "JSON lines, one object per line, inside a fenced findings-v2 block" rule.
2. Define the telemetry value once: first-pass valid blocks over reviewers dispatched, recorded before any re-ask or orchestrator remap; record the post-repair count separately.
3. Stop the orchestrator remapping findings itself (run 07): a block that fails first parse gets the bounded re-ask only, as the skill says.

## Recommended next step

Apply solutions 1.1, 1.2, 2.1, 3.1 and 3.2 to the reflect skill and brief, add a test that the brief carries the schema and that the skill names the required keys, reinstall, and rerun a batch. This changes a skill that real users run, so it needs your approval before I edit it. Until then, additional shadow runs will repeat these failures.
