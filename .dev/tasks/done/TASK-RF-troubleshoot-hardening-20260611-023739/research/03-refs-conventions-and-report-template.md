# Research: Refs Conventions + Report Template

> ⚠️ **SUPERSEDED (design conclusions only):** This file was researched against the older DRAFT spec. Its CODEBASE anchors (SKILL.md headings/lines, refs house-style, sync model, MDTM mechanics) are VALID and re-verified. But its DESIGN CONCLUSIONS (ref count, output-contract field count, testing scope, draft §6.2/§7/§9 section numbers) are STALE — see `08-v1.1.0-deliverable-reconciliation.md` + `07-release-spec-structure.md` (AUTHORITATIVE for v1.1.0: 6 refs, 10+1 fields incl. waiver_status/contract_version/backtest_status, 17+6 tests, advisory REQUIRED).


**Topic type:** Patterns & Conventions
**Scope:** refs/ + report-template + remediation-handoff
**Status:** Complete
**Date:** 2026-06-10

---

## 1. Ref-file house style (the convention the 5 new refs MUST match)

Exemplars read in full: `hypothesis-card-template.md` (8.5KB), `escalation-rubric.md` (7.7KB), `triage-checklist.md` (3.6KB), plus the two edit targets `report-template.md` (16.9KB) and `remediation-handoff.md` (5.4KB). All paths under `src/superclaude/skills/sc-troubleshoot-protocol/refs/`.

### 1.1 Frontmatter — NONE. This is the single most important convention.

**No ref file in this directory has YAML frontmatter.** Every ref opens with a top-level `# Title` ATX heading on line 1:

- `hypothesis-card-template.md:1` → `# Hypothesis Card Template`
- `escalation-rubric.md:1` → `# Escalation Rubric`
- `triage-checklist.md:1` → `# Triage Checklist (Wave 1)`
- `report-template.md:1` → `# REPORT.md Template`
- `remediation-handoff.md:1` → `# Tier 3 Remediation Handoff (Wave 6)`

**MD025 implication (critical):** MD025 (single-H1 / `front_matter_title`) only trips when a file has BOTH frontmatter `title:` AND a body `# H1` (per memory `reference_markdownlint_md025_frontmatter_title.md`). Because these refs have NO frontmatter and exactly ONE `# ` line, they are MD025-clean. **The 5 new refs MUST follow the same shape: no frontmatter, exactly one `# Title` on line 1, all other headings `##`/`###`.** Do NOT add YAML frontmatter to any new ref — it would diverge from every sibling AND risk MD025 if a `title:` is included.

### 1.2 Heading hierarchy

- Line 1: `# <Title>` (one only).
- Section headers: `## <Section>`. Sub-sections: `### <Subsection>`.
- The (Wave N) parenthetical in the title is common but optional: `triage-checklist.md:1`, `remediation-handoff.md:1` use it; `hypothesis-card-template.md:1`, `escalation-rubric.md:1` do not. For new refs, prefer a short descriptive title; if wave-tagging, use the new H-namespace (e.g. "Pipeline Hardening Closure (Waves H0-H5)").

### 1.3 How a ref opens (title → purpose → consumer)

Every ref opens with the `# Title`, then 1-3 lines of prose stating WHO loads it and WHEN, before any template. Examples:

- `hypothesis-card-template.md:3` — "Used by every agent that produces a hypothesis — `root-cause-analyst` in Wave 1.7, and every Tier 2 agent in Wave 3."
- `escalation-rubric.md:3` — "Used in Wave 1.7 (to calibrate the Tier 1 hypothesis confidence) and in Wave 2 ..."
- `triage-checklist.md:3` — "Passed to the `root-cause-analyst` agent as part of the Tier 1 brief."
- `report-template.md:3` — "The final deliverable of every `/sc:troubleshoot` invocation, regardless of tier. Loaded only in Wave 5."
- `remediation-handoff.md:1-2` — "Loaded only when `--fix` is set and Wave 5 produced a `success` ... report."

**New refs must open identically:** `# Title` + a "Loaded in Wave H<n> when <trigger>" purpose line tying back to spec §7.

