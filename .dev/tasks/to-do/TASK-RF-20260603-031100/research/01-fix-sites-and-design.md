# Research: Reflect-V3-Serena audit remediation — verified fix sites + design

**Topic type:** File Inventory + Solution Research (consolidated)
**Scope:** the 4 sites flagged by the /sc:reflect UC-2 audit (REPORT.md at .dev/reflect/post-rv3low-impl-audit-20260602T211900/)
**Status:** Complete
**Date:** 2026-06-03
**Grounding:** every current-state line below was Read directly from disk this session (sed -n verified).

---

## F-1 (HIGH regression) — FR-8 C1 unbounded predicate inverted

**Site:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md:432` (§6.3 Retention sweep).
**Current (CODE-VERIFIED):**
> When `(slug_count − readonly_count) > 20` after the sweep, the budget cannot be met by deletion alone; emit `memory_retention_unbounded: true`...

`(slug_count − readonly_count)` = `deletable_count`. Fires on `deletable > 20` (the bounded case — sweep CAN delete down to 20). WRONG.

**Spec (CODE-VERIFIED, 04-spec-low-complexity.md:271,280):** C1 = emit the loud flag when read-only entries make the **≤20-TOTAL target unreachable** (25 total / 24 readonly / 1 deletable → must fire).
**Own fixture contradiction (CODE-VERIFIED, cases/serena-memory-retention/expected.yaml:21):** asserts `memory_retention_unbounded: true` for "25 total, 24 readonly, deletable=1" — protocol predicate computes `1 > 20 = false`.
**Fix design:** rewrite the predicate to fire on read-only-dominated total-unreachable, e.g.: `when slug_count > 20 AND (slug_count − readonly_count) ≤ 20` (total exceeds 20 but deletables are within budget → read-only are the cause). Reconcile SKILL.md:432 ↔ expected.yaml:21 wording. **This is the load-bearing fix (C1 = spec review's CRITICAL item).**

## F-2 (LOW regression) — FR-6 onboarding_status_source enum mismatch (3 sites)

**Spec (CODE-VERIFIED, 04-spec:239):** `onboarding_status_source: activation_msg | list_memories_proxy | unknown`.
**Sites (all CODE-VERIFIED current state):**
- `SKILL.md:230` → `(`activation_message` | `list_memories_proxy` | `none`)`
- `cases/serena-wave0-config/expected.yaml:20` → `onboarding_status_source: activation_message  # {activation_message, list_memories_proxy, none}`
- `evals/evals.json:527` → description text `... (activation_message | list_memories_proxy | none)`
**Fix design:** rename `activation_message`→`activation_msg` and `none`→`unknown` at all 3 sites. (`none`→`unknown` is the material one — aligns the SOURCE enum with the STATUS enum and FR-6.4.) Mechanical; no design choice.

## G-1 (follow-up) — report-template.md stale contract_version

**Site (CODE-VERIFIED):** `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:14` → `contract_version: 1.0.0` (hardcoded in the report-header yaml template).
**Context:** pre-existing (git-confirmed untouched by TASK-RF-20260602-135209); outside research-07's 5-site bump scope. After §9.1 bumped to 1.1.0 a generated REPORT.md header renders stale 1.0.0.
**Fix design:** change line 14 to `contract_version: 1.1.0`. Mechanical, low risk.

## G-2 (follow-up) — evals.json ids 22/24 yaml_list_contains won't grade

**Sites:** `.dev/eval-workspaces/sc-reflect/evals/evals.json` id 22 (`field_path: missing_implementations.0.abstract_name_path`, value `PaymentHandler`) + id 24 (`field_path: third_party_api_grounding.0.api_name`, value `fastapi.Depends`).
**Grader semantics (CODE-VERIFIED, grader.py:177-188):** `check_yaml_list_contains` resolves `field_path` via `reduce` (int-index for digits), then requires `isinstance(node, list)`. An indexed-scalar path (`...0.abstract_name_path`) resolves to a `str` → returns `False, "is not a list (got str)"`. Always-False at grade time. `missing_implementations` / `third_party_api_grounding` are **lists of dicts**, so `yaml_list_contains` cannot check a nested scalar member.
**Fix design (recommended):** replace the two `yaml_list_contains` assertions with `regex_present` against `with_skill/outputs/contract.yaml` for the value (`PaymentHandler` / `fastapi\.Depends`). Alternatives: (b) point `field_path` at a top-level scalar **list** if one exists; (c) add a scalar-capable grader assertion type (heavier — touches grader.py). Recommend (a) regex_present — minimal, no grader change. Apply uniformly to ids 22 AND 24.

## Conventions (CODE-VERIFIED from CLAUDE.md + prior task)

- SKILL.md + refs edits target `src/superclaude/` ONLY → `make sync-dev` → `make verify-sync`. NEVER stage `.claude/` mirrors.
- Eval-workspace edits (`.dev/eval-workspaces/`) are committed source but NOT sync-dev'd (no src mirror).
- markdownlint MUST count ALL rules (HEAD-vs-current full count), not just MD060 — a prior phase missed an MD032 from a `1a.`-list insertion.
- Preserve: corrected-form guards (`check_onboarding_performed`=0, `find_referencing_code_snippets`=0 in SKILL.md), no project-mutating Serena symbolic-editing tools, C2/C3/C4/C5 invariants, spec-mandated colon-namespaced degrade tokens.
- After edits: re-run the failing eval assertions' static checks; re-verify the F-1 fixture↔predicate reconciliation.

## Suggested phasing for the MDTM (Template 02)

- Phase 1: F-1 SKILL.md:432 predicate rewrite + expected.yaml:21 reconcile → sync-dev + verify-sync + all-rule markdownlint → rf-qa task-integrity gate.
- Phase 2: F-2 enum rename ×3 sites → sync-dev (for SKILL.md) + verify-sync + lint → rf-qa gate.
- Phase 3: G-1 report-template.md:14 bump → sync-dev + verify-sync + lint → rf-qa gate.
- Phase 4: G-2 ids 22/24 assertion swap (regex_present) → evals.json JSON-validity check (no sync-dev) → rf-qa gate.
- Phase 5: final rf-qa structural + rf-qa-qualitative pair across the whole change; confirm guards intact, contract_version consistent, JSON valid.

## AMBIGUITIES_FOR_USER
None blocking. G-2 has a small design choice (regex_present vs field_path change vs new grader type) — recommend regex_present; the builder should encode that as the default with the alternatives noted.
