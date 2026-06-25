# Research: Skill Conventions

**Status:** Complete
**Date:** 2026-06-19
**Researcher:** R02 (Patterns & Conventions)
**Scope:** HOW an implementer must author the five RFMerger (P1–P5) edits so they read like the surrounding generator.

All citations are `path:line` relative to the worktree root
`/config/workspace/IronClaude/.claude/worktrees/RFMerger-Tasklist/`. Primary file:
`src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1631 lines).

---

## 0. House terms / anchor map (quick reference for implementers)

| Convention | Where it lives | Line |
|---|---|---|
| Skill title + version banner | SKILL.md | `:12` (`# Tasklist Generator Protocol (Deterministic, Value-Preserving) v4.0`) |
| Determinism objective ("same input -> same output") | SKILL.md | `:35` |
| Tier scoring algorithm (P5/P1 must NOT mutate) | SKILL.md | `:544-648` |
| Emitted task markdown template | SKILL.md | `:871-957` |
| Emitted checkpoint markdown template | SKILL.md | `:958-1097` |
| "Do not invent repository file paths" (P1 guard) | SKILL.md | `:1107` |
| 20-check pre-write quality gate (P4 serialization target) | SKILL.md | `:1132-1187` |
| Stage Completion Reporting Contract + verdict format | SKILL.md | `:1525-1603` |
| Section-level numbering style (`### 5.3.1`, `#### 5.3.2`) | SKILL.md | `:550-614` |
| Stage-level numbering style (`### Stage 7:`) | SKILL.md | `:1244, :1312, :1409, :1429, :1460` |
| Tier algorithm read-only mirror | rules/tier-classification.md | whole file |
| Emission shape read-only mirror | rules/file-emission-rules.md | whole file |

---

## 1. How a "Stage" / "Section" is structured in SKILL.md

There are TWO heading conventions in play; an implementer must pick by where the
edit attaches:

**(a) Numbered behavioral SECTIONS** (`### 5.3`, `#### 5.3.1`) — used for the
deterministic enrichment rules (Effort/Risk/Tier/Confidence). The house pattern,
seen at SKILL.md:544-614, is:

1. A `### N.M <Name> (mandatory, deterministic)` heading. The parenthetical
   `(mandatory, deterministic)` tag is a recurring house signature — it appears on
   §5.1 (`:446`), §5.2 (`:493`), §5.3 (`:544`), §5.4 (`:616`), §5.5 (`:631`).
2. A one-sentence purpose line, often "Each task must include a **X** computed
   deterministically..." (SKILL.md:546).
3. Sub-sections `#### N.M.K` each opening with a short imperative directive, then
   a bullet list of literal scoring rules with inline `code` tokens and explicit
   numeric weights, e.g. `**STRICT keywords (+0.4 each match):**` (SKILL.md:572).

**(b) Numbered pipeline STAGES** (`### Stage 7: <Name> (...)`) — used for the
post-generation validation pipeline. Pattern at SKILL.md:1244-1460:

1. `### Stage N: <Name> (<short qualifier>)` heading (e.g. `### Stage 7: Roadmap
   Validation (2N Parallel Agents)`, `:1244`).
2. `**Purpose**:` line (SKILL.md:1246).
3. `**<Step name> (deterministic)**:` blocks with numbered algorithm steps
   (SKILL.md:1248).
4. Blockquote `>` for instructions handed to a spawned agent (SKILL.md:1267-1286).
5. A `**Stage gate**:` line stating the structural pass condition (SKILL.md:1310).

**Determinism-algorithm prose style** (applies to both): rules are written as pure
mappings — `Start X = 0` → additive `+N` clauses keyed on literal keyword/path
substrings → a final `Map score -> label` table. See the Risk algorithm at
SKILL.md:523-538 as the cleanest worked example:

```text
Compute `RISK_SCORE`:
- Start `RISK_SCORE = 0`
- ...
  - `+2` if text contains any of: `security`, `vulnerability`, ...
Map score -> label:
- `0-1` -> `Low`
- `2-3` -> `Medium`
- `4+` -> `High`
```