### 1.4 Fenced card blocks — language tags matter

The house style uses fenced blocks with EXPLICIT language tags, never bare ``` ```:

- **`text`** for literal cards/prompts the agent fills in (no markdown rendering wanted):
  - `report-template.md:160` hard-stop block uses a ```` ```text ```` fence.
  - `remediation-handoff.md:9,42,82,100` (user offer, BUILD_REQUEST, exec gate, validate cmd) use a **bare ```** in the current file. This is a pre-existing minor inconsistency, NOT the pattern to copy.
  - **Spec §7 H1 card (spec lines 136-151) and §7 H4 card (spec lines 241-253) are written as ```` ```text ```` in the spec.** The new refs MUST tag these card fences ```` ```text ````.
- **`markdown`** for templates that ARE markdown the agent renders into the report:
  - `hypothesis-card-template.md:9` and `:127` use ```` ```markdown ```` fences.
  - **Spec §8 report section (spec lines 299-312) is written as ```` ```markdown ````.** The report-template.md insertion MUST tag it ```` ```markdown ````.
- **Nested fences:** `report-template.md` wraps its whole template in a **four-backtick** ```` ````markdown ```` fence (opens line 7, closes line 203) precisely because the template body contains a three-backtick ```` ```text ```` block (line 160). Any new ref that nests a fenced block inside another fenced block needs the same four-backtick outer wrapper. Single-card refs (H1, H4) won't nest. For `pipeline-hardening-closure.md`, present the §8 markdown block as a normal section-level ```` ```markdown ```` fence — do NOT double-wrap.

**markdownlint MD040 (fenced-code-language):** every fence needs a language. Use `text` for fill-in cards, `markdown` for report fragments.

### 1.5 Table style — GitHub pipe tables, raw (not fenced)

All tables are raw GFM pipe tables with a `|---|` separator row, rendered (not inside a code fence):

- `escalation-rubric.md:11-18` (6-dim rubric), `:41-48` (cross-tab); `triage-checklist.md:20-34` (cause-class); `remediation-handoff.md:32-36` (decision matrix). Report header fields are prose-bold, not a table.
- Separator style is bare `|---|---|` (no alignment colons) — e.g. `escalation-rubric.md:12`, `triage-checklist.md:21`.
- **Spec §7 H2 ledger (spec lines 171-180) is a 2-col `| Field | Required content |` pipe table** — render it as a raw pipe table in `contract-enumeration.md`, matching this style. Same for the §6.2 output-contract field table (spec lines 102-111).

### 1.6 Typical length & closing conventions

- Length: refs run ~60-260 lines. `triage-checklist.md` (66) is the floor; `report-template.md` (259) the ceiling. New single-card refs (H1, H4) should land ~40-90 lines; `pipeline-hardening-closure.md` (the index/mode ref) will be longest, ~120-200.
- Refs frequently close with a **"Rendering rules" / "Filling the card" / "Why this is..." rationale** section:
  - `hypothesis-card-template.md:118` "## Filling the card" + `:125` "## Worked example".
  - `report-template.md:205` "## Rendering rules" + `:212` "## Test-is-wrong rule".
  - `escalation-rubric.md:74` "## Why 0.85?".
  - `remediation-handoff.md:108` "## Why this is the only safe handoff" + `:116` "## Failure modes".
  - New refs SHOULD close with a `## Blocking rule` section restating the spec's per-gate blocking criteria (spec §7 lines 153-156, 184-187, 220-223, 255-258) and the `NOT PROVEN` requirement (spec §8 line 314).
- **Worked examples** are illustrative-only and labeled: `hypothesis-card-template.md:125` "## Worked example (illustrative — not a real card)". Mirror this label.
- Tone: `report-template.md:207` "No trailing emoji or decorative headers." and `:208` "Cite or drop." apply repo-wide. No emoji in new refs.

### 1.7 SKILL.md cross-link convention (so the builder wires the 5 new refs)

