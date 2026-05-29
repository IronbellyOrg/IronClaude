# Integration Points — Wave 1.6 Insertion Map

**Researcher**: 3 of 5 (Integration Points)
**Task**: TASK-RF-20260529-160318
**Status**: Complete
**Date**: 2026-05-29

**Scope**: Map every cross-reference, wave-graph hook point, and Output Contract consumer affected by inserting Wave 1.6 between Waves 1.5 and 1.7 in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (468 lines) and `refs/report-template.md` (197 lines).

---

## Part A — SKILL.md Cross-References

### 1. Wave-graph ASCII diagram

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Lines**: 75-85 (the fenced code block; opening fence at L75, closing fence at L85)
**Format**: ```text fenced block.

**Verbatim current contents** (L75-85):

```text
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)
Wave 1.5: Documentation Grounding    ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes Wave 1.5 Documentation Context Card; produces single hypothesis card + calibration
Wave 2: Confidence Gate              ← decides escalation via refs/escalation-rubric.md
Wave 3: Tier 2 — Parallel Hypotheses (conditional)
Wave 4: Tier 2 — Adversarial Fix Debate (conditional, requires ≥2 viable fixes)
Wave 5: Synthesis + Report        ← always finalises; loads refs/report-template.md
Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)
```

**Insertion point**: After L77 (Wave 1.5 line), before L78 (Wave 1.7 line). The new Wave 1.6 line must be inserted between these two lines while preserving the trailing-arrow comment style (`← ...`) used by every other wave line.

**Alignment note**: existing arrows are NOT column-aligned (e.g., Wave 1 uses 2 spaces before `←`, Wave 1.5 uses 4 spaces, Wave 1.7 uses 1 space). The new Wave 1.6 line does not need column alignment — it should follow the loose pattern of the surrounding lines.

---

### 2. Wave 1.5 step 5 exit / handoff to Wave 1.7

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

**Exit-criteria block for Wave 1.5**: L170-174

Verbatim (L170-174):

```text
**Exit criteria**:

- Three branch outputs written to disk at `<output-dir>/wave1_5-branch-<A|B|C>.md`.
- One synthesised Documentation Context Card written to `<output-dir>/doc-context.md` with all four named sections populated (Release context, Architectural docs consulted, Restrictions / decisions that constrain the fix, Re-frame signals).
- Emit "Wave 1.5 complete: doc_context_card_path=<output-dir>/doc-context.md".
```

**Wave 1 → Wave 1.5 handoff phrasing** (the pattern Wave 1.5 must use to hand off to Wave 1.6): L146:

```text
**Exit criteria**: Real-code grounding complete (auggie + serena results captured in audit log, or `Glob`/`Grep` fallback noted); observation captured at `<output-dir>/tier1-observation.md` (or "no repro available" recorded in audit). Emit "Wave 1 complete: grounding done; handing off to Wave 1.5".
```

**Required handoff change**: The Wave 1.5 exit emit message on L174 currently does not name the next wave. After Wave 1.6 inserts, **two options** exist:

1. Leave L174 unchanged (it just names the artifact, not the next wave). Wave 1.6 then opens with "Preconditions: Wave 1.5 complete; ..." mirroring how Wave 1.7 currently opens.
2. Append a "handing off to Wave 1.6" clause to L174, mirroring Wave 1 L146's phrasing.

Either is consistent with the existing pattern. Builder should pick option 1 (less invasive) unless spec §10 dictates otherwise.

---

### 3. Wave 1.7 preconditions (current text → new clause)

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Line**: 194

**Verbatim current preconditions** (L194):

```text
**Preconditions**: Wave 1 (real-code grounding) is complete; Wave 1.5 has produced a Documentation Context Card at `<output-dir>/doc-context.md` (or `--no-doc-discovery` was set and `doc_context_card_path` is `null`).
```

**Required change**: append the Wave 1.6 hard-stop precondition. The new clause per spec §10 is:

> "Wave 1.6 did NOT fire its hard-stop (or was skipped via `--no-diagnosability-audit`, or fired soft-warn under `--no-escalate`)"

This becomes a third semicolon-separated clause within the same L194 sentence, preserving the existing parenthetical-alternation style ("...(or `--no-doc-discovery` was set...)").

---

### 4. Wave 5 step 2 REPORT.md composition list

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Lines**: 331-342 (Wave 5 step 2 — "Compose `REPORT.md` filling in:")

**Verbatim current list** (L331-340):

```text
2. Compose `REPORT.md` filling in:
   - Header (target, tier reached, confidence, escalation reason)
   - Summary (2-4 sentence executive summary)
   - Documentation Context (≤6-line summary of the Wave 1.5 Documentation Context Card at `<output-dir>/doc-context.md`; omit this section entirely and add a line to Grounding Gaps when `--no-doc-discovery` was set)
   - Diagnosis (the chosen hypothesis — from Tier 1 alone, or from the adversarial merge)
   - Evidence (cited `file:line` and command outputs)
   - Proposed Fix (the recommended change; if a doc-update + fix bundle was produced in Wave 4, render BOTH the doc file(s) to update and the code change(s) in this section)
   - Alternative Fixes Considered (Tier 2 only — the losing proposals from the debate, with one-line reason each)
   - Risk + Rollback (what to watch after applying)
   - Next Steps (Tier 1: rerun with `--depth deep` if needed; Tier 2 without `--fix`: re-invoke with `--fix` to authorize remediation; Tier 2 with `--fix`: confirm to proceed to Wave 6)
