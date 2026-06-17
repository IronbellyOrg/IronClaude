# QA Report — POST-completion Content / Domain-Accuracy Lens (doc-qualitative)

**Topic:** TFEP forensic→troubleshoot backend migration
**Date:** 2026-06-16
**Phase:** doc-qualitative (domain-accuracy content lens; POST-completion)
**Fix cycle:** N/A (report-only; `fix_authorization: false`)
**Adversarial stance:** assumed ≥5 domain-accuracy errors; hunted for them.

---

## Overall Verdict: FAIL

Two genuine domain-accuracy defects found where the migrated TFEP does NOT
genuinely work against the troubleshoot backend as written: one CRITICAL
(consumer reads a field absent from the wire contract) and one IMPORTANT
(consumer Step 5 reads a field the producer defaults to `null`, contradicting
the very next sub-step). The six explicit brief checks otherwise PASS.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every adapter field the §4.5 consumer reads is a real troubleshoot Output Contract field | FAIL | All 7 wire fields exist; but consumer line 225 reads `behavior_is_documented` which is NOT in the 7-field wire set (grep matrix: `in_wire_yaml_block=0`). See CRITICAL-1. |
| 2 | Dispatch flags `--caller`/`--context`/`--output-dir`/`--depth` accepted by /sc:troubleshoot | PASS | Producer Wave 0 step 1 (SKILL.md:120) lists `--context`,`--caller`,`--output-dir`,`--depth` as accepted; command argument-hint (troubleshoot.md:8) carries all four. |
| 3 | `--depth standard` / `--depth deep` are valid depth values | PASS | troubleshoot.md:51 Options table (`quick`/`standard`/`deep`, default `standard`); SKILL.md:137 audit header `<quick\|standard\|deep\|auto>`; Wave 2 SKILL.md:300 `--depth standard or unset`; SKILL.md:299 `--depth deep`. |
| 4 | Incident-template rebound sources (root_cause_summary, solution_summary, report_path, audit_log_path) exist in the contract | PASS | `root_cause_summary`/`solution_summary` = wire fields (SKILL.md:76-77, wire set:471); `report_path`/`audit_log_path` = Output Contract fields (SKILL.md:45-46), correctly cited as diagnostic-artifacts (not wire fields) at task-protocol:260. |
| 5 | troubleshoot genuinely emits `return-contract.yaml` under `caller=task-unified` (Wave 5 step 4.5) | PASS | SKILL.md:148 (`caller=task-unified` marks Wave 5 to emit) + SKILL.md:471 (step 4.5 writes it) + 481 (exit criterion). Consumer always passes `--caller task-unified` (task-protocol:215,268-269). |
| 6 | No reference to a non-existent backend artifact (no rca-verdict.md / solution-verdict.md) | PASS | grep across all 5 files: NONE found. No `forensic` leakage either. |
| 7 | Consumer Step 5 `tasklist_insertion_path` read vs producer default | FAIL | Step 5 line 233 "Read `tasklist_insertion_path`" → "Insert the remediation block", but producer defaults it to `null` in diagnosis-only TFEP mode (SKILL.md:471). See IMPORTANT-1. |
| 8 | report-template TFEP Consumer YAML block matches producer 7-field wire set | PASS | report-template:160-168 lists exactly the 7 producer wire fields (status, test_is_wrong, recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary). |
| 9 | `root_cause_summary`/`solution_summary` source sections exist in report-template | PASS | Diagnosis (report-template:65), Proposed Fix (85), Next Steps (146) all present; producer sourcing (SKILL.md:76-77) matches. |

