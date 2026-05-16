# task-builder Adjacent Surface — Definition vs Execution Routing

**Task:** T03.03 — Analyze `task-builder` adjacent surface
**Roadmap Item:** R-010
**Generated:** 2026-05-15
**Tier:** EXEMPT (read-only analysis)

## Purpose

Define which classes of donor feature (from `/sc:task`) affect work-*definition*
— and therefore route to the `task-builder` skill — versus work-*execution*,
which route to the `/task` executor. The Phase 4 adversarial debate uses this
routing rule to send each donor feature to exactly one surface, so a feature
that shapes *what work is defined* cannot accidentally land inside the F1 loop
and violate INV-05 (refusal-of-definition).

## Source of Truth (R-RULE-10)

Both adjacent skills are single-file skills. Source-of-truth lives in
`src/superclaude/`; `.claude/` copies are byte-identical mirrors produced by
`make sync-dev`.

| Skill | `src/` (canonical) | `.claude/` (dev copy) |
|---|---|---|
| `task-builder` | `src/superclaude/skills/task-builder/SKILL.md` (1709 lines) | `.claude/skills/task-builder/SKILL.md` (byte-identical, verified via `diff`) |
| `task` (executor) | `src/superclaude/skills/task/SKILL.md` (376 lines) | `.claude/skills/task/SKILL.md` (byte-identical, verified via `diff`) |

All `file:line` evidence below cites `src/superclaude/skills/...`; the
`.claude/` mirrors resolve identically.

---

## Section 1 — Builder Responsibilities (Evidence)

The builder owns the *definition* of work: it produces an MDTM task file
ready for the executor, plus the research and QA artifacts that justify it.
Below are its load-bearing responsibilities with side-tagged `file:line`
evidence.

### 1.1 Builder Output: an MDTM Task File + Research/QA Trail

> "Creates MDTM task files by researching the actual codebase with parallel
> agents, running quality gates, and spawning the `rf-task-builder` agent to
> produce a validated, ready-to-execute task file."
> — `src/superclaude/skills/task-builder/SKILL.md:8` (`src/`)

> "This skill stops after task file creation. There is no Stage B — the user
> reviews the task file and executes it with `/task [path]` when ready."
> — `src/superclaude/skills/task-builder/SKILL.md:12` (`src/`)

**Owned artifacts** — `src/superclaude/skills/task-builder/SKILL.md:120-129`
(`src/`):

| Artifact | Owner | Location |
|---|---|---|
| **MDTM task file** | builder | `${TASK_DIR}${TASK_ID}.md` |
| Research notes (scope discovery) | builder | `${TASK_DIR}research-notes.md` |
| Codebase research files (parallel researchers) | builder | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files (optional) | builder | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Analyst completeness report | builder | `${TASK_DIR}qa/analyst-completeness-report.md` |
| Research-gate QA report | builder | `${TASK_DIR}qa/qa-research-gate-report.md` |
| Task structural QA report | builder | `${TASK_DIR}qa/qa-task-validation-report.md` |
| Task qualitative QA report | builder | `${TASK_DIR}qa/qa-qualitative-review.md` |

Everything in this table is produced *before* execution begins; none of these
artifacts is touched by the F1 loop.

### 1.2 MDTM Structure the Builder Owns

The builder is the sole authority over:

- **Template selection** — Template 01 (generic) vs Template 02 (complex),
  decided in Stage A.6 and embedded in `BUILD_REQUEST: TEMPLATE`.
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:375-391` and
  `src/superclaude/skills/task-builder/SKILL.md:731-733` (`src/`).
- **Granularity** — per-file / per-component checklist items per template
  rules A3 (Complete Granular Breakdown) and A4 (Iterative Process Structure).
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:428-433` and
  `src/superclaude/skills/task-builder/SKILL.md:788-794` (`src/`).
- **`QA_GATE_REQUIREMENTS`** — `NONE` / `FINAL_ONLY` / `PER_PHASE` —
  determines what phase-gate items the *task file* will contain (the
  executor merely runs whatever gate items it finds).
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:735-743` (`src/`).
- **`VALIDATION_REQUIREMENTS`** — which lint / type-check / build commands
  the generated checklist items must include.
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:744-749` (`src/`).
- **`TESTING_REQUIREMENTS`** — `NONE` / `UNIT` / `INTEGRATION` / `E2E` /
  `ALL` — what test items must appear.
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:750-756` (`src/`).
- **B2 self-contained item embedding** — each checklist item embeds its
  full agent prompt, context references, action steps, output paths, and
  verification criteria. The executor pulls these verbatim.
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:900-902` (`src/`),
  and on the executor side `src/superclaude/skills/task/SKILL.md:301-302`
  (`src/`).
