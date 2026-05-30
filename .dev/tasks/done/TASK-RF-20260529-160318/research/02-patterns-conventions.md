# Research 02: Patterns & Conventions

**Status:** Complete
**Researcher:** Researcher 2 of 5
**Task:** TASK-RF-20260529-160318
**Topic:** Structural and stylistic conventions for new diagnosability-audit files

## Sources

- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md` (182 lines) — structural twin of new `refs/diagnosability-audit.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (468 lines) — wave pattern source
- `/config/workspace/IronClaude/CLAUDE.md` — project source-of-truth rules
- `/config/workspace/IronClaude/src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` — MDTM template 02 (status emoji convention)
- `/config/workspace/IronClaude/.dev/brainstorms/20260529-141819-troubleshoot-wave-1-6-diagnosability/merged-output.md` — brainstorm artifact (HTML provenance comments)

---

## Part A — Doc-Discovery.md Deep Structural Extraction

The new `refs/diagnosability-audit.md` MUST mirror the section structure, schema patterns, and code-fence conventions established in `doc-discovery.md`. Below is the load-bearing structural extraction.

### A.1 — Top-of-file framing (lines 1-7)

Pattern: H1 title (3 words or fewer + "Rules"/"Discovery"/etc.), one-line wave anchor, one-paragraph orientation, then `---` separator.

Verbatim from `doc-discovery.md:1-7`:

```markdown
# Documentation Grounding Rules

Wave 1.5 of the sc:troubleshoot protocol. Loaded on demand by Wave 1.5 only.

This ref defines the three parallel discovery branches (A: release-doc, B: architectural-doc with currency validation, C: semantic-restriction), the per-branch structured-output schemas, and the synthesised Documentation Context Card template that Waves 1, 3, 4, and 5 consume.

---
```

**Pattern for diagnosability-audit.md:** open with `# Diagnosability Audit Rules` (or similar), one-line "Wave 1.6 of the sc:troubleshoot protocol. Loaded on demand by Wave 1.6 only." anchor, then a one-paragraph orientation naming the parallel branches and the synthesised artifact the downstream waves consume.

### A.2 — Section heading convention (lines 9, 39, 72, 131)

Pattern: `## Section <N>: <imperative title>` — numbered, colon-separated, title-case-of-subject.

| Source line | Heading |
|---|---|
| `doc-discovery.md:9` | `## Section 1: Auggie query templates per branch` |
| `doc-discovery.md:39` | `## Section 2: Branch B currency-check procedure` |
| `doc-discovery.md:72` | `## Section 3: Structured-output schema per branch` |
| `doc-discovery.md:131` | `## Section 4: Documentation Context Card template` |
| `doc-discovery.md:180` | `## Loading discipline` (terminal, un-numbered) |

Sections are separated by `---` horizontal rules. The terminal `## Loading discipline` section is un-numbered and intentionally short (one paragraph at lines 180-182).

### A.3 — Section 1: Auggie query template format

**Sub-heading pattern:** `### Branch <Letter> — <Imperative phrase>` (e.g., `### Branch A — Release-doc lookup`, line 13).

**Per-branch structure** (3 elements, in this order):

1. One-line `Query target:` declaration naming the path(s) the branch scans. Example (`doc-discovery.md:15`):

   > `Query target: .dev/releases/current/` and `.dev/releases/complete/` for prior release artifacts (PRDs, TDDs, specs) that scope the symptom's component.`