## Summary
- Checks passed: 7 / 9
- Checks failed: 2
- Critical issues: 1
- Important issues: 1
- Minor issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| CRITICAL-1 | CRITICAL | sc-task-protocol/SKILL.md:225 | The asymmetric-cost branch reads `behavior_is_documented == true` directly "from the return contract", but `behavior_is_documented` is NOT one of the 7 fields in the `return-contract.yaml` wire set. Producer step 4.5 (SKILL.md:471) enumerates exactly `status, test_is_wrong, recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary`; it uses `behavior_is_documented` only internally to *compose* `remediation_target`, and does NOT emit it. The report-template TFEP Consumer YAML block (report-template:160-168) and the consumer's own Step 4 field list (task-protocol:219) both omit it. Consequence: the `behavior_is_documented == true` predicate evaluates against a missing/undefined field at runtime — the docs-protection branch silently never fires on that predicate. | Rewrite the branch to key ONLY on the wire-available `remediation_target == "docs"` (the producer's intended docs signal), e.g. "If `remediation_target == "docs"`: present to user for spec/stakeholder review." Remove the `behavior_is_documented == true` primary predicate, OR add `behavior_is_documented` as an 8th field to the producer wire set + report-template YAML block + Step-4 field list so all three agree. Do NOT leave the consumer reading a field the contract does not carry. |
| IMPORTANT-1 | IMPORTANT | sc-task-protocol/SKILL.md:233 (Step 5 item 10) | Step 5 instructs "Read `tasklist_insertion_path` from the return contract" then "Insert the remediation block". But the producer (SKILL.md:471) defaults `tasklist_insertion_path` to `null` in diagnosis-only TFEP mode and explicitly states task-protocol composes the `## Failure Remediation Plan (Adjudicated)` block from `remediation_target`/`root_cause_summary`/`solution_summary` — which Step 5 item 11 (task-protocol:236) actually does. The "Read `tasklist_insertion_path`" instruction is vestigial and contradicts the next sub-step: under the remediation-ownership decision the field is null in the normal path, so an executor literally following item 10 first reads null and may stall. | Reword item 10 to: "Read `tasklist_insertion_path`; it is `null` in the normal diagnosis-only flow (the producer's default) — when null, compose the remediation block from `remediation_target`/`root_cause_summary`/`solution_summary` (item 11). Only when non-null does troubleshoot supply a standalone adjudicated plan file to splice in." Make the null-default the documented primary path so item 10 and item 11 agree. |

## Actions Taken
None — `fix_authorization: false` (report-only). Both findings are within the
migrated file set (task-protocol §4.5 is an in-scope edited file), so neither is
OUT-OF-SCOPE; they are documented for the orchestrator/fix-cycle to remediate.

## Self-Audit (reliance vs verification)
This lens received no `## Inherited Structural Verdict` block, so I ran fully
standalone (no reliance to audit).

**(a) Reliance list — rf-qa PASS items skipped:** none (no inherited verdict supplied).

**(b) Independent semantic checks (≥1 required):**
- Wire-contract field-existence parity — built a grep matrix over all 8
  consumer-read field names against (i) producer Output Contract and (ii) the
  return-contract.yaml YAML block in report-template:160-168. Surfaced
  `behavior_is_documented: in_wire_yaml_block=0` → CRITICAL-1. Tool evidence:
  Bash grep loop over `skills/sc-troubleshoot-protocol/SKILL.md` +
  `refs/report-template.md`.
- Producer-default vs consumer-read flow check — read SKILL.md:471 (`tasklist_insertion_path`
  default `null`) against task-protocol:233-236 → IMPORTANT-1. Tool evidence: Read +
  sed of both regions.
- Non-existent-artifact sweep — grep `rca-verdict|solution-verdict|forensic` across
  all 5 files → NONE. Tool evidence: Bash grep.

### Self-Audit answers (mandatory)
1. Factual claims independently verified against source: 9 checklist items + 8-field
   parity matrix + 3 cross-file flow traces — every adapter field, every dispatch
   flag, both depth values, all artifact names verified against actual file content.
2. Files read in full: all 5 edited files (sc-task-protocol/SKILL.md,
   sc-troubleshoot-protocol/SKILL.md, commands/troubleshoot.md, commands/task.md,
   refs/report-template.md), plus targeted grep/sed re-reads of the wire-contract and
   §4.5 regions.
3. Why trust the verdict found issues: the two findings are backed by exact
   line citations and a reproducible grep matrix (`behavior_is_documented` shows
   `in_wire_yaml_block=0` while all 7 real wire fields show `=1`); the producer's own
   step 4.5 enumeration is the contradicting ground truth.
4. Web research: none performed — this is a fully local file-bound contract-parity
   review; no external lookup was required, so no Tavily/fallback engagement applies.

## Confidence
Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 5 | Grep: 6 | Glob: 0 | Bash: 6

## Recommendations
- Resolve CRITICAL-1 before this migration ships: the docs-protection branch
  (the asymmetric-cost gate that prevents auto-applying a code fix when the
  behavior is the documented contract) currently keys on a field the wire
  contract does not carry. Either drop to `remediation_target == "docs"` (lowest-risk,
  no producer change) or promote `behavior_is_documented` to a real 8th wire field
  in all three places (producer step 4.5 + report-template YAML + consumer Step 4 list).
- Resolve IMPORTANT-1 so the Step 5 insertion flow is internally consistent with
  the remediation-ownership decision (null is the normal path).
- Re-run this lens (fix-cycle) after edits to confirm `behavior_is_documented`
  is either removed from the consumer read-path or added to the wire set in all
  three locations.

## QA Complete