> Implementer note: P1 (Execution Context block) and P5 (Tier Calibration
> Advisory) should each be authored as a numbered behavioral SECTION in the
> §5.x family if they enrich per-task emission, OR as a `#### <Name>` sub-block
> under the existing Output Templates section if they only add emitted markdown.
> R01/R04 own the exact attachment point; R02's contract is the *form*: a
> `(mandatory, deterministic)`-tagged heading + purpose line + pure-function rule
> list, never discretionary prose.

---

## 2. DETERMINISM convention (critical for P1 + P5)

**Canonical phrasing.** The skill's contract word is "deterministic" and the
canonical full phrasing is the Objective bullet:

> `- **Deterministic:** same input -> same output.` (SKILL.md:35)

The opening mandate reinforces it: "transform a roadmap into a **deterministic,
execution-ready task list** with **no discretionary choices**" (SKILL.md:14), and
the Decision-free objective: "no 'choose A or B'; you pick one policy and apply it
uniformly" (SKILL.md:36-37). When a roadmap implies alternatives, the skill
chooses deterministically (SKILL.md:400) rather than asking.

**Scored tiers are a PURE FUNCTION of the roadmap text.** The tier is computed,
never chosen:

- "Each task must include a **Compliance Tier** computed deterministically using
  the `/sc:task` classification algorithm." (SKILL.md:546)
- Priority order is fixed: `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)`
  (SKILL.md:548; mirrored rules/tier-classification.md:9-11).
- Inputs are ONLY: compound-phrase overrides checked first (SKILL.md:550-566),
  additive keyword weights (SKILL.md:568-595), and context boosters from file
  count / path patterns / operation type (SKILL.md:596-614). Confidence is then a
  pure function of `max(tier_scores)` with fixed ambiguity/compound/vague
  adjustments (SKILL.md:620-625).
- The read-only mirror `rules/tier-classification.md` exists "for human review;
  the skill uses its own inline copy" (rules/tier-classification.md:3) — i.e. the
  authoritative algorithm is the SKILL.md inline copy at :544-614. An implementer
  editing tier behavior must edit BOTH the inline copy AND the mirror, or neither.

**P5 hard constraint (advisory MUST NOT mutate scored tiers).** Because the Tier
is defined as `computed deterministically` (SKILL.md:546) and the Style Rules
forbid discretionary additions (SKILL.md:1104 "no 'nice to have' unless the
roadmap states it"), P5's "Tier Calibration Advisory" must be authored as a
*read-only annotation layer* — it reports/suggests but the emitted `Tier` field in
the task table (SKILL.md:884) is still produced solely by the §5.3 algorithm. The
existing precedent for an advisory-but-non-mutating layer is the Pre-Reflect
gate: PARTIAL/FAIL verdicts are recorded and the bundle "**still ships**
(audit-first)" and reflect "NEVER auto-mutates the phase file" (SKILL.md:1477).
P5 should phrase its non-mutation guarantee the same way.

**P1 hard constraint (block must be deterministic).** Any `## Execution Context`
block P1 adds must be derivable purely from roadmap text + the already-computed
deterministic metadata (Tier/Effort/Risk/Traceability) — no new inference. The
worked-example to imitate is Stage 10.5's depth resolution: "`--depth`/`--tier`
per phase is computed deterministically from signals the generator already
produces (Tier Distribution, Critical Path Override, Risk, task count,
Traceability Matrix) — **no inference**" (SKILL.md:1487).

---

## 3. Markdown EMISSION shapes (so P1's `## Execution Context` + P5's `## Tier Calibration Advisory` match house style)

The generator specifies *exact emitted markdown* by quoting the literal heading
token in backticks, then defining its sub-structure. Two house patterns:

**(a) Section-heading-as-literal pattern.** For index sections, the skill writes
the literal heading on its own line in backticks, then the rule list. Example
(SKILL.md:782-793, Execution Log Template):

```text
#### Execution Log Template

`## Execution Log Template`

This is a template to be filled during execution (do not fabricate entries).

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

Table schema:

| Timestamp (ISO 8601) | Task ID | Tier | ... |
|---|---:|---|---|

Rules:
- If no command is provided in the roadmap, set `Validation Run` to `Manual`.
```

> So P1 should emit its block as `## Execution Context` (literal, backtick-quoted
> in the spec) and P5 as `## Tier Calibration Advisory`, each followed by a
> `**Intended Path:**` (if it lands in a file) or a clear "lives in the index /
> phase file" boundary statement, then an explicit rule list.

