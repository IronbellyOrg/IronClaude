# Research: sc:tasklist Full Audit

**Investigation type:** Code Tracer
**Scope:** sc-tasklist-protocol SKILL.md + rules/ + templates/
**Status:** Complete
**Date:** 2026-03-24

---

## Section 1: Input Contract

### Source: SKILL.md lines 47–57 (`## Input Contract`)

The skill states explicitly:

> "You receive exactly one input: **the roadmap text**."
> "Treat the roadmap as the **only source of truth**."

The roadmap may contain phases, milestones, versions, epics, bullets, paragraphs, requirements, features, risks, success metrics, constraints, and vague items.

### The `--spec` Flag

The skill header at line 9 declares:

```
argument-hint: "<roadmap-path> [--spec <spec-path>] [--output <output-dir>]"
```

This is the **only reference to `--spec`** in the entire SKILL.md. There is no section in the body that defines what `--spec` does, how the spec content is processed, what it enriches, or how it interacts with TASKLIST_ROOT computation. The flag is advertised in the argument-hint but is **completely unimplemented** — no instructions exist for handling it.

The `--output` flag is similarly mentioned in the argument hint but also has no body implementation. TASKLIST_ROOT is computed solely from the roadmap text content (Section 3.1 / lines 65–73), not from any `--output` argument.

### Conclusion: What sc:tasklist Actually Accepts

| Input | Status |
|---|---|
| Roadmap text (primary) | Fully defined and processed |
| `--spec <spec-path>` | Listed in argument-hint; **no implementation defined** |
| `--output <output-dir>` | Listed in argument-hint; **no implementation defined** |

---

## Section 2: Deterministic Generation Algorithm (Steps 4.1–4.11)

### Source: SKILL.md lines 124–265

The algorithm is 11 numbered steps. All are hard rules (no discretionary choices permitted).

### Step 4.1 — Parse Roadmap Items

Split the roadmap top-to-bottom into "roadmap items" at:
- Any markdown heading (`#`, `##`, `###`, ...)
- Any bullet point (`-`, `*`, `+`)
- Any numbered list item (`1.`, `2.`, ...)
- Paragraphs are split at semicolons/sentences **only when** each clause is independently actionable

Each roadmap item gets a deterministic ID: `R-001`, `R-002`, ... in appearance order. These IDs are used in the Traceability Matrix.

### Step 4.2 — Determine Phase Buckets

- If roadmap explicitly labels phases/versions/milestones: treat each such heading as a phase bucket in order of appearance.
- Else: use top-level headings (`##`). If no headings exist, create exactly 3 default buckets: Phase 1 Foundations, Phase 2 Build, Phase 3 Stabilize.

### Step 4.3 — Fix Phase Numbering

Renumber all phases sequentially by appearance order (1, 2, 3, ..., N) with no gaps, regardless of gaps in the source roadmap. The "Missing Phase 8 Rule" means gaps are never preserved.

### Step 4.4 — Convert Roadmap Items into Tasks

Default: 1 task per roadmap item. Split into multiple tasks ONLY if the item contains two or more of:
- A new component/service/module AND a migration
- A feature AND a test strategy
- An API AND a UI
- A build/release pipeline change AND an application change

### Step 4.5 — Task ID, Ordering, and Naming

Task IDs: `T<PP>.<TT>` (zero-padded, 2-digit each). Example: `T01.03`.
Ordering: roadmap top-to-bottom order within each phase. Dependencies may trigger reordering within a phase but never across phases.

### Step 4.6 — Clarification Tasks

When a task cannot be made executable due to missing specifics (target platform, data source, auth model, SLA), or when tier confidence < 0.70, insert a Clarification Task immediately before the blocked task.

Clarification Task title formats:
- `Clarify: <missing detail>` (for missing info)
- `Confirm: <task title> tier classification` (for low-confidence tier)

### Step 4.7 — Acceptance Criteria and Validation

