# Research: tasklist command + templates

Status: In Progress
Date: 2026-06-04
Researcher: R3
Scope (3 files only):
- `src/superclaude/commands/tasklist.md` (118 lines)
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (126 lines)
- `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md` (141 lines)

Proposal driver: `.dev/proposals/reflect-in-sc-tasklist.md` — §6 "Flag/stage summary" (lines 282-286), §1(b) "Templated POST task" (lines 163-211), §1(a) index "Pre-Reflect Sign-off" column (lines 137-162).

> Note: line counts above are the file lengths as Read this session; cite line numbers below are from those same Reads.

---

## Proposal anchors (re-stated for the builder)

- **§6 (lines 282-286)** — surface changes: add `--no-reflect` escape hatch to BOTH `commands/tasklist.md` Arguments table AND the skill `argument-hint` (default off; skips both gates; used by `--dry-run`). **No model-routing flag is added.** (Skill-side Stage 10.5 + Stage 5 templating + 4-invariant amendment are out of R3 scope — they live in the SKILL.md, R2's territory.)
- **§1(a) (lines 159-161)** — index gets a new **"Pre-Reflect Sign-off" table column** (`reflect_pre: PASS (depth=<d>, coverage=<pct>)` per phase) plus a bundle-level `reflect_pre_summary: {pass: x, partial: y, fail: z}` in index metadata.
- **§1(b) (lines 163-209)** — templated terminal POST task with exact metadata table, spawn directive, 4 acceptance criteria, placed AFTER the end-of-phase checkpoint.

---

## A. `src/superclaude/commands/tasklist.md`

### A.1 — Full Arguments table (quoted, lines 32-38)

```
## Arguments                                                            (L32)

| Argument | Required | Default | Description |                          (L34)
|----------|----------|---------|-------------|                          (L35)
| `<roadmap-path>` | Yes | -- | Path to roadmap file. Accepts `@file` reference or explicit path. |   (L36)
| `--spec <spec-path>` | No | -- | Supplementary spec/context file for additional generation context. |  (L37)
| `--output <output-dir>` | No | Auto-derived from roadmap `TASKLIST_ROOT` | Output directory for the tasklist bundle. |  (L38)
```

Three flags total. The table body is lines 36-38; header is 34-35.

### A.2 — `--spec` ALREADY EXISTS (verified via grep). DO NOT re-add.

grep `-- "--spec"` returns SIX hits, confirming the flag is fully wired:

- **L23** (Usage code block): `/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>]`
- **L26**: "Both `@file` syntax and explicit file paths are supported for `<roadmap-path>` and `--spec`."
- **L37** (Arguments table row — the canonical definition): `| `--spec <spec-path>` | No | -- | Supplementary spec/context file for additional generation context. |`
- **L63** (Input Validation check #2): "**Spec file exists (if provided)**: `--spec` path resolves to a readable file."
- **L93** (example): `/sc:tasklist @roadmap.md --spec @specs/auth-system-prd.md`
- **L99** (example): full invocation with `--spec @specs/v3-prd.md`

**VERDICT for builder: `--spec` is real and complete. The proposal's §3 (line 220) assertion `commands/tasklist.md:37` is CORRECT. The builder must NOT re-add `--spec` — only thread it into the reflect gates (skill-side, R2 scope). No command-file edit needed for `--spec`.**

### A.3 — `argument-hint` location for `--no-reflect`

**There is NO `argument-hint` frontmatter key in this command file.** Frontmatter (lines 1-10) contains only: `name`, `description`, `category`, `complexity`, `allowed-tools`, `mcp-servers`, `personas`, `version`. Quoted frontmatter:

```
---                                                                     (L1)
name: tasklist                                                          (L2)
description: "Generate deterministic, Sprint CLI-compatible tasklist bundles from roadmaps with integrated roadmap validation"  (L3)
category: utility                                                       (L4)
complexity: high                                                        (L5)
allowed-tools: Read, Glob, Grep, Write, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Skill   (L6)
mcp-servers: [sequential, context7]                                     (L7)
personas: [analyzer, architect]                                         (L8)
version: "2.0.0"                                                        (L9)
---                                                                     (L10)
```

The **de-facto argument-hint** is the **Usage code block at line 23**:

```
## Usage                                                                (L20)

```                                                                     (L22)
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>]   (L23)
```                                                                     (L24)
```

**ANCHOR for builder:** The proposal (§6, line 284) says add `--no-reflect` to "the skill `argument-hint`" — that is the SKILL.md's frontmatter (R2 scope), NOT this command file, which has no such key. On the COMMAND side, the equivalent surfaces to update are:
1. **Usage code block (line 23)** — append `[--no-reflect]` → `/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]`
2. **Arguments table (after line 38)** — add a new row for `--no-reflect`.

> Caveat: the proposal's literal wording is "skill `argument-hint`". If the builder reads §6 strictly, the `argument-hint`-named field belongs to SKILL.md (R2). This command file has no `argument-hint` field; its analogue is the Usage block. Builder should update BOTH the command's Usage/Arguments AND the skill's `argument-hint` for surface consistency.

### A.4 — "Command does no generation, invokes Skill" (proposal Finding 1) — CONFIRMED

Two quotes confirm the command is a thin parse/validate/dispatch shell:

- **L30** (Behavioral Summary): "The command parses arguments, validates inputs, derives the output directory, and invokes the `sc:tasklist-protocol` skill which contains the full generation algorithm. **The command itself does not execute any generation logic.**"
- **L74-75** (Activation, MANDATORY): "Before executing any protocol steps, invoke: > Skill sc:tasklist-protocol"
- **L83**: "Do NOT attempt to generate the tasklist using only this command file."
- **L115** (Boundaries / Will Not): "Execute the generation algorithm (that is the skill's job)"

**VERDICT: Finding 1 (proposal line 29, citing `commands/tasklist.md:28-31` and `:74-84`) is CORRECT.** Consequence per proposal: all generation-side reflect wiring (Stage 10.5, POST templating) lands in the SKILL, not this command. The ONLY command-file edit in scope is the `--no-reflect` flag (Usage line 23 + Arguments table after line 38).

### A.5 — Exact `--no-reflect` landing in the command

- **Arguments table:** insert a 4th row immediately **after line 38** (the `--output` row), keeping the `| Argument | Required | Default | Description |` shape:
  `| `--no-reflect` | No | off (false) | Escape hatch: skip both reflect gates (pre-reflect sign-off + templated post-reflect task). Set automatically by `--dry-run`. |`
- **Usage hint (line 23):** append `[--no-reflect]` to the bracketed optional-flag list.
- **Optional consistency touch points (not strictly required by proposal but cohesive):** the Boundaries "Will Not" list (lines 113-118) and Examples block (lines 88-100) could note the flag; proposal does not mandate these.

> Default semantics: proposal §6 line 284 = "default off; skips both gates — e.g. for `--dry-run`". So `--no-reflect` is a boolean store-true flag, default `false` (reflect ON). Memory `feedback_dryrun_skips_subskills.md` is the cited justification.

---

## B. `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`

> IMPORTANT STRUCTURAL NOTE: This template file is a **read-only human-review mirror**. Header line 4: "Read-only reference extracted from SKILL.md Section 6B. This file exists for human review; **the skill uses its own inline copy.**" => Editing this template alone changes nothing at generation time; the builder MUST also edit the inline copy in SKILL.md Section 6B (R2 scope). This template should be kept in sync for human reviewers.

### B.1 — Structure dump

**Task heading format (lines 22-24):**
```
### T<PP>.<TT> -- <Task Title>                                          (L23)
```

**Per-task metadata table (lines 26-41)** — 13 fields, this exact shape:
```
| Field | Value |                                                       (L26)
|---|---|                                                               (L27)
| Roadmap Item IDs | `R-###` (comma-separated; must include at least 1) |   (L28)
| Why | <1-2 sentences derived from roadmap> |                          (L29)
| Effort | `<XS|S|M|L|XL>` |                                            (L30)
| Risk | `<Low|Medium|High>` |                                          (L31)
| Risk Drivers | `<matched categories/keywords only>` |                 (L32)
| Tier | `<STRICT|STANDARD|LIGHT|EXEMPT>` |                             (L33)
| Confidence | `[████████--] XX%` |                                     (L34)
| Requires Confirmation | `Yes | No` (Yes if confidence < 0.70) |       (L35)
| Critical Path Override | `Yes | No` |                                 (L36)
| Verification Method | `<method per tier>` |                           (L37)
| MCP Requirements | `<Required: X, Y | Preferred: Z | None>` |         (L38)
| Fallback Allowed | `Yes | No` |                                       (L39)
| Sub-Agent Delegation | `Required | Recommended | None` |              (L40)
| Deliverable IDs | `D-####` (comma-separated; must include at least 1) |   (L41)
```

**Then per-task body sections (lines 43-76):**
- `**Artifacts (Intended Paths):**` (L43-47)
- `**Deliverables:**` 1-5 outputs (L49-51)
- `**Steps:**` numbered, tagged [PLANNING]/[EXECUTION]/[VERIFICATION]/[COMPLETION] (L53-60)
- `**Acceptance Criteria:** (exactly 4 bullets)` (L62-67)
- `**Validation:** (exactly 2 bullets)` (L69-72)
- `**Dependencies:**` / `**Rollback:**` / `**Notes:**` (L74-76)

**Acceptance-criteria specificity rules (lines 78-99):** "Near-Field Completion Criterion" (L78-93) — first AC bullet MUST name a specific verifiable output; rejected forms include "Tests pass." without naming the suite. **Specificity by tier (L95-99):** STRICT = ALL criteria artifact-referencing; STANDARD = >=1; **LIGHT and EXEMPT = no minimum (L99).** => The POST task is EXEMPT, so it is exempt from the artifact-referencing minimum — its ACs (proposal §1b lines 198-201) are fine.

**Inline checkpoints (lines 102-115):** `### Checkpoint: Phase <P> / Tasks <start>-<end>` with Purpose / Checkpoint Report Path / Verification (3 bullets) / Exit Criteria (3 bullets). Deterministic names `CP-P<PP>-T<start>-T<end>.md` and `CP-P<PP>-END.md`.

**End-of-Phase Checkpoint — MANDATORY (lines 117-125):**
```
## End-of-Phase Checkpoint (Mandatory)                                  (L117)

Every phase file MUST end with:                                         (L119)

```                                                                     (L121)
### Checkpoint: End of Phase <N>                                        (L122)
```                                                                     (L123)

This checkpoint serves as the gate for the next phase and must include all standard checkpoint fields.  (L125)
```

### B.2 — Insertion point for the new terminal POST-reflect task

The "checkpoint is last" invariant is asserted here at **lines 119-125** ("Every phase file MUST end with … `### Checkpoint: End of Phase <N>`"). The proposal (Decision C1, §1b) places the POST-reflect task **AFTER** this end-of-phase checkpoint, making it the true terminal task.

**EXACT INSERTION ANCHOR:** add a new subsection **after line 125** (the last content line of the file), titled e.g. `## Terminal Post-Execution Reflection Task (when --no-reflect is off)`, and **amend line 119/125** wording so it no longer claims the checkpoint is the absolute last element. Recommended amended sentence (replacing/augmenting L119 + L125):

> "Every phase file MUST contain an end-of-phase `### Checkpoint: End of Phase <N>` as its last **checkpoint**. When reflect gating is enabled (default), the templated `### T<PP>.<final> -- Post-Execution Reflection` task is the **sole** task permitted to follow that checkpoint and is the absolute last task in the file."

This mirrors the 4-invariant amendment the proposal requires in SKILL.md (check #6 / check #18 / gate #19 / gate #20, proposal line 117, 164, 292) — but in THIS template file the only place to amend is the "Every phase file MUST end with …" claim at L119-125. The builder appends the POST task template block after L125.

### B.3 — Cross-check: POST-task template fields (template requires vs proposal §1b provides)

Proposal §1b POST-task metadata table (lines 169-184) vs the 13-field template table (L28-41):

| Template field (L#) | Proposal §1b value | Status |
|---|---|---|
| Roadmap Item IDs (L28) | "<all R-### in this phase, comma-separated>" (L171) | ✔ provided |
| Why (L29) | "Independent post-execution deviation audit…" (L172) | ✔ provided |
| Effort (L30) | `S` (L173) | ✔ |
| Risk (L31) | `Low` (L174) | ✔ |
| Risk Drivers (L32) | `None` (L175) | ✔ |
| Tier (L33) | `EXEMPT` (* reflect is the auditor *) (L176) | ✔ |
| Confidence (L34) | `[██████████] 100%` (L177) | ✔ |
| Requires Confirmation (L35) | `No` (L178) | ✔ |
| Critical Path Override (L36) | `No` (L179) | ✔ |
| Verification Method (L37) | `Skip verification (reflect IS the verification)` (L180) | ✔ |
| MCP Requirements (L38) | `None` (L182) | ✔ |
| Fallback Allowed (L39) | `Yes` (L181) | ✔ |
| Sub-Agent Delegation (L40) | `Required (fresh-session reflect ensemble)` (L183) | ✔ |
| Deliverable IDs (L41) | `D-RF<PP>` (L184) | ✔ |

**ALL 13 template-required metadata fields are supplied by the proposal. No omissions.**

**Body-section cross-check (template L43-76 vs proposal L186-208):**

| Template section | Proposal §1b | Status / Note |
|---|---|---|
| `**Artifacts (Intended Paths):**` (L43-47) | — | **MISSING in proposal.** Proposal supplies `**Reflect Report Path:**` (L186) + `**Spawn Directive:**` (L188-190) instead. Template's strict "Artifacts (Intended Paths)" block is NOT in proposal. The Reflect Report Path (`TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md`) is the de-facto artifact. **Builder decision needed:** either (a) relax the template to accept Reflect Report Path as the artifact block for this EXEMPT task, or (b) add an `**Artifacts (Intended Paths):**` line pointing at the REPORT.md. Recommend (a) — EXEMPT task, and the report path is already named. |
| `**Deliverables:**` 1-5 (L49-51) | — | **Not explicitly listed** in proposal as a "Deliverables:" bullet block. Deliverable ID `D-RF<PP>` is in the metadata table (L184). Builder may add a one-line Deliverables bullet ("Reflect post-execution REPORT.md for Phase <PP>") to satisfy the template's Deliverables section. |
| `**Steps:**` (L53-60) | `**Steps:** 1-3` (L192-195) | ✔ provided (3 steps, tagged [VERIFICATION]/[VERIFICATION]/[COMPLETION]). Template shows 6 example steps but count is not fixed — 3 is acceptable. |
| `**Acceptance Criteria:** (exactly 4 bullets)` (L62-67) | "(exactly 4 bullets)" (L197-201) | ✔ EXACT match — proposal explicitly provides 4 bullets, matching the template's hard "exactly 4" rule. |
| `**Validation:** (exactly 2 bullets)` (L69-72) | "Manual check" + "Evidence" (L203-205) | ✔ provided (exactly 2). |
| `**Dependencies:**` (L74) | "all regular + checkpoint tasks in Phase <PP>" (L207) | ✔ provided. |
| `**Rollback:**` (L75) | "N/A (reflect is read-only audit…)" (L208) | ✔ provided. |
| `**Notes:**` optional (L76) | — | optional; proposal omits. OK. |

**FIELDS THE TEMPLATE REQUIRES THAT THE PROPOSAL OMITS:**
1. **`**Artifacts (Intended Paths):**`** block (template L43-47) — proposal substitutes `**Reflect Report Path:**`. Builder must reconcile.
2. **`**Deliverables:**` bullet block** (template L49-51) — proposal names `D-RF<PP>` in metadata but provides no standalone Deliverables bullet list.
3. The proposal ADDS two non-template fields the template doesn't have: **`**Reflect Report Path:**`** (L186) and **`**Spawn Directive (fresh session):**`** (L188-190). These are extensions; the builder should ensure the SKILL.md self-check / structural gates don't reject extra `**...:**` blocks on the POST task (R2/R4 to verify the validators).

---

## C. `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md`

> SAME read-only-mirror caveat: header line 4 — "Read-only reference extracted from SKILL.md Section 6A … the skill uses its own inline copy." Builder must also edit SKILL.md Section 6A inline copy (R2 scope).

### C.1 — Structure dump

**Index metadata table (lines 21-32)** — where `Total Phases / Total Tasks / Complexity Class` live:
```
| Field | Value |                                                       (L21)
|---|---|                                                               (L22)
| Sprint Name | ... |                                                   (L23)
| Generator Version | `Roadmap->Tasklist Generator v4.0` |              (L24)
| Generated | `<ISO-8601 date>` |                                       (L25)
| TASKLIST_ROOT | `<computed per Section 3.1>` |                        (L26)
| Total Phases | `<N>` |                                                (L27)
| Total Tasks | `<count>` |                                             (L28)
| Total Deliverables | `<count>` |                                      (L29)
| Complexity Class | `LOW|MEDIUM|HIGH` |                                (L30)
| Primary Persona | `<derived from roadmap domain>` |                   (L31)
| Consulting Personas | `<comma-separated>` |                           (L32)
```

**Artifact Paths table (lines 36-47)** — note **L46**: `| Validation Reports | `TASKLIST_ROOT/validation/` |` already exists (the parent dir the proposal's `reflect-pre/` + `reflect-post/` subdirs nest under).

**Phase Files table (lines 53-57)** — the table that needs the new "Pre-Reflect Sign-off" column:
```
## Phase Files                                                          (L51)

| Phase | File | Phase Name | Task IDs | Tier Distribution |             (L53)
|---|---|---|---|---|                                                   (L54)
| 1 | phase-1-tasklist.md | Foundation | T01.01-T01.04 | STRICT: 1, STANDARD: 2, EXEMPT: 1 |   (L55)
| 2 | phase-2-tasklist.md | Backend Core | T02.01-T02.05 | STRICT: 2, STANDARD: 3 |   (L56)
| ... | ... | ... | ... | ... |                                         (L57)
```
Rules block L59-64. **Current columns: Phase | File | Phase Name | Task IDs | Tier Distribution (5 columns). NO sign-off / validation column exists today** — confirmed by reading the full table; the only validation surface is the `Validation Reports` artifact-path row (L46) and the `## Traceability Matrix` with a `Confidence` column (L96), neither of which is a per-phase sign-off.

Other registries/templates present (for context, not in scope): Source Snapshot (L66-70), Deterministic Rules Applied (L72-76), Roadmap Item Registry (L79-84), Deliverable Registry (L86-90), Traceability Matrix (L92-97), Execution Log Template (L99-106), Checkpoint Report Template (L108-119), Feedback Collection Template (L121-128), Glossary (L130-134), Generation Notes (L136-140).

### C.2 — Insertion points for "Pre-Reflect Sign-off" column + `reflect_pre_summary` metadata

**(i) New Phase Files column (proposal §1a line 159):** add a 6th column to the Phase Files table (L53-57). Amend header (L53), separator (L54), and example rows (L55-57):
```
| Phase | File | Phase Name | Task IDs | Tier Distribution | Pre-Reflect Sign-off |
|---|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Foundation | T01.01-T01.04 | STRICT: 1, STANDARD: 2, EXEMPT: 1 | PASS (depth=quick, coverage=100%) |
```
Cell value format per proposal L159: `reflect_pre: PASS (depth=<d>, coverage=<pct>)` → rendered as `PASS (depth=<d>, coverage=<pct>)` (or `PARTIAL`/`FAIL` + REPORT.md link per L160). Also amend the Rules block (L59-64) to document the new column.

**(ii) New `reflect_pre_summary` metadata (proposal §1a line 161, §6):** add a row to the index **Metadata table** — insert immediately **after line 30** (`Complexity Class`) or after L29 (`Total Deliverables`), keeping the `| Field | Value |` shape:
```
| Reflect Pre Summary | `{pass: <x>, partial: <y>, fail: <z>}` |
```
This is the bundle-level `reflect_pre_summary: {pass: x, partial: y, fail: z}` from proposal L161.

**(iii) No new artifact-path row strictly needed** — `Validation Reports | TASKLIST_ROOT/validation/` (L46) already covers `validation/reflect-pre/` and `validation/reflect-post/`. Optional: add explicit rows for `reflect-pre/` and `reflect-post/` and the `depth-map.yaml` (proposal §4 line 272) for discoverability, but the parent path already resolves them.

### C.3 — Note on `Generator Version`

L24 reads `Roadmap->Tasklist Generator v4.0`. The proposal does not mandate bumping this, but adding reflect gating is a generation-behavior change; builder may consider a version bump (cross-check with R2/SKILL.md which owns the canonical version string). Out of strict R3 scope — flagged only.

---

## Summary — anchor → action per file

| File | Anchor (line) | Action for builder |
|---|---|---|
| **commands/tasklist.md** | `--spec` rows L23/26/**37**/63/93/99 | **NO ACTION** — `--spec` ALREADY EXISTS & is fully wired. Do NOT re-add. Proposal §3 (`:37`) confirmed correct. |
| commands/tasklist.md | Usage code block **L23** | Append `[--no-reflect]` to the optional-flag list. |
| commands/tasklist.md | Arguments table, **after L38** | Add `--no-reflect` row: `No | off (false) | skip both reflect gates; auto-set by --dry-run`. |
| commands/tasklist.md | Frontmatter L1-10 | **No `argument-hint` key exists here.** The proposal's "skill `argument-hint`" (§6 L284) refers to SKILL.md (R2). Command's analogue is the Usage block (above). |
| commands/tasklist.md | L30, L74-75, L83, L115 | Finding 1 CONFIRMED — command does no generation, invokes `Skill sc:tasklist-protocol`. All gate-generation wiring is skill-side (R2). |
| **phase-template.md** | L4 (read-only mirror notice) | Editing this template alone is cosmetic — also edit SKILL.md §6B inline copy (R2). Keep in sync for reviewers. |
| phase-template.md | End-of-Phase Checkpoint **L117-125** | Amend "Every phase file MUST end with … checkpoint" → checkpoint is last *checkpoint*; POST-reflect task may follow as absolute-last task. **Append POST-task template block after L125.** |
| phase-template.md | Metadata table L28-41 + ACs L62-67 | All 13 POST-task metadata fields + the "exactly 4" ACs supplied by proposal §1b. EXEMPT tier ⇒ exempt from artifact-AC minimum (L99). |
| phase-template.md | Body sections L43-51 | **OMISSIONS:** proposal lacks the template's `**Artifacts (Intended Paths):**` (L43-47) and standalone `**Deliverables:**` (L49-51) blocks — substitutes `**Reflect Report Path:**` + `**Spawn Directive:**`. Builder must reconcile (recommend relaxing template for the EXEMPT POST task / accept REPORT.md as the artifact). |
| **index-template.md** | L4 (read-only mirror notice) | Same — also edit SKILL.md §6A inline copy (R2). |
| index-template.md | Phase Files table **L53-57** | Add 6th column "Pre-Reflect Sign-off" (header L53 + sep L54 + rows L55-57 + Rules L59-64). Cell: `PASS\|PARTIAL\|FAIL (depth=<d>, coverage=<pct>)`. |
| index-template.md | Metadata table, **after L30** | Add `| Reflect Pre Summary | {pass: x, partial: y, fail: z} |` row. |
| index-template.md | Artifact Paths **L46** | `Validation Reports | TASKLIST_ROOT/validation/` already covers reflect-pre/reflect-post; explicit rows optional. |

### Critical builder facts
1. **`--spec` already exists** (command L37 + 5 other refs) — proposal's `:37` citation is accurate; builder must NOT re-add it.
2. **No `argument-hint` frontmatter field** in the command file — the Usage block (L23) is its analogue; the `argument-hint` named in proposal §6 belongs to SKILL.md (R2).
3. **Both template files are read-only human-review mirrors** (header L4 each) — the live copies are inline in SKILL.md §6A/§6B (R2 scope). Template edits keep reviewers in sync but do not alter generation.
4. **Proposal omits 2 template-required body blocks** on the POST task (`Artifacts (Intended Paths)`, standalone `Deliverables`) and adds 2 non-template blocks (`Reflect Report Path`, `Spawn Directive`) — reconciliation needed against SKILL.md self-check/structural gates (coordinate with R2/R4).

Status: Complete
