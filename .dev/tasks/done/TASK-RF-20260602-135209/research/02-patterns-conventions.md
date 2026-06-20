# Research: SKILL.md Patterns & Conventions

Topic type: Patterns & Conventions
Scope: src/superclaude/skills/sc-reflect-protocol/SKILL.md — house style for wave steps, audit emit, fail-open, telemetry, degrade tokens, contract-version policy, S_dev_density references.
Status: Complete
Date: 2026-06-02

File: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1585 lines)

---

## Pattern 1 — §6.1 chain step phrasing (the template for new steps 2a/3b/7/7')

The mandatory evidence-gathering chain is a **fenced plain-text block** (NOT yaml), numbered `1.`–`6.`, with the tool name written as a bare `mcp__serena__X <arg>` token, followed by a **column-aligned `#` inline comment** describing intent. Verbatim, SKILL.md:354-365:

```
### 6.1 Mandatory evidence-gathering chain (Wave 1A)

For every touched file in UC-2, or every spec-referenced module in UC-1:

  1. mcp__serena__activate_project (once, idempotent at Wave 0)
  2. mcp__serena__get_symbols_overview <file>            # structural map
  3. mcp__serena__find_symbol <relevant-symbol>          # symbol body
  4. mcp__serena__find_referencing_symbols <symbol>      # downstream impact
  5. mcp__serena__get_diagnostics_for_file <file>        # LSP-level issues
  6. Re-Read each cited file:line range before quoting    # citation-grounding
```

