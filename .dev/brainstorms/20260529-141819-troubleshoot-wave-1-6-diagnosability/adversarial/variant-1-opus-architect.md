# Variant 1 — Architect Perspective

## Design Position

Wave 1.6 should be a **structural twin of Wave 1.5**: same 3-branch parallel `Task` fan-out, same lazy-loaded ref, same single synthesised "Context Card" artifact (the `Diagnosability Audit Card` parallel to the Documentation Context Card), same opt-out symmetry (`--no-diagnosability-audit` mirroring `--no-doc-discovery`), same `doc_context_card_path`-style nullable pointer in the Output Contract. The complexity gate **reuses the existing escalation-rubric dimensions** read from Wave 0/Wave 1 signals — we do NOT add a second classification surface. The Wave 1.6 hard-stop is implemented as a new terminal exit edge that jumps directly to Wave 5 (synthesis + report) with `tier_reached=1`, `status=halted_diagnosability`, mirroring the existing Wave 2 STOP-jump-to-Wave-5 pattern. This minimises the wave-graph delta to one new node and one new STOP edge, keeps every downstream consumer working without changes, and re-uses every adjacent abstraction already in the protocol.

## Wave 1.6 Placement & Entry/Exit Criteria

**Position in graph** (delta to SKILL.md:75-85):

```text
Wave 0 → 1 → 1.5 → 1.6 → 1.7 → 2 → 3 → 4 → 5 → 6
                     │
                     └── (hard_stop_diagnosability) ──→ 5 (synthesis with diagnosability_halted)
```

**Preconditions**:

- Wave 1 (real-code grounding) complete; observation captured at `<output-dir>/tier1-observation.md`.
- Wave 1.5 complete; `doc_context_card_path` is either a real path or `null` (the latter when `--no-doc-discovery`).
- `--no-diagnosability-audit` is NOT set. When it IS set: skip the wave entirely, emit `diagnosability_verdict: skipped`, `diagnosability_audit_card_path: null`, surface a Grounding Gaps line in Wave 5, and proceed to Wave 1.7. **Symmetric with Wave 1.5's `--no-doc-discovery` handling.**

**Steps** (5-step structure mirroring Wave 1.5):

1. **Load `refs/diagnosability-audit.md`** — lazy load (per SKILL.md:90 "Refs are loaded per-wave, never pre-loaded"). Read Section 1 (auggie/serena query templates for the 3 branches), Section 2 (per-branch schemas), Section 3 (sufficiency rubric), Section 4 (complexity gate signal extraction), Section 5 (Diagnosability Audit Card template).
2. **Spawn three audit branches in parallel** via `Task` (single message with three Task calls):
   - **Branch D — Logger-call audit** (analogous to Wave 1.5 Branch A): inventory logger/print/exception-handler calls within and adjacent to the symptom site identified by Wave 1.
   - **Branch E — Log-config audit** (analogous to Wave 1.5 Branch B): inspect log-config files (`logging.yaml`, `logging.conf`, `pyproject.toml [tool.logging]`, Sentry/structlog init, log-level config) to determine if existing instrumentation, if present, would reach an output sink at runtime.
   - **Branch F — Symptom-coverage audit** (analogous to Wave 1.5 Branch C): cross-reference the symptom's "when/where/why" against what the existing logging would have captured. This is the *inverse* of the symptom: if the logging had fired, would it have answered the user's question?