**(b) Field-table pattern** (for anything attached to a task). The emitted task is
a `### T<PP>.<TT> -- <Title>` heading followed by a two-column `| Field | Value |`
metadata table, then bolded `**Section:**` blocks with fixed bullet counts. The
authoritative emitted-task example is SKILL.md:875-927:

```text
### T<PP>.<TT> -- <Task Title>

| Field | Value |
|---|---|
| Roadmap Item IDs | `R-###` (comma-separated; must include at least 1) |
| Effort | `<XS|S|M|L|XL>` (per Section 5.2.1) |
| Risk | `<Low|Medium|High>` (per Section 5.2.2) |
| Tier | `<STRICT|STANDARD|LIGHT|EXEMPT>` (per Section 5.3) |
| Confidence | `[████████--] XX%` (per Section 5.4) |
| Verification Method | `<method per tier>` (per Section 4.10) |
...

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-####/spec.md`

**Steps:**
1. **[PLANNING]** Load context and identify scope
...

**Acceptance Criteria:** (exactly 4 bullets)
```

House conventions an implementer MUST preserve in any new emitted block:

- Fixed bullet counts are stated in the heading parenthetical, e.g.
  `**Acceptance Criteria:** (exactly 4 bullets)` (SKILL.md:913),
  `**Validation:** (exactly 2 bullets)` (SKILL.md:920),
  `**Verification:** (exactly 3 bullets)` (SKILL.md:988).
- Every field value carries a `(per Section N.M)` back-reference (SKILL.md:881-892).
- Confidence is rendered as a visual bar `[████████--] XX%` (SKILL.md:885, 1108).
- Placeholder paths only — `TASKLIST_ROOT/...` patterns, never invented repo paths
  (SKILL.md:894-898, 1107).
- Em-dash `--` separator in task/phase headings (SKILL.md:875, 864).

> P1 `## Execution Context`: if it renders per-task it must slot into THIS table or
> sit as a bolded `**Execution Context:**` block among the `**Steps:**`/`**Artifacts:**`
> blocks, with a stated fixed structure. If per-phase, mirror the
> section-heading-as-literal pattern (3a).

---

## 4. "Generator works on roadmap TEXT, not a live codebase" (P1 must NOT invent per-step file paths)

This principle is stated emphatically and in multiple places — P1 authoring is
gated by it:

- Input contract: "You receive exactly one input: **the roadmap text**." and
  "Treat the roadmap as the **only source of truth**." (SKILL.md:49, 57).
- Non-Leakage Rule 1: "**No file/system access claims.** You must not claim to have
  read, searched, opened, or modified any files... unless their contents are
  explicitly included in the user-provided input." (SKILL.md:22).
- Non-Leakage Rule 2: "**No invented context.** Do not invent existing code,
  architecture, libraries... not stated in the roadmap." (SKILL.md:23).
- Artifact-path discipline: "You must not claim these paths exist; they are
  **intended locations**." (SKILL.md:89) and the Style Rule "Do not invent
  repository file paths; only use the deterministic artifact paths defined in
  Section 3 and Section 5.1." (SKILL.md:1107).
- Non-invention completion constraint: "Do not invent test commands, file paths,
  or acceptance states not implied by the roadmap." (SKILL.md:944-945).

