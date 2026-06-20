# Research (Gap-Fill): contract_version resolution — Issue #1 from research-gate QA

**Topic type:** Gap-Fill (resolves rf-qa research-gate CRITICAL Issue #1)
**Scope:** SKILL.md §9.1 / §9.4 / §12.x contract_version + repo precedent
**Status:** Complete (round 2 — 5-edit set after adversarial QA found the L1503 5th site)
**Date:** 2026-06-02

---

## The conflict (as raised by rf-qa research-gate)

The 6 researchers documented BOTH sides of a `contract_version` literal conflict but did not converge:
- Spec mandates `contract_version: "1.1.0"` (3-segment), repeated 5× (spec L318/351/402/471/498).
- SKILL.md §9.4 **declares** the format as `"<major>.<minor>"` (2-segment) — `SKILL.md:640` [CODE-VERIFIED].
- SKILL.md §9.1 **current value** is `contract_version: "1.0"` (2-segment) — `SKILL.md:494` [CODE-VERIFIED]; heading also says `1.0` at `SKILL.md:491`.

## New evidence resolving the conflict (orchestrator-verified, 2026-06-02)

1. **§9.4's own versioning-rule bullets are written in 3-SEGMENT form** — `SKILL.md:642-644` [CODE-VERIFIED]:
   - Patch: `1.0.x`; Minor: `1.x.0`; Major: `X.0.0`.
   So §9.4's *semantics* already assume 3-segment `major.minor.patch`; only the format-declaration *string* at `SKILL.md:640` says 2-segment. The §9.4 section is internally inconsistent today.
2. **In-skill 3-segment precedent already exists**: `refs/report-template.md:14` uses `contract_version: 1.0.0` (3-segment) [CODE-VERIFIED]. The skill's own report artifact is already 3-segment.
3. Cross-skill precedent is mixed and NON-authoritative here: `sc-brainstorm-protocol/SKILL.md:338` = `"1.0"` (2-seg); `sc-cli-portify-protocol/SKILL.md:470` = `"2.0"` (2-seg). These are different skills' contracts and do not govern sc-reflect.

## RESOLUTION (authoritative directive for the builder)

Adopt **`contract_version: "1.1.0"`** (3-segment). Rationale: (a) the spec is the driving document and mandates it 5×; (b) it matches the skill's own `refs/report-template.md` (`1.0.0`); (c) it matches §9.4's own rule-bullet form (`1.x.0`). The only thing it contradicts is the stale format-declaration STRING at L640 — which is itself already contradicted by the bullets directly beneath it.

This converts the FR-1/2/4/5 contract bump into a **coordinated 5-edit set** (two extra edits beyond R1/R3's 3 sites). The 5th site (L1503) was surfaced by adversarial QA re-check and verified [CODE-VERIFIED] 2026-06-02 — ALL contract_version literal occurrences in SKILL.md were swept via `grep -nE 'contract_version'`:

| # | Site | Current (verified) | New | Source |
|---|------|---------|-----|--------|
| 1 | SKILL.md §9.1 heading `:491` | `### 9.1 Stable contract (contract_version: 1.0)` | `... (contract_version: 1.1.0)` | R1 #7 / R3 #5 |
| 2 | SKILL.md §9.1 value `:494` | `contract_version: "1.0"` | `contract_version: "1.1.0"` | R1 #7 / R3 #5 |
| 3 | SKILL.md §9.1 trailer `:599` | prose: `` Contract version is `v1.0`. `` (prose `v1.0`, NOT quoted) | `` Contract version is `v1.1.0`. `` | R1 #7 (anchor corrected to :599) |
| 4 | **SKILL.md §9.4 format-decl `:640`** | `` versioned via `contract_version: "<major>.<minor>"` `` | `... "<major>.<minor>.<patch>"` | gap-fill round 1 (NEW) |
| 5 | **SKILL.md §12.x falsifier/grader assertion `:1503`** | `` `return-contract.yaml contract_version == "1.0"` `` (table cell: "§9.1 versioned return contract stability" `yaml_field` assertion) | `... contract_version == "1.1.0"` | gap-fill round 2 (NEW — adversarial QA catch) |

**Do-NOT-edit (verified non-sites):** `SKILL.md:1289` is symbolic `"<contract_version from §9.1>"` — auto-tracks the bump, NO edit. The §9.4 rule bullets at `:644-646` (1.0.x / 1.x.0 / X.0.0) are already 3-segment — NO edit, they are the consistency target.

**Builder MUST** apply ALL FIVE edits as one atomic contract-bump item. Critical: edit #5 (`:1503`) is a falsifier/grader equality assertion — if §9.1 is bumped but L1503 is left at `"1.0"`, the "§9.1 versioned return contract stability" eval gate asserts `contract_version == "1.0"` and **fails on every run**. Edit #4 reconciles the L640 format-declaration string with its own 3-segment rule bullets + the §9.1 value + `report-template.md:14`.

**Note on edit #5's `return-contract.yaml` reference:** that grader assertion names `return-contract.yaml`, but OQ-5 confirmed no such file exists (contract is inline §9.1). The literal-version bump (`"1.0"`→`"1.1.0"`) is required regardless; whether the `return-contract.yaml` *filename* in that assertion also needs reconciliation to point at the inline §9.1 source is a PRE-EXISTING discrepancy — flag as a one-line Open Question for the builder, do NOT expand scope to fix it in this work unless trivially co-located.

## Issue #2 carry-forward (confirmed, no new research needed)

Spec L318 says the bump covers "FR-1/2/4/**8**"; spec L402 (authoritative, the telemetry-vs-contract split) says "FR-1/2/4/**5**". R3/R6 correctly adopted L402. Builder carries forward: the `contract_version` bump covers the four **contract-bearing** FRs **1/2/4/5**; FR-8's fields are §9.2 **telemetry** (no bump). [Resolved in research; recorded here for the builder's Open Questions.]