2. A fenced code block (` ``` ` with NO language tag — plain triple-backtick) containing the verbatim Auggie query body. Placeholders are angle-bracketed snake_case: `<issue_description>`, `<scope>`, `<component_paths>`.

3. No trailing prose — the next `### Branch X` sub-heading follows immediately (or the `---` separator at the end of Section 1).

**Verbatim template (Branch A, `doc-discovery.md:17-19`):**

```
In the .dev/releases/ tree (both current/ and complete/), find any PRD, TDD, spec, or roadmap artifact that scopes <component_paths> or names <issue_description>'s subject area. For each hit, return the artifact path, a 2-3 sentence summary of how the artifact constrains the behavior of <component_paths>, and a confidence score (0.0-1.0) reflecting how directly the artifact addresses the symptom.
```

**Placeholder syntax (load-bearing):**

| Placeholder | Source | Filled by |
|---|---|---|
| `<issue_description>` | `doc-discovery.md:11, 18, 26, 34` | Wave 1.5 orchestrator from Wave 0 parsed input |
| `<scope>` | `doc-discovery.md:11, 34` | Wave 1.5 orchestrator (may be unset) |
| `<component_paths>` | `doc-discovery.md:11, 18, 26, 34` | Wave 1.5 orchestrator |

Lead-in paragraph at `doc-discovery.md:11` MUST appear before the first `### Branch A` and MUST name every placeholder used in any branch template. Verbatim:

> Each branch issues ONE `mcp__auggie__codebase-retrieval` call (single message, fan-out via parallel Task spawns from the Wave 1.5 orchestrator). The placeholders `<issue_description>`, `<scope>`, and `<component_paths>` are filled by the Wave 1.5 orchestrator from the parsed Wave 0 input.

### A.4 — Section 2: Currency-check / shell-procedure shape

**Pattern: Step header → fenced shell block → prose rule → next step → final verdict-combination table.**

**Step heading format** (`doc-discovery.md:43, 51`): `### Step <N> — <Mechanism name>`.

**Shell command embedding** uses fenced blocks with NO language tag (plain ` ``` `), one command per block:

`doc-discovery.md:44-46`:

```
stat -c '%Y' <doc_path>
```

`doc-discovery.md:52-54`:

```
grep -E '^(Last reviewed|Status|Owner|Updated):' <doc_path> | head -5
```

The placeholders inside shell blocks use the SAME angle-bracket convention (`<doc_path>` etc.) as the Auggie query templates.

**Prose-rule pattern after each shell block:** one paragraph that explains what to do with the output and emits a `verdict` keyword (lowercase, no backticks around the keyword itself). Example (`doc-discovery.md:49`):

> Compare the returned epoch seconds against the mtime of the most recent file in the directory listed in `<component_paths>` (i.e., the code surface the doc claims to describe). Rule: if `mtime(doc) < mtime(code) - (90 days)`, the doc is at least 3 months staler than the code it describes — emit verdict `stale`.

**Verdict-combination table** (`doc-discovery.md:59-66`) — terminal pattern of Section 2. Header is a `### Verdict combination rule` H3, followed by a markdown table with 3 columns. The verdict values appear in code-formatting backticks within table cells:

```markdown
| Step 1 mtime | Step 2 marker | Verdict |
|---|---|---|
| fresh (< 90 days behind code) | no markers OR "Status: current" / "Last reviewed: < 6 months" | `current` |
| fresh | "Status: deprecated/archived" OR "Last reviewed: > 6 months" | `stale` |
| stale (≥ 90 days behind code) | any | `stale` |
| mtime unobtainable | any | `unknown` |
```

A one-paragraph "downstream semantics" closer follows the table (`doc-discovery.md:68`):

> Both `stale` and `unknown` verdicts surface in the Documentation Context Card with a CAUTION note; only `current`-verdict docs are weighted as authoritative by downstream waves.

### A.5 — Section 3: Per-branch structured-output schema format

**Pattern: ONE output file per branch at `<output-dir>/wave<N>-branch-<Letter>.md`, schemas declared as fenced JSON blocks (` ```json `) with no inline comments.**

Lead-in line (`doc-discovery.md:74`):

> Each branch agent writes ONE structured-output file at `<output-dir>/wave1_5-branch-<A|B|C>.md`. The schemas:

**Schema styles used (the new ref MUST use the same three):**

1. **Single object** (Branch A, `doc-discovery.md:80-87`):

   ```json
   {
     "release_slug": "<slug from .dev/releases/...>",
     "artifact_paths": ["<absolute path 1>", "<absolute path 2>"],
     "summary": "<2-3 sentence summary>",
     "confidence": 0.85
   }
   ```

2. **Sentinel "no hit" object** (Branch A, `doc-discovery.md:91-93`):

   ```json
   { "hit": false }
   ```

3. **Array of objects (zero-or-more)** (Branch B, `doc-discovery.md:99-108`):

   ```json
   [
     {
       "doc_path": "<absolute path>",
       "summary": "<2-3 sentence summary of the documented behavior of <component_paths>, per the Section 1 Branch B query template>",
       "currency_verdict": "current",
       "reason": "<one-line rationale for the currency_verdict, tied to Section 2 procedure>"
     }
   ]
   ```

**Field-value conventions:**

- String fields use angle-bracket placeholder slots: `"<absolute path>"`, `"<2-3 sentence summary>"`.
- Enumerated string fields document the allowed values OUTSIDE the JSON block in a separate prose line. Example (`doc-discovery.md:110`):

  > `currency_verdict` ∈ `{current, stale, unknown}`. Empty array means no relevant docs found.

- Numeric fields use literal example values (e.g., `"confidence": 0.85`, `"file_line": 42`).
- "Empty array means no relevant docs found" is the standard close-line for array-style schemas.
- NO JSON-with-comments. Plain JSON code-fences only.
- Per-schema `### Branch <Letter> schema` sub-headings — the same Branch-letter convention used in Section 1.

### A.6 — Section 4: Context Card template format

**Pattern: a single fenced markdown block (` ```markdown `) containing the complete card skeleton, opened by a one-paragraph orientation that names where it is written and which downstream waves consume it.**

Orientation (`doc-discovery.md:133`):

> After all three branches complete, the Wave 1.5 orchestrator synthesises a single Documentation Context Card at `<output-dir>/doc-context.md`. The card has 4 sections matching the consumption pattern downstream waves expect:

**Card skeleton structure** (`doc-discovery.md:135-176`):

1. H1 title: `# Documentation Context Card`
2. Three frontmatter-style bold-key lines:

   ```markdown
   **Generated**: <ISO 8601 timestamp>
   **Wave**: 1.5
   **Scope**: <scope used by Wave 1.5; or "(none)" if --scope was unset>
   ```

3. One H2 section per consumed branch + a final synthesis H2. The four named sections of `doc-discovery.md` are:
   - `## Release context` (consumes Branch A)
   - `## Architectural docs consulted` (consumes Branch B)
   - `## Restrictions / decisions that constrain the fix` (consumes Branch C)
   - `## Re-frame signals` (synthesis across A+B+C)

4. Each section opens with a one-line "Findings from Branch <X>" attribution, then a `Format:` declaration introducing the bullet template.

5. **Bullet templates use backtick-formatted path tokens and en-dash separators:**

   `doc-discovery.md:155`:

   > `- <doc_path>` — verdict: `<current | stale | unknown>` — <one-line summary derived from the schema `summary` field>

   `doc-discovery.md:165`:

   > `- <source_file>:<file_line>` (<applies_to>) — "<quoted_text>"

6. **Blockquote-CAUTION pattern** for advisory annotations (`doc-discovery.md:159`):

   ```markdown
   > CAUTION: <doc_path> is <stale|unknown> per the Section 2 currency check; treat its claims as advisory, not authoritative.
   ```

7. **Synthesis-section escape clause** (terminal pattern for `## Re-frame signals`, `doc-discovery.md:175`):

   > If no signals reframe the bug-as-stated, write the literal: "No documentation-derived reframing applies — proceed with normal hypothesis generation."

The new `refs/diagnosability-audit.md` Context Card MUST mirror all 7 sub-patterns: H1 + 3 bold-key headers + per-branch H2 + Format declaration + backticked path bullets + blockquote CAUTION + literal-text escape clause for the synthesis section.

### A.7 — Terminal "Loading discipline" section

Always closes with a `## Loading discipline` un-numbered H2 (`doc-discovery.md:180-182`):

> This ref is loaded only by Wave 1.5. Do not pre-load. The three branch agents receive their query templates from Section 1 by quotation in the Wave 1.5 brief; they do NOT load this entire ref. The synthesised Documentation Context Card from Section 4 is the only artifact consumed by downstream waves (Waves 1, 3, 4, 5).

The new ref MUST close with the equivalent: "This ref is loaded only by Wave 1.6. Do not pre-load. ..." naming the branch count and the single downstream-consumed artifact.

---

## Part B — SKILL.md Wave-Structure Pattern Extraction

### B.1 — The 6-section wave template

Every wave in `SKILL.md` follows the same 6-section block. Confirmed from `SKILL.md:152-187` (Wave 1.5), `SKILL.md:129-148` (Wave 1), and `SKILL.md:190-207` (Wave 1.7):

1. **`### Wave <N>: <Title>`** (H3 wave heading, line 152 for Wave 1.5)
2. **`**Goal**: ...`** — one-paragraph mission statement (line 154)
3. **`**Preconditions**: ...`** — what must be true before the wave runs (line 156). May include skip-conditions (e.g., `--no-doc-discovery is NOT set`).
4. **`**Steps**:`** — numbered list (1., 2., 3., ...) where each item names the action + the artifact path it writes (`SKILL.md:158-168`).
5. **`**Exit criteria**:`** — bullet list of "what must exist on disk" checks, terminated by a literal `Emit "Wave <N> complete: <key=value pairs>"` line (`SKILL.md:170-174`).
6. **`**Failure handling**:`** — markdown table with three columns: `Scenario | Behavior | Fallback` (`SKILL.md:178-184`).
7. **`**Token budget**:`** — one-sentence statement of the wave's Claude-token target (`SKILL.md:186`).

The wave block is closed by a `---` horizontal rule before the next `### Wave` heading.

**Exit-criteria emit format (verbatim, `SKILL.md:174`):**

> Emit "Wave 1.5 complete: doc_context_card_path=<output-dir>/doc-context.md".

The new Wave 1.6 MUST emit a parallel line — e.g., `Emit "Wave 1.6 complete: diagnosability_audit_path=<output-dir>/diagnosability-audit.md"`.

**Token-budget statement format (verbatim, `SKILL.md:186`):**

> **Token budget**: Wave 1.5 should consume ≤ 2k Claude tokens (the auggie calls offload heavy retrieval). If it goes over 3k Claude tokens, audit-log the overrun — the wave is meant to be retrieval-offload, not Claude reasoning.

Pattern: a soft ceiling (`≤ Nk`) + a hard-overrun escalation behavior + a one-sentence rationale.

### B.2 — Wave-graph ASCII format

Located in `SKILL.md:75-85`, inside a fenced ```text block. Each wave gets one line: `Wave <N>: <Short Title>  ← <when it runs + which ref it loads>`:

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

Convention observations:

- Decimal wave numbers (`1.5`, `1.7`) are used for new waves inserted between integer waves. Wave 1.6 (the new diagnosability audit) fits this convention naturally between 1.5 and 1.7.
- The `←` arrow introduces the load-condition / ref-load note.
- Conditional waves are marked `(conditional, requires <condition>)`.
- Closing one-liner follows the block (`SKILL.md:87`): "Each wave has explicit entry/exit criteria. Refs are loaded per-wave, never pre-loaded."

### B.3 — Output Contract row format

The Output Contract table sits in `SKILL.md:41-58`. Schema:

```markdown
| Field | Type | Description |
|-------|------|-------------|
| `field_name` | `type_name` | <full English-language description, may include conditional behavior, asymmetric-cost annotations, and back-references to derivation rules> |
```

**Type values observed:**

- `string`
- `int`
- `float`
- `bool`
- `list[path]`
- `string \| null` (pipe-escaped in markdown)

**Description-cell conventions:**

- Bool-flagged asymmetric cost: `| ``test_is_wrong`` | bool | ... Asymmetric-cost flag — downstream automation MUST NOT auto-apply ...` (`SKILL.md:49`)
- Path-typed fields whose null state is meaningful name BOTH the populated meaning and the null meaning (`SKILL.md:50, 52`)
- Repo-relative-vs-absolute discipline is called out explicitly when paths are involved.

For Wave 1.6, the new Output Contract row will need (per task brief context):

| Field | Type | Description |
|---|---|---|
| `diagnosability_audit_path` | `string \| null` | Mirror the `doc_context_card_path` convention from `SKILL.md:52` — repo-relative path, null only on skip-flag, empty-card when wave runs but finds no signals. |

### B.4 — Refs table format

`SKILL.md:459-466`:

```markdown
| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1.7 (calibration) |
| `refs/doc-discovery.md` | Wave 1.5 (documentation grounding — Auggie query templates, currency-check procedure, output schemas, Documentation Context Card template) |
```

Two columns: backticked file path + bullet-style "When loaded" cell that names the wave(s) and (in parens) the artifacts the wave extracts from the ref. The new `refs/diagnosability-audit.md` row MUST follow this pattern.

### B.5 — Tool Coordination matrix

`SKILL.md:391-403`. Row-per-tool, column-per-tier (Tier 1 / Tier 2 / Tier 3). Cell values are `✓` (used), `—` (not used), or `✓ <condition>`. The `mcp__auggie__codebase-retrieval` row (`SKILL.md:393`) is the load-bearing precedent for Wave 1.6 — already includes the `Wave 1.5 doc-grounding fan-out` annotation pattern that Wave 1.6 should extend.

---

## Part C — Project Conventions

### C.1 — Status emoji set (MDTM frontmatter)

Source: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:5` and the F5 protocol at lines 447-451. The canonical 4-emoji set:

| Status | Emoji + label | When set |
|---|---|---|
| To Do | `🟡 To Do` | Initial frontmatter (line 5) |
| Doing | `🟠 Doing` | Upon task start (F5, line 448) |
| Done | `🟢 Done` | Upon completion (F5, line 449) |
| Blocked | `⚪ Blocked` | If blocked (F5, line 450) |

Type/priority emoji are also templated at line 6-7: `type: "📝 Documentation"`, `priority: "🔼 High"`.

**Note on user-stated convention:** The task brief lists "🟡 To Do, 🟢 Done" — the full canonical set extends this with `🟠 Doing` and `⚪ Blocked`. The new MDTM task file MUST use all four emoji forms in the F5 lifecycle order.

### C.2 — Source-of-truth discipline (`src/superclaude/` → `make sync-dev` → `.claude/`)

Source: `CLAUDE.md` "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents" section.

**The rule:**

> `.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev output** of `src/superclaude/`. The ONLY tracked file under `.claude/` is `.claude/settings.json` (project hook + permission registrations, not auto-generated). Upstream regenerates `.claude/` via `superclaude install`; the local copy exists for Claude Code to read during development.

**Forbidden operations:**

- `git add .claude/skills/...`, `.claude/commands/...`, `.claude/agents/...`, `.claude/hooks/...`, `.claude/templates/...`
- `git add -f` on any `.claude/` path
- Suggesting staging `.claude/` mirrors in paste-ready commit commands
- Authoring task-file instructions telling the user to stage `.claude/` paths

**Mechanical gates (layered, both required):**

1. `.gitignore` rule: `.claude/` excluded except `!.claude/settings.json`
2. Pre-commit `verify-sync` local hook fails on src/ ↔ .claude/ divergence

**The `-f` rule (verbatim from `CLAUDE.md`):**

> If `git add` requires `-f` on any `.claude/` path, that `-f` is the violation siren. STOP. Move the change to `src/superclaude/` first, run `make sync-dev`, and stage only the `src/` side.

**Implications for the new files:**

- Both `refs/diagnosability-audit.md` and the SKILL.md Wave 1.6 edit MUST be written under `src/superclaude/skills/sc-troubleshoot-protocol/`, then propagated via `make sync-dev` to `.claude/skills/sc-troubleshoot-protocol/`.
- The MDTM task file MUST instruct the executor to edit `src/`, run `make sync-dev`, and `git add` ONLY the `src/superclaude/` paths.
- The MDTM task MUST NOT contain any `git add .claude/...` instructions.
- After sync, `make verify-sync` MUST pass before commit.

### C.3 — HTML provenance comments (`<!-- Source: Variant N -->`)

Confirmed via grep against `/config/workspace/IronClaude/.dev/brainstorms/20260529-141819-troubleshoot-wave-1-6-diagnosability/merged-output.md`. Examples:

- `merged-output.md:16` — `<!-- Source: Variant 3 (base) with V1 SKILL.md diff fidelity + V4 component-identification step S0.1 -->`
- `merged-output.md:72` — `<!-- Source: Variant 3 (base) — 2-branch fan-out with literal auggie queries and bash fallbacks -->`
- `merged-output.md:557` — `<!-- Source: Variant 1's structured table (better fidelity than V3's prose) + V3's contract fields substituted -->`

**These comments are sc:adversarial brainstorm-artifact metadata** documenting which variant each merged section was sourced from during the adversarial merge. They are NOT a project content convention.

**Rule for the new files:** `<!-- Source: Variant N -->` comments MUST NOT propagate into `SKILL.md` or `refs/diagnosability-audit.md`. The brainstorm provenance lives in `.dev/brainstorms/.../merged-output.md` only; the canonical SKILL.md and ref content is brainstorm-agnostic.

### C.4 — Extended-metadata HTML comment (canonical, DOES propagate)

A different HTML-comment pattern that DOES belong in SKILL.md, for reference (`SKILL.md:7-12`):

```markdown
<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
-->
```

This is intentional pseudo-frontmatter for human readers. Don't confuse it with the brainstorm provenance comments — they live in different files and serve different purposes.

---

## Summary

The new `refs/diagnosability-audit.md` MUST be a structural twin of `doc-discovery.md`: same 4-numbered-section layout (Auggie queries → procedure → schemas → Context Card), same fenced-code conventions (no language tag for shell/Auggie blocks, `json` tag for schema blocks, `markdown` tag for the Card skeleton), same `<placeholder>` angle-bracket convention, same `### Branch <Letter> — ...` sub-headings, same closing `## Loading discipline` paragraph. The new Wave 1.6 in `SKILL.md` MUST mirror Wave 1.5's 6-section block (Goal / Preconditions / Steps / Exit criteria / Failure handling table / Token budget), be wired into the wave-graph ASCII at `SKILL.md:75-85` between 1.5 and 1.7, contribute a row to the Refs table at `SKILL.md:459-466`, and (per task scope) add a `diagnosability_audit_path` field to the Output Contract following the `doc_context_card_path` precedent at `SKILL.md:52`. All edits go to `src/superclaude/` first, then `make sync-dev`, then commit only the `src/` side per `CLAUDE.md`'s ABSOLUTE RULE on `.claude/` staging. The `<!-- Source: Variant N -->` provenance comments from `merged-output.md` MUST NOT propagate. MDTM status lifecycle uses the four-emoji set `🟡 To Do → 🟠 Doing → 🟢 Done` (or `⚪ Blocked`) per template 02 F5.