Every task requires:
- **Deliverables:** 1–5 concrete outputs
- **Steps:** 3–8 numbered imperative steps with phase markers: `[PLANNING]`, `[EXECUTION]`, `[VERIFICATION]`, `[COMPLETION]`
- **Acceptance Criteria:** exactly **4** bullets
  1. Functional completion — must name specific, objectively verifiable output (the "Near-Field Completion Criterion")
  2. Quality/safety criterion
  3. Determinism/repeatability criterion
  4. Documentation/traceability criterion
- **Validation:** exactly **2** bullets (verbatim commands from roadmap if present; otherwise deterministic placeholders)

### Step 4.8 — Checkpoints (Exact Cadence)

- After every 5 tasks within a phase: `Checkpoint: Phase <P> / Tasks <start>-<end>`
- At end of every phase: `Checkpoint: End of Phase <P>`

Each checkpoint: Purpose (1 sentence), Verification (exactly 3 bullets), Exit Criteria (exactly 3 bullets).

### Step 4.9 — No Policy Forks + Tier Conflict Resolution

If roadmap implies alternatives, choose deterministically using tie-breakers in priority order:
1. Prefer approach explicitly named in roadmap
2. Else prefer no new external dependencies
3. Else prefer reversible approach
4. Else prefer fewest existing interface changes

Tier conflict priority order: `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)`

### Step 4.10 — Verification Routing

| Tier | Method | Token Budget | Timeout |
|---|---|---|---|
| STRICT | Sub-agent (quality-engineer) | 3–5K | 60s |
| STANDARD | Direct test execution | 300–500 | 30s |
| LIGHT | Quick sanity check | ~100 | 10s |
| EXEMPT | Skip verification | 0 | 0s |

### Step 4.11 — Critical Path Override

Applied when task involves paths matching: `auth/`, `security/`, `crypto/`, `models/`, `migrations/`.
Forces `Critical Path Override: Yes` and always triggers CRITICAL verification regardless of computed tier.

---

## Section 3: Roadmap Sections That Drive Task Generation

### Source: SKILL.md lines 47–57, 124–134, 141–150

The signals sc:tasklist reads from the roadmap to generate tasks:

| Signal | Used For |
|---|---|
| Phase/milestone/version headings | Phase bucket creation (4.2) |
| Top-level `##` headings | Phase buckets if no explicit phases (4.2) |
| All headings at any level (`#`–`###`) | Roadmap item parsing (4.1) |
| Bullet points (`-`, `*`, `+`) | Roadmap item parsing (4.1) |
| Numbered list items | Roadmap item parsing (4.1) |
| Independently actionable sentences/clauses | Roadmap item splitting (4.1) |
| Version tokens (`v<digits>.<digits>`) | TASKLIST_ROOT computation (3.1) |
| Path substring `.dev/releases/current/<segment>/` | TASKLIST_ROOT computation (3.1) |
| Keywords for tier classification | Tier assignment (5.3) |
| Explicit commands/tests | Verbatim Validation fields (4.7) |
| Explicitly defined terms | Glossary inclusion (index template) |
| Any mention of missing specifics | Clarification Task generation (4.6) |

**There is no special handling for any named section of a spec or TDD.** The skill processes the raw text of whatever document it receives as the roadmap. It does not key off section numbers, headings like "§7 Data Models", API tables, component inventories, testing strategies, migration plans, or release criteria as distinct structured inputs. Everything is flattened to bullets/headings and processed uniformly.

---

## Section 4: TASKLIST_ROOT Determination

### Source: SKILL.md lines 64–86

Three-step priority:

1. If roadmap text contains `.dev/releases/current/<segment>/` (first match): `TASKLIST_ROOT = .dev/releases/current/<segment>/`
2. Else if roadmap text contains version token `v<digits>(.<digits>)+` (first match): `TASKLIST_ROOT = .dev/releases/current/<version-token>/`
3. Else: `TASKLIST_ROOT = .dev/releases/current/v0.0-unknown/`