3. **Wait for all three branches**. Read each output file.
4. **Synthesise the Diagnosability Audit Card** at `<output-dir>/diagnosability-audit.md` using the Section 5 template. The card has 4 fixed sections: `Existing instrumentation inventory` (Branch D), `Reachability at runtime` (Branch E), `Symptom-coverage gap` (Branch F), and `Verdict + complexity classification` (synthesis applying Section 3 rubric + Section 4 complexity gate).
5. **Apply the complexity gate** (Section 4) using **already-extracted signals** from Wave 0's parsed type/scope/keywords and Wave 1's grounding observations — *no new auggie call*. Decide `verdict × complexity` branch:
   - `insufficient` AND non-trivial → **hard-stop**: emit `diagnosability-tasklist.md`, set `diagnosability_verdict: insufficient`, `diagnosability_complexity: non-trivial`, set output-contract pointer, **jump to Wave 5** with a special synthesis mode.
   - `insufficient` AND trivial → soft-warn: emit the tasklist (for the user's optional follow-up), continue to Wave 1.7.
   - `partial` / `sufficient` / `unknown` → continue to Wave 1.7 normally; surface findings in REPORT.md's Diagnosability Context section.

**Exit criteria** (mirroring SKILL.md:170-174):

- Three branch outputs written at `<output-dir>/wave1_6-branch-<D|E|F>.md`.
- One synthesised Diagnosability Audit Card at `<output-dir>/diagnosability-audit.md` with all 4 sections populated.
- If the gate fired hard-stop, `<output-dir>/diagnosability-tasklist.md` is also written.
- Emit `Wave 1.6 complete: verdict=<verdict> complexity=<complexity> hard_stop=<bool>`.

**Token budget**: ≤ 2.5k Claude tokens (between Wave 1.5's 2k and Wave 1.7's 3k targets, reflecting one extra synthesis dimension — verdict + complexity). Bulk auggie offload is enforced by the lazy-loaded query templates.

## Audit Mechanics

Each branch issues ONE auggie call (mirroring Wave 1.5's discipline) plus, when needed, narrow serena symbol lookups. Native `Read`/`Grep`/`Glob` fallback when MCPs are unavailable, with `degraded: true` marked in the branch output (mirroring SKILL.md:181).

| Branch | Query target | Auggie/serena call | Emits |
|--------|--------------|--------------------|-------|
| **D — Logger-call audit** | Symptom site (from Wave 1) + 50-line window around it; the file containing the failing test or stack-trace bottom frame | `mcp__auggie__codebase-retrieval` query: "Find every logger call, `print` statement, `try/except` block with logging, and exception-handler body within `<symptom_site>` and its immediate callers (1 frame up). For each, return file:line, log level, fields logged, whether the handler re-raises or swallows." | Branch D schema: array of `{ file_line, kind: logger\|print\|except\|structured, level, fields, scope }` |
| **E — Log-config audit** | Repo-root + standard config dirs | `Glob` for `logging.{yaml,conf,json,toml}`, `log4j2.xml`, `pyproject.toml`, sentry/structlog initializers; `Grep` for `logging.basicConfig`, `logging.getLogger`, `logger.setLevel`, `structlog.configure`, `Sentry.init` | Branch E schema: array of `{ config_path, framework, root_level, handler_kinds, sinks, captures_unhandled, captures_uncaught_in_scope }` plus a `reachability_verdict: reaches_sink \| filtered_out \| unknown` for the Branch D inventory |
| **F — Symptom-coverage audit** | Branch D output + Wave 0 issue description + Wave 1 observation (passed in the brief; no new auggie call) | Pure synthesis — no MCP call. Cross-references the 3 W's of the symptom ("when did it happen? where in code? why this state?") against Branch D's instrumentation inventory + Branch E's reachability verdict | Branch F schema: object `{ when_answerable, where_answerable, why_answerable, coverage_score, narrative }` where each `*_answerable` is `yes \| partial \| no` |

Branch F's "no new MCP call" property is load-bearing for the token budget: it's pure Claude synthesis against the two on-disk branch outputs, costing ~300-500 tokens.

**Defer to devops variant**: log-framework-specific recognizer patterns (e.g., distinguishing Loguru from std logging from structlog, recognizing Sentry vs Datadog vs raygun-style init, handling Java `log4j2.xml` filter rules) — the architect variant fixes the *shape* (3 branches, named schemas, single synthesised card), not the per-framework recognition catalogue.

## Sufficiency Rubric

Synthesis applies a **two-step rubric** on the synthesised Diagnosability Audit Card:

**Step 1 — Per-branch primary signal** (Branch D inventory density + Branch E reachability + Branch F coverage answers):

| Branch D inventory near symptom site | Branch E reachability | Branch F coverage (when/where/why) | Verdict |
|--------------------------------------|----------------------|------------------------------------|---------|
| Rich (≥3 structured logger calls with fields covering symptom state) | `reaches_sink` | all 3 W's `yes` | `sufficient` |
| Rich | `reaches_sink` | 2 of 3 W's `yes` | `sufficient` |
| Moderate (1-2 structured calls OR ≥3 unstructured prints) | `reaches_sink` | 2-3 W's `yes` | `partial` |
| Moderate | `filtered_out` (e.g. level=WARNING but only INFO logs around symptom) | any | `partial` |
| Sparse (0 structured, ≤2 prints, no exception-handler context) | any | ≤1 W `yes` | `insufficient` |
| Any | `unknown` (config missing or unparseable) AND Branch D `degraded: true` | any | `unknown` |
| Symptom IS the stack trace itself (Python uncaught → traceback already self-documenting) | n/a | when/where = `yes` from trace | `sufficient` *(short-circuit — see worked example 1)* |

**Step 2 — Short-circuit overrides**:

- **Stack-trace-self-documents short-circuit**: if Wave 1's observation is a complete Python traceback / Node stack trace AND the symptom is a deterministic exception, override to `sufficient` regardless of inventory density. The trace IS the log. (Addresses Open Question #7 without coupling to cause-class.)
- **Intermittent-with-no-trace short-circuit**: if Wave 0 type ∈ {`test`, `performance`, `deployment`} AND Wave 0 issue text contains `intermittent | flaky | sometimes | randomly | only in prod | only in CI` AND Branch F coverage `when_answerable != yes`, override to `insufficient`. The bug definitionally requires a runtime trace to triangulate.

**Worked Example 1 — Deterministic NameError, no nearby logger.exception**:

- Branch D: 0 structured logger calls, no exception handler. *Sparse.*
- Branch E: reachability `unknown` (no log config). But Branch D `degraded: false` (we found the file just fine).
- Branch F: `when_answerable: yes` (stack trace gives line + commit), `where: yes`, `why: yes` (NameError is self-explanatory).
- Stack-trace-self-documents short-circuit fires → `sufficient`. *Continues to Wave 1.7.*

**Worked Example 2 — Intermittent race condition, only `print('entered foo')` at function entry**:

- Branch D: 1 unstructured print, no structured logging, no exception handler. *Sparse.*
- Branch E: `reaches_sink` (stdout captured by CI).
- Branch F: `when_answerable: no` (print has no timestamp/thread-id), `where: partial`, `why: no` (no state snapshot).
- Step 1 rubric → `insufficient`. Intermittent-with-no-trace short-circuit confirms → `insufficient`.
- Complexity gate → non-trivial → **hard-stop**.

## Complexity Gate

**Firm position on Open Question #1: option (a) — reuse the existing escalation-rubric dimensions**, not (b) new score and definitely not (c) defer to Wave 1.7 (which is downstream and would break the hard-stop's "skip 1.7-5" cleanliness).

**Justification (architect grounds)**:

1. **One source of truth for complexity.** Adding a second classification surface (option b) means future tuning splits across two rubrics that will drift. Option (a) makes Wave 1.6 a *consumer* of the same complexity signals Wave 2 consumes.
2. **The rubric's signals are already available without a hypothesis pass.** The relevant escalation-rubric dimensions are extractable from Wave 0 (`--type`, parsed scope, intermittent keywords) and Wave 1 (grounding observations, stack-trace clarity, scope-file-count) **without** running `root-cause-analyst`. We re-use the *signal extraction*, not the post-hypothesis confidence calibration.
3. **No circular dependency risk.** Wave 2's *confidence-driven* escalation requires Wave 1.7's hypothesis. Wave 1.6's *complexity gate* only needs the rubric's **structural** dimensions: multi-domain, intermittent, scope file count, security_caution, `claim_class` heuristic (derivable from Wave 0 type + Wave 1 trace classification).

**Concrete signal table** (extracted at Wave 1.6 entry, no new agent spawn):

| Signal | Source | Trivial value | Non-trivial value |
|--------|--------|---------------|-------------------|
| `--type` (Wave 0) | parsed flags | `bug`, `build` | `performance`, `deployment`, `security`, `test` (intermittent) |
| Scope-file count (Wave 1) | grounding result | 1 file | >1 file or undetermined |
| Intermittent keywords (Wave 0) | issue text grep | absent | present (`intermittent`, `flaky`, `sometimes`, `only in CI/prod`, `randomly`) |
| Stack-trace clarity (Wave 1) | observation file | complete trace with file:line bottom frame | no trace OR trace bottoms in compiled/closed-source code |
| Reproduces in Tier 1 (Wave 1) | observation file | `repro_attempted: true` AND `repro_succeeded: true` | repro skipped or failed |
| Security flag (Wave 0) | `--type security` | n/a | always non-trivial |

**Gate rule**: classified `non-trivial` if **any 2 of 6** signals score non-trivial, OR `--type security` is set (security is always non-trivial — asymmetric cost), OR intermittent keywords are present (the rubric's existing `intermittent` escalation reason at `refs/escalation-rubric.md:66` already names this signal as load-bearing).

**Defensive note** ("if I'm wrong it's because..."): if reuse turns out to be too coupled (e.g., a future rubric tuning changes Wave 2 behavior in ways that misclassify Wave 1.6), the migration path is to extract these signals into a shared `refs/complexity-signals.md` consumed by both — but that refactor is *cheaper* than maintaining two parallel rubrics from day 1.

## Output Contract Additions

Three new fields, all additive, all backwards-compatible (every existing field is unchanged; downstream consumers that don't read the new fields keep working — explicit statement matching SKILL.md's existing approach to `doc_context_card_path`):

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `diagnosability_verdict` | string | `null` | One of `sufficient`, `partial`, `insufficient`, `unknown`, `skipped` (when `--no-diagnosability-audit`). `null` only if Wave 1.6 was not reached (e.g., Wave 0 STOP). |
| `diagnosability_audit_card_path` | string \| null | `null` | **Repo-relative** path to `<output-dir>/diagnosability-audit.md`. `null` ONLY when `--no-diagnosability-audit` was set OR Wave 1.6 was not reached. When the wave runs but finds no instrumentation at all, the card is still emitted with "None found" sections, mirroring the Wave 1.5 doc-context-card pattern at SKILL.md:182. |
| `diagnosability_tasklist_path` | string \| null | `null` | **Repo-relative** path to `<output-dir>/diagnosability-tasklist.md`. Populated when verdict ∈ {`insufficient`, `partial`} AND tasklist was emitted (hard-stop OR soft-warn case). `null` for `sufficient` / `unknown` / `skipped`. |

**One existing field gets a new enum value** (additive, semver-minor):

- `status`: new value `halted_diagnosability` — set when the Wave 1.6 hard-stop fires. Downstream consumers that switch on `status ∈ {success, partial, failed}` will hit a default branch; the migration is to add `halted_diagnosability` to their switch (or treat unknown statuses as a soft-fail, which is the documented contract).

**Backwards-compat statement**: Downstream consumers of the Output Contract — Tier 3 task-builder (Wave 6), fleet auto-apply wrappers, telemetry — that read only the existing 13 fields are **unaffected**. They will see `null` in the new fields (or the unfamiliar `status` value, which is documented as a soft-fail-equivalent for the auto-apply path: any unrecognized status MUST inhibit auto-apply, which is already the safe default).

## Tasklist Artifact Format

`<output-dir>/diagnosability-tasklist.md` is **not an MDTM file** (that's task-builder's job in Wave 6). It is a structured **proposal** that a downstream `task-builder` invocation can consume verbatim, OR that a user can act on directly.

Position on Open Question #3: **emit the tasklist artifact in Wave 1.6** (parallel to other Wave artifacts, mirroring `doc-context.md`). **Do NOT** auto-hand-off to `task-builder` — that breaks the "no auto-execution" constraint and couples Wave 1.6 to Wave 6's contract. A new flag `--diagnosability-handoff` is out-of-scope for v1 (revisit if user feedback warrants).

**Template** (defer per-framework log-call examples to devops variant):

```markdown
# Diagnosability Tasklist

**Generated**: <ISO 8601>
**Wave**: 1.6
**Verdict**: insufficient | partial
**Complexity**: trivial | non-trivial
**Hard-stop fired**: <bool>
**Symptom**: <2-3 sentence summary from Wave 0 + Wave 1>

## Why instrumentation first

<1-paragraph rationale tied to the sufficiency-rubric Step 1 signals — names which W's of the symptom the existing logging cannot answer>

## Proposed instrumentation tasks

<For each task, a structured atom>:

### Task 1: <one-line title, e.g., "Add structured entry/exit logging around `process_batch`">

- **File**: `<repo-relative path>`
- **Insertion point**: `<file:line>` (after line N, before line M)
- **Log framework**: `<detected from Branch E, e.g., structlog | std logging | loguru | n/a — file currently has no logger>`
- **Level**: `INFO` | `DEBUG` | `WARNING` | `ERROR`
- **Suggested fields**: `<list, e.g., request_id, batch_size, latency_ms, retry_count>`
- **Scope**: `<entry-exit | exception-handler | state-change | timing | n/a>`
- **Rationale**: <one-line tie-back to which W this addresses>

### Task 2: ...

## Verification

After instrumenting, re-run the reproducer and check that the log captures:

- [ ] When (timestamp + context)
- [ ] Where (file:line + function)
- [ ] Why (state at the moment of symptom)

Then re-run `/sc:troubleshoot` with `--skip-diagnosability-audit` (per-issue skip) OR include the new log excerpts in the issue description.
```

**Actionability bar** (Open Question #8): **medium-high specificity** — file + insertion line + framework + level + suggested fields. We do NOT require the rubric to understand the local data model (no "infer that the fields should be `{request_id, attempt}`"). The "suggested fields" come from Branch D's inventory of *existing* nearby logger fields, extended with Wave 0 symptom-derived hints (e.g., "user said 'after retries'" → suggest `retry_count`). If Branch D found zero adjacent logger fields, the suggested fields fall back to a generic `{timestamp, function_name, args, return_value, exception}` set. **Concrete enough for `task-builder` to consume without further design; not so over-specified that Wave 1.6's token budget blows past 2.5k.**

## Off-Ramp UX

**Chat-surface message** (rendered immediately after Wave 1.6 emits the hard-stop, before Wave 5 synthesis):

```
Wave 1.6 Diagnosability Audit — HALT

The reported symptom looks non-trivial (signals: <list of 2-3 firing signals>), and the existing
instrumentation around the symptom site is insufficient to triangulate it: <1-line specific gap>.

Hypothesizing harder against blind code at this point produces low-confidence answers. The protocol
will halt the deep-debugging pipeline and emit an instrumentation tasklist instead.

  Diagnosability Audit Card:  <abs path>
  Instrumentation Tasklist:   <abs path>
  Diagnostic REPORT.md:       <abs path>

Next steps:
  1. Review the tasklist and instrument (or invoke task-builder against it):
       /task <tasklist-path>
  2. Re-run /sc:troubleshoot once new log evidence exists.
  3. To override and proceed with deep debugging anyway, re-run with:
       /sc:troubleshoot --no-diagnosability-audit <original args>
```

**REPORT.md `Next Steps` section additions** (for the hard-stop case, replacing the standard tier-1 / tier-2 next-steps lines at SKILL.md:340):

```markdown
## Next Steps

1. **Instrument first**: review `diagnosability-tasklist.md` and apply the proposed logging atoms (manually, or via `/task <tasklist-path>` to drive a task-builder pass).
2. **Re-run with evidence**: once the new logs have captured the symptom, re-run `/sc:troubleshoot` with the log excerpt in the issue description, OR pass `--skip-diagnosability-audit` per-issue.
3. **Override (use with caution)**: if you accept the lower-confidence diagnosis risk, re-run with `--no-diagnosability-audit` to force the deep-debugging pipeline to proceed against the current evidence.
```

**REPORT.md `Diagnosability Context` section** (always rendered when Wave 1.6 ran, mirroring the Documentation Context section pattern at SKILL.md:334):

```markdown
## Diagnosability Context

**Verdict**: <sufficient | partial | insufficient | unknown>
**Complexity classification**: <trivial | non-trivial>

<≤ 6-line summary of the Diagnosability Audit Card. Names the existing instrumentation in 1 line, names the gap in 1 line, names the implication for the diagnosis confidence in 1 line. If verdict is `sufficient`, the summary may be 2 lines noting the stack trace / inventory carries the signal.>

(Full card: `<abs path to diagnosability-audit.md>`)
```

When `--no-diagnosability-audit` was set, omit this section entirely AND add to Grounding Gaps: `Diagnosability audit skipped by --no-diagnosability-audit — diagnosis confidence is not weighted against existing logging coverage.` (Symmetric to the Wave 1.5 skip handling at SKILL.md:342.)

**Position on Open Question #4 (interaction with `--depth deep`)**: `--depth deep` does NOT force the hard-stop. The user invoking `--depth deep` is asserting "I want thoroughness against the available evidence" — Wave 1.6 can soft-warn but the hard-stop is reserved for the "no evidence to be thorough against" case, and `--depth deep` does not change that. Architect rationale: `--depth deep` interacts with Wave 2's escalation (forces Tier 2), not with Wave 1.6's evidence-availability check; conflating them couples two orthogonal axes.

**Position on Open Question #5 (interaction with `--no-escalate`)**: `--no-escalate` **DOES** suppress the hard-stop. Rationale: `--no-escalate` is the user's explicit "give me a Tier 1 best-effort answer" assertion (SKILL.md:216). The hard-stop is itself a kind of escalation ("go instrument first") — suppressing escalation must suppress it consistently. We surface the would-have-halted verdict in the Diagnosability Context section + Grounding Gaps, so the user retains the signal without being blocked. Architect rationale: opt-out symmetry. The user has one global "don't escalate" lever; honoring it consistently is the systems-design hygiene play.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **R1: Branch D auggie query misses non-obvious logger patterns** (e.g., custom log decorator, AOP-style log injection, framework-specific `@log_call` decorators) | Medium | Causes false `insufficient` verdict → unnecessary hard-stop → user friction | Branch D query template includes "and any decorator or wrapper that injects logging into the call site"; Branch E inventories detected log frameworks so the synthesis knows whether to widen the search; **fallback `unknown` verdict (per the no-silent-downgrade constraint) when Branch D `degraded: true`**. |
| **R2: Complexity gate misclassifies a trivial issue as non-trivial** → unnecessary hard-stop on a fast bug | Medium | One round-trip of user friction | The 2-of-6-signals threshold is tunable; the soft-warn fallback exists for `insufficient + trivial`; users can force-through with `--no-diagnosability-audit`; explicit override path in the chat-surface message. |
| **R3: Tasklist staleness — user re-runs `/sc:troubleshoot` months after the codebase has moved on** | Low-medium | Tasklist proposes instrumentation in moved/renamed code | Tasklist file:line targets are validated at re-run entry via a lightweight Read check on the cited line; if the cited line content has changed, the tasklist is marked stale and Wave 1.6 re-emits. (This is a downstream concern — flagged for v1.1; v1 just emits with timestamp.) |
| **R4: Coupling Wave 1.6 to specific log frameworks** (e.g., the v1 recognizers handle Python + JS but not Go/Java/Rust) | Medium | Wave 1.6 returns `unknown` on Go/Java codebases → soft-warn → no harm but no value either | Devops variant defines the v1 framework matrix; Branch E schema explicitly returns `framework: unknown` when no recognizer matches; the rubric's `unknown` verdict path is the safe default. |
| **R5: Hard-stop creates a "ratchet" — once Wave 1.6 halts, user feels they MUST instrument before progressing** | Low | UX friction; user perceives the tool as bossy | Explicit `--no-diagnosability-audit` override path is documented in EVERY hard-stop chat message; the soft-warn case (`insufficient + trivial`) is the primary path for cases the user wants to push through; off-ramp UX explicitly names "if you accept the lower-confidence risk" — preserves user agency. |

## Ref-File Changes

**New ref**: `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` (canonical structural twin of `refs/doc-discovery.md`). Contains:

- **Section 1**: Auggie + serena query templates for Branches D, E, F (3 sub-sections; placeholders `<symptom_site>`, `<scope>`, `<component_paths>` filled by Wave 1.6 orchestrator).
- **Section 2**: Per-branch structured-output schemas (D, E, F — JSON-ish per Wave 1.5 ref Section 3 style).
- **Section 3**: Sufficiency rubric table (the Step 1 + Step 2 short-circuits from this variant).
- **Section 4**: Complexity gate signal extraction (the 6-signal table from this variant + the 2-of-6 + intermittent + security override rule).
- **Section 5**: Diagnosability Audit Card template (4 fixed sections, mirroring the doc-discovery Section 4 template).
- **Section 6**: Tasklist template (the template from this variant's "Tasklist Artifact Format" section).

Defer per-framework recognizer catalogue (Section 1's *contents* for log-framework patterns) to devops variant for adoption into Section 1.

**Modified ref**: `refs/hypothesis-card-template.md` — add a single line under the `## Grounding gaps` section explaining how to reference the Diagnosability Audit Card when the audit identified gaps that the hypothesis is acknowledging:

```markdown
If Wave 1.6 emitted a Diagnosability Audit Card with `verdict ∈ {partial, insufficient}`, reference
it here (e.g., "Diagnosability verdict: partial — see <audit-card-path>; coverage of 'why' is missing,
so this hypothesis cannot be falsified at runtime without the proposed instrumentation").
```

**Modified ref**: `refs/escalation-rubric.md` — append a new short section `## Diagnosability interaction` (≤15 lines) noting that Wave 1.6's complexity gate reuses the structural dimensions from this rubric (multi-domain, intermittent, security_caution) but does NOT consume the calibrated confidence (which fires after Wave 1.7). This is a *forward reference* documenting the coupling, not a new behavioral rule.

**Modified ref**: `refs/report-template.md` — add the `## Diagnosability Context` section template (rendered when Wave 1.6 ran) and the `Next Steps` variant for the hard-stop case. (Exact diff in this variant's "Off-Ramp UX" section above.)

**Unchanged refs**: `refs/triage-checklist.md`, `refs/doc-discovery.md`, `refs/remediation-handoff.md`, `refs/hypothesis-card-template.md` (other than the one-line addition).

## SKILL.md Diff Sketch

| Section | Current line range | Change |
|---------|-------------------|--------|
| Wave Structure ASCII | 75-85 | Insert `Wave 1.6: Diagnosability Audit ← always; loads refs/diagnosability-audit.md on demand; skipped only by --no-diagnosability-audit; may hard-stop to Wave 5` between current Wave 1.5 and Wave 1.7 lines. Add the hard-stop edge documentation: `Wave 1.6 hard-stop edge: → Wave 5 (skip Waves 1.7-4)`. |
| Output Contract table | 41-57 | Add 3 new rows for `diagnosability_verdict`, `diagnosability_audit_card_path`, `diagnosability_tasklist_path`. Update the `status` row's enum to include `halted_diagnosability`. |
| Wave 1.5 Exit criteria | 170-174 | No change to Wave 1.5 itself; Wave 1.6 entry takes over from Wave 1.5 exit. |
| New section: `### Wave 1.6: Diagnosability Audit` | insert after current line 187 | New ~60-line section mirroring the Wave 1.5 structure (Goal / Preconditions / Steps / Exit criteria / Failure handling table / Token budget). Template per this variant's "Wave 1.6 Placement & Entry/Exit Criteria" section. |
| Wave 1.7 Preconditions | 194-196 | Update to mention Wave 1.6 ran (or was skipped via `--no-diagnosability-audit`). Add: `Wave 1.6 did NOT fire its hard-stop (verdict ≠ insufficient + non-trivial).` |
| Wave 5 step 2 (REPORT.md composition) | 331-342 | Add `Diagnosability Context` to the list of sections to compose (after `Documentation Context`, before `Diagnosis`). Add the `halted_diagnosability` rendering path: when status=halted_diagnosability, replace the Diagnosis section with a "Halted — instrumentation required" prose block referencing the tasklist. |
| Tool Coordination Summary | 391-403 | Add a Wave 1.6 column or annotate Tier 1 column. Add row entries indicating `mcp__auggie__codebase-retrieval` ✓ (1 query in Branch D), `Glob`/`Grep` ✓ (Branch E config inventory), `Task` ✓ (3 parallel branches + 1 synthesis). |
| Will Do / Will Not Do | 404-425 | Add to Will Do: "Run Wave 1.6 Diagnosability Audit by default; opt-out via `--no-diagnosability-audit`. Halt Wave 1.7-4 when the audit verdict is `insufficient` AND complexity is non-trivial AND `--no-escalate` is not set." Add to Will Not Do: "Auto-apply the diagnosability tasklist (it is a proposal, not an execution). Force the hard-stop when `--no-escalate` is set." |
| Token Cost Profile table | 446-454 | Add Wave 1.6 line: `+0.5-1k auggie, +1-2.5k Claude, +30-60s wall clock`. Hard-stop case yields a net token *saving* (skip Waves 1.7-4) — note this explicitly. |
| Error Handling table | 428-444 | Add 4 new rows: `--no-diagnosability-audit set` (skip + null pointer + Grounding Gap line); auggie unavailable in Wave 1.6 (Glob/Grep fallback, mark `degraded`); All three branches return empty (write card with "None found", verdict `unknown`, continue to 1.7); Branch synthesis times out (mark missing section, do not block 1.7). |
| Refs table | 458-466 | Add row: `refs/diagnosability-audit.md` — `Wave 1.6 (audit query templates, schemas, sufficiency rubric, complexity gate, audit card template, tasklist template)`. |

## Persona-Distinctive Claims

These are the architect-perspective claims I expect to defend in debate against the analyzer and devops variants:

1. **"Structural twin of Wave 1.5 wins over anything else."** Any variant that proposes a single-agent audit, a different schema family, or a non-symmetric opt-out flag (e.g., `--audit-coverage` instead of `--no-diagnosability-audit`) violates the principle of least surprise for protocol maintainers and breaks the established Wave 1.5 fan-out precedent. *Defensible because the protocol already pays a "Wave 1.5/1.7 split tax" (per seed brief §Constraints) — adding Wave 1.6 in the same shape costs zero new tax; adding it in a different shape doubles the maintenance burden.* **If I'm wrong it's because** the single-agent shape's token-budget win outweighs the structural-symmetry win — but the seed brief's ≤2-3k Claude budget for Wave 1.6 is already met by the 3-branch shape per the budgets I've itemized.

2. **"Reuse the escalation rubric, don't invent a new complexity score."** Option (b) from Open Question #1 (purpose-built score) and option (c) (defer to Wave 1.7) both add classification surfaces. Option (a) makes Wave 1.6 a consumer of the same complexity signals downstream waves consume — one rubric, one source of truth, one place to tune. *Defensible because the escalation rubric's structural dimensions (multi-domain, intermittent, security) are derivable from Wave 0 + Wave 1 without running a hypothesis — no circular dependency.* **If I'm wrong it's because** the post-hypothesis calibration in the rubric is so entangled with the structural dimensions that they can't be cleanly extracted — but the rubric already names them as separate at `refs/escalation-rubric.md:64-69` (signal-driven escalation reasons).

3. **"Output Contract additions are 3 fields + 1 enum-extension, full stop."** The analyzer variant may propose richer fields (e.g., per-branch verdicts, per-task confidence scores in the Output Contract); the devops variant may propose log-framework-specific fields. Both bloat the contract. The architect position: anything per-branch lives in the Diagnosability Audit Card (the synthesised artifact, just like the Documentation Context Card). The Output Contract gets only the verdict, the card path, the tasklist path. *Defensible because the existing contract already follows this discipline — `doc_context_card_path` is the only Wave 1.5 field, with all per-branch detail inside the card.* **If I'm wrong it's because** downstream telemetry needs structured per-branch fields for analytics — but telemetry can parse the card; the contract is for control flow.

4. **`--no-escalate` SHOULD suppress the hard-stop; `--depth deep` should NOT force it.** These are the only two flag-interaction positions where the analyzer (more conservative) and devops (more aggressive) variants likely differ from each other. The architect position threads the needle on systems-design grounds: `--no-escalate` is the user's global opt-out for any "escalation-style" detour, and the hard-stop IS an escalation in spirit; `--depth deep` is orthogonal — it forces *post-hypothesis* deep work, not *pre-hypothesis* instrumentation. **If I'm wrong it's because** users mentally bundle "deep" with "instrument first" — but that's a UX education problem solvable with one CHANGELOG line, not an architectural decision.

5. **"Tasklist lives in `<output-dir>/`, not handed off to task-builder by default."** Open Question #3 admits 3 options; the architect picks "in output-dir, parallel to other Wave artifacts," explicitly rejecting the auto-handoff. The handoff coupling violates the "no auto-execution" constraint, and a v1 hand-off to `task-builder` would couple Wave 1.6 to Wave 6's MDTM contract (which evolves on its own cadence). The architect position is "the file is the contract; the consumer can be a human, a task-builder invocation, or a future automation — keep them decoupled." *Defensible because Wave 6 already has its own preconditions (REPORT.md `success` status, user accept) — having a parallel Wave 1.6 → task-builder edge with different gates fragments the remediation pipeline.* **If I'm wrong it's because** a `--diagnosability-handoff` flag is so cheap that withholding it is bureaucratic — but the seed brief explicitly invites this as a follow-up flag, not a v1 requirement, and the architect job is to defend "ship the smallest correct thing first."
