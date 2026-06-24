# Research: task-builder SKILL.md anchors

**Status:** Complete
**Date:** 2026-06-04
**Scope:** `src/superclaude/skills/task-builder/SKILL.md` ONLY (current length: **2190 lines**, NOT 2191 as the proposal's header states).
**Driving proposal:** `.dev/proposals/reflect-in-task-builder.md` (§6 Pipeline Wiring + §8 Implementer Checklist).

> **DRIFT BANNER:** The proposal's cited line anchors have drifted. The single biggest structural drift: a NEW section **`### A.10.6: DM-005 Phase Contract`** (lines 1339–1396) now sits **between A.10.5 and A.11**. The proposal repeatedly says the PRE gate inserts "between A.10.5 and A.11" — that boundary is no longer adjacent. See edit-site 3 for the corrected insertion point. Every line number below was re-verified by Read on 2026-06-04 against the current file.

---

## Edit-site 1 — Input / flags surface (`--spec`)

**Section:** `## Input` starts at **line 29**. Structure is a 4-item numbered list (NOT a flag table):

- L29 `## Input`
- L31 prose: "four pieces of information … first is mandatory; the rest are optional"
- L33 `1. **GOAL — what task to build** (mandatory)`
- L35 `2. **WHY — context** (strongly recommended)`
- L37 `3. **WHERE — source directories** (optional, …)`
- L39 `4. **BUILD_REQUEST file path** (optional)`
- L41 `### Effective Prompt Examples`

**Finding:** There is **no flags table** anywhere in the Input section — inputs are described as natural-language GOAL/WHY/WHERE + an optional BUILD_REQUEST path. There is **no existing `--spec`, `--depth`, or any `--flag` documented in the Input section** (verified: `grep -nE "^\s*[-*].*--[a-z]" ` returns nothing in 29–87). The `--spec` flag must be added as a **new numbered item 5** (or a sub-note on item 1/4), since the proposal (§6.3) wants the priority order `explicit --spec → @file in GOAL → SPEC:/PRD:/TDD: in BUILD_REQUEST → none`. Recommended anchor: insert a new item after **line 39** (item 4) and before `### Effective Prompt Examples` (line 41).

---

## Edit-site 2 — A.2 Parse & Triage (spec_path resolution)

**Section heading:** `### A.2: Parse & Triage` at **line 190** (proposal cites "SKILL.md:190" — STILL ACCURATE).

Current structure of A.2:
- L190 `### A.2: Parse & Triage`
- L192 "Break the user's request into structured components:"
- L194–197 bullet list: `**GOAL**`, `**WHY**`, `**OUTPUTS**`, `**CONTEXT**`
- L199 `**Triage into Scenario A or B:**`
- L209 "**Do NOT interrogate the user…**"
- L211 `**Determine track count:**`

**Best insertion anchor for spec_path resolution:** immediately after the GOAL/WHY/OUTPUTS/CONTEXT bullet block (after **line 197**, before line 199 `**Triage into Scenario A or B:**`). Add a `**SPEC_PATH** (resolved in priority order: explicit --spec → @file in GOAL → SPEC:/PRD:/TDD: in BUILD_REQUEST → none)` component. The proposal §6.3 also says the resolved path is "written to tasklist frontmatter as `spec_path:`" — that wiring is edit-site 7.

---

## Edit-site 3 — A.10.7 PRE reflect gate insertion boundary (CRITICAL DRIFT)

**Proposal claim:** insert `### A.10.7: PRE Reflect Gate` "between A.10.5 qualitative validation and A.11 present results" / "after the qualitative gate (A.10.5:1194) and before A.11 (SKILL.md:1398)".

**CURRENT REALITY (drift):**
- L1194 `### A.10.5: Task File Qualitative Validation` ✅ (proposal's 1194 still accurate for A.10.5 heading)
- A.10.5 body runs **1194 → 1337** (ends after the INV-010 enumeration procedure, last line at L1337).
- **L1339 `### A.10.6: DM-005 Phase Contract — rf-qa → rf-qa-qualitative (published row)`** ← NEW section the proposal did not anticipate. Runs **1339 → 1396**.
- L1398 `### A.11: Present Results` ✅ (proposal's 1398 still accurate for A.11 heading).

**Corrected insertion point:** A new `### A.10.7: PRE Reflect Gate` must go **after A.10.6 ends (line 1396) and before A.11 (line 1398)** — i.e. insert at the blank line between L1396 and L1397/L1398. (The literal numbering "A.10.7" is fine and stays after A.10.6.) Inserting between A.10.5 and A.10.6 would split the qualitative-validation → phase-contract pair and is NOT recommended. Exact boundary text:

```
1396:- Future consumers of `schema_version: 1.0.0` versioning baseline: …
1397:(blank)
1398:### A.11: Present Results
```

Insert the new `### A.10.7` block at line 1397 (between 1396 and 1398).

---

## Edit-site 4 — Pipeline-overview numbered steps (Execution Overview)

**Section:** `## Execution Overview` at **line 143**. The numbered "Stage A" list is at **lines 149–161** (proposal cites "current steps 12 and 13, SKILL.md:160-162" — CLOSE; the list is 149–161, step 12 = L160, step 13 = L161):

- L159 `11. Task file structural validation — rf-qa … (A.10)`
- L160 `12. Task file qualitative validation — rf-qa-qualitative … (A.10.5)`
- L161 `13. Present results — task file path, quality gate summary, … (A.11)`

**Insertion:** Add a NEW bullet **between step 12 (L160) and step 13 (L161)** for the PRE reflect gate (A.10.7), e.g. a new "13. PRE reflect gate …" and renumber present-results to 14. NOTE: this numbered list does **not** mention A.10.6 (the DM-005 Phase Contract is documentation, not a runtime pipeline step), so the overview jumps A.10.5 → A.11 today; the new A.10.7 bullet is the only addition needed.

**Companion resume-map drift:** lines **163–169** (and the A.1 resume map, lines **180–188**) enumerate resume points ("Task file + both validation reports exist → skip to A.11"). If the PRE gate becomes a resumable step, these two maps may also need an A.10.7 entry — flag for the task builder, but the proposal §8 does not explicitly require it.

---

## Edit-site 5 — A.9 BUILD_REQUEST `EXECUTION_CONTEXT_REQUIREMENTS` field (POST_REFLECT_GATE insert)

**Section:** `### A.9: Spawn Builder` at **line 781**. The BUILD_REQUEST template block starts at L787 (` ```text `) inside an `Agent:` spawn spec.

**`EXECUTION_CONTEXT_REQUIREMENTS` field block:** **lines 827–847** (proposal cites "SKILL.md:804-847" for the field cluster; the EXECUTION_CONTEXT_REQUIREMENTS field specifically is **827–847**). It opens:
```
827:    EXECUTION_CONTEXT_REQUIREMENTS: [OPTIONAL signal (API-001-M2) controlling
...
847:      or omitting the block under REQUIRED.]
```
The next field after it is `DOCUMENTATION STALENESS WARNINGS:` at **line 849**.

**Insertion for the new `POST_REFLECT_GATE` field:** insert immediately after **line 847** (the closing `]` of EXECUTION_CONTEXT_REQUIREMENTS) and before **line 849** (`DOCUMENTATION STALENESS WARNINGS:`) — i.e. at the blank line 848. This matches the proposal's "strictly-additive, after `EXECUTION_CONTEXT_REQUIREMENTS`" (§6.2).

---

## Edit-site 6 — Critical Rules #16 / #17 / #18 (new POST-gate rule)

**Section:** `## Critical Rules (Non-Negotiable)` at **line 1998**. Numbered list starts at L2000 (rule 1).

Verbatim current rules (proposal cites #16 at "SKILL.md:2030" — STILL ACCURATE):

- **L2030 — Rule 16:** `**QA gates in generated task files.** When the BUILD_REQUEST specifies QA_GATE_REQUIREMENTS of FINAL_ONLY or PER_PHASE, the builder MUST encode corresponding QA gate checklist items in the generated task file. These items must specify the QA agent type (rf-analyst, rf-qa, rf-qa-qualitative), the QA mode, the files to verify, and the pass/fail handling. A generated task file that omits required QA gates is a MALFORMED output.`
- **L2032 — Rule 17:** `**Validation in generated task files.** … Validation items must be placed AFTER the phase they validate and BEFORE the next phase begins. A task file with implementation items but no validation items (when VALIDATION_REQUIREMENTS is non-empty) is a MALFORMED output.`
- **L2034 — Rule 18:** `**Testing in generated task files.** … Testing items are placed after implementation items and before QA gate items. A generated task file that requires testing items … but omits them is a MALFORMED output.`

**Highest rule number = 18.** After rule 18 (L2034) there is a `**Precedence rule:**` paragraph at **L2036** (un-numbered), then the section closes with `---` at L2038 and `## Research Quality Signals` at L2040.

**Insertion for the new POST-gate rule (#19):** insert as a new numbered **19.** between rule 18 (L2034) and the `**Precedence rule:**` paragraph (L2036) — OR after the Precedence rule (L2036) before the `---` (L2038). Recommended: insert as **#19 immediately after L2034 and before L2036**, keeping the precedence note last. The proposal's drafted rule (§6.2): *"When `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase … a fresh-session reflect handoff item … writes `reflect_post: PENDING` … and HALTs."* Phrase as MALFORMED-on-omission to mirror Rule #16.

---

## Edit-site 7 — Output Structure: frontmatter + Phase N example

**Section:** `## Output Structure` at **line 1861**. Generated-MDTM example fenced block runs **1865–1949**.

### 7a. Frontmatter block (where `spec_path` / `reflect_pre` / `reflect_post` go)
**Lines 1866–1885** (the `---` … `---` YAML block):
```
1866:---
1867:id: "TASK-RF-YYYYMMDD-HHMMSS"
1868:title: …
1870:status: "🟡 To Do"
1871:type: "🔧 Refactor"  # or 📝 Documentation, ✨ Feature, etc.
1873:created_date / 1874:updated_date / 1875:assigned_to
1876:template_schema_doc / 1877:estimation / 1878:task_type: static
1879:related_docs: (1880–1881)
1882:tags: (1883–1884)
1885:---
```
**Insertion:** add `spec_path:`, `reflect_pre:`, `reflect_post:` keys inside this YAML — natural home is after `task_type: static` (L1878) and before `related_docs:` (L1879), or after `tags:` (before closing `---` at L1885). The proposal §6.1 sign-off block (`reflect_pre: {verdict, coverage_pct, depth, tcs, run_id, report, reviewed_at}`) lands here. NOTE: `type: "🔧 Refactor"` at **L1871** is the exact field S6 (TCS signal 6) reads — confirm the refactor-class enum values cited in proposal §5.1 (`🔧 Refactor`) match this line's emitted value.

### 7b. `## Phase N` final-phase example (where the penultimate reflect item inserts)
**Lines 1928–1935:**
```
1928:## Phase N: [Final Phase — includes completion items]
1929:(blank)
1930:- [ ] **N.X — Update task status to Done**
1931:  - **Context**: All phases complete.
1932:  - **Action**: Update frontmatter: status to "🟢 Done", set completion_date.
1933:  - **Output**: Task file updated.
1934:  - **Verification**: Frontmatter shows "🟢 Done".
1935:  - **Completion gate**: Task marked complete.
```
**Insertion:** the new POST reflect item (`N.{X-1}`) inserts as the **penultimate** item — between **line 1929** (blank after the Phase N heading) and **line 1930** (`N.X — Update task status to Done`), so the Done item stays last (anti-orphaning, see edit-site 8). The proposal §6.2 supplies the full B2-self-contained templated item body.

---

## Edit-site 8 — Task File Validation Checklist (POST-reflect-item check)

**Section:** `## Task File Validation Checklist` at **line 1953**. Checklist items run **1957–1979**.

- L1957 `- [ ] Frontmatter properly populated (id, title, status, created_date, related_docs)`
- **L1969 `- [ ] Task completion items inside final phase (anti-orphaning)`** ← the anti-orphaning criterion the proposal §2.2 cites as "SKILL.md:1969" (STILL ACCURATE).
- L1972–1979 are the `TB-Add-1` … `TB-Add-8` enumerated additions (TB-Add-8 at **L1979** is the last existing item).

**Insertion for the new "POST reflect item present + positioned when enabled" check:** add a new **`TB-Add-9`** immediately after **line 1979** (TB-Add-8), before the closing `---` at L1981. Place near/after the anti-orphaning line (L1969) conceptually, but mechanically appending as TB-Add-9 keeps the numbered TB-Add catalogue contiguous. The proposal §8 + §7-risk-5 want a Rule#16-style MALFORMED guard: "POST reflect item present and positioned penultimate (before Done) when `POST_REFLECT_GATE: ENABLED`."

> **Cross-skill note (DO NOT EDIT here, flag for R2/rf-qa.md):** the TB-Add catalogue's *authoritative source* is `rf-qa.md`'s `#### Structural Gate Additions` span, dynamically enumerated by the A.10.5 INV-010 procedure (SKILL.md:1326–1337). Adding a `TB-Add-9` only to this SKILL.md checklist without a matching entry in `rf-qa.md` will be an **orphan** (INV-010 cross-check, L1332 fails the spawn with `INV-010-orphan-tb-add`). The task builder MUST add the TB-Add-9 row to `src/superclaude/agents/rf-qa.md` too. This is an integration hazard outside this file's scope — surfaced for the parent.

---

## Edit-site 9 — A.11 present-results output blocks (REFLECT GATES + per-track row)

**Section:** `### A.11: Present Results` at **line 1398** (proposal cites "SKILL.md:1404-1433" for the output block — accurate).

### 9a. Single-track result format
Fenced ```text``` block **1404–1433**. Relevant region:
```
1414:QUALITY GATES:
1415:  Research gate: [PASS/FAIL] ([N] researchers, [N] gap-fill rounds)
1416:  Task structural validation: [PASS/FAIL] ([N] issues fixed in-place)
1417:  Task qualitative validation: [PASS/FAIL] ([N] issues fixed in-place)
1418:(blank)
1419:TASK FOLDER: ${TASK_DIR}
...
1431:TO EXECUTE:
1432:  /task ${TASK_DIR}${TASK_ID}.md
1433:================================================================  (closing fence at 1434)
```
**Insertion for the `REFLECT GATES` block (proposal §6.5):** add after the `QUALITY GATES:` block (after **L1417**, before the blank L1418 / `TASK FOLDER`). The proposal's drafted block (PRE verdict line + POST "TEMPLATED as final-phase item N.{X-1}") lands here. The `TO EXECUTE: /task …` at L1431–1432 already uses `/task` (never `/sc:task`) — preserve that.

### 9b. Multi-track result format
Fenced ```text``` block **1438–1461** (proposal §7-risk-6 cites "SKILL.md:1436" for the multi-track format heading; the `**Multi-track result format:**` label is at **L1436**, fence opens L1438). Per-track rows:
```
1443:--- Track 1: [goal] ---
1445:TEMPLATE: [01/02] | ITEMS: [X] | PHASES: [N] | BATCH: [N]
1446:GATES: research=[PASS/FAIL] | validation=[PASS/FAIL]
1448:--- Track 2: [goal] ---
1450–1451: (same shape)
```
**Insertion for the per-track REFLECT row:** add a `REFLECT: pre=[…] | post=[templated]` line under each track's `GATES:` line (after **L1446** for Track 1, after **L1451** for Track 2). The proposal §7-risk-6 requires "a per-track `REFLECT` row."

---

## Edit-site 10 — Where the new `## Reflect Depth (Deterministic TCS)` section best lands

**Recommendation:** Insert a new top-level `## Reflect Depth (Deterministic TCS)` section **between `## Critical Rules` (ends with `---` at L2038) and `## Research Quality Signals` (L2040)** — i.e. insert at **line 2039**. Rationale:
- The TCS formula is referenced by the new A.10.7 PRE gate (computes `pre_depth`) AND by the POST_REFLECT_GATE BUILD_REQUEST field (computes `DEPTH` floored at standard). Placing it as a standalone `##` after the rules keeps it a stable, citable anchor both upstream references can point to.
- Alternative considered: immediately after A.10.7 (near L1397). Rejected — A.10.7 sits mid-pipeline (Stage A), and a long TCS-formula table there would bloat the pipeline narrative. The reference-section neighborhood (Critical Rules → Research Quality Signals → Artifact Locations) is the established home for non-pipeline reference material.

Surrounding headings at the recommended insertion point:
```
2036:**Precedence rule:** …
2038:---
2039:(insert `## Reflect Depth (Deterministic TCS)` here)
2040:## Research Quality Signals
```

---

## Edit-site 11 — S4 / TCS TRIM CONFIRMATION

**Command run:** `grep -nE "TCS|Tasklist Complexity|S4|blockedBy|depends_on|after Phase" src/superclaude/skills/task-builder/SKILL.md`

**Result — single hit:**
```
1993:| Phase dependencies | Explicit ordering: "after Phase N completes" | Implicit ordering relying on execution order |
```

**Interpretation:**
- **`TCS`** — 0 occurrences. **No existing "Tasklist Complexity Score" content.** ✅ The entire TCS section (formula, threshold table, FERs) is NEW content to author at edit-site 10 — there is **no existing anchor to edit**, only new content to write.
- **`Tasklist Complexity` / `S4`** — 0 occurrences.
- **`blockedBy`** — **0 occurrences.** Confirms the user's S4 trim: the proposal's `blockedBy:` token would match **nothing** in the current corpus, so dropping it from the S4 token set is safe and avoids an inert signal.
- **`after Phase`** — 1 occurrence, **L1993**, but it is a **Content-Rules table cell** (`| Phase dependencies | Explicit ordering: "after Phase N completes" | …`) — it is *guidance prose about how to phrase dependencies in generated tasklists*, NOT a token emitted into a generated MDTM body. So the S4 extraction rule (which counts dependency tokens *in generated tasklist items*) would not collide with this — but the implementer should be aware the literal string `after Phase` exists once in the skill's own Content Rules.
- Supplementary grep `depends on|depends_on|after N\.`: `depends_on` = 0; `depends on` appears at L220 (`- No track depends on another track's outputs`, a Multi-Track rule) and L2124 (same string in Track Determination Rules) — both are **track-isolation prose**, not generated-MDTM dependency tokens, so no collision with S4 counting.

**S4 token-set guidance for the task builder:** Write S4's frozen token set as **`{after Phase \d+, depends_on:}`** per the user's instruction — **drop `blockedBy:`** (0 corpus hits, would be inert) **and drop `after N\.\d+`** (the proposal's 4-token form). The remaining `after Phase \d+` form has exactly one same-skill occurrence (L1993, a Content-Rules description) and the `depends_on:` form has zero — neither collides with the *generated-tasklist* counting surface S4 targets.

---

## Summary: edit-site → current-line map

| # | Edit site | Current heading / anchor | Current line(s) | Insert at | Drift vs proposal |
|---|-----------|--------------------------|-----------------|-----------|-------------------|
| 1 | Input/flags `--spec` | `## Input` (4-item numbered list, NO flag table) | 29; items 33/35/37/39 | after L39 (new item 5) | proposal assumes a flags surface; it's a prose list |
| 2 | A.2 spec_path resolution | `### A.2: Parse & Triage` | 190; components 194–197 | after L197 | ✅ L190 accurate |
| 3 | A.10.7 PRE gate boundary | A.10.5 (1194) → **A.10.6 (1339–1396)** → A.11 (1398) | 1396↔1398 | L1397 | ⚠️ NEW A.10.6 now between A.10.5 & A.11 |
| 4 | Pipeline overview steps | `## Execution Overview` list | 149–161 (step12=160, step13=161) | between L160 & L161 | ✅ ~accurate (list is 149–161) |
| 5 | A.9 BUILD_REQUEST field | `EXECUTION_CONTEXT_REQUIREMENTS` | 827–847 | L848 (before L849 STALENESS) | ✅ 827–847 |
| 6 | Critical Rules 16/17/18 | `## Critical Rules` | R16=2030, R17=2032, R18=2034 | new #19 after L2034 (before Precedence L2036) | ✅ #16=2030; highest=18 |
| 7a | Frontmatter (spec_path/reflect_*) | Output Structure YAML | 1866–1885 (type at 1871) | after L1878 or before L1885 | ✅ |
| 7b | Phase N reflect item | `## Phase N: [Final Phase …]` | 1928–1935 (Done item 1930) | between L1929 & L1930 (penultimate) | ✅ 1928–1935 |
| 8 | Validation checklist | `## Task File Validation Checklist` (anti-orphan L1969; TB-Add-8 L1979) | 1953; 1957–1979 | new TB-Add-9 after L1979 | ✅ 1969 accurate; +rf-qa.md cross-edit needed |
| 9a | A.11 single-track REFLECT block | `### A.11` single-track fence | 1404–1433 (QUALITY GATES 1414–1417) | after L1417 | ✅ |
| 9b | A.11 multi-track per-track row | multi-track fence | 1436–1461 (GATES 1446/1451) | after L1446 & L1451 | ✅ |
| 10 | New TCS section | between `## Critical Rules` (---L2038) and `## Research Quality Signals` (L2040) | — | L2039 | NEW content, no existing anchor |
| 11 | S4/TCS trim confirm | only `after Phase` at L1993 (Content-Rules cell) | 1993 | n/a (NEW content) | TCS/blockedBy/depends_on = 0 hits |

**Note on file length:** current = **2190 lines** (proposal header says 2191; off by 1 — negligible but noted for evidence integrity).