The `--output` flag in the argument hint is not wired to this computation. TASKLIST_ROOT is always derived from roadmap text content.

---

## Section 5: Output File Format

### Source: SKILL.md lines 88–122, 435–723; templates/index-template.md; templates/phase-template.md

### File Count

Exactly **N+1 files** in Stages 1–6 (N = number of phases), plus up to 2 additional validation artifacts (Stages 7–10):
- `tasklist-index.md`
- `phase-1-tasklist.md` through `phase-N-tasklist.md`
- `TASKLIST_ROOT/validation/ValidationReport.md` (always)
- `TASKLIST_ROOT/validation/PatchChecklist.md` (only if drift found)

### Index File Structure (`tasklist-index.md`)

```
# TASKLIST INDEX -- <Roadmap Name or Short Description>

## Metadata & Artifact Paths    ← table with Sprint Name, Generator Version, date, TASKLIST_ROOT, counts, complexity, personas
## Phase Files                  ← table: Phase | File (literal filename) | Phase Name | Task IDs | Tier Distribution
## Source Snapshot              ← 3–6 bullets strictly from roadmap text
## Deterministic Rules Applied  ← 8–12 bullets
## Roadmap Item Registry        ← table: R-### | Phase Bucket | Original Text (≤20 words)
## Deliverable Registry         ← table: D-#### | T<PP>.<TT> | R-### | Deliverable | Tier | Verification | Artifact Paths | Effort | Risk
## Traceability Matrix          ← table: R-### | Task ID(s) | D-#### | Tier | Confidence | Artifact Paths
## Execution Log Template       ← empty table schema
## Checkpoint Report Template   ← template markdown
## Feedback Collection Template ← empty table schema
## Glossary                     ← only if roadmap defines terms
## Generation Notes             ← optional; fallback behaviors activated
```

### Phase File Structure (`phase-N-tasklist.md`)

```
# Phase N -- <Phase Name>     ← level-1 heading, em-dash, ≤50 chars name
<one-paragraph phase goal>

### T<PP>.<TT> -- <Task Title>
| Roadmap Item IDs | R-### |
| Why              | ... |
| Effort           | XS|S|M|L|XL |
| Risk             | Low|Medium|High |
| Risk Drivers     | matched categories only |
| Tier             | STRICT|STANDARD|LIGHT|EXEMPT |
| Confidence       | [████████--] XX% |
| Requires Confirmation | Yes|No |
| Critical Path Override | Yes|No |
| Verification Method | ... |
| MCP Requirements | ... |
| Fallback Allowed | Yes|No |
| Sub-Agent Delegation | Required|Recommended|None |
| Deliverable IDs  | D-#### |

**Artifacts (Intended Paths):** ...
**Deliverables:** 1–5 concrete outputs
**Steps:** 1. [PLANNING] ... 2. [PLANNING] ... 3–6. [EXECUTION] ... 7. [VERIFICATION] ... 8. [COMPLETION] ...
**Acceptance Criteria:** exactly 4 bullets
**Validation:** exactly 2 bullets
**Dependencies:** Task IDs or "None"
**Rollback:** TBD or as stated in roadmap
**Notes:** optional, max 2 lines

### Checkpoint: Phase <P> / Tasks <start>-<end>   ← after every 5 tasks
### Checkpoint: End of Phase <N>                   ← mandatory last section
```

Phase files contain ONLY tasks for that phase. No registries, traceability matrices, or global templates.

---

## Section 6: Tier Classification Rules

### Source: rules/tier-classification.md; SKILL.md lines 336–416

### Priority Order

```
STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)
```

### Compound Phrase Overrides (Checked First, +0.15 confidence boost)

**LIGHT overrides:** "quick fix", "minor change", "fix typo", "small update", "update comment", "refactor comment", "fix spacing", "fix lint", "rename variable"

**STRICT overrides:** "fix security", "add authentication", "update database", "change api", "modify schema"; also any LIGHT modifier + security keyword → STRICT

### Keyword Scoring

