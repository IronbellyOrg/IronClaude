# Research: Patterns & Conventions

Status: Complete
Date: 2026-06-02
Track goal: Implement 4 Medium-Complexity Serena Adoptions (FR-RV3-MED.1-4) into
sc-reflect-protocol per `.dev/releases/current/Reflect-V3.5-Serena_Mediums/05-spec-medium-complexity.md`.
Scope: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` + project `CLAUDE.md`.
Focus: EXACT editing patterns each generated task item must follow so output stays
consistent with the live skill.

All file:line evidence is against the live SKILL.md
(`src/superclaude/skills/sc-reflect-protocol/SKILL.md`, 1585 lines total) as read 2026-06-02.

---

## 1. Per-step audit-emit convention (the 5-field row shape)

**Anchor: SKILL.md:124** (the actual line is :124, not the spec's "~:124" — confirmed exact).

Verbatim:

> **Per-step audit emit convention.** Every numbered step within every wave emits one row
> to `<output>/audit.log` with shape: `{wave: <N>, step: <M>, timestamp: <ISO-8601>,
> outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}`. This is the audit-granularity
> unit that resolves the 9-wave vs 7-wave structural disagreement: each step (not each wave)
> is the audit row.

**The exact 5 fields are**: `wave`, `step`, `timestamp`, `outcome`, `evidence_ref`.
**The `outcome` enum is exactly**: `ok | warn | fail | skip`.
**`evidence_ref`** is a single `<path-or-null>` slot — it points at ONE artifact path, not a
structured blob.

**WHY this constrains FR-4 (`execute_shell_command`):** the per-invocation verification data
(`verify_invocations[]` = `[{cmd, exit_code, duration_ms, stdout_path, stderr_path,
blocked_reason, deviation_class}]`) is a variable-length array. It CANNOT be inlined into the
fixed 5-field row because the row has exactly one free-form slot (`evidence_ref`). The
correct, spec-mandated pattern (FR-4.1, spec:230,246 — "resolves M-ARC1") is:

- Write the per-invocation array to a SEPARATE artifact:
  `<output>/verify-logs/invocations.yaml`.
- The step-5.5 audit row sets `evidence_ref: <output>/verify-logs/invocations.yaml`.
- The fixed 5-field schema stays intact.

Every NEW step (4.5, 5.5, 0.7b, Wave-6 handoff) the task adds MUST emit exactly one such row
with these 5 fields and an `outcome` drawn from `ok|warn|fail|skip`. Skip-on-absence cases
(FR-1.4, FR-2.4) use `outcome: skip`. Degrade-on-error cases (FR-1.5) use `outcome: warn` (or
`fail`) with `evidence_ref` pointing at the degrade detail when applicable.

---

## 2. Fail-open policy (§6.5) and the `degraded` token grammar

**Anchor: §6.5 SKILL.md:397-399** (spec said "~:397-399" — exact). Verbatim:

> ### 6.5 Fail-open policy
>
> Every Serena call is fail-open per `sc-validate-roadmap-protocol` convention. Missing Serena
> → fall back to `Grep`/`Glob` with `degraded: true` in the audit. The protocol must never
> abort because Serena is unavailable.

**Two distinct degrade idioms coexist in the skill — the task must match the right one:**

**(a) `degraded: [<tool>]` array form** (per-Serena-call, in the audit / fail-open table). Used
in the §14 degraded-mode table at SKILL.md:1041-1043:

- `degraded: ["auggie"]` (SKILL.md:1041) — auggie unavailable.
- `degraded: ["serena"]` (SKILL.md:1042) — Serena unavailable; ALSO note this row says
  "skip `get_diagnostics_for_file`" — the established precedent for skipping a Serena
  sub-step when the backend is down.
- `degraded: ["context7"]` (SKILL.md:1043) — context7 unavailable in `--depth deep` UC-1.

  This is the form the spec's FR-1.5 (`degraded: ["type_hierarchy:backend_error"]`) and
  FR-4 fail-open (`degraded: ["<tool>"]`, spec:148,259) follow. **Token grammar for the new
  qualified tokens** is `"<tool>:<reason>"` (e.g. `type_hierarchy:backend_error`) — a colon-
  qualified extension of the bare `["serena"]` precedent. The bare-tool form (`["serena"]`,
  `["auggie"]`) is used when the whole tool is missing; the colon-qualified form
  (`type_hierarchy:backend_error`) distinguishes a specific failure mode from plain absence.

**(b) `degraded_components: [<list>]` contract field** (run-level rollup, in the return
contract / telemetry). Distinct from (a). Existing tokens grepped:

- `degraded_components: ["env-aliases"]` (SKILL.md:116, 201, 202, 1036).
- The contract field is declared at SKILL.md:610: `degraded_components: [<list>]   # e.g.
  ["auggie", "evidence-validator", "env-aliases"]` and mirrored in the JSON schema at
  SKILL.md:1347.

**Other `degraded` enum-valued telemetry fields** (value `full | degraded`, NOT array form):
`t2_model_class_diversity` (SKILL.md:203-204,545), `calibrator_diversity` (SKILL.md:548,812,
815,1040), `t2_vendor_diversity: single` (SKILL.md:773). These are diversity-grade fields, not
tool-availability tokens — the task should NOT model new Serena-tool degrades on these.

**Rule for the task:** each NEW Serena call (`type_hierarchy`, `onboarding`,
`prepare_for_new_conversation`, `execute_shell_command`) inherits §6.5. On
missing/error/excluded it emits a `degraded: [<tool>]` (or `[<tool>:<reason>]`) audit entry and
continues — NEVER aborts. The phrase "The protocol must never abort because Serena is
unavailable" (SKILL.md:399) is the load-bearing invariant; every FR's fail-open clause restates
it ("never block", "never a hard STOP").

---

## 3. Telemetry vs contract split (§9.4) and contract_version bump

**Current contract_version value (§9.1):** `contract_version: "1.0"` at **SKILL.md:494**
(quoted verbatim). The heading at SKILL.md:491 reads `### 9.1 Stable contract
(contract_version: 1.0)`. The grader assertion at SKILL.md:1503 pins
`return-contract.yaml contract_version == "1.0"`.

> NOTE / DISCREPANCY the task must reconcile: the live field is the 2-segment string `"1.0"`
> (major.minor), but §9.4 (SKILL.md:640) describes versioning as `"<major>.<minor>"` while its
> examples use 3-segment forms (`1.0.x` patch, `1.x.0` minor). The spec
> (spec:294,325) asks to "bump `contract_version` to `1.1.0`". Bumping `"1.0"` → `"1.1.0"`
> changes the segment count AND would break the SKILL.md:1503 grader assertion
> (`== "1.0"`). The task MUST: (i) update the §9.1 literal at SKILL.md:494, (ii) update the
> §9.1 heading at SKILL.md:491, (iii) update the grader assertion at SKILL.md:1503, and (iv)
> update the JSON-block `skill_version` reference at SKILL.md:1289
> (`"<contract_version from §9.1>"`). Recommend `"1.1"` (matching the live 2-segment style) OR
> `"1.1.0"` per spec — but whichever is chosen MUST be applied consistently across all four
> sites. Flag this as a precision point for the implementer.

**§9.4 evolution policy — verbatim governing rules (SKILL.md:644-646):**

> - **Patch (1.0.x):** typo, comment, or doc-only change in a field's description; no shape
>   change. No consumer action required.
> - **Minor (1.x.0):** purely additive change — new top-level field(s) added, no existing
>   field renamed/removed/retyped, no semantic change to existing fields. Forward-compatible:
>   consumers MUST tolerate unknown top-level fields (read-and-ignore). Consumers that wish to
>   use the new field opt in by reading it explicitly.
> - **Major (X.0.0):** any field rename, removal, retype (e.g., `bool → enum`), or semantic
>   change (e.g., gate condition tightening). Breaking.

**The split rule (load-bearing for which fields trigger a bump):**

- **Stable contract (§9.1, SKILL.md:491-600)** — adding a NEW top-level field here is a MINOR
  bump. FR-1's `hierarchy_slice_path` / `hierarchy_coverage_pct`, FR-3's `handoff_memory_key`,
  and FR-4's `verification_ran` / `verification_invocations` / `verification_failures` /
  `verification_regressions_detected` / `verification_skip_reason` are NEW §9.1 fields →
  they DRIVE the minor bump.
- **Telemetry block (§9.2 "non-stable", SKILL.md:601)** — `### 9.2 Telemetry (non-stable)`.
  Per the spec's §4.5 annotations (spec:339): telemetry fields are "observability,
  NON-contractual (no contract bump per §9.4)". So all `*_invoked`, `hierarchy_backend`,
  `onboarding_*`, `handoff_persist_*`, `verify_timeout_hit`, `verify_flaky_suspected` etc.
  go into §9.2 and add NO version pressure.
