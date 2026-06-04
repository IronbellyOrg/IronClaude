# Remediation context — Reflect-V3-Serena low-complexity audit findings

> **Purpose:** full-context input for a brainstorm→adversarial-validate→task-build→execute pipeline.
> **Source audit:** `.dev/reflect/post-rv3low-impl-audit-20260602T211900/REPORT.md` (UC-2, Tier 2, heterogeneous ensemble).
> **Driving spec (gold standard):** `.dev/releases/current/Reflect-V3-Serena/04-spec-low-complexity.md`.
> **Task under remediation:** `TASK-RF-20260602-135209` (8 Serena adoptions into sc-reflect-protocol).
> **All edits target `src/superclaude/skills/sc-reflect-protocol/` then `make sync-dev` + `make verify-sync`; NEVER stage `.claude/` mirrors.**

Brainstorm one best-fix proposal per issue below, adversarially validate the set, write a single MDTM remediation task file, then execute it with `/task`.

## Issue F-1 — REGRESSION (HIGH): FR-8 C1 unbounded-retention predicate inverted

- **Site:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md:432` (§6.3 Retention sweep, "Unbounded-gap loud flag (C1)").
- **Current (wrong):** fires `memory_retention_unbounded: true` when `(slug_count − readonly_count) > 20` — i.e. `deletable_count > 20`.
- **Spec (FR-8.6 / C1, `04-spec-low-complexity.md:271,280`):** fire when read-only entries make the **≤20-TOTAL target unreachable** (e.g. 25 total / 24 readonly / 1 deletable → `1 > 20 = false` → currently never fires, but the spec mandates it fire).
- **Internal contradiction:** the case's own eval fixture `.dev/eval-workspaces/sc-reflect/cases/serena-memory-retention/expected.yaml:21` asserts `memory_retention_unbounded: true` for 25/24/1 — protocol text disagrees with its own fixture.
- **Fix direction:** key the predicate on total-unreachable-due-to-readonly, e.g. `slug_count > 20 AND (slug_count − readonly_count) ≤ 20`. Reconcile SKILL.md:432 ↔ expected.yaml:21. C1 was the spec review's single provably-wrong (CRITICAL) item — this is the load-bearing fix.

## Issue F-2 — REGRESSION (LOW / mechanical): FR-6 onboarding_status_source enum mismatch

- **Sites:** `SKILL.md:230`; `.dev/eval-workspaces/sc-reflect/cases/serena-wave0-config/expected.yaml:20`; `.dev/eval-workspaces/sc-reflect/evals/evals.json:527`.
- **Current (wrong):** `activation_message | list_memories_proxy | none`.
- **Spec (FR-6.1, `04-spec-low-complexity.md:239`):** `activation_msg | list_memories_proxy | unknown`.
- **Fix direction:** rename `activation_message`→`activation_msg` and `none`→`unknown` across all three sites (`none`→`unknown` is the material one — `unknown` aligns with the §9.2 `onboarding_status` enum and FR-6.4).

## Issue G-1 — follow-up: report-template.md stale contract_version

- **Site:** `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md:14` — hardcoded `contract_version: 1.0.0`.
- **Context:** pre-existing (git-confirmed untouched by the task); outside research-07's 5-site bump scope. After the §9.1 bump to 1.1.0 a generated REPORT.md header would render the stale 1.0.0.
- **Fix direction:** bump to `1.1.0` for contract consistency (low risk, mechanical).

## Issue G-2 — follow-up: evals.json yaml_list_contains indexed-scalar field_path won't grade

- **Sites:** `.dev/eval-workspaces/sc-reflect/evals/evals.json` eval ids 22 (`missing_implementations.0.abstract_name_path`) and 24 (`third_party_api_grounding.0.api_name`).
- **Context:** `grader.py` `yaml_list_contains` (grader.py:177-183) requires the resolved node to be a LIST; an indexed-scalar field_path resolves to a string → always-False at grade time. Harmless for un-graded scaffolds; must be fixed before scaffold promotion.
- **Fix direction:** choose one — (a) switch to a list-membership-friendly field_path, (b) use `regex_present` against the YAML, or (c) add a scalar-capable grader assertion type. This is the issue with the most genuine design choice.

## Out-of-scope guardrails (do NOT regress)

Keep adherent: corrected-form guards (`check_onboarding_performed`=0, `find_referencing_code_snippets`=0 in SKILL.md), no project-mutating Serena symbolic-editing tools in allowed-tools, the 5-site contract bump (SKILL.md), §9.1/§9.2 fence discipline, C2/C3/C4/C5 invariants, the spec-mandated colon-namespaced degrade tokens. The 136 pre-existing MD060 lint violations are out of scope.