| Tier | Keywords | Score Per Match |
|---|---|---|
| STRICT | authentication, security, authorization, password, credential, token, secret, encrypt, permission, session, oauth, jwt, database, migration, schema, model, transaction, query, refactor, remediate, restructure, overhaul, multi-file, system-wide, breaking change, api contract | +0.4 |
| EXEMPT | what, how, why, explain, understand, describe, clarify, explore, investigate, analyze, review, check, show, plan, design, brainstorm, consider, evaluate, commit, push, pull, merge, rebase, status, diff, log | +0.4 |
| LIGHT | typo, spelling, grammar, format, formatting, whitespace, indent, comment, documentation (inline), rename (simple), lint, style, minor, small, quick, trivial, simple, tiny, brief | +0.3 |
| STANDARD | implement, add, create, update, fix, build, modify, change, edit, remove, delete, deprecate | +0.2 |

### Context Boosters

| Signal | Tier | Boost |
|---|---|---|
| Task affects >2 files | STRICT | +0.3 |
| Task affects exactly 1 file | LIGHT | +0.1 |
| Paths contain `auth/`, `security/`, `crypto/` | STRICT | +0.4 |
| Paths contain `docs/`, `*.md` | EXEMPT | +0.5 |
| Paths contain `tests/` | STANDARD | +0.2 |
| Read-only operation | EXEMPT | +0.4 |
| Git operation | EXEMPT | +0.5 |

### Confidence Scoring

1. Base: `max(tier_scores)` capped at 0.95
2. Reduce by 15% if top two tiers are within 0.1 of each other (ambiguity penalty)
3. Boost by 15% if a compound phrase matched
4. Reduce by 30% if no keywords matched (vague input)

Threshold: Confidence < 0.70 → `Requires Confirmation: Yes`

---

## Section 7: File Emission Rules

### Source: rules/file-emission-rules.md; SKILL.md lines 88–121

- Exactly **N+1 files** during generation (Stages 1–6), up to 2 more in validation (Stages 7–10)
- **Naming convention:** `phase-N-tasklist.md` — no mixed aliases
- **Phase heading format:** `# Phase N -- <Name>` (level 1, em-dash, ≤50 chars name) — required for Sprint CLI TUI
- **Index Phase Files table:** must contain literal filenames (e.g., `phase-1-tasklist.md`), not path-prefixed — required for Sprint CLI regex discovery
- **Content boundary:** phase files contain ONLY their phase's tasks; no cross-phase metadata

### Directory Layout

```
TASKLIST_ROOT/
  tasklist-index.md
  phase-1-tasklist.md
  ...
  phase-N-tasklist.md
  artifacts/
  evidence/
  checkpoints/
  validation/
  execution-log.md
  feedback-log.md
```

---

## Section 8: Key Questions Answered

### Q1: Does sc:tasklist accept a --spec flag? If yes, what does it do with spec content?

**Answer:** The `--spec <spec-path>` flag appears in the `argument-hint` field of the SKILL.md frontmatter (line 9) but is **completely unimplemented**. There is no body section, no conditional logic, no instruction block, and no processing rule anywhere in SKILL.md that describes what to do with a spec path or spec content. The flag is effectively declared but dead.

The `--output` flag has the same status: listed in the argument hint, never implemented in the body.

### Q2: Can sc:tasklist accept a TDD directly as its spec input?

**Answer:** Technically, you could pass a TDD document as the "roadmap" argument, since the Input Contract only states "you receive exactly one input: the roadmap text." If the TDD were passed as the roadmap, it would be processed through the same algorithm. However:

- The algorithm parses headings, bullets, and numbered list items uniformly; it has no awareness of TDD section semantics (e.g., it would not treat §7 differently from §1).
- TDD section structures like data model tables, API spec tables, component inventories with new/modified/deleted columns, and migration plans would be processed as generic roadmap items — likely producing noisy or poorly-formed tasks.
- The `--spec` flag that appears to be intended for this purpose is unimplemented.

