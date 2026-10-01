# R2 Research: SKILL.md CONTRACT + CLASSIFY + FAIL-OPEN Anchors

Status: Complete
Date: 2026-06-20
Researcher: R2 of 5 (Track 1)
Scope: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` ONLY — contract/taxonomy/fail-open sections.

---

File: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — CURRENT total = **1854 lines**.

## Site 1 — §9.1 Stable contract block + UC-2 field region (FR-RSR.7 append target)

- **§9.1 header:** `SKILL.md:660` — `### 9.1 Stable contract (contract_version: 1.5.0)`.
- **contract_version value (VERIFIED `"1.5.0"`):** `SKILL.md:663` —
  `contract_version: "1.5.0"   # 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; ...`
  - Confirmed at 3 sites: `:663` (the field), `:804` (`Contract version is `v1.5.0`.`), and the kill-list/invariant test at `:1772` (`return-contract.yaml contract_version == "1.5.0"`). FR-RSR (minor-bump per §9.4) would take this to **`"1.6.0"`** and ALL THREE sites must move together.
- **UC-2 specific region:** opens at `SKILL.md:689` (`# UC-2 specific`) and runs through the Reuse-Miss sub-block. The natural append point for FR-RSR.7's 6 fields is the **end of the UC-2 block** — after the `verification_*` cluster (`:705-709`) and BEFORE the `# Reuse-Miss neighbour sweep` comment at `:711`. (Reuse-Miss is its own labeled sub-section; new runtime-surface fields should get their own `# Runtime-surface reachability (FR-RSR — UC-2)` comment banner to match house style.)
- **Field-list shape/style to MATCH** (each line: `field_name: <type/enum> | null   # FR-tag (one-line semantics)`), e.g.:
  - `:705` `verification_ran: <bool>                   # FR-4 (UC-2 verification triangle, §6.1 step 5.5)`
  - `:708` `verification_regressions_detected: <int>   # FR-4 (taxonomy-classified Regression exits on a claimed-passing file)`
  - `:712-720` the Reuse-Miss cluster shows the pattern for a list-typed + scalar mix, incl. `reuse_verdict_count_by_type: { ... }` inline-dict style and `<abs path> | null`.
- **FR-RSR.7's 6 additive fields** (append here, FR-RSR-tagged):
  `runtime_surface_requirements: [<list str>]`, `runtime_surface_sweep_ran: <bool>`, `runtime_surface_ledger_path: <abs path> | null`, `runtime_surface_unreached: <int>`, `runtime_surface_degraded: <bool>`, `unreached_surfaces: [<list of UnreachedSurface>]`.
- **NOTE for §9.4 compliance:** the comment at `:663` is the canonical changelog string; a 1.6.0 bump should APPEND `; 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields)` to it, matching the existing additive-changelog convention.

## Site 2 — §9.3 Consumer Field Map (advisory UC-2 consumer row + sprint/executor.py rollback row)

- **§9.3 header:** `SKILL.md:851` (`### 9.3 Consumer Field Map`). Intro at `:853` notes "60+ fields" and that **adding a field to a consumer's load-bearing row requires a contract version bump per §9.4**.
- **Table header:** `:855` (`| Consumer | Surface | Load-bearing fields (3-5) | Routing semantics |`), divider `:856`.
- **Sprint/executor.py rollback row (the `regression` → TurnLedger rollback consumer):** `SKILL.md:858` —
  `| **`superclaude sprint run` (executor.py TurnLedger)** | CLI consumer of return-contract.yaml | `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`, `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade` | ... `deviation_class == regression` triggers TurnLedger rollback; ... |`
  - NOTE: the TurnLedger rollback trigger here reads `per_task_verdicts[].deviation_class == regression`, NOT a top-level `deviation_count_by_class.regression`. (A SECOND consumer — `sc-task-protocol` end-of-task hook at `:859` — reads `deviation_count_by_class.regression > 0` → "escalate to troubleshoot".) The TDD's phrasing "reads deviation_count_by_class.regression and triggers TurnLedger rollback" conflates two distinct rows; the **rollback** is the executor.py row at `:858` keyed on `per_task_verdicts[].deviation_class`.
