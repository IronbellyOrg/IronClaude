# Research: Command + Output Contract Integration

**Topic type:** Integration Points
**Scope:** troubleshoot.md + SKILL.md output contract
**Status:** Complete
**Date:** 2026-06-10

**Summary:** The command (`commands/troubleshoot.md`, 201 lines) advertises via `description` (L3) + Behavioral Summary (L60-67) and hands off at the Activation section L80 (`> Skill sc:troubleshoot-protocol`). "Keep thin" is enforced in-file at L62 + L82 — command edits must be advertising-only (description, Behavioral Summary step 4 / L67, `--output-dir` artifact list / L56, optional boundary line); NO hardening logic. The skill's output contract is a **markdown table** at SKILL.md L37-61 (NOT JSON/YAML); spec §6.2's 8 fields append cleanly after L61. A YAML-in-HTML-comment audit footer (L413-424) carries a curated subset. The downstream chain (Wave 5 close L411-433 → Tier 3 Wave 6 L437-451 → task-builder → reflect/auggie-review) already wires the off-path reviewers H5 needs; a `blocked` closure verdict should gate the `success`-only Tier 3 precondition (L439) the way dropped citations set `status: partial` (L409-410). Existing optional-field precedents to mirror: `diagnosability_verdict` (L58, `unknown`/never-silently-skipped) for `pipeline_hardening_verdict`/`not_applicable`; `doc_context_card_path` (L52, `string|null`) for the 4 path fields; `diagnosability_hard_stop` (L61, bool) for `pipeline_hardening_applicable`.

---

## 1. `commands/troubleshoot.md` — full content map (201 lines)

File: `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`

### 1.1 Frontmatter (lines 1-9)

```yaml
name: troubleshoot
description: "Tiered debugging — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in task-builder remediation chain"   # line 3
category: analysis
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
argument-hint: "[<issue description>] [--type ...] [--depth ...] [--scope ...] [--no-escalate] [--fix] [--models ...] [--output-dir ...] [--no-doc-discovery] [--no-mcp]"   # line 8
```

- The `description` (line 3) is the user-visible advertisement string. **Spec §5.1 bullet 1** ("update the behavioral summary to advertise pipeline hardening...") most naturally extends the Behavioral Summary block (§1.2 below) and optionally this `description` — but note R1/R5 own the description-vs-skill-description sync. The `argument-hint` (line 8) is the flag inventory; spec §5.1 introduces **no new flags** (hardening is auto-triggered, not flag-gated), so `argument-hint` need not change.

### 1.2 Behavioral Summary block (lines 60-75) — QUOTED

This is the block spec §5.1 bullet 1 targets ("update the behavioral summary to advertise pipeline hardening"). Current text, lines 60-67:

```
## Behavioral Summary

The full multi-wave protocol lives in the skill. The command file performs only:

1. **Parse arguments** → resolve `--type` (auto-detect if absent), `--scope`, `--depth`, etc.
2. **Validate environment** → at least one of MCPs is available (or `--no-mcp` is set); output dir is writable.
3. **Hand off to the skill** via the Activation section below.
4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, and (if `--fix`) the Tier 3 remediation offer.
```

- Line 62 is the **load-bearing "keep thin" sentence**: *"The full multi-wave protocol lives in the skill. The command file performs only:"* — this is the in-file enforcement of acceptance criterion #1.
- Lines 64-67 enumerate the 4 command-only actions. **Step 4 (line 67)** is the *output-surfacing* contract: "surface: REPORT path, tier reached, confidence, chosen fix, and (if `--fix`) the Tier 3 remediation offer." This is the spot where spec §5.1 bullet 2 ("extend the output description to mention hardening evidence paths when the protocol enters pipeline-hardening mode") lands — additively append a hardening clause (e.g. "...and (when pipeline-hardening mode ran) the closure verdict + hardening evidence paths").
- The three-tier table follows at lines 69-75 (Tier 1 / Tier 2 / Tier 3 "When/What/Cost"). Pipeline Hardening Closure is a *new mode* (spec §6) that runs **after Tier 1 diagnosis, before report closure** (spec §5.2 bullet 1) — it is NOT a 4th tier. A thin command-side mention can be one advisory sentence near this table; the mode mechanics stay in the skill.

### 1.3 Output description / surfacing — there is no standalone "Output" section