**In its current state: yes technically, but no in any useful sense.** The output quality would degrade significantly because the parsing algorithm is tuned for roadmap prose and phase/bullet structure, not TDD structured tables.

### Q3: Does sc:tasklist currently use information from these TDD sections?

| TDD Section | Currently Used? | How / Why Not |
|---|---|---|
| **§7 Data Models** | Only via keyword matching | If the roadmap mentions "schema", "migration", "model", "database", those keywords elevate tier to STRICT and risk score. The skill does not parse data model tables, field definitions, or relationship diagrams. No structured extraction. |
| **§8 API Specifications** | Only via keyword matching | Keywords like "api contract", "query", "transaction" boost STRICT. The skill does not read API endpoint tables, HTTP methods, request/response schemas, or versioning. |
| **§10 Component Inventory (new/modified/deleted)** | Not at all | There is no structured handling of component inventories. A component inventory might contribute as generic roadmap items if formatted as bullets, but new/modified/deleted categorization is not used to influence tier, effort, risk, or task splitting. |
| **§15 Testing Strategy** | Only via keyword matching | "tests/" path boosts STANDARD. If a roadmap item mentions a testing strategy, it may split into a feature + test strategy task (per 4.4). But the skill does not parse test suite names, coverage targets, test types, or acceptance gates. |
| **§19 Migration & Rollout Plan** | Partially via keywords + split rule | "migration", "rollback", "deploy" keywords boost STRICT/risk. The split rule (4.4) handles "build/release pipeline change AND application change." But phase sequencing, environment-by-environment rollout steps, feature flags, and canary/blue-green details are not extracted structurally. |
| **§24 Release Criteria** | Not at all | Release criteria (sign-off gates, stakeholder approvals, go/no-go conditions) are not handled. They might appear as Clarification Tasks if the roadmap item lacks specifics, but there is no structural extraction of release gates. |

### How Could sc:tasklist Generate Tasks from These Sections if Upgraded?

**§7 Data Models:** If upgraded, the skill could parse table rows as individual roadmap items (one task per entity/migration), extract field names/types to populate acceptance criteria, and use relationship information to detect cross-component STRICT risk.

**§8 API Specifications:** API endpoint tables could generate one task per endpoint group (or per breaking change), with HTTP method + path populating the "named artifact" in acceptance criteria and auto-assigning STRICT tier for breaking changes.

**§10 Component Inventory:** The new/modified/deleted classification maps directly to task generation rules — new → create task, modified → update task with delta scope, deleted → remove + migration task. This is structurally cleaner than inferring from prose.

**§15 Testing Strategy:** Named test suites could be extracted and wired directly into the Validation field (verbatim command), replacing the generic `Manual check: ...` placeholder. Coverage targets could populate acceptance criteria specificity.

**§19 Migration & Rollout Plan:** Phase-level migration tasks could be auto-generated per environment or rollout segment. Rollback procedures from the TDD could populate the `Rollback:` field directly rather than defaulting to "TBD."

**§24 Release Criteria:** Each release criterion could generate an EXEMPT (review) or STRICT (verification) task at the end of the final phase, with the criterion text populating acceptance criteria.

---

## Section 9: Post-Generation Validation Pipeline (Stages 7–10)

### Source: SKILL.md lines 857–1099

After the initial generation (Stages 1–6), the skill runs four mandatory validation stages:

- **Stage 7:** Spawns 2N parallel agents (2 per phase) to compare each generated task against the source roadmap for drift, contradictions, omissions, weakened criteria, and invented content.
- **Stage 8:** Consolidates agent findings into `ValidationReport.md` and `PatchChecklist.md` in `TASKLIST_ROOT/validation/`. If zero findings, writes a clean report and skips Stages 9–10.
- **Stage 9:** Delegates patch execution to `sc:task-unified --compliance strict` via the `Skill` tool.
- **Stage 10:** Re-reads each flagged task to verify the patch was applied; appends verification results to `ValidationReport.md`. UNRESOLVED findings are logged but do not block completion.