House-style rules a new step in this chain MUST match:
- Tool token is the **bare fully-qualified MCP name** `mcp__serena__<tool>` (no backticks inside the fence, no parens-with-args except step 1's idempotency note).
- Args are `<angle-bracket-placeholders>` (`<file>`, `<symbol>`, `<relevant-symbol>`).
- Trailing **right-aligned `#` comment** stating the *purpose* in 2-4 words (`# structural map`, `# downstream impact`, `# LSP-level issues`).
- A non-Serena step (Re-Read) is allowed in the same numbered list and uses the same comment style.

The §6.3 memory block (SKILL.md:375-381) is the **command-with-args** variant of the same fence style — note `key=...` / `value=...` kwarg form and the right-aligned `#` Wave annotation:

```
  mcp__serena__read_memory  key=reflect/last-pass-{project-slug}      # Wave 0 hydrate
  mcp__serena__write_memory key=reflect/last-pass-{slug} value=<summary>  # Wave 5 persist
  mcp__serena__list_memories                                          # Wave 0 inventory
```

When a NEW chain/sub-chain references a Serena tool, mirror the bare-token + `<placeholder>` + right-aligned `# purpose` form exactly.

---

## Pattern 2 — CONDITIONAL ("when/if"-gated) step phrasing

There are TWO co-existing conditional-step templates. New FR steps that fire on a predicate (e.g. "when kind ∈ {Interface,...}") should mirror the **§4.1 "Detailed step additions" prose template**, which is the most-evolved gated-step form in the file.

### 2a. The §4.1 detailed-step template (PRIMARY — use this for new gated steps)

Each new step is its own bolded paragraph headed `**Step <N><Letter>.<sub> (<short title>).**` then a `When <predicate>:` clause, then a numbered procedure, then an `Emit <field>: <value>` sentence that names the telemetry written on-run vs on-skip. Verbatim, SKILL.md:233-241:

```
**Step 1B.3 (cross-task interaction-effects scan, UC-2 tasklist-scope only).** When mode is UC-2 AND the tasklist contains ≥3 completed tasks, run the symbol-overlap scan:

1. For each task in the tasklist, derive its touched symbols via `mcp__serena__find_symbol` against the task's diff hunks.
2. Build a symbol-overlap graph: nodes = symbols, edges = "touched by task X and task Y." Cap at top-30 most-touched symbols (heuristic; full enumeration is bounded at 30 to control cost).
3. For each overlap edge, query `mcp__serena__find_referencing_symbols` to determine whether the symbol is genuinely shared or just transiently named the same.
4. For each confirmed interaction, check whether either task description explicitly cites the other (textual match on task ID). If neither cites the other, **flag as a cross-task interaction risk**.
5. Each risk becomes a synthetic invariant probe entry tagged `category: cross_task` (in addition to the existing 6 categories — see §11.2). Severity scales with the symbol's call-site count: HIGH if >5 referencing call sites, MEDIUM if 2-5, LOW if 1.

Emit `interaction_effects_scanned: true` in the contract when this step runs; `interaction_effects_scanned: false` when skipped (tasklist < 3 tasks OR mode == UC-1). This is the differentiating value of end-of-tasklist reflect — single-scope review misses interaction effects, and this is where reflect catches them.
```

Conventions a new gated step MUST match (this is the load-bearing one for FR-LOW steps):
- **Header:** `**Step <id> (<title + scope qualifier>).**` — the scope qualifier in the parens states the gate at a glance (`, UC-2 tasklist-scope only`, `, UC-1`).
- **Predicate sentence:** prose `When <condition> AND <condition>, <do X>:` — uses spelled-out `AND`, `OR`, comparison glyphs `≥` / `<`, and `mode is UC-2` / `mode == UC-1` phrasing.
- **Body:** numbered procedure `1.`–`N.`; inline Serena tool refs are written **in backticks** here (prose context), e.g. `` `mcp__serena__find_symbol` `` — contrast with the bare unbacked tokens inside §6.1's fence.
- **Emit clause:** a closing sentence of the exact form `Emit <field>: <value> ... when this step runs; <field>: <value> when skipped (<skip-condition>).` Always names BOTH the run-value and the skip-value and the skip condition.
- Other §4.x examples to mirror: Step 1B.1 / 1B.2 (SKILL.md:229-231, STOP-gated guards) and Step 5.0 (SKILL.md:251-257, the F1/F2/F3 fallback ladder).

### 2b. The §5.3 / §4 Wave-0 table-row predicate form (when a step's gate is a clean enumerable matrix)

When the gate is a small enumerable set of input values mapping to outcomes, the house style is a Markdown table whose first column is the predicate and last column is the emitted telemetry. Verbatim, the alias-routing rows SKILL.md:201-204:

```
| 0 | (any except `--tier 2`) | T1-only path; WARN "T2 requires ≥1 model class"; degraded | `degraded_components: ["env-aliases"]` |
| 1 | (any) | T1-only path; WARN "T2 requires ≥2 model classes" | `t2_model_class_diversity: degraded` |
```

And the §5.3 first-match decision table (SKILL.md:293-302) uses `| # | Condition | Decision |` with the condition column written as a backticked boolean expression: `` `C ≥ 0.90` AND `S_scope ≤ 5 files` AND `S_domains == 1` ... ``. Use 2b only if an FR's gate is genuinely a closed enumeration; otherwise use 2a.

---

## Pattern 3 — audit.log per-step emit convention (§4 ~:124)

The canonical per-step audit row shape is defined once, in bold prose, SKILL.md:124:

```
**Per-step audit emit convention.** Every numbered step within every wave emits one row to `<output>/audit.log` with shape: `{wave: <N>, step: <M>, timestamp: <ISO-8601>, outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}`. This is the audit-granularity unit that resolves the 9-wave vs 7-wave structural disagreement: each step (not each wave) is the audit row.
```

Field-naming style for audit rows:
- **snake_case keys**, lowercase: `wave`, `step`, `timestamp`, `outcome`, `evidence_ref`.
- Enum values are **pipe-delimited lowercase tokens**: `ok|warn|fail|skip`.
- The row is written as an inline `{...}` object in prose; placeholder values are `<angle-bracket>` (`<N>`, `<M>`, `<ISO-8601>`, `<path-or-null>`).

The "loud-never-silent" rule for new conditional steps' audit emission is stated at SKILL.md:257: `The fallback path is **loud, never silent**: every F-step writes to audit.log; the return contract carries `adversarial_unavailable: true`.` — i.e. a new step that can degrade MUST (a) write an audit row, and (b) set a contract/telemetry flag.

The grader can assert a named checkpoint row exists — SKILL.md:899: `` `checkpoint_logged` — verify `audit.log` includes a row for a named checkpoint ``. So a new step that wants eval coverage should give its audit row a stable, nameable `step` id.

**Convention for new `<tool>_invoked`-style booleans:** the file's existing pattern is `<verb-past>_<noun>: <bool>` written as a CONTRACT field, not embedded in the audit row object — e.g. `interaction_effects_scanned: bool` (SKILL.md:574), `evidence_validator_ran: bool` (SKILL.md:536), `citation_revalidation_at_promotion: bool` (SKILL.md:537). A new "did we call serena tool X" flag should follow `<thing>_<pastverb>: bool` snake_case and live in §9.1/§9.2, with the per-run audit row recording `outcome: ok|skip`.

---

## Pattern 4 — §6.5 fail-open envelope phrasing (the exact template)

The fail-open envelope is one sentence, SKILL.md:397-399:

```
### 6.5 Fail-open policy

Every Serena call is fail-open per `sc-validate-roadmap-protocol` convention. Missing Serena → fall back to `Grep`/`Glob` with `degraded: true` in the audit. The protocol must never abort because Serena is unavailable.
```

The reusable envelope shape is: **`<trigger: missing/error> → fall back to `Grep`/`Glob` with `degraded: ...` in the audit. <never-abort assertion>.`**

Per-MCP instances of the SAME envelope live in the §14 Error Handling Matrix as table rows `| <Scenario> | <Behavior with fallback + degrade mark> | Continue |`. Verbatim, SKILL.md:1041-1043:

```
| Auggie unavailable | Fall back to Grep/Glob in Wave 1A; mark `degraded: ["auggie"]` | Continue |
| Serena unavailable | Fall back to Grep/Glob; skip `get_diagnostics_for_file`; mark `degraded: ["serena"]` | Continue |
| Context7 unavailable in `--depth deep` UC-1 | Skip best-practice external lookup; mark `degraded: ["context7"]` | Continue |
```

Note the Serena row already encodes "skip the unsupported sub-call" semantics (`skip `get_diagnostics_for_file``) — a new Serena tool step that has a no-fallback sub-call should append it to this skip-list phrasing. Other fail-open rows to mirror in tone (SKILL.md:795, 1027, 1028): `Validator subprocess crash → fall back to inline citation re-Read, mark `evidence_validator_ran: false`, force `status: partial`.`

**Template for a new Serena tool's fail-open clause:** `<tool> unavailable/errors → fall back to `Grep`/`Glob`; [skip <dependent-sub-step>]; mark `degraded: ["serena:<token>"]`; continue (never abort).`

---

## Pattern 5 — degraded token format (TWO co-existing styles — pick correctly)

The file uses TWO distinct degrade-token surfaces; a new step must write to BOTH the right one:

1. **Audit-row inline mark `degraded: [...]` or `degraded: true`** — used in §6.5 and the §14 matrix. Plain mcp-name string elements, no colon-suffix: `degraded: true` (SKILL.md:399), `degraded: ["auggie"]` / `degraded: ["serena"]` / `degraded: ["context7"]` (SKILL.md:1041-1043). This is the lightweight audit-side mark.

2. **Telemetry list `degraded_components: [<list>]`** — the §9.2 contract field. Verbatim, SKILL.md:610:

```
degraded_components: [<list>]   # e.g. ["auggie", "evidence-validator", "env-aliases"]
```

   Element tokens here are **hyphenated component slugs** (`"env-aliases"`, `"evidence-validator"`) NOT colon-namespaced. Existing concrete emission: `degraded_components: ["env-aliases"]` (SKILL.md:116, 201-202, 1036).

**Finding on `serena:context-excluded`-style sub-tokens:** there is **NO existing colon-namespaced degrade token in the file** (no `["serena:..."]` instance exists). Every current token is either a bare mcp slug (`"serena"`, `"auggie"`) or a hyphenated component slug (`"env-aliases"`). The other axis-of-state convention the file DOES use is a **separate `*_diversity: full | degraded` enum field** rather than a sub-namespaced list element — e.g. `t2_model_class_diversity: degraded` (SKILL.md:203-204, 545), `calibrator_diversity: degraded` (SKILL.md:548, 812). RECOMMENDATION for builder: if an FR needs to distinguish *which* serena capability degraded, prefer either (a) a dedicated boolean/enum field in §9.2 (matching `*_diversity` precedent) or (b) extend `degraded_components` with a hyphenated slug like `"serena-context"` — do NOT introduce colon namespacing, as it has no precedent and would break the existing token grammar.

---

## Pattern 6 — telemetry field naming/casing (§9.2)

§9.2 is a fenced ```yaml block. Verbatim, SKILL.md:603-618:

```yaml
wave_durations_ms: { wave_0: <ms>, wave_1: <ms>, wave_2: <ms>, ... }
token_usage: { wave_0: <est>, ... }
reviewer_models: [<list>]
reviewer_personas: [<list>]
reviewer_vendors: [<list>]
serena_checkpoints_path: <path>
degraded_components: [<list>]   # e.g. ["auggie", "evidence-validator", "env-aliases"]
fallback_path: null | F1 | F2 | F3
executor_class_source: flag | env | log-heuristic | unknown
executor_class_resolved: bool                                  # false → §7.1 anti-self-confirmation WARN emitted
executor_exclusion_degraded: bool                              # true when executor class collision dropped reviewer count below N=2 → T1 fallback
citations_dropped_extrapolated: <int>   # sampled-mode telemetry (recording, not deciding) — see §11.5
memory_hits: <int>                       # serena read_memory hits in Wave 0
memory_misses: <int>
```

Casing/naming conventions for new telemetry fields (these are the rules FR-added fields must match):
- **All keys are `snake_case`**, lowercase. No camelCase, no kebab.
- **Booleans:** `<thing>: bool` (the literal token `bool`, not `true|false`) — e.g. `executor_class_resolved: bool`, `executor_exclusion_degraded: bool`. Past-participle/state phrasing: `_resolved`, `_degraded`, `_ran`, `_scanned`.
- **Counts:** `<noun>: <int>` with literal placeholder `<int>` — e.g. `memory_hits: <int>`, `memory_misses: <int>`, `citations_dropped_extrapolated: <int>`.
- **Paths:** `<noun>_path: <path>` suffix — e.g. `serena_checkpoints_path: <path>`. (In §9.1 the stable form is `<noun>_path: <abs path>`, SKILL.md:498-499.)
- **Lists:** `<plural-noun>: [<list>]` — e.g. `reviewer_models: [<list>]`, `degraded_components: [<list>]`.
- **Enums:** `<noun>: <a> | <b> | <c>` pipe-separated bare tokens — e.g. `executor_class_source: flag | env | log-heuristic | unknown`, `fallback_path: null | F1 | F2 | F3`.
- **Inline `#` comment** explaining trigger/semantics, often citing the governing § — e.g. `# false → §7.1 anti-self-confirmation WARN emitted`. Right-aligned where a cluster of fields shares column alignment.
- A serena-specific telemetry field already exists as precedent: `memory_hits` / `memory_misses` with comment `# serena read_memory hits in Wave 0` (SKILL.md:616-617). New serena-call telemetry should mirror this `<capability>_hits`/`<capability>_misses` or `<capability>_invoked: bool` style.

The §9.1 stable contract (SKILL.md:494-597) uses the same yaml conventions PLUS section-grouping `# Comment` banners (e.g. `# UC-1 specific`, `# Hallucination guard`, `# Tier 2 artifacts`, SKILL.md:503/529/539). A new stable field should be placed under the matching banner group, not appended at the end.

---

## Pattern 7 — contract-version evolution policy (§9.4)

§9.4 (SKILL.md:638-661) describes additive minor bumps as **"purely additive"**. Verbatim, SKILL.md:642-646:

```
**Versioning rule.**

- **Patch (1.0.x):** typo, comment, or doc-only change in a field's description; no shape change. No consumer action required.
- **Minor (1.x.0):** purely additive change — new top-level field(s) added, no existing field renamed/removed/retyped, no semantic change to existing fields. Forward-compatible: consumers MUST tolerate unknown top-level fields (read-and-ignore). Consumers that wish to use the new field opt in by reading it explicitly.
- **Major (X.0.0):** any field rename, removal, retype (e.g., `bool → enum`), or semantic change (e.g., gate condition tightening). Breaking. All consumers in the §9.3 map MUST update before producing-side ships.
```

Implication for the 8 FR-LOW telemetry additions: **adding new top-level telemetry/contract fields is a MINOR bump** (`1.0 → 1.1`). The builder must:
- Bump `contract_version: "1.0"` (SKILL.md:494) to `"1.1"` and update the §9.1 header `### 9.1 Stable contract (contract_version: 1.0)` (SKILL.md:491) + closing line `Contract version is `v1.0`.` (SKILL.md:599).
- NOT rename/retype any existing field (that would force a major bump + §9.3 consumer migration).
- The §9.3 field-deletion guard (SKILL.md:636) confirms: `Additions are minor-version bumps.`
- Deprecation/migration machinery (SKILL.md:648-661) only applies to removals — additive FR work does not trigger the `deprecated_fields` telemetry or the one-minor-cycle migration window.

---

## Pattern 8 — `S_dev_density` rubric-signal reference style

`S_dev_density` is the rubric signal FR-1/6/7 sub-terms must reference. House style for referencing it:

- **Definition site (§5.2 rubric inputs, bulleted list), SKILL.md:287:** `` - `S_dev_density` — for UC-2 only: ratio of unmapped diff hunks to total hunks; for UC-1: ratio of unmapped spec requirements to total requirements `` — i.e. backticked token, em-dash, then a `for UC-2 ... ; for UC-1 ...` dual-mode definition. New sub-terms should extend this same bullet or sit as sibling `S_*` bullets (`S_scope`, `S_domains` at SKILL.md:285-286 are the naming precedent: `S_<lowercase_noun>`, PascalCase-free, backticked).
- **Used in decision logic (§5.3 table)** as a backticked threshold expression: `` `S_dev_density ≤ 0.05` `` (SKILL.md:295), `` `S_dev_density ≤ 0.10` `` (SKILL.md:296), `` `S_dev_density > 0.20` `` (SKILL.md:299).
- **Rationale prose (§5.5), SKILL.md:329:** `` - `S_dev_density > 0.20` is the "structural ambiguity" trigger — at one in five unmapped artifacts... `` — threshold restated, then plain-English meaning.
- **Recorded in audit yaml (§5.6 escalation log), SKILL.md:343:** `  S_dev_density: 0.07` — bare key (NO backticks inside yaml), snake-with-leading-cap `S_` prefix preserved, float value.
- **Influenced by a step (§6.4 checkpoint table), SKILL.md:391:** `...if model surfaces a gap, log it and influence rubric `S_dev_density` upward` — the phrasing for "this step nudges the signal" is `influence rubric `S_dev_density` <up/down>ward`.
- **Computation owner is a ref file (§16 ref map), SKILL.md:1394:** `` | `refs/coverage-mapping.md` | Wave 1B (UC-1) | ... `S_dev_density` calculation | `` — so the actual sub-term math lives in `refs/coverage-mapping.md`, and SKILL.md only references the signal. FR-1/6/7 that ADD sub-terms to `S_dev_density` should (a) add a backticked mention at the §5.2 definition bullet and (b) point the calculation detail at `refs/coverage-mapping.md` (R3's scope), keeping SKILL.md reference-only.

---

## Summary (for the builder)

1. **§6.1 chain steps** = fenced plain-text, bare `mcp__serena__X <placeholder>` tokens, right-aligned `# 2-4-word purpose` comment. New steps 2a/3b/7/7' go in the fence in this exact form.
2. **Conditional steps** = §4.1 `**Step <id> (<title + scope qualifier>).**` + `When <predicate>:` + numbered body (backticked tool refs in prose) + closing `Emit <field>: <run-val> ... ; <field>: <skip-val> when skipped (<cond>).` Use the §5.3/Wave-0 table form only for closed enumerable gates.
3. **Audit emit** = `{wave, step, timestamp, outcome: ok|warn|fail|skip, evidence_ref}` snake_case; new step gets a nameable `step` id for grader `checkpoint_logged`; degrade-capable steps are "loud, never silent" (audit row + contract flag).
4. **Fail-open envelope** = `Missing/error → fall back to `Grep`/`Glob` with `degraded: ...` in the audit. The protocol must never abort.` + a §14 matrix row `| <scenario> | <fallback + mark `degraded: [...]`> | Continue |`.
5. **Degrade tokens** = two surfaces: audit `degraded: ["serena"]` (bare slug) and telemetry `degraded_components: ["env-aliases"]` (hyphenated slug). NO colon-namespacing exists; for capability granularity prefer a `*_diversity: full | degraded` enum field or a hyphenated slug, never `serena:context-excluded`.
6. **Telemetry §9.2** = snake_case keys; `bool` / `<int>` / `[<list>]` / pipe-enum / `<noun>_path` value placeholders; inline `#` comment citing governing §; serena precedent = `memory_hits`/`memory_misses`.
7. **Version policy §9.4** = adding fields is a MINOR bump (1.0 → 1.1); bump `contract_version`, the §9.1 header, and the §599 closing line; never rename/retype (that's major + consumer migration).
8. **`S_dev_density`** = backticked token in prose/tables, bare key in yaml, `S_<noun>` naming; SKILL.md references the signal only — sub-term math belongs in `refs/coverage-mapping.md`. Extend the §5.2 definition bullet for new sub-terms.

Status: Complete