- **`regression_present`** is an EXISTING field (SKILL.md:557) — FR-4 only changes its SOURCE
  (verified vs task-log-claimed), not its shape. Per §9.4 a SEMANTIC change to an existing
  field is technically a MAJOR concern; the spec treats it as additive-source (spec:335 marks
  it "EXISTING field … now verified-sourced"). The implementer should keep `regression_present`
  shape-identical (`<bool>`) so it stays inside the minor bump, and document the source change
  in the field comment (patch-grade doc change) rather than retyping it.

**Bottom line for the task:** put FR-1/3/4 contract fields in §9.1 and bump
`contract_version` ONCE (minor) to cover all of them — the spec explicitly co-designs this to
"avoid two consecutive contract minor bumps" (spec:91). Put every telemetry field in §9.2 with
no bump.

---

## 4. Flag declaration pattern (where & how new flags are declared)

**Anchor: flag list at SKILL.md:68-86** (under §3, the input-flag block). The established
one-line declaration shape is:

> `` - `--flagname <arg>` — <description> (see §N) ``

Verbatim precedents (SKILL.md:73-78):

- `` - `--depth quick | standard | deep` — Tier-1-only / Tier-1-then-rubric / force-Tier-2 (see §5) `` (SKILL.md:73)
- `` - `--tier 1 | 2 | auto` — explicit tier pin (overrides rubric); `auto` is default `` (SKILL.md:74)
- `` - `--no-mcp`, `--no-evidence-validator` (debug only; auto-warns), `--remediate` (offer Tier 3) `` (SKILL.md:78)