- **Existing advisory-row template to MIRROR for a new UC-2 advisory consumer:** `SKILL.md:862` —
  `| **Any UC-1 consumer (advisory, D13)** | Optional read | `coverage_degraded`, `coverage_pct_union`, `unmapped_requirements_union` | NON-GATING advisory: ... Existing consumers need no change ... |`
  - A new FR-RSR advisory UC-2 row should be inserted in this table (recommended adjacent to `:862`, or after the sprint/task consumer rows) reading the `runtime_surface_*` fields as NON-GATING advisory, matching this exact "Optional read / NON-GATING advisory" shape.
- **Field-deletion guard line:** `SKILL.md:868` —
  `**Field-deletion guard.** Removing or renaming a field listed here is a **breaking change** that requires a contract major-version bump (§9.4). Additions are minor-version bumps. ...`

## Site 3 — §9.4 Contract Evolution / versioning rules

- **§9.4 header:** `SKILL.md:870` (`### 9.4 Contract Evolution`). Versioning preamble `:872`.
- **Minor-bump definition (the FR-RSR governing clause):** `SKILL.md:877` —
  `- **Minor (1.x.0):** purely additive change — new top-level field(s) added, no existing field renamed/removed/retyped, no semantic change to existing fields. Forward-compatible: consumers MUST tolerate unknown top-level fields (read-and-ignore). Consumers that wish to use the new field opt in by reading it explicitly.`
- Patch rule `:876`; Major rule `:878`.
- **Read-and-ignore forward-compat (the consumer obligation that makes FR-RSR safe):** `SKILL.md:895` —
  `**Unknown-field tolerance (forward-compat).** All consumers MUST treat unknown top-level fields as read-and-ignore. A consumer that fails on an unknown field is non-conforming and breaks the minor-release additive guarantee.`
  - Implication for FR-RSR: appending 6 `runtime_surface_*` fields = pure minor bump (1.5.0 → 1.6.0); NO consumer in §9.3 needs to change; existing consumers read-and-ignore.

## Site 4 — §10 Deviation Taxonomy (classify sites + end-of-§10 insertion point for new §10.9)

- **§10 header:** `SKILL.md:899` (`## 10. Deviation Taxonomy`); "4-category taxonomy (not 5)" stated `:901`.
- **§10.3 Drift** — header `SKILL.md:937`; definition "silent change not in the original spec/tasklist with no inline rationale" `:939`; the **needs-unmapped-hunk detection signal** at `:943` (`Diff hunk does NOT map to any tasklist item.`) + `:945` (does NOT contradict any criterion — distinguishes drift from regression).
- **§10.4 Regression** — header `SKILL.md:952`; definition "contradicts an acceptance criterion ... or a previously-passing test" `:954`; **the contradicted-criterion detection** at `:958`. The exit-code-sourcing-into-`verification_regressions_detected` mechanic (step 5.5) at `:959` (`... a non-zero exit that the exit-code taxonomy ... classifies as Regression sets `verification_regressions_detected += 1` then `regression_present: true` ...`). Exit-code→class taxonomy table `:962-974`.
- **§10.5 Classification precedence** — `SKILL.md:980` (header), `:982`: precedence **Regression > Drift > Necessary > Authorized**; `rationale does not authorise contradiction` (the "rationale does not override a contradiction" line). Also stated at `:905` (large-diff scaling) and `:974`.
- **§10.6 Grounding Gaps** — header `SKILL.md:984`; required-fields YAML `:988-1000`; the `needs_human_decision: true` + `status: partial` forcing at `:1004-1005`. Cross-ref to §17.7 kill list at `:1008`.
- **§10.8 Reuse-Miss finding-modifier (THE pattern §10.9 mirrors):** header `SKILL.md:1014` (`### 10.8 Reuse-Miss (finding modifier — NOT a 5th deviation class)`). Maps-onto-the-4-by-evidence rule `:1016-1023`; "no `deviation_count_by_class.reuse_miss` counter (§17.7)" at `:1025`. This is the canonical "finding modifier, NOT a 5th class, maps onto existing 4 by evidence" template that a new §10.9 (runtime-surface reachability as a finding modifier) must mirror.
- **§10.7 Reporting** sits BETWEEN: `SKILL.md:1010` (header `### 10.7 Reporting`). So §10 order is 10.1–10.6, 10.7 Reporting, 10.8 Reuse-Miss.
- **EXACT end-of-§10 insertion point for a NEW §10.9:** §10.8 ends at `SKILL.md:1025` (the "Default remediation." line). The section terminator `---` is at `SKILL.md:1027` (blank line `:1026`). A new `### 10.9 ...` subsection must be inserted **between line 1025 and the `---` at line 1027** (i.e., a new block after `:1025`, before `:1027`), so it lands inside §10 and ahead of §11 (`## 11. Hallucination Guardrails` at `:1029`).