> P1 consequence: an `## Execution Context` block may reference ONLY
> `TASKLIST_ROOT/...` intended paths and roadmap-derived names. It must NOT emit
> per-step real repo paths (e.g. `src/foo/bar.py`) unless that literal string is in
> the roadmap text. The block must phrase context as "intended"/"derived from
> roadmap", echoing SKILL.md:89.

---

## 5. The 20-check pre-write quality gate (P4 `gate-results.txt` serialization must match)

The gate is at SKILL.md:1132-1187. It is NOT a flat list of 20 — it is three named
sub-gates, numbered contiguously 1-20:

| Sub-gate | Heading | Check #s | Form |
|---|---|---|---|
| Sprint-Compatibility | `## Sprint Compatibility Self-Check (Pre-Write, Mandatory)` (`:1132`) | 1-8 | numbered prose list |
| Semantic Quality | `### Semantic Quality Gate (Pre-Write, Mandatory)` (`:1147`) | 9-12 | numbered prose list (+ generation-discipline checkboxes `:1162-1166`) |
| Structural Quality | `### Structural Quality Gate (Pre-Write, Mandatory)` (`:1174`) | 13-20 | `\| # \| Check \| Rationale \|` TABLE |

Key structural facts an implementer/P4 serializer must honor:

- The opening contract line: "All checks in this section MUST pass before any
  `Write()` call. Invalid output is never written." (SKILL.md:1134).
- Checks 1-12 are authored as `N. <prose>` numbered items; checks 13-20 are TABLE
  rows `| 13 | Task count bounds: ... | Prevents empty phases ... |`
  (SKILL.md:1176-1185), each row being `| # | Check | Rationale |`.
- The closing aggregate verdict line: "If any check 1-20 fails, fix it before
  writing any output file." (SKILL.md:1187).
- Note the internal naming drift to watch: the Stage Completion contract says
  "Self-Check: all 17 checks passed" (SKILL.md:1597) — historical count; the live
  gate is 1-20. P4 should serialize the 20-check reality, not the stale "17".