The command has **no dedicated `## Output` heading**. The output description is split across two places:
- **Behavioral Summary step 4 (line 67)** — the in-chat surfacing list (above).
- **Options table `--output-dir` row (line 56)**: *"Where REPORT.md, hypothesis cards, fix proposals, adversarial artifacts, and audit log are written."* — Spec §5.1 bullet 2's "output description" can be read as this enumeration of artifacts written to the output dir. Adding hardening artifacts (runtime-entrypoint card, contract ledger, unmask-sweep, effective-input card) to this list is the thin, additive change.

### 1.4 Handoff line to the skill (lines 77-82) — EXACT

The handoff is the **Activation** section:

```
## Activation                                                          # line 77

**MANDATORY**: Before executing any protocol steps, invoke:            # line 79
> Skill sc:troubleshoot-protocol                                       # line 80

Do NOT proceed with protocol execution using only this command file. The full behavioral specification — wave structure, escalation rubric, agent selection, file:line validation, hallucination contract, remediation chain — is in the protocol skill.   # line 82
```

- **Line 80** is the literal handoff: `> Skill sc:troubleshoot-protocol`.
- **Line 82** already lists the categories of logic that live ONLY in the skill ("wave structure, escalation rubric, ... remediation chain"). The cleanest additive edit is to append "pipeline hardening closure" to that enumeration so the command keeps advertising the seam without duplicating logic.

### 1.5 Boundaries blocks that mention output discipline

- **Will list (lines 158-168)** and **Will Not list (lines 170-180)**: these are behavioral guarantees. Spec acceptance #1 ("thin command") is reinforced here, but no hardening logic should be added — at most a one-line "Will: enter Pipeline Hardening Closure when the diagnosed issue is a pipeline escape (mechanics in the skill)".
- **CRITICAL BOUNDARIES (lines 182-192)** — diagnose-first / `--fix` discipline. Unaffected by hardening; hardening is a *proof gate*, not a code-applier.
- **Related Commands (lines 194-201)** — lists `/sc:reflect`, `task-builder`, `/sc:adversarial`, `/sc:auggie-review`. The hardening mode's off-path-reviewer rule (spec §6/H5) leans on `/sc:reflect` and `/sc:auggie-review`, which are already listed — no new command relationship needs introducing.

### 1.6 "Keep thin" constraint — CONFIRMED (acceptance #1)

- Enforced in-file at **line 62** ("The command file performs only:") and **line 82** ("Do NOT proceed with protocol execution using only this command file... is in the protocol skill").
- **Spec §5.1 bullet 3** ("Keep the command thin... hardening logic belongs in the skill and refs") + **acceptance #1** ("`/sc:troubleshoot` remains a thin command handoff and does not duplicate heavy protocol logic").
- **Builder constraint:** command-side edits MUST be limited to *advertising* (description, Behavioral Summary step 4, `--output-dir` artifact list, one boundary/tier-table mention). The H0–H5 waves/gates, the closure verdict logic, and the evidence-card templates MUST live in SKILL.md + new refs (spec §9). Do NOT replicate any of §6.2's verdict computation or §7's gate blocking rules into the command file.

---

## 2. The skill's OUTPUT CONTRACT / result object

File: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (548 lines)

### 2.1 Where the contract is defined — TWO surfaces

The structured result has **two co-existing representations** the spec §6.2 fields must be added to:

**(A) The "Output Contract" markdown table (lines 37-61)** — the canonical field list. Header at **line 37-39**: *"## Output Contract / The skill returns a structured dictionary on completion:"*. It is a **3-column markdown table** (`| Field | Type | Description |`, line 41-42). This is **NOT** YAML/JSON/frontmatter — it is a documented dictionary spec rendered as a table. **This is the primary surface spec §6.2's 8 new rows get appended to** (after line 61).

**(B) The audit-log machine-readable footer (lines 413-424)** — an HTML-comment block emitted at end of Wave 5:

```text
<!-- SC:TROUBLESHOOT:SUMMARY
status: <success|partial>          # line 415
tier_reached: <1|2|3>
confidence: <float>
escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>
hypothesis_count: <N>
adversarial_invoked: <bool>
fix_authorized: <bool>
duration_sec: <N>
-->                                # line 424
```

This is **YAML-style key:value inside an HTML comment** (`SC:TROUBLESHOOT:SUMMARY` sentinel). NOTE: this footer is a **subset** of the table (A) — it does NOT mirror every table field today (e.g. `test_is_wrong`, `doc_context_card_path`, `diagnosability_*` are in the table but NOT in the footer). So the builder is NOT obligated to add all 8 §6.2 fields here; precedent is "footer carries a curated subset." A minimal hardening footer addition would be `pipeline_hardening_applicable` + `pipeline_hardening_verdict`.