- **Frontmatter, phases, dependencies** — initial frontmatter, phase
  decomposition, inter-phase dependencies are all authored by the builder;
  the executor only updates the four lifecycle fields per F5.
  Evidence: `src/superclaude/skills/task-builder/SKILL.md:823-833` (`src/`)
  for builder-side authoring; `src/superclaude/skills/task/SKILL.md:159-168`
  (`src/`) for the executor's allowed frontmatter edits.

### 1.3 Builder/Executor Boundary (Evidence on Both Sides)

The boundary is stated symmetrically on both skills.

**Builder side — Stage A is the only stage; execution is out of scope:**

> "This skill operates in a single stage (Stage A only). Unlike the
> canonical document skills which have Stage A (create task file) +
> Stage B (delegate to `/task` for execution), this skill stops after
> task file creation. The user reviews the task file and executes it
> with `/task [path]` when ready."
> — `src/superclaude/skills/task-builder/SKILL.md:139-141` (`src/`)

> "TO EXECUTE: /task ${TASK_DIR}${TASK_ID}.md"
> — `src/superclaude/skills/task-builder/SKILL.md:1035-1036` (`src/`)

**Executor side — definition is explicitly refused:**

> "What this skill does NOT do: It does not create task files (use
> `rf:task-builder` for that), does not define what work to do (the
> task file defines that), and does not prescribe which agents to use
> (the task file's B2 self-contained items embed all context, actions,
> and agent prompts). This skill is the disciplined loop that ensures
> every item gets executed completely, in order, with evidence of
> completion."
> — `src/superclaude/skills/task/SKILL.md:12` (`src/`)

> "Execute items as written. Do not reinterpret, abbreviate, or
> 'improve' checklist items. They were authored with specific context
> references, action steps, output paths, and verification criteria for
> a reason."
> — `src/superclaude/skills/task/SKILL.md:333` (`src/`, Critical Rule 4)

> "Modifying items — Do not rewrite, rephrase, or reinterpret checklist
> items. Execute them as written. ... Adding items — Do not add new
> checklist items unless the task file contains DYNAMIC CONTENT MARKER
> sections that explicitly permit it."
> — `src/superclaude/skills/task/SKILL.md:113-114` (`src/`, F2)

### 1.4 The Skill vs the Agent (Two Builder Surfaces)

The `task-builder` namespace has *two* invocation surfaces — both produce
task files (definition), neither runs the F1 loop:

> "This skill is invoked directly by users via `/task-builder [request]`.
> Other document-producing skills (tech-reference, prd, tdd,
> operational-guide, repo-cleanup, readme) spawn the `rf-task-builder`
> **agent** via the Agent tool during their Stage A — they use the
> agent definition at `.claude/agents/rf-task-builder.md`, not this
> skill. The agent and the skill share the same builder logic but
> operate in different contexts: the agent receives a BUILD_REQUEST
> from the orchestrating skill, while this skill IS the orchestrator."
> — `src/superclaude/skills/task-builder/SKILL.md:82` (`src/`)

Routing implication: a donor feature that affects what the builder
*produces* must route to the builder regardless of whether the entry
point is the user-facing `/task-builder` skill or the `rf-task-builder`
agent invoked by another skill. Both are definition surfaces.

---

## Section 2 — The Definition-vs-Execution Routing Rule

### 2.1 The Rule (Unambiguous, Single-Sentence Form)

> **Routing Rule (R-RULE-10/INV-05):**
> A donor feature routes to **`task-builder`** if and only if it
> changes *what* an MDTM task file will contain — its template,
> granularity, items, gates, frontmatter, dependencies, or required
> verification criteria — *as authored before execution begins*.
> A donor feature routes to **`/task` executor** if and only if it
> changes *how* an existing MDTM task file is processed at runtime
> by the F1 loop — its READ, IDENTIFY, EXECUTE, UPDATE, or REPEAT
> steps, or the gates and policies that fire between phases and at
> end-of-task.
> Any donor feature that would require the executor to *decide* the
> shape of work (template, granularity, gating policy, testing
> requirement, persona, allowed-tools, etc.) at runtime — rather than
> reading those decisions from the authored task file — is a
> routing-error candidate for `task-builder` and **must not** be
> attached to the executor.