`--remediate` is declared inline on SKILL.md:78 and then USED at SKILL.md:255 (F3 routing),
702, 716, 730 (remediation triggers), 1110+. `--rerun-tests` is NOT declared in the §3 flag
block — it appears ONLY at SKILL.md:725 inside the §10.4 Regression detection signal
("by re-running tests if `--rerun-tests` set"). This is the flag FR-4 subsumes/deprecates.

**Promotion-gate flags use a nested sub-block** (SKILL.md:80-85) under the bold header
`- **Promotion gate flags (UC-2 only — see §14.5):**`, each child flag with a 2-space indent and
a default annotation, e.g. SKILL.md:81:

> `` - `--no-promote` — suppress Wave 7 promotion. Default is *default-on*: … `` and there is
> also a full per-flag table at SKILL.md:1145 (`| `--no-promote` | unset | … |`) and §3
> expanded semantics referenced via `refs/input-resolution.md` (SKILL.md:87).

**Pattern the 3 NEW flags MUST follow:**

| New flag | FR | Default | Declaration site | Mirror needed |
|----------|----|---------|------------------|---------------|
| `--no-verify` | FR-4 | default-OFF (verification default-ON in UC-2) | add a line in §3 block (near SKILL.md:78, alongside other `--no-*`) | telemetry `verification_skip_reason: … \| --no-verify`; §10.4 edit replacing `--rerun-tests` |
| `--onboard` | FR-2 | default-OFF (opt-in) | add a line in §3 block | gate logic in Wave 0.7b; telemetry `onboarding_skipped_reason` |
| `--with-hierarchy` | FR-1 | default-OFF (opt-in; off on `lsp` backend) | add a line in §3 block | backend-probe gate in Wave 0.5c / step 4.5 |