**(C) REPORT.md frontmatter (report-template.md lines ~8-26)** — the user-facing `**Key**: <value>` bold-key list (Target/Type/Tier reached/Confidence/Status/Escalation reason/Test is wrong/Test file to update/Behavior is documented/Doc context card/Diagnosability audit/Duration/Date). This is a **third surface** but R3 owns report-template.md; flagged here only so the builder threads §8's `## Pipeline Hardening Closure` section consistently. The spec §8 already provides the exact REPORT.md section block.

### 2.2 Current field list — QUOTED with line refs (table A)

| Line | Field | Type |
|---|---|---|
| 43 | `status` | string (`success`/`partial`/`failed`) |
| 44 | `tier_reached` | int (1,2,3) |
| 45 | `report_path` | string (absolute) |
| 46 | `audit_log_path` | string (absolute) |
| 47 | `confidence` | float 0.0-1.0 |
| 48 | `escalation_reason` | string |
| 49 | `test_is_wrong` | bool |
| 50 | `test_file_path` | string \| null |
| 51 | `behavior_is_documented` | bool |
| 52 | `doc_context_card_path` | string \| null |
| 53 | `hypothesis_cards` | list[path] |
| 54 | `adversarial_artifacts_dir` | string |
| 55 | `task_file_path` | string |
| 56 | `remediation_offered` | bool |
| 57 | `remediation_accepted` | bool |
| 58 | `diagnosability_verdict` | string (`sufficient`/`partial`/`insufficient`/`unknown`) |
| 59 | `diagnosability_context_card_path` | string \| null |
| 60 | `diagnosability_tasklist_path` | string \| null |
| 61 | `diagnosability_hard_stop` | bool |

**Insertion point for §6.2's 8 new fields:** immediately after line 61 (end of the table, before the blank line at 62 and the `**test_is_wrong** derivation rule` prose at line 63). The 8 new rows (`pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path`, `off_path_review_decision`, `known_escapes_caught`) append cleanly as 8 more `| field | type | desc |` rows — purely additive, no existing row changes.

### 2.3 Format confirmation