```

**Insertion point for new `Diagnosability Context` bullet**: between L334 (Documentation Context bullet) and L335 (Diagnosis bullet). The bullet pattern is `   - <SectionName> (<one-line description; conditional behavior in parens>)` — the new bullet must follow this exact pattern with 3-space indent + ` - `.

**Continuation paragraph after the list** (L342):

```text
   When `--no-doc-discovery` was set, omit the Documentation Context section entirely AND populate the Grounding Gaps section with: "Documentation grounding skipped by `--no-doc-discovery` — diagnosis is not weighted against documented behavior or restrictions."
```

A parallel paragraph for `--no-diagnosability-audit` (or for the Wave 1.6 hard-stop case) likely belongs here after the new Diagnosability Context bullet's continuation — exact wording will come from spec §10.

---

### 5. Output Contract consumers — Tier 3 / fleet auto-apply / telemetry / status

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

#### 5a. `Tier 3 task-builder` mentions

- **L67** (output contract prose): "downstream automation (Tier 3 task-builder, fleet auto-apply wrappers, telemetry) can short-circuit on the asymmetric-cost case without parsing prose."
- **L379** (Wave 6 Phase A): "invoke the `task-builder` skill via `Skill` with a `BUILD_REQUEST` whose GOAL is..."
- **L398** (Tool Coordination table, Tier 3 row): "`Skill` | — | ✓ (`sc:adversarial-protocol`) | ✓ (`task-builder`, `/sc:reflect`)"
- **L440** (Error Handling): "`task-builder` unavailable in Wave 6 | Surface the fix proposal path; recommend manual task creation; don't fail the whole skill"

Verbatim L67:

```text
The prose REPORT.md is still the human-readable source of truth; this flag exists so downstream automation (Tier 3 task-builder, fleet auto-apply wrappers, telemetry) can short-circuit on the asymmetric-cost case without parsing prose.
```

This sentence establishes the downstream-consumer model: contract is additive, prose is canonical, machine flags exist for short-circuit decisions. **No change required** for the 4 new Wave 1.6 fields — they extend the contract additively, matching this pattern.

#### 5b. `fleet auto-apply` mentions

Only L67 (cited above). Single reference; not parsed by code in-repo. Additive contract fields are safe.

#### 5c. `telemetry` mentions

Only L67 (cited above). Additive fields are safe.

#### 5d. `status: success | partial | failed` references

- **L43** (Output Contract table, status row): "`status` | string | `success`, `partial` (some findings dropped for grounding), `failed`"
- **L343** (Wave 5 evidence-validator): "if any were dropped, set the report's frontmatter `status: partial` and add a 'Grounding Gaps' entry referencing them."
- **L344** (Wave 5 evidence-validator fallback): "mark `status: partial` and add a Grounding Gap entry noting the validator was unavailable."
- **L349** (audit footer block): "status: <success|partial>"
- **L373** (Wave 6 preconditions): "`REPORT.md` is `success` (not `partial`)"
- **L443** (Error Handling, evidence-validator fails): "mark `status: partial` and add a Grounding Gap entry"
- **report-template.md L14**: "**Status**: <success|partial>"

Verbatim L43:

```text
| `status` | string | `success`, `partial` (some findings dropped for grounding), `failed` |
```

**Key finding**: The status enum (`success | partial | failed`) is unchanged. Wave 1.6's hard-stop case must map to one of these existing values (likely `partial` or `failed` depending on spec §10's semantics). The 4 new contract fields are **additive** and do not require any status enum change. Downstream consumers parsing the contract will see new fields they don't recognize and ignore them per JSON-compatible additive evolution.

**Verification finding (additive contract safety)**: nothing else in SKILL.md or report-template.md programmatically parses the contract — every consumer is described in prose. The 4 new fields therefore require no schema/parser updates anywhere in-repo.

---

### 6. Tool Coordination Summary table

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Lines**: 389-402

**Verbatim** (L389-402):

```text
## Tool Coordination Summary

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| `mcp__auggie__codebase-retrieval` | ✓ (one focused query + Wave 1.5 doc-grounding fan-out: 3 parallel branch queries) | ✓ (per-hypothesis queries) | — |
| `mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview` | ✓ | ✓ | — |
| `mcp__context7__query-docs` | — | ✓ when framework/library named | — |
| `mcp__tavily__tavily-search` | — | ✓ rate-limited (≤2 queries) | — |
| `mcp__sequential-thinking__sequentialthinking` | — | ✓ for synthesis | — |
| `Task` (agent spawn) | ✓ (root-cause-analyst + confidence-calibrator) | ✓ (2-4 hypothesis agents in parallel + per-card confidence-calibrator + evidence-validator at Wave 5) | ✓ (self-review for post-exec) |
| `Skill` | — | ✓ (`sc:adversarial-protocol`) | ✓ (`task-builder`, `/sc:reflect`) |
| `Read` / `Grep` / `Glob` | ✓ | ✓ | — |
| `Bash` | ✓ (repro when cheap) | ✓ (diagnostic commands) | — |
| `Write` | ✓ (hypothesis + report) | ✓ (hypothesis cards, fix proposals) | — |
```

**Pattern**: 4 columns (Tool, Tier 1, Tier 2, Tier 3). Rows are per-tool, with ✓ + parenthetical scope-note for each tier that uses it, `—` for tiers that don't.

**Wave 1.6 row insertion**: The table is organized **by tool, not by wave**. Wave 1.6's tools (likely auggie + serena + Task for the diagnosability-audit subagent + possibly Bash for file checks) need to be **annotated into existing rows**, not added as a new row.

Specifically:
- `mcp__auggie__codebase-retrieval` Tier 1 cell already mentions "Wave 1.5 doc-grounding fan-out" — Wave 1.6's auggie use (if any) gets appended in the same cell.
- `Task` Tier 1 cell currently lists "(root-cause-analyst + confidence-calibrator)" — if Wave 1.6 spawns a `diagnosability-auditor` subagent, that name appends here.
- Other tool rows: only annotate if Wave 1.6 actually uses them (per spec §10).

**Critical**: do NOT add a new "Wave 1.6" column or row — the table's axis is tool × tier, not wave.

---

### 7. Token Cost Profile table

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Lines**: 446-455

**Verbatim** (L446-455):

```text
## Token Cost Profile