Notes for the implementer:
- `--no-verify` is a disable-flag for a DEFAULT-ON behavior → model it on `--no-promote`
  (SKILL.md:81): declare it, give it a default annotation, and add a skip_reason token.
- `--onboard` and `--with-hierarchy` are enable-flags for DEFAULT-OFF behavior → model on
  `--remediate` (SKILL.md:78 inline declaration + usage-site gating).
- `--rerun-tests` (SKILL.md:725) is the ONLY pre-existing precedent for a verification flag and
  it lives at the usage site, NOT in §3. FR-4 must (a) declare `--no-verify` in §3 AND (b) edit
  SKILL.md:725 to replace the opt-in `--rerun-tests` clause with default-on verification +
  `--no-verify` opt-out (spec:219,301 — `--rerun-tests` becomes a deprecated alias, NOT
  removed; §4.3 spec:301).

**Skip-reason field grammar (load-bearing for FR-2/FR-4):** the established `*_skip_reason`
shape is an enum-valued string field. Precedent: `promotion_skip_reason: user-flag |
gate-failed | adapter-unresolved | dry-run | null` (SKILL.md:590). FR-4's
`verification_skip_reason: tool-unavailable|read-only-project|--no-verify|null` (spec:334) and
FR-2's `onboarding_skipped_reason: context-excluded|memories-present|null` (spec:347) MUST
follow this exact `<token>|<token>|null` enum form. STOP reasons use `stop_reason:`
(SKILL.md:202) — but note NONE of the 4 FRs ever STOP (all fail-open), so the task must NOT
introduce a `stop_reason` for any new tool.

---

## 5. Frontmatter `allowed-tools` editing

**Anchor: SKILL.md:5** (frontmatter, single line). Current verbatim list:

> `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill,
> mcp__auggie__codebase-retrieval, mcp__serena__find_symbol,
> mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview,
> mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory,
> mcp__serena__write_memory, mcp__serena__list_memories,
> mcp__serena__search_for_pattern, mcp__serena__activate_project,
> mcp__context7__resolve-library-id, mcp__context7__query-docs,
> mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking`

**Existing Serena tools present**: `find_symbol`, `find_referencing_symbols`,
`get_symbols_overview`, `get_diagnostics_for_file`, `read_memory`, `write_memory`,
`list_memories`, `search_for_pattern`, `activate_project`.

**The 4 NEW tools to ADD** (comma-separated, same single-line `mcp__serena__<tool>` prefix
convention):

- `mcp__serena__type_hierarchy` (FR-1)
- `mcp__serena__onboarding` (FR-2)
- `mcp__serena__prepare_for_new_conversation` (FR-3)
- `mcp__serena__execute_shell_command` (FR-4)

Editing pattern: append to the existing comma-separated list on SKILL.md:5. The list is a
single physical line (no wrapping); the task MUST keep it single-line and comma+space
delimited to match the existing style and avoid breaking the YAML frontmatter parse. Per the
spec §4.2 (spec:290): "Frontmatter `allowed-tools`: add `type_hierarchy`, `onboarding`,
`prepare_for_new_conversation`, `execute_shell_command`."

> Cross-check: research track 03 owns refs edits / inline contract; this pattern is ONLY the
> frontmatter line. Track 01 owns the precise body insertion anchors for steps 4.5/5.5/0.7b/
> Wave-6.

---

## 6. `think_about_*` non-load-bearing convention vs the 4 NEW load-bearing tools

**Anchor: §6.4 SKILL.md:385-395** (spec said "~:385-395" — exact). Key verbatim sentence
(SKILL.md:395):

> These are scripted, not optional. Their output is captured to `<output>/serena-checkpoints.log`
> for audit. They are not the reflection — they are a free 200-token nudge layered on top.
> **They are NOT listed in frontmatter `allowed-tools`** (declaring them as protocol surface
> would overweight their role).