**GATE verdict-line format (what P4's `gate-results.txt` should mirror).** The
skill has no single literal `GATE: PASS` token, but the established verdict shapes
P4 must imitate are:

- Per-stage structural pass/fail: stages report "the failed criterion" and the
  binary advance/block decision — "**Structural gates** (blocking)... the skill
  reports the failed criterion and attempts correction before advancing."
  (SKILL.md:1545).
- The canonical machine-parseable verdict token in this skill is the reflect-gate
  line: `PASS|PARTIAL|FAIL (depth=<d>, coverage=<pct>)` (SKILL.md:725, also
  `reflect_pre: PASS (depth=<d>, coverage=<pct>)` at SKILL.md:1477). This
  `<VERDICT> (key=val, key=val)` shape is the house verdict grammar — P4's
  gate-results lines should follow `<CHECK-ID>: PASS|FAIL (reason=...)` to match.
- Per-stage completion strings use a fixed `<Stage>: <summary with counts>` shape,
  e.g. Stage 8: "Patch Plan: ... X high / Y medium / Z low issues" and Stage 10:
  "Spot-Check: X/Y findings verified resolved" (SKILL.md:1599, 1601). A
  `gate-results.txt` summary line should adopt the same `N/M`/`X high / Y med /
  Z low` counting idiom.

> P4 serialization recommendation (form only; R03/R05 own the contract): emit one
> line per check in `<sub-gate>/<check-#>: PASS|FAIL` order 1→20, then an aggregate
> `GATE: PASS (20/20)` / `GATE: FAIL (k failing: ...)` line echoing the
> `<VERDICT> (key=val)` grammar at SKILL.md:725.

---

## 6. Source-of-truth + sync + UV + lint conventions (mechanical authoring discipline)

These are NOT in SKILL.md; they are the repo-level editing rules every edit to the
generator must obey. Cited from `CLAUDE.md` (worktree-tracked project instructions):

- **UV only.** "This project uses **UV** for all Python operations. Never use
  `python -m`, `pip install`, or `python script.py` directly." (CLAUDE.md:7). Tests
  for any P1-P5 Python changes run via `uv run pytest` (CLAUDE.md:65).
- **Source of truth = `src/superclaude/`.** Edit the skill at
  `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (and its `rules/`,
  `templates/`) — NEVER `.claude/`. `.claude/{skills,commands,agents,hooks,
  templates}/*` is "gitignored sync-dev output of `src/superclaude/`"
  (CLAUDE.md:18).
- **Sync workflow:** edit `src/` → `make sync-dev` (copies → `.claude/`,
  CLAUDE.md:122, 148) → `make verify-sync` ("Check src/ and .claude/ are in sync";
  "also run before committing" — CLAUDE.md:123, 149). A pre-commit `verify-sync`
  local hook enforces this (CLAUDE.md:31).
- **Never stage `.claude/` mirrors.** ABSOLUTE RULE at CLAUDE.md:16-31: never
  `git add .claude/skills/...`; if `git add` needs `-f` on a `.claude/` path,
  "that `-f` is the violation siren. STOP. Move the change to `src/superclaude/`
  first, run `make sync-dev`, and stage only the `src/` side." (CLAUDE.md:27). Only
  `.claude/settings.json` is tracked.
- **Ruff lint + format-check** (from global SuperClaude rules + memory
  `reference_make_lint_vs_ci_ruff_format`): `make lint` runs only `ruff check`; CI
  separately runs `ruff format --check src/ tests/`. For any Python touched by
  P1-P5, run `uv run ruff format --check src/ tests/` before pushing — green
  `make lint` ≠ green CI format.

> Note: `src/superclaude/core/RULES.md` did not contain literal `sync-dev` /
> `verify-sync` / `ruff` tokens (grep at :1-260 returned no hits) — the
> sync/UV/lint discipline is authoritative in `CLAUDE.md`, not RULES.md.
> **Unverified** that RULES.md restates these; treat CLAUDE.md as the source.

---

## 7. Summary — the R02 authoring contract for P1–P5

1. **Headings:** numbered behavioral SECTION (`### N.M (mandatory, deterministic)`
   + purpose line + pure-function rule list) for enrichment edits; numbered
   pipeline STAGE (`### Stage N: (...)` + `**Purpose**` + `**Stage gate**`) for
   pipeline edits. (§1)
2. **Determinism:** phrase as "same input -> same output"; scored Tier stays a pure
   function of roadmap text (SKILL.md:546). P5 advisory = read-only annotation,
   non-mutating (imitate the audit-first reflect gate, SKILL.md:1477); P1 block
   derives only from already-computed deterministic metadata (no inference,
   SKILL.md:1487). (§2)
3. **Emission:** literal backtick-quoted heading token (`## Execution Context`,
   `## Tier Calibration Advisory`) + fixed-count bulleted sub-blocks +
   `(per Section N.M)` back-refs + `[████████--] XX%` bars + `TASKLIST_ROOT/...`
   placeholder paths only. (§3)
4. **No live codebase:** roadmap text is the only input; "intended locations" never
   "exists"; no invented repo file paths in P1 steps. (§4)
5. **20-check gate:** three sub-gates (Sprint-Compat 1-8 prose, Semantic 9-12
   prose, Structural 13-20 table); P4 gate-results should serialize 1→20 + an
   aggregate `GATE: PASS|FAIL (n/20)` line in the `<VERDICT> (key=val)` grammar
   (SKILL.md:725). (§5)
6. **Mechanics:** edit `src/superclaude/` → `make sync-dev` → `make verify-sync`;
   never stage `.claude/{skills,...}`; UV-only `uv run pytest`; run
   `uv run ruff format --check src/ tests/` before push. (§6)

**Caveats / Unverified:** RULES.md does not restate sync/UV/lint (CLAUDE.md is
authoritative). The Stage-contract "17 checks" string (SKILL.md:1597) is stale vs
the live 20-check gate — flagged for the implementer to reconcile, not silently
copy.