## Site 5 — §17.7 Kill List item 6 (rejects a 5th deviation class)

- **§17.7 header:** `SKILL.md:1785` (`## 17.7 Kill List — Features Deliberately Excluded`).
- **Item 6 (the 5th-class rejection — FR-RSR.6 must add NO 5th class / NO new counter):** `SKILL.md:1799` —
  `6. **5th `unknown` deviation category in deviation-ledger** — Rejected because structural cleanliness requires the 4-category ledger to remain pure; insufficient-evidence findings route to a *separate* artifact (`grounding-gaps.yaml`) with required-field rigor. *Replaces with:* §10.6 Grounding Gaps parallel artifact.`
- Reinforcing anchors: `:1008` ("See §17.7 Kill List for why a 5th deviation category was rejected"), `:1686` ("Route evidence-insufficient findings to `grounding-gaps.yaml` (§10.6), NOT to a 5th deviation category"). Constraint for FR-RSR.6: runtime-surface reachability is a **finding modifier (like §10.8)**, maps onto the existing 4 classes by evidence, adds NO `deviation_count_by_class.runtime_surface` key.

## Site 6 — §0.5d availability surface (backend/chain-degraded report — FR-RSR.8 consumer)

- **Wave-map reference:** `SKILL.md:137` (`0.5d verification/adoption availability probe (backend + execute_shell_command + onboarding + read_only — consume 0.5c snapshot)`).
- **§0.5d body:** `SKILL.md:242` (`**Step 0.5d (verification & adoption availability probe — M-ARC3 four-field contract).**`).
- **Four-field availability contract YAML:** `SKILL.md:244-250`:
  `backend: jetbrains | lsp | none` (`:246`), `execute_shell_command_available: <bool>` (`:247`), `onboarding_available: <bool>` (`:248`), `read_only: <bool>` (`:249`).
- **Where backend/chain-degraded is reported (FR-RSR.8 consumer surface):** the **Fail-open clause** at `SKILL.md:261` —
  `**Fail-open (§6.5):** any parse failure of any field → set that field to its unavailable value (`backend: none` / `*_available: false` / `read_only` unconfirmed → treat triangle as disabled), emit the matching skip reason to the consuming FR's telemetry, and continue. This step never STOPs the skill.`
  - `backend: none` is the degraded/unavailable sentinel FR-RSR.8 reads to decide whether a runtime-surface sweep can run; the `:259` Consumption rule ("do NOT re-probe downstream") is the binding contract for any FR-RSR consumer (READ this Wave-0 field, do not re-derive).

## Site 7 — `degraded_components` telemetry list (FR-RSR.8 appends `"runtime-surface:backend_unavailable"`)