- Primary contract = **markdown table** (not JSON/YAML object literal). Type column already uses the `string | null` and `list[path]` conventions §6.2's `string | null` / `list[string]` types match exactly.
- Machine footer = **YAML-ish key:value in an HTML comment** with the `SC:TROUBLESHOOT:SUMMARY` sentinel (line 414).
- REPORT.md = **bold-key list** frontmatter-style block (R3's territory).

---

## 3. Downstream handoff chain (where new hardening verdicts/paths thread)

The chain runs: **Wave 5 (report closure) → output contract → Wave 6 (Tier 3 remediation) → task-builder → /sc:reflect → /task → /sc:reflect validate**. Pipeline Hardening Closure inserts **between Wave 1 diagnosis and Wave 5 report closure** (spec §5.2 bullet 1), so its verdicts are computed *before* the contract is finalized and *before* the Tier 3 offer.

### 3.1 Wave 5 → contract → user surface (SKILL.md lines 411-433)

- Line 411-424: audit-log footer emitted (contract surface B).
- Line 426-431: in-chat surface to user (summary, REPORT path, chosen fix, tier+confidence, next-step). **Line 433 exit criteria:** *"If `--fix` is not set, return the output contract and STOP."* — so the contract (with new hardening fields) is the terminal deliverable for the no-`--fix` path. New hardening verdicts/paths must be populated before this return.

### 3.2 Wave 6 Tier 3 remediation handoff (SKILL.md lines 437-451)

- **Precondition (line 439):** `--fix` set AND `REPORT.md` is `success` (NOT `partial`) AND user accepts.
- Phase A (line 445): invokes `task-builder` via `Skill` with a `BUILD_REQUEST` (GOAL="Apply the fix described in `<REPORT.md path>`", WHY=summary, WHERE=cited files, TEMPLATE=01 generic / 02 complex).
- Phase B (line 446): `/sc:reflect --type task --analyze` against the new task file.
- Phase C (line 447): execution gate — surfaces literal `/task <path>`; user runs it.
- Phase D (line 448): `/sc:reflect --type task --validate` (or `self-review` fallback) post-execution.

**Threading point for hardening:** spec §8 says a pipeline escape **cannot be marked remediated** when required hardening gates are missing/failed/`N/A`-without-rationale, and §314 says use `NOT PROVEN` blockers. This interacts with the Wave 6 precondition at **line 439** (`success` not `partial`). The builder should consider: a `pipeline_hardening_verdict=blocked` should force `status: partial` (or block the Tier 3 offer) the same way dropped evidence citations do (lines 409-410 set `status: partial`). That is the seam where the closure verdict gates the remediation offer.

### 3.3 remediation-handoff.md seam (refs/remediation-handoff.md)

File: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`

- Header: *"Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report."* — reaffirms the `success`-gates-remediation seam. The user-offer prompt block enumerates the chain (build MDTM → reflect analyze → `/task` → reflect validate). Decision matrix maps yes/no → `remediation_accepted`. Phase A constructs the `BUILD_REQUEST` from the report.
- **Seam for hardening:** the offer prompt's "Fix to be applied / Files that will change" pull from REPORT.md sections. If the hardening closure adds a `## Pipeline Hardening Closure` section (§8), the offer could optionally surface the closure verdict so the user sees hardening status before accepting. (R3 owns the failure-state model of this file — flagged for the seam only.)

### 3.4 Onward to reflect / auggie-review (off-path-reviewer rule, spec §6/H5)

- Spec H5 (off-path-reviewer rule) names acceptable off-path forms: adversarial review, **independent reflect review with effective-input proof**, runtime smoke/e2e, consumer-side ledger audit, heterogeneous reviewer. The command already lists `/sc:reflect --type task` (line 198) and `/sc:auggie-review` (line 201) as Related Commands, and `/sc:adversarial` is invoked in Wave 4 (line 196). So the off-path reviewer the H5 rule needs is **already wired into the chain** — no new command relationship is required; the hardening mode just *invokes the existing reflect/auggie-review/adversarial seams* and records the `off_path_review_decision` field.

---

## 4. Existing optional-field / not_applicable patterns to MIRROR

Spec §6.1 requires `pipeline_hardening_applicable=false` (+ one-sentence reason) when the mode is skipped near a pipeline boundary. The contract **already has multiple precedents** for optional/skip-state fields the new fields should mirror:

1. **`string | null` skip sentinel** — `test_file_path` (line 50), `doc_context_card_path` (line 52), `diagnosability_context_card_path` (line 59), `diagnosability_tasklist_path` (line 60). All use `null` to mean "not produced / wave skipped." → `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path` should be `string | null` with `null` = "gate did not run", matching §6.2's stated `string | null` type exactly.

2. **`unknown` / skipped-but-never-silent verdict enum** — `diagnosability_verdict` (line 58): *"default `unknown` when audit could not run ... never silently skipped"*. This is the **closest precedent** for `pipeline_hardening_verdict` (§6.2 enum `pass`/`blocked`/`advisory`/`not_applicable`). The `not_applicable` value directly mirrors `diagnosability_verdict=unknown`'s "skipped but explicitly recorded" semantics. The builder should adopt the same "never silently skipped — record `not_applicable` + reason" discipline (which aligns with spec §6.1's mandatory one-sentence reason and §7 H0's "if skipped, report must state the concrete reason and boundary scan").

3. **`bool` applicability flag** — `diagnosability_hard_stop` (line 61, bool) and `remediation_offered`/`remediation_accepted` (lines 56-57, bool) are precedent for `pipeline_hardening_applicable` (bool, §6.2). `diagnosability_hard_stop` is also described as *"mutually informative with existing `status: partial`"* — the same coupling the hardening `blocked` verdict should have with `status` (see §3.2).

4. **Skip-state handled in the State / failure-state tables** — SKILL.md has explicit failure-state rows (lines 184-189 for Wave 1.5, 240-245 + 506-522 for Wave 1.6) that document `--no-doc-discovery` / `--no-diagnosability-audit` skip behaviors and what contract value gets emitted. The new hardening waves should add analogous rows so the `applicable=false` / `not_applicable` paths are explicitly enumerated, not implicit. R3 owns the failure-state model details; this confirms the structural precedent exists.

**Net mirror recipe for the builder:**
- `pipeline_hardening_applicable` → bool, mirror `diagnosability_hard_stop`.
- `pipeline_hardening_verdict` → enum incl. `not_applicable`, mirror `diagnosability_verdict`'s "never silently skipped" rule.
- 4 `*_card_path` / `*_ledger_path` / `*_sweep_path` fields → `string | null`, mirror `doc_context_card_path`.
- `off_path_review_decision` → enum string, no null precedent needed (always has a value: `required`/`performed`/`waived_with_rationale`/`not_required`); closest analog is `escalation_reason` (line 48, always-present string).
- `known_escapes_caught` → `list[string]`, mirror `hypothesis_cards` `list[path]` (line 53) for the list-type convention.