---

## Summary

**Status:** Complete
**Date:** 2026-03-24

### What sc:tasklist Accepts

The skill accepts exactly one input: roadmap text. The `--spec` and `--output` flags listed in the argument hint are **unimplemented** — they appear only in the frontmatter `argument-hint` field and have no corresponding processing logic anywhere in the skill body.

### How Task Generation Works

The algorithm is entirely text-driven: parse headings and bullets into R-### roadmap items, bucket into phases, convert 1:1 to tasks (split only for compound deliverables), enrich each task with deterministic tier/effort/risk/confidence scoring based on keyword matching, and emit a multi-file bundle. No semantic awareness of document structure, section types, or domain-specific tables exists.

### What Roadmap Signals Drive Generation

Phase headings, bullet points, numbered items, version tokens (for TASKLIST_ROOT), keyword matches (for tier/risk), and explicit commands in the roadmap text (for verbatim Validation fields). Nothing else.

---

## Gaps and Questions

1. [Critical] **`--spec` flag is a ghost.** It is declared in the argument-hint but has zero implementation. Any caller passing `--spec` gets silently ignored behavior. This is a meaningful gap if the intent was to allow TDD-enriched task generation.

2. [Important] **`--output` flag is also unimplemented.** TASKLIST_ROOT is always computed from roadmap text, never from a CLI argument. A user who passes `--output` expecting to control output location will be surprised.

3. [Important] **No TDD-section awareness.** The skill has no structured extraction from §7, §8, §10, §15, §19, or §24. All TDD content that could improve task specificity — API specs, data models, component inventories, test suite names, rollout plans, release gates — is either lost or converted to generic bullet-level tasks.

4. [Minor] **Acceptance criteria "non-invention constraint" limits TDD value.** If a TDD were passed as the roadmap, the non-invention rule (no inventing file paths, test commands, or acceptance states not implied by the roadmap) would prevent the skill from using schema details or API endpoint tables to write specific acceptance criteria — because it would "invent" repository paths.

5. [Important] **The `--spec` flag's intended semantics are undefined.** Is it meant to enrich tasks from spec content? Provide metadata? Restrict task scope? Override TASKLIST_ROOT? There is no documentation anywhere in the skill files.

6. [Important] **Validation pipeline (Stages 7–10) validates only against the roadmap.** If a spec/TDD were provided, the validation agents have no instructions to check generated tasks against spec content. The validation loop is roadmap-only.

---

## Key Takeaways

1. **sc:tasklist is a roadmap-to-tasklist transformer, not a spec-to-tasklist transformer.** Its input model, parsing algorithm, and validation pipeline are designed around roadmap structure (phases, bullets, milestones). Passing a TDD as input would work mechanically but produce lower-quality output.

2. **The `--spec` flag is declared intent, not working code.** Someone designed the interface to accept a spec, but never wrote the implementation. This is the most actionable gap for an upgrade.

3. **Keyword-based tier classification is the only TDD-aware signal.** Words like "migration," "schema," "auth," and "api contract" in roadmap text do influence tier and risk scoring — but this is coincidental pattern matching, not semantic TDD integration.

4. **Output quality scales linearly with roadmap quality.** A well-structured roadmap with explicit phase headings, action verbs, and named components produces excellent tasklists. A TDD or spec passed directly would require significant pre-processing or skill upgrades to achieve comparable output quality.

5. **The post-generation validation pipeline is the skill's strongest feature.** The 2N parallel agent validation loop (Stage 7) actively detects drift between generated tasks and source document. This same mechanism could, with modification, validate against a TDD spec in addition to the roadmap.

6. **Specificity constraints work against unstructured TDD input.** The Near-Field Completion Criterion and non-invention rules require every acceptance criteria bullet to name a specific, verifiable output derived from the roadmap. A TDD's structured tables (API schemas, component lists) contain exactly this kind of specificity — but the skill has no mechanism to extract and use it.