| Tier reached | Auggie tokens (offloaded) | Claude tokens (orchestration + agents) | Wall clock |
|--------------|---------------------------|----------------------------------------|------------|
| Tier 1 only | ~2-5k | ~3-6k | 1-3 min |
| Tier 2 (no adversarial) | ~5-15k | ~15-30k | 4-7 min |
| Tier 2 (with adversarial) | ~10-25k | ~30-60k | 8-15 min |
| Tier 3 added | +0 (auggie not used) | +20-40k (task-builder) | +5-10 min |

These are targets, not hard caps. Auggie tokens are offloaded to a free / low-cost retrieval tier; Claude tokens are the constrained resource. The escalation gate exists specifically to keep the Tier-1-only path inside the 3-9k Claude-token band for the common case.
```

**Pattern**: 4 columns (Tier reached, Auggie tokens, Claude tokens, Wall clock). Rows are per-tier (or "+X" delta rows for additions like Tier 3).

**Wave 1.6 row insertion**: Wave 1.6 is part of Tier 1 (it runs before the confidence gate). Per spec §10, the new row likely takes the `+X delta` form (e.g., `| Wave 1.6 added | +<auggie> | +<claude> | +<seconds> min |`) and inserts **between the existing Tier 1 row and the Tier 2 row** — i.e., between L450 and L451.

The exact deltas come from spec §10; this researcher's job is the integration point, not the cost numbers.

**Trailing paragraph** (L455) is unchanged by the addition — Wave 1.6's cost stays inside the Tier-1 cost band claim already made there.

---

### 8. Error Handling table

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Lines**: 427-444

**Verbatim** (L427-444):

```text
## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality is degraded; native tools only | None |
| auggie unavailable (others OK) | Fall back to `Grep` + `Glob` for grounding; mark in audit | None |
| auggie unavailable in Wave 1.5 (others OK) | Fall back to `Grep`/`Glob` against the per-branch query targets (`.dev/releases/`, `docs/`, `<scope>`); mark `degraded: true` per branch; do NOT block the Tier 1 hypothesis | None |
| All three Wave 1.5 branches return empty / no-hit | Write Documentation Context Card with "None found" in every section; set `doc_context_card_path` to the (still-emitted) empty card; mark `behavior_is_documented` derivation as `no_docs_found` candidate | None |
| `--no-doc-discovery` set by user | Skip Wave 1.5 entirely; emit `doc_context_card_path: null`; record skip-line in Wave 5 Grounding Gaps | None |
| root-cause-analyst agent fails in Tier 1 | Skill produces a degraded Tier 1 (Claude inline) and recommends `--depth deep` | None |
| All Tier 2 agents fail | Downgrade to Tier 1 result; report `partial`; recommend rerun | None |
| `sc:adversarial-protocol` fails in Wave 4 | Pick the highest-confidence Tier 2 fix proposal as the chosen fix; note in audit and report header | None |
| `self-review` flags blocker on adversarial merge | STOP at Wave 5 with `partial` status; report includes the blocker; recommend rerun with `--depth deep` or different focus | None |
| `task-builder` unavailable in Wave 6 | Surface the fix proposal path; recommend manual task creation; don't fail the whole skill | None |
| User declines remediation offer | Return success; report stands | None |
| `--depth deep` requested on under-specified input | STOP at Wave 0; ask user to add detail | None |
| `evidence-validator` agent fails (subprocess crash, timeout, or malformed report) | Inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); mark `status: partial` and add a Grounding Gap entry noting the validator was unavailable | None — the inline path is the fallback |
| `confidence-calibrator` agent fails for any card | Fall back to inline orchestrator calibration for that card; mark the card with `calibration: inline-fallback` in the audit log; do NOT block escalation on a missing calibration | None |
```

**Pattern**: 3 columns (Scenario, Behavior, Fallback). Rows are ordered loosely by wave-progression (Wave 0 → Wave 1 → Wave 1.5 → Wave 3 → Wave 4 → Wave 5 → Wave 6) with cross-cutting "All MCPs unavailable" at the top.

**Insertion zone for Wave 1.6 rows**: The 6 new rows per spec §10 should insert as a contiguous block **between the last Wave 1.5 row (L435: `--no-doc-discovery set by user`) and the first Wave 1.7-ish row (L436: `root-cause-analyst agent fails in Tier 1`)**.

That is, insert after L435 and before L436. This preserves the wave-progression order.

---

### 9. Refs table

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Lines**: 457-468

**Verbatim** (L457-468):

```text
## Refs

| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1.7 (calibration) |
| `refs/triage-checklist.md` | Wave 1 (real-code grounding load) AND Wave 1.7 (passed to root-cause-analyst as part of the brief) |
| `refs/doc-discovery.md` | Wave 1.5 (documentation grounding — Auggie query templates, currency-check procedure, output schemas, Documentation Context Card template) |
| `refs/hypothesis-card-template.md` | Wave 1.7 and Wave 3 (passed to agents) |
| `refs/report-template.md` | Wave 5 |
| `refs/remediation-handoff.md` | Wave 6 |

Each ref is loaded only by the wave that needs it. Do not pre-load.
```

**Pattern**: 2 columns (File, When loaded). Rows ordered by wave that loads the ref.

**Wave 1.6 new row insertion point**: between L463 (`refs/doc-discovery.md` — Wave 1.5) and L464 (`refs/hypothesis-card-template.md` — Wave 1.7 and Wave 3). The new row is:

```text
| `refs/diagnosability-audit.md` | Wave 1.6 (<one-line scope from spec §10>) |
```

The exact "When loaded" description comes from spec §10's diagnosability-audit ref content. Pattern follows the existing rows verbatim.

---

### 10. Will Do / Will Not Do lists

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

**Will Do** at L404-413 (verbatim):

```text
## Will Do