`SKILL.md` references refs in two places (verified via grep of `src/.../SKILL.md`):
1. **Inline lazy-load prose** in the relevant wave step, e.g. `SKILL.md:391` "Load `refs/report-template.md` (not before now — lazy load)." and `SKILL.md:443` "read the prompt template in `refs/remediation-handoff.md`."
2. **A ref→wave lookup table** at `SKILL.md:540-546`, one row per ref: `` | `refs/<name>.md` | <wave(s)> | ``. Example rows: `:544` `` | `refs/report-template.md` | Wave 5 | ``; `:545` `` | `refs/remediation-handoff.md` | Wave 6 | ``.

**Builder action (note for R1's SKILL.md track — flagged, not owned here):** each of the 5 new refs needs a row appended to that table (e.g. `` | `refs/pipeline-hardening-closure.md` | Wave H0-H5 (pipeline-hardening mode) | ``) AND a lazy-load mention in the new pipeline-hardening wave step. This is R1's structural-map territory; recorded here only so the convention is documented.

## 2. report-template.md — full section map + EXACT insertion point

File: `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`, 259 lines. Structure: a `# REPORT.md Template` title (line 1), a `## Template` (line 5) whose body is wrapped in a **four-backtick** ```` ````markdown ```` fence (opens line 7, closes line 203), then post-template rule sections.

### 2.1 Section map of the embedded template (inside the four-backtick fence)

| Template section | Line range | Notes |
|---|---|---|
| Header field block (`# Troubleshoot Report` + `**Target**`…`**Date**`) | 8-22 | bold key/value lines |
| `---` rule | 24 | |
| Diagnosability Caveat banner (conditional) | 26-30 | blockquote |
| `## Summary` | 32-37 | |
| `## Documentation Context` | 39-48 | |
| `## Diagnosability Context` | 50-63 | |
| `## Diagnosis` | 65-73 | |
| `## Evidence` | 75-83 | |
| `## Proposed Fix` | 85-99 | incl. "Files that MUST NOT change", "Apply with" |
| `## Alternative Fixes Considered` | 101-110 | |
| `## Risk + Rollback` | 112-120 | |
| `## Follow-up tasks` | 122-132 | |
| `## Grounding Gaps` | 134-144 | |
| `## Next Steps` | 146-154 | + `### Hard-stop variant` 156-194 |
| `## Audit` | 196-202 | last section inside the fence |
| Four-backtick fence CLOSE | 203 | |
| `## Rendering rules` (post-template) | 205-210 | |
| `## Test-is-wrong rule` | 212-231 | |
| `## Behavior-is-documented rule` | 233-259 | EOF |

### 2.2 EXACT insertion point for `## Pipeline Hardening Closure`

The new section content is spec §8 (spec lines 299-312, a ```` ```markdown ```` block). It belongs **inside the embedded template**, as a new `##` section. Placement decision:

- It is closure-verdict content (PASS/FAIL/N-A per gate + closure verdict), conceptually a sibling of `## Risk + Rollback` and `## Follow-up tasks`, and must appear BEFORE `## Grounding Gaps` / `## Next Steps` / `## Audit` (those are tail sections).
- **Recommended insertion: immediately AFTER `## Follow-up tasks` (ends line 132) and BEFORE `## Grounding Gaps` (begins line 134).** I.e. insert between current line 132 and 133.
  - Rationale: the closure block is the last *diagnostic-substance* section; Grounding Gaps + Next Steps + Audit are meta/closing and should stay at the tail so `NOT PROVEN` blockers surfaced in the closure feed naturally into Grounding Gaps directly below.
- **Exact anchor for the builder's Edit:** insert after the line ``If there are no follow-ups, write "None."`` (currently line 132), before the `## Grounding Gaps` header (line 134). The blank line 133 separates them.

### 2.3 Content to insert (verbatim spec §8 markdown block)

Insert the spec §8 block (spec lines 300-312) as a rendered markdown section. Because it sits INSIDE the four-backtick `````markdown````` template fence, write it as plain markdown (NOT a nested fence — the outer four-backtick fence already establishes markdown context, same as every other `##` section in 8-202):

```
## Pipeline Hardening Closure

Render this section ONLY when `pipeline_hardening_applicable=true`. Omit entirely when the mode did not fire (and add the `pipeline_hardening_applicable=false` one-line reason to Grounding Gaps instead — see §6.1 of the hardening spec).

- Applicability: applicable | not applicable
- Mechanism statement:
- Runtime-entrypoint verification: PASS | FAIL | N/A — <card path>
- Contract enumeration: PASS | FAIL | N/A — <ledger path>
- Unmask-and-sweep: PASS | FAIL | N/A — <sweep path>
- Effective-input proof: PASS | FAIL | N/A — <card path>
- Off-path review decision: required | performed | waived_with_rationale | not_required
- Severity/blast-radius decision:
- Known escapes this would have caught: E...
- Closure verdict: pass | blocked | advisory
```

(The leading conditional-render sentence is house-style: mirrors `## Documentation Context` "If `--no-doc-discovery` ... omit this section" at `report-template.md:48` and `## Diagnosability Context` conditional at `:52`.)

### 2.4 NOT PROVEN blocker language requirement (spec §8 last paragraph, spec line 314)

Spec §8 line 314 mandates: *"The protocol must use `NOT PROVEN` blockers when any required proof is absent. This is intentionally stronger than ordinary confidence language because the canonical escapes came from accepting adjacent proof as if it covered the runtime contract."*

This is NOT captured by the §8 markdown block's enum (`pass | blocked | advisory`). The builder must ALSO add, in a post-template rule section (alongside `## Test-is-wrong rule` at line 212 and `## Behavior-is-documented rule` at line 233), a **`## Pipeline Hardening Closure rule`** that:
1. States that any missing required gate proof renders that gate line `FAIL` and the token to use is the literal `NOT PROVEN` (not "low confidence", not "unverified") — distinguishing it from the ordinary `## Grounding Gaps` softer language.
2. Sets `Closure verdict: blocked` whenever any required H1/H2/H3/H4 gate is `NOT PROVEN`.
3. Cross-links the per-gate refs (pipeline-hardening-closure.md etc.).

Recommended placement of this rule section: after `## Behavior-is-documented rule` (EOF, line 259) — append at end, consistent with the "rules accrete at the file tail" pattern (Test-is-wrong then Behavior-is-documented were each appended). This keeps the embedded template (8-203) and the rule sections (205-EOF) cleanly separated.

**Builder caution:** the `## Pipeline Hardening Closure` SECTION goes INSIDE the four-backtick fence (between lines 132-134); the `## Pipeline Hardening Closure rule` PROSE goes OUTSIDE/after the fence (after line 259). Conflating them breaks the fence nesting.

## 3. remediation-handoff.md — failure/blocked/remediated state model + §5.2 wiring point

File: `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`, 123 lines.

### 3.1 Current section map

| Section | Line range |
|---|---|
| `# Tier 3 Remediation Handoff (Wave 6)` + load condition | 1-2 |
| `## The user offer` (verbatim prompt, bare ``` fence) | 4-28 |
| `## Decision matrix` (yes/no/ambiguous table) | 30-37 |
| `## Phase A — Build the task file` (BUILD_REQUEST, bare ``` fence) | 39-66 |
| `## Phase B — Pre-execution review` (OK / Recommends refactor / **Blocker**) | 68-77 |
| `## Phase C — Execution gate (always user-initiated)` | 79-92 |
| `## Phase D — Post-execution validation (optional)` | 94-106 |
| `## Why this is the only safe handoff` | 108-114 |
| `## Failure modes` (4-row table) | 116-123 (EOF) |

### 3.2 Current model of failure / blocked / remediated states

remediation-handoff.md does **not** currently use an explicit `remediated` enum. The state language present:

- **Load gate (line 1):** the whole chain only loads when "Wave 5 produced a `success` (not `partial`) report." So a `partial` report already blocks Tier 3 entry — this is the existing coarse gate.
- **`remediation_accepted`** boolean (lines 33-36, 119): `true`/`false` per user consent; this is consent state, not proof state.
- **Blocker** state (Phase B, line 76): "STOP. Surface the blocker. Do not advance to Phase C until the user resolves it." — closest existing "blocked" concept.
- **`## Failure modes` table (116-123):** 4 rows mapping a failure → behaviour (task-builder error; reflect flags a blocker; refactor-then-no; user no-response).

There is NO current notion of "a fix is verified/remediated only if hardening gates passed." That is exactly the gap spec §5.2 fills.

### 3.3 Spec §5.2 rule to wire (spec lines 72-78)

Spec §5.2 (under "`sc:troubleshoot-protocol` skill", spec line 78) mandates: *"Wire failure states: a pipeline escape cannot be marked remediated when required hardening gates are missing, failed, or marked `N/A` without rationale."*

This is a **precondition on entering / closing the Tier 3 chain**, parallel to the existing `success`-not-`partial` load gate (line 1). Two coordinated edits:

**(a) Tighten the load/entry gate.** Edit the load-condition line (line 1-2) OR add an explicit pre-offer gate near `## The user offer` (line 4). Add a subsection — recommended `## Pipeline-hardening precondition` inserted BETWEEN line 2 and `## The user offer` (line 4), or as the first sub-bullet of the offer — stating:

> When `pipeline_hardening_applicable=true`, the Tier 3 offer is GATED: it does not surface (or surfaces only as a NOT-PROVEN blocker notice) unless `pipeline_hardening_verdict ∈ {pass, advisory}`. If any required gate (H1 runtime-entrypoint, H2 contract-ledger, H3 unmask-sweep, H4 effective-input when triggered) is `NOT PROVEN`, `FAIL`, or `N/A` without a written rationale, the escape **cannot be marked remediated**; the chain is BLOCKED and the report's Pipeline Hardening Closure verdict is `blocked`.

**(b) Add a `## Failure modes` row.** The cleanest, lowest-risk wiring is appending a row to the existing 4-row `## Failure modes` table (lines 116-123). **Exact anchor:** the table's last data row is line 122 (`| User does not respond ... | Treat as decline ... |`); the file ends at line 123. Insert a new row after line 122:

```
| `pipeline_hardening_applicable=true` but `pipeline_hardening_verdict ∈ {blocked}` or any required gate is `NOT PROVEN` / `N/A`-without-rationale | Do NOT offer or proceed with the chain; the escape is NOT remediated. Surface the `NOT PROVEN` gate(s) and the closure verdict `blocked`; record `remediation_accepted=false`, `remediated=false`; point the user back to the failing hardening gate ref |
```

This matches the existing table's `| Failure | Behaviour |` 2-col shape (header line 117, separator line 118).

### 3.4 Recommendation on where the §5.2 rule primarily lives

Put the **authoritative rule** in `pipeline-hardening-closure.md` (the new mode ref) as a `## Remediation gating` / blocking-rule section, and add only the **two thin wiring touches above** to remediation-handoff.md (one precondition subsection + one failure-modes row) that REFERENCE it. Rationale: remediation-handoff.md's job is the consent/handoff choreography (offer → A → B → C → D), not hardening semantics; keeping the hardening verdict logic in the hardening ref preserves the SKILL.md-stays-navigable / refs-own-detail convention (spec §5.2 line 76: "Add one or more refs/templates for the closure cards, so the main SKILL.md remains navigable"). The two touches keep handoff correctness local without duplicating the rule.

## 4. The 5 NEW refs — per-file build recommendation

All under `src/superclaude/skills/sc-troubleshoot-protocol/refs/`. Each: no frontmatter, one `# Title` line 1, purpose line, then templates/tables/blocking-rule. Filenames are fixed by spec §9 (spec lines 329-333) and the track goal.

### 4.1 `pipeline-hardening-closure.md` (the mode index/orchestrator ref)

- **Derives from:** spec §6 (mode: trigger §6.1, output-contract fields §6.2), §7 Wave H0 (applicability statement), §8 (report section + NOT PROVEN), §5.2 (remediation gating).
- **Must contain:**
  - Purpose line: "Loaded when the Pipeline Hardening Closure mode fires (after Tier 1 diagnosis, before Wave 5 closure)." (spec §5.2 line 75).
  - `## Trigger` — the §6.1 bullet list (spec lines 84-94) + the skip rule "`pipeline_hardening_applicable=false` with a one-sentence reason" (spec line 96).
  - `## Output contract fields` — raw pipe table = spec §6.2 (spec lines 102-111), 8 fields.
  - `## Wave H0 — applicability and mechanism statement` — spec lines 115-128 (the `pipeline_hardening_applicable` decision, mechanism paragraph, candidate `known_escapes_caught`, pass criteria).
  - `## Report section` — the spec §8 ```` ```markdown ```` block (cross-ref to report-template.md so it is not duplicated divergently — state "rendered into REPORT.md per report-template.md `## Pipeline Hardening Closure`").
  - `## Closure verdict + NOT PROVEN rule` — spec §8 line 314 verbatim requirement; `blocked` whenever any required gate is NOT PROVEN.
  - `## Remediation gating` — the authoritative §5.2 rule (escape not remediated unless gates pass; see this report §3.4).
  - `## Index of gate refs` — links to the 4 gate refs below (H1→runtime-entrypoint-verification.md, H2→contract-enumeration.md, H3→unmask-and-sweep.md, H4→effective-input-proof.md).
- **Length estimate:** ~130-190 lines (longest of the 5; it is the hub).

### 4.2 `runtime-entrypoint-verification.md` (Gate H1)

- **Derives from:** spec §7 Gate H1 (spec lines 130-163).
- **Must contain:**
  - Purpose line + "Maps to generalized R1, R3, R5, R6" (spec line 132).
  - `## Card` — the ```` ```text ```` card VERBATIM from spec lines 136-151 (13 fields: Production/operator entrypoint … Known escapes caught).
  - `## Blocking rule` — spec lines 153-156 (helper-only proof fails; ≥1 negative control required for forbidden interpretations).
  - `## Escapes caught in one shot` — spec lines 158-162 (E1/E2/E3/E4/E5 mappings) as a bullet list.
- **Length estimate:** ~55-75 lines.

### 4.3 `contract-enumeration.md` (Wave H2)

- **Derives from:** spec §7 Wave H2 (spec lines 165-194).
- **Must contain:**
  - Purpose line + "Maps to generalized R1, R2, R5, R6" (spec line 167).
  - `## Ledger` — the 9-row ```` | Field | Required content | ```` pipe table VERBATIM from spec lines 171-180 (Contract, Producers, Transformers, Consumers, How found, Role, Expected behavior, Decision, Evidence). Render as a RAW pipe table (per §1.5 of this report), NOT inside a fence.
  - `## Blocking rule` — spec lines 184-187 (unclassified live consumer fails; generic-for-product fails; un-swept siblings fail).
  - `## Escapes caught in one shot` — spec lines 189-194.
- **Length estimate:** ~50-70 lines.

### 4.4 `unmask-and-sweep.md` (Wave H3)

- **Derives from:** spec §7 Wave H3 (spec lines 196-231).
- **Must contain:**
  - Purpose line + "Maps to generalized R3, R4, R6, R7" (spec line 198).
  - `## Required outputs` — the 10-item bullet list (spec lines 202-211: anchor failure … severity cost review).
  - `## Minimum regression pattern` — the 4-item ordered list (spec lines 215-218: positive case, sibling/off-path negative, full-artifact/live-boundary, severity assertion).
  - `## Blocking rule` — spec lines 220-223 (repro-only fails; hard-fatal heuristic parser without adversarial false-positive fixtures + cost rationale fails).
  - `## Escapes caught in one shot` — spec lines 225-231.
- **Length estimate:** ~55-75 lines.

### 4.5 `effective-input-proof.md` (Gate H4)

- **Derives from:** spec §7 Gate H4 (spec lines 233-264).
- **Must contain:**
  - Purpose line + "Maps to generalized R5" (spec line 235).
  - `## Trigger` — spec line 237 (indirect selector: diff range, file list, path glob, artifact path, cached metadata, stdout/log capture, resume state, model-produced filename).
  - `## Required proof` — the ```` ```text ```` "Effective Input Proof" card VERBATIM from spec lines 241-253 (10 fields).
  - `## Blocking rule` — spec lines 255-258 (PASS-artifact/reviewer/command-presence insufficient; fails closed on absent/empty/non-reproducible/foreign input).
  - `## Escapes caught in one shot` — spec lines 260-264 (E5 directly, E4/E1 secondarily).
- **Length estimate:** ~55-75 lines.

### 4.6 RECOMMENDATION: Rule H5 (off-path-reviewer) — fold into `pipeline-hardening-closure.md`, do NOT create a 6th ref

**Decision: H5 is a RULE, not a card/gate, and should live as a `## Rule H5 — off-path-reviewer` section inside `pipeline-hardening-closure.md` — NOT as its own ref, and NOT inside effective-input-proof.md.**

Rationale (evidence-based):
1. **Spec taxonomy:** spec §1 lists H5 as the 4th item "Off-path-reviewer rule" (spec line 16), and spec §7 labels it **"### Rule H5"** (spec line 266) — a sibling of the §7 "### Gate H1", "### Gate H4" headers but explicitly typed a *Rule*, not a *Gate/Wave*. The 5 named new-ref filenames in spec §9 (lines 329-333) do NOT include an `off-path-reviewer.md` — the spec author already chose 5 files and H5 is not one. Creating a 6th ref would contradict the spec's own file inventory.
2. **H5 has no fill-in card.** Unlike H1 (spec lines 136-151) and H4 (spec lines 241-253) which each carry a ```` ```text ```` card that justifies a dedicated card-ref, H5 is three prose lists: trigger conditions (spec lines 270-280), acceptable forms (spec lines 282-288), waiver standard (spec lines 290-294). It is decision/policy prose, which the house style keeps in a hub ref's `##` section (cf. escalation-rubric.md's "## Escalation decision" prose at lines 52-72).
3. **H5 output is a single contract field, not an artifact path.** The §6.2 contract (spec line 110) exposes H5 only as `off_path_review_decision` (`required | performed | waived_with_rationale | not_required`) — no `*_card_path`/`*_path` field, unlike H1/H2/H3/H4 which each get a path field (spec lines 106-109). Refs in this dir map 1:1 to artifact-producing gates; H5 produces a *decision token*, which belongs in the mode-index ref that already owns the output-contract table.
4. **Why NOT fold into effective-input-proof.md:** H5's triggers (spec lines 270-280) span ALL boundary types (subprocess, filesystem, generated artifacts, persisted state, sibling pipelines, HALT/WARN control), not just review-input selectors. effective-input-proof.md (H4) is narrowly scoped to review/audit selector inputs. Folding the broad off-path policy into the narrow H4 ref would mis-scope it and hide it from non-review escapes (E1/E2/E3). The hub ref `pipeline-hardening-closure.md` already references all four gates and is where the cross-cutting H5 decision is recorded.

**Net:** 5 new refs exactly (matching spec §9). H5 = a `## Rule H5 — off-path-reviewer` section in `pipeline-hardening-closure.md`, carrying the trigger list + acceptable-forms list + waiver standard (spec lines 270-294) and feeding the `off_path_review_decision` contract field.

## 5. markdownlint considerations (so new/edited refs pass pre-commit)

The repo runs a pre-commit markdownlint hook (per memory `reference_markdownlint_md025_frontmatter_title.md`). Rules that bite for THIS work:

- **MD025 (single-H1 / front_matter_title):** No frontmatter on any ref (§1.1). Exactly one `# ` per file (line 1). New refs: do NOT add `---` frontmatter and do NOT add a `title:` — that combination is what trips MD025 against a body H1. Existing siblings are clean precisely because they have no frontmatter.
- **MD040 (fenced-code-language):** EVERY fence needs a language. Use `text` for fill-in cards (H1 card, H4 card — both ```` ```text ```` in spec), `markdown` for the §8 report block. Do NOT leave bare ``` ``` (the pre-existing bare fences in remediation-handoff.md:9/42/82/100 are tolerated legacy, but new content should tag fences).
- **MD031 / MD032 (blanks around fences and lists):** keep a blank line before and after every fenced block and every list — the exemplar refs do (e.g. blank line before ```` ```markdown ```` at hypothesis-card-template.md:8/9). The verbatim spec blocks already have surrounding blanks; preserve them on copy.
- **MD013 (line-length):** check whether the repo disables it — the exemplar refs contain very long lines (e.g. escalation-rubric.md:18, report-template.md:226 run well past 80 chars) and are committed clean, so MD013 is effectively OFF or relaxed in `.markdownlint*` config. Builder should still verify by running the hook; do NOT hard-wrap prose to 80 (would diverge from house style).
- **MD024 (no-duplicate-heading):** the 4 gate refs each use `## Blocking rule` and `## Escapes caught in one shot` — these are in DIFFERENT files, so no collision. WITHIN `pipeline-hardening-closure.md`, avoid repeating an identical `##` text (e.g. don't have two `## Blocking rule`); if needed, qualify (`## Closure verdict + NOT PROVEN rule`).
- **MD047 (single-trailing-newline) / MD009 (no-trailing-spaces):** standard; just end each file with one newline and no trailing whitespace.
- **Four-backtick fence integrity (report-template.md edit):** when inserting `## Pipeline Hardening Closure` between lines 132-134, you are inside the four-backtick `````markdown````` fence (7→203). Do NOT introduce a three-backtick fence there unless intended as nested content (the §8 block is rendered markdown prose, not a nested code block — keep it bare inside the outer fence, exactly like every other `##` section in 8-202). Re-verify the closing ```` ```` at line 203 still matches after the edit.

**Post-edit verification the builder must run:** the pre-commit markdownlint hook, plus `make sync-dev` then `make verify-sync` (src→.claude mirror; per CLAUDE.md and spec §10 item 10). Never stage `.claude/` mirrors (CLAUDE.md absolute rule).

## 6. Summary for the builder (what to create/edit, precisely)

**CREATE 5 refs** in `src/superclaude/skills/sc-troubleshoot-protocol/refs/` (no frontmatter, one `# Title`, purpose line, then spec-verbatim cards/tables + blocking rule):
1. `pipeline-hardening-closure.md` — hub: trigger (§6.1), output-contract table (§6.2), Wave H0 (§7), report-section cross-ref + NOT PROVEN rule (§8), remediation gating (§5.2), **and `## Rule H5 — off-path-reviewer`** (§7 lines 266-294). ~130-190 lines.
2. `runtime-entrypoint-verification.md` — Gate H1, ```` ```text ```` card (spec 136-151) + blocking rule + escapes.
3. `contract-enumeration.md` — Wave H2, raw 9-row ledger pipe table (spec 171-180) + blocking rule + escapes.
4. `unmask-and-sweep.md` — Wave H3, required outputs + minimum regression pattern + blocking rule + escapes.
5. `effective-input-proof.md` — Gate H4, ```` ```text ```` card (spec 241-253) + trigger + blocking rule + escapes.

**EDIT 2 files:**
- `report-template.md`: (a) insert `## Pipeline Hardening Closure` section (spec §8 block) INSIDE the four-backtick template fence, between line 132 (after `If there are no follow-ups, write "None."`) and line 134 (`## Grounding Gaps`); (b) append a `## Pipeline Hardening Closure rule` prose section AFTER current EOF (line 259) encoding the `NOT PROVEN` blocker requirement (spec line 314).
- `remediation-handoff.md`: (a) add a `## Pipeline-hardening precondition` subsection between line 2 and `## The user offer` (line 4) gating the Tier 3 offer on hardening verdict; (b) append one row to the `## Failure modes` table after line 122 for the `NOT PROVEN`/`blocked` case. Authoritative §5.2 rule lives in pipeline-hardening-closure.md; these are thin wiring touches.

**FLAGGED for R1 (SKILL.md track):** append 5 rows to the ref→wave table at `SKILL.md:540-546` (one per new ref) + a lazy-load mention in the new pipeline-hardening wave step.

**Status:** Complete