### 2.2 Diagnostic Questions (How to Apply the Rule)

For any candidate donor feature, ask these in order:

1. **Does the feature affect the *generation* of a task file?**
   If yes (e.g., template selection, item granularity, embedded
   gates, allowed-tools listing, persona auto-activation embedded
   in items, testing requirements selection) → route to
   `task-builder`. Stop.
2. **Does the feature affect the *runtime processing* of an
   *already-authored* task file?**
   If yes (e.g., new parallelization heuristic, new phase-gate QA
   policy, new error-handling path, new subagent dispatcher mode,
   new resumption strategy, new incremental-writing rule) → route
   to the `/task` executor. Stop.
3. **Does the feature *appear* to be execution but actually requires
   the executor to read intent that isn't in the task file?**
   If yes → it is a definition feature in disguise. Route to
   `task-builder` (the authored task file must carry the intent so
   the executor merely runs it). **This is the failure case INV-05
   protects against** — see §3.

### 2.3 Worked Examples — Routing of `/sc:task` Donor Features

The eight `/sc:task` features inventoried in
`.dev/releases/current/task-sc-task-directional-merge/artifacts/donor-feature-catalog.md`
route as follows. These resolutions are illustrative — Phase 4's
adversarial debate is still authoritative — but the rule is
deterministic enough to anchor that debate.

| Donor feature | Shapes *what* or *how*? | Surface | Reasoning |
|---|---|---|---|
| **Tier classification** (STRICT/STANDARD/LIGHT/EXEMPT) | What — selects the *gating shape* baked into the task file | `task-builder` | A tier determines which validation/QA gate items the task file must contain; once baked in, the executor runs them blindly. Routing to executor would require runtime tier inference, leaking definition into execution. |
| **Classification header emission** | What — adds a frontmatter / header block to the task file | `task-builder` | Header content is task-file metadata authored once; the executor only reads it. |
| **TFEP** (Test Failure Escalation Protocol) | How — runtime branching after a test failure | `/task` executor | Triggered inside EXECUTE / error-handling at runtime; the task file references the protocol but execution decides escalation path. |
| **Per-tier flow branching** | What — different *phase shapes* per tier | `task-builder` | The branching is realized as different phase layouts in the authored task file; the executor's loop is tier-agnostic. |
| **MCP server declarations** | What — declared per-item in the task file | `task-builder` | MCP requirements belong in checklist-item B2 context blocks; the executor passes prompts verbatim. |
| **Persona auto-activation** | What — embedded in item prompts | `task-builder` | Persona selection is a property of the *authored* item; the executor must not re-infer persona at runtime. |
| **Allowed-tools declarations** | What — declared as item-level metadata | `task-builder` | Tool allowances are part of item context; the executor obeys what is written. |
| **Compliance gating** | Mixed — definition surface for *which* gates exist, execution surface for *firing* them | `task-builder` (gate authoring) + `/task` executor (gate-firing mechanism, only if a gate-firing capability is missing) | Authoring which compliance gates exist is definition; the actual fire-and-pass mechanics already live in `/task`'s phase-gate QA (extension point #10). If the donor adds new gate-firing semantics, that portion routes to executor. |

For features that span both surfaces (the last row above), the routing
rule applies *per slice*: the authoring slice routes to `task-builder`;
the runtime slice routes to `/task`. They are debated independently in
Phase 4.

### 2.4 Anti-Patterns the Rule Refuses

The rule explicitly refuses three classes of attempted attachment:

1. **Runtime template selection** — A donor that asks the executor to
   pick Template 01 vs 02 at runtime based on inspection of items.
   *Refused:* template selection is a builder responsibility
   (§1.2); the executor sees only the result.
2. **Runtime granularity rewriting** — A donor that asks the executor
   to split or merge checklist items based on observed scope.
   *Refused:* F2 prohibits modifying items
   (`src/superclaude/skills/task/SKILL.md:113` `src/`); item
   granularity is fixed by the builder.
3. **Runtime gate-policy inference** — A donor that asks the executor
   to decide whether a phase needs a QA gate based on item content.
   *Refused:* `QA_GATE_REQUIREMENTS` is a `BUILD_REQUEST` field
   (`src/superclaude/skills/task-builder/SKILL.md:735-743` `src/`); the
   executor runs whichever gate items the authored task file contains.