- Always run Tier 1 first; respect the "quick first option" contract
- Auto-escalate only when the rubric in `refs/escalation-rubric.md` says so, or when `--depth deep` is set
- Fan out 2-4 specialist agents in parallel in Tier 2, chosen by signal mix
- Use auggie/serena every tier for in-repo grounding; use context7/tavily only in Tier 2 and only when the symptom suggests external knowledge
- Run `/sc:adversarial` only when Tier 2 produces 2-3 competing strong fixes (not when there is consensus — that wastes the debate)
- Run `self-review` after the adversarial merge to catch obvious regressions before reporting
- Validate every `file:line` citation in the report against the real file
- Stop at the natural off-ramp for each tier; never silently proceed to a deeper tier than the user authorized
```

**Will Not Do** at L415-425 (verbatim):

```text
## Will Not Do

- Apply code changes without `--fix` and explicit user confirmation
- Skip Tier 1 and jump straight to Tier 2 (even with `--depth deep`, Tier 1 still runs first — it's cheap and its output feeds Tier 2)
- Spawn Tier 2 hypothesis agents on consensus single-domain Tier 1 results
- Spawn more than 4 hypothesis agents in Tier 2 (token waste; signal already saturated)
- Call tavily without a focused query (the rate cap exists for a reason)
- Trust agent-reported confidence without independent re-grading (the `confidence-calibrator` agent or the inline fallback applies the rubric in a fresh context)
- Ship a `REPORT.md` whose `file:line` citations have not passed through `evidence-validator` (or the inline fallback)
- Auto-execute the Tier 3 task file — that is always a separate user-initiated `/task` invocation
- Auto-commit after Tier 3 — `/sc:reflect — type task --validate` is the final gate the user runs before committing
```

**Pattern**: bullet list, single `- ` prefix per item, one-line statement (occasionally with a parenthetical clarifier). No sub-bullets, no numbering.

**Insertion points for new bullets per spec §10**: append to the end of each list (after L413 for Will Do, after L425 for Will Not Do), matching the existing bullet style. Spec §10 specifies the literal bullet text.

---

## Part B — REPORT.md template (refs/report-template.md) Integration

### B1. `## Documentation Context` end → `## Diagnosis` begin

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`

- `## Documentation Context` header at **L31**.
- Section ends at **L41** (last bullet/line of the section: "If `--no-doc-discovery` was set, omit this section entirely and add a line to **Grounding Gaps**: "Documentation grounding skipped by `--no-doc-discovery`."").
- `## Diagnosis` header at **L43**.

**Insertion point for new `## Diagnosability Context` section**: between L41 and L43. Insert as a new section block (header + body) using the same pattern as the surrounding sections:

Verbatim current `## Documentation Context` section header + body (L31-41) for pattern reference:

```text
## Documentation Context

Wave 1.5 documentation grounding result. ≤6-line summary of the Documentation Context Card.

- **Relevant refs**: <comma-separated doc paths from Branch A + Branch B + Branch C, or "None found">
- **Documented behavior**: <one-line summary of what the docs say about the affected surface>
- **Restrictions honored**: <one-line list of doc-cited constraints the chosen fix respects>
- **Restrictions overridden**: <one-line list of doc-cited constraints the chosen fix violates; cite the doc-update + fix bundle if applicable, otherwise "None">
- **Card path**: <output-dir>/doc-context.md

If `--no-doc-discovery` was set, omit this section entirely and add a line to **Grounding Gaps**: "Documentation grounding skipped by `--no-doc-discovery`."
```

The new `## Diagnosability Context` section should mirror this pattern: brief intro sentence, bulleted key-value fields with `<placeholders>`, then a conditional-omission rule referencing `--no-diagnosability-audit`.

---

### B2. `## Next Steps` section (hard-stop variant)

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
**Lines**: 124-132

**Verbatim**:

```text
## Next Steps

Pick the line(s) that apply:

- Tier 1, high confidence: "Apply the fix manually, or re-run with `/sc:troubleshoot --fix <args>` to generate an MDTM task."
- Tier 1, low confidence (but `--no-escalate`): "Re-run without `--no-escalate` (or with `--depth deep`) to enable Tier 2 fan-out."
- Tier 2 without `--fix`: "Re-run with `--fix` added to your previous invocation to enter the remediation chain."
- Tier 2 with `--fix`, awaiting user accept: "Reply **yes** to proceed to the task-builder remediation chain, or apply the fix manually."
- Tier 3 chain completed (post-`/task`): "Run `/sc:reflect --type task --validate <task-file>` before committing."
```

**Pattern**: bulleted list, each bullet is `- <state-description>: "<quoted user-facing recommendation>"`.

**Insertion point for the hard-stop variant**: append a new bullet at the end of this list (after L132, before the `## Audit` header at L134). The new bullet follows the same `- <state>: "<recommendation>"` pattern. Exact wording from spec §10.

---

### B3. Top-of-report content (`--depth deep` banner location)

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`

**Current top-of-report layout** (L8-25):

```text
# Troubleshoot Report

**Target**: <one-line: the symptom or scope as given>
**Type**: <bug|performance|security|build|deployment|test|auto>
**Tier reached**: <1|2|3>
**Confidence**: <0.0–1.0>
**Status**: <success|partial>
**Escalation reason**: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent|not_reproducible|security_caution>
**Test is wrong**: <true|false> <!-- ... -->
**Test file to update**: <...>
**Behavior is documented**: <true|false|n/a> <!-- ... -->
**Doc context card**: <...>
**Duration**: <seconds>
**Date**: <ISO 8601>

---

## Summary
```

- Title at **L8** (`# Troubleshoot Report`).
- Header fields block at **L10-21** (bold-key + value pairs, one per line).
- Horizontal rule `---` at **L23**.
- `## Summary` header at **L25**.

**`--depth deep` banner insertion point**: per the researcher prompt, "above the Summary." Two possible interpretations:

1. **Above the title** (L8) — globally above all report content. Unusual but unambiguous.
2. **Between the `---` (L23) and `## Summary` (L25)** — visually "above the Summary" while remaining inside the report body. More consistent with how a banner-style alert is rendered.

The builder should default to interpretation 2 unless spec §10 explicitly says otherwise — that location makes the banner act as a section-level alert between the metadata block and the prose summary.

---

### B4. Header field section (location of `Diagnosability audit: SKIPPED ...` line)

**File**: `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
**Lines**: 10-21 (the **bolded-key + value** header field block)

This IS the header field section. The new `**Diagnosability audit**: SKIPPED / RAN / HARD_STOP / SOFT_WARN ...` line follows the same `**Key**: <value-or-placeholder> <!-- optional inline comment -->` pattern.

**Insertion point**: The header field block has no enforced ordering convention beyond loosely-grouped metadata (Target/Type → tier/confidence/status → flags → paths → duration/date). A reasonable position for the new field is **between the Doc context card line (L19) and the Duration line (L20)**, grouping it with the other Wave 1.5/1.6 grounding-context fields.

Verbatim L18-20 for pattern reference:

```text
**Behavior is documented**: <true|false|n/a> <!-- See "Behavior-is-documented rule" below. ... -->
**Doc context card**: <repo-relative path to <output-dir>/doc-context.md when Wave 1.5 ran (path is present even if the card's sections all read "None found"); `null` ONLY when `--no-doc-discovery` was set>
**Duration**: <seconds>
```

The new line should follow the same bold-key + placeholder + optional `<!-- ... -->` rule-reference style.

---

## Part C — Summary of Edit Locations (for the Builder)

The following table summarizes every file:line touch point for the builder's Edit instructions:

| # | File | Line(s) | Action |
|---|------|---------|--------|
| 1 | SKILL.md | 75-85 (insert after L77) | Add new Wave 1.6 line to wave-graph ASCII |
| 2 | SKILL.md | 174 (optionally) | Append "handing off to Wave 1.6" to Wave 1.5 exit emit |
| 3 | SKILL.md | 188 (insert new section after) | Insert new `### Wave 1.6: ...` section between Waves 1.5 and 1.7 |
| 4 | SKILL.md | 194 | Append Wave 1.6 hard-stop clause to Wave 1.7 preconditions |
| 5 | SKILL.md | 334 (insert after) | Insert `Diagnosability Context` bullet in Wave 5 step 2 list |
| 6 | SKILL.md | 342 (extend / add parallel paragraph) | Add `--no-diagnosability-audit` omission rule |
| 7 | SKILL.md | 393 / 398 (annotate cells) | Annotate Tool Coordination Summary cells (NOT new row) |
| 8 | SKILL.md | 450 (insert after) | Insert Wave 1.6 row in Token Cost Profile table |
| 9 | SKILL.md | 435 (insert after, 6 new rows before L436) | Insert 6 Wave 1.6 error-handling rows |
| 10 | SKILL.md | 463 (insert after) | Insert `refs/diagnosability-audit.md` row in Refs table |
| 11 | SKILL.md | 413 (append after) | Append Wave 1.6 Will Do bullet(s) |
| 12 | SKILL.md | 425 (append after) | Append Wave 1.6 Will Not Do bullet(s) |
| 13 | report-template.md | 41 (insert after) | Insert new `## Diagnosability Context` section |
| 14 | report-template.md | 132 (append bullet) | Add hard-stop Next Steps bullet |
| 15 | report-template.md | 23-25 (insert between) | Insert `--depth deep` banner above Summary |
| 16 | report-template.md | 19 (insert after) | Insert `**Diagnosability audit**: ...` header field |

---

## Part D — Cross-Reference / Consumer Impact Findings

1. **The Output Contract is additive-safe.** The 4 new Wave 1.6 fields slot in next to the existing `doc_context_card_path` style additive fields (L52). No status enum expansion required; no downstream consumer (Tier 3 task-builder, fleet auto-apply, telemetry) parses the contract via code in-repo — every reference is prose. Additive evolution is the documented pattern (per L67).

2. **`status: success | partial | failed` enum is unchanged.** Wave 1.6's hard-stop case must map to one of these existing values per spec §10. Researcher 1 (file inventory) and Researcher 2 (patterns) will have confirmed which value the spec assigns.

3. **Wave-progression order is the organizing principle of all four downstream tables.** Error Handling, Refs, Token Cost Profile, and (implicitly) Wave 5 composition list all preserve Wave 0 → 1 → 1.5 → 1.7 → 2 → ... order. Insertion points for Wave 1.6 are between the Wave 1.5 row(s) and the Wave 1.7 row(s) in each.

4. **Tool Coordination Summary is the lone exception** — organized by tool × tier, not by wave. Wave 1.6 tool usage gets annotated into existing cells, NOT a new row.

5. **`--no-diagnosability-audit` flag** must be added to the Wave 0 flag-parsing list at L97 (current verbatim: "Parse flags. Required: issue description OR `--scope`. Optional: `--type`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`."). This is implied by Wave 1.7's new precondition referencing `--no-diagnosability-audit` but is NOT explicitly in the researcher prompt — flagging for the builder.

6. **Wave 1.6's relationship to `--no-escalate`** (per researcher prompt: "fired soft-warn under `--no-escalate`") means Wave 1.6's hard-stop semantics interact with the existing `--no-escalate` flag in Wave 2 (currently L216: "`--depth quick` OR `--no-escalate` → STOP at Tier 1 regardless of confidence"). The interaction needs to be reflected somewhere in the new Wave 1.6 section's body.

7. **The single REPORT.md doc-context omission pattern at L342** (Wave 5 step 2 trailing paragraph) is the template for how Wave 1.6's `--no-diagnosability-audit` and hard-stop cases get surfaced into REPORT.md — a parallel paragraph or extended one is the natural shape.

8. **Two minor `<!-- ... -->` HTML comments at L7-12 of SKILL.md** are extended metadata not parsed by the loader — Wave 1.6 does not require any changes there.

---

## Status: Complete

All 10 SKILL.md hook points and 4 report-template.md hook points have been mapped with file:line citations and verbatim current text. The builder has every coordinate needed to write precise Edit instructions.
