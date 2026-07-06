# Research: SKILL.md Structural Map

**Topic type:** File Inventory + structure
**Scope:** src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
**Status:** Complete
**Date:** 2026-06-10

---

> NOTE: File is **549 lines** as of read (brief said 548; off by one — confirmed by Read).

## 0. Top-level section index (line ranges)

| Lines | Section | Role for hardening builder |
|---|---|---|
| 1–5 | YAML frontmatter (`name`, `description`, `allowed-tools`) | §7 below — extend description if mode is advertised |
| 7–12 | Extended-metadata HTML comment (category/complexity/mcp/personas) | non-parsed; informational |
| 14–24 | `# Troubleshoot Protocol` / `## Purpose` (+ Core contract, Why this works, Hallucination contract) | framing; H0 mechanism-statement house style |
| 26–35 | `## Required Input (STOP if missing)` | existing STOP wiring example |
| 37–75 | `## Output Contract` (table 41–61 + derivation rules 63–75) | **§3 — extend table with new fields here** |
| 77–93 | `## Wave Structure` (ASCII map 79–91) | **§2/§6 — insert H-waves into this map** |
| 95–453 | Per-wave detail sections (Wave 0 → Wave 6) | **§1/§2 — hardening trigger goes between Wave 1.7 and Wave 5** |
| 455–468 | `## Tool Coordination Summary` table | update if H-waves add tool usage |
| 470–483 | `## Will Do` | add hardening "Will Do" bullets |
| 484–497 | `## Will Not Do` | **§4 — add "cannot mark remediated when H-gates missing/failed"** |
| 499–522 | `## Error Handling` table | add H-wave failure rows |
| 524–534 | `## Token Cost Profile` table | add hardening-mode cost row |
| 536–549 | `## Refs` table (538–546) | **§5 — register new refs/*.md here** |

## §7. Frontmatter shape (top of file)

Lines 1–5 are YAML frontmatter:

- L2 `name: sc:troubleshoot-protocol`
- L3 `description: "..."` — single long quoted string (the auto-trigger blurb). To advertise pipeline-hardening (spec §5.1/§5.2), this string is the surface to extend; it is one physical line.
- L4 `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking` — **no new tool needed for H-waves** (Task, Write, Read, Grep, Glob, Bash, mcp__auggie all already present). Adding H-cards requires no allowed-tools change.
- Lines 7–12 are a non-parsed HTML comment block of extended metadata (`category`, `complexity: advanced`, `mcp-servers`, `personas`). Builder may leave as-is.

## §1 + §2. Tier structure, Tier-1 conclusion point, and the hardening insertion seam

**Key terminology note:** SKILL.md uses **Waves** as the literal section headers; **Tiers** are a conceptual grouping that the Wave headers name inline ("Wave 1: Tier 1 — …", "Wave 3: Tier 2 — …", "Wave 6: Tier 3 — …"). There are NO standalone `## Tier 1` headers — Tier identity is carried in the Wave headers.

### Tier → Wave mapping (with line ranges)

| Tier | Waves (header line) | Span | What it does |
|---|---|---|---|
| **Tier 1** | Wave 1 (L135), Wave 1.5 (L158), Wave 1.6 (L196), Wave 1.7 (L251) | **L135–268** | Real-code grounding (W1), doc grounding (W1.5), diagnosability audit (W1.6, may hard-stop), single hypothesis + calibration (W1.7) |
| (gate) | Wave 2 Confidence Gate (L271) | L271–288 | Decides STOP-at-Tier-1 vs escalate. **On STOP → "jump to Wave 5"** (L285). |
| **Tier 2** | Wave 3 (L291), Wave 4 (L356) | **L291–382** | Parallel hypotheses (W3), adversarial fix debate (W4, conditional ≥2 fixes) |
| (report) | Wave 5 Synthesis + Report (L385) | L385–433 | Builds REPORT.md — **this is "final report closure"** |
| **Tier 3** | Wave 6 (L437) | L437–451 | Remediation chain (task-builder), conditional on `--fix` + accept |

### Where Tier-1 diagnosis CONCLUDES (the spec's "after Tier 1 diagnosis") — PINNED

- **Wave 1.7: Tier 1 — Hypothesis Formation** (header **L251**) is the LAST Tier-1 diagnosis wave. Its **Exit criteria are at L263**: "One hypothesis card at `<output-dir>/tier1-hypothesis.md`, a calibration report … Emit 'Wave 1.7 complete: confidence=<x>'." Wave 1.7 body ends at **L267** (token-budget line); the `---` divider is **L269**.
- Immediately after comes **Wave 2: Confidence Gate** (**L271–288**), which is the existing branch point: STOP-at-Tier-1 vs escalate-to-Tier-2.
- **Spec §5.2 wants the hardening trigger "after Tier 1 diagnosis and before final report closure."** Tier-1 diagnosis = through Wave 1.7 (ends L267). Final report closure = Wave 5 (starts L385). So the hardening mode logically belongs **on the path into / out of Wave 5**, NOT before Wave 2 — because Tier 2 (Waves 3–4) is part of "diagnosis" too and a pipeline escape may only be confirmed after escalation. The cleanest single insertion seam that satisfies "after diagnosis, before closure" for BOTH tier outcomes is **a new wave between Wave 4 and Wave 5** (i.e., a new `### Wave 4.5: Pipeline Hardening Closure` header inserted at **L383**, the blank line before the `---` that precedes Wave 5 at L385), OR as a **mandatory pre-step inside Wave 5 step 1** (before report compose at L391).

### Where "final report closure" BEGINS — PINNED

- **Wave 5: Synthesis + Report** header is **L385**. Goal line L387: "Produce one diagnosis report at `<output-dir>/REPORT.md`". Step 1 (load report-template) is **L391**. Step 2 (compose REPORT.md, the section list) runs **L392–408**. This is the report-closure machinery the spec §8 wants to extend with a "Pipeline Hardening Closure" section.

## §3. OUTPUT CONTRACT location + current fields (extend HERE)

- Section header `## Output Contract` at **L37**. Intro line L39: "The skill returns a structured dictionary on completion:".
- **The field table is L41–61** (header row L41 `| Field | Type | Description |`, separator L42, rows L43–61). To add the 8 new fields from spec §6.2 (`pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path`, `off_path_review_decision`, `known_escapes_caught`), **append rows after L61** (last current row is `diagnosability_hard_stop`, L61).
- Current 19 fields (L43–61), in order: `status` (43), `tier_reached` (44), `report_path` (45), `audit_log_path` (46), `confidence` (47), `escalation_reason` (48), `test_is_wrong` (49), `test_file_path` (50), `behavior_is_documented` (51), `doc_context_card_path` (52), `hypothesis_cards` (53), `adversarial_artifacts_dir` (54), `task_file_path` (55), `remediation_offered` (56), `remediation_accepted` (57), `diagnosability_verdict` (58), `diagnosability_context_card_path` (59), `diagnosability_tasklist_path` (60), `diagnosability_hard_stop` (61).
- **Format/house-style precedent for new fields:** existing optional path fields use the type `string \| null` and the phrase "**repo-relative** path" with a parenthetical example and an explicit null condition (see `doc_context_card_path` L52, `test_file_path` L50, `diagnosability_context_card_path` L59). New `*_card_path`/`*_ledger_path`/`*_path` fields should mirror this: `string \| null`, repo-relative, with a stated null condition. `pipeline_hardening_verdict` enum (`pass`/`blocked`/`advisory`/`not_applicable`) mirrors `diagnosability_verdict`'s enum style (L58 lists its enum inline).
- **Derivation-rule precedent:** Output Contract fields with non-trivial logic get a bold "**`field` derivation rule**" prose block immediately after the table — see `test_is_wrong` (L63–71) and `behavior_is_documented` (L73–75). A `pipeline_hardening_applicable`/`pipeline_hardening_verdict` derivation rule block would follow this same pattern, placed after L75 (end of the existing derivation prose) and before `## Wave Structure` (L77).

## §4. Existing failure-state / blocking / halt / STOP wiring (precedent for the "cannot mark remediated" rule)

The builder asked where halt/blocking lives so the hardening gates can add "escape cannot be marked remediated when hardening gates missing/failed." Existing precedents, by mechanism:

**(a) STOP conditions (hard input/flag gates):**
- `## Required Input (STOP if missing)` L26; bold **STOP** at L33 and L35.
- Wave 0 "STOP conditions" line **L131** (missing input, conflicting flags, under-specified deep, unwritable output-dir).

**(b) Hard-stop / halt wiring (the closest analog to a blocking gate):**
- Wave 1.6 **hard-stop**: L220 (`insufficient AND non-trivial AND NOT --no-escalate → hard-stop`), sets `diagnosability_hard_stop=true`, jumps to Wave 5 with `status partial`, skips Waves 1.7–4.
- Wave 5 renders the halt block: L408 ("When `diagnosability_hard_stop=true`, replace the Diagnosis section with a 'Halted — instrumentation required' prose block").
- Per-defect 3-round cap that **refuses** to proceed: L227, L245, L522 ("refuse next tasklist until `--reset-diagnosability-rounds`").

**(c) Gate that BLOCKS report publishing (best template for "cannot mark remediated"):**
- **"Tier 2 calibration completeness gate (hard precondition for report publishing)"** — header **L327**, body **L327–337**. L332: "the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence." This is the strongest existing "MUST NOT publish unless proof exists on disk" pattern and is the **direct house-style template** for an H-gate blocking rule ("MUST NOT mark remediated / MUST NOT publish closure verdict=pass unless H1–H4 cards exist on disk and pass"). It even includes an on-disk verification command (L337).

**(d) Wave 4 self-review blocker → STOP:**
- L377: "If self-review flags a blocker, surface it and STOP — do not proceed to Wave 5 with a known-broken proposal."

**(e) Remediation preconditions (Tier 3 / Wave 6) — where "marked remediated" is gated today:**
- Wave 6 preconditions **L439**: "`--fix` is set AND `REPORT.md` is `success` (not `partial`) AND user explicitly accepts." So remediation already requires `status: success`. The hardening rule (spec §5.2 / §10.6) can hook here: force `status: partial` (or a new `blocked` verdict) when required H-gates are missing/failed/`N/A`-without-rationale, which mechanically prevents Wave 6 remediation via the existing L439 precondition.
- Spec §8 also wants `NOT PROVEN` blockers — there is no existing "NOT PROVEN" token in SKILL.md (new vocabulary), but the `force-degrade` / `failed_to_calibrate` pattern at L335 is the nearest precedent for "downgrade confidence + annotate when proof absent."

**(f) "Will Not Do" negative-rule list (L484–497):** every bullet is a hard prohibition. Add the hardening prohibitions here (e.g., "Mark a pipeline escape remediated when a required H-gate is missing, FAIL, or N/A without rationale"). Current bullets relevant as templates: L495 "Auto-apply the diagnosability tasklist", L496 "Force the Wave 1.6 hard-stop when `--no-escalate`".

## §5. How SKILL.md references its refs/ files (linking convention + examples)

**Convention:** refs are cited inline as backticked **relative paths** `refs/<name>.md`, always paired with the wave that lazy-loads them, plus a central `## Refs` registry table at the end.

Example citation lines (backticked `refs/...`):
- L20 `the rubric in `refs/escalation-rubric.md` decides.`
- L166 (Wave 1.5 step 1) "**Load `refs/doc-discovery.md`** — read the Section 1 …" — shows the house pattern: bold **Load `refs/x.md`** then "read Section N (…)".
- L211 (Wave 1.6 S1.6.1) "**S1.6.1 — Load `refs/diagnosability-audit.md`** (lazy load, mirroring Wave 1.5's discipline). Read Section 1 (…), Section 2 (…) …".
- L391 (Wave 5 step 1) "Load `refs/report-template.md` (not before now — lazy load)."
- L443 (Wave 6 step 1) "read the prompt template in `refs/remediation-handoff.md`."

**Central `## Refs` registry table — L536–549:**
- Header `## Refs` L536; table header L538 `| File | When loaded |`; rows L540–546.
- Current 7 ref rows: `refs/escalation-rubric.md` (540), `refs/triage-checklist.md` (541), `refs/doc-discovery.md` (542), `refs/hypothesis-card-template.md` (543), `refs/report-template.md` (544), `refs/remediation-handoff.md` (545), `refs/diagnosability-audit.md` (546).
- Closing line L548: "Each ref is loaded only by the wave that needs it. Do not pre-load."
- **New refs (spec §9: `pipeline-hardening-closure.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`) must be registered as new rows appended after L546**, with a "When loaded" value naming the H-wave (e.g., "Wave 4.5 H1 / runtime-entrypoint gate").

## §6. Wave/gate naming conventions already used (so H0–H5 match house style)

**Wave header format** (must match for new H-waves):
- `### Wave <N>: <Tier label —> <Title>` e.g. L135 `### Wave 1: Tier 1 — Real-Code Grounding`, L196 `### Wave 1.6: Diagnosability Audit`, L385 `### Wave 5: Synthesis + Report`.
- Fractional wave numbers are ALREADY in use: **Wave 1.5** (L158), **Wave 1.6** (L196), **Wave 1.7** (L251) — so inserting **Wave 4.5** for Pipeline Hardening Closure is consistent with existing precedent, OR sub-numbered steps could be used.
- Each wave section has, in order: **Goal**, **Preconditions**, **Steps** (numbered), **Exit criteria** (with an `Emit "Wave N complete: …"` line), and optionally **Failure handling** (a `| Scenario | Behavior | Fallback |` table — see L184, L238, L346), **Token budget**. H-waves should reproduce this skeleton.

**Step-numbering sub-convention:** Wave 1.6 uses `S1.6.0`, `S1.6.1`, … `S1.6.4` (L209–219) — a `S<wave>.<step>` scheme for fine-grained steps. H-waves with internal steps can mirror this (e.g., `H1.0`, `H1.1`) or use the simpler "1./2./3." numbering most waves use.

**Gate vs Wave vs Rule naming (matches spec H0–H5 exactly):** The spec already names them "Wave H0", "Gate H1", "Wave H2", "Wave H3", "Gate H4", "Rule H5" (spec §7). SKILL.md uses **"Gate"** for decision points (Wave 2 is titled "Confidence Gate" L271; "Tier 2 calibration completeness gate" L327) and **"Wave"** for work phases — so the spec's Wave/Gate/Rule mix is consistent with existing vocabulary. No naming friction.

**Emit-string convention:** every wave ends with an `Emit "Wave N complete: <k=v ...>"` (L129, L152, L180, L234, L263). H-waves should emit e.g. `Emit "Wave H1 complete: verdict=<pass|fail|n/a>"`.

**Verdict/enum house style:** lowercase tokens (`sufficient|partial|insufficient|unknown` L58; `success|partial|failed` L43; `pass|blocked|advisory` already proposed in spec §6.2) — H-wave verdicts must be lowercase to match.

**ASCII Wave Structure map (code fence L79–91)** — any new H-wave must also be added as a line in this map. Verified map lines: `Wave 0` L80, `Wave 1` L81, `Wave 1.5` L82, `Wave 1.6` L83, `Wave 1.7` L84, `Wave 2` L85, `Wave 3` L86, `Wave 4` L87, `Wave 5` L88, hard-stop-edge note L89, `Wave 6` L90, fence-close L91. Insert the H-wave map line (e.g. `Wave 4.5: Pipeline Hardening Closure (conditional)`) **after L87 (Wave 4) and before L88 (Wave 5)**.

---

## Recommended insertion points (for the task builder)

Ordered by edit location, top→bottom of SKILL.md. All line numbers verified against the read of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (549 lines).

1. **Frontmatter `description` (L3)** — extend the trigger blurb to advertise pipeline-hardening (spec §5.1). `allowed-tools` (L4) needs **no change** — Task/Write/Read/Grep/Glob/Bash/auggie all already present.
2. **Wave Structure ASCII map — insert after L87, before L88** — add `Wave 4.5: Pipeline Hardening Closure (conditional)` line.
3. **Output Contract table — append rows after L61** (`diagnosability_hard_stop` is the last current row). Add the 8 spec §6.2 fields, mirroring the `string | null` + repo-relative house style of L50/L52/L59; mirror `diagnosability_verdict`'s inline-enum style (L58) for `pipeline_hardening_verdict`.
4. **Derivation-rule prose — insert after L75, before `## Wave Structure` (L77)** — add a `**`pipeline_hardening_applicable` derivation rule**` block, matching the `test_is_wrong` (L63–71) / `behavior_is_documented` (L73–75) precedent.
5. **New `### Wave 4.5: Pipeline Hardening Closure` section — insert at the `---` seam at L383, before Wave 5 (L385).** This is the load-bearing insertion: it sits "after Tier 1 diagnosis (Wave 1.7 ends L267) and after Tier 2 (Waves 3–4 end L382), and before final report closure (Wave 5 L385)" — satisfying spec §5.2 for BOTH tier outcomes. Use the standard wave skeleton (Goal / Preconditions / Steps with H0–H5 / Exit criteria w/ `Emit "Wave H… complete: …"` / Failure-handling table). Lazy-load `refs/pipeline-hardening-closure.md` per the L166/L211 "**Load `refs/x.md`**" convention. Alternatively (if the builder prefers not to add a wave number), insert as a mandatory pre-step inside Wave 5 **before step 1 at L391** — but a dedicated Wave 4.5 is cleaner and matches the fractional-wave precedent (1.5/1.6/1.7).
6. **Wave 5 report compose — insert into the section list at L408 area** — add a "Pipeline Hardening Closure" REPORT.md section per spec §8 (after the existing render-conditionals at L406–408, before the file:line validation pass at L409).
7. **Blocking gate — model on L327–337** ("Tier 2 calibration completeness gate … MUST NOT publish"). Add an analogous "Pipeline-hardening completeness gate" that BLOCKS `pipeline_hardening_verdict=pass` / blocks marking remediated when H1–H4 cards are missing/FAIL/`N/A`-without-rationale, including an on-disk verification command (L337 precedent).
8. **Wave 6 precondition (L439)** — already requires `status: success`; the hardening gate should force `status: partial`/`blocked` when H-gates fail, mechanically preventing remediation. Optionally tighten L439 to also require `pipeline_hardening_verdict ∈ {pass, not_applicable}`.
9. **`## Will Not Do` — append after L497** — add "Mark a pipeline escape remediated when a required H-gate is missing, FAIL, or N/A without rationale" (template: L495/L496 bullets).
10. **`## Will Do` — append after L482** — add hardening-mode "Will Do" bullets.
11. **`## Error Handling` table — append rows after L522** — add H-wave failure rows (auggie unavailable in H2 sweep, off-path reviewer unavailable, etc.), matching the existing `| Scenario | Behavior | Fallback |` format.
12. **`## Refs` table — append rows after L546** — register the 5 new refs (spec §9): `pipeline-hardening-closure.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`, each with a "When loaded = Wave 4.5 / Hx" value.
13. **`## Token Cost Profile` table (L524–534)** — optionally add a "Pipeline-hardening mode added" cost row, matching the "Wave 1.6 added" row (L532) style.

**Cross-cutting house-style constraints the builder must honor:**
- Lowercase verdict/enum tokens (L43, L58).
- `string | null` + "repo-relative" + explicit null-condition for every new path field (L50/L52/L59).
- Every wave emits `Emit "Wave … complete: …"` (L129/L152/L180/L234/L263).
- refs cited as backticked relative `refs/x.md` + lazy-loaded by their wave + registered in the L536 table.
- The strongest blocking precedent ("MUST NOT publish unless proof on disk + verification command") is the Tier 2 calibration gate at **L327–337** — reuse its shape for the hardening completeness gate.

**Status:** Complete