So the skill's deliberate convention is: **non-load-bearing scripted checkpoints
(`think_about_collected_information`, `think_about_task_adherence`,
`think_about_whether_you_are_done`) are intentionally EXCLUDED from `allowed-tools`** — their
output is logged to `<output>/serena-checkpoints.log` (SKILL.md:395) but never gates a verdict.

**CONTRAST — the 4 NEW tools ARE load-bearing and SHOULD be in `allowed-tools`:**

- `execute_shell_command` (FR-4) produces the verified exit code that DETERMINISTICALLY sets
  `regression_present` (SKILL.md:557) and blocks the §14.5.2 promotion gate (SKILL.md:1097) —
  it is the load-bearing signal, not a nudge.
- `type_hierarchy` (FR-1) feeds `hierarchy_coverage_pct` into the §5 rubric `S_dev_density`.
- `onboarding` (FR-2) writes calibration-baseline memory consumed by §6.3 hydrate.
- `prepare_for_new_conversation` (FR-3) materializes the handoff blob consumed by Wave 6.

Because all four FEED verdicts/contract fields (unlike `think_about_*`), they belong in
`allowed-tools` (pattern 5). The §6.4 exclusion rationale ("declaring them as protocol surface
would overweight their role") is the INVERSE of the new tools' situation — the new tools' role
SHOULD be weighted as protocol surface. The task must NOT accidentally apply the §6.4
exclusion logic to the 4 new tools.

---

## 7. SoT discipline (CLAUDE.md) — edit src/, never the .claude/ mirror

**Anchors: CLAUDE.md:16-33 and CLAUDE.md:141-154.**

Verbatim (CLAUDE.md:18):

> `.claude/{skills,commands,agents,hooks,templates}/*` is **gitignored sync-dev output** of
> `src/superclaude/`. The ONLY tracked file under `.claude/` is `.claude/settings.json`.

Verbatim (CLAUDE.md:141, §"Component Sync"):

> **Source of truth**: `src/superclaude/` is the canonical location for all distributable
> components (skills, agents, commands, core files).

The `-f` rule (CLAUDE.md:27):

> If `git add` requires `-f` on any `.claude/` path, that `-f` is the violation siren. STOP.
> Move the change to `src/superclaude/` first, run `make sync-dev`, and stage only the `src/`
> side.

**Mandatory editing workflow for EVERY task item (CLAUDE.md:147-149):**

1. Edit ONLY `src/superclaude/skills/sc-reflect-protocol/{SKILL.md, refs/*.md}` — NEVER the
   `.claude/skills/...` mirror.
2. `make sync-dev` (CLAUDE.md:122) — copies `src/superclaude/{skills,agents}` → `.claude/`.
3. `make verify-sync` (CLAUDE.md:123,149) — CI-friendly check that src/ and .claude/ match;
   run before committing. There is a **pre-commit `verify-sync` local hook** (CLAUDE.md:31).

The spec restates this at §4.2 (spec:297): "Per CLAUDE.md SoT discipline: all edits land in
`src/superclaude/` then `make sync-dev`. **No `.claude/` paths are touched directly.**" Every
task item that edits SKILL.md or refs MUST target the `src/` path and end with a sync+verify
step. NEVER `git add .claude/...`; NEVER `git add -f` on a `.claude/` path.

**Markdownlint gate:** SKILL.md begins with `<!-- markdownlint-disable MD013 MD040 -->`
(SKILL.md:8) — MD013 (line-length) and MD040 (fenced-code-language) are disabled for this
file, which is WHY the frontmatter `allowed-tools` line (pattern 5) and long table rows are
allowed to exceed normal line length. The task MUST keep this disable comment intact and may
rely on it for long additive lines, but other markdownlint rules still apply project-wide (the
freshness/markdownlint hooks block edits that violate them — do EXACTLY what a blocking hook
says, never pivot to mdformat/sed/prettier to escape it).

---

## 8. Existing skip-reason / degraded-component precedents for FR-4 `verification_skip_reason`

The exact precedent FR-4's `verification_skip_reason` and FR-2's `onboarding_skipped_reason`
must mirror:

- **Enum-string skip-reason field** — `promotion_skip_reason: user-flag | gate-failed |
  adapter-unresolved | dry-run | null` (SKILL.md:590, also mirrored SKILL.md:1231). Form:
  `<field>: <token>|<token>|...|null`. FR-4 → `verification_skip_reason:
  tool-unavailable|read-only-project|--no-verify|null` (spec:334). FR-2 →
  `onboarding_skipped_reason: context-excluded|memories-present|null` (spec:347).

- **Degraded-mode table rows that SKIP a Serena sub-step** — the canonical "skip a Serena
  step and continue" precedent is SKILL.md:1042: `| Serena unavailable | Fall back to
  Grep/Glob; skip `get_diagnostics_for_file`; mark `degraded: ["serena"]` | Continue |`. This
  is the row FR-4's "tool-unavailable → fall back to `get_diagnostics_for_file` LSP signal
  only" degrade (spec:259) extends. Other rows: SKILL.md:1041 (`degraded: ["auggie"]`),
  SKILL.md:1043 (`degraded: ["context7"]`), SKILL.md:1044 (`--no-mcp` → "Run with native
  tools only; WARN that quality is degraded").

- **`degraded_components` rollup tokens currently in use** (grep `degraded`): only
  `"env-aliases"` appears as a literal token (SKILL.md:116,201,202,1036); the field comment
  lists `["auggie", "evidence-validator", "env-aliases"]` as examples (SKILL.md:610). New
  tool-availability degrades use the per-call `degraded: [<tool>]` audit array (pattern 2a),
  NOT necessarily a new `degraded_components` rollup token — but FR-4/FR-1's
  context-excluded/read-only degrades MAY add a rollup token (e.g. the spec's §4.4 mentions
  "read_only / context-excluded → degraded_components enrichment", spec:310-311). Implementer
  choice; both forms have precedent.

- **§14 fail-row to EXTEND for FR-3 fallback** — SKILL.md:1067: `| Serena `write_memory`
  fails at Wave 5 (disk full, permission denied, serena down) | Continue: report still ships;
  emit `memory_persist_failed: true` in telemetry; emit WARN… | None |`. FR-3.3/3.4
  (spec:205-206,213) extends THIS row to cover the `prepare_for_new_conversation` →
  `write_memory` fallback → `handoff_persist_failed: true` chain. The new tool's fallback uses
  the SAME "Continue: report still ships; emit `<x>_failed: true`; WARN" shape.

- **WARN-not-STOP idiom** — FR-2.3 (context-excluded → WARN "switch context", "never a hard
  STOP", spec:186) and FR-4.7 (read_only → WARN, proceed, spec:254) follow the §6.5 fail-open
  invariant. STOP is reserved ONLY for the irresolvable `--tier 2` + zero-aliases conflict
  (SKILL.md:202,209). NONE of the 4 new tools may STOP — confirmed against every FR's
  fail-open clause.

---

## Cross-cutting line-anchor confirmations (verified, not assumed)

These spec-cited anchors were independently re-Read and confirmed EXACT against the live
SKILL.md on 2026-06-02:

- SKILL.md:124 — per-step audit-emit convention (5-field row). EXACT.
- SKILL.md:397-399 — §6.5 fail-open policy. EXACT.
- SKILL.md:494 — `contract_version: "1.0"` (note: 2-segment `"1.0"`, not `"1.1.0"`). EXACT.
- SKILL.md:491 — §9.1 heading `(contract_version: 1.0)`. EXACT.
- SKILL.md:601 — §9.2 `Telemetry (non-stable)` heading. EXACT.
- SKILL.md:638-646 — §9.4 contract-evolution versioning rules. EXACT.
- SKILL.md:557 — `regression_present: bool` (FR-4 deterministic latch target). EXACT.
- SKILL.md:1097 — §14.5.2 promotion gate condition 4
  (`deviation_count_by_class.regression == 0` blocks promotion). EXACT.
- SKILL.md:725 — `--rerun-tests` opt-in clause in §10.4 (FR-4 replaces this). EXACT.
- SKILL.md:1067 — §14 `write_memory` fail row (FR-3 extends). EXACT.
- SKILL.md:5 — frontmatter `allowed-tools` line. EXACT.
- SKILL.md:8 — `<!-- markdownlint-disable MD013 MD040 -->`. EXACT.
- SKILL.md:385-395 — §6.4 `think_about_*` non-load-bearing convention. EXACT.
- SKILL.md:590 — `promotion_skip_reason` enum (skip-reason precedent). EXACT.
- CLAUDE.md:18,27,31,141,147-149 — SoT discipline + sync/verify gates. EXACT.

**Unverified / flagged for implementer precision:**

- The `contract_version` 2-segment (`"1.0"`) vs spec-requested 3-segment (`"1.1.0"`)
  discrepancy (pattern 3). MUST be reconciled at FOUR sites (SKILL.md:491, 494, 1289, 1503).
- `prepare_for_new_conversation` signature is UNVERIFIED at the tool level (spec OQ-M1,
  spec:199,208) — runtime-probe before parameter-dependent wiring. This is a spec-acknowledged
  open question, not a SKILL.md convention gap.

---

## Summary (for the task-builder)

Eight editing conventions extracted from the live skill, each with exact file:line evidence:

1. **Audit rows are a FIXED 5-field schema** `{wave, step, timestamp, outcome(ok|warn|fail|
   skip), evidence_ref}` (SKILL.md:124). Variable/per-invocation data (FR-4
   `verify_invocations[]`) goes to a separate artifact (`<output>/verify-logs/invocations.yaml`)
   referenced by `evidence_ref` — NEVER inlined.
2. **Fail-open (§6.5, SKILL.md:399)** is absolute: each new Serena call emits `degraded:
   [<tool>]` (bare) or `[<tool>:<reason>]` (colon-qualified, e.g.
   `type_hierarchy:backend_error`) and continues; the run-level rollup is
   `degraded_components` (SKILL.md:610). Never abort.
3. **Telemetry vs contract split (§9.4):** put FR-1/3/4 NEW stable fields in §9.1 + ONE minor
   `contract_version` bump (currently `"1.0"`, SKILL.md:494); put all `*_invoked`/backend/
   reason telemetry in §9.2 (non-stable, no bump). Reconcile the version-string format at all
   4 sites.
4. **Flags:** declare `--no-verify` / `--onboard` / `--with-hierarchy` in the §3 block
   (SKILL.md:68-86), modeling `--no-verify` on `--no-promote` (disable-default-on) and the
   two opt-ins on `--remediate`. `--rerun-tests` (SKILL.md:725) is subsumed/deprecated, not
   removed. Skip-reason fields use the `<tok>|<tok>|null` enum form (SKILL.md:590).
5. **Frontmatter (SKILL.md:5):** append the 4 `mcp__serena__<tool>` names to the single-line
   comma-delimited `allowed-tools` list.
6. **Load-bearing contrast:** unlike `think_about_*` (deliberately EXCLUDED from allowed-tools,
   §6.4 SKILL.md:395), all 4 new tools feed verdicts/contract → they BELONG in allowed-tools.
7. **SoT (CLAUDE.md:18,141,147-149):** edit ONLY `src/superclaude/...`, then `make sync-dev`
   + `make verify-sync`; NEVER touch/stage `.claude/` mirror; keep the markdownlint-disable
   comment (SKILL.md:8). Obey blocking hooks literally.
8. **Skip-reason / fallback precedents:** `verification_skip_reason` / `onboarding_skipped_
   reason` mirror `promotion_skip_reason` (SKILL.md:590); FR-3 fallback extends the §14
   `write_memory`-fail row (SKILL.md:1067) with the "Continue: report ships; emit
   `<x>_failed: true`; WARN" shape; WARN-not-STOP is mandatory for all 4 tools.

Status: Complete