- **Canonical telemetry declaration:** `SKILL.md:815` (in §9.2 Telemetry) —
  `degraded_components: [<list>]   # e.g. ["auggie", "evidence-validator", "env-aliases"]`
- **Append-convention precedents (the `"<component>:<reason>"` slug style FR-RSR.8 must match):**
  - `:237` `append `"serena:context-excluded"` to `degraded_components``
  - `:471` `degraded_components += "neighbour-search:auggie_unavailable"; NEVER STOP.`
  - `:484` `degraded_components: ["search_deps:lsp_unindexed"]`
  - `:271` `degraded_components: ["serena:onboarding-parse"]`
  - `:542` `degraded_components: ["serena:pre-v1.5-no-rename-propagation"]`
  - `:488` (`"type_hierarchy:backend_error"`)
- FR-RSR.8's `"runtime-surface:backend_unavailable"` slug matches this `prefix:reason` convention exactly. Also surfaced in the JSON audit-log emission at `:1616` (`"degraded_components": [<list of strings>],`).

## Site 8 — "Will Not run /task" invariant (reflect AUTHORS, never executes — NG5)

- **§"Will Not" section header:** `SKILL.md:1700` (`### Will Not`).
- **The invariant line:** `SKILL.md:1705` —
  `- Auto-execute a Tier 3 remediation task — task-builder produces a file, the user runs `/task <path>`.`
- **Reinforcing in-body anchors (reflect AUTHORS but NEVER runs /task):**
  - `:339` (`Either way reflect AUTHORS but NEVER runs `/task` (§"Will Not").`)
  - `:348` (`This is the path-EMISSION only — reflect AUTHORS but NEVER runs `/task` (the §"Will Not" invariant is preserved); ...`)
  - `:757` (`remediation_task_path` semantics — reflect emits the path; the reflect-wrapper auto-fix loop is the sole auto-runner).
- Constraint for FR-RSR: any runtime-surface remediation output must follow the SAME author-not-execute discipline — emit a path / register entry, never auto-run `/task`.

---

## Summary (R2)

All 8 sites re-anchored against the CURRENT 1854-line SKILL.md. Key re-anchoring deltas vs the TDD's older revision:

- **contract_version is `"1.5.0"`** (VERIFIED) at THREE sites that must move in lockstep on a 1.6.0 minor bump: `:663` (field + changelog comment), `:804` (prose), `:1772` (kill-list invariant test). FR-RSR is a clean §9.4 **minor** bump (purely additive, `:877`); existing §9.3 consumers read-and-ignore (`:895`) — no consumer change needed.
- **FR-RSR.7 6-field append point:** end of `# UC-2 specific` block, between `:709` and the `# Reuse-Miss` banner at `:711`. Match the `field: <type> | null   # FR-tag (semantics)` style.
- **§9.3 advisory-row template** to mirror = `:862` ("Optional read / NON-GATING advisory"). Field-deletion guard = `:868`. CORRECTION: TurnLedger **rollback** is the executor.py row at `:858` keyed on `per_task_verdicts[].deviation_class == regression` — NOT `deviation_count_by_class.regression` (that key drives the `sc-task-protocol` escalate-to-troubleshoot row at `:859`).
- **NEW §10.9 insertion point:** strictly between `:1025` (end of §10.8) and the `---` at `:1027`. §10.8 (`:1014`) is the exact "finding modifier, NOT a 5th class, maps onto 4 by evidence" pattern to mirror.
- **§17.7 item 6** at `:1799` is the binding rejection of a 5th class/counter (FR-RSR.6 constraint).
- **§0.5d** four-field contract at `:244-250`; degraded reporting via fail-open `:261` (`backend: none` sentinel) + `degraded_components` at `:815` using the `prefix:reason` slug convention. The "do-not-re-probe" consumption rule is `:259`.
- **NG5 "Will Not run /task"** invariant at `:1705` (reinforced `:339`, `:348`, `:757`).

Status: Complete.