---

## Section 3 — INV-05 Cross-Reference (Refusal-of-Definition)

### 3.1 INV-05 (from the Sprint Specification)

> **INV-05** — Refusal-of-definition — `/task` does not decide
> *what* to do; the MDTM file does. The F1 loop only *executes*.
> — `.dev/releases/current/task-sc-task-directional-merge/task-sc-task-directional-merge/prompt.md:48`
> and `.dev/releases/current/task-sc-task-directional-merge/tasklist-index.md:59`

### 3.2 Why the Routing Rule and INV-05 Are the Same Constraint

INV-05 says the F1 loop must not decide work shape; the routing rule
says definition features must route to `task-builder` not `/task`. These
are two phrasings of the same constraint: **definition features that
slip into the executor force the F1 loop to decide work shape, which is
exactly the failure mode INV-05 prevents.**

Enforcement evidence on the executor side (the same lines cited in
T03.01 / T03.02 for the INV-05 bound):

- `src/superclaude/skills/task/SKILL.md:12` (`src/`) — "does not define
  what work to do (the task file defines that)".
- `src/superclaude/skills/task/SKILL.md:113-114` (`src/`, F2) —
  "Modifying items ... Adding items".
- `src/superclaude/skills/task/SKILL.md:333` (`src/`, Critical Rule 4)
  — "Execute items as written. Do not reinterpret, abbreviate, or
  'improve' checklist items."
- `src/superclaude/skills/task/SKILL.md:349` (`src/`, Critical Rule 12)
  — "The F1 loop is non-delegable" (and by extension, undecorable with
  definition logic).

### 3.3 What Happens When the Rule Is Violated (Failure Mode)

If a definition feature is mis-attached to the executor:

1. The authored task file no longer fully describes the work — it
   leaves a definition decision unspecified.
2. The executor, forced to make that decision at runtime, must
   *interpret* item content (banned by Critical Rule 4) or
   *modify/add* items (banned by F2).
3. The on-disk task file ceases to be the single source of truth —
   the same task file processed in two sessions can produce different
   work because the executor's runtime inference differs.
4. INV-04 (resumability from disk) is collaterally broken because
   resume state now depends on runtime decisions not captured on disk.

The routing rule blocks (1) by sending the feature to `task-builder`
instead, so the decision is baked into the task file before execution
begins, and the executor remains a pure loop.

### 3.4 Routing-Error Detection Heuristic

A debate that proposes attaching a feature to a `/task` extension point
should be checked against this signal: *does the proposed integration
require the executor to read item content and decide something about
it that the authored task file does not already specify?* If yes, the
proposal violates INV-05 and the feature must be re-routed (in whole
or per-slice) to `task-builder`.

---

## Section 4 — Routing Outputs for Phase 4

For each donor feature, Phase 4 debates must produce one of three
routing tags:

- **BUILDER** — feature routes to `task-builder` (definition surface).
  Debate occurs against builder Stage A.x extension points (template
  triage, BUILD_REQUEST fields, item-granularity rules, QA gates
  embedded in generated tasks).
- **EXECUTOR** — feature routes to `/task` executor (execution
  surface). Debate occurs against the extension points enumerated in
  `recipient-extension-points.md` and constrained by
  `extension-point-contracts.md`.
- **SPLIT** — feature has both an authoring slice and a runtime slice.
  Each slice is debated independently; the slice's verdict applies
  only to its slice.

A feature routed to BUILDER but evaluated only against `/task`
extension points should be flagged as a routing error before scoring
in Phase 4. A feature routed to SPLIT but missing a per-slice
evaluation is also flagged.

---

## Acceptance Criteria Coverage

| Acceptance criterion | Where satisfied |
|---|---|
| Builder responsibilities documented with side-tagged `file:line` evidence | §1.1, §1.2, §1.3, §1.4 |
| Unambiguous definition-vs-execution routing rule stated | §2.1 |
| Routing rule cross-references INV-05 | §3.1, §3.2, §3.3 |

## Validation

A sample donor feature resolves to exactly one surface (or one
slice-per-surface for SPLIT) using §2.2's three diagnostic questions
applied in order. The eight `/sc:task` features in §2.3 are pre-resolved
as a worked example; the same procedure applies to any future donor.
